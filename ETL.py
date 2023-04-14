
# ####################################################################################################################
# ################################                                             #######################################
# ################################     Loading data - Importing .csv files     #######################################
# ################################                                             #######################################
# ####################################################################################################################


# Importing libraries:
import pandas as pd
from datetime import datetime
import matplotlib as plt
import numpy as np

# Loading the rating files:
df1 = pd.read_csv("ratings/1.csv")
df2 = pd.read_csv("ratings/2.csv")
df3 = pd.read_csv("ratings/3.csv")
df4 = pd.read_csv("ratings/4.csv")
df5 = pd.read_csv("ratings/5.csv")
df6 = pd.read_csv("ratings/6.csv")
df7 = pd.read_csv("ratings/7.csv")
df8 = pd.read_csv("ratings/8.csv")

# Loading the Platform files:
dfa = pd.read_csv("amazon_prime_titles.csv")
dfd = pd.read_csv("disney_plus_titles.csv")
dfh = pd.read_csv("hulu_titles.csv")
dfn = pd.read_csv("netflix_titles.csv")


# ####################################################################################################################
# ########################################                             ###############################################
# ########################################     Data Transformation     ###############################################
# ########################################                             ###############################################
# ####################################################################################################################


###  1. Generate ID field:
###  Each record's ID should consist of the first letter of the platform name, followed by the show_id already present in the dataset (e.g., "as123" for Amazon titles).

###  2. Fix Nulls:
###  Replace null values in the "rating" field with the string "G" (which corresponds to a maturity rating of "general for all audiences").

###  3. Normalize Dates:
###  If present, dates should be in the format "YYYY-mm-dd".

###  4. Normalize Case [camelCase]:
###  All text fields should be in lower case, without exception.

###  5. Transform the "duration" field:
###  The "duration" field should be split into two fields: "duration_int", which should be an integer representing the duration, and "duration_type", which should be a string indicating the unit of measurement ("min" for minutes or "season" for TV seasons).


# ############################################################################
# ######################### 1. GENERATE ID FIELDS  ###########################
# ############################################################################


# Merging the rating files into one since they are related:
# Creating one main data frame: Data Frame Ratings [dfR]

dfR = pd.concat([df1, df2, df3, df4, df5, df6, df7, df8], ignore_index = True)
# dfR.tail()

# Creating a unique ID for the dataframes so, when I merge them, there are not going to be 'show_id' duplicates.
dfa = dfa.assign(id = 'a' + dfa['show_id'].astype(str))
dfd = dfd.assign(id = 'd' + dfd['show_id'].astype(str))
dfh = dfh.assign(id = 'h' + dfh['show_id'].astype(str))
dfn = dfn.assign(id = 'n' + dfn['show_id'].astype(str))

# Merging the Platform files into one since they are related:
# Creating one main data frame: Data Frame Platform [dfP]

dfP = pd.concat([dfa, dfd, dfh, dfn], ignore_index = True)

# Sending the 'id' column to be first
cols = dfP.columns.tolist()
cols = ['id'] + [col for col in cols if col != 'id']
dfP = dfP.reindex(columns=cols)



# ############################################################################
# ############################## 2. FIX NULLS  ###############################
# ############################################################################

# I want to take a look at the unique values in dfP['rating']
#print(dfP['rating'].unique())       # After taking a look at 'rating' uniques values, i realized that there where values from 'duration'
                                    # I will copy the durations to the correct column


# Replace null values in 'duration' column with values from 'rating' column
dfP.loc[dfP['rating'].str.contains(' min', na=False), 'duration'] = dfP['rating']

# Replace remaining null values in 'duration' column with a string
dfP['duration'] = dfP['duration'].fillna('unknown')

# Replacing NULL values from 'rating' with 'G'
dfP['rating'] = dfP['rating'].fillna('G')

# Replace the 'duration' values in the 'rating' column with a string
dfP.loc[dfP['rating'].str.contains(' min', na=False), 'rating'] = 'Unknown'



# ############################################################################
# ########################### 3. NORMALIZE DATES  ############################
# ############################################################################

# Some dates have white spaces therefore, they give error because they have another format.
# Stripping the white spaces from the dates:
dfP['date_added'] = dfP['date_added'].str.strip()

