# ####################################################################################################################
# ################################                                             #######################################
# ################################     Loading data - Importing .csv files     #######################################
# ################################                                             #######################################
# ####################################################################################################################

# Importing libraries:
import pandas as pd
from fastapi import FastAPI


# Loading the files:
df = pd.read_csv("data.csv")


# ####################################################################################################################
# ######################################                                 #############################################
# ######################################         Development API         #############################################
# ######################################                                 #############################################
# ####################################################################################################################

### I proposed to make the company's data available using the FastAPI framework, generating different endpoints that will be consumed in the API.
### Create 6 functions (remember that each one must have a decorator for each one@app.get('/'))):

# 1. Movie (only movie, not series, or documentaries, etc.) with the longest duration by year, platform, and duration type. The function must be called get_max_duration(year, platform, duration_type) and must return only the string of the movie name.

# 2. Number of movies (only movies, not series or documentaries, etc.) by platform, with a score higher than XX in a certain year. The function must be called get_score_count(platform, scored, year) and must return an int, with the total number of movies that meet the requested criteria.

# 3. Number of movies (only movies, not series or documentaries, etc.) by platform. The function must be called get_count_platform(platform) and must return an int, with the total number of movies on that platform. The platforms must be named Amazon, Netflix, Hulu, Disney.

# 4. Actor that appears the most by platform and year. The function must be called get_actor(platform, year) and must return only the string with the name of the actor that appears the most by the given platform and year.

# 5. The quantity of content/products (everything available on streaming) that was published by country and year. The function must be called prod_per_county(type, country, year) and should return the type of content (movie, series, documentary) by country and year in a dictionary with the variables named 'country' (name of the country), 'year' (year), 'movie' (type of content).

# 6. The total quantity of content/products (everything available on streaming, series, documentaries, movies, etc.) according to the given audience rating (for which audience was the movie classified). The function must be called get_contents(rating) and must return the total number of content with that audience rating.


# Creating a FastAPI instance
app = FastAPI()

# ############################################################################
# ########################## 1. get_max_duration  ############################
# ############################################################################

# The function must be called get_max_duration(year, platform, duration_type) and must return only the string of the movie name.

@app.get("/get_max_duration/{year}/{platform}/{duration_type}")
def get_max_duration(year: int, platform: str, duration_type: str):

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
    maskPlatform = df[df['id'].str.contains(p, na = False)].copy()

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
    return {"movieName": movieName}


test = get_max_duration(2014, 'amazon', 'min')
print(test)


# ############################################################################
# ########################## 2. get_score_count  #############################
# ############################################################################

# 2. Number of movies (only movies, not series or documentaries, etc.) by platform, with a score higher than XX in a certain year.
# The function must be called get_score_count(platform, scored, year) and must return an int, with the total number of movies that meet the requested criteria.

@app.get("/get_score_count/{platform}/{scored}/{year}")
def get_score_count(platform: str, scored: float, year: int):

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
    mask = df[df['type'].str.contains('movie', na = False)].copy()

    # Filter by platform
    mask_platform = mask[mask['id'].str.contains(p, na = False)]

    # Filter by scored
    mask_score_platform = mask_platform[mask_platform['score'] >= s]


    # Filter by year
    mask_score_platform_year = mask_score_platform[mask_score_platform['release_year'] == y]

    # Making a COUNT() for the movies that meet all the criteria above
    get_score_count = mask_score_platform_year.title.count()
    get_score_count = int(get_score_count)

    mask_score_platform_year.head(3)

    return {
        "platform" : platform,
        "quantity" : get_score_count,
        "year" : year,
        "score" : scored
        }

print(get_score_count('amaZon', 3.6, 2014))



# ############################################################################
# ######################### 3. get_count_platform  ###########################
# ############################################################################

# 3. Number of movies (only movies, not series or documentaries, etc.) by platform.
# The function must be called get_count_platform(platform) and must return an int, with the total number of movies on that platform.
# The platforms must be named Amazon, Netflix, Hulu, Disney.

@app.get("/get_count_platform/{platform}")
def get_count_platform(platform: str):
    
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
    mask_plt_3 = df[df['id'].str.contains(plt, na = False)].copy()

    mask_movie_3 = mask_plt_3[mask_plt_3['type'].str.contains('movie', na = False)]

    # Making a count for the different titles of movies
    num_movies = mask_movie_3['title'].count()
    num_movies = int(num_movies)

    
    return {
        "platform" : platform,
        "movies" : num_movies
        }
    
