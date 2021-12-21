library(lme4)
library(AICcmodavg)
library(tidyverse)
library(cowplot)
library(here)
library(car)
library(lmerTest)
library(ggbeeswarm)
theme_set(theme_cowplot())

all_data <- read.csv(here::here("processed_data","Words_final_preprocessed.csv"))

#### plot overall development of score ####

average_score_by_trial_across_subj <- all_data %>%
  filter(trialType=="test") %>%
  group_by(version,block,trialNumber) %>%
  summarize(
    N=n(),
    mean_score=mean(score),
    sd_score=sd(score),
    ci_score=qt(0.975, N-1)*sd_score/sqrt(N),
    lower_ci=mean_score-ci_score,
    upper_ci=mean_score+ci_score,
    angleDiffFromMatch=mean(angleDiffFromMatch)
  )

ggplot(average_score_by_trial_across_subj,aes(trialNumber,mean_score,color=block))+
  geom_errorbar(aes(ymin=lower_ci,ymax=upper_ci),width=0)+
  geom_line()+
  geom_point()+
  facet_wrap(~version)

average_score_by_blocks_across_subj <- all_data %>%
  filter(trialType=="test") %>%
  mutate(block_8=floor(trialNumber/8)+1) %>%
  group_by(version,subjCode,block,block_8) %>%
  summarize(
    num_trials=n(),
    score=mean(score)
  ) %>%
  ungroup() %>%
  group_by(version,block,block_8) %>%
  summarize(
    N=n(),
    mean_score=mean(score),
    sd_score=sd(score),
    ci_score=qt(0.975, N-1)*sd_score/sqrt(N),
    lower_ci=mean_score-ci_score,
    upper_ci=mean_score+ci_score
  )

ggplot(average_score_by_blocks_across_subj,aes(block_8,mean_score,color=block))+
  geom_errorbar(aes(ymin=lower_ci,ymax=upper_ci),width=0)+
  geom_line()+
  geom_point()+
  facet_wrap(~version)

#exp1
m <- lmer(score~1+trialNumber+angleDiffFromMatchC+
            (1+trialNumber+angleDiffFromMatchC|subjCode)+
            (1|targetLabel),
          data=filter(all_data, trialType=="test"&version=="exp1"))
summary(m)
#exp2
m <- lmer(score~1+trialNumber+angleDiffFromMatchC+
            (1+trialNumber+angleDiffFromMatchC|subjCode)+
            (1|targetLabel),
          data=filter(all_data, trialType=="test"&version=="exp2"))
summary(m)
#exp3
m <- lmer(score~1+trialNumber+angleDiffFromMatchC+
            (1+trialNumber+angleDiffFromMatchC|subjCode)+
            (1|targetLabel),
          data=filter(all_data, trialType=="test"&version=="exp3"))
summary(m)
#exp4
m <- lmer(score~1+trialNumber+angleDiffFromMatchC+
            (1+trialNumber+angleDiffFromMatchC|subjCode)+
            (1|targetLabel),
          data=filter(all_data, trialType=="test"&version=="exp4"))
summary(m)

####main conclusion:
#Score does not increase across time (controlling for angle difference)
#Score also does not appear to increase within specific block types

#### plot score by trial type ####

#specifically hf trials
average_score_by_freq_by_trial_across_subj <- all_data %>%
  filter(trialType=="test"&!is.na(hfTrial)) %>%
  group_by(version,trialNumber,hfTrial) %>%
  summarize(
    N=n(),
    mean_score=mean(score),
    sd_score=sd(score),
    ci_score=qt(0.975, N-1)*sd_score/sqrt(N),
    lower_ci=mean_score-ci_score,
    upper_ci=mean_score+ci_score,
    angleDiffFromMatch=mean(angleDiffFromMatch)
  )

ggplot(average_score_by_freq_by_trial_across_subj,aes(trialNumber,mean_score,color=as.factor(hfTrial)))+
  #geom_errorbar(aes(ymin=lower_ci,ymax=upper_ci),width=0)+
  geom_line()+
  geom_point()+
  facet_wrap(~version)

#exp 1
m <- lmer(score~1+hfTrial+angleDiffFromMatchC+
            (1+hfTrial+angleDiffFromMatchC|subjCode)+
            (1|targetLabel),
          data=filter(all_data, version=="exp1"&listChoice==1))
summary(m)
#Anova(m, type="III",test="F")

