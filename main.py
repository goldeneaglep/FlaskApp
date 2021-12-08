from logging import fatal
from sys import meta_path
from flask import Flask, redirect, url_for, render_template, request, session
from datetime import timedelta
from flask.helpers import flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "nokkel"

ipOfDB = '80.213.239.129'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+ipOfDB+'users.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.permanent_session_lifetime = timedelta(days=31)

db = SQLAlchemy(app)

class users(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    olSmall = db.Column(db.Integer)
    vin = db.Column(db.Integer)
    olLarge = db.Column(db.Integer)
    shot = db.Column(db.Integer)

    def __init__(self, name):
        self.name = name

def leggeTil(typeDrikke, antall):
    if type(typeDrikke) != int:
        typeDrikke = antall
    elif antall < 0 and typeDrikke <= 0:
        typeDrikke = 0
    else:
        typeDrikke += antall
    
    return typeDrikke

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        user = request.form["nm"]
        session["user"] = user

        ###function to delete a row from database (enter name of user in login tab to delete)
        """found_user = users.query.filter_by(name=user).delete()
        db.session.commit()"""

        found_user = users.query.filter_by(name=user).first()

        if not found_user:
            usr = users(user)
            db.session.add(usr)
            db.session.commit()

        return redirect(url_for("user"))
    else:
        if "user" in session:
            return redirect(url_for("user"))
            
        return render_template("login.html")

@app.route("/user", methods= ["POST", "GET"])
def user():
    olSmall = 0
    vin = 0
    olLarge = 0
    shot = 0
    if "user" in session:
        user = session["user"]

        found_user = users.query.filter_by(name=user).first() 
        if request.method == "POST":
            """ session["olSmall"] = found_user.olSmall
            session["vin"] = vin
            session["olLarge"] = olLarge
            session["shot"] = shot """

            if request.form.get("vin"):
                found_user.vin = leggeTil(found_user.vin, 1)
            if request.form.get("-vin"):
                found_user.vin = leggeTil(found_user.vin, -1)
            if request.form.get("olSmall"):
                found_user.olSmall = leggeTil(found_user.olSmall, 1)
            if request.form.get("-olSmall"):
                found_user.olSmall = leggeTil(found_user.olSmall, -1)
            if request.form.get("olLarge"):
                found_user.olLarge = leggeTil(found_user.olLarge, 1)
            if request.form.get("-olLarge"):
                found_user.olLarge = leggeTil(found_user.olLarge, -1)
            if request.form.get("shot"):
                found_user.shot = leggeTil(found_user.shot, 1)
            if request.form.get("-shot"):
                found_user.shot = leggeTil(found_user.shot, -1)

            vin = found_user.vin
            olSmall = found_user.olSmall
            olLarge = found_user.olLarge
            shot = found_user.shot

            db.session.commit()
        else:
            if "vin" in session:
                vin = found_user.vin
            if "olSmall" in session:
                olSmall = found_user.olSmall
            if "olLarge" in session:
                olLarge = found_user.olLarge
            if "shot" in session:
                shot = found_user.shot
            
        return render_template("user.html", olSmall=olSmall, vin=vin, usr=user, olLarge=olLarge, shot=shot)
    else:
        return redirect(url_for("login"))

@app.route("/logout")
def logout():
    session.pop("user", None)
    session.pop("olSmall", None)
    session.pop("vin", None)
    session.pop("olLarge", None)
    session.pop("shot", None)
    return redirect(url_for("home"))

@app.route("/stats")
def stats():
    return render_template("stats.html", values=users.query.all())
"""
    @app.route("/jonas")
    def jonas():
        return render_template("jonas.html")

    @app.route("/peter")
    def peter():
        return render_template("peter.html")

    @app.route("/fredrik")
    def fredrik():
        return render_template("fredrik.html")

    @app.route("/kristian")
    def kristian():
    return render_template("kristian.html")
"""

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True,host="0.0.0.0")

