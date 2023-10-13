from nicpub.data import setup
from nicpub.stats import descriptive
from nicpub.viz import figs


def main():
    """
    Main routine
    :return: None
    """
    setup.setup_folders()
    mcs1_p_int = setup.load_data()
    variables = setup.list_vars()
    descriptive.summaries(mcs1_p_int,
                          variables)
    figs.summary_plots(mcs1_p_int,
                       variables)
    export_dat = mcs1_p_int.loc[:, variables.index]
    export_dat.to_csv('data/processed/MCS1.csv')
