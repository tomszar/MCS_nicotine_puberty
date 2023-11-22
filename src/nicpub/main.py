import subprocess
from nicpub.viz import figs
import nicpub.data.setup as st
import nicpub.data.transform as tf
import nicpub.stats.descriptive as dsc


def main():
    """
    Main routine
    :return: None
    """
    st.setup_folders()
    dat = st.load_data()
    variables = tf.list_vars('all')
    dsc.summaries(dat,
                  variables)
    figs.summary_plots(dat,
                       variables)
    dat.to_csv('data/processed/MCS1.csv')
    subprocess.call(['Rscript', 'src/nicpub/stats/multinom.R'])
