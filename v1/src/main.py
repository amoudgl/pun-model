"""
This script implements probabilistic model for puns. Two measures namely,
ambiguity and distinctivenessare are computed by the model for each sentence
in the puns dataset [data-agg.csv]. It reproduces the measures computed by
author's implementation [github.com/justinek/pun-paper].

References:
    * http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.361.7510
    * https://github.com/justinek/pun-paper
"""
import math
import itertools
import argparse

import numpy as np

import models
from utils import data2numpy, normalize

args = None
parser = argparse.ArgumentParser(description='Pun model')
parser.add_argument('-r', '--self-relatedness', default=13.0, type=float,
                    help='relatedness of a observed homophone with itself')
parser.add_argument('-s', '--scaling-parameter', default=0.0, type=float,
                    help='scale relatedness data with a constant factor')


def compute_measures(data_model, data):
    global args
    num_puns = len(data_model)
    amb = np.zeros((num_puns))
    dist = np.zeros((num_puns))

    # loop over all sentences in puns dataset
    for idx in range(num_puns):

        # puntype: near or identical?
        puntype = data[idx][1]

        # extract data for the given sentence
        m1_ngram = data_model.trigram[idx]['m1']
        m2_ngram = data_model.trigram[idx]['m2']
        m1_ngram = [math.log(ngram) for ngram in m1_ngram]
        m2_ngram = [math.log(ngram) for ngram in m2_ngram]
        m1_relatedness = data_model.relatedness[idx]['m1']
        m2_relatedness = data_model.relatedness[idx]['m2']
        words = data_model.word_vector[idx]
        m1 = words[0]   # convention in justine's data: first word will be m1
        pm1 = math.log(data_model.homo_unigram[puntype]['m1'][m1])
        pm2 = math.log(data_model.homo_unigram[puntype]['m2'][m1])

        num_words = len(words)
        focus_vectors = list(itertools.product([False, True],
                                               repeat=num_words))
        # vector containing proabilities for each f,w combination given m1
        f_w_given_m1 = []
        # vector containing probabilities for each f,w combination given m2
        f_w_given_m2 = []
        sum_m = 0.0
        sum_m1_f = 0.0
        sum_m2_f = 0.0

        # iterate through all subsets of indices in context subsets
        for fv in focus_vectors:
            # probabilty of each word being in focus (coin weight)
            pw_focus = 0.5  # can be tweaked

            # probability of a focus vector
            # determined by the number of words in focus
            # (number of "True" in focus_vector) vs not
            num_words_focus = sum(fv)
            pf = (math.pow(pw_focus, num_words_focus) *
                  math.pow(1 - pw_focus, num_words - num_words_focus))

            words_focus = []
            sum_logpw_given_m1_f = 0.0
            sum_logpw_given_m2_f = 0.0
            for j in range(num_words):
                wj = words[j]
                if fv[j] is True:
                    words_focus.append(wj)
                    logpw_given_m1_f = (m1_ngram[j] + m1_relatedness[j] +
                                        args.scaling_parameter)
                    logpw_given_m2_f = (m2_ngram[j] + m2_relatedness[j] +
                                        args.scaling_parameter)
                    sum_logpw_given_m1_f = (sum_logpw_given_m1_f +
                                            logpw_given_m1_f)
                    sum_logpw_given_m2_f = (sum_logpw_given_m2_f +
                                            logpw_given_m2_f)
                else:
                    logpw_given_m1_f_ngram = m1_ngram[j]
                    logpw_given_m2_f_ngram = m2_ngram[j]
                    sum_logpw_given_m1_f = (sum_logpw_given_m1_f +
                                            logpw_given_m1_f_ngram)
                    sum_logpw_given_m2_f = (sum_logpw_given_m2_f +
                                            logpw_given_m2_f_ngram)

            # with homophone prior, calculate P(m,F | words)
            pm1_f_given_w = math.exp(pm1 + math.log(pf) + sum_logpw_given_m1_f)
            pm2_f_given_w = math.exp(pm2 + math.log(pf) + sum_logpw_given_m2_f)

            # P(F | words, m) \propto P(w | m, f)P(f | m)
            # since f, m are independent, this is just P(f)
            pf_given_w_m1 = math.exp(math.log(pf) + sum_logpw_given_m1_f)
            pf_given_w_m2 = math.exp(math.log(pf) + sum_logpw_given_m2_f)
            f_w_given_m1.append(pf_given_w_m1)
            f_w_given_m2.append(pf_given_w_m2)

        # sum over all possible focus vectors for P(m1|w)
        sum_m1_f = sum_m1_f + pm1_f_given_w
        sum_m2_f = sum_m2_f + pm2_f_given_w
        sum_m = sum_m + pm1_f_given_w + pm2_f_given_w

        # normalize and calcualte entropy
        pm1_given_w = sum_m1_f / sum_m
        pm2_given_w = sum_m2_f / sum_m
        entropy = - (pm1_given_w * math.log(pm1_given_w) +
                     pm2_given_w * math.log(pm2_given_w))

        # normalize probability vectors of F to sum to 1 for m1 and m2
        normfw_given_m1 = normalize(f_w_given_m1)
        normfw_given_m2 = normalize(f_w_given_m2)

        max_m1_fv = focus_vectors[normfw_given_m1.index(max(normfw_given_m1))]
        max_m2_fv = focus_vectors[normfw_given_m2.index(max(normfw_given_m2))]

        # find words in focus given max_m1_fv and max_m2_fv
        m1_focus_words = []
        m2_focus_words = []
        for i in range(len(max_m1_fv)):
            if max_m1_fv[i] is True:
                m1_focus_words.append(words[i])
            if max_m2_fv[i] is True:
                m2_focus_words.append(words[i])

        # compute KL between the two distributions
        kl1 = 0
        kl2 = 0
        for i in range(len(normfw_given_m1)):
            kl1 = kl1 + (math.log(normfw_given_m1[i] / normfw_given_m2[i]) *
                         normfw_given_m1[i])
            kl2 = kl2 + (math.log(normfw_given_m2[i] / normfw_given_m1[i]) *
                         normfw_given_m2[i])
        kl = kl1 + kl2

        # save measures
        amb[idx] = entropy
        dist[idx] = kl
    return amb, dist


if __name__ == '__main__':
    args = parser.parse_args()
    # load model
    rpaths = ['../data/wordPair_relatedness_smoothedTrigrams_near.csv',
              '../data/wordPair_relatedness_smoothedTrigrams_identical.csv']
    upaths = ['../data/homophones_unigram_near.csv',
              '../data/homophones_unigram_identical.csv']
    puns_data_path = '../data/data-agg.csv'
    data_model = models.DataModelV1(rpaths, upaths, puns_data_path,
                                    args.self_relatedness)

    # compute ambiguity and distinctiveness for each sentence in dataset
    data = data2numpy("../../data/data-agg.csv")
    amb, dist = compute_measures(data_model, data)

    # write output in csv
    output_path = "../results/data.csv"
    f_v1 = open(output_path, "w")
    f_v1.write("idx,sentenceID,punType,sentenceType,ambiguity," +
               "distinctiveness,sentence\n")
    for idx in range(len(data)):
        sent_id = data[idx][2]
        sent_puntype = data[idx][1]
        sent_type = data[idx][3]
        sent_amb = str(amb[idx])
        sent_dist = str(dist[idx])
        sent = '"' + data[idx][-4] + '"\n'
        row = [str(idx), sent_id, sent_puntype, sent_type, sent_amb,
               sent_dist, sent]
        row_str = ",".join(row)
        f_v1.write(row_str)
    print("model results saved in %s" % (output_path))
