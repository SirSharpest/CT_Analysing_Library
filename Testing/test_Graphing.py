import pytest
from testing_helper_functions import DATA_FOLDER, EXTRA_INFO, data, data_extra_info
from ct_analysing_library.graphing import InvalidPlot, plot_difference_of_means, plot_forest_plot, plot_boxplot, plot_qqplot, plot_histogram, plot_pca


@pytest.fixture
def trace():
    from ct_analysing_library.statistical_tests import baysian_hypothesis_test
    import numpy as np
    df = data_extra_info().get_data()
    t1 = df['Sample Type'].unique()[0]
    t2 = df['Sample Type'].unique()[1]
    g1 = np.array(df[df['Sample Type'] == t1]['volume'])
    g2 = np.array(df[df['Sample Type'] == t2]['volume'])
    trace, s = baysian_hypothesis_test(g1, g2, t1, t2)
    return trace


def test_plot_difference_of_means(trace):
    plot_difference_of_means(trace)


def test_plot_forest_plot(trace):
    assert 0


def test_plot_boxplot(data_extra_info):
    assert 0


def test_plot_qqplot(data_extra_info):
    assert 0


def test_plot_histogram(data_extra_info):
    assert 0
