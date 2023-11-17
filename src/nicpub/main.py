from nicpub.viz import figs
import nicpub.data.setup as st
import nicpub.stats.descriptive as dsc
import nicpub.data.transform as tf


def main():
    """
    Main routine
    :return: None
    """
    st.setup_folders()
    mcs1_p_int = st.load_data()
    variables = tf.list_vars('all')
    dsc.summaries(mcs1_p_int,
                  variables)
    figs.summary_plots(mcs1_p_int,
                       variables)
    export_dat = mcs1_p_int.loc[:, ['ID'] + variables.index.tolist()]
    export_dat.to_csv('data/processed/MCS1.csv')
