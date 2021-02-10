from math import sqrt
import sys
import ezdxf
import utm
import csv


class Extractor:
    def __init__(self):
        self.doc = None
        self.poles_labels = []

    def find_dist(self, pole, label):
        delta_x = pole['x'] - label['x']
        delta_y = pole['y'] - label['y']
        return sqrt((delta_x ** 2 + delta_y ** 2))

    def open_dxf(self, filename):
        try:
            self.doc = ezdxf.readfile(filename)
            self.current_file = filename
        except IOError:
            print(f'Not a DXF file or a generic I/O error.')
            sys.exit(1)
        except ezdxf.DXFStructureError:
            print(f'Invalid or corrupted DXF file.')
            sys.exit(2)

    def extract(self):
        msp = self.doc.modelspace()
        poles = []
        labels = []
        # iterate through all drawing entities
        for e in msp:
            # grab any labels
            if e.dxftype() == 'MTEXT':
                new_label = {
                    'type': e.dxftype(),
                    'text': e.text,
                    'x': e.dxf.insert[0],
                    'y': e.dxf.insert[1],
                }
                labels.append(new_label)
            # grab any poles
            if e.dxftype() == 'INSERT':
                # print(e.dxftype(), e.dxf.layer, e.dxf.name, e.dxf.insert)
                x = e.dxf.insert[0]
                y = e.dxf.insert[1]
                lat_lon = utm.to_latlon(x, y, 17, "T")
                new_pole = {
                    'type': e.dxftype(),
                    'text': e.dxf.name,
                    'x': x,
                    'y': y,
                    'lat': lat_lon[0],
                    'lon': lat_lon[1],
                }
                poles.append(new_pole)

        # find nearest label for each pole
        self.poles_labels = []
        for p in poles:
            shortest_dist = 999999999
            i = -1
            for index, l in enumerate(labels):
                dist = self.find_dist(p, l)
                if dist < shortest_dist and dist < 10:
                    i = index
                    shortest_dist = dist
            if i != -1:
                new_pair = {
                    'pole': p,
                    'label': labels[i]
                }
            else:
                new_pair = {
                    'pole': p,
                    'label': 'None'
                }
            # poles, their lat/lon and label
            self.poles_labels.append(new_pair)

    def write_csv(self):
        csv_filename = "./csv/" + FILENAME.split(".")[0] + ".csv"
        with open(csv_filename, mode='w', newline='', encoding='utf-8') as out_file:
            writer = csv.writer(out_file, delimiter=",")
            writer.writerow(['Lead', 'Location', 'Species', 'Length', 'Class', 'Latitude', 'Longitude'])
            for pl in self.poles_labels:
                print(pl)
                lead = ""
                # check if there is a label associated with the pole
                if pl['label'] == 'None':
                    location = "None"
                else:
                    location = pl['label']['text']
                species = ""
                length = ""
                _class = ""
                lat = pl['pole']['lat']
                lon = pl['pole']['lon']
                writer.writerow([lead, location, species, length, _class, lat, lon])
