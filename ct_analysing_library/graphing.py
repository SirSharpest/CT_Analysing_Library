#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Mon Feb  5 21:48:07 2018

@author: nathan

This file is for graphing functions that don't yet have a place
in the rest of the program

"""
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from scipy.stats import shapiro as normaltest
plt.style.use('ggplot')  # this is default, make changeable in future


class Error(Exception):
    """Base class for other exceptions"""
    pass


class InvalidPlot(Error):
    """Except to trigger when a graph is given wrong args"""
    pass


def percentile_grid(dataframe, attributes):
    fig, axes = plt.subplots(2, 4, sharex=True)
    for idx, att in enumerate(attributes):
        x = idx // 4
        y = idx % 4
        percentiles = [np.percentile(dataframe[att], i)
                       for i in range(1, 100)]
        axes[x, y].bar(np.arange(1, 100), percentiles)
        axes[x, y].set_title(att)

        if x < 0:
            axes[x, y].set_xlabel('')
        else:
            axes[x, y].set_xlabel('Percentile')

        if y == 0 or y == 4:
            axes[x, y].set_ylabel('Value of {0}'.format(att))
        else:
            axes[x, y].set_ylabel('')

    return (fig, axes)


def qq_grid(dataframe, attributes):
    fig, axes = plt.subplots(2, 4, sharex=True, sharey=True)
    for idx, att in enumerate(attributes):
        x = idx // 4
        y = idx % 4

        # Convert everything to log10 for this
        qqplot(np.log10(dataframe[att]), plot=axes[x, y])
        axes[x, y].set_title(att)

        if x < 0:
            axes[x, y].set_xlabel('')

        if y == 0 or y == 4:
            axes[x, y].set_ylabel('Ordered Values')
        else:
            axes[x, y].set_ylabel('')

        axes[x, y].get_lines()[0].set_marker('o')
        axes[x, y].get_lines()[0].set_markerfacecolor('white')
        w, p = normaltest(dataframe[att])

        if p < 1e-2:
            p = '<0.01'
        elif p < 5e-1:
            p = '<0.05'
        else:
            p = '>0.05'

        axes[x, y].text(1, -6, r'$P${0}'.format(p))
    return (fig, axes)


def plot_boxplot(df, attribute, x_var='Sample name', hue='None'):
    """
    This should just create a single boxplot and return the figure
    and an axis, useful for rapid generation of single plots
    Rather than the madness of the plural function
    """
    fig, ax = plt.subplots(1)
    print(attribute)
    sns.boxplot(data=df, x=attribute, y=x_var, ax=ax)
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


def plot_boxplots(df, attributes, x_var='Sample name', hue='', one_legend=False):
    try:
        hue = check_var_args('hue=\'{0}\''.format(hue))
        x_var = check_var_args('x=\'{0}\''.format(x_var))
        fig, axes = plt.subplots(2, 4, sharex=True)
        for idx, att in enumerate(attributes):
            x = idx // 4
            y = idx % 4
            func_template = 'sns.boxplot(data=df, y=att, ax=axes[x,y] {0}{1})'
            print(func_template.format(x_var, hue))
            eval(func_template.format(x_var, hue))

            if one_legend:
                axes[x, y].legend().set_visible(False)
                if x == 0 and y == 3:
                    axes[x, y].legend().set_visible(True)

        return (fig, axes)
    except:
        raise InvalidPlot


def plot_histogram(df, attribute, norm_hist=True, kde=False):
    """
    Simple histogram function

    returns a plot axes 
    """
    ax = plt.subplot(111)
    sns.distplot(df[attribute], ax=ax, norm_hist=norm_hist, kde=kde)
    return ax


def check_var_args(arg):
    """
    Helper function to fix bad arguments
    before they get used in evaluations
    """
    if arg.rsplit('=', 1)[1] == '' or arg.rsplit('=', 1)[1] == '\'\'':
        return ''
    arg = ',{0}'.format(arg)
    return arg


