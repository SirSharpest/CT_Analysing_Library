import sys
import pytest
sys.path.append('ct_analysing_library/')

from ct_analysing_library.ct_data import CTData, NoDataFoundException

# Some globals that are needed for loading in the data
DATA_FOLDER = 'Test_Data/'
EXTRA_INFO = 'Test_Files/extra_information.xlsx'


@pytest.fixture
def data():
    """
    Loads example data
    """
    return CTData(DATA_FOLDER, False)


def test_load_data():
    assert CTData(DATA_FOLDER, False) is not None


def test_NoDataFoundException():
    with pytest.raises(NoDataFoundException):
        CTData('/test/no_data_here/', False)
