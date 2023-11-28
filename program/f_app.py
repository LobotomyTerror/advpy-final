from typing import Any
from flask import Flask, render_template, request, redirect, url_for
from . import main

app = Flask(__name__)


@app.route('/')
def index() -> Any:
    return render_template('index.html')


@app.route('/search', methods=['GET', 'POST'])
def search() -> Any:
    if request.method == 'POST':
        search_query = request.form['searchInput']
        return redirect(url_for('search_results', query=search_query))
    return redirect(url_for('index'))


@app.route('/search_results')
def search_results() -> Any:
    search_query = request.args.get('query', '')
    movie_ids = main.get_movies_by_genre(search_query)
    movie_data = main.return_movie_data(movie_ids)

    return render_template(
        'search_results.html',
        query=search_query,
        results=movie_data
        )


@app.route('/clear_db', methods=['POST'])
def clear_db() -> Any:
    main.remove_from_db()
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)
