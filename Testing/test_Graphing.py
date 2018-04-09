import pytest
from testing_helper_functions import DATA_FOLDER, EXTRA_INFO, data, data_extra_info
from ct_analysing_library.graphing import InvalidPlot, plot_difference_of_means,  plot_boxplot, plot_qqplot, plot_histogram, plot_pca


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
    return (trace, t1, t2)


@pytest.fixture
def split_on_two_sample_types():
    df = data_extra_info().get_data()
    t1 = df['Sample Type'].unique()[0]
    t2 = df['Sample Type'].unique()[1]
    result = df[(df['Sample Type'] == t1) | (df['Sample Type'] == t2)]
    result.reset_index(drop=True, inplace=True)
    return result


def test_plot_difference_of_means(trace):
    plot_difference_of_means(trace[0])


def test_plot_boxplot_as_dataframe(data_extra_info):
    plot_boxplot(data_extra_info.get_data(), 'volume')


def test_plot_boxplot_as_object(data_extra_info):
    plot_boxplot(data_extra_info, 'volume')


def test_plot_qqplot(data_extra_info):
    plot_qqplot(data_extra_info.get_data()['volume'])


def test_plot_histogram_as_object(data_extra_info):
    plot_histogram(data_extra_info, 'volume')


def test_plot_histogram_as_dataframe(data_extra_info):
    plot_histogram(data_extra_info.get_data(), 'volume')


def test_plot_pca(split_on_two_sample_types):
    from ct_analysing_library.data_transforms import perform_pca
    atts = ['length', 'width', 'depth', 'volume',
            'surface_area', 'length_depth_width']
    df, pca = perform_pca(split_on_two_sample_types, atts,
                          'Sample Type', standardise=True)

    g = plot_pca(pca, df, 'Sample Type')
