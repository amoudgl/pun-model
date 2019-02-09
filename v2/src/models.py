from utils import data2numpy


class DataModelV2:
    """
    Class for parsing the cleaned relatedness, unigram and trigram data.

    For each sentence in puns dataset [data-agg.csv], we have precomputed
    relateness and trigram data. We just pass this data for a sentence to a
    probabilistic model which computes ambiguity and distinctiveness for a 
    given pun/nonpun.

    Note:
        Word vector for each sentence is extracted from relatedness data.
    """
    def __init__(self, relatedness_path, unigrams_path, trigrams_path):
        self.unigram = {}
        self.trigram = {}
        self.relatedness = {}
        self.word_vector = {}
        self._parse_relatedness(relatedness_path)
        self._parse_unigrams(unigrams_path)
        self._parse_trigrams(trigrams_path)
        print('loaded justine data model')

    # returns number of sentences in puns dataset
    def __len__(self):
        return len(self.trigram)

    # save word vectors and data in dictionary
    def _parse_relatedness(self, path):
        print('parsing relatedness data...')
        data = data2numpy(path)
        for row in data:
            words = [row[0].lower(), row[1].lower()]
            words.sort()
            words = tuple(words)
            relatedness = float(row[2])
            self.relatedness[words] = relatedness
        print('done')
        return

    # parse unigrams
    def _parse_unigrams(self, path):
        print('parsing unigram data...')
        data = data2numpy(path)
        for row in data:
            word = row[0].lower()
            unigram = float(row[1])
            self.unigram[word] = unigram
        print('done')
        return

    # parse trigrams
    def _parse_trigrams(self, path):
        print('parsing trigram data...')
        data = data2numpy(path)
        for row in data:
            idx = int(row[0])
            word = row[1].lower()
            m1_trigram = float(row[2])
            m2_trigram = float(row[3])
            # save trigram data
            if idx not in self.trigram:
                self.trigram[idx] = {}
                self.word_vector[idx] = []
                self.trigram[idx]['m1'] = []
                self.trigram[idx]['m2'] = []
            self.trigram[idx]['m1'].append(m1_trigram)
            self.trigram[idx]['m2'].append(m2_trigram)
            self.word_vector[idx].append(word)
        print('done')
        return


if __name__ == '__main__':
    # load model
    rpath = "../data/relatedness_clean.csv"
    upath = "../data/unigrams_clean.csv"
    tpath = "../data/trigrams_clean.csv"
    model = DataModelV2(rpath, upath, tpath)

    # test model on first sample of puns dataset
    print(model.word_vector[0])  # word vector
    print(model.relatedness[('allowed', 'use')])  # relatedness between words
    print(model.trigram[0]['m1'])  # m1 trigrams
    print(model.trigram[0]['m2'])  # m2 trigrams
    print(model.unigram['son'])  # unigram of a word
