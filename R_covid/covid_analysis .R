library(ggplot2)
library(dplyr)
library(reshape2)
library(tidyverse)

df <- read.csv('covid.csv', header=TRUE, sep=';')

df1<-df %>% 
  select(continent, deaths, cases) %>%
  group_by(continent)%>%
  summarise(deaths=sum(deaths),cases=sum(cases))
ggplot(df1, aes(x=deaths,y=cases,color=continent))+
  geom_point() + geom_abline(slope=40)
cor(df1['cases'],df1['deaths'])
#It is obvious the fact that there is correlation between the total number of cases and the total number of deaths

df2<- melt(df1, id.vars='continent')
ggplot(df2,aes(x=continent,y=value,fill=variable)) + 
  geom_bar(stat='identity',position='dodge')
#Plotting number of deaths/cases vs continents with two different bar graphs

df3<-df%>%
  select(country,deaths)%>%
  group_by(country)%>%
  summarise(deaths=sum(deaths))%>%
  arrange(desc(deaths))
df3<-df3[1:5,]
ggplot(df3,aes(x=country,y=deaths,fill=country))+
  geom_bar(stat='identity',position='dodge')
#Top 5 countries with the highest number of deaths

df4<-df%>%
  select(country,cases)%>%
  group_by(country)%>%
  summarise(cases=sum(cases))%>%
  arrange(desc(cases))
df4<-df4[1:5,]
ggplot(df4, aes(x=country,y=cases,fill=country))+
  geom_bar(stat="identity",position='dodge')
#Top 5 countries with the highest number of cases


df5 <-df%>%
  select(month,cases,year)%>%
  group_by(year,month)%>%
  summarise(total_cases=sum(cases))%>%
  arrange(year)%>%
  mutate(Date=paste(as.character(month),as.character(year), sep="/"))%>%
  arrange(Date)
df5
ggplot(df5, aes(x=total_cases,y=Date)) +
  geom_bar(stat='identity',position='dodge',fill='blue')
#We plot the total number of cases by month

df6 <-df%>%
  select(month,deaths,year)%>%
  group_by(year,month)%>%
  summarise(total_deaths=sum(deaths))%>%
  arrange(year)%>%
  mutate(Date=paste(as.character(month),as.character(year), sep="/"))%>%
  arrange(Date)
df6
ggplot(df6, aes(x=total_deaths,y=Date)) +
  geom_bar(stat='identity',position='dodge',fill='blue')
#We plot the total number of deaths by month

df7 <-df%>%
  select(day,month,year,cases,deaths)%>%
  group_by(day,year,month)%>%
  summarise(cases=sum(cases),deaths=sum(deaths))
df7
df7[which.max(df7$deaths),]
df7[which.max(df7$cases),]
#Days with the highest number of cases and deaths 