#exp 2
m <- lmer(score~1+hfTrial+angleDiffFromMatchC+
            (1+hfTrial+angleDiffFromMatchC|subjCode)+
            (1|targetLabel),
          data=filter(all_data, version=="exp2"&listChoice==1))
summary(m)
#Anova(m, type="III",test="F")

#exp 3
m <- lmer(score~1+hfTrial+angleDiffFromMatchC+
            (1+hfTrial+angleDiffFromMatchC|subjCode)+
            (1|targetLabel),
          data=filter(all_data, version=="exp3"&listChoice==1))
summary(m)
#Anova(m, type="III",test="F")

#exp 4
m <- lmer(score~1+hfTrial+angleDiffFromMatchC+
            (1+hfTrial+angleDiffFromMatchC|subjCode)+
            (1|targetLabel),
          data=filter(all_data, version=="exp4"&listChoice==1))
summary(m)
#Anova(m, type="III",test="F")

####main conclusion:
#People do (much) better on high-frequency trials in terms of score (controlling for angle difference)

##### Optimal score

all_data <- all_data %>%
  ungroup() %>%
  mutate(optimal_score=(45-angleDiffFromMatch)*2,
         base_score = case_when(
           is.na(angleDiff) ~ NA_real_,
           is.na(label_raw) ~ NA_real_,
           is.na(leftLabel) ~ NA_real_,
           label_raw == leftLabel ~ as.numeric(45-angleDiff),
           is.na(rightLabel) ~ 0,
           label_raw == rightLabel ~ as.numeric(angleDiff),
           TRUE ~ 0
         ),
         optimal_score_2000=(45-angleDiffFromMatch)*(1+(5000-2000)/5000),
         optimal_score_own_rt=(45-angleDiffFromMatch)*(1+(5000-rt)/5000)) %>%
  mutate(
    diff_optimal=optimal_score-score,
    diff_optimal_score_2000=optimal_score_2000-score,
    diff_optimal_own_rt= optimal_score_own_rt-score
    
  ) 
ggplot(filter(all_data,!is.na(hfTrial)),aes(as.factor(hfTrial),diff_optimal_own_rt,color=as.factor(hfTrial)))+
  geom_quasirandom(alpha=0.05,bandwidth=2)+
  geom_violin(width=1)+
  facet_wrap(~version)

#difference in score between hf trials
average_diff_optimal_score_by_freq_by_trial_across_subj <- all_data %>%
  filter(trialType=="test"&!is.na(hfTrial)) %>%
  group_by(version,trialNumber,hfTrial) %>%
  summarize(
    N=n(),
    mean_diff_optimal_score=mean(diff_optimal),
    sd_diff_score=sd(diff_optimal),
    ci_diff_score=qt(0.975, N-1)*sd_diff_score/sqrt(N),
    lower_diff_ci=mean_diff_optimal_score-ci_diff_score,
    upper_diff_ci=mean_diff_optimal_score+ci_diff_score,
    angleDiffFromMatch=mean(angleDiffFromMatch)
  )

ggplot(average_diff_optimal_score_by_freq_by_trial_across_subj,aes(trialNumber,mean_diff_optimal_score,color=as.factor(hfTrial)))+
  #geom_errorbar(aes(ymin=lower_ci,ymax=upper_ci),width=0)+
  geom_line()+
  geom_point()+
  facet_wrap(~version)

#exp 1
m <- lmer(diff_optimal_own_rt~1+hfTrial+angleDiffFromMatchC+
            (1+hfTrial+angleDiffFromMatchC|subjCode)+
            (1|targetLabel),
          data=filter(all_data, version=="exp1"&listChoice==1))
summary(m)
#exp 2
m <- lmer(diff_optimal_own_rt~1+hfTrial+angleDiffFromMatchC+
            (1+hfTrial+angleDiffFromMatchC|subjCode)+
            (1|targetLabel),
          data=filter(all_data, version=="exp2"&listChoice==1))
summary(m)
#exp 3
m <- lmer(diff_optimal_own_rt~1+hfTrial+angleDiffFromMatchC+
            (1+hfTrial+angleDiffFromMatchC|subjCode)+
            (1|targetLabel),
          data=filter(all_data, version=="exp3"&listChoice==1))
summary(m)
#exp 4
m <- lmer(diff_optimal_own_rt~1+hfTrial+angleDiffFromMatchC+
            (1+hfTrial+angleDiffFromMatchC|subjCode)+
            (1|targetLabel),
          data=filter(all_data, version=="exp4"&listChoice==1))
