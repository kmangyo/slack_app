# https://api.slack.com/custom-integrations/legacy-tokens
# devtools::install_github("bnosac/cronR")
# install.packages('miniUI')
# install.packages('shiny')
# install.packages('shinyFiles')
# install.packages('slackr')
# install.packages('googleLanguageR')
# install.packages('stringr')
# install.packages("reshape2")

library(googleLanguageR)
library(stringr)
library(cronR)
library(slackr)
library(dplyr)
library(reshape2)
library(ggplot2)

# read the file
twit<-read.csv("tweets_kmangyo.csv")
twit$date<-as.Date(twit$timestamp)

# today
today <- as.Date(Sys.time(),tz='Asia/Seoul')

day <- list()
for(i in 1:8){
  day[i] <-as.Date(today - (365*i))
}

# select today twit
memory <- list()
for (i in 1:length(day)){
  memory[[i]]<- subset(twit, date==as.Date(day[[i]], origin='1970-01-01'))
}

slackr_setup(config_file='slack.slackr')

# send the twit and date
for(i in 1:length(memory)){
  slackr(as.character(memory[[i]]$date[1]),channel = '#memory')
  Sys.sleep(5)
  slackr(as.character(memory[[i]]$text,channel = '#memory'))
  Sys.sleep(5)
}

myword <- list()

# except RTs
for(i in 1:length(memory)){
  myword[[i]] <- subset(memory[[i]], str_detect(text, '^RT @')==FALSE)
}

gl_auth("XXXX.json")

# using google API
snt_result <- list()
for(i in 1:length(memory)){
  snt_result[[i]] <- gl_nlp(as.character(myword[[i]]$text), language = "ko")
}

# getting sentiment score
vplot <- list()
for(i in 1:length(memory)){
 vplot[[i]] <- snt_result[[i]]$documentSentiment$score
}

y_date <- list()
for(i in 1:length(memory)){
  y_date[[i]] <- myword[[i]]$date
}

# Null issues (only rt day) 
for(i in 1:length(memory)) {
  if (is.null(vplot[[i]]) == TRUE) {
    vplot[[i]] <- NA 
  } else {
    vplot[[i]] <- vplot[[i]]
  }
}

vplot_df <- melt(vplot)
vplot_df <- subset(vplot_df, value!=c('NA'))
y_date <- melt(y_date)
  
vplot_df <- cbind(vplot_df, y_date)
names(vplot_df)[3] <- 'date'

# sent cnt twit
ggslackr(ggplot(vplot_df, aes(x=date)) +geom_bar(stat="count"))

# send boxplot smt
ggslackr(ggplot(vplot_df, aes(x=as.factor(substr(vplot_df$date,1,4)), y=value)) + geom_boxplot())
