# DataAlchemy
Project involving Data Engineering, Data Science, and Machine Learning.

Files:
 - ETL.py: Cleanning process of the data.
 - P00.ipynb: The complete proyect in a jupyter notebook. It is more friendly to read.
 - README.md: The readme file.
 - data.csv: Is the cleaned data file to use then in the machine learning function.
 - main.py: Where the functions are located and is read by the server and deployed in the cloud.
 - requirements.txt: You can ignore this

 

# Index

## 1. Load the data
 Loading the data from the different .csv files.

## 2. Data Transformation
 Cleaning, fixing nulls, and nomralizing data.

## 3. Development of the API
 Creation of an API. I proposed to make the company's data available using the FastAPI framework, generating different endpoints that will be consumed in the API.

## 4. Exploratory Data Analisys [EDA]
 Investigate the relationships between the variables of the datasets, see if there are any outliers or anomalies (which do not necessarily have to be errors), and look for any interesting patterns that are worth exploring in a further analysis.


## 5. Recomendation system with Machine Learning
 This consists of recommending movies to the users based on similar movies, so the similarity score between that movie and the rest of the movies must be found. They will be ordered according to the score and a Python list with 5 values will be returned, each being the string of the name of the movies with the highest score, in descending order.
