library(ggplot2)
library(packcircles)

setwd("/Users/michelle/Documents/covid19-xenophobia/data-viz")
data <- read.csv("../slur-data/slur_counts.csv")

data$date <- as.Date(data$date, format= "%Y-%m-%d")
data <- data[(data$date >= "2020-02-01"),]
data$total <- rowSums(data[,2:10])

ggplot(data, aes(date, total)) +
  geom_line(na.rm = TRUE) +
  xlab("Date (2020)") +
  ylab("Number of Tweets Containing Slurs") +
  scale_x_date(date_breaks = "1 month", minor_breaks = NULL, date_labels = "%b", limits = c(as.Date("2020-02-01"), NA)) +
  scale_y_continuous(breaks = round(seq(0, max(data$total),
                                        by = 100), 1)) + theme_bw() +
  theme(panel.grid.major.x = element_blank(),
        panel.grid.minor.x = element_blank())

slur <- colnames(data)[2:10]
count <- unname(colSums(data[2:10]))
top_data <- data.frame(slur, count)
top_data <- top_data[(top_data$count > 0),]

ggplot(top_data, aes(reorder(slur, count), count)) +
  geom_bar(stat="identity") +
  xlab("Slur") +
  ylab("Number of Tweets Containing Slur") + 
  scale_y_continuous(trans = "log10") + theme_bw() +
  coord_flip()

top_data2 <- top_data[order(-top_data$count),]
packing <- circleProgressiveLayout(top_data2$count)
top_data_c <- cbind(top_data2, packing)
dat.gg <- circleLayoutVertices(packing, npoints = 50)

ggplot() +
  geom_polygon(data = dat.gg, aes(x, y, group = id, fill = as.factor(id)), colour = "black", alpha = 0.6) +
  # geom_text(data = top_data_c, aes(x, y, size = count, label = slur)) +
  scale_size_continuous(range = c(1,4)) +
  labs(fill = "key") +
  scale_fill_hue(labels = top_data2$slur) +
  theme_void() +
  coord_equal()
