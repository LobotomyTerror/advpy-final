from typing import Any
from flask import Flask, render_template, request, redirect, url_for

# add request and redirect to flas
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
    return render_template('search_results.html', query=search_query)


if __name__ == "__main__":
    app.run(debug=True)
