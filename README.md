# Prediction of role a player played in League of Legends matches.
Orlando Fang's DSC 80 Project 5

by Orlando Fang (tifang@ucsd.edu)

My exploratory data analysis on this dataset can be found [here](https://orlandofang.github.io/most-exciting-league-in-league-of-legends/).

## Problem Identification
Prediction Problem: Predict which role (top-lane, jungle, support, etc.) a player played given their post-game data.

Problem Type: multiclass classification (total of 5 different values: top,jug,mid,bot,and sup)

Response Variable: Position the player played in a match. I chose the positions of each player as the response variable because positions represent the roles of the players, which is what I am trying to predict.

Metric I am using to evaluate your model: Accuracy, because a false positive and a false negative are equally bad when predicting a role. Also, I've checked the counts of each position in the testing dataset and found out that each position has a proportion of roughly 1/5, meaning that there is no class imbalance in the data set. If I predict all data points to a single position, I would only get 1/5 accuracy. Thus, accuracy will not be misleading. Also, since the purpose of this website is for the general public, I think accuracy, which represents the proportion of data the model predicted correctly, will be easier to interpret compared to F1-Score.

