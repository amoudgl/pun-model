Pun model `v1`
==============

This is a re-implementation of [`v0`](../v0) and it is compatible with python3.

- [`v1/src/main.py`](./src/main.py) implements the core probabilistic model.   
- [`v1/src/models.py`](./src/models.py) implements a `DataModelV1` class which parses the original relatedness, trigram and unigram data released by author.
- Rest of the utility scripts in `v1/src` are borrowed from `v0`.

## Data

This model uses the same data as `v0`. Please go through [`v0/README.md`](../v0/README.md) for more details.

## Instructions to run

Navigate to `src` and run:

```shell
# save measures computed by current model
python main.py -r 13 -s 0
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

All the measures computed exactly match the author's original model `v0/ModelOutputs/data.csv`.

**Linear regression analysis**

```
                          OLS Regression Results                            
==============================================================================
Dep. Variable:                      y   R-squared:                       0.170
Model:                            OLS   Adj. R-squared:                  0.167
Method:                 Least Squares   F-statistic:                     44.50
Date:                Sat, 09 Feb 2019   Prob (F-statistic):           2.67e-18
Time:                        12:00:06   Log-Likelihood:                -496.17
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
