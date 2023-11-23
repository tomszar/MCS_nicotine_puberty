# Variables Dictionary

## Smoking

| Variable  | Label                                           | Type    |
|-----------|-------------------------------------------------|---------|
| APSMMA00  | How many cigarettes per day                     | Scale   |   
| APPIOF00  | Frequency of pipe smoking                       | Nominal |
| APSMTY00  | Smoked in last 2 years                          | Nominal |
| APSMEV00  | Ever regularly smoked tobacco products          | Nominal |
| APCIPR00  | Number of cigarettes smoked per day before preg | Scale   |
| APSMCH00  | Changed number smoked during pregnancy          | Nominal |
| APWHCH00  | When changed smoking habits                     | Nominal |
| APCICH00  | Number smoked per day after change              | Scale   |
| APSMKR00  | Whether anyone smokes in the same room as CM    | Nominal |

* APSMMA00 (How many cigarettes per day )
    * -8.0 (Don't Know)
    * -1.0 (Not applicable)
    * -9.0 (Refusal)

* APPIOF00 (Frequency of pipe smoking)
    * 1.0 = Every day
    * 2.0 = 5-6 times per week 
    * 3.0 = 3-4 times per week 
    * 4.0 = 1-2 times per week 
    * 5.0 = 1-2 times per month 
    * 6.0 = Less than once a month 
    * -9.0 = Refusal 
    * -8.0 = Don't Know 
    * -1.0 = Not applicable

* APSMTY00 (Smoked in last 2 years)
    * 1.0 = Yes 
    * 2.0 = No 
    * -9.0 = Refusal 
    * -8.0 = Don't Know 
    * -1.0 = Not applicable 

* APSMEV00 (Ever regularly smoked tobacco products)
    * 1.0 = Yes
    * 2.0 = No
    * -9.0 = Refusal
    * -8.0 = Don't Know
    * -1.0 = Not applicable

* APCIPR00 (Number of cigarettes smoked per day before preg)
    * -8.0 = Don't Know
    * -1.0 = Not applicable
    * -9.0 = Refusal

* APSMCH00 (Changed number smoked during pregnancy)
    * Value = 1.0 Label = Yes
    * Value = 2.0 Label = No
    * Value = 3.0 Label = Can't remember
    * Value = -9.0 Label = Refusal
    * Value = -8.0 Label = Don't Know
    * Value = -1.0 Label = Not applicable

* APWHCH00 (When changed smoking habits)
    * Value = 1.0 Label = First
    * Value = 2.0 Label = Second
    * Value = 3.0 Label = Third
    * Value = 4.0 Label = Fourth
    * Value = 5.0 Label = Fifth
    * Value = 6.0 Label = Sixth
    * Value = 7.0 Label = Seventh
    * Value = 8.0 Label = Eighth
    * Value = 9.0 Label = Ninth
    * Value = 10.0 Label = Can't remember
    * Value = -9.0 Label = Refusal
    * Value = -8.0 Label = Don't Know
    * Value = -1.0 Label = Not applicable

* APCICH00 (Number smoked per day after change)
    * Value = 0.0 Label = Gave Up
    * Value = 96.0 Label = Less than one a day
    * Value = 97.0 Label = Can't remember
    * Value = -8.0 Label = Don't Know
    * Value = -9.0 Label = Refusal
    * Value = -1.0 Label = Not applicable

* APSMKR00 (Whether anyone smokes in the same room as CM)
    * Value = 1.0 Label = Yes
    * Value = 2.0 Label = No
    * Value = -9.0 Label = Refusal
    * Value = -8.0 Label = Don't Know
    * Value = -1.0 Label = Not applicable

## Pubertal Timing

| Variable | Label   | Type    |
|----------|---------|---------|
| FCCSEX00 | CM Sex  | Nominal |

* FCCSEX00 (CM Sex)
    * Value = 1.0	Label = Male
    * Value = 2.0	Label = Female

For boy and girls the common variables to determine PT scores are:

| Variable | Label                    | Type    |
|----------|--------------------------|---------|
| FCPUHG00 | CM growth spurt          | Nominal |
| FCPUBH00 | CM no body hair          | Nominal |
| FCPUSK00 | CM skin changes eg spots | Nominal |

* FCPUHG00 (CM growth spurt)
    * Value = 1.0	Label = My growth spurt has not yet begun
    * Value = 2.0	Label = My growth spurt has barely started
    * Value = 3.0	Label = My growth spurt has definitely started
    * Value = 4.0	Label = My growth spurt seems completed
    * Value = -9.0	Label = Don't want to answer
    * Value = -8.0	Label = Don't know
    * Value = -1.0	Label = Not applicable

* FCPUBH00 (CM no body hair)
    * Value = 1.0	Label = My body hair has not yet begun to grow
    * Value = 2.0	Label = My body hair has barely started to grow
    * Value = 3.0	Label = My body hair has definitely started to grow
    * Value = 4.0	Label = My body hair growth seems completed 
    * Value = -9.0	Label = Don't want to answer 
    * Value = -8.0	Label = Don't know
    * Value = -1.0	Label = Not applicable

* FCPUSK00 (CM skin changes eg spots)
    * Value = 1.0	Label = My skin has not yet started changing 
    * Value = 2.0	Label = My skin has barely started changing 
    * Value = 3.0	Label = My skin has definitely started changing
    * Value = 4.0	Label = My skin changes seem completed
    * Value = -9.0	Label = Don't want to answer 
    * Value = -8.0	Label = Don't know 
    * Value = -1.0	Label = Not applicable 

For girls the exclusive variables are:

| Variable  | Label                    | Type    |
|-----------|--------------------------|---------|
| FCPUBR00  | CM breast growth         | Nominal |
| FCPUMN00  | CM started to menstruate | Nominal |

* FCPUBR00 (CM breast growth)
    * Value = 1.0	Label = My breasts have not yet started to grow
    * Value = 2.0	Label = My breasts have barely started to grow
    * Value = 3.0	Label = My breasts have definitely started to grow
    * Value = 4.0	Label = My breast growth seems completed 
    * Value = -9.0	Label = Don't want to answer 
    * Value = -8.0	Label = Don't know 
    * Value = -1.0	Label = Not applicable

* FCPUMN00 (CM started to menstruate)
    * Value = 1.0	Label = Yes 
    * Value = 2.0	Label = No 
    * Value = -9.0	Label = Don't want to answer 
    * Value = -8.0	Label = Don't know 
    * Value = -1.0	Label = Not applicable 
    * __Note__: This variable is recoded as 3 (Yes) and 0 (No) 

For boys the exclusive variables are:

| Variable | Label           | Type    |
|----------|-----------------|---------|
| FCPUVC00 | CM voice change | Nominal |
| FCPUFH00 | CM facial hair  | Nominal |

* FCPUVC00 (CM voice change)
    * Value = 1.0	Label = My voice has not yet started getting deeper
	* Value = 2.0	Label = My voice has barely started getting deeper
	* Value = 3.0	Label = My voice has definitely started getting deeper
	* Value = 4.0	Label = My voice change seems completed
	* Value = -9.0	Label = Don't want to answer 
	* Value = -8.0	Label = Don't know 
	* Value = -1.0	Label = Not applicable
  
* FCPUFH00 (CM facial hair)
    * Value = 1.0	Label = My facial hair has not yet started to grow
	* Value = 2.0	Label = My facial hair has barely started to grow
	* Value = 3.0	Label = My facial hair has definitely started to grow
	* Value = 4.0	Label = My facial hair growth seems completed 
	* Value = -9.0	Label = Don't want to answer 
	* Value = -8.0	Label = Don't know 
	* Value = -1.0	Label = Not applicable 

## Covariates

| Variable | Label                                                       | Type    |
|----------|-------------------------------------------------------------|---------|
| AOECDSC0 | DV OECD Income Weighted Quintiles (Single Country Analysis) | Nominal |
| APWTKG00 | Birth weight kilos and grams                                | Scale   |
| ADDAGB00 | Respondent age at birth of CM                               | Scale   |
| ADBMIPRE | BMI of respondent before CM born                            | Scale   |

* AOECDSC0 (DV OECD Income Weighted Quintiles (Single Country Analysis))
    * Value = 1.0 Label = Lowest quintile
    * Value = 2.0 Label = Second quintile
    * Value = 3.0 Label = Third quintile
    * Value = 4.0 Label = Fourth quintile
    * Value = 5.0 Label = Highest quintile
    * Value = -1.0 Label = Not applicable

## Weights

| Variable | Label                                        | Type  |
|----------|----------------------------------------------|-------|
| PTTYPE2  | Stratum within Country                       | Scale |
| FOVWT2   | S6: Overall Weight (inc NR adjustment) whole | Scale |

*  PTTYPE2 (Stratum within Country)
    * Value = 1.0 Label = England - Advantaged
    * Value = 2.0 Label = England - Disadvantaged
    * Value = 3.0 Label = England - Ethnic
    * Value = 4.0 Label = Wales - Advantaged
    * Value = 5.0 Label = Wales - Disadvantaged
    * Value = 6.0 Label = Scotland - Advantaged
    * Value = 7.0 Label = Scotland - Disadvantaged
    * Value = 8.0 Label = Northern Ireland - Advantaged
    * Value = 9.0 Label = Northern Ireland - Disadvantaged
    * Value = -1.0 Label = Not applicable
    * 