""" This file handles that actual deployment and rendering
of the app itself. Where any search (POST) and clearing (GET)
operations are handled and used to display the web app files
(HTML/CSS).

    Returns:
        _type_: Any
    """

from typing import Any
from flask import Flask, render_template, request, redirect, url_for
from . import main

app = Flask(__name__)


@app.route('/')
def index() -> Any:
    """This is the starting function for the application.
    When the app is deployed it locates the templates file
    in the root directory and then displays the 'index.html'
    file that is located in the templates directory.

    Returns:
        Any: Render template just renders the HTML file
        that is being returned (displays it on the screen)
    """
    return render_template('index.html')


@app.route('/redirect_search', methods=['POST'])
def redirect_search() -> Any:
    search_criteria = request.form['search_type']
    if search_criteria == 'discover_movies_by_genre':
        return render_template('movie_search.html')
    if search_criteria == 'discover_tv_by_genre':
        return render_template('tv_search.html')


@app.route('/search', methods=['GET', 'POST'])
def search() -> Any:
    """ This function waits for a POST to happen. When the
    'index.html' file is rendered there is a search bar that
    allows for stuff to be entered, once something is entered
    the return acts as a submit in-turn a POST. When a query is
    entered into the search bar the POST value (genre) is stored
    into the request object and if it is a POST then we set the
    search_query equal to the the value of the request.form dict at
    the given value. So search_query would be the (genre) string,
    where we then redirect the app to the 'search_results' function
    that renders the 'search_results.html' file.

    Returns:
        Any: Either a redirect to the search results function if
        condition is true. Else we redirect to the index function
    """
    if request.method == 'POST':
        search_query = request.form['searchInput']
        type_query = request.form['search_type']
        return redirect(
            url_for('search_results',
                    query=search_query,
                    search_param=type_query))
    return redirect(url_for('index'))


@app.route('/search_results')
def search_results() -> Any:
    """ When we reach this point the search_query then
    gets the query result from request object or an empty
    string if it doesn't match (this is passed this originally
    from the previous function above where query=search_query).
    Once this happens then it runs through the main module, which
    in-turn access the mongodb database and gets all the JSON data.
    Then it renders the template for the search_results.html webpage
    along with the query (genre string) and the movie data (JSON file)
    where Jinja2 is implemented to display the data (don't worry about
    this part).

    Returns:
        Any: If condition is true then we render the search_results.
        html page. Otherwise we return to the index page.
    """

    search_query = request.args.get('query', '')
    type_of_search = request.args.get('search_param', '')

    if type_of_search == 'movie_search':
        movie_ids = main.search_by_genre(search_query, type_of_search)
        if movie_ids != 0:
            movie_data = main.return_movie_data(movie_ids)

            return render_template(
                'search_results.html',
                query=search_query,
                results=movie_data
                )
    if type_of_search == 'tv_search':
        tv_ids = main.search_by_genre(search_query, type_of_search)
        if tv_ids != 0:
            tv_data = main.return_movie_data(tv_ids)

            return render_template(
                'search_results.html',
                query=search_query,
                results=tv_data
            )
    return redirect(url_for('index'))


@app.route('/clear_db', methods=['POST'])
def clear_db() -> Any:
    """ This fucntion just allows for the clearing of the mongodb
    database when the button on the search_results.html page is
    pressed. This particular function decleration can only be
    accessed if a POST has been made thus clearing the database
    in mongodb of all the data and return the user to the index
    page.

    Returns:
        Any: Redirect to the index function
    """
    main.remove_from_db()
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)
