Pun model `v2`
==============

This is the final version of the pun model and it is built on top of [`v1`](../v1). Following are the updates from [`v1`](../v1):

- Relatedness and unigram data are cleaned and saved in a new format. All the cleanup scripts can be found in [`v2/cleanup`](./cleanup) directory.
- New data model class is written in [`v2/src/models.py`](./src/models.py) which parses the cleaned data.
- Fixes implementation bugs in [`v0`](../v0).
- Due to data cleanup, this model doesn't exactly reproduce ambiguity and distinctiveness values for sentences in puns dataset. However, with some hyperparamter tuning, I get slightly better results (R-squared value in linear regression analysis) than the author's implementation.


## Issues in [`v0`](../v0)

**Relatedness data**

- Ideally, relatedness between two words should be a single constant value. In the author's relatedness data files  `wordPair_relatedness_smoothedTrigrams_near.csv` and `wordPair_relatedness_smoothedTrigrams_identical.csv`, I found many pairs had multiple relatedness values.
- All such pairs can be found in this [cleanup log](./cleanup/clean_relatedness_data.log).
- I just picked one relatedness value for pairs having multiple such values since they didn't differ much. View [relatedness cleanup script](./cleanup/clean_relatedness_data.py) for more details.

**Unigram data**

- Author's implementation uses two unigram data files: [`homophones_unigram_identical.csv`](../v0/ProcessedData/homophones_unigram_identical.csv), [`homophones_unigram_near.csv`](../v0/ProcessedData/homophones_unigram_near.csv). I found out that the data is not consistent for some words i.e. if the same word appears in these two files, its unigram frequencies in these two files are different.
- All such words with multiple unigram frequencies can be found in this [cleanup log](./cleanup/clean_unigram_data.log).
- Following the same strategy as the above relatedness data section, I picked one unigram value for words with multiple unigram frequencies. View [unigram cleanup script](./cleanup/clean_unigram_data.py) for more details.

**Implementation bugs**

- [Bug 1](../v0/ModelScripts/computeMeasures.py#L238-L240): These three lines L238-L240 in author's implementation `v0/ModelScripts/computeMeasures.py` should be indented, i.e. they should be inside the for loop. Basically, these three lines sum `P(m,f | w)` for each focus vector `f` and a meaning word `m`. Hence, it should be inside the loop which iterates over all the focus vectors.
- [Bug 2](../v0/ModelScripts/computeMeasures.py#L52-L56): Each row in author's unigram data contains two meanings (`m1` and `m2`) and their unigram frequencies. In author's implementation, two dictionaries namely, `m1ProbDict` and `m2ProbDict` are constructed to parse this data but the key to *both* dictionaries is `m1`. This causes an issue when there are pairs with the same `m1` but different `m2`. Example of such pairs from the dataset: [`traumatic`, `dramatic`]; [`traumatic`, `grammatic`].


## Data

The pun model `v2` uses the following data files:

- [`relatedness_clean.csv`](./data/relatedness_clean.csv): Each line contains a word pair and its relatedness.
- [`unigrams_clean.csv`](./data/unigrams_clean.csv): Each line contains a word and its unigram frequency.
- [`trigrams_clean.csv`](./data/trigrams_clean.csv): It has the format `idx,word,m1_trigram,m2_trigram`. `idx` refers to index of sentence in the puns dataset.


## Instructions to run

Navigate to `src` and run:

```shell
# save measures computed by current model
python main.py -r 15 -s 0
```
Ambiguity and distinctiveness measures for each sentence will be saved in `v1/results/data.csv`.

**Arguments:**

`-r / --self-relatedness`: Relatedness of a meaning word with itself. In the paper, it is set to 13.     
`-s / --scaling-parameter`: Scale relatedness values (on exponential scale) by this factor. It is set to 1 by default, implying no scaling (exp(0) = 1).    

To fit a simple linear regression on the generated ambiguity and distinctiveness measures [`v1/results/data.csv`], do:

```shell
# simple linear regression analysis
python regression_analysis.py   
```
## Results

We get a slightly better fit (judging by R-squared) than author's implementation at self relatedness value (r) = 15.

**`v2` linear regression results (r = 15):**
```shell
                            OLS Regression Results                            
==============================================================================
Dep. Variable:                      y   R-squared:                       0.174
Model:                            OLS   Adj. R-squared:                  0.170
Method:                 Least Squares   F-statistic:                     45.68
Date:                Tue, 05 Feb 2019   Prob (F-statistic):           1.00e-18
Time:                        20:36:32   Log-Likelihood:                -495.18
No. Observations:                 435   AIC:                             994.4
Df Residuals:                     433   BIC:                             1003.
Df Model:                           2                                         
Covariance Type:            nonrobust                                         
==============================================================================
coef    std err          t      P>|t|      [95.0% Conf. Int.]
------------------------------------------------------------------------------
x1             2.2145      0.233      9.498      0.000         1.756     2.673
x2            -0.0113      0.004     -2.523      0.012        -0.020    -0.002
==============================================================================
Omnibus:                       62.079   Durbin-Watson:                   1.856
Prob(Omnibus):                  0.000   Jarque-Bera (JB):               87.376
Skew:                           1.097   Prob(JB):                     1.06e-19
Kurtosis:                       3.086   Cond. No.                         56.0
==============================================================================
```

**`v2` linear regression results (r = 13):**
```shell
                            OLS Regression Results                            
==============================================================================
Dep. Variable:                      y   R-squared:                       0.144
Model:                            OLS   Adj. R-squared:                  0.140
Method:                 Least Squares   F-statistic:                     36.52
Date:                Tue, 05 Feb 2019   Prob (F-statistic):           2.21e-15
Time:                        20:36:23   Log-Likelihood:                -502.92
No. Observations:                 435   AIC:                             1010.
Df Residuals:                     433   BIC:                             1018.
Df Model:                           2                                         
Covariance Type:            nonrobust                                         
==============================================================================
coef    std err          t      P>|t|      [95.0% Conf. Int.]
------------------------------------------------------------------------------
x1             1.8063      0.213      8.469      0.000         1.387     2.225
x2            -0.0123      0.005     -2.350      0.019        -0.023    -0.002
==============================================================================
Omnibus:                       57.440   Durbin-Watson:                   1.754
Prob(Omnibus):                  0.000   Jarque-Bera (JB):               79.024
Skew:                           1.044   Prob(JB):                     6.92e-18
Kurtosis:                       2.979   Cond. No.                         44.6
==============================================================================
```
