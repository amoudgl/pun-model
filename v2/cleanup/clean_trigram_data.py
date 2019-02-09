#!/usr/bin/env python3
from utils import data2numpy, map_puntypeID_to_idx

relatedness_near_datapath = ("./wordPair_relatedness_" +
                             "smoothedTrigrams_near.csv")
relatedness_identical_datapath = ("./wordPair_relatedness_" +
                                  "smoothedTrigrams_identical.csv")

# map puntype (near/identical) and puntypeID to index in puns dataset
# for example, m['near'][1] will yield index of the pun with 'near' homophone
# and having 'near' sentence ID = 1 in puns dataset
puns_datapath = "../../data/data-agg.csv"
get_idx = map_puntypeID_to_idx(data2numpy(puns_datapath))

# process near homophone type sentences
data = data2numpy(relatedness_near_datapath)
trigram_data = []
for row in data:
    trigram_data.append(row)
trigrams = {}
for row in trigram_data:
    id = int(row[0])
    idx = get_idx['near'][id]
    m1_trigram = float(row[-3])
    m2_trigram = float(row[-2])
    word = row[3].lower()
    if idx not in trigrams:
        trigrams[idx] = {}
        trigrams[idx]['values'] = []
        trigrams[idx]['words'] = []
    trigrams[idx]['values'].append([m1_trigram, m2_trigram])
    trigrams[idx]['words'].append(word)

# process identical homophone type sentences
trigram_data = []
data = data2numpy(relatedness_identical_datapath)
for row in data:
    trigram_data.append(row)
for row in trigram_data:
    id = int(row[0])
    idx = get_idx['identical'][id]
    m1_trigram = float(row[-3])
    m2_trigram = float(row[-2])
    word = row[3].lower()
    if idx not in trigrams:
        trigrams[idx] = {}
        trigrams[idx]['values'] = []
        trigrams[idx]['words'] = []
    trigrams[idx]['values'].append([m1_trigram, m2_trigram])
    trigrams[idx]['words'].append(word)

# write output
output_path = "../data/trigrams_clean.csv"
num_samples = len(trigrams)
f = open(output_path, "w")
f.write("index,word,m1_trigram,m2_trigram\n")
for idx in range(num_samples):
    for i, word in enumerate(trigrams[idx]['words']):
        m1_trigram = trigrams[idx]['values'][i][0]
        m2_trigram = trigrams[idx]['values'][i][1]
        row = [str(idx), word, str(m1_trigram), str(m2_trigram)]
        row_str = ",".join(row) + "\n"
        f.write(row_str)
print("saved clean trigram data at {}".format(output_path))
