import pandas as pd
import pickle
from sklearn.metrics.pairwise import cosine_similarity
import os

print("Loading datasets...")
movies = pd.read_csv("../data/movies.csv")
ratings = pd.read_csv("../data/ratings.csv")

print("Merging data...")
merged = ratings.merge(movies, on="movieId")

print("Creating pivot table...")
pivot = merged.pivot_table(index="userId", columns="title", values="rating").fillna(0)

print("Computing similarity...")
similarity = cosine_similarity(pivot.T)
similarity_df = pd.DataFrame(similarity, index=pivot.columns, columns=pivot.columns)

print("Saving model...")
os.makedirs("model", exist_ok=True)

pickle.dump(list(pivot.columns), open("model/movie_list.pkl", "wb"))
pickle.dump(similarity_df, open("model/similarity.pkl", "wb"))

print("MODEL TRAINING COMPLETE!")
