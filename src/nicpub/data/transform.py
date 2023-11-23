"""
Different transformations on variables
"""
import numpy as np
import pandas as pd
from functools import reduce


def list_vars(list_type='smoking'):
    """
    Give a list with MCS variables names depending on the type of list required.

    :param str list_type: Type of variables wanted. Default 'smoking'
    (options are 'smoking', 'pubertal', 'pubertal_scores', 'demographic',
    'weights', or 'all')
    :return: Dataframe with variable information or list with variable names
    :rtype: pd.DataFrame or list[str]
    """
    variables = []
    ind_smok = ['APSMMA00', 'APPIOF00', 'APSMTY00', 'APSMEV00', 'APCIPR00',
                'APSMCH00', 'APWHCH00', 'APCICH00', 'APSMKR00', 'CHANGE',
                'SCORE_1', 'SCORE_2', 'SCORE_3', 'SCORE_T']
    d_smok = {
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
                          index=ind_smok),
        'Type': pd.Series(data=['Scale', 'Nominal', 'Nominal', 'Nominal',
                                'Scale', 'Nominal', 'Nominal', 'Scale',
                                'Nominal', 'Scale', 'Scale', 'Scale',
                                'Scale', 'Scale'],
                          index=ind_smok)
        }
    ind_pub = ['FCPUHG00', 'FCPUBH00', 'FCPUSK00', 'FCPUBR00', 'FCPUMN00',
               'FCPUVC00', 'FCPUFH00']
    d_pub = {
        'Name': pd.Series(data=
                          ['CM growth spurt',
                           'CM no body hair',
                           'CM skin changes eg spots',
                           'CM breast growth',
                           'CM started to menstruate',
                           'CM voice change',
                           'CM facial hair'],
                          index=ind_pub),
        'Type': pd.Series(data=['Nominal', 'Nominal', 'Nominal', 'Nominal',
                                'Nominal', 'Nominal', 'Nominal'],
                          index=ind_pub)
        }
    ind_pub_s = ['DUI', 'PD', 'PDCAT']
    d_pub_s = {
        'Name': pd.Series(data=
                          ['Days until interview',
                           'Pubertal development score',
                           'Pubertal development category'],
                          index=ind_pub_s),
        'Type': pd.Series(data=['Scale', 'Scale', 'Nominal'],
                          index=ind_pub_s)
        }
    ind_demo = ['MCSID', 'FCCSEX00']
    d_demo = {
        'Name': pd.Series(data=
                          ['MCS ID',
                           'CM Sex'],
                          index=ind_demo),
        'Type': pd.Series(data=['ID', 'Nominal'],
                          index=ind_demo)
        }
    # List only variables used in the regression
    ind_regression = ['PDCAT', 'PTTYPE2', 'FOVWT2', 'SCORE_1',
                      'SCORE_T', 'AOECDSC0', 'APWTKG00', 'ADDAGB00', 'ADBMIPRE']
    d_regression = {
        'Name': pd.Series(data=
                          ['Pubertal development category',
                           'Stratum within Country',
                           'S6: Overall Weight (inc NR adjustment) whole',
                           'Smoking score during first trimester',
                           'Smoking score during preg',
                           'DV OECD Income Weighted Quintiles (Single Country Analysis)',
                           'Birth weight kilos and grams',
                           'Respondent age at birth of CM',
                           'BMI of respondent before CM born'],
                          index=ind_regression),
        'Type': pd.Series(data=['Scale', 'Nominal', 'Scale', 'Scale', 'Scale',
                                'Nominal', 'Scale', 'Scale', 'Scale'],
                          index=ind_regression)
        }
    if list_type == 'smoking':
        variables = pd.DataFrame(d_smok)
    elif list_type == 'pubertal':
        variables = pd.DataFrame(d_pub)
    elif list_type == 'pubertal_scores':
        variables = pd.DataFrame(d_pub_s)
    elif list_type == 'demographic':
        variables = pd.DataFrame(d_demo)
    elif list_type == 'regression':
        variables = pd.DataFrame(d_regression)
    elif list_type == 'all':
        variables = pd.concat([pd.DataFrame(d_smok),
                               pd.DataFrame(d_pub),
                               pd.DataFrame(d_pub_s),
                               pd.DataFrame(d_demo)],
                              axis=0)
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
    variables = list_vars('all')
    cat_vars = variables[variables['Type'] == 'Nominal']
    cat_mapping = categorical_mapping()
    for var in cat_vars.index:
        if var != 'PDCAT':
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
         'FCCSEX00': {
                      1.0: 'Male',
                      2.0: 'Female'},
         'FCPUHG00': {
                      1.0: 'My growth spurt has not yet begun',
                      2.0: 'My growth spurt has barely started',
                      3.0: 'My growth spurt has definitely started',
                      4.0: 'My growth spurt seems completed'},
         'FCPUBH00': {
                      1.0: 'My body hair has not yet begun to grow',
                      2.0: 'My body hair has barely started to grow',
                      3.0: 'My body hair has definitely started to grow',
                      4.0: 'My body hair growth seems completed'},
         'FCPUSK00': {
                      1.0: 'My skin has not yet started changing',
                      2.0: 'My skin has barely started changing',
                      3.0: 'My skin has definitely started changing',
                      4.0: 'My skin changes seem completed'},
         'FCPUBR00': {
                      1.0: 'My breasts have not yet started to grow',
                      2.0: 'My breasts have barely started to grow',
                      3.0: 'My breasts have definitely started to grow',
                      4.0: 'My breast growth seems completed'},
         'FCPUMN00': {  # Remember that this values are changed right after load
                      3.0: 'Yes',
                      0.0: 'No'},
         'FCPUVC00': {
                      1.0: 'My voice has not yet started getting deeper',
                      2.0: 'My voice has barely started getting deeper',
                      3.0: 'My voice has definitely started getting deeper',
                      4.0: 'My voice change seems completed'},
         'FCPUFH00': {
                      1.0: 'My facial hair has not yet started to grow',
                      2.0: 'My facial hair has barely started to grow',
                      3.0: 'My facial hair has definitely started to grow',
                      4.0: 'My facial hair growth seems completed'},
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


