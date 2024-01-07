from flask import Flask, render_template, request
import pickle
import pandas as pd
app = Flask(__name__)

# Load the saved similarity matrix
with open('similarity.pkl', 'rb') as model_file:
    similarity_matrix = pickle.load(model_file)

# Load the DataFrame with movie titles and tags
new_df = pd.read_csv('newdata.csv')  # Update with the actual path to your DataFrame


@app.route('/')
def home():
    # Pass the list of movies to the template
    movie_list = new_df['title'].tolist()
    return render_template('index.html', movie_list=movie_list)


@app.route('/recommend', methods=['POST'])
def recommend():
    if request.method == 'POST':
        movie_name = request.form['movie_name']
        recommendations = get_recommendations(movie_name)
        return render_template('result.html', movie_name=movie_name, recommendations=recommendations)


def get_recommendations(movie):
    movie_index = new_df[new_df['title'] == movie].index[0]
    distances = similarity_matrix[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = [new_df.iloc[i[0]]['title'] for i in movies_list]
    return recommended_movies


if __name__ == '__main__':
    app.run(debug=True)
