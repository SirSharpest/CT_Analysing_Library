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
from pandas import DataFrame
import pymc3 as pm
plt.style.use('ggplot')  # this is default, make changeable in future


class Error(Exception):
    """Base class for other exceptions"""
    pass


class InvalidPlot(Error):
    """Except to trigger when a graph is given wrong args"""
    pass


def plot_difference_of_means(trace, **kwargs):
    ps1 = pm.plot_posterior(trace, varnames=['difference of means'],
                            ref_val=0,
                            color='#87ceeb', **kwargs)
    return ps1


def plot_forest_plot(trace, name1, name2):
    fp1 = pm.forestplot(trace, varnames=[name1, name2], rhat=False)
    return fp1


def plot_boxplot(data, attribute, **kwargs):
    """
    This should just create a single boxplot and return the figure
    and an axis, useful for rapid generation of single plots
    Rather than the madness of the plural function

    Accepts Kwargs for matplotlib and seaborn
    """
    fig, ax = plt.subplots(1)
    if type(data) is not DataFrame:
        sns.boxplot(data=data.get_data(), x=attribute, **kwargs)
    else:
        sns.boxplot(data=data, x=attribute, **kwargs)
    fig.tight_layout()
    return (fig, ax)


def plot_qqplot(vals, plot=None):
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


def plot_histogram(data, attribute, **kwargs):
    """
    Simple histogram function which accepts
    seaborn and matplotlib kwargs
    returns a plot axes
    """
    if type(data) is not DataFrame:
        ax = plt.subplot(111)
        sns.distplot(data.get_data()[attribute], ax=ax, **kwargs)
    else:
        ax = plt.subplot(111)
        sns.distplot(data[attribute], ax=ax, **kwargs)
    return ax


def plot_pca(pca, dataframe, groupby, single_plot=False):
    """
    Plots the PCA of the data given in a 2D plot
    """
    if not single_plot:
        g = sns.lmplot(data=dataframe, x='principal component 1',
                       y='principal component 2', hue=groupby, fit_reg=False, col=groupby, scatter_kws={'alpha': 0.6}, size=7, aspect=1.5)
    else:
        g = sns.lmplot(data=dataframe, x='principal component 1',
                       y='principal component 2', hue=groupby, fit_reg=False, scatter_kws={'alpha': 0.6}, size=7, aspect=1.5)

    g.set_xlabels(
        'Principal Component 1 - %{0:.2f}'.format(pca.explained_variance_ratio_[0] * 100), fontsize=15)
    g.set_ylabels(
        'Principal Component 2 - %{0:.2f}'.format(pca.explained_variance_ratio_[1] * 100), fontsize=15)
    g.fig.suptitle('2 component PCA total explained: %{0:.2f}'.format(
        pca.explained_variance_ratio_.cumsum()[1] * 100))
    return g


def check_var_args(arg):
    """
    Helper function to fix bad arguments
    before they get used in evaluations
    """
    if arg.rsplit('=', 1)[1] == '' or arg.rsplit('=', 1)[1] == '\'\'':
        return ''
    arg = ',{0}'.format(arg)
    return arg
