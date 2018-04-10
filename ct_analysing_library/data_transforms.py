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
import pylab as pl


def box_cox_data(values_array):
    """
    The powers or Box_Cox transform

    Appears to be something which could really help with the kind of skewed data which this
    library seeks to assist with.

    @param values_array a numpy array of numbers to be transformed
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

    @param df the data to be standarised
    @param features the list of features to standardise
    @param groupby how the columns should be grouped
    @returns scaled values
    """
    # Separating out the features
    x = df.loc[:, features].values

    # Attempt to normalise through power transforms
    box_cox_data(x)

    # Standardizing the features
    x = StandardScaler().fit_transform(x)
    return x


def perform_pca(df, features, groupby, groupby2=None, groupby3=None, standardise=False):
    """
    This function will perform a PCA and return the principle components as a
    dataframe.

    Read: https://stackoverflow.com/questions/22984335/recovering-features-names-of-explained-variance-ratio-in-pca-with-sklearn

    @param n_components components to check form
    @param df dataframe of the data to analyse
    @param features features from the dataframe to use
    @param groupby the column in the df to use
    @param standardise=False asks whether to standardise the data prior to PCA
    @returns a dataframe of the data, the pca object and the scaled data for reference
    """
    pca = PCA(n_components=2)
    data = standarise_data(
        df, features, groupby) if standardise else df.loc[:, features].values
    principalComponents = pca.fit_transform(data)

    principalDf = pd.DataFrame(data=principalComponents, columns=[
                               'principal component 1', 'principal component 2'])

    if groupby2 is None:
        return (pd.concat([principalDf, df[[groupby]]], axis=1), pca, data)
    if groupby3 is None:
        return (pd.concat([principalDf, df[[groupby]], df[[groupby2]]], axis=1), pca, data)
    else:
        return (pd.concat([principalDf, df[[groupby]], df[[groupby2]], df[[groupby3]]], axis=1), pca, data)


def pca_to_table(pca):
    """
    Creates a dataframe of the PCA weights for each
    attribute

    https://stackoverflow.com/questions/22984335/recovering-features-names-of-explained-variance-ratio-in-pca-with-sklearn
    @returns a pca table
    """
    return pca
