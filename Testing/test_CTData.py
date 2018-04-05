import pytest
from testing_helper_functions import DATA_FOLDER, EXTRA_INFO, data, data_extra_info
from ct_analysing_library.ct_data import CTData, NoDataFoundException


def test_load_data():
    assert CTData(DATA_FOLDER, False) is not None


def test_NoDataFoundException():
    with pytest.raises(NoDataFoundException):
        CTData('/test/no_data_here/', False)


def test_clean_data_maximum_removed(data_extra_info):
    ctd = data_extra_info
    ctd.clean_data()
    assert ctd.get_data()['volume'].max() < 60


def test_clean_data_minimum_removed(data_extra_info):
    ctd = data_extra_info
    ctd.clean_data()
    assert ctd.get_data()['volume'].min() > 3


def test_load_additional_data(data):
    data.get_spike_info(EXTRA_INFO)


def test_load_additional_data_no_data(data):
    with pytest.raises(FileNotFoundError):
        data.get_spike_info('bad_file name.xlsx')


def test_aggregate_spike_averages(data_extra_info):
    data_extra_info.aggregate_spike_averages(
        ['volume', 'length', 'width', 'depth'], groupby='Sample name')
