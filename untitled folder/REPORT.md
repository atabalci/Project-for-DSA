# Analysis of Factors Affecting Movie Ratings

## 1. Project Aim

This project studies which factors affect movie ratings.  
I used two datasets:

- **Netflix dataset** for movie information such as title, genre, release year, and duration
- **IMDb dataset** for audience information such as IMDb score and number of votes

The main goal is to understand which variables are related to movie ratings.

---

## 2. Data Collection

The data comes from two CSV files:

1. `netflix_titles.csv`
2. `movie_metadata.csv`

### Why these datasets were used

The Netflix dataset gives content-related variables:
- title
- type
- release year
- duration
- listed genres

The IMDb dataset gives rating-related variables:
- IMDb score
- number of voted users

Using both datasets together is useful because one dataset shows movie characteristics and the other shows audience response.

### Data merging

The two datasets were merged by movie title.

### Data cleaning steps

- Only **movies** were kept from the Netflix dataset
- Titles were changed to lowercase to make merging easier
- Only rows with the **same release year** in both datasets were kept
- Duration was converted to minutes
- The first listed Netflix genre was used as the main genre
- Missing values were removed from the final analysis table

### Final dataset size

After cleaning and merging, the final dataset includes **671 movies**.

---

## 3. Variables Used

The main variables in the final dataset are:

- `title`
- `release_year`
- `duration_min`
- `primary_genre`
- `imdb_score`
- `num_voted_users`

The dependent variable is **IMDb score**.  
The independent variables are **genre**, **release year**, **duration**, and **number of voted users**.

---

## 4. Exploratory Data Analysis (EDA)

### 4.1 Distribution of IMDb scores

The histogram shows that most movies are between medium and high scores.  
Very low scores are less common.

### 4.2 Genre and rating

The genre chart shows that average IMDb scores are not the same for all genres.

Main results:
- **Classic Movies** have the highest average score among large groups
- **Dramas** also have high average scores
- **Horror Movies** have the lowest average score among large groups

### 4.3 Vote count and rating

The scatter plot shows a positive relationship between vote count and IMDb score.  
Movies with more votes often have higher scores.

### 4.4 Release year and rating

The line graph shows that movie ratings change across years.  
Older movies in this merged sample have a slightly higher average score than newer movies.

### 4.5 Duration and rating

The duration plot shows a positive relationship between movie length and IMDb score.  
Longer movies often have slightly higher scores in this sample.

---

## 5. Hypothesis Testing

### Hypothesis 1: Vote count and IMDb score

- **H0:** There is no relationship between vote count and IMDb score.
- **H1:** There is a relationship between vote count and IMDb score.

**Test used:** Pearson correlation

**Result:**  
- Correlation = **0.521**
- p-value = **5.69927e-48**

**Decision:** Since p < 0.05, I reject H0.  
There is a statistically significant positive relationship between vote count and IMDb score.

---

### Hypothesis 2: Genre and IMDb score

- **H0:** Average IMDb scores are the same across genres.
- **H1:** At least one genre has a different average IMDb score.

**Test used:** One-way ANOVA

**Genres used in the test:** Action & Adventure, Dramas, Comedies, Children & Family Movies, Horror Movies, Classic Movies

**Result:**  
- F-statistic = **30.613**
- p-value = **6.71522e-28**

**Decision:** Since p < 0.05, I reject H0.  
Genre has a statistically significant effect on IMDb score.

---

### Hypothesis 3: Old movies vs new movies

- **H0:** Movies released before 2000 and movies released in 2000 or later have the same average IMDb score.
- **H1:** Their average IMDb scores are different.

**Test used:** Welch's t-test

**Result:**  
- Mean IMDb score before 2000 = **6.866**
- Mean IMDb score in 2000 and after = **6.483**
- t-statistic = **3.684**
- p-value = **0.00029439**

**Decision:** Since p < 0.05, I reject H0.  
There is a statistically significant difference between older and newer movies in this sample.

---

## 6. Conclusion

This analysis shows that movie ratings are related to more than one factor.

The most important findings are:

1. Movies with more votes tend to have higher IMDb scores.
2. Average IMDb scores change by genre.
3. Older movies in this sample have higher average scores than newer movies.
4. Longer movies also seem to have somewhat higher ratings.

In general, both **content-related variables** and **audience-related variables** help explain movie ratings.

---

## 7. Files in This Project

- `merged_cleaned_movies.csv` -> final cleaned dataset
- `summary_statistics.csv` -> summary statistics
- `genre_rating_summary.csv` -> average scores by genre
- `hypothesis_test_results.txt` -> test outputs
- `plots/` -> all figures
- `data_collection_eda_hypothesis_testing.py` -> full analysis code

