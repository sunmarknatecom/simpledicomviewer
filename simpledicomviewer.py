import pydicom, os
import numpy as np
from pydicom.data import get_testdata_file

filename_mr = get_testdata_file("MR_small.dcm")
filename_ct = get_testdata_file("CT_small.dcm")

print(filename_mr)
print(filename_ct)

# 예제파일들의 경로
print(os.path.dirname(filename_mr))

# 예제파일들을 확인
print(os.listdir(os.path.dirname(filename_mr)))

mr_object = pydicom.dcmread(filename_mr)
ct_object = pydicom.dcmread(filename_ct)

mr_image = mr_object.pixel_array
ct_image = ct_object.pixel_array

print(type(mr_image))
print(type(ct_image))

print(np.shape(mr_image))
#(65,64)
print(np.shape(ct_image))
#(128,128)

print("MR_max_value", np.max(mr_image), ", ", "MR_min_value", np.min(mr_image))
print("CT_max_value", np.max(ct_image), ", ", "CT_min_value", np.min(ct_image))
