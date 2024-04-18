import pydicom
import numpy as np
from PIL import Image

file_path = "path"

try:
    file_object = pydicom.dcmread(file_path)
    image_array = file_object.pixel_array
    if len(np.shape(temp_images)) !=3:
        temp_array = np.array([image_array])
    else:
        temp_array = image_array
except Exception as e:
    print("Error loading DICOM file: ", e)
    temp_array = []
