from flask import Flask, request, render_template
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import requests

TMDB_API_KEY = "87ed44f4aeb6dcdd22c7604ec0e80edd"
app = Flask(__name__)

# Load movie dataset
df = pd.read_csv("movie_dataset.csv")

# Select features
features = ['keywords', 'cast', 'genres', 'director']

for feature in features:
    df[feature] = df[feature].fillna('')

def combine_features(row):
    return row['keywords'] + " " + row['cast'] + " " + row["genres"] + " " + row["director"]

df["combined_features"] = df.apply(combine_features, axis=1)

cv = CountVectorizer()
count_matrix = cv.fit_transform(df["combined_features"])
cosine_sim = cosine_similarity(count_matrix)

def get_title_from_index(index):
    return df[df.index == index]["title"].values[0]

def get_index_from_title(title):
    return df[df.title == title]["index"].values[0]


def get_movie_poster(title):
    """
    Fetch the movie poster URL from TMDb API based on the movie title.
    """
    try:
        url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={title}"
        response = requests.get(url)
        data = response.json()
        if data["results"]:
            poster_path = data["results"][0]["poster_path"]
            return f"https://image.tmdb.org/t/p/w500{poster_path}" 
        else:
            return "https://via.placeholder.com/500x750?text=No+Image"  # Placeholder for missing posters
    except Exception as e:
        print(f"Error fetching poster for {title}: {e}")
        return "https://via.placeholder.com/500x750?text=No+Image"
    
@app.route('/', methods=['GET', 'POST'])
def home():
    search_query = request.form.get('search', '')  
    if search_query:
        movies = df[df['title'].str.contains(search_query, case=False, na=False)][['title']].head(50).copy()
    else:
        movies = df.head(50)[['title']].copy()

    movies['poster_url'] = movies['title'].apply(get_movie_poster)  # Fetch posters
    return render_template('main.html', movies=movies.to_dict(orient='records'), search_query=search_query)


@app.route('/recommend/<movie_name>')
def recommend_movie(movie_name):
    try:
        movie_index = get_index_from_title(movie_name)
        similar_movies = list(enumerate(cosine_sim[movie_index]))
        sorted_similar_movies = sorted(similar_movies, key=lambda x: x[1], reverse=True)

        recommendations = []
        for element in sorted_similar_movies[1:11]:  
            index = element[0]
            movie_title = get_title_from_index(index)
            movie_details = {
                "title": movie_title,
                "keywords": df.iloc[index]["keywords"],
                "cast": df.iloc[index]["cast"],
                "genres": df.iloc[index]["genres"],
                "director": df.iloc[index]["director"],
                "vote_average": df.iloc[index]["vote_average"],
                "vote_count": df.iloc[index]["vote_count"],
                "poster_url": get_movie_poster(movie_title)
            }
            recommendations.append(movie_details)

        return render_template('recommendations.html', recommendations=recommendations, movie_name=movie_name)
    except Exception as e:
        return render_template('recommendations.html', error=f"Movie not found or error: {e}.")
    
@app.route('/recommend', methods=['POST'])
def recommend():
    movie_user_likes = request.form['movie_name']
    try:
        movie_index = get_index_from_title(movie_user_likes)
        similar_movies = list(enumerate(cosine_sim[movie_index]))
        sorted_similar_movies = sorted(similar_movies, key=lambda x: x[1], reverse=True)

        recommendations = []
        for element in sorted_similar_movies[1:11]:  
            index = element[0]
            movie_title = get_title_from_index(index)
            movie_details = {
                "title": movie_title,
                "keywords": df.iloc[index]["keywords"],
                "cast": df.iloc[index]["cast"],
                "genres": df.iloc[index]["genres"],
                "director": df.iloc[index]["director"],
                "vote_average": df.iloc[index]["vote_average"],
                "vote_count": df.iloc[index]["vote_count"],
                "poster_url": get_movie_poster(movie_title)
            }
            recommendations.append(movie_details)

        return render_template('index.html', recommendations=recommendations, movie_name=movie_user_likes)
    except Exception as e:
        return render_template('index.html', error=f"Movie not found or error: {e}. Please try another.")



if __name__ == "__main__":
    app.run(debug=True)