summary(m)

#### how much do people deviate from the optimal choice? ####
# scaling the score by people's own median RT for a given item!!

all_data <- all_data %>%
  ungroup() %>%
  mutate(
    list_label= case_when(
      is.na(label) ~ NaN,
      label == as.character(word1) ~ 1,
      label == as.character(word2) ~ 1,
      label == as.character(word3) ~ 1,
      label == as.character(word4) ~ 1,
      label == as.character(word5) ~ 1,
      label == as.character(word6) ~ 1,
      label == as.character(word7) ~ 1,
      label == as.character(word8) ~ 1,
      TRUE ~0
    )
  )

subj_label_dictionary <- all_data %>%
  ungroup() %>%
  select(version, subjCode,word1,word2,word3,word4,word5,word6,word7,word8) %>%
  pivot_longer(word1:word8,names_to="label_dict_num",values_to="label") %>%
  unique()

subj_median_rt_test <- all_data %>%
  ungroup() %>%
  filter(trialType=="test"&list_label==1) %>%
  group_by(version,subjCode,label) %>%
  summarize(
    label_produced_n=n(),
    median_label_rt=median(rt,na.rm=TRUE),
    median_label_rt_hfTrials=median(rt[!is.na(hfTrial)],na.rm=TRUE)
  ) %>%
  full_join(select(subj_label_dictionary, version, subjCode,label)) %>%
  mutate(label_produced_n=ifelse(is.na(label_produced_n),0,label_produced_n)) 

#add median rts nearby words in full data set test trials
all_data <- all_data %>%
  left_join(subj_median_rt_test,by = c("nearbyLabel1"="label","version"="version","subjCode"="subjCode")) %>%
  rename(
    label_produced_n_label1=label_produced_n,
    median_label_rt_label1=median_label_rt,
    median_label_rt_hfTrials_label1=median_label_rt_hfTrials
  ) %>%
  left_join(subj_median_rt_test,by = c("nearbyLabel2"="label","version"="version","subjCode"="subjCode")) %>%
  rename(
    label_produced_n_label2=label_produced_n,
    median_label_rt_label2=median_label_rt,
    median_label_rt_hfTrials_label2=median_label_rt_hfTrials
  ) 

#compute optimal score based on median RTs for each item
all_data <- all_data %>%
  mutate(
    diff_label1=abs((angle-nearbyAngle1+180) %% 360 -180),
    diff_label2=abs((angle-nearbyAngle2+180) %% 360 -180),
    diff_labels_sum=diff_label1+diff_label2,
    check_diff=ifelse(angleDiffFromMatch == diff_label1 | angleDiffFromMatch==diff_label2,1,0)
  ) %>%
  mutate(
    median_rt_score_1=round((45-diff_label1)*(1+(5000-median_label_rt_label1)/5000),0),
    median_rt_score_2=round((45-diff_label2)*(1+(5000-median_label_rt_label2)/5000),0),
    median_rt_hfTrials_score_1=round((45-diff_label1)*(1+(5000-median_label_rt_hfTrials_label1)/5000),0),
    median_rt_hfTrials_score_2=round((45-diff_label2)*(1+(5000-median_label_rt_hfTrials_label2)/5000),0)
  ) %>%
  mutate(
    optimal_median_rt_label=case_when(
      median_rt_score_1>=median_rt_score_2 ~ nearbyLabel1,
      median_rt_score_1<median_rt_score_2 ~ nearbyLabel2
    ),
    optimal_median_rt_hfTrials_label=case_when(
      median_rt_hfTrials_score_1>=median_rt_hfTrials_score_2 ~ nearbyLabel1,
      median_rt_hfTrials_score_1<median_rt_hfTrials_score_2 ~ nearbyLabel2
    )
  ) %>%
  mutate(
    optimal_median_rt_choice=ifelse(label==optimal_median_rt_label,1,0),
    optimal_median_rt_hfTrials_choice=ifelse(label==optimal_median_rt_hfTrials_label,1,0)
  ) %>%
  mutate(
    optimal_median_rt_score=pmax(median_rt_score_1,median_rt_score_2),
    optimal_median_rt_hfTrials_score=pmax(median_rt_hfTrials_score_1,median_rt_hfTrials_score_2),
    diff_optimal_median_rt_score=optimal_median_rt_score-score,
    diff_optimal_median_rt_hfTrials_score=optimal_median_rt_hfTrials_score-score,
  )

