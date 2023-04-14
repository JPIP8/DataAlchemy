# # Loading data
# #### Importing .csv files

#
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


# # Data Transformation
# #### 1. Generate ID field:
#     Each record's ID should consist of the first letter of the platform name, followed by the show_id already present in the dataset (e.g., "as123" for Amazon titles).
# #### 2. Fix Nulls:
#     Replace null values in the "rating" field with the string "G" (which corresponds to a maturity rating of "general for all audiences").
# #### 3. Normalize Dates:
#     If present, dates should be in the format "YYYY-mm-dd".
# #### 4. Normalize Case [camelCase]:
#     All text fields should be in lower case, without exception.
# #### 5. Transform the "duration" field:
#     The "duration" field should be split into two fields: "duration_int", which should be an integer representing the duration, and "duration_type", which should be a string indicating the unit of measurement ("min" for minutes or "season" for TV seasons).

#
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

dfP.head(3)
# dfP.tail()

#
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

# print(dfP['rating'].unique())       # Now there are no values from 'duration' [for example: '136 min']
dfP.head(3)

#
# ############################################################################
# ########################### 3. NORMALIZE DATES  ############################
# ############################################################################

# Some dates have white spaces therefore, they give error because they have another format.
# Stripping the white spaces from the dates:
dfP['date_added'] = dfP['date_added'].str.strip()

# Now that I don't have white spaces, I can change the format.
dfP['date_added'] = pd.to_datetime(dfP['date_added'], format='%B %d, %Y').dt.strftime('%Y-%m-%d')

dfP.head(3)

#
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

dfP.head(3)

#
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
dfP['duration_int'] = dfP['duration_int'].str.replace(r'[^0-9]', '')
dfP['duration_int'] = dfP['duration_int'].str.strip()

# Setting the 'duration_int' type as integer
dfP['duration_int'] = pd.to_numeric(dfP['duration_int'].replace('', '0'))
dfP['duration_int'] = dfP['duration_int'].astype(int)

# Replacing nulls with 'unknown' in the cast column
dfP['cast'].fillna('unknown', inplace=True)


dfP.head(3)
# dfP.info()


#
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
dfP['rating'].replace({'13+': 'PG-13', 'ALL': 'G', 'ALL_AGES': 'G', 'AGES_18_': 'NC-18', '18+': 'NC-18', '16+': 'NC-16', 'AGES_16_': 'NC-16', '16': 'NC-16', '7+': 'TV-Y7', 'TV-Y7-FV': 'TV-Y7'}, inplace=True)


# Change the name of rating to score
dfR = dfR.rename(columns={'rating': 'score'})

# I will GROUP BY 'movieId' and i'll take the mean from the ratings
dfR_gouped = dfR.groupby('movieId', as_index = False)   # Grouping while maintaining the original index
score = dfR_gouped.score.mean().round(1)               # Taking the mean of the grouped df and rounding it with one decimal

# Changing the name of "movieId" to 'id' so, it matches with the other dataFrame.
score = score.rename(columns = {'movieId' : 'id'})

# Merging the dfP [Platform] and dfR [Ratings] dataFrames with their id.
df_score = pd.merge(dfP, score, on = 'id', how = 'outer')



# # Development API:
# ## I proposed to make the company's data available using the FastAPI framework, generating different endpoints that will be consumed in the API.
# 
# #### Create 6 functions (remember that each one must have a decorator for each one@app.get('/'))):
# 
# 1. Movie (only movie, not series, or documentaries, etc.) with the longest duration by year, platform, and duration type. The function must be called get_max_duration(year, platform, duration_type) and must return only the string of the movie name.
# 
# 2. Number of movies (only movies, not series or documentaries, etc.) by platform, with a score higher than XX in a certain year. The function must be called get_score_count(platform, scored, year) and must return an int, with the total number of movies that meet the requested criteria.
# 
# 3. Number of movies (only movies, not series or documentaries, etc.) by platform. The function must be called get_count_platform(platform) and must return an int, with the total number of movies on that platform. The platforms must be named Amazon, Netflix, Hulu, Disney.
# 
# 4. Actor that appears the most by platform and year. The function must be called get_actor(platform, year) and must return only the string with the name of the actor that appears the most by the given platform and year.
# 
# 5. The quantity of content/products (everything available on streaming) that was published by country and year. The function must be called prod_per_county(type, country, year) and should return the type of content (movie, series, documentary) by country and year in a dictionary with the variables named 'country' (name of the country), 'year' (year), 'movie' (type of content).
# 
# 6. The total quantity of content/products (everything available on streaming, series, documentaries, movies, etc.) according to the given audience rating (for which audience was the movie classified). The function must be called get_contents(rating) and must return the total number of content with that audience rating.

