import pytest
from testing_helper_functions import DATA_FOLDER, EXTRA_INFO, data, data_extra_info
from ct_analysing_library.statistical_tests import baysian_hypothesis_test, check_normality


def test_baysian_hypothesis_test(data_extra_info):
    baysian_hypothesis_test()


def test_test_normality(data_extra_info):
    check_normality()


def test_t_test(data_extra_info):
    assert 0


def test_anova(data_extra_info):
    assert 0


def test_manova(data_extra_info):
    assert 0
