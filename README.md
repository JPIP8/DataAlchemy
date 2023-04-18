# DataAlchemy
Project involving Data Engineering, Data Science, and Machine Learning.

Important Files:
 - ETL.py: Cleanning process of the data.
 - P00.ipynb: The complete proyect in a jupyter notebook. It is more friendly to read.
 - README.md: The readme file.
 - main.py: Where the functions are located and is read by the server and deployed in the cloud.
 
 
 DataSets:
 - data.csv: Is the cleaned data file to use then in the machine learning function.
 - indx_4_ML.csv: Is the filtered data for the Machine Learning engine
 
 Files:
- requirements.txt: You can ignore this
- Count_vectorizer.joblib: You can ignore this
- cosine_similarity.joblib: You can ignore this
 

# Index

## 1. Load the data
 Loading the data from the different .csv files.

## 2. Data Transformation
 Cleaning, fixing nulls, and nomralizing data.

## 3. Development of the API
 Creation of an API. I proposed to make the company's data available using the FastAPI framework, generating different endpoints that will be consumed in the API.
 This is my working API: https://api-juanpabloidrovo.onrender.com/docs#/
 
 ### Allow me to explain the API calls, we have the following:
 
  - Get Max Duration: returns the longest movie of that year. Parameters:
    * year - the year of the movie
    * platform - the platform that has the movie
    * duration_type - minutes or seasons (in this case, only min)
    
  - Get Score Count: returns the number of movies that scored higher that the score of the user's input. Parameters:
    * platform - the platform that has the movie
    * scored - the score that the user wants
    * year - the year of the movie
  
  - Get Count Platform: returns the number of movies in the platform. Parameter:
    * platform - the platform that has the movie
    
  - Get Actor: returns the actor that appears the most by platform and year. Parameter:
    * platform - the platform that has the movie
    * year - the year of the movie
    
  - Get Prod Per Country: returns the NUMBER of content that was published by country and year. Parameters:
    * types - the type, movie or tv show
    * country - the country that the user wants
    * year - the year
    
  - Get Contents: returns the total NUMBER of content according to the given audience rating. Parameters:
    * rating - the rating of the given audience

  - Get Recommendation: returns a list of 5 similar movies according to the one that the user inputs. Parameters:
    * title - the title of the movie

## 4. Exploratory Data Analisys [EDA]
 Investigate the relationships between the variables of the datasets, see if there are any outliers or anomalies (which do not necessarily have to be errors), and look for any interesting patterns that are worth exploring in a further analysis.


## 5. Recomendation system with Machine Learning
 This consists of recommending movies to the users based on similar movies, so the similarity score between that movie and the rest of the movies must be found. They will be ordered according to the score and a Python list with 5 values will be returned, each being the string of the name of the movies with the highest score, in descending order.
