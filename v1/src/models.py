from utils import map_puntypeID_to_idx, data2numpy


class DataModelV1:
    """
    Class for parsing the original relatedness, unigram and trigram data
    released by author.

    For each sentence in puns dataset [data-agg.csv], relateness and trigram
    data has been precomputed by author and saved in csv files namely,
    wordPair_relatedness_smoothedTrigrams* and homophones_unigram*. This model
    class parses the data from these files and saves it in appropriate format
    which can be passed directly to our pun model v1 [v1/main.py].

    Note:
        Word vector for each sentence is extracted from relatedness data.
    """
    def __init__(self,
                 relatedness_paths,
                 homophone_unigram_paths,
                 puns_data_path,
                 self_relatedness=13.0):
        self.self_relatedness = self_relatedness
        self.use_trigrams = True
        self.unigram = {}
        self.trigram = {}
        self.homo_unigram = {}
        self.relatedness = {}
        self.word_vector = {}
        self.get_idx = map_puntypeID_to_idx(data2numpy(puns_data_path))
        self._parse_relatedness(data2numpy(relatedness_paths[0]), 'near')
        self._parse_relatedness(data2numpy(relatedness_paths[1]), 'identical')
        self._parse_unigrams(data2numpy(homophone_unigram_paths[0]), 'near')
        self._parse_unigrams(data2numpy(homophone_unigram_paths[1]),
                             'identical')
        print('loaded data model v1')

    # returns number of sentences in puns dataset
    def __len__(self):
        return len(self.relatedness)

    # save word vectors and data in dictionary
    def _parse_relatedness(self, data, puntype):
        print('parsing relatedness data...')
        for row in data:
            sent_id = int(row[0])
            m = row[2]
            word = row[3]
            idx = self.get_idx[puntype][sent_id]
            # save word vector
            if idx not in self.word_vector:
                self.word_vector[idx] = []
            self.word_vector[idx].append(word)

            # save relatedness data
            if idx not in self.relatedness:
                self.relatedness[idx] = {}
                self.relatedness[idx]['m1'] = []
                self.relatedness[idx]['m2'] = []
            if word == m:
                self.relatedness[idx]['m1'].append(self.self_relatedness)
                self.relatedness[idx]['m2'].append(0.0)
            else:
                self.relatedness[idx]['m1'].append(float(row[4]))
                self.relatedness[idx]['m2'].append(float(row[5]))

            # save trigram data
            if idx not in self.trigram:
                self.trigram[idx] = {}
                self.trigram[idx]['m1'] = []
                self.trigram[idx]['m2'] = []
            self.trigram[idx]['m1'].append(float(row[6]))
            self.trigram[idx]['m2'].append(float(row[7]))

            # save unigram data
            if idx not in self.unigram:
                self.unigram[idx] = []
            self.unigram[idx].append(float(row[-1]))
        print('done')
        return

    # parse homsophone_unigram* files
    def _parse_unigrams(self, data, puntype):
        print('parsing homophones unigram data...')
        for row in data:
            w1 = row[2].lower()
            if puntype not in self.homo_unigram:
                self.homo_unigram[puntype] = {}
                self.homo_unigram[puntype]['m1'] = {}
                self.homo_unigram[puntype]['m2'] = {}
            self.homo_unigram[puntype]['m1'][w1] = float(row[-2])
            self.homo_unigram[puntype]['m2'][w1] = float(row[-1])
        print('done')
        return


if __name__ == '__main__':
    # load model
    rpaths = ['../data/wordPair_relatedness_smoothedTrigrams_near.csv',
              '../data/wordPair_relatedness_smoothedTrigrams_identical.csv']
    upaths = ['../data/homophones_unigram_near.csv',
              '../data/homophones_unigram_identical.csv']
    puns_data_path = '../data/data-agg.csv'
    model = DataModelV1(rpaths, upaths, puns_data_path)

    # test model on first sample of puns dataset
    print(model.word_vector[0])  # word vector
    print(model.relatedness[0]['m1'])  # relatedness of all words with m1
    print(model.relatedness[0]['m2'])  # relatedness of all words with m2
    print(model.trigram[0]['m1'])  # m1 trigrams
    print(model.trigram[0]['m2'])  # m2 trigrams
    print(model.unigram[0])  # unigrams of all content words
