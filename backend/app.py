from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import os

app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
movies = pd.read_csv(os.path.join(BASE_DIR, "../data/movies.csv"))

@app.route("/")
def home():
    return "Movie Recommendation API is running"

@app.route("/recommend", methods=["GET"])
def recommend():
    movie_name = request.args.get("movie")

    if not movie_name:
        return jsonify({"error": "Please provide a movie name"}), 400

    selected = movies[movies["title"].str.contains(movie_name, case=False, na=False)]

    if selected.empty:
        return jsonify({"error": "Movie not found"}), 404

    selected_genres = set(selected.iloc[0]["genres"].split("|"))

    def score(genres):
        return len(set(genres.split("|")) & selected_genres)

    movies["score"] = movies["genres"].apply(score)

    result = (
        movies[movies["title"] != selected.iloc[0]["title"]]
        .sort_values(by="score", ascending=False)
        .head(5)
        [["movieId", "title", "genres"]]
        .to_dict(orient="records")
    )

    return jsonify({"recommendations": result})

if __name__ == "__main__":
    app.run(debug=True)