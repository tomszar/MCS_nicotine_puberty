import numpy as np
import matplotlib.pyplot as plt


def summary_plots(dat,
                  variables):
    """
    Create a series of histograms or bar plots depending on type of variable.

    :param pd.DataFrame dat: Dataframe where to pull out the data
    :param pd.DataFrame variables: Dataframe of variables to
    select with index as variable code, and variable name and type in columns.
    :return: None
    """
    scales = variables[variables['Type'] == 'Scale']
    nominal = variables[variables['Type'] == 'Nominal']
    bar_plots(dat, nominal)
    hist_boxplots(dat, scales)


def bar_plots(dat,
              variables):
    """
    Create a series of bar plots, providing the dataframe and columns to use.
    Make sure to provide categorical variables.

    :param pd.DataFrame dat: Dataframe where to pull out the data
    :param pd.DataFrane variables: Dataframe with variables to use including
    code and name
    :return: None
    """
    for v in variables.index:
        if v + '_cat' in dat.columns:
            counts = dat[v + '_cat'].value_counts()
        else:
            counts = dat[v].value_counts()
        fig, ax = plt.subplots()
        ax.bar(counts.index,
               counts)
        ax.set_title(variables.loc[v, 'Name'])
        ax.tick_params(axis='x', rotation=70)
        fig.tight_layout()
        fig.savefig('results/figures/' + v + '.pdf')


def hist_boxplots(dat,
                  variables):
    """
    Create a series of histograms with boxplots, providing the dataframe and
    columns to use.
    Make sure to provide continuous variables.

    :param pd.DataFrame dat: Dataframe where to pull out the data
    :param pd.DataFrane variables: Dataframe with variables to use including
    code and name
    :return: None
    """
    for v in variables.index:
        filtered_dat = dat[v][~np.isnan(dat[v])]
        fig, ax = plt.subplots(nrows=2,
                               sharex='all',
                               gridspec_kw={"height_ratios": (.3, .7)})
        # Boxplot
        ax[0].boxplot(filtered_dat,
                      vert=False)
        # Remove borders
        for t in ['top', 'right', 'left']:
            ax[0].spines[t].set_visible(False)
        ax[0].get_yaxis().set_visible(False)
        # Histogram
        ax[1].hist(filtered_dat)
        ax[1].set_title(variables.loc[v, 'Name'])
        # Save fig
        fig.tight_layout()
        fig.savefig('results/figures/' + v + '.pdf',
                    dpi=600)
        plt.close(fig)
