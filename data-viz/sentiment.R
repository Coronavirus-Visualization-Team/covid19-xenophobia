library(ggplot2)
library(grid)
library(reshape2)

setwd("/Users/michelle/Documents/covid19-xenophobia/data-viz")
data <- read.csv("../sentiment-data/agg_filled.csv")

data$date <- as.Date(data$date)

spikes <- as.Date(c(
  "2020-03-09",
  "2020-03-18",
  "2020-03-26",
  "2020-05-01",
  "2020-06-21",
  "2020-07-10",
  "2020-07-21",
  "2020-09-11",
  "2020-09-16",
  "2020-10-02"))

add_labels = function(plot, h) {
  plot + geom_label(aes(x = as.Date(spikes[1]), y = h, label = "A"), label.size = 0) +
  geom_label(aes(x = as.Date(spikes[2]), y = h, label = "B"), label.size = 0) +
  geom_label(aes(x = as.Date(spikes[3]), y = h, label = "C"), label.size = 0) +
  geom_label(aes(x = as.Date(spikes[4]), y = h, label = "D"), label.size = 0) +
  geom_label(aes(x = as.Date(spikes[5]), y = h, label = "E"), label.size = 0) +
  geom_label(aes(x = as.Date(spikes[6]), y = h, label = "F"), label.size = 0) +
  geom_label(aes(x = as.Date(spikes[7]), y = h, label = "G"), label.size = 0) +
  geom_label(aes(x = as.Date(spikes[8]), y = h, label = "H"), label.size = 0, label.padding = unit(0.1, "lines")) +
  geom_label(aes(x = as.Date(spikes[9]), y = h, label = "I"), label.size = 0, label.padding = unit(0.1, "lines")) +
  geom_label(aes(x = as.Date(spikes[10]), y = h, label = "J"), label.size = 0)
}

plot1 <- ggplot(data, aes(date, neg_count)) +
  geom_line(na.rm = TRUE) +
  xlab("Date (2020)") +
  ylab("Number of Negative Tweets") +
  scale_x_date(breaks = seq.Date(as.Date("2020-02-01"), as.Date("2020-10-31"), by = "month"), minor_breaks = NULL, date_labels = "%b", limits = c(as.Date("2020-02-01"), NA)) +
  scale_y_continuous(breaks = round(seq(min(data$neg_count), max(data$neg_count),
                                        by = 2500), 1)) + theme_bw() +
  theme(panel.grid.major.x = element_blank(),
        panel.grid.minor.x = element_blank()) +
  geom_vline(xintercept = spikes, linetype = 3, colour = "black") + 
  coord_cartesian(ylim = c(0, 14000), clip = "off") + 
  theme(plot.margin = unit(c(3,1,1,1), "lines"))

print(add_labels(plot1, 15200))

data2 <- data
data2$neutral_count <- data2$total - data2$neg_count
dataMelted <- reshape2::melt(data2[ , c("date", "neg_count", "neutral_count")], id.var="date")

plot2 <- ggplot(dataMelted, aes(x = date, y = value, col = variable)) + 
  # geom_line(na.rm = TRUE, data = data, aes(date, neg_count), color = "red", key_glyph = draw_key_rect) +
  # geom_line(na.rm = TRUE, data = data, aes(date, total - neg_count), color = "blue", key_glyph = draw_key_rect) +
  geom_line(na.rm = TRUE) +
  xlab("Date (2020)") +
  ylab("Number of Tweets") +
  scale_x_date(breaks = seq.Date(as.Date("2020-02-01"), as.Date("2020-10-31"), by = "month"), minor_breaks = NULL, date_labels = "%b", limits = c(as.Date("2020-02-01"), NA)) +
  scale_y_continuous(breaks = round(seq(0, max(data$total),
                                        by = 10000), 1)) + theme_bw() +
  theme(panel.grid.major.x = element_blank(),
        panel.grid.minor.x = element_blank()) +
  coord_cartesian(ylim = c(0, 50000), clip = "off") + 
  labs(colour = "key") + 
  scale_color_manual(labels = c("negative", "postive/neutral"), values = c("#F8766D", "#06BEC4"))

print(plot2)

plot3 <- ggplot(data, aes(date, neg_count / total)) +
  geom_line(na.rm = TRUE) +
  xlab("Date (2020)") +
  ylab("Proportion of Negative Tweets") +
  scale_x_date(breaks = seq.Date(as.Date("2020-02-01"), as.Date("2020-10-31"), by = "month"), minor_breaks = NULL, date_labels = "%b", limits = c(as.Date("2020-02-01"), NA)) +
  scale_y_continuous(breaks = round(seq(min(data$neg_count / data$total), max(data$neg_count / data$total),
                                        by = 0.1), 1)) + theme_bw() +
  theme(panel.grid.major.x = element_blank(),
        panel.grid.minor.x = element_blank()) +
  coord_cartesian(ylim = c(0, 0.525), clip = "off") + 
  theme(plot.margin = unit(c(3,1,1,1), "lines")) +
  geom_vline(xintercept = spikes,linetype = 3, colour = "black")

print(add_labels(plot3, 0.575))

data3 <- data2
data3$neg_prop <- data3$neg_count / data3$total
data3$neutral_prop <- data3$neutral_count / data3$total
dataMelted2 <- reshape2::melt(data3[ , c("date", "neg_prop", "neutral_prop")], id.var="date")

plot4 <- ggplot(dataMelted2, aes(x = date, y = value, col = variable)) +
  geom_line(na.rm = TRUE) +
  xlab("Date (2020)") +
  ylab("Proportion of Tweets") +
  scale_x_date(breaks = seq.Date(as.Date("2020-02-01"), as.Date("2020-10-31"), by = "month"), minor_breaks = NULL, date_labels = "%b", limits = c(as.Date("2020-02-01"), NA)) +
  scale_y_continuous(breaks = round(seq(0, 0.95,
                                        by = 0.1), 1)) + theme_bw() +
  theme(panel.grid.major.x = element_blank(),
        panel.grid.minor.x = element_blank()) +
  coord_cartesian(ylim = c(0, 0.95), clip = "off") + 
  theme(plot.margin = unit(c(3,1,1,1), "lines"))

print(plot4)
