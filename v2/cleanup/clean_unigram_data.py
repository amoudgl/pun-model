#!/usr/bin/env python3
from utils import data2numpy

near_unigram_datapath = './homophones_unigram_near.csv'
identical_unigram_datapath = './homophones_unigram_identical.csv'

# get the whole homophone unigram data in a single list
unigram_data = []
near_unigram_data = data2numpy(near_unigram_datapath)
for row in near_unigram_data:
    unigram_data.append(row)
data = data2numpy(identical_unigram_datapath)
for row in data:
    unigram_data.append(row)

# make word to unigram mapping
# ideally, it should be a one to one mapping
unigram = {}
for row in unigram_data:
    w1 = row[2].lower()
    w2 = row[3].lower()
    # unigram probabilities
    p_w1 = float(row[4])
    p_w2 = float(row[5])

    if w1 not in unigram:
        unigram[w1] = []
    if w2 not in unigram:
        unigram[w2] = []

    # log mutliple unigram values for a single key, if any
    if p_w1 not in unigram[w1]:
        unigram[w1].append(p_w1)
    if p_w2 not in unigram[w2]:
        unigram[w2].append(p_w2)

# for each word "w", unigram[w1] should return a list containing single element
# let's see how many duplicates we have
keys = unigram.keys()
for key in keys:
    if (len(unigram[key]) > 1):
        print("multiple unigram values found for word {}:".format(key),
              end=" ")
        print(unigram[key])

# pick a single value for duplicate cases and save clean data
output_path = "../data/unigrams_clean.csv"
f = open(output_path, "w")
f.write("word,unigram\n")
for key in keys:
    row = [key, str(unigram[key][0])]
    row_str = ",".join(row) + "\n"
    f.write(row_str)
print("saved clean unigram data at {}".format(output_path))
