# Movie Rating Analysis

## Overview

This project analyzes movie ratings using Netflix and IMDb datasets.

The goal is to understand which factors affect movie ratings.

---

## Methods

* Data collection and merging (Netflix + IMDb)
* Data cleaning
* Exploratory Data Analysis (EDA)
* Hypothesis testing

---

## Visualizations and Code

### IMDb Score Distribution

![IMDb](plots/grafik/imdb_score_distribution.png)

```python
plt.hist(clean["imdb_score"], bins=20)
plt.xlabel("IMDb Score")
plt.ylabel("Frequency")
plt.title("Distribution of IMDb Scores")
```

This graph shows how IMDb scores are distributed across movies.

---

### Average Score by Genre

![Genre](plots/grafik/average_score_by_genre.png)

```python
plt.bar(genre_plot.index, genre_plot["mean"])
plt.xticks(rotation=45)
plt.title("Average IMDb Score by Genre")
```

This graph shows that some genres have higher average ratings than others.

---

### Votes vs Score

![Votes](plots/grafik/votes_vs_score.png)

```python
plt.scatter(clean["num_voted_users"], clean["imdb_score"])
plt.xlabel("Votes")
plt.ylabel("Score")
```

This graph shows a positive relationship between votes and ratings.

---

### Year vs Score

![Year](plots/grafik/score_by_release_year.png)

```python
plt.plot(year_avg["release_year"], year_avg["imdb_score"])
plt.xlabel("Year")
plt.ylabel("Score")
```

This graph shows how ratings change over time.

---

### Duration vs Score

![Duration](plots/grafik/duration_vs_score.png)

```python
plt.scatter(clean["duration_min"], clean["imdb_score"])
```

This graph shows the relationship between movie duration and rating.

---

## Conclusion

* Movies with more votes tend to have higher ratings
* Genre has a significant effect on ratings
* Older movies tend to have slightly higher ratings in this dataset
* Duration also has a small effect on ratings

---

## Author

Alim Ata Balcı
