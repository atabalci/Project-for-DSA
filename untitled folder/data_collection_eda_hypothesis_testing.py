import os
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import pearsonr, f_oneway, ttest_ind

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PLOTS_DIR = os.path.join(BASE_DIR, "plots")
os.makedirs(PLOTS_DIR, exist_ok=True)

netflix = pd.read_csv("netflix_titles.csv")
movie = pd.read_csv("movie_metadata.csv")

netflix_movies = netflix[netflix["type"] == "Movie"].copy()
netflix_movies["title_norm"] = netflix_movies["title"].astype(str).str.strip().str.lower()
movie["title_norm"] = movie["movie_title"].astype(str).str.strip().str.lower()

merged = pd.merge(
    netflix_movies,
    movie,
    on="title_norm",
    suffixes=("_netflix", "_imdb")
)

merged = merged[merged["release_year"] == merged["title_year"]].copy()
merged["duration_min"] = merged["duration_netflix"].astype(str).str.extract(r"(\d+)").astype(float)
merged["primary_genre"] = merged["listed_in"].astype(str).str.split(",").str[0].str.strip()
merged["imdb_score"] = pd.to_numeric(merged["imdb_score"], errors="coerce")
merged["num_voted_users"] = pd.to_numeric(merged["num_voted_users"], errors="coerce")
merged["release_year"] = pd.to_numeric(merged["release_year"], errors="coerce")

clean = merged[
    ["title", "release_year", "duration_min", "primary_genre", "imdb_score", "num_voted_users"]
].dropna().copy()

clean.to_csv(os.path.join(BASE_DIR, "merged_cleaned_movies.csv"), index=False)
clean[["release_year", "duration_min", "imdb_score", "num_voted_users"]].describe().round(2).to_csv(
    os.path.join(BASE_DIR, "summary_statistics.csv")
)

genre_summary = clean.groupby("primary_genre")["imdb_score"].agg(["mean", "count"]).sort_values("mean", ascending=False).round(3)
genre_summary.to_csv(os.path.join(BASE_DIR, "genre_rating_summary.csv"))

corr_votes, p_votes = pearsonr(clean["num_voted_users"], clean["imdb_score"])

genre_counts = clean["primary_genre"].value_counts()
top_genres = genre_counts[genre_counts >= 20].index.tolist()
anova_groups = [clean.loc[clean["primary_genre"] == g, "imdb_score"] for g in top_genres]
anova_stat, anova_p = f_oneway(*anova_groups)

old_movies = clean.loc[clean["release_year"] < 2000, "imdb_score"]
new_movies = clean.loc[clean["release_year"] >= 2000, "imdb_score"]
ttest_stat, ttest_p = ttest_ind(old_movies, new_movies, equal_var=False)

with open(os.path.join(BASE_DIR, "hypothesis_test_results.txt"), "w", encoding="utf-8") as f:
    f.write(f"""H1 Pearson correlation: {corr_votes:.3f}, p-value: {p_votes:.6g}
H2 ANOVA: F = {anova_stat:.3f}, p-value = {anova_p:.6g}
H3 Welch t-test: t = {ttest_stat:.3f}, p-value = {ttest_p:.6g}
Mean old movies: {old_movies.mean():.3f}
Mean new movies: {new_movies.mean():.3f}
""")

plt.figure(figsize=(8, 5))
plt.hist(clean["imdb_score"], bins=20)
plt.xlabel("IMDb Score")
plt.ylabel("Frequency")
plt.title("Distribution of IMDb Scores")
plt.tight_layout()
plt.savefig(os.path.join(PLOTS_DIR, "imdb_score_distribution.png"))
plt.close()

genre_plot = genre_summary[genre_summary["count"] >= 20].sort_values("mean", ascending=False)
plt.figure(figsize=(10, 6))
plt.bar(genre_plot.index, genre_plot["mean"])
plt.xticks(rotation=45, ha="right")
plt.xlabel("Genre")
plt.ylabel("Average IMDb Score")
plt.title("Average IMDb Score by Genre")
plt.tight_layout()
plt.savefig(os.path.join(PLOTS_DIR, "average_score_by_genre.png"))
plt.close()

plt.figure(figsize=(8, 5))
plt.scatter(clean["num_voted_users"], clean["imdb_score"], alpha=0.6)
plt.xlabel("Number of Voted Users")
plt.ylabel("IMDb Score")
plt.title("Vote Count vs IMDb Score")
plt.tight_layout()
plt.savefig(os.path.join(PLOTS_DIR, "votes_vs_score.png"))
plt.close()

year_avg = clean.groupby("release_year")["imdb_score"].mean().reset_index()
plt.figure(figsize=(10, 5))
plt.plot(year_avg["release_year"], year_avg["imdb_score"])
plt.xlabel("Release Year")
plt.ylabel("Average IMDb Score")
plt.title("Average IMDb Score by Release Year")
plt.tight_layout()
plt.savefig(os.path.join(PLOTS_DIR, "score_by_release_year.png"))
plt.close()

plt.figure(figsize=(8, 5))
plt.scatter(clean["duration_min"], clean["imdb_score"], alpha=0.6)
plt.xlabel("Duration (minutes)")
plt.ylabel("IMDb Score")
plt.title("Duration vs IMDb Score")
plt.tight_layout()
plt.savefig(os.path.join(PLOTS_DIR, "duration_vs_score.png"))
plt.close()

print("Analysis completed successfully.")
print(f"Final dataset size: {len(clean)}")