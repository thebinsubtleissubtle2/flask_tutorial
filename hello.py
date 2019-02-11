#!/usr/bin python3
#!/usr/bin/env python3

from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime

app = Flask(__name__)
bootstrap = Bootstrap(app = app)
moment = Moment(app = app)

@app.route("/")
def index():
    return render_template("index.html", current_time = datetime.utcnow())

@app.route("/user/<user>")
def user(user):
    return render_template("user.html", user = user)

# errors
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html", e = e), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html", e = e), 500


# for development and testing purposes only
if __name__ == "__main__":
    app.run(host = "localhost", port = 5000, debug = True)