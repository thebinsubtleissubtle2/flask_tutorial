#!/usr/bin python3
#!/usr/bin/env python3

from flask import Flask, request, make_response, redirect, abort
app = Flask(__name__)

@app.route("/")
def index():
    # getting user agent
    # user_agent = request.headers.get("User-Agent")
    # return "<p>Your browser is {}.".format(user_agent)
    
    # returning requests
    # return "<h1>Bad Request</h1>", 400

    # make_response
    # response = make_response("<h1>This document carries a cookie!</h1>")
    # response.set_cookie("answer", "42")
    # return response

    # redirect
    return redirect("http://www.example.com")

@app.route("/user/<id>")
def get_user(id):
    user = load_user(id)
    if not user:
        abort(404)
    return "<h1>Hello, {}</h1>".format(user.name)

@app.route("/user/<name>")
def user(name):
    return "<h1>Hello, {}</h1>".format(name)


app.add_url_rule("/", "index", index)

if __name__ == "__main__":

    app.run(host = "localhost", port = 5000, debug = True)