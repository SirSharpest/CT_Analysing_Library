import pytest
from testing_helper_functions import DATA_FOLDER, EXTRA_INFO, data, data_extra_info, atts
from ct_analysing_library.data_transforms import standarise_data, perform_pca, box_cox_data, pca_to_table


@pytest.fixture
def split_on_two_sample_types():
    df = data_extra_info().get_data()
    t1 = df['Sample Type'].unique()[0]
    t2 = df['Sample Type'].unique()[1]
    result = df[(df['Sample Type'] == t1) | (df['Sample Type'] == t2)]
    result.reset_index(drop=True, inplace=True)
    return result


def test_standardise_data(split_on_two_sample_types):
    standarise_data(split_on_two_sample_types, atts, 'Sample Type')


def test_perform_pca(split_on_two_sample_types):
    df, pca, d = perform_pca(split_on_two_sample_types, atts,
                             'Sample Type', standardise=True)


def test_box_cox_data(data_extra_info):
    box_cox_data(data_extra_info.get_data().loc[:, atts].values)


def test_pca_to_table(split_on_two_sample_types):
    df, pca, d = perform_pca(split_on_two_sample_types, atts,
                             'Sample Type', standardise=True)
    print(pca_to_table(pca))
