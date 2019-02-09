# computes the entropy of P(m | w) using
# word pair relatedness and trigram probabilities
# from wordPair_relatedness_smoothedTrigrams_*.csv
# homophone log probability from homophones_unigram_*.csv.

import sys, re, string, itertools
import math

# parameters
# indicates whether puns are identical or homophone puns
punType = sys.argv[1]
useTrigrams = bool(int(sys.argv[2]))
self_relatedness = float(sys.argv[3])
scaling_parameter = float(sys.argv[4])

ngramType = "unigram"
if useTrigrams:
    ngramType = "trigram"

filename = "../ModelOutputs/" + punType + "_" + ngramType + "_" + str(int(self_relatedness)) + "_" + str(int(scaling_parameter)) + ".csv"
print filename
writeFile = open(filename, "wr")

# The output is formatted as follows:
writeFile.write("punType,sentenceID,sentenceType,sum_m1_ngram,sum_m2_ngram,sum_m1_relatedness,sum_m2_relatedness,p_m1_given_w,p_m2_given_w,entropy,m1KL,m2KL,KL,m1Focus,m2Focus\n")

# A function that takes in a list and normalizes to sum to 1

def normListSumTo(L, sumTo=1):
    sum = reduce(lambda x,y:x+y, L)
    return [ x/(sum*1.0)*sumTo for x in L]

# a dictionary holding unigram probabilities for m1 (original homophone)
# indexed by the original homophone
m1ProbDict = dict()

# a dictionary holding unigram probabilities for m2 (modified homophone)
# indexed by the oriignal homophone
m2ProbDict = dict()

# homophone unigram
unigramFile = open("../ProcessedData/homophones_unigram_" + punType + ".csv", "r")

firstLine = 0

for l in unigramFile:
    if firstLine == 0:
        firstLine = 1
    else:
        l = l.strip()
        toks = l.split(",")
        key = toks[2].lower()
        m1Prob = float(toks[4])
        m2Prob = float(toks[5])
        m1ProbDict[key] = math.log(m1Prob)
        m2ProbDict[key] = math.log(m2Prob)

# a dictionary holding word pair information, with each entry being a sentence
sentenceDict = dict()
pairFile = open("../ProcessedData/wordPair_relatedness_smoothedTrigrams_" + punType + ".csv", "r")
firstLine = 0
for l in pairFile:
    if firstLine == 0:
        firstLine = 1
    else:
        l = l.strip()
        toks = l.split(",")
        sentenceID = int(toks[0])
        sentenceType = toks[1]
        # observed homophone
        m1 = toks[2]
        # content word
        word = toks[3]
        # relatedness of observed word with observed homophone (m1)
        m1_relatedness = float(toks[4])
        # relatedness of observed word with alternative homophone (m2)
        m2_relatedness = float(toks[5])
        # prior trigram probability of the content word with observed homophone (m1)
        m1_ngram = math.log(float(toks[6]))
        # prior trigram probability of the content word with the alternative homophone (m2)
        m2_ngram = math.log(float(toks[7]))
        # prior unigram probabiltiy of the content word
        content_unigram = math.log(float(toks[8]))

        # if this is the first word pair entry for the sentence,
        # intializes all the relevant information and puts it in
        # the dictionary indexed by sentence ID
        if sentenceID not in sentenceDict:
            # wordArray is an array of observed words for each sentence
            wordArray = [word]

            # hom1RelatednessArray is an array of relatedness for the observed words
            # and the original homophone (h1)
            m1RelatednessArray = [self_relatedness]

            # hom2RelatednessArray is an array of relatedness for the observed words
            # and the modified homophone (h2)
            m2RelatednessArray = [0]

            # m1NgramArray is an array of ngram probabilities for the observed words and the original homophone
            m1NgramArray = [m1_ngram]

            # m2NgramArray is an array of ngram probs for the observed words and the modified homophone
            m2NgramArray = [m2_ngram]

            # contentUnigramArray is an array of unigram probs for the observed words
            contentUnigramArray = [content_unigram]

            # infoArray is an array of all the relevant information for a sentence,
            # namely whether it is a pun, the original homophone, the array of observed words,
            # the array of relatedness for the observed words and h1, and the array of relatedness
            # for the observed words and h2
            infoArray = [sentenceType, m1, wordArray, m1RelatednessArray, m2RelatednessArray, m1NgramArray, m2NgramArray, contentUnigramArray]

            # places the infoArray for the sentence in the dictionary
            sentenceDict[sentenceID] = infoArray

        # if the sentence is already in the dictionary, updates the information for that sentence
        # with information from the new pair
        else:
            # retrieves the current infoArray for the sentence
            infoArray = sentenceDict[sentenceID]

            # the array of observed words. Updates it with the observed word from current pair
            infoArray[2].append(word)

            # the array of relatedness with m1. Updates it with relatedness from current pair
            infoArray[3].append(m1_relatedness)

            # the array of relatedness with m2. Updates it with relatedness from current pair
            infoArray[4].append(m2_relatedness)

            # the array of ngram with m1
            infoArray[5].append(m1_ngram)

            # the array of ngram with m2
            infoArray[6].append(m2_ngram)

            # the array of unigram for content word
            infoArray[7].append(content_unigram)

            # puts the updated infoArray into the dictionary indexed by sentenceID
            sentenceDict[sentenceID] = infoArray

