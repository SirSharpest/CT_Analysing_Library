import pytest
from testing_helper_functions import DATA_FOLDER, EXTRA_INFO, data, data_extra_info
from ct_analysing_library.data_transforms import standarise_data, perform_pca, box_cox_data, pca_to_table


def test_standardise_data(data_extra_info):
    standarise_data()


def test_perform_pca(data_extra_info):
    perform_pca()


def test_box_cox_data(data_extra_info):
    box_cox_data()


def test_pca_to_table(data_extra_info):
    pca_to_table()
