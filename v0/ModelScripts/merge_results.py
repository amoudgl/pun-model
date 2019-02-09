"""
This script merges two model output files for near and identical type puns
which are computed by author's original script 'computeMeasures.py'. Measures
are saved in a new csv file.
"""
from utils import data2numpy, map_puntypeID_to_idx, save_results

if __name__ == '__main__':
    jokes = data2numpy("../../data/data-agg.csv")
    get_idx = map_puntypeID_to_idx(jokes)
    jokes_data = {}

    # fill dictionary with model output on identical and near puns
    jokes_data = save_results('../ModelOutputs/near_trigram_13_0.csv',
                              jokes_data, get_idx)
    jokes_data = save_results('../ModelOutputs/identical_trigram_13_0.csv',
                              jokes_data, get_idx)

    # write model outputs in a new csv file
    output_path = "../ModelOutputs/data.csv"
    f_v0 = open(output_path, "wr")
    f_v0.write("idx,sentenceID,punType,sentenceType,ambiguity,distinctiveness,"
               + "sentence\n")

    # parse measures from original data sheet pun-model/data/data-agg.csv and
    # save it in the same format as data.csv for comparing model results
    f_original = open("../ModelOutputs/data-agg-measures.csv", "wr")
    f_original.write("idx,sentenceID,punType,sentenceType,ambiguity,"
                     + "distinctiveness,sentence\n")
    for idx in range(len(jokes_data)):
        f_v0.write(str(idx) +
                   ","+jokes_data[idx] +
                   ","+'"'+jokes[idx][-4]+'"\n')
        sent_id = jokes[idx][2]
        pun_type = jokes[idx][1]
        sent_type = jokes[idx][3]
        amb = jokes[idx][4]
        dist = jokes[idx][7]
        sent = '"'+jokes[idx][-4]+'"\n'
        row_str = ",".join([str(idx), sent_id, pun_type, sent_type,
                           amb, dist, sent])
        f_original.write(row_str)
    print("model results saved in %s" % (output_path))
