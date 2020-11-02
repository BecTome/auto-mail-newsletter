#%% Load Packages & Params
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

TEAM = '230618'

#%% Load Dataset Frim Source Folder

# A random sample of 100 teams from original dataset is read
dir_in = Path("src/data/")

df = pd.read_csv(dir_in.joinpath('Submissions_sum.csv'),
                 dtype={'Id':str,
                        'TeamId':str},
                 index_col=0)

df['SubmittedUserId'] = df['SubmittedUserId'].apply(lambda x: '{:0.0f}'.format(x))

df['ScoreDate'] = pd.to_datetime(df.ScoreDate, 
                                 infer_datetime_format=True)


#%% Scores Timeseries Plot

# Set dark background in order to be in harmony with the mail html background
plt.style.use('dark_background')

# Let's Filter by Team
df_g = df.copy()
df_g = df_g[(df_g['TeamId'] == TEAM)]

# Calculate best score by day from team
sc_by_team = df_g[['ScoreDate', 'PublicScoreFullPrecision', 'PrivateScoreFullPrecision']].\
              groupby('ScoreDate').max()

axscore = sc_by_team.plot(figsize=(18,10),style='--')

# Calculate best score by day and user in the team
sc_by_user = df_g[['ScoreDate', 'SubmittedUserId', 'PrivateScoreFullPrecision']].\
              groupby(['ScoreDate', 'SubmittedUserId']).max().reset_index(level=1).\
              pivot(columns='SubmittedUserId', values='PrivateScoreFullPrecision')

axscore2= sc_by_user.plot(ax=axscore, style='-o', markersize=12, linewidth=4)

l1 = axscore.legend(['Public', 'Private'], prop={'size': 20})
l2 = axscore2.legend(prop={'size': 20}) # this removes l1 from the axes.
axscore.add_artist(l1) # <-- just change here, refer to ax1 explicitly
axscore.set_title('Team {}: Performance in Kaggle Competition (User IDs)'.format(TEAM),
                  fontsize=30)
axscore.tick_params(axis='both', labelsize=15)

axscore.set_xlabel(axscore.get_xlabel(), fontsize=18)
axscore.set_ylabel(axscore.get_ylabel(), fontsize=18)
plt.savefig('src/img/scores_ts.png')
plt.show()

#%% Users Contributions Pie Chart

# Plot a piechart of the amount of contributions by user in the final solution
axpie = df_g[['SubmittedUserId', 'PrivateScoreFullPrecision']].\
                 groupby('SubmittedUserId').count().\
                 plot.pie(y='PrivateScoreFullPrecision', figsize=(10, 10),
                 autopct='%.2f%%', fontsize=20, pctdistance=.7, 
                 legend=False )
sns.color_palette("husl", 8)
axpie.set_title('Team {}: Members Submissions Amount (User IDs)'.format(TEAM), fontsize=30)
axpie.set_ylabel('')
plt.savefig('src/img/contrib_pie.png')
plt.show()

#%% Export Team Info to Attach
df_g.to_excel('src/other/team_{}.xlsx'.format(TEAM), index=False)