import pydicom
from pydicom.data import get_testdata_file

filename_mr = get_testdata_file("MR_small.dcm")
filename_ct = get_testdata_file("CT_small.dcm")

print(filename_mr)
print(filename_ct)

# 예제파일들의 경로
print(os.path.dirname(filename_mr))

# 예제파일들을 확인
print(os.listdir(os.path.dirname(filename_mr)))
