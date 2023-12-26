import subprocess
from nicpub.viz import figs
import nicpub.data.setup as st
import nicpub.data.transform as tf
import nicpub.stats.descriptive as dsc


def create_folders():
    """
    Folder creation routine

    :return: None
    """
    st.setup_folders()

def main():
    """
    Main routine

    :return: None
    """
    dat = st.load_data()
    variables = tf.list_vars('all')
    # TODO: fully remove python summaries
    dsc.summaries(dat,
                  variables)
    figs.summary_plots(dat,
                       variables)
    figs.scatter_plot(dat,
                      variables.loc[['SCORE_T', 'PD'], :])
    figs.violin_cat(dat,
                    variables.loc[['SCORE_T', 'PDCAT'], :],
                    log_transform=True)
    dat.to_csv('data/processed/MCS1.csv')
    subprocess.call(['Rscript', 'src/nicpub/stats/multinom.R'])
    subprocess.call(['Rscript', 'src/nicpub/stats/summaries.R'])
