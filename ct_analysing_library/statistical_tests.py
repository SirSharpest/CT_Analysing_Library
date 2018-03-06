#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  5 12:09:35 2018

@author: Nathan

"""

from scipy.stats import shapiro as normaltest
import matplotlib.pyplot as plt
import numpy as np


def test_normality(vals):
    """
    https://stackoverflow.com/a/12839537

    Null Hypothesis is that X came from a normal distribution

    which means:
    If the p-val is very small, it means it is 
    unlikely that the data came from a normal distribution

    As for chi-square: 
    https://biology.stackexchange.com/questions/13486/deciding-between-chi-square-and-t-test
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
