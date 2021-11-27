from logging import fatal
from sys import meta_path
from flask import Flask, redirect, url_for, render_template, request, session
from datetime import timedelta
from flask.helpers import flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "nokkel"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
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
    shot =0
    if "user" in session:
        user = session["user"]

        if request.method == "POST":

            found_user = users.query.filter_by(name=user).first() 

            session["olSmall"] = olSmall
            session["vin"] = vin
            session["olLarge"] = olLarge
            session["shot"] = shot

            vin = found_user.vin
            olSmall = found_user.olSmall
            olLarge = found_user.olLarge
            shot = found_user.shot

            if request.form.get("vin"):

                if type(found_user.vin) != int:
                    found_user.vin = 1
                else:
                    found_user.vin += 1

            if request.form.get("-vin"):

                if type(found_user.vin) != int:
                    found_user.vin = 1
                elif found_user.vin <= 0:
                    found_user.vin = 0
                else:
                    found_user.vin -= 1

            if request.form.get("olSmall"):

                if type(found_user.olSmall) != int:
                    found_user.olSmall = 1
                else:
                    found_user.olSmall += 1

            if request.form.get("-olSmall"):

                if type(found_user.olSmall) != int:
                    found_user.olSmall = 1
                elif found_user.olSmall <= 0:
                    found_user.olSmall = 0
                else:
                    found_user.olSmall -= 1

            if request.form.get("olLarge"):

                if type(found_user.olLarge) != int:
                    found_user.olLarge = 1
                else:
                    found_user.olLarge += 1
                    
            if request.form.get("-olLarge"):

                if type(found_user.olLarge) != int:
                    found_user.olLarge = 1
                elif found_user.olLarge <= 0:
                    found_user.olLarge = 0
                else:
                    found_user.olLarge -= 1

            if request.form.get("shot"):

                if type(found_user.shot) != int:
                    found_user.shot = 1
                else:
                    found_user.shot += 1

            if request.form.get("-shot"):

                if type(found_user.shot) != int:
                    found_user.shot = 1
                elif found_user.shot <= 0:
                    found_user.shot = 0
                else:
                    found_user.shot -= 1

            db.session.commit()
            
        else:
            if "vin" in session:
                vin = session["vin"]
            if "olSmall" in session:
                olSmall = session["olSmall"]
            
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

@app.route("/piotr")
def piotr():
    return render_template("piotr.html", values=users.query.all())
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
    app.run(debug=True)

