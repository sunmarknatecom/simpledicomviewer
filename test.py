import tkinter as tk
from tkinter import filedialog
import pydicom
from PIL import Image, ImageTk

class DICOMViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("DICOM Viewer")

        self.frame = tk.Frame(self.root)
        self.frame.pack(padx=10, pady=10)

        self.canvas = tk.Canvas(self.frame, bg="black", width=512, height=512)
        self.canvas.pack()

        self.button = tk.Button(self.frame, text="Open DICOM", command=self.open_dicom)
        self.button.pack(pady=5)

        self.image_index = 0
        self.images = []

    def open_dicom(self):
        file_path = filedialog.askopenfilename(title="Select DICOM file", filetypes=(("DICOM files", "*.dcm"), ("All files", "*.*")))
        if file_path:
            self.images = self.load_dicom_images(file_path)
            if self.images:
                self.show_image()

    def load_dicom_images(self, file_path):
        try:
            dicom_data = pydicom.dcmread(file_path)
            images = [self.convert_to_image(frame) for frame in dicom_data.pixel_array]
            return images
        except Exception as e:
            print("Error loading DICOM file:", e)
            return []

    def convert_to_image(self, frame):
        image = Image.fromarray(frame)
        return ImageTk.PhotoImage(image)

    def show_image(self):
        if self.images:
            image = self.images[self.image_index]
            self.canvas.delete("all")
            self.canvas.config(width=image.width(), height=image.height())
            self.canvas.create_image(0, 0, anchor=tk.NW, image=image)

            # Add navigation buttons
            prev_button = tk.Button(self.frame, text="Previous", command=self.show_previous_image)
            prev_button.pack(side=tk.LEFT, padx=5)
            next_button = tk.Button(self.frame, text="Next", command=self.show_next_image)
            next_button.pack(side=tk.LEFT, padx=5)

    def show_previous_image(self):
        if self.images and self.image_index > 0:
            self.image_index -= 1
            self.show_image()

    def show_next_image(self):
        if self.images and self.image_index < len(self.images) - 1:
            self.image_index += 1
            self.show_image()

def main():
    root = tk.Tk()
    app = DICOMViewer(root)
    root.mainloop()

if __name__ == "__main__":
    main()
