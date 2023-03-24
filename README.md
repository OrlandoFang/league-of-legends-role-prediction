# Prediction of role a player played in League of Legends competitive matches.
Orlando Fang's DSC 80 Project 5

by Orlando Fang (tifang@ucsd.edu)

My exploratory data analysis on this dataset can be found [here](https://orlandofang.github.io/most-exciting-league-in-league-of-legends/).

## Problem Identification
Prediction Problem: Predict which role (top-lane, jungle, support, etc.) a player played given their post-game data.

Problem Type: multiclass classification (total of 5 different values: top,jug,mid,bot,and sup)

Response Variable: Position the player played in a match. I chose the positions of each player as the response variable because positions represent the roles of the players, which is what I am trying to predict.

Metric I am using to evaluate your model: Accuracy, because a false positive and a false negative are equally bad when predicting a role. Both false positive and false negative means that the player did not performed like the role the player was assigned. Also, I've checked the counts of each position in the testing dataset and found out that each position has a similar proportion of roughly 1/5, meaning that there is no class imbalance in the data set. If I predict all data points to a single position, I would only get 1/5 accuracy. Thus, accuracy will not be misleading. Also, since the purpose of this website is for the general public, I think accuracy, which represents the proportion of data the model predicted correctly, will be easier to interpret compared to F1-Score.

Time of prediction: Predicting roles given post-game data, so all data can be used for training.

## Baseline Model
For my baseline model, I used champion and total cs as the features for predicting position. There is one nominal feature, champion, which values are the name of the champion that each player picked. There is one quantitative(discrete) feature, total cs, which is the creep score or the number minions and jungle monsters a player killed throughout the game. There is no ordinal feature. I chose champion and total cs as the two features for training my baseline model because some champions are highly correlated with certain positions, so by one hot encoding the champion column I should be classify roles better. I also included total cs as one the features because different roles have different total cs, for example a support should have the lowest total cs for most matches, so I've included total cs to help me with classifying roles based on such differences.
I tranformed the champion column with one hot encoding with the OneHotEncoder transformer since it contains nominal values. With ColumnTransformer, I am only one hot encoding the champion column and leaving the numerical features as-is.
For the baseline model, I used DecisionTreeClassifier because I am working with a multiclass classification problem. I reached a score of 0.672 for the training dataset and a score of 0.672 for the testing dataset, meaning that for both my training dataset and my testing dataset my baseline model predicted 67.2% of the position correctly. 
I do not think my current baseline model is a good model because the accuracy score is not great. The current model can only predict correctly roughly 2/3 of the time, which makes it very untrustworthy. Also, different roles in League of Legends have different tasks, meaning that difference between roles should be obvious, so a good model should be able to differenciate positions more accurately.

## Final Model
For the final  model, I improved upon the baseline model and added the following features:
- damageshare. In League of Legends, mid and bot are usually roles that does most of the damages. Top and jug sometimes do a lot of damage depending on the champions they picked. Sup usually does the least damages. I think the damageshare of each player can signal the player's role in the team, which can help me identify the role of the player, where high damageshare would be assigned with a higher probability of being mid or bot, and low damageshare would be assigned with a higher probabiliy to being sup. I standardized the values so that the difference between damageshare of different roles are clear.
- damagetakenperminute. In League of Legends, top usually pick tank champions and takes the largest amount of the damages. Sup and jug sometimes take a lot of damage depending on the champions they picked. Bot and mid usually have low health and thus take the leasest amount of damages. I think the damagetakenperminute of each player can signal the player's role in the team, which can help me identify the role of the player, where a high damagetakenperminute would increase the likelyhood of being top lane. I standardized the values so that the difference between damagetakenperminute of different roles are clear.
- minionkills. Mid and bot are roles that usually has more minionkills than other positions because mid and bot are the damage-dealers of the team and they need to kill minions to gain gold and buy items. Top usually has higher minionkills than sup and jug, but not as high as mid and bot because top lane players usually have to assist other lanes and thus sacrifice their time that could be used for killing minions. Jug has low minionkills because jug players earn their gold by killing monsters instead of killing minions. Sup also has low minionkills because sup players let bot players kill most of the minions so that bot players have more gold. Because the difference between minionkills of top,mid,bot players and jug,sup players is large, I decided to binarize the column with a threshold on the mean of minionkills. Then most top,mid,bot players will have a value of 1 and most jug,sup players will have a value of 0. This can help my model to differentiate between roles.
- monsterkills. Similar reason as minionkills. Jug players have highest monsterkills while other roles gain most of their gold by kill minions instead of monsters. Binarized with a threshold on the mean of monsterkills so that most Jug players will be assigned with a value of 1 and other players will have a value of 0. This can help my model to predict jug players more accurately.
- vspm. Similar reason as minionkills. Sup players usually have the highest vspm (Vision Score per Minute) because their main task is to support the team instead of dealing damages, and supports can support the team by providing more wards, which give vision for the team, and clearing enemy wards. Jug players usually also have higher vspm than top,mid,bot players because jug players need to clear enemy wards in order to gank enemy players or take control of Dragons, Barons, and Rift Herald. I also binarized with a threshold on the mean of vspm because vspm is usually higher for sup and jug players, and this can my model to differentiate between roles.

Since I am dealing with a multiclass classification problem where I want to predict the players' roles, which are nominal values, I believe using a DecisionTreeClassifier would be the simplest way to implement the model and it can provide me with the most accurate results.
I used GridSearchCV to find the best combination of hyperparameters out of a total of 80 combinations. The combinations consists 8 different values of max_depth, 5 different values of min_samples_split, and 2 different values for criterion. The hyperparameters that ended up performing the best is the combination: {'criterion': 'gini', 'max_depth': 77, 'min_samples_split': 100}

Before tuning the best hyperparameters, my scores for my training dataset and my testing dataset were both around 0.81, which is a large improvement in accuracy compared to my baseline model, showing that the features I added for the final model did improve accuracy. After tuning for the best hyperparameters and passing the combination to my DecisionTreeClasifier, I reached a score of 0.970 for my training dataset and a score of 0.962 for my testing dataset. While there seems to be a slight overfitting, the accuracy for unseen data largely improved. Compared to my baseline model's score of 0.672 for unseen data, my final model's performance is a lot better where accuracy greatly improved and a lot more roles are predicted correctly. The performance also largely improved after tuning for the best hyperparameters, showing that both adding new features and finding best hyperparameters are essential for improving performance.

## Fairness Analysis
Check fairness based on damageshare each player contributed. If a player contributed over 1/5 of the damageshare, the player is a damage-dealer, otherwise a support. Threshold set at 1/5 because there are 5 players on a team, so each player is expected to contribute a damageshare of 0.2. However, in League of Legends, not all roles are expected to contribute equal amount of damages, there are damage-dealing roles and support/tank roles, so I assigned a player as damage-dealer if the player's damageshare is larger than 0.2, otherwise a support.

Group X: Damage-dealer

Group Y: Support

Evalution metric: Accuracy, because a false positive and a false negative are equally bad when predicting a role. Both false positive and false negative means that the player did not performed like the role the player was assigned. Also, I've checked the counts of each position in the testing dataset and found out that each position has a similar proportion of roughly 1/5, meaning that there is no class imbalance in the data set. If I predict all data points to a single position, I would only get 1/5 accuracy. Thus, accuracy will not be misleading. Also, since the purpose of this website is for the general public, I think accuracy, which represents the proportion of data the model predicted correctly, will be easier to interpret compared to F1-Score.

Null Hypothesis: Our model is fair. Its precision for damager-dealers and supports are roughly the same, 
and any differences are due to random chance.

Alternative Hypothesis: Our model is unfair. Its precision for damager-dealers is lower than its precision for supports.

Test statistic: Difference in accuracy (support minus damage-dealers).

Significance level: 0.01
 
I picked Significance level of 0.01 to be highly significant and to minimize the risk of concluding that a difference exists when there is no actual difference.
  
Resulting p-value: 0.00

Result after 1000 repetitions of permutation test.

Conclusion: Since my resulting p-value 0.00 is smaller than the significance level of 0.01, I reject the null hypothesis, which claims that the model is fair and its precision for damager-dealers and supports are roughly the same and any differences are due to random chance. 
