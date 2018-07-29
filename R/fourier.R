library(readr)
library(stringr)
library(ggplot2)
library(waved)
library()
path = "PycharmProjects/TravelMode/data/fourier\ test/"
for(file in list.files(path)){
  Accelometr = read.csv(paste0(path,file))
  for(i in 2:length(Accelometr)){
    furier = abs(fftshift(fft(Accelometr[,i])))
    x = seq(-100,100,2*100/length(furier))[1:length(furier)]
    lable = paste0(str_sub(file,1,-5),colnames(Accelometr)[i])
    print(ggplot() + geom_line(aes(x = x,y = furier)) + ggtitle(lable))    
  }
}

Rotation = read.csv("PycharmProjects/TravelMode/data/fourier test/RotationVector.csv")
Rotation