for k, v in sentenceDict.iteritems():

    # sentenceID
    sentenceID = str(k)

    # isPun
    sentenceType = v[0]

    # the original homophone (not necessarily the one observed. Just the more standard one.
    m1 = v[1]
    #print hom
    #print m1ProbDict

    # the log probablity of the original homophone m1
    m1PriorProb = m1ProbDict[m1]

    # the log probability of the modified homophone h2
    m2PriorProb = m2ProbDict[m1]

    # array of all observed words in the sentence
    words = v[2]

    # number of content words in sentence
    numWords = len(words)

    # array of relatedness measures with all words and h1
    m1Relatedness = v[3]

    # array of relatedness measures with all words and h2
    m2Relatedness = v[4]

    if useTrigrams:
        # array of ngram with all words and h1
        m1Ngram = v[5]
        # array of ngram with all words and h2
        m2Ngram = v[6]
    else:
        # array of unigram of all words
        m1Ngram = v[7]
        m2Ngram = v[7]

    # makes a list of all possible focus vectors
    focusVectors = list(itertools.product([False, True], repeat=numWords))
    #print focusVectors

    # vector containing proabilities for each f,w combination given m1
    fWGivenM1 = []
    # vector containing probabilities for each f,w combination given m2
    fWGivenM2 = []

    sumOverMF = 0
    sumM1OverF = 0
    sumM2OverF = 0
    # iterates through all subsets of indices in contextSubsets
    for fVector in focusVectors:
        # probabilty of each word being in focus (coin weight)
        probWordInFocus = 0.5  # can be tweaked

        # Probability of a focus vector
        # Determined by the number of words in focus (number of "True" in vector) vs not
        numWordsInFocus = sum(fVector)

        probFVector = math.pow(probWordInFocus, numWordsInFocus) * math.pow(1 - probWordInFocus, numWords - numWordsInFocus)

        wordsInFocus = []
        sumLogProbWordsGivenM1F = 0
        sumLogProbWordsGivenM2F = 0
        for j in range(numWords):
            wordj = words[j]
            if fVector[j] is True:
                wordsInFocus.append(wordj)
                logProbWordGivenM1 = m1Ngram[j] + m1Relatedness[j] + scaling_parameter
                logProbWordGivenM2 = m2Ngram[j] + m2Relatedness[j] + scaling_parameter
                sumLogProbWordsGivenM1F = sumLogProbWordsGivenM1F + logProbWordGivenM1
                sumLogProbWordsGivenM2F = sumLogProbWordsGivenM2F + logProbWordGivenM2
            else:
                logProbWordGivenM1_ngram = m1Ngram[j]
                logProbWordGivenM2_ngram = m2Ngram[j]
                sumLogProbWordsGivenM1F = sumLogProbWordsGivenM1F + logProbWordGivenM1_ngram
                sumLogProbWordsGivenM2F = sumLogProbWordsGivenM2F + logProbWordGivenM2_ngram

        # with homophone prior, calculate P(m,F | words)
        probM1FGivenWords = math.exp(m1PriorProb + math.log(probFVector) + sumLogProbWordsGivenM1F)
        probM2FGivenWords = math.exp(m2PriorProb + math.log(probFVector) + sumLogProbWordsGivenM2F)

        # P(F | words, m) \propto P(w | m, f)P(f | m)
        # since f, m are independent, this is just P(f)
        probFGivenWordsM1 = math.exp(math.log(probFVector) + sumLogProbWordsGivenM1F)
        probFGivenWordsM2 = math.exp(math.log(probFVector) + sumLogProbWordsGivenM2F)
        fWGivenM1.append(probFGivenWordsM1)
        fWGivenM2.append(probFGivenWordsM2)

    # sums over all possible focus vectors for P(m1|w)
    sumM1OverF = sumM1OverF + probM1FGivenWords
    sumM2OverF = sumM2OverF + probM2FGivenWords
    sumOverMF = sumOverMF + probM1FGivenWords + probM2FGivenWords
    # normalizes and calcualtes entropy
    probM1 = sumM1OverF / sumOverMF
    probM2 = sumM2OverF / sumOverMF
    entropy = - (probM1 * math.log(probM1) + probM2 * math.log(probM2))

    # normalizes probability vectors of F to sum to 1 for m1 and m2
    normalizedFWGivenM1 = normListSumTo(fWGivenM1, 1)
    normalizedFWGivenM2 = normListSumTo(fWGivenM2, 1)

    maxM1FocusVector = focusVectors[normalizedFWGivenM1.index(max(normalizedFWGivenM1))]
    maxM2FocusVector = focusVectors[normalizedFWGivenM2.index(max(normalizedFWGivenM2))]

    # find words in focus given maxM1FocusVector and maxM2FocusVector
    maxM1FocusWords = []
    maxM2FocusWords = []
    for i in range(len(maxM1FocusVector)):
        if maxM1FocusVector[i] is True:
            maxM1FocusWords.append(words[i])
        if maxM2FocusVector[i] is True:
            maxM2FocusWords.append(words[i])
    # coomputes KL between the two distributions
    KL1 = 0
    KL2 = 0
    for i in range(len(normalizedFWGivenM1)):
        KL1 = KL1 + math.log(normalizedFWGivenM1[i] / normalizedFWGivenM2[i]) * normalizedFWGivenM1[i]
        KL2 = KL2 + math.log(normalizedFWGivenM2[i] / normalizedFWGivenM1[i]) * normalizedFWGivenM2[i]

    writeFile.write(punType + "," + sentenceID + "," + sentenceType + "," + str(sum(m1Ngram)) + "," + str(sum(m2Ngram)) + "," + str(sum(m1Relatedness)) + "," + str(sum(m2Relatedness)) + "," + str(probM1) + "," + str(probM2) + "," + str(entropy) + "," + str(KL1) + "," + str(KL2) + "," + str(KL1 + KL2) + "," + ";".join(maxM1FocusWords) + "," + ";".join(maxM2FocusWords)+"\n")
