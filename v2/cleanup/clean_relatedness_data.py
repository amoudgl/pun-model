#!/usr/bin/env python3
from utils import data2numpy, map_puntypeID_to_idx

relatedness_near_datapath = ("./wordPair_relatedness_" +
                             "smoothedTrigrams_near.csv")
relatedness_identical_datapath = ("./wordPair_relatedness_" +
                                  "smoothedTrigrams_identical.csv")

# get m1 and m2 (two meanings/interpretations) for each sentence in the dataset
meanings = {}
puns_datapath = '../../data/data-agg.csv'
puns_data = data2numpy(puns_datapath)
for i, row in enumerate(puns_data):
    meanings[i] = [row[-3], row[-2]]

# map puntype (near/identical) and puntypeID to index in puns dataset
# for example, m['near'][1] will yield index of the pun with 'near' homophone
# and having 'near' sentence ID = 1 in puns dataset [data-agg.csv]
get_idx = map_puntypeID_to_idx(data2numpy(puns_datapath))

# clean up relatedness data
relatedness = {}
data = data2numpy(relatedness_near_datapath)
for row in data:
    id = int(row[0])
    idx = get_idx['near'][id]
    m1 = meanings[idx][0]
    m2 = meanings[idx][1]
    word = row[3]
    m1_relatedness = float(row[4])
    m2_relatedness = float(row[5])

    # build word pairs
    t1 = [word, m1]
    t1.sort()
    t1 = tuple(t1)
    t2 = [word, m2]
    t2.sort()
    t2 = tuple(t2)

    # save relatedness data
    if t1 not in relatedness:
        relatedness[t1] = []
    if t2 not in relatedness:
        relatedness[t2] = []

    # log duplicate data, if any for a given tuple
    if m1_relatedness not in relatedness[t1]:
        relatedness[t1].append(m1_relatedness)
    if m2_relatedness not in relatedness[t2]:
        relatedness[t2].append(m2_relatedness)

data = data2numpy(relatedness_identical_datapath)
for row in data:
    id = int(row[0])
    idx = get_idx['identical'][id]
    m1 = meanings[idx][0]
    m2 = meanings[idx][1]
    word = row[3]
    m1_relatedness = float(row[4])
    m2_relatedness = float(row[5])

    # build word pairs
    t1 = [word, m1]
    t1.sort()
    t1 = tuple(t1)
    t2 = [word, m2]
    t2.sort()
    t2 = tuple(t2)

    # save relatedness data
    if t1 not in relatedness:
        relatedness[t1] = []
    if t2 not in relatedness:
        relatedness[t2] = []

    # log duplicate data, if any for a given tuple
    if m1_relatedness not in relatedness[t1]:
        relatedness[t1].append(m1_relatedness)
    if m2_relatedness not in relatedness[t2]:
        relatedness[t2].append(m2_relatedness)

# for tuple key "t", relatedness[t] should return a list containing single
# element; let's see how many duplicates we have
keys = relatedness.keys()
for key in keys:
    if (len(relatedness[key]) > 1):
        print("multiple relatedness values " +
              "found for tuple ({}, {}):".format(key[0], key[1]), end=" ")
        print(relatedness[key])

# pick a single value for tuples with mutliple relatedness values
# and save clean data
output_path = "../data/relatedness_clean.csv"
f = open(output_path, "w")
f.write("word1,word2,relatedness\n")
for key in keys:
    row = [key[0], key[1], str(relatedness[key][0])]
    row_str = ",".join(row) + "\n"
    f.write(row_str)
print("saved clean relatedness data at {}".format(output_path))
