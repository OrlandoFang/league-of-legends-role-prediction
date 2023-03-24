# Prediction of role a player played in League of Legends matches.
Orlando Fang's DSC 80 Project 5

by Orlando Fang (tifang@ucsd.edu)

My exploratory data analysis on this dataset can be found [here](https://orlandofang.github.io/most-exciting-league-in-league-of-legends/).

## Problem Identification
Prediction Problem: Predict which role (top-lane, jungle, support, etc.) a player played given their post-game data.

Problem Type: multiclass classification (total of 5 different values: top,jug,mid,bot,and sup)

Response Variable: Position the player played in a match. I chose the positions of each player as the response variable because positions represent the roles of the players, which is what I am trying to predict.

Metric I am using to evaluate your model: Accuracy, because a false positive and a false negative are equally bad when predicting a role. Also, I've checked the counts of each position in the testing dataset and found out that each position has a similar proportion of roughly 1/5, meaning that there is no class imbalance in the data set. If I predict all data points to a single position, I would only get 1/5 accuracy. Thus, accuracy will not be misleading. Also, since the purpose of this website is for the general public, I think accuracy, which represents the proportion of data the model predicted correctly, will be easier to interpret compared to F1-Score.

Time of prediction: Predicting roles given post-game data, so all data can be used for training.

## Baseline Model
Describe your model and state the features in your model, including how many are quantitative, ordinal, and nominal, and how you performed any necessary encodings. Report the performance of your model and whether or not you believe your current model is “good” and why.
For my baseline model, I used champion and total cs as the features for predicting position. There is one nominal feature, champion, which values are the name of the champion that each player picked. There is one quantitative(discrete) feature, total cs, which is the creep score or the number minions and jungle monsters a player killed throughout the game. There is no ordinal feature.
I tranformed the champion column with one hot encoding with the OneHotEncoder transformer since it contains nominal values. With ColumnTransformer, I am only one hot encoding the champion column and leaving the numerical features as-is.
For the baseline model, I've reached a score of 0.672 for the training dataset and a score of 0.672 for the testing dataset, meaning that for both my training dataset and my testing dataset my baseline model predicted 67.2% of the position correctly. 
I do not think my current baseline model is a good model because the accuracy score is not great. The current model can only predict correctly roughly 2/3 of the time, which makes it very untrustworthy. Also, different roles in league of legends have different tasks, so a good model should be able to differenciate positions more accurately.

