#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: Nathan

"""
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from scipy.stats import boxcox
import pandas as pd
import numpy as np
from numpy import log10


def box_cox_data(values_array):
    """
    The powers or Box_Cox transform

    Appears to be something which could really help with the kind of skewed data which this
    library seeks to assist with.
    """
    for c in values_array.T:
        c = boxcox(c)


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

    To try and fit a normal distribution I am applying log scales of log_2
    """
    # Separating out the features
    x = df.loc[:, features].values

    # Attempt to normalise through power transforms
    box_cox_data(x)

    # Standardizing the features
    x = StandardScaler().fit_transform(x)
    return x


def perform_pca(n_components, df, features, groupby, standardise=False):
    """
    This function will perform a PCA and return the principle components as a
    dataframe.

    Read: https://stackoverflow.com/questions/22984335/recovering-features-names-of-explained-variance-ratio-in-pca-with-sklearn

    @param n_components components to check form
    @param df dataframe of the data to analyse
    @param features features from the dataframe to use
    @param  groupby the column in the df to use
    @param  standardise=False asks whether to standardise the data prior to PCA

    """
    pca = PCA(n_components=2)
    principalComponents = pca.fit_transform(
        standarise_data(df, features, groupby) if standardise else df.loc[:, features].values)

    principalDf = pd.DataFrame(data=principalComponents, columns=[
                               'principal component 1', 'principal component 2'])

    return (pd.concat([principalDf, df[[groupby]]], axis=1), pca)
