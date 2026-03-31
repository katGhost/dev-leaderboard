from flask import Blueprint, render_template, session, redirect, url_for

app_bp = Blueprint('app', __name__)


@app_bp.route("/")
def home():
    return render_template("index.html")


@app_bp.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("home"))

    user = session["user"]
    return render_template("dashboard.html", user=user)


@app_bp.route("/leaderboard")
def leaderboard():
    return render_template("leaderboard.html")


# TODO: Add Auth0 login/logout routes here