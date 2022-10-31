library(tidyverse)         #Needed for read_table function


# 2. Load lexicon file
lexicon1 <- read_table(file = "~/researchdrive/M21033303_DenA (Projectfolder)/DA_Onderzoek/2022sean/lexicons/DuOMAn-subjectivitylexicon_1.0 [NL]/subj_assessments.txt",
                       col_names = c('word', 'gender', 'an1', 'an2'), 
                       col_types = c(col_character(), col_character(), col_character(), col_character()))