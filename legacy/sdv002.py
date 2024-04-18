import tkinter as tk
from tkinter import filedialog
import pydicom
from PIL import Image, ImageTk
import numpy as np

class DICOMViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple DICOM Viewer")

        self.frame_count_label = tk.Label(self.root, text="Frames: 0", fg="green")
        self.frame_count_label.grid(row=0, column=1, sticky="ne", padx=10, pady=10)

        self.current_frame_label = tk.Label(self.root, text="Current frame: 0", fg="green")
        self.current_frame_label.grid(row=0, column=0, sticky="nw", padx=10, pady=10)

        self.frame = tk.Frame(self.root)
        self.frame.grid(row=1, column=0, columnspan=2)

        self.canvas = tk.Canvas(self.frame, bg="black", width=512, height=512)
        self.canvas.pack()

        self.open_button = tk.Button(self.frame, text="Open", width=7, command=self.open_dicom)
        self.open_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.prev_button = tk.Button(self.frame, text="Previous", width=7, command=self.show_previous_image)
        self.next_button = tk.Button(self.frame, text="Next", width=7, command=self.show_next_image)
        self.close_button = tk.Button(self.frame, text="Close", width=7, command=root.destroy)

        self.image_index = 0
        self.images = []
        self.photo_image = None

        self.frame_count = 0

        self.update_frame_count_label()

        # Bind key events
        self.root.bind('o', lambda event: self.open_dicom())
        self.root.bind('<Up>', lambda event: self.show_previous_image())
        self.root.bind('<Down>', lambda event: self.show_next_image())
        self.root.bind('q', lambda event: root.destroy())

    def open_dicom(self):
        file_path = filedialog.askopenfilename(title="Select DICOM file", filetypes=(("DICOM files", "*.dcm"), ("All files", "*.*")))
        if file_path:
            self.images = self.load_dicom_images(file_path)
            self.show_image()
            self.frame_count = len(self.images)
            self.update_frame_count_label()

    def load_dicom_images(self, file_path):
        try:
            dicom_data = pydicom.dcmread(file_path)
            temp_images = dicom_data.pixel_array
            if len(np.shape(temp_images)) != 3:
                return np.array([temp_images])
            else:
                return temp_images
        except Exception as e:
            print("Error loading DICOM file:", e)
            return []

    def convert_to_image(self, frame):
        tempImg = self.normalize(frame)
        image = Image.fromarray(tempImg)
        return ImageTk.PhotoImage(image)

    def show_image(self):
        if self.photo_image:
            del self.photo_image  # Delete the previous PhotoImage object to avoid memory leak
        self.photo_image = self.convert_to_image(self.images[self.image_index])
        self.canvas.delete("all")
        self.canvas.config(width=self.photo_image.width(), height=self.photo_image.height())
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo_image)

        self.prev_button.pack(side=tk.LEFT, padx=5)
        self.next_button.pack(side=tk.LEFT, padx=5)
        self.close_button.pack(side=tk.RIGHT, padx=5, pady=5)

    def show_previous_image(self):
        if self.image_index > 0:
            self.image_index -= 1
            self.show_image()
            self.update_frame_count_label()

    def show_next_image(self):
        if self.image_index < len(self.images) - 1:
            self.image_index += 1
            self.show_image()
            self.update_frame_count_label()

    def normalize(self, input):
        if np.max(input) != 0:
            maxV = np.max(input)
            minV = np.min(input)
            upper_value = input - minV
            lower_value = maxV - minV
            tempImg = upper_value / lower_value
            tempImg = np.array(tempImg * 255, dtype=np.uint8)
            return tempImg
        else:
            return input

    def update_frame_count_label(self):
        self.frame_count_label.config(text=f"Frames: {self.frame_count}")

        if self.frame_count > 0:
            self.current_frame_label.config(text=f"Current frame: {self.image_index + 1}")

def main():
    root = tk.Tk()
    app = DICOMViewer(root)
    root.mainloop()

if __name__ == "__main__":
    main()
