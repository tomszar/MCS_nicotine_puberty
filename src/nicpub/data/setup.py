import os
import pandas as pd


def setup_folders():
    """
    Setup folders by creating data/raw, data/processed, results/figures, and
    results/reports directories.

    :return: None
    """
    parent_data = 'data'
    subdir_data = ['raw', 'processed']

    parent_results = 'results'
    subdir_results = ['figures', 'reports']

    for folder in [parent_data, parent_results]:
        if not os.path.exists(folder):
            os.mkdir(folder)

    for subdir in subdir_data:
        path = os.path.join(parent_data, subdir)
        if not os.path.exists(path):
            os.mkdir(path)

    for subdir in subdir_results:
        path = os.path.join(parent_results, subdir)
        if not os.path.exists(path):
            os.mkdir(path)

    print('Directories created\nRemember to upload the raw data')


def load_data():
    """
    Load datasets.

    :return: MCS data
    :rtype: pd.DataFrame
    """
    dat = pd.read_csv('data/raw/tab/mcs1_parent_interview.tab',
                      sep='\t',
                      index_col=0,
                      na_values=[-1.0,  # Not applicable
                                 -8.0,  # Don't know
                                 -9.0])  # Refusal
    return dat


def list_vars(list_type='smoking'):
    """
    Give a list with MCS variables names depending on the type of list required.

    :param str list_type: Type of variables wanted.
    :return: List of variables
    :rtype: list[str]
    """
    variables = []
    if list_type == 'smoking':
        variables = ['APSMMA00',
                     'APPIOF00',
                     'APSMTY00',
                     'APSMEV00',
                     'APCIPR00',
                     'APSMCH00',
                     'APWHCH00',
                     'APCICH00',
                     'APSMKR00']

    return variables