summarize_subj_optimal_rt_choice <- 
  all_data %>% 
  filter(!is.na(hfTrial)& listChoice==1) %>%
  group_by(version,subjCode,hfTrial) %>%
  summarize(
    N=n(),
    mean_optimal_median_rt_choice=mean(optimal_median_rt_choice,na.rm=T),
    mean_optimal_median_rt_hfTrials_choice=mean(optimal_median_rt_hfTrials_choice,na.rm=T),
    mean_optimal_median_rt_score=mean(optimal_median_rt_score,na.rm=T),
    mean_optimal_median_rt_hfTrials_score=mean(optimal_median_rt_hfTrials_score,na.rm=T),
    mean_score=mean(score),
    mean_diff_optimal_median_rt_score=mean(diff_optimal_median_rt_score,na.rm=T),
    mean_diff_optimal_median_rt_hfTrials_score=mean(diff_optimal_median_rt_hfTrials_score,na.rm=T)
  )

#choice
ggplot(summarize_subj_optimal_rt_choice,aes(as.factor(hfTrial),mean_optimal_median_rt_choice,color=as.factor(hfTrial)))+
  geom_violin()+
  geom_point()+
  facet_wrap(~version)

#score
ggplot(summarize_subj_optimal_rt_choice,aes(as.factor(hfTrial),mean_diff_optimal_median_rt_score,color=as.factor(hfTrial)))+
  geom_violin()+
  geom_point()+
  facet_wrap(~version)

#model
#exp1
#choice
m <- glmer(optimal_median_rt_choice~hfTrial+angleDiffFromMatchC+(1+hfTrial+angleDiffFromMatchC|subjCode)+(1|targetLabel),data=subset(all_data, version=="exp1"& listChoice==1),family=binomial,glmerControl(optimizer="bobyqa"))
summary(m)
#score
m <- lmer(optimal_median_rt_score~hfTrial+angleDiffFromMatchC+(1+hfTrial+angleDiffFromMatchC|subjCode)+(1|targetLabel),data=subset(all_data, version=="exp1"& listChoice==1))
summary(m)
#exp2
#choice
m <- glmer(optimal_median_rt_choice~hfTrial+angleDiffFromMatchC+(1+hfTrial+angleDiffFromMatchC|subjCode)+(1|targetLabel),data=subset(all_data, version=="exp2"& listChoice==1),family=binomial,glmerControl(optimizer="bobyqa"))
summary(m)
#score
m <- lmer(optimal_median_rt_score~hfTrial+angleDiffFromMatchC+(1+hfTrial+angleDiffFromMatchC|subjCode)+(1|targetLabel),data=subset(all_data, version=="exp2"& listChoice==1))
summary(m)
#exp3
#choice
m <- glmer(optimal_median_rt_choice~hfTrial+angleDiffFromMatchC+(1+hfTrial+angleDiffFromMatchC|subjCode)+(1|targetLabel),data=subset(all_data, version=="exp3"& listChoice==1),family=binomial,glmerControl(optimizer="bobyqa"))
summary(m)
#score
m <- lmer(optimal_median_rt_score~hfTrial+angleDiffFromMatchC+(1+hfTrial+angleDiffFromMatchC|subjCode)+(1|targetLabel),data=subset(all_data, version=="exp3"& listChoice==1))
summary(m)
#exp4
#choice
m <- glmer(optimal_median_rt_choice~hfTrial+angleDiffFromMatchC+(1+hfTrial+angleDiffFromMatchC|subjCode)+(1|targetLabel),data=subset(all_data, version=="exp4"& listChoice==1),family=binomial,glmerControl(optimizer="bobyqa"))
summary(m)
#score
m <- lmer(optimal_median_rt_score~hfTrial+angleDiffFromMatchC+(1+hfTrial+angleDiffFromMatchC|subjCode)+(1|targetLabel),data=subset(all_data, version=="exp4"& listChoice==1))
summary(m)

#basic conclusion:
#people do worse in low-frequency trials compared to high-frequency trials
#not just due to some artifact of the scoring system - they are sacrificing more points than they could have achieved,
#even taking differences in rt into account. For instance, they make suboptimal choices even when median rt for each specific option for that participant
#is taken into account to project score.

              

