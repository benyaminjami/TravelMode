library(dplyr)
library(readr)
library(ggplot2)
Car = read_csv('PycharmProjects/git/data/WalkCarClustering/Car/CarNormalized.csv')
Walk = read_csv('PycharmProjects/git/data/WalkCarClustering/Walk/WalkNormalized.csv')

library(tidyr)

period = 1175

Car %>%
  select(-c(RotationVectorX,RotationVectorY,RotationVectorZ,RotationVectorcos,RotationVectorheadingAccuracy,GPSLatitude,GPSLongitude,GPSAltitude)) %>% 
  mutate(Block = floor(Milliseconds / period), sample = floor((Milliseconds %% period)/25)) %>% 
  select(-Milliseconds) -> Car
Car %>% gather(Var, val, -(Block:sample)) %>% 
  unite(Var1,Var, sample) %>% 
  spread(Var1, val) %>% mutate(Label = 1) -> CarBlocked

Walk %>%
  select(-c(RotationVectorX,RotationVectorY,RotationVectorZ,RotationVectorcos,RotationVectorheadingAccuracy,GravityX,GravityY,GravityZ)) %>% 
  mutate(Block = floor(Milliseconds / period), sample = floor((Milliseconds %% period)/25)) %>% 
  select(-Milliseconds) -> Walk
Walk %>% gather(Var, val, -(Block:sample)) %>% 
  unite(Var1,Var, sample) %>% 
  spread(Var1, val) %>% mutate(Label = 2) -> WalkBlocked

data = rbind(CarBlocked,WalkBlocked)
data %>% drop_na() -> data
kmeans(data %>% select(-c(Label,Block)) %>% scale(),centers = 2) -> kcl
prcomp(data %>% select(-c(Label,Block)),scale. = T) -> pca
pca$x %>% as.data.frame() %>% select(PC1,PC2) -> pca_data
pca_data$Label = data$Label
ggplot() + geom_point(data = pca_data,aes(x = PC1,y=PC2,color = as.factor(Label),size = as.factor(kcl$cluster)))

data = rbind(Car %>% mutate(Label = 1),Walk %>% mutate(Label = 2))
data %>% drop_na() -> data
kmeans(data %>% select(-c(Label,Block)) %>% scale(),centers = 2) -> kcl
prcomp(data %>% select(-c(Label,Block)),scale. = T) -> pca
pca$x %>% as.data.frame() %>% select(PC1,PC2) -> pca_data
pca_data$Label = data$Label
ggplot() + geom_point(data = pca_data,aes(x = PC1,y=PC2,color = as.factor(Label)))
