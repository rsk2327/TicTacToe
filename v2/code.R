setwd("/media/rsk/RSK1/Acads/LoanPrediction")

library(data.table)
library(dplyr)
library(mice)
library(mi)

train = fread("train_u6lujuX_CVtuZ9i.csv",stringsAsFactors = TRUE)
is.na(train)  = 
train[Gender=="",Gender := NA]

train2 = read.csv("train_u6lujuX_CVtuZ9i.csv",na.strings = c("",", ,"," ","NA"))
train$Loan_ID = as.character(train2$Loan_ID)


train[ , lapply(.SD,function(x){ sum(is.na(x))}) ,]

train[is.na(Gender),":="(Gender ="Male" )]
train[is.na(Married),":="(Married ="Yes" )]


a = mice(train)
a = mice(train2)
a$imp
d = complete(a,2)
summary(d)
