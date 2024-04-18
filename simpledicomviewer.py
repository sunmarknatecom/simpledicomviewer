import pydicom
import numpy as np
from PIL import Image

file_path = "path"

file_object = pydicom.dcmread(file_path)
image_array = file_object.pixel_array

show_image = Image.fromarray(image_array)
show_image.show()
