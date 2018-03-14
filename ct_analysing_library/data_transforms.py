#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: Nathan

"""
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import pandas as pd
from numpy import log10


def box_cox_data(df, features, groupby):
    """
    The powers or Box_Cox transform
    https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.boxcox.html

    Appears to be something which could really help with the kind of skewed data which this
    library seeks to assist with.
    """
    pass


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
    # Attempt to normalise
    x = log10(x)
    # Standardizing the features
    x = StandardScaler().fit_transform(x)
    return x


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
    pca = PCA(n_components=2)
    principalComponents = pca.fit_transform(
        standarise_data(df, features, groupby) if standardise else df.loc[:, features].values)
    principalDf = pd.DataFrame(data=principalComponents, columns=[
                               'principal component 1', 'principal component 2'])

    finalDf = pd.concat([principalDf, df[[groupby]]], axis=1)

    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(1, 1, 1)
    ax.set_xlabel('Principal Component 1', fontsize=15)
    ax.set_ylabel('Principal Component 2', fontsize=15)
    ax.set_title('2 component PCA', fontsize=20)
    targets = df[groupby].unique()
    for target in targets:
        indicesToKeep = finalDf[groupby] == target
        ax.scatter(finalDf.loc[indicesToKeep, 'principal component 1'],
                   finalDf.loc[indicesToKeep, 'principal component 2'], s=50)
    ax.legend(targets)
    # ax.grid()
    plt.show()