# Now that I don't have white spaces, I can change the format.
dfP['date_added'] = pd.to_datetime(dfP['date_added'], format='%B %d, %Y').dt.strftime('%Y-%m-%d')



# ############################################################################
# ######################### 4. NORMALIZE lowercase  ##########################
# ############################################################################

dfP['type'] = dfP['type'].str.lower()
dfP['title'] = dfP['title'].str.lower()
dfP['director'] = dfP['director'].str.lower()
dfP['cast'] = dfP['cast'].str.lower()
dfP['country'] = dfP['country'].str.lower()
dfP['duration'] = dfP['duration'].str.lower()
dfP['listed_in'] = dfP['listed_in'].str.lower()
dfP['description'] = dfP['description'].str.lower()


# ############################################################################
# ################### 5. TRANSFORM THE 'DURATION' FIELD  #####################
# ############################################################################

# Stripping the white spaces from the duration:
dfP['duration'] = dfP['duration'].str.strip()

# Analyzing the content of the field duration:
dfP['duration'].unique()

# Creating two new columns
dfP['duration_int'] = dfP['duration']
dfP['duration_type'] = dfP['duration']


# Setting the 'duration_type' column
dfP.loc[dfP['duration_type'].str.contains('min', na = False), 'duration_type'] = 'min'
dfP.loc[dfP['duration_type'].str.contains('season', na = False), 'duration_type'] = 'season'

# Setting the 'duration_int' column
# dfP['duration_int'] = dfP['duration_int'].str.replace(r'[^0-9]', '')
dfP['duration_int'] = dfP['duration_int'].apply(lambda x: ''.join(filter(str.isdigit, str(x))))
dfP['duration_int'] = dfP['duration_int'].str.strip()

# Setting the 'duration_int' type as integer
# dfP['duration_int'] = pd.to_numeric(dfP['duration_int'].replace('', '0'))
dfP['duration_int'] = dfP['duration_int'].fillna('').replace('', 0)
dfP['duration_int'] = dfP['duration_int'].astype(int)

# Replacing nulls with 'unknown' in the cast column
dfP['cast'].fillna('unknown', inplace=True)



# ############################################################################
# #################### 6. TRANSFORMATIONS - BONUS TRACK ######################
# ############################################################################

# Drop show_id column because now we have id column
dfP.drop(columns = 'show_id', inplace = True)

# Drop duration column because we splitted that one in two
dfP.drop(columns = 'duration', inplace = True)

# Replacing some unknown values with 'not rated'.
dfP['rating'].replace({'UNRATED': 'not rated', 'NOT_RATE': 'not rated', 'NOT RATED': 'not rated', 'Unknown': 'not rated', 'UR': 'not rated', 'NR': 'not rated'}, inplace=True)
mask = dfP['rating'].str.contains('eason')
dfP.loc[mask, 'rating'] = 'not rated'

# Replacing some known repeated values with one unified value.
dfP['rating'].replace({'13+': 'PG-13', 'ALL': 'g', 'ALL_AGES': 'g', 'AGES_18_': 'NC-18', '18+': 'NC-18', '16+': 'NC-16', 'AGES_16_': 'NC-16', '16': 'NC-16', '7+': 'TV-Y7', 'TV-Y7-FV': 'TV-Y7'}, inplace=True)

# NORMALIZE lowercase
dfP['rating'] = dfP['rating'].str.lower()


# Change the name of rating to score
dfR = dfR.rename(columns={'rating': 'score'})

# I will GROUP BY 'movieId' and i'll take the mean from the ratings
dfR_gouped = dfR.groupby('movieId', as_index = False)   # Grouping while maintaining the original index
score = dfR_gouped.score.mean().round(1)               # Taking the mean of the grouped df and rounding it with one decimal

# Changing the name of "movieId" to 'id' so, it matches with the other dataFrame.
score = score.rename(columns = {'movieId' : 'id'})

# Merging the dfP [Platform] and dfR [Ratings] dataFrames with their id.
df_score = pd.merge(dfP, score, on = 'id', how = 'outer')


# For testing purposes:
# print(df_score.head())


# ############################################################################
# ########################## 7. EXPORTING AS .CSV ############################
# ############################################################################

df_score.to_csv('data.csv', index = False)
