#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: Nathan

"""

from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler


def standarise_data(df, features, groupby):
    """
    This is to conform with the likes of PCA, the following text is borrowed from:
    https://towardsdatascience.com/pca-using-python-scikit-learn-e653f8989e60
    Some code also also heavily borrowed from this page and I take minimal credit for it.

    PCA is effected by scale so you need to scale the features in your data before applying PCA. 
    Use StandardScaler to help you standardize the dataset’s features onto unit scale (mean = 0 and variance = 1)
    which is a requirement for the optimal performance of many machine learning algorithms. 
    If you want to see the negative effect not scaling your data can have, scikit-learn has a section
    on the effects of not standardizing your data.

    uses: \dfrac{x_i – mean(x)}{stdev(x)}
    assumes Normal Distribution
    """

    # Separating out the features
    x = df.loc[:, features].values
    # Separating out the target
    y = df.loc[:, [groupby]].values
    # Standardizing the features
    x = StandardScaler().fit_transform(x)


def perform_pca(n_components, df, features, groupby, standardise=False):

"""
This function will perform a PCA and return the principle components as a 
dataframe. 

@param n_components components to check form 
@param df dataframe of the data to analyse 
@param features features from the dataframe to use
@param  groupby the column in the df to use 
@param  standardise=False asks whether to standardise the data prior to PCA

"""
    pass
