from nicpub.data import setup
from nicpub.stats import descriptive


def main():
    """
    Main routine
    :return: None
    """
    setup.setup_folders()
    mcs1_p_int = setup.load_data()
    variables = setup.list_vars()
    print(mcs1_p_int.loc[:, variables].head())
    descriptive.summaries(mcs1_p_int,
                          variables)

