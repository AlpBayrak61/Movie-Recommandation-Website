
# Movie Recommendation System

## Description
This is a Flask-based web application that provides movie recommendations based on user input. It uses content-based filtering to recommend movies similar to the one selected by the user. The application retrieves movie posters dynamically from the TMDb API and displays them on the website.

## Features
- Search for movies using a search bar.
- Display a list of movies with posters on the homepage.
- Clickable movie posters to view recommendations for similar movies.
- Dynamically fetch movie posters using the TMDb API.

## Technologies Used
- **Backend Framework**: Flask
- **Frontend**: HTML, CSS (with Jinja2 templating)
- **Database**: CSV file (`movie_dataset.csv`)
- **Machine Learning**: scikit-learn (content-based filtering using cosine similarity)
- **API Integration**: TMDb API for fetching movie posters

## Requirements
- Python 3.8 or higher
- Dependencies listed in `requirements.txt`

## Installation
1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-repo/movie-recommendation-app.git
   cd movie-recommendation-app
   ```

2. **Create a virtual environment** (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the TMDb API**:
   - Sign up at [TMDb](https://www.themoviedb.org/) and get an API key.
   - Replace the placeholder API key in `app.py` with your TMDb API key:
     ```python
     TMDB_API_KEY = "your_tmdb_api_key"
     ```

5. **Run the application**:
   ```bash
   python app.py
   ```
   The application will be available at `http://127.0.0.1:5000/`.

## Deployment
To deploy the app on platforms like **Render**, **Heroku**, or **Vercel**:
1. Ensure you have a `requirements.txt` file and, optionally, a `runtime.txt` file specifying the Python version.
2. Follow the platform-specific deployment instructions.

For example, to deploy on Render:
- Add a `runtime.txt` file with your desired Python version:
  ```
  python-3.11.11
  ```
- Push the code to a GitHub repository and link it to Render.

## File Structure
```
project/
├── app.py                # Main Flask application
├── movie_dataset.csv      # Movie dataset used for recommendations
├── requirements.txt       # Python dependencies
├── runtime.txt            # Python version for deployment
├── static/                # Static files (CSS)
│   ├── style.css
├── templates/             # HTML templates
│   ├── main.html          # Homepage
│   ├── recommendations.html  # Recommendation page
```

## Usage
1. **Homepage**:
   - Displays the first 50 movies from the dataset.
   - Use the search bar to find a specific movie.

2. **Recommendations**:
   - Click on a movie poster to see recommendations for similar movies.

## Contributing
Contributions are welcome! Feel free to submit a pull request or open an issue for any bugs or feature requests.

## License
This project is licensed under the MIT License.

## Acknowledgements
- **Flask** for making web development simple and intuitive.
- **TMDb** for providing movie posters and metadata.
- **scikit-learn** for powering the recommendation algorithm.

---
