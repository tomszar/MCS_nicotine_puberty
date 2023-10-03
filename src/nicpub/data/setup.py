import os
import numpy as np
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
    # TODO: select correct dtype for columns
    dat = categories_to_str(dat)
    dat = change_after_preg(dat)
    return dat


def list_vars(list_type='smoking'):
    """
    Give a list with MCS variables names depending on the type of list required.

    :param str list_type: Type of variables wanted.
    :return: Dataframe with variable information
    :rtype: pd.DataFrame
    """
    variables = []
    if list_type == 'smoking':
        ind = ['APSMMA00', 'APPIOF00', 'APSMTY00', 'APSMEV00', 'APCIPR00',
               'APSMCH00', 'APWHCH00', 'APCICH00', 'APSMKR00', 'CHANGE']
        d = {
            'Name': pd.Series(['How many cigarettes per day',
                               'Frequency of pipe smoking',
                               'Smoked in last 2 years',
                               'Ever regularly smoked tobacco products',
                               'Number of cigarettes smoked per day before preg',
                               'Changed number smoked during pregnancy',
                               'When changed smoking habits',
                               'Number smoked per day after change',
                               'Whether anyone smokes in the same room as CM',
                               'Change of number smoked per day before and after'],
                              index=ind),
            'Type': pd.Series(['Scale', 'Nominal', 'Nominal', 'Nominal',
                               'Scale', 'Nominal', 'Nominal', 'Scale',
                               'Nominal', 'Scale'],
                              index=ind)
            }
        variables = pd.DataFrame(d)
    else:
        Warning('Not correct list_type input')

    return variables


def categories_to_str(dat):
    """
    Add new variables by converting categorical answers from numbers to str in
    dat database.

    :param pd.DataFrame dat: Dataframe to convert
    :return: Dataframe with new categorical variables
    :rtype: pd.DataFrame
    """
    variables = list_vars()
    cat_vars = variables[variables['Type'] == 'Nominal']
    cat_mapping = categorical_mapping()
    for var in cat_vars.index:
        new_column = var + '_cat'
        dat = dat.assign(**{new_column: dat[var].map(cat_mapping[var])})

    return dat


def categorical_mapping():
    """
    Dictionary of the value:label mapping of the categorical variables.

    :return: Mapping dictionary
    :rtype: dict{dict}
    """
    d = {'APPIOF00': {1.0: 'Every day',
                      2.0: '5-6 times per week',
                      3.0: '3-4 times per week',
                      4.0: '1-2 times per week',
                      5.0: '1-2 times per month',
                      6.0: 'Less than once a month'},
         'APSMTY00': {1.0: 'Yes',
                      2.0: 'No'},
         'APSMEV00': {1.0: 'Yes',
                      2.0: 'No'},
         'APSMCH00': {1.0: 'Yes',
                      2.0: 'No',
                      3.0: 'Can\'t remember'},
         'APWHCH00': {1.0: 'First',
                      2.0: 'Second',
                      3.0: 'Third',
                      4.0: 'Fourth',
                      5.0: 'Fifth',
                      6.0: 'Sixth',
                      7.0: 'Seventh',
                      8.0: 'Eighth',
                      9.0: 'Ninth',
                      10.0: 'Can\'t remember'},
         'APSMKR00': {1.0: 'Yes',
                      2.0: 'No'},
         }
    return d


def change_after_preg(dat):
    """
    Make multiple changes to the variables number smoked per day before and
    after pregnancy.

    Changes include:
    - For respondents that didn't change number smoked during pregnancy
    (APSMCH00), keep the same number as before pregnancy in number smoked per
    day after change (APCICH00).
    - Change the response of number smoked per day after change (APCICH00) from
    96.0 (Less than one a day) to 1, and 97 (can't remember) to NaN.
    - Create a new variable CHANGE, with the subtraction of before and after
    (after - before)

    :param pd.DataFrame dat: Dataframe to convert
    :return: Dataframe with added values
    :rtype: pd.DataFrame
    """
    # Copy numbers from before to after
    not_changed = dat.loc[:, 'APSMCH00'] == 2
    dat[not_changed].loc[:, 'APCICH00'] = dat[not_changed].loc[:, 'APCIPR00']
    # Replace less than one category, to one, and can't remember to NaN
    dat['APCICH00'] = dat['APCICH00'].replace(96, 1)
    dat['APCICH00'] = dat['APCICH00'].replace(97, np.NaN)
    # Create CHANGE variable
    dat['CHANGE'] = dat['APCICH00'] - dat['APCIPR00']

    return dat
