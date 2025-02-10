import pydicom
import os

ct_paths = [os.path.join("TEST_CT",elem) for elem in os.listdir("TEST_CT")]
pt_paths = [os.path.join("TEST_PT",elem) for elem in os.listdir("TEST_PT")]

ct_objs = [pydicom.dcmread(elem) for elem in ct_paths]
pt_objs = [pydicom.dcmread(elem) for elem in pt_paths]

rearranged_ct_objs = sorted(ct_objs, key=lambda x: x.SliceLocation)
rearranged_pt_objs = sorted(pt_objs, key=lambda x: x.SliceLocation)

for i in range(len(ct_objs)):
    if rearranged_ct_objs[i].SliceLocation != rearranged_pt_objs[i].SliceLocation:
            print(i)
    else:
            continue

print("CT images size is ", ct_objs[0].Columns, ", ", ct_objs[0].Rows)
print("PT images size is ", pt_objs[0].Columns, ", ", pt_objs[0].Rows)
