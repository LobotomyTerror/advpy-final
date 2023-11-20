from typing import Any
from flask import Flask, render_template

# add request and redirect to flas
app = Flask(__name__)


@app.route('/')
def index() -> Any:
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)
