#
# Generate summary stats with survey weights
#
suppressPackageStartupMessages({
  library(tidyverse)
  library(srvyr)
  library(survey)
})
dat <- read_csv("data/processed/MCS1.csv")

dat_design <- svydesign(ids=~MCSID,
                        strata=~PTTYPE2,
                        weights=~FOVWT2,
                        data=dat,
                        nest=T)
dat_design <- as_survey(dat_design)

cols_cat <- c("PDCAT", "AOECDSC0")

# PT Category males
for(g in cols_cat){
  filename <- paste0("results/reports/summary_", g, ".csv")
  summary_cat <- dat_design %>%
    group_by(across(all_of(g))) %>%
    summarise(pct = survey_prop(vartype="ci",
                                level=0.95,
                                proportion=TRUE)*100)
  write.csv(summary_cat, filename, row.names=FALSE)
}

summary_cont <- dat_design %>%
  group_by(PDCAT) %>%
  summarise(across(c(SCORE_T, SCORE_1, APWTKG00, ADDAGB00, ADBMIPRE),
                   list(mean=mean,
                        sd=sd,
                        min=min,
                        max=max)))
write.csv(summary_cont,
          "results/reports/summary_cont.csv",
          row.names=FALSE)
