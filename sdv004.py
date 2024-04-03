import tkinter as tk
from PIL import Image, ImageTk
import pydicom, os
import numpy as np
from tkinter import filedialog
from glob import glob

class SimpleDicomViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple DICOM Viewer")
        self.menubar = tk.Menu(root)
        #---menu1---#
        self.menu1 = tk.Menu(self.menubar, tearoff=0)
        self.menu1.add_command(label="Open", command=self.open_dicom)
        self.menu1.add_command(label="Open_dir", command=self.open_folder)
        self.menu1.add_command(label="Close", command=self.close)
        #---menu2---#
        self.menu2 = tk.Menu(self.menubar, tearoff=0)
        self.menu2.add_command(label="Invert", command=self.invert)
        #---menu3---#
        self.menu3 = tk.Menu(self.menubar, tearoff=0)
        self.menu3.add_command(label="Info", command=self.show_info_window)
        #---menubar---#
        self.menubar.add_cascade(label="File",menu=self.menu1)
        self.menubar.add_cascade(label="Color", menu=self.menu2)
        self.menubar.add_cascade(label="Help", menu=self.menu3)
        self.root.config(menu=self.menubar)
        self.frame = tk.Frame(self.root)
        self.frame.pack(fill=tk.BOTH, expand=True)
        self.canvas = tk.Canvas(self.frame, bg="white", width=1024, height=1024)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.prev_button = tk.Button(self.frame, text="PREV", width=7, command=self.show_previous_image)
        self.next_button = tk.Button(self.frame, text="NEXT", width=7, command=self.show_next_image)
        self.root.resizable(True, True)
        self.image_index = 0
        self.images = []
        self.photo_image = None
    def open_dicom(self):
        file_path = filedialog.askopenfilename(title="Select DICOM file", filetypes=(("DICOM files", "*.dcm"), ("All files", "*.*")))
        if file_path:
            self.images = self.load_dicom_images(file_path)
            self.show_image()
    def open_folder(self):
        folder_path = filedialog.askdirectory(title="Select Folder")
        if folder_path:
            self.images = self.load_dicom_folder(folder_path)
            self.show_image()    
    def load_dicom_images(self, file_path):
        try:
            dicom_data = pydicom.dcmread(file_path)
            temp_images = dicom_data.pixel_array
            if len(np.shape(temp_images)) !=3:
                return np.array([temp_images])
            else:
                return temp_images
        except Exception as e:
            print("Error Loading DICOM file:", e)
            return []
    def load_dicom_folder(self, folder_path):
        try:
            temp_images = [pydicom.dcmread(elem).pixel_array for elem in glob(folder_path+"\\*.dcm")]
            return np.array(temp_images)
        except Exception as e:
            print("Error Loading DICOM file:", e)
            return []
    def convert_to_image(self, frame):
        tempImg = self.normalize(frame)
        image = Image.fromarray(tempImg)
        return ImageTk.PhotoImage(image)
    def show_image(self):
        if self.photo_image:
            del self.photo_image
        self.canvas.delete("all")
        self.photo_image = self.convert_to_image(self.images[self.image_index])
        self.canvas.config(width=self.photo_image.width(), height=self.photo_image.height())
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo_image)
        self.prev_button.pack(side=tk.LEFT, padx=5)
        self.next_button.pack(side=tk.RIGHT, padx=5)
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
