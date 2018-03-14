import sys
import pytest
sys.path.append('../ct_analysing_library')

from ct_analysing_library.ct_data import CTData


DATA_FOLDER = ''
EXTRA_INFO = ''


@pytest.fixture
def data():
    """
    Loads example data
    """
    return CTData(folder, rachis)
