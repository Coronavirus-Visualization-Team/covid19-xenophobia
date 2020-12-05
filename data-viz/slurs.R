library(ggplot2)

setwd("/Users/michelle/Documents/covid19-xenophobia/data-viz")
data <- read.csv("../slur-data/FreqCSV_Sinophobia.csv")

data$date <- as.Date(data$date)

ggplot(data, aes(date, totalCount)) +
  geom_line(na.rm = TRUE) +
  xlab("date") +
  xlim(as.Date("2020-01-27"), NA) +
  ylab("slur count") +
  scale_y_continuous(breaks = round(seq(min(data$totalCount), max(data$totalCount),
                                        by = 50000), 1)) + theme_bw() 

# scale_x_continuous(name = "date", 
#                    limits = c(as.Date("2020-01-27"), NA), 
#                    breaks = round(seq(min(data$date), max(data$date), 
#                                       by = as.difftime(30, units="days")), 1))
# theme(axis.text.x = element_text(angle = 45, vjust = 1, hjust = 1))

ggplot(data, aes(date, neg_count / total)) +
  geom_line(na.rm = TRUE) +
  xlab("date") +
  xlim(as.Date("2020-01-27"), NA) +
  ylab("negative tweet proportion") +
  scale_y_continuous(breaks = round(seq(min(data$neg_count / data$total), max(data$neg_count / data$total),
                                        by = 0.1), 1)) + theme_bw() +
  geom_vline(xintercept = as.Date(c(
    "2020-01-30",
    "2020-02-07",
    "2020-03-09",
    "2020-03-18",
    "2020-03-26",
    "2020-04-16",
    "2020-06-21",
    "2020-07-10",
    "2020-07-21",
    "2020-09-16",
    "2020-10-02"
  )),
  linetype = 4, colour = "black")


