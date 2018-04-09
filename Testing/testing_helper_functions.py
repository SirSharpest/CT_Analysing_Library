import sys
sys.path.append('./ct_analysing_library/')
import pytest
from ct_analysing_library.ct_data import CTData, NoDataFoundException

# Some globals that are needed for loading in the data
DATA_FOLDER = 'Testing/Test_Data/'
EXTRA_INFO = 'Testing/Test_Files/extra_information.xlsx'


@pytest.fixture
def data():
    """
    Loads example data
    """
    return CTData(DATA_FOLDER, False)


@pytest.fixture
def data_extra_info():
    ctd = CTData(DATA_FOLDER, False)
    ctd.get_spike_info(EXTRA_INFO)
    ctd.clean_data()
    ctd.fix_colnames()
    return ctd
