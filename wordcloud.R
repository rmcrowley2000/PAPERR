#!/usr/bin/env Rscript

library(tm)
library(wordcloud)
#setwd("D:/Dropbox/Conferences/NTU Finance 2018/Discussion")
text <- read.csv("Data/text.txt", stringsAsFactors = FALSE)
corp <- Corpus(VectorSource(text$text))
corp = tm_map(corp, content_transformer(tolower))
corp = tm_map(corp, removeNumbers)
corp = tm_map(corp, removePunctuation)
corp = tm_map(corp, removeWords, c("the", "and", stopwords("english"), stopwords("french")))
corp =  tm_map(corp, stripWhitespace)
tdm <- TermDocumentMatrix(corp)
tdm <- as.matrix(tdm)
v = sort(rowSums(tdm), decreasing = TRUE)
png("Figures/wordcloud.png", width = 3200, height = 2400, res=400)
wordcloud(names(v),v, scale= c(4, .5), colors = c(rep("#151C5522",10),rep("#8A704C22",length(v)-10)), ordered.colors=TRUE, random.color = FALSE, random.order = FALSE)
dev.off()
library("magick")
wc <- image_read("Figures/wordcloud.png")
wc <- image_crop(wc,"2200x2200+500+100")
image_write(wc, path = "Backgrounds/wordcloud.png", format = "png")
file.remove("Figures/wordcloud.png")