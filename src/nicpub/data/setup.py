import os
import pandas as pd
from functools import reduce
import nicpub.data.scores as sc
import nicpub.data.transform as tf


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
    # Get MCS1 information and merge them
    # noinspection PyTypeChecker
    mcs1_pi = tf.create_id(pd.read_csv('data/raw/tab/mcs1_parent_interview.tab',
                                       sep='\t',
                                       index_col=0,
                                       na_values=[-1.0,  # Not applicable
                                                  -8.0,  # Don't know
                                                  -9.0]))  # Refusal
    mcs1_pi = tf.change_after_preg(mcs1_pi)
    mcs1_pi = sc.create_sm_score(mcs1_pi)
    smoke_vars = tf.list_vars()
    mcs1_pi = mcs1_pi[['ID'] + smoke_vars.index.tolist()]

    mcs1_fd = pd.read_csv('data/raw/tab/mcs1_family_derived.tab',
                          sep='\t',
                          index_col=0,
                          usecols=['MCSID',
                                   'AOECDSC0'])
    # noinspection PyTypeChecker
    mcs1_pci = tf.create_id(pd.read_csv('data/raw/tab/mcs1_parent_cm_interview.tab',
                                        sep='\t',
                                        index_col=0,
                                        usecols=['MCSID',
                                                 'APNUM00',
                                                 'APBIWT00',
                                                 'APWTLB00',
                                                 'APWTOU00',
                                                 'APWTKG00'],
                                        na_values=[-1.0,  # Not applicable
                                                   -8.0,  # Don't know
                                                   -9.0]))  # Refusal))
    mcs1_pci = tf.lboz_to_kg(mcs1_pci)
    # noinspection PyTypeChecker
    mcs1_pd = tf.create_id(pd.read_csv('data/raw/tab/mcs1_parent_derived.tab',
                                       sep='\t',
                                       index_col=0,
                                       usecols=['MCSID',
                                                'APNUM00',
                                                'ADDAGB00',
                                                'ADBMIPRE'],
                                       na_values=[-1.0,  # Not applicable
                                                  -2.0,  # Not known
                                                  -8.0,  # Don't know
                                                  -9.0]))  # Refusal))))
    dats = [mcs1_pi.reset_index(), mcs1_pci, mcs1_pd]
    mcs1 = reduce(lambda left, right: pd.merge(left, right, on=['ID'],
                                               how='inner'),
                  dats).set_index('MCSID')
    mcs1 = pd.merge(mcs1, mcs1_fd, right_index=True, left_index=True)

    # Get MCS6 information
    mcs6_cmd = tf.create_id(pd.read_csv('data/raw/tab/mcs6_cm_derived.tab',
                                        sep='\t',
                                        index_col=0,
                                        usecols=['MCSID',
                                                 'FCNUM00',
                                                 'FCCDBY00',
                                                 'FCCDBM00',
                                                 'FCINTY00',
                                                 'FCINTM00']),
                            prefix='FC')
    mcs6_cmd = tf.create_dui(mcs6_cmd)
    mcs6_cmd = mcs6_cmd[['ID', 'DUI']]
    pub_vars = tf.list_vars('pubertal')
    # noinspection PyTypeChecker
    mcs6_cmi = tf.create_id(pd.read_csv('data/raw/tab/mcs6_cm_interview.tab',
                                        sep='\t',
                                        index_col=0,
                                        na_values=[-1.0,  # Not applicable
                                                   -8.0,  # Don't know
                                                   -9.0],  # Don't want
                                        usecols=['MCSID',
                                                 'FCNUM00',
                                                 'FCCSEX00'] + \
                                                pub_vars.index.tolist()),
                            prefix='FC')
    mcs6_cmi['FCPUMN00'] = mcs6_cmi['FCPUMN00'].replace({1: 3, 2: 0})
    # Merge sweep 6 and create PD scores
    mcs6 = pd.merge(mcs6_cmd.reset_index(),
                    mcs6_cmi,
                    on='ID',
                    how='inner').set_index('MCSID')
    mcs6 = sc.create_pd_score(mcs6)
    mcs6 = sc.create_pd_cat(mcs6)

    # Merge sweeps 1 and 6
    mcs16 = pd.merge(mcs1.reset_index(),
                     mcs6,
                     on='ID',
                     how='inner').set_index('MCSID')

    # Get across sweeps information
    mcsl_ff = pd.read_csv('data/raw/tab/mcs_longitudinal_family_file.tab',
                          sep='\t',
                          index_col=0,
                          usecols=['MCSID',
                                   'PTTYPE2',
                                   'FOVWT2'])
    # Merge sweeps 1-6 with longitudinal family file on index
    mcs = pd.merge(mcs16,
                   mcsl_ff,
                   left_index=True,
                   right_index=True)
    dat = tf.categories_to_str(mcs)
    return dat
