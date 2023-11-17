import os
import pandas as pd
import nicpub.data.transform as tf
import nicpub.data.scores as sc


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
    Load datasets from MCS sweep 1 and 6, and merge them.

    :return: MCS data from sweep 1 and 6 merged
    :rtype: pd.DataFrame
    """
    # noinspection PyTypeChecker
    dat1 = pd.read_csv('data/raw/tab/mcs1_parent_interview.tab',
                       sep='\t',
                       index_col=0,
                       na_values=[-1.0,  # Not applicable
                                  -8.0,  # Don't know
                                  -9.0])  # Refusal
    dat2 = pd.read_csv('data/raw/tab/mcs6_cm_derived.tab',
                       sep='\t',
                       index_col=0)
    # noinspection PyTypeChecker
    dat3 = pd.read_csv('data/raw/tab/mcs6_cm_interview.tab',
                       sep='\t',
                       index_col=0,
                       na_values=[-1.0,  # Not applicable
                                  -8.0,  # Don't know
                                  -9.0])  # Don't want
    dat3['FCPUMN00'] = dat3['FCPUMN00'].replace({1: 3, 2: 0})
    dat2 = tf.create_dui(dat2)
    dat1 = tf.create_id(dat1)
    dat2 = tf.create_id(dat2, prefix='FC')
    dat3 = tf.create_id(dat3, prefix='FC')
    dat2 = dat2[['ID', 'DUI']]
    # Merge 2 and 3
    dat23 = pd.merge(left=dat2,
                     right=dat3,
                     on='ID',
                     how='inner')
    dat23 = sc.create_pd_score(dat23)
    dat23 = sc.create_pd_cat(dat23)
    # TODO: select correct dtype for columns
    dat1 = tf.change_after_preg(dat1)
    dat1 = sc.create_sm_score(dat1)
    dat = pd.merge(left=dat1,
                   right=dat23,
                   on='ID',
                   how='inner')
    dat = tf.categories_to_str(dat)
    return dat
