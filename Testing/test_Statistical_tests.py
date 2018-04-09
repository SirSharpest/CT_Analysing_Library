import pytest
from testing_helper_functions import DATA_FOLDER, EXTRA_INFO, data, data_extra_info
from ct_analysing_library.statistical_tests import baysian_hypothesis_test, check_normality, perform_t_test


def test_baysian_hypothesis_test(data_extra_info):
    import numpy as np
    df = data_extra_info.get_data()
    t1 = df['Sample Type'].unique()[0]
    t2 = df['Sample Type'].unique()[1]
    g1 = np.array(df[df['Sample Type'] == t1]['volume'])
    g2 = np.array(df[df['Sample Type'] == t2]['volume'])
    trace, s = baysian_hypothesis_test(g1, g2, t1, t2)


def test_test_normality(data_extra_info):
    check_normality(data_extra_info.get_data()['volume'])


def test_t_test(data_extra_info):
    import numpy as np
    df = data_extra_info.get_data()
    t1 = df['Sample Type'].unique()[0]
    t2 = df['Sample Type'].unique()[1]
    g1 = np.array(df[df['Sample Type'] == t1]['volume'])
    g2 = np.array(df[df['Sample Type'] == t2]['volume'])
    perform_t_test(g1, g2)
