#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
reated on Mon Feb  5 21:48:07 2018

@author: nathan

This file is for graphing functions that don't yet have a place
in the rest of the program

"""
import scipy.stats as stats
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
plt.style.use('ggplot')  # this is default, make changeable in future


class Error(Exception):
    """Base class for other exceptions"""
    pass


class InvalidPlot(Error):
    """Except to trigger when a graph is given wrong args"""
    pass


def plot_boxplot(data, attribute, **kwargs):
    """
    This should just create a single boxplot and return the figure
    and an axis, useful for rapid generation of single plots
    Rather than the madness of the plural function

    Accepts Kwargs for matplotlib and seaborn
    """
    fig, ax = plt.subplots(1)
    print(attribute)
    sns.boxplot(data=data.get_data(), x=attribute, **kwargs)
    fig.tight_layout()
    return (fig, ax)


def qqplot(vals, plot=None):
    """
    What's a QQ plot?
    https://stats.stackexchange.com/questions/139708/qq-plot-in-python
    """
    z = (vals - np.mean(vals)) / np.std(vals)
    if plot:
        stats.probplot(z, dist="norm", plot=plot)
        plt.title("Normal Q-Q plot")
    else:
        stats.probplot(z, dist="norm", plot=plt)
        plt.title("Normal Q-Q plot")
        plt.show()


def plot_histogram(data, attribute, **kwargs):
    """
    Simple histogram function which accepts
    seaborn and matplotlib kwargs
    returns a plot axes
    """
    ax = plt.subplot(111)
    sns.distplot(data.get_data()[attribute], ax=ax, **kwargs)
    return ax


def plot_pca(dataframe, groupby):
    """
    Plots the PCA of the data given in a 2D plot
    """
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(1, 1, 1)
    ax.set_xlabel('Principal Component 1', fontsize=15)
    ax.set_ylabel('Principal Component 2', fontsize=15)
    ax.set_title('2 component PCA', fontsize=20)
    targets = dataframe[groupby].unique()
    for target in targets:
        indicesToKeep = dataframe[groupby] == target
        ax.scatter(dataframe.loc[indicesToKeep, 'principal component 1'],
                   dataframe.loc[indicesToKeep, 'principal component 2'], s=50)
    ax.legend(targets)
    plt.show()


def check_var_args(arg):
    """
    Helper function to fix bad arguments
    before they get used in evaluations
    """
    if arg.rsplit('=', 1)[1] == '' or arg.rsplit('=', 1)[1] == '\'\'':
        return ''
    arg = ',{0}'.format(arg)
    return arg
