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
    dat = create_scores(dat)
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
               'APSMCH00', 'APWHCH00', 'APCICH00', 'APSMKR00', 'CHANGE',
               'SCORE_1', 'SCORE_2', 'SCORE_3', 'SCORE_T']
        d = {
            'Name': pd.Series(data=
                              ['How many cigarettes per day',
                               'Frequency of pipe smoking',
                               'Smoked in last 2 years',
                               'Ever regularly smoked tobacco products',
                               'Number of cigarettes smoked per day before preg',
                               'Changed number smoked during pregnancy',
                               'When changed smoking habits',
                               'Number smoked per day after change',
                               'Whether anyone smokes in the same room as CM',
                               'Change of n smoked per day before and after',
                               'Smoking score during first trimester',
                               'Smoking score during second trimester',
                               'Smoking score during third trimester',
                               'Smoking score during preg'],
                              index=ind),
            'Type': pd.Series(data=['Scale', 'Nominal', 'Nominal', 'Nominal',
                                    'Scale', 'Nominal', 'Nominal', 'Scale',
                                    'Nominal', 'Scale', 'Scale', 'Scale',
                                    'Scale', 'Scale'],
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
    Make multiple changes to the variables number smoked per day before,
    after pregnancy, and when changed habits.

    Changes include:
    - For respondents that didn't change number smoked during pregnancy
    (APSMCH00), keep the same number as before pregnancy in number smoked per
    day after change (APCICH00).
    - Change the response of number smoked per day after change (APCICH00) from
    96.0 (Less than one a day) to 1, and 97 (can't remember) to NaN.
    - Change value 10 (Can't remember) in variable APWHCH00
    (When changed smoking habits) to rounded average.
    - Create a new variable CHANGE, with the subtraction of before and after
    (after - before)

    :param pd.DataFrame dat: Dataframe to convert
    :return: Dataframe with added values
    :rtype: pd.DataFrame
    """
    # Copy numbers from before to after
    not_changed = dat.loc[:, 'APSMCH00'] == 2
    dat.loc[not_changed, 'APCICH00'] = dat.loc[not_changed, 'APCIPR00']
    # Replace less than one category, to one, and can't remember to NaN
    dat['APCICH00'] = dat['APCICH00'].replace(96, 1)
    dat['APCICH00'] = dat['APCICH00'].replace(97, np.NaN)
    # Replace can't remember month to average
    average = round(dat['APWHCH00'].mean())
    dat['APWHCH00'] = dat['APWHCH00'].replace(10, average)
    # Create CHANGE variable
    dat['CHANGE'] = dat['APCICH00'] - dat['APCIPR00']

    return dat


def create_scores(dat):
    """
    Creates smoking scores during pregnancy, based on the mean number of
    cigarettes smoked while taking into account the month in which they
    changed.
    It generates a total average and separated by trimester.

    :param pd.DataFrame dat: Database to use
    :return: Dataframe with scores added
    :rtype: pd.DataFrame
    """
    # Create new columns
    cols = ['SCORE_1',
            'SCORE_2',
            'SCORE_3',
            'SCORE_T']
    for c in cols:
        dat.loc[:, c] = 0
    # For participants that didn't change, their score is the same as
    # before and after preg always
    not_changed = dat.loc[:, 'APSMCH00'] == 2
    for c in cols:
        dat.loc[not_changed, c] = dat.loc[not_changed, 'APCICH00']
    # For participant that changed, their score is equal to before preg times
    # the month changed, plus after preg times 9 minus month changed, all of
    # that divided by 9
    changed = dat.loc[:, 'APSMCH00'] == 1
    tops = [3, 6, 9]
    for i in range(len(tops)):
        top = tops[i]
        bot = top - 3
        month = dat.loc[changed, 'APWHCH00']
        more = dat.loc[changed, 'APWHCH00'] > top
        less = dat.loc[changed, 'APWHCH00'] < bot
        month[more] = top
        month[less] = bot
        score = ((dat.loc[changed, 'APCIPR00'] * (month - bot)) +
                 (dat.loc[changed, 'APCICH00'] *
                 (top - month))) / 3
        dat.loc[changed, cols[i]] = score
    dat.loc[changed, 'SCORE_T'] = (dat.loc[changed, 'SCORE_1'] +
                                   dat.loc[changed, 'SCORE_2'] +
                                   dat.loc[changed, 'SCORE_3']) / 3
    return dat
