#
# Script for multinomial regression in R with complex survey designs
#
suppressPackageStartupMessages({
  library(svyVGAM)
  library(srvyr)
  library(survey)
})

# Read data
dat <- read.csv("data/processed/MCS1.csv")
options(survey.adjust.domain.lonely=TRUE)
options(survey.lonely.psu="adjust")
# Relevel and set factors
dat$PDCAT <- as.factor(dat$PDCAT)
dat$PDCAT <- relevel(dat$PDCAT,
                     ref="ontime")
dat$AOECDSC0 <- as.factor(dat$AOECDSC0)
# Sex stratify
dat_m <- dat[dat["FCCSEX00_cat"] == "Male", ]
dat_f <- dat[dat["FCCSEX00_cat"] == "Female", ]

# Regression and survey design
df_list <- list(dat_f, dat_m)
titles <- list("=== REGRESSION MODEL IN FEMALES ===",
               "=== REGRESSION MODEL IN MALES ===")
sink("results/reports/multinomial_regression.txt")
for(i in seq_along(df_list)){
  dat_design <- svydesign(ids=~MCSID,
                          strata=~PTTYPE2,
                          weights=~FOVWT2,
                          data=df_list[[i]],
                          nest=T)
  dat_design <- as_survey(dat_design)
  multi_model <- svy_vglm(PDCAT ~ SCORE_1 + SCORE_T +
    AOECDSC0 + APWTKG00 + ADDAGB00 + ADBMIPRE, design=dat_design, family=multinomial(refLevel="ontime"))
  samplesize <-
  print(titles[[i]])
  print(summary(multi_model$fit))
  print("")
}
sink()
