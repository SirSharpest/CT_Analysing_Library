#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  5 12:09:35 2018

@author: Nathan

"""

from scipy.stats import shapiro as normaltest
from scipy.stats import ttest_ind
import numpy as np
import pymc3 as pm
import pandas as pd
import matplotlib.pyplot as plt


def baysian_hypothesis_test(group1, group2, group1_name, group2_name):
    """
    Implements and uses the hypothesis test outlined as a robust replacement
    for the t-test

    for reference http://www.indiana.edu/~kruschke/BEST/BEST.pdf

    @param group1 a numpy array to test
    @param group2 a numpy array to test
    @param group1_name the name of the first group
    @param group2_name the name of the second group
    @returns a summary dataframe
    """
    if not isinstance(group1, np.ndarray) or not isinstance(group2, np.ndarray):
        raise TypeError

    group1 = np.log10(group1)
    group2 = np.log10(group2)

    y = pd.DataFrame(dict(value=np.r_[group1, group2], group=np.r_[
                     [group1_name]*len(group1), [group2_name]*len(group2)]))

    mu_m = y.value.mean()
    mu_s = y.value.std()*2

    # This model will assume the same distributions
    # are shared across both groups, for simplicity

    with pm.Model() as model:
        group1_mean = pm.Normal('{0}_mean'.format(group1_name), mu_m, sd=mu_s)
        group2_mean = pm.Normal('{0}_mean'.format(group2_name), mu_m, sd=mu_s)

    sig_low = 1
    sig_high = 1000

    with model:
        group1_std = pm.Uniform('{0}_std'.format(
            group1_name), lower=sig_low, upper=sig_high)
        group2_std = pm.Uniform('{0}_std'.format(
            group2_name), lower=sig_low, upper=sig_high)

    with model:
        nu = pm.Exponential('nu_minus_one', 1/29.) + 1

    with model:
        lambda_1 = group1_std**-2
        lambda_2 = group2_std**-2

        group1 = pm.StudentT(group1_name, nu=nu, mu=group1_mean,
                             lam=lambda_1, observed=group1)
        group2 = pm.StudentT(group2_name, nu=nu, mu=group2_mean,
                             lam=lambda_2, observed=group2)

    with model:
        diff_of_means = pm.Deterministic(
            'difference of means', group1_mean - group2_mean)
        diff_of_stds = pm.Deterministic(
            'difference of stds', group1_std - group2_std)
        effect_size = pm.Deterministic('effect size',
                                       diff_of_means / np.sqrt((group1_std**2 + group2_std**2) / 2))

    with model:
        trace = pm.sample(2000, cores=2)

    return trace, pm.summary(trace, varnames=['difference of means',
                                              'difference of stds', 'effect size'])


def check_normality(vals):
    """
    https://stackoverflow.com/a/12839537

    Null Hypothesis is that X came from a normal distribution

    which means:
    If the p-val is very small, it means it is
    unlikely that the data came from a normal distribution

    As for chi-square:
    https://biology.stackexchange.com/questions/13486/deciding-between-chi-square-and-t-test

    @param vals the values to test for normality
    @returns a boolean to indicate if normal or not
    """
    w, p = normaltest(vals)

    if p < 1e-2:
        print(
            'P-value of: {0}\nThat is highly significant\nData is not normally distributed'.format(p))
        return False
    elif p < 5e-1:
        print(
            'P-valueof: {0}\nThat is statistically significant\nData is not normally distributed'.format(p))
        return False
    else:
        print(
            'P-valueof: {0}\nThat is not statistically significant\nData is normally distributed'.format(p))
        return True


def perform_t_test(group1, group2, equal_var=True):
    """
    Performs the standard t-test and returns a p-value

    @param group1 the first group to compare
    @param group2 the second group to compare

    @returns a p-value of the ttest
    """
    t, p = ttest_ind(group1, group2, equal_var=equal_var)
    return p
