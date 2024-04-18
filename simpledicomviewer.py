import pydicom
import numpy as np
from PIL import Image

file_path = "path"

try:
    file_object = pydicom.dcmread(file_path)
    image_array = file_object.pixel_array
    if len(np.shape(image_array)) !=3:
        temp_array = np.array([image_array])
    else:
        temp_array = image_array
except Exception as e:
    print("Error loading DICOM file: ", e)
    temp_array = []

def normalize(input_frame):
    max_value = np.max(input_frame)
    min_value = np.min(input_frame)
    return np.array(((input_frame-min_value)/(max_value-min_value))*255, dtype=np.uint8)
