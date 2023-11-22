# MCS_nicotine_puberty
Repo to analyze effects of nicotine exposure on puberty, using the MCS.

## Clone the repository

To clone the repository, open the Terminal, and type:

```bash
git clone https://github.com/tomszar/MCS_nicotine_puberty.git
```

And enter the repository:

```bash
cd MCS_nicotine_puberty
```

## Create the conda environment and install

With [Conda](https://docs.conda.io/en/latest/), or [Mamba](https://mamba.readthedocs.io/en/latest/installation.html) already installed in your system, install the environment using the `environment.yml` file:

```bash
mamba env create -f environment.yml
```

Then, activate the environment, and install the package and dependencies with [poetry](https://python-poetry.org/docs/).

```bash
conda activate nicpub
poetry install
```

## R packages

We use R and some extra packages to run a multinomial with a complex survey design.
Specifically, we use the `svyVGAM` and `srvyr` library.
Although R is installed through conda, `svyVGAM` and `srvyr` cannot. 
Therefore, once the conda env has been created and activated, 
run R and install `svyVGAM` and `srvyr`:

```R
install.packages("svyVGAM")
install.packages("srvyr")
```