#
# 1. Importing FASTAPI
from fastapi import FastAPI

# 2. Creating a FastAPI instance
app = FastAPI()

# 3. Defining a path operation decorato@app.get("/")

# 4. Define the path operation function
async def root():

# 5. Returning the content
    return {"message": "Hello World"}



#
dfP.head(3)

#
# ############################################################################
# ########################## 1. get_max_duration  ############################
# ############################################################################

# The function must be called get_max_duration(year, platform, duration_type) and must return only the string of the movie name.

@app.get("/get_max_duration/{year}/{platform}/{duration_type}")
async def get_max_duration(year: int, platform: str, duration_type: str):
# def get_max_duration(year: int, platform: str, duration_type: str):
    # Setting variables to lowercase
    platform = platform.lower()
    duration_type = duration_type.lower()

    # Setting the year variable type to int
    year = int(year)

    # This is an if statement for the user input variable [platform] transformation and for catching some potential errors.
    if platform in ['amazon prime', 'amazon', 'a']:
        p = 'a'
    elif platform in ['netflix', 'n']:
        p = 'n'
    elif platform in ['disney plus', 'disney', 'd']:
        p = 'd'
    elif platform in ['hulu', 'h']:
        p = 'h'
    else:
        somethingIsWrong = "Please enter correct values"
        return somethingIsWrong

    # This is an if statement for the user input variable [duration_type] transformation and for catching some potential errors.
    if duration_type in ['minutes', 'm', 'min']:
        d = 'min'
    elif duration_type in ['seasons', 'season', 's']:
        somethingIsWrong = "There are no movies with seasons"
        return somethingIsWrong
    else:
        somethingIsWrong = "Please enter correct values"
        return somethingIsWrong
    
    # This is an if statement for the user input variable [year] transformation and for catching some potential errors.
    if year < 1000:
        somethingIsWrong = "That year is too low"
        return somethingIsWrong
    elif year > 2030:
        somethingIsWrong = "Are you from the future? That year is too high"
        return somethingIsWrong
    else:
        y = year
     

    # Creating a filter for the different platforms that the user might set as an input.
    maskPlatform = dfP[dfP['id'].str.contains(p, na = False)].copy()

    # Creating a filter for the different duration types that the user might set as an input.
    mask_P_D= maskPlatform[maskPlatform['duration_type'].str.contains(d, na = False)]

    # Creating a filter for the different year that the user might set as an input.
    mask= mask_P_D[mask_P_D['release_year'] == y]


    # Looking for the MAX value in the filtered dataFrames.
    maxValue = mask['duration_int'].max(skipna = True)
    
    # Looking for the ROW with the MAX value in the filtered dataFrames.
    mask = mask.loc[mask['duration_int'] == maxValue].head(1)

    # Looking for the title of the movie in the filtered data.
    movieName = mask['title'].to_string(index = False)

    # Returning the title of the movie.
    return {"title": movieName}


test = get_max_duration(2014, 'amazon', 'min')
# print(test)


#
# ############################################################################
# ########################## 2. get_score_count  #############################
# ############################################################################

# 2. Number of movies (only movies, not series or documentaries, etc.) by platform, with a score higher than XX in a certain year.
# The function must be called get_score_count(platform, scored, year) and must return an int, with the total number of movies that meet the requested criteria.

