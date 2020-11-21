library(ggplot2)

setwd("/Users/michelle/Documents/covid19-xenophobia/data-viz")
data <- read.csv("agg_filled.csv")

data$date <- as.Date(data$date)

plot(data$date, data$neg_count, type="l")
