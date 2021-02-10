from extractor import Extractor
import os

DXF_DIRECTORY = "./dxf/"
CSV_DIRECTORY = "./csv/"

for filename in os.listdir(DXF_DIRECTORY):
    dxf_filepath = os.path.join(DXF_DIRECTORY, filename)
    print(dxf_filepath)
    csv_filepath = os.path.join(CSV_DIRECTORY, filename)
    print(csv_filepath)