@app.get("/get_score_count/{platform}/{scored}/{year}")
async def get_score_count(platform: str, scored: float, year: int):
# def get_score_count(platform: str, scored: float, year: int):

    # Error proof for user input - platform
    platform = platform.lower()
    if platform in ['amazon prime', 'amazon', 'a']:
        p = 'a'
    elif platform in ['netflix', 'n']:
        p = 'n'
    elif platform in ['disney plus', 'disney', 'd']:
        p = 'd'
    elif platform in ['hulu', 'h']:
        p = 'h'
    else:
        somethingIsWrong = "Please enter correct values"
        return somethingIsWrong

    # Error proof for user input - scored
    # Setting the scored variable type to float
    scored = float(scored)
    if scored < 0.0:
        somethingIsWrong = "The score provided is too low"
        return somethingIsWrong
    elif scored > 5.01:
        somethingIsWrong = "The score provided is too high"
        return somethingIsWrong
    else:
        s = scored

    # Error proof for user input - year
    # Setting the year variable type to int
    year = int(year)

    if year < 1000:
        somethingIsWrong = "The year provided is too low"
        return somethingIsWrong
    elif year > 2030:
        somethingIsWrong = "Are you from the future? The year provided is too high"
        return somethingIsWrong
    else:
        y = year



    # Filter by type - only movies
    mask = df_score[df_score['type'].str.contains('movie', na = False)].copy()

    # Filter by platform
    mask_platform = mask[mask['id'].str.contains(p, na = False)]

    # Filter by scored
    mask_score_platform = mask_platform[mask_platform['score'] >= s]


    # Filter by year
    mask_score_platform_year = mask_score_platform[mask_score_platform['release_year'] == y]

    # Making a COUNT() for the movies that meet all the criteria above
    get_score_count = mask_score_platform_year.title.count()
    get_score_count = int(get_score_count)

    # df_outer.info()
    mask_score_platform_year.head(3)

    return {"get_score_count" : get_score_count}

get_score_count('amaZon', 3.6, 2014)


#
# ############################################################################
# ######################### 3. get_count_platform  ###########################
# ############################################################################

# 3. Number of movies (only movies, not series or documentaries, etc.) by platform.
# The function must be called get_count_platform(platform) and must return an int, with the total number of movies on that platform.
# The platforms must be named Amazon, Netflix, Hulu, Disney.

@app.get("/get_count_platform/{platform}")
async def get_count_platform(platform: str):
# def get_count_platform(platform: str):
    
    # This is an if statement for the user input variable [platform] transformation and for catching some potential errors.
    platform = platform.lower()
    if platform in ['a', 'az', 'amazon', 'amazon prime']:
        plt = 'a'
    elif platform in ['n', 'netflix']:
        plt = 'n'
    elif platform in ['h', 'hulu']:
        plt = 'h'
    elif platform in ['d', 'disney', 'disney plus']:
        plt = 'd'
    else:
        somethingIsWrong = "Please enter correct values"
        return somethingIsWrong

    # Creating a filter for the different platforms that the user might set as an input.
    mask_plt_3 = dfP[dfP['id'].str.contains(plt, na = False)].copy()

    mask_movie_3 = mask_plt_3[mask_plt_3['type'].str.contains('movie', na = False)]

    # Making a count for the different titles of movies
    num_movies = mask_movie_3['title'].count()
    num_movies = int(num_movies)

    
    return {"num_movies": num_movies}
    # title - a9668! - n8807! - d1450! - h3073!
    
get_count_platform('az')




#
# ############################################################################
# ############################# 4. get_actor  ################################
# ############################################################################

# 4. Actor that appears the most by platform and year. The function must be called get_actor(platform, year)
# and must return only the string with the name of the actor that appears the most by the given platform and year.


