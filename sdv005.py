import tkinter as tk
import pydicom, os
import numpy as np
from PIL import Image, ImageTk
from tkinter import filedialog, ttk
from glob import glob

class SimpleDicomViewer:
    def __init__(self, root):
        '''
        Title: SimpleDicomViewer
        init function-
        root
        L___menubar                             |
        L___frame(grid) canvas in frame         |
            L____pre_btn --- slider --- nxt_btn |
        '''
        self.root = root
        self.root.title("Simple DICOM Viewer")
        self.create_menu()
        #----frame----#
        self.frame = tk.Frame(self.root)
        self.frame.grid(row=0, column=0, columnspan=3)
        #----canvas----#
        self.canvas = tk.Canvas(self.frame, bg="white", width=512, height=768)
        self.canvas.grid(row=0, column=0, columnspan=3)
        #----scrollbar_vertical---#
        self.scrollbar_vertical = ttk.Scrollbar(self.frame, orient="vertical", command=self.canvas.yview)
        self.scrollbar_vertical.grid(row=0,column=3, sticky="sn")
        self.canvas.configure(yscrollcommand=self.scrollbar_vertical.set)
        #----scrollbar_horizontal----#
        self.scrollbar_horizontal = ttk.Scrollbar(self.frame, orient="horizontal", command=self.canvas.xview)
        self.scrollbar_horizontal.grid(row=1,column=0, columnspan=3, sticky="ew")
        self.canvas.configure(xscrollcommand=self.scrollbar_horizontal.set)
        #----button---#
        self.prev_button = tk.Button(self.frame, text="PREV", width=7, command=self.show_previous_image)
        self.prev_button.grid(row=2, column=0)
        #----slider init----#
        self.slider = tk.Scale(self.frame, from_=0, to=0, orient=tk.HORIZONTAL, length=200, command=self.update_image_index)
        self.slider.grid(row=2, column=1)
        #----slider----#
        #----button----#
        self.next_button = tk.Button(self.frame, text="NEXT", width=7, command=self.show_next_image)
        self.next_button.grid(row=2,column=2)
        #----button----#
        self.root.resizable(False, False)
        #----global variables-----#
        self.image_index = 0
        self.images = []
        self.converted_images = []
        self.file_objects = []
        self.photo_image = None
        self.var = 0
    def create_menu(self):
        #----menubar----#
        self.menubar = tk.Menu(self.root)
        #----menu1----#
        self.menu1 = tk.Menu(self.menubar, tearoff=0)
        #----menu1 submenu----#
        self.menu1_submenu = tk.Menu(self.menu1, tearoff=0)
        self.menu1_submenu.add_command(label="File", command=self.open_dicom_file)
        self.menu1_submenu.add_command(label="Directory", command=self.open_folder)
        #----menu1 submenu----#
        self.menu1.add_cascade(label="Import", menu=self.menu1_submenu)
        self.menu1.add_separator()
        self.menu1.add_command(label="Close", command=self.close)
        #----menu2----#
        self.menu2 = tk.Menu(self.menubar, tearoff=0)
        self.menu2.add_command(label="Invert", command=self.invert)
        #----menu3----#
        self.menu3 = tk.Menu(self.menubar, tearoff=0)
        self.menu3.add_command(label="Info", command=self.show_info_window)
        #----menu4----#
        self.menu4 = tk.Menu(self.menubar, tearoff=0)
        self.menu4.add_command(label="Cont HU", command=self.show_control_HU_window)
        #----menubar----#
        self.menubar.add_cascade(label="File",menu=self.menu1)
        self.menubar.add_cascade(label="View", menu=self.menu2)
        self.menubar.add_cascade(label="ProcWindow", menu=self.menu4)
        self.menubar.add_cascade(label="Help", menu=self.menu3)
        self.root.config(menu=self.menubar)
        #----end of menubar----#
    def open_dicom_file(self):
        '''
        open a dicom file
        '''
        file_path = filedialog.askopenfilename(title="Select DICOM file", filetypes=(("DICOM files", "*.dcm"), ("All files", "*.*")))
        if file_path:
            self.images = self.load_dicom_images(file_path)
            self.show_image()
    def open_folder(self):
        '''
        open dicom files from folder
        '''
        folder_path = filedialog.askdirectory(title="Select Folder")
        if folder_path:
            self.images = self.load_dicom_folder(folder_path)
            self.show_image()    
    def load_dicom_images(self, file_path):
        '''
        load a dicom file
        '''
        try:
            dicom_data = pydicom.dcmread(file_path)
            self.file_objects = [dicom_data]
            temp_images = dicom_data.pixel_array
            if len(np.shape(temp_images)) !=3:
                return np.array([temp_images])
            else:
                return temp_images
        except Exception as e:
            print("Error Loading DICOM file:", e)
            return []
    def load_dicom_folder(self, folder_path):
        '''

        '''
        try:
            self.file_objects = [pydicom.dcmread(elem) for elem in glob(folder_path+"\\*.dcm")]
            self.images = [elem2.pixel_array for elem2 in self.file_objects]
            return self.images
        except Exception as e:
            print("Error Loading DICOM file:", e)
            return []
    def convert_to_image(self, frame):
        tempImg = self.normalize(frame)
        image = Image.fromarray(tempImg)
        return ImageTk.PhotoImage(image)
    def convert_to_CTHU_image(self, frame):
        index = self.image_index
        tempImg = int(self.file_objects[index][0x0028,0x1052].value)*frame+int(self.file_objects[index][0x0028,0x1052].value)
        tempImg = self.normalize(tempImg)
        image = Image.fromarray(tempImg)
        return ImageTk.PhotoImage(image)
    def update_image_index(self, value):
        self.image_index = int(value)
        self.show_image()
    def show_image(self):
        if self.photo_image:
            del self.photo_image
        self.canvas.delete("all")
        temp_image = self.images[self.image_index]
        temp_fObj = self.file_objects[self.image_index]
        if temp_fObj.Modality == "CT":
            temp_image = temp_image*temp_fObj.RescaleSlope+temp_fObj.RescaleIntercept
        self.photo_image = self.convert_to_image(temp_image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo_image)
        self.canvas.config(scrollregion=self.canvas.bbox("all"), confine=True)
        self.prev_button.grid(row=2, column=0)
        # slider part
        self.slider.config(from_=0, to=len(self.images)-1)
        self.slider.set(self.image_index)
        self.slider.grid(row=2, column=1)
        # slider part
        self.next_button.grid(row=2, column=2)
    def normalize(self, input):
        if np.max(input) != 0:
            maxValue = np.max(input)
            minValue = np.min(input)
            return np.array(((input-minValue)/(maxValue-minValue))*255, dtype=np.uint8)
        else:
            return input
    def show_previous_image(self):
        if self.image_index > 0:
            self.image_index -= 1
            self.show_image()
    def show_next_image(self):
        if self.image_index < len(self.images) -1:
            self.image_index +=1
            self.show_image()
    def close(self):
        self.root.quit()
        self.root.destroy()
    def invert(self):
        self.images = [np.max(elem)-elem for elem in self.images]
        self.show_image()
    def show_control_HU_window(self):
        # self.var = tk.IntVar()
        contHU_window=tk.Toplevel(self.root)
        contHU_window.title=("Control windowning of CT")
        contHU_window.geometry("300x200")
        # scale = tk.Scale(contHU_window, variable=self.var, command=self.select, oritent="horizontal", showvalue=False, tickinterval=50, to=500, length=200)
        # scale.pack()
        contHU_window.transient(self.root)
        contHU_window.grab_set()
        self.root.wait_window(contHU_window)
    def select(self):
        value = "value : "+str(tk.scale.get())
        self.label.config(text=value)
    def show_info_window(self):
        info_window = tk.Toplevel(self.root)
        info_window.title("Info")
        info_window.geometry("300x200")
        info_label = tk.Label(info_window, text="Developer: Mark S. Hong\n\nE-mail:sunmark@nate.com")
        info_label.pack(padx=10, pady=10)
        close_button = tk.Button(info_window, text="Close", command=info_window.destroy)
        close_button.pack(padx=10, pady=10)
        info_window.transient(self.root)
        info_window.grab_set()
        self.root.wait_window(info_window)

def main():
    root = tk.Tk()
    app = SimpleDicomViewer(root)
    root.mainloop()

if __name__ == "__main__":
    main()
