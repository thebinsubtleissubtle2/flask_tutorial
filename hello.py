#!/usr/bin python3
#!/usr/bin/env python3

import os
from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail, Message
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_moment import Moment
from datetime import datetime
from threading import Thread

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)

# configs
app.config["SECRET_KEY"] = "execute-order-66"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "data.sqlite")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD")
app.config["FLASKY_MAIL_SUBJECT_PREFIX"] = "[Flasky]"
app.config["FLASKY_MAIL_SENDER"] = "Flasky Admin <flasky@example.com>"
app.config["FLASKY_ADMIN"] = os.environ.get("FLASKY_ADMIN")

# flask extensions
bootstrap = Bootstrap(app = app)
moment = Moment(app = app)
db = SQLAlchemy(app = app)
migrate = Migrate(app = app, db = db)
mail = Mail(app = app)

# classes
class Role(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), unique = True)
    users = db.relationship("User", backref = "role", lazy = "dynamic")

    def __repr__(self):
        return "<Role %r>" % self.name

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), unique = True, index = True)
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"))

    def __repr__(self):
        return "<User %r>" % self.username

class NameForm(FlaskForm):
    name = StringField(label = "What is your name?", validators = [DataRequired()])
    submit = SubmitField(label = "Submit")

def send_email(to, subject, template, **kwargs):
    msg = Message(subject = app.config["FLASKY_MAIL_SUBJECT_PREFIX"] + subject, sender = app.config["FLASKY_MAIL_SENDER"], recipients = [to])
    msg.body = render_template(template + ".txt", **kwargs)
    msg.html = render_template(template + ".html", **kwargs)
    mail.send(msg)

@app.route("/", methods = ["GET", "POST"])
def index():
    name = None
    form = NameForm()
    if form.validate_on_submit():

        # sessions
        # old_name = session.get("name")
        # if old_name is not None and old_name != form.name.data:
        #     flash("Looks like you have changed your name.", category = "message")
        # session["name"] = form.name.data
        # return redirect(url_for("index"))

        user = User.query.filter_by(username = form.name.data).first()
        if user is None:
            user = User(username = form.name.data)
            db.session.add(user)
            db.session.commit()
            session["known"] = False
            if app.config["FLASKY_ADMIN"]:
                send_email(to = app.config["FLASKY_ADMIN"], subject = "New User", template = "mail/new_user", user = user)
        else:
            session["known"] = True
        session["name"] = form.name.data
        form.name.data = ""
        return redirect(url_for("index"))
    return render_template("index.html", current_time = datetime.utcnow(), form = form, name = session.get("name"), known = session.get("known", False))

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