@app.get("/get_actor/{platform}/{year}")
async def get_actor(platform: str, year: int):
# def get_actor(platform: str, year: int):
    
    # This is an if statement for the user input variable [platform] transformation and for catching some potential errors.
    platform = platform.lower()
    if platform in ['a', 'az', 'amazon', 'amazon prime']:
        plt = 'a'
    elif platform in ['n', 'netflix']:
        plt = 'n'
    elif platform in ['h', 'hulu']:
        plt = 'h'
    elif platform in ['d', 'disney', 'disney plus']:
        plt = 'd'
    else:
        somethingIsWrong = "Please enter correct values"
        return somethingIsWrong
    
    # This is an if statement for the user input variable [year] transformation and for catching some potential errors.
    if year < 1000:
        somethingIsWrong = "That year is too low"
        return somethingIsWrong
    elif year > 2030:
        somethingIsWrong = "Are you from the future? That year is too high"
        return somethingIsWrong
    else:
        y = year
    
    # Creating a filter for the different platforms that the user might set as an input.
    mask_plt_4 = dfP[dfP['id'].str.contains(plt, na = False)].copy()

    # Creating a filter for the different year that the user might set as an input.
    mask_year_4 = mask_plt_4[mask_plt_4['release_year'] == y]
    cast = mask_year_4['cast']

    # create a dictionary to count the frequency of each word
    word_counts = {}

    # iterate through the rows
    for row in cast:
        # iterate through the comma-separated elements in each row
        row = row.split(',')
        row = [word.strip() for word in row]

    # Count the number of occurrences of each word
        for word in row:
            if word in word_counts:
                word_counts[word] += 1
            else:
                word_counts[word] = 1

    # sorting the dictionary "word_counts"
    sorted_dict = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)

    # Taking the second value because the first value is "unknown" [they were nulls]
    second_max_key = sorted_dict[1][0] # Name of actor
    second_max_value = sorted_dict[1][1] # Number of times the actor appears

    actorName = second_max_key

    return {'actorName': actorName}

# Second max key: anne-marie newland
# Second max value: 5
get_actor('amazon', 2014)

#
dfP.head()
# dfP.type.unique()

#

# ############################################################################
# ########################## 5. prod_per_country  #############################
# ############################################################################

# 5. The quantity of content/products (everything available on streaming) that was published by country and year.
# The function must be called prod_per_country(type, country, year) and should return the type of content (movie, series, documentary)
# by country and year in a dictionary with the variables named 'country' (name of the country), 'year' (year), 'movie' (type of content).

@app.get("/prod_per_country/{types}/{country}/{year}")
async def prod_per_country(types: str, country: str, year: int):
# def prod_per_country(types: str, country: str, year: int):

    # Error proof for user input - country
    c = country.lower()


    # Error proof for user input - type
    types = types.lower()

    if types in ['movie', 'mov', 'm', 'pelicula', 'peli']:
        t = 'movie'
    elif types in ['tv show', 'tvshow', 'show', 'tv', 'series', 'season', 's']:
        t = 'tv show'
    else:
        somethingIsWrong = "Oops! The type provided is not right"
        return somethingIsWrong


    # Error proof for user input - year
    # Setting the year variable type to int
    year = int(year)

    if year < 1000:
        somethingIsWrong = "The year provided is too low"
        return somethingIsWrong
    elif year > 2030:
        somethingIsWrong = "Are you from the future? The year provided is too high"
        return somethingIsWrong
    else:
        y = year

    # Filtering by the user input - country
    mask_country = dfP[dfP['country'].str.contains(c, na = False)].copy()

    # Filtering by the user input - type
    mask_country_type = mask_country[mask_country['type'].str.contains(t, na = False)]

    # Filtering by the user input - type
    mask_country_type_year = mask_country_type[mask_country_type['release_year'] == y]

    # mask_country_type_year = mask_country_type_year.type.country.release_year

    prod_per_country = mask_country_type_year[['type', 'country', 'release_year']].reset_index(drop=True).to_dict('index')

    return {"prod_per_country" : prod_per_country}

prod_per_country('movie', 'indi', 2021)

#
dfP.head(3)

#
# ############################################################################
# ########################### 6. get_contents  ###############################
# ############################################################################

# 6. The total quantity of content/products (everything available on streaming, series, documentaries, movies, etc.)
# according to the given audience rating (for which audience was the movie classified).
# The function must be called get_contents(rating) and must return the total number of content with that audience rating.

@app.get("/get_contents/{rating}")
async def get_contents(rating: str):

# def get_contents(rating: str):

    # Creating a filter for the different RATING that the user might set as an input.
    mask_rating = dfP[dfP['rating'].str.contains(rating, na = False)].copy()

    # Making a count for the different titles of movies
    num_content = mask_rating['title'].count()
    get_contents = int(num_content)

    return {"get_contents" : get_contents}

get_contents('G')



