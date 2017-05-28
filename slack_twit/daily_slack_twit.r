# devtools::install_github("bnosac/cronR")
library(cronR)
# install.packages('miniUI')
# install.packages('shiny')
# install.packages('shinyFiles')

library(slackr)
library(dplyr)

twit<-read.csv("twit_data.csv")
twit$date<-as.Date(twit$date)

slackrSetup(config_file='slack.slackr')
today <- as.Date(Sys.time(),tz='KST')

day <- list()
for(i in 1:7){
  day[i] <-as.Date(today - (365*i))
}

memory <- list()
for (i in 1:length(day)){
  memory[[i]]<- subset(twit, date==as.Date(day[[i]], origin='1970-01-01'))
}

for(i in 1:length(memory)){
  slackr(print(memory[[i]]$date[1]))
  Sys.sleep(5)
  slackr(as.character(memory[[i]]$text))
  Sys.sleep(5)
}
