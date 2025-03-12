import os
from flask import Flask, session, render_template, redirect, request
from flask_session import Session
from dotenv import load_dotenv

# Import models
from models import User

# Import db from extensions
from extensions import db

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)

# Use environment variables
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")

# Configurate SQLAchemy database
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("SQLALCHEMY_DATABASE_URI")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# initialize the database
db.init_app(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Check the data from form
        username = request.form.get('username')
        password = request.form.get('password')

        # # Ensure username was submitted
        # if not request.form.get("username"):
        #     return apology("must provide username", 403)

        # # Ensure password was submitted
        # elif not request.form.get("password"):
        #     return apology("must provide password", 403)

        # Query database for username
        user = User.query.filter_by(username=username).first()

        print(user, user.check_password(password))

        # Remember which user has logged in
        # session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


if __name__ == '__main__':
    app.run(debug=True)