print(get_count_platform('az'))





# ############################################################################
# ############################# 4. get_actor  ################################
# ############################################################################

# 4. Actor that appears the most by platform and year. The function must be called get_actor(platform, year)
# and must return only the string with the name of the actor that appears the most by the given platform and year.


@app.get("/get_actor/{platform}/{year}")
def get_actor(platform: str, year: int):
    
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
    mask_plt_4 = df[df['id'].str.contains(plt, na = False)].copy()

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
    actorName = sorted_dict[1][0] # Name of actor
    frequency = sorted_dict[1][1] # Number of times the actor appears

    return {
        "platform" : platform,
        "year" : year,
        "actor" : actorName,
        "frequency" : frequency}


print(get_actor('amazon', 2014))



# ############################################################################
# ########################## 5. prod_per_country  #############################
# ############################################################################

# 5. The quantity of content/products (everything available on streaming) that was published by country and year.
# The function must be called prod_per_country(type, country, year) and should return the type of content (movie, series, documentary)
# by country and year in a dictionary with the variables named 'country' (name of the country), 'year' (year), 'movie' (type of content).

@app.get("/prod_per_country/{types}/{country}/{year}")
def prod_per_country(types: str, country: str, year: int):

    # Error proof for user input - country
    c = country.lower()


    # Error proof for user input - type
    types = types.lower()

    if types in ['movie', 'movies', 'mov', 'm', 'pelicula', 'peli']:
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
    mask_country = df[df['country'].str.contains(c, na = False)].copy()

    # Filtering by the user input - type
    mask_country_type = mask_country[mask_country['type'].str.contains(t, na = False)]

    # Filtering by the user input - type
    mask_country_type_year = mask_country_type[mask_country_type['release_year'] == y]



    prod_per_country = mask_country_type_year[['type', 'country', 'release_year']].reset_index(drop=True)
    count_type = int(prod_per_country.type.count())


    return {
        "country" : prod_per_country.country[0],
        "year" : year,
        "movies" : count_type}

print(prod_per_country('movie', 'indi', 2021))


# ############################################################################
# ########################### 6. get_contents  ###############################
# ############################################################################

# 6. The total quantity of content/products (everything available on streaming, series, documentaries, movies, etc.)
# according to the given audience rating (for which audience was the movie classified).
# The function must be called get_contents(rating) and must return the total number of content with that audience rating.

@app.get("/get_contents/{rating}")
def get_contents(rating: str):

    # Creating a filter for the different RATING that the user might set as an input.
    mask_rating = df[df['rating'].str.contains(rating, na = False)].copy()

    # Making a count for the different titles of movies
    num_content = mask_rating['title'].count()
    get_contents = int(num_content)

    return {
        "rating" : rating,
        "contents" : get_contents}

print(get_contents('g'))


# ############################################################################
# ######################## 7. get_recommendation  ############################
# ############################################################################

# import pickle

import joblib

# 7. This consists of recommending movies to the users based on similar movies, so the similarity score between
# that movie and the rest of the movies must be found. They will be ordered according to the score and a Python
# list with 5 values will be returned, each being the string of the name of the movies with the highest score,
# in descending order.



@app.get("/get_recommendation/{title}")
def get_recommendation(title: str):

    # Loading the files:
    indx = pd.read_csv("indx_4_ML.csv")


    # Loading the cosine similarity matrix
    accurate_cosine_sim = joblib.load('cosine_similarity.joblib')

    idx = indx[indx['title'] == title].index[0]



    # Creating score for similar movies
    similarScores = list(enumerate(accurate_cosine_sim[idx]))

    # Sorting that score
    similarScores = sorted(similarScores, key = lambda x : x[1], reverse = True)

    # Taking the score of the first 5 movies
    similarScores = similarScores[1:6]

    # Finding the index from those movies
    movieIndex = [i[0] for i in similarScores]
    recommendationTitles =  df.title.iloc[movieIndex]
    recommendationTitles = recommendationTitles.tolist()

    return {"recommendation" : recommendationTitles}

print(get_recommendation('sweet girl'))

