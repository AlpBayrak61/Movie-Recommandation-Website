from flask import Flask, request, render_template
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# Load movie dataset
df = pd.read_csv("movie_dataset.csv")

# Select features
features = ['keywords', 'cast', 'genres', 'director']

# Fill NaN values with empty strings and combine features
for feature in features:
    df[feature] = df[feature].fillna('')

def combine_features(row):
    return row['keywords'] + " " + row['cast'] + " " + row["genres"] + " " + row["director"]

df["combined_features"] = df.apply(combine_features, axis=1)

# Create count matrix and cosine similarity matrix
cv = CountVectorizer()
count_matrix = cv.fit_transform(df["combined_features"])
cosine_sim = cosine_similarity(count_matrix)

# Helper functions
def get_title_from_index(index):
    return df[df.index == index]["title"].values[0]

def get_index_from_title(title):
    return df[df.title == title]["index"].values[0]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    movie_user_likes = request.form['movie_name']
    try:
        movie_index = get_index_from_title(movie_user_likes)
        similar_movies = list(enumerate(cosine_sim[movie_index]))
        sorted_similar_movies = sorted(similar_movies, key=lambda x: x[1], reverse=True)

        recommendations = []
        for i, element in enumerate(sorted_similar_movies[1:11]):  # Skip the first (itself)
            recommendations.append(get_title_from_index(element[0]))
        return render_template('index.html', recommendations=recommendations, movie_name=movie_user_likes)
    except:
        return render_template('index.html', error="Movie not found. Please try another.")

if __name__ == "__main__":
    app.run(debug=True)
