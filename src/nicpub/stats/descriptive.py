import pandas as pd


def summaries(dat,
              variables=None):
    """
    Give basic summary information

    :param pd.DataFrame dat: Database to use.
    :param list[str] or None variables: List of variables to select. If None,
    use all columns
    :return: None
    """
    if variables is None:
        for col in dat.columns:
            print(dat.loc[:, col].describe())
    else:
        for var in variables:
            print(dat.loc[:, var].describe())
