import csv
import numpy as np


def data2numpy(filepath):
    csv_file = open(filepath, 'rU')
    # csv_file = open(filepath, encoding="latin-1") # python3
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    data = []
    for row in csv_reader:
        line_count += 1
        assert isinstance(row, object)
        if row:
            data.append(row)
    data = np.array(data)
    data = data[1:, :]
    return data


def map_puntypeID_to_idx(joke):
    puntype_ID2idx = {}
    for sample in joke:
        idx = int(sample[0])
        puntype = sample[1]
        ID = int(sample[2])
        if puntype not in puntype_ID2idx:
            puntype_ID2idx[puntype] = {}
        puntype_ID2idx[puntype][ID] = idx-1
    return puntype_ID2idx
