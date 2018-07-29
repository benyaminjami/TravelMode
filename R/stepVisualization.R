library(highcharter)
library(readr)
library(dplyr)
library(pracma)
library(tidyr)
data = read_csv('PycharmProjects/TravelMode/data/NormalizationTest/Normalized.csv')

data %>% select(Milliseconds,AccelerometerLinearX,AccelerometerLinearY,AccelerometerLinearZ) %>% 
  gather()  
data = data %>% filter(Milliseconds < 17000)
highchart() %>% 
  hc_add_series(data,name = "X","line",hcaes(Milliseconds,AccelerometerLinearX)) %>% 
  hc_add_series(data,name = "Y","line",hcaes(Milliseconds,AccelerometerLinearY)) %>%
  hc_add_series(data,name = "Z","line",hcaes(Milliseconds,AccelerometerLinearZ)) 

X<-movavg(data$AccelerometerLinearX,5,"s")
data$AccelerometerLinearXMAf = X
Y<-movavg(data$AccelerometerLinearY,5,"s")
data$AccelerometerLinearYMAf = Y
Z<-movavg(data$AccelerometerLinearZ,5,"s")
data$AccelerometerLinearZMAf = Z
highchart() %>% 
  hc_add_series(data,name = "X","line",hcaes(Milliseconds,AccelerometerLinearX)) %>% 
  hc_add_series(data,name = "Y","line",hcaes(Milliseconds,AccelerometerLinearY)) %>%
  hc_add_series(data,name = "Z","line",hcaes(Milliseconds,AccelerometerLinearZ)) %>% 
  hc_add_series(data,name = "XMAF","line",hcaes(Milliseconds,AccelerometerLinearXMAf)) %>% 
  hc_add_series(data,name = "YMAF","line",hcaes(Milliseconds,AccelerometerLinearYMAf)) %>%
  hc_add_series(data,name = "ZMAF","line",hcaes(Milliseconds,AccelerometerLinearZMAf)) 
