"""
Fits a linear regression model over the computed measures - ambiguity and
distinctiveness. Groundtruth funniness ratings are obtained from
pun-model/data/data-agg.csv. Regression model summary is printed on console.
"""

import statsmodels.api as sm
import numpy as np
from utils import data2numpy

if __name__ == '__main__':
    # read ground truth funniness ratings
    jokes_data_path = "../../data/data-agg.csv"
    jokes_data = data2numpy(jokes_data_path)
    gt = np.array(jokes_data[:, -1]).astype(float)

    # read ambiguity and distinctiveness measures computed by model
    model_output = data2numpy("../results/data.csv")
    amb = np.array(model_output[:, 4]).astype(float)
    dist = np.array(model_output[:, 5]).astype(float)

    # fit linear regression model
    X = np.stack([amb, dist]).transpose()
    y = gt
    model = sm.OLS(y, X)
    results = model.fit()
    print(results.summary())