def create_id(dat,
              prefix='AP'):
    """
    Create new unique identifier, ID, by concatenating the MCSID and person
    identifier.

    :param pd.DataFrame dat: Database to use
    :param str prefix: Prefix to identify the person identifier column
    :return: Database with new ID column
    :rtype: pd.DataFrame
    """
    pid_col = prefix + 'NUM00'
    list1 = dat.index.tolist()
    list2 = [str(x) for x in dat.loc[:, pid_col]]
    new_id = pd.Series(reduce(lambda res, l: res + [l[0] + '_' + l[1]],
                              zip(list1, list2), []))
    dat.insert(loc=0,
               column='ID',
               value=new_id.values,
               allow_duplicates=False)
    return dat


def create_dui(dat):
    """
    For MCS 6 sweep, cm derived file, get the days until interview (DUI).

    :param pd.DataFrame dat: Database to use
    :return: Database with DUI column
    :rtype: pd.DataFrame
    """
    # Get DOB info
    d = {'year': dat['FCCDBY00'], 'month': dat['FCCDBM00']}
    dob = pd.DataFrame(d)
    dob['day'] = 15  # Add a default day value
    dob = pd.to_datetime(dob)
    # Get interview date info
    i = {'year': dat['FCINTY00'], 'month': dat['FCINTM00']}
    interview_date = pd.DataFrame(i)
    interview_date['day'] = 15  # Add a default day value
    interview_date = pd.to_datetime(interview_date)
    t = (interview_date - dob) / np.timedelta64(1, 'D')
    # Create new column
    dat['DUI'] = t
    return dat


def lboz_to_kg(dat):
    """
    Convert pounds and oz to kilograms.

    :param pd.DataFrame dat: Database to use. Should be mcs1_parent_cm_interview
    :return: Database with converted units
    :rtype: pd.DataFrame
    """
    new_dat = dat.reset_index().set_index('ID')
    # Convert lb to oz
    oz = new_dat['APWTLB00'] * 16
    oz = oz + new_dat['APWTOU00']
    # Convert oz to kg
    kg = oz * 0.0283495231
    replace_kg = kg.loc[kg > 0]
    replace_kg.name = 'APWTKG00'
    # Remove duplicated index
    replace_kg = replace_kg.groupby(replace_kg.index).first()
    # Update in place
    new_dat.update(replace_kg)
    new_dat = new_dat.reset_index().set_index('MCSID')
    return new_dat


def clean_data(dat):
    """
    Remove rows with NAs

    :param pd.DataFrame dat: Database to use. Preferably, should be the final
    merged database
    :return: Clean database
    :rtype: pd.DataFrame
    """
    variables = list_vars('regression')
    final_dat = dat.reset_index().set_index('ID')
    keep_index = final_dat[variables.index].dropna().index
    final_dat = final_dat.loc[keep_index, :]
    return final_dat
