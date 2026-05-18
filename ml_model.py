
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

# Load dataset
df = pd.read_csv("untitled folder/merged_cleaned_movies.csv")

# Convert categorical variable into numerical dummy variables
df = pd.get_dummies(df, columns=["primary_genre"], drop_first=True)

# Define target variable
y = df["imdb_score"]

# Define features
X = df.drop(columns=["imdb_score", "title"])

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Define multiple ML models
models = {
    "Linear Regression": Pipeline([
        ("scaler", StandardScaler()),
        ("model", LinearRegression())
    ]),
    "Ridge Regression": Pipeline([
        ("scaler", StandardScaler()),
        ("model", Ridge(alpha=1.0))
    ]),
    "Random Forest": RandomForestRegressor(
        n_estimators=200,
        random_state=42
    ),
    "Gradient Boosting": GradientBoostingRegressor(
        random_state=42
    )
}

# Train and evaluate each model
results = []

for name, model in models.items():
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)

    mse = mean_squared_error(y_test, predictions)
    rmse = mse ** 0.5
    mae = mean_absolute_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)

    results.append({
        "Model": name,
        "RMSE": rmse,
        "MAE": mae,
        "R2": r2
    })

# Save model comparison results
results_df = pd.DataFrame(results)
results_df.to_csv("ml_model_comparison.csv", index=False)

print("Machine Learning Model Comparison")
print(results_df)

# Plot model comparison using RMSE
plt.figure(figsize=(8, 5))
plt.bar(results_df["Model"], results_df["RMSE"])
plt.xlabel("Model")
plt.ylabel("RMSE")
plt.title("Model Comparison by RMSE")
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig("plots/ml_model_comparison_rmse.png")
plt.close()

# Plot model comparison using R2
plt.figure(figsize=(8, 5))
plt.bar(results_df["Model"], results_df["R2"])
plt.xlabel("Model")
plt.ylabel("R2 Score")
plt.title("Model Comparison by R2 Score")
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig("plots/ml_model_comparison_r2.png")
plt.close()

# Actual vs predicted plot for the best model
best_model_name = results_df.sort_values("RMSE").iloc[0]["Model"]
best_model = models[best_model_name]
best_predictions = best_model.predict(X_test)

plt.figure(figsize=(8, 5))
plt.scatter(y_test, best_predictions)
plt.xlabel("Actual IMDb Score")
plt.ylabel("Predicted IMDb Score")
plt.title(f"Actual vs Predicted IMDb Scores ({best_model_name})")
plt.tight_layout()
plt.savefig("plots/ml_actual_vs_predicted_best_model.png")
plt.close()

# Feature importance for Random Forest
rf_model = models["Random Forest"]
rf_importances = pd.DataFrame({
    "Feature": X.columns,
    "Importance": rf_model.feature_importances_
}).sort_values("Importance", ascending=False)

rf_importances.to_csv("ml_feature_importance.csv", index=False)

top_features = rf_importances.head(10)

plt.figure(figsize=(10, 6))
plt.barh(top_features["Feature"], top_features["Importance"])
plt.xlabel("Importance")
plt.ylabel("Feature")
plt.title("Top 10 Feature Importances - Random Forest")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig("plots/ml_feature_importance.png")
plt.close()

print("\nBest model based on RMSE:", best_model_name)
print("\nTop 10 important features:")
print(top_features)