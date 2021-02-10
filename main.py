from extractor import Extractor
import os

DXF_DIRECTORY = "./dxf/"
CSV_DIRECTORY = "./csv/"

ext = Extractor()

# for each dxf file in ./dxf/ generate one csv file with the same name
# in ./csv/
processed = 0
for filename in os.listdir(DXF_DIRECTORY):
    dxf_filepath = os.path.join(DXF_DIRECTORY, filename)
    # try to open the file, break if invalid file
    if ext.open_dxf(dxf_filepath):
        try:
            # extract pole coordinates/labels
            ext.extract()
            # write the csv
            csv_filepath = filename.split(".")[0] + ".csv"
            csv_filepath = os.path.join(CSV_DIRECTORY, csv_filepath)
            ext.write_csv(csv_filepath)
            processed += 1
        except:
            print(f"Error processing file {dxf_filepath}!")

    else:
        print(f"Could not open {dxf_filepath}, skipping...")

print(f"Complete. Successfully processed {processed} of {len(os.listdir(DXF_DIRECTORY))} files.")
