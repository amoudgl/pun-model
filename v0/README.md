Pun model `v0`
==============

I cloned the author's original repository `justinek/pun-paper`, cleaned it up and dubbed it as `v0`.

**Clean up steps**

- Removed `userConfusability` [argument](https://github.com/justinek/pun-paper/blob/master/ModelScripts/computeMeasures.py#L13) since it was not used in the final version of the paper.
- Removed `depuns` from [`wordPair_relatedness_smoothedTrigrams_identical.csv`](https://github.com/justinek/pun-paper/blob/master/ProcessedData/wordPair_relatedness_smoothedTrigrams_identical.csv#L359-L582) since my focus was to reproduce results for puns and nonpuns.
- Removed all the tex files, csv files and utility scripts which were not used to reproduce measures.

## Data

`v0` uses the following data files (all present in `v0/ProcessedData/`):
- [`wordPair_relatedness_smoothedTrigrams_identical.csv`](./ProcessedData/wordPair_relatedness_smoothedTrigrams_identical.csv`): Contains relatedness and trigram data for all the "identical" puntype sentences.
- [`wordPair_relatedness_smoothedTrigrams_near.csv`](./ProcessedData/wordPair_relatedness_smoothedTrigrams_near.csv):  Contains relatedness and trigram data for all the "near" puntype sentences.
- [`homophones_unigram_identical.csv`](./ProcessedData/homophones_unigram_identical.csv): Contains unigram frequency of the two meanings for each "identical" puntype sentence in dataset.
- [`homophones_unigram_near.csv`](./ProcessedData/homophones_unigram_near.csv): Contains unigram frequency of the two meanings for each "near" puntype sentence in dataset.
- [`data-agg.csv`](../data/data-agg.csv) (puns dataset): Contains 435 sentences (145 puns + 290 nonpuns) along with groundtruth funniness ratings, two meanings [`m1`, `m2`] (think of them as two possible interpretations) for each pun/nonpun, ambiguity and distinctiveness computed by model, focus words for each meaning etc.

Since, I'm mainly interested in reproducing ambiguity and distinctiveness measures for each sentence in the puns dataset, I extracted them from `data-agg.csv` and generated a [`pun-model/data/data-agg-measures.csv`](../data/data-agg-measures.csv) containing 5 columns as described below:

`idx`: index of sentence in puns dataset.   
`sentenceID`: index of near or identical puntype sentence.   
`punType`: near or identical.   
`sentenceType`: pun or nonpun.   
`ambiguity`: original ambiguity measure computed by author.   
`distinctiveness`: original distinctiveness measure by author.    
`sentence`: sentence.

### Important Note

We will treat `pun-model/data/data-agg-measures.csv` as the groundtruth. It is used to compare different experiments in this repository. Each experiment generates a `data.csv` which has the same format as `data-agg-measures.csv`.

## Instructions to run

Navigate to `v0/ModelScripts` and run:

```shell
# compute ambiguity and dinstictiveness for "near" type puns/nonpuns
python computeMeasures.py near 1 13 0

# compute ambiguity and dinstictiveness for "identical" type puns/nonpuns
python computeMeasures.py identical 1 13 0
```

**Arguments:**
1. `punType` (string):    
      Possible values: `["near", "identical"]`     
      Evaluate model on near or identical puntype sentences. Based on the input, it will fetch respective relatedness `wordPair_relatedness*` and unigram data `homophones_unigram*`.
2. `useTrigrams` (bool)
      Possible values: `[0, 1]`    
      Whether to use trigram or unigram for the noise component in generative model.
3. `self_relatedness` (float)   
      Possible values: `[-inf, inf]`     
      Relatedness of a meaning word with itself. In the paper, it is set to 13.
4. `scaling_parameter` (float)    
      Possible values: `[-inf, inf]`    
      Scale relatedness values (on exponential scale) by this factor. It is set to 1 by default, implying no scaling (exp(0) = 1).

Finally, run the following command to get a single sheet `v0/ModelOutputs/data.csv` containing results:

```shell
# save measures in a csv file
python merge_results.py  
```

To fit a simple linear regression on the generated ambiguity and distinctiveness [`data.csv`] by model for getting funniness ratings, do:

```shell
# simple linear regression analysis
python regression_analysis.py   
```

## Results

Ambiguity and distinctiveness values computed by this model `v0` exactly match the groundtruth `data/data-agg-measures.csv`.

**Linear regression analysis**

```
                           OLS Regression Results                            
==============================================================================
Dep. Variable:                      y   R-squared:                       0.170
Model:                            OLS   Adj. R-squared:                  0.167
Method:                 Least Squares   F-statistic:                     44.50
Date:                Wed, 06 Feb 2019   Prob (F-statistic):           2.67e-18
Time:                        20:08:23   Log-Likelihood:                -496.17
No. Observations:                 435   AIC:                             996.3
Df Residuals:                     433   BIC:                             1004.
Df Model:                           2                                         
Covariance Type:            nonrobust                                         
==============================================================================
coef    std err          t      P>|t|      [95.0% Conf. Int.]
------------------------------------------------------------------------------
x1             2.0866      0.223      9.360      0.000         1.648     2.525
x2            -0.0129      0.005     -2.535      0.012        -0.023    -0.003
==============================================================================
Omnibus:                       60.789   Durbin-Watson:                   1.817
Prob(Omnibus):                  0.000   Jarque-Bera (JB):               84.899
Skew:                           1.081   Prob(JB):                     3.67e-19
Kurtosis:                       3.088   Cond. No.                         47.3
==============================================================================

```
