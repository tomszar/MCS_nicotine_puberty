import sys
import pandas as pd


def summaries(dat,
              variables=None):
    """
    Print basic summary information to file.

    :param pd.DataFrame dat: Database to use.
    :param pd.DataFrame or None variables: Dataframe of variables to
    select with index as variable code, and variable name and type in columns.
    If None, use all columns.
    :return: None
    """
    f = open('results/reports/summaries.txt', 'w')
    sys.stdout = f
    if variables is None:
        for col in dat.columns:
            print(dat.loc[:, col].describe())
            print('')
    else:
        scales = variables[variables['Type'] == 'Scale']
        d = {}
        for i in scales.index:
            d[i] = ['min', 'max', 'median', 'mean', 'count']
        print(scales)
        print('')
        print(dat.agg(d).round(2))
        print('')
        nominal = variables[variables['Type'] == 'Nominal']
        for n in nominal.index:
            print(nominal.loc[n, 'Name'])
            print(dat[n + '_cat'].value_counts(dropna=False))
            print('')
    f.close()
