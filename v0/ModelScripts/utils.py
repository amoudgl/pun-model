"""
Implements several utility functions.
"""
import csv
import numpy as np


def map_puntypeID_to_idx(data):
    puntype_ID2idx = {}
    for sample in data:
        idx = int(sample[0])
        puntype = sample[1]
        ID = int(sample[2])
        if puntype not in puntype_ID2idx:
            puntype_ID2idx[puntype] = {}
        puntype_ID2idx[puntype][ID] = idx-1
    return puntype_ID2idx


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


def save_results(path, output_dict, get_idx):
    data = data2numpy(path)
    for sample in data:
        sent_id = sample[1]  # index of near/identical type
        pun_type = sample[0]  # near or identical
        sent_type = sample[2]  # pun or nonpun
        amb = sample[-6]
        dist = sample[-3]
        row = [sent_id, pun_type, sent_type, amb, dist]
        row_str = ",".join(row)
        if (pun_type == 'identical' or pun_type == 'near') and \
           (sent_type == 'pun' or sent_type == 'nonpun'):
            idx = get_idx[pun_type][int(sent_id)]
            output_dict[idx] = row_str
    return output_dict
