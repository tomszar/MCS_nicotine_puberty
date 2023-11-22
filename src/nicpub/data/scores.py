"""
Module with functions that create different scores
"""
import pandas as pd
import nicpub.data.transform as tf


def create_sm_score(dat):
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


def create_pd_score(dat):
    """
    Create Pubertal Development Score, using the mcs6 interview and derived
    files. Remember to have them merged before passing them to this function.

    :param pd.DataFrame dat: Database to use. It should be the mcs6 interview and derived
    merged
    :return: Database with PD score column.
    :rtype: pd.DataFrame
    """
    pub_vars = tf.list_vars('pubertal')
    d = dat[pub_vars.index.tolist() + ['FCCSEX00', 'ID']]  # Add sex and DUI
    pub_vars_boys = list(pub_vars.index.tolist()[i] for i in [0, 1, 2, 5, 6])
    pub_vars_girls = pub_vars.index.tolist()[:5]
    mixed_pvars = [pub_vars_boys, pub_vars_girls]
    for i, s in enumerate([1, 2]):
        sex_dat = d.loc[d['FCCSEX00'] == s, mixed_pvars[i] + ['ID']]
        means = sex_dat[mixed_pvars[i]].mean(axis='columns',
                                             skipna=False)
        means_dui = pd.concat([sex_dat['ID'], means],
                              axis='columns')
        means_dui = means_dui.rename(columns={0: 'PD'})
        if i == 0:
            pd_table = means_dui
        else:
            pd_table = pd.concat([pd_table, means_dui],
                                 axis='rows')
    dat = pd.merge(dat.reset_index(),
                   pd_table,
                   on='ID').set_index('MCSID')
    return dat


def create_pd_cat(dat):
    """
    Create a Pubertal Development category comparing cm to group of same sex
    people six months around birthday.

    :param pd.DataFrame dat: Database to use. Should have at least the
    following columns: DUI, FCCSEX00, and PD
    :return: Database with PDCAT column
    :rtype: pd.DataFrame
    """
    # TODO: optimize this function
    dat['PDCAT'] = 'not_estimated'
    for row, ind in enumerate(dat.index):
        pdcat_bool = dat.columns == 'PDCAT'
        dui = dat.iloc[row, :]['DUI']
        sex = dat.iloc[row, :]['FCCSEX00']
        pd_score = dat.iloc[row, :]['PD']
        same_sex = dat['FCCSEX00'] == sex
        dui_bool = dat.loc[same_sex, 'DUI'].between(dui - 90,
                                                    dui + 90)
        mean_pd = dat[same_sex].loc[dui_bool, 'PD'].mean()
        sd_pd = dat[same_sex].loc[dui_bool, 'PD'].std()
        lower_bound = mean_pd - sd_pd
        upper_bound = mean_pd + sd_pd
        if pd_score > upper_bound:
            dat.iloc[row, pdcat_bool] = 'early'
        elif pd_score < lower_bound:
            dat.iloc[row, pdcat_bool] = 'late'
        elif upper_bound > pd_score > lower_bound:
            dat.iloc[row, pdcat_bool] = 'ontime'
        else:
            dat.iloc[row, pdcat_bool] = 'check'
    return dat
