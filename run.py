import os
from flask import Flask, session, render_template, redirect, request
from flask_session import Session
from flask_migrate import Migrate
from dotenv import load_dotenv
from sqlalchemy.exc import IntegrityError

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
app.config['SQLALCHEMY_ECHO'] = True

# initialize the database
db.init_app(app)

# Initialize Flask-Migrate (this is critical)
migrate = Migrate(app, db)

# Import models
from models import User



@app.route("/")
def index():

    print("Logged in user session:", dict(session))
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

        print("Login POST received for user:", username)  # Debug log

        # Ensure username was submitted
        if not username:
            return render_template("login.html", apology="Please, write an username")

        # Ensure password was submitted
        elif not password:
            return render_template("login.html", apology="Please, write a password")

        # Query database for username
        user = User.query.filter_by(username=username).first()

        # Ensure username exists and password is correct
        if not user:
            return render_template("login.html", apology="Wrong username")
        elif not user.check_password(password):
            return render_template("login.html", apology="Wrong password")


        # Remember which user has logged in
        session["username"] = user.username

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        print("Index route called", session)
        return render_template("login.html")
    

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")   


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # Forget any user_id
    session.clear()

    if request.method == "POST":

        # Validate submission
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Ensure username was submitted
        if not username:
            return render_template("register.html", apology="Please, write an username")

        # Ensure password was submitted
        if not password or not confirmation:
            return render_template("register.html", apology="Please, write a password")
        
        # Validate submission
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return render_template("register.html", apology="Username already taken")
        if password != confirmation:
            return render_template("register.html", apology="Passwords do not match")
        
        # Remember user
        else:
            try:
                new_user = User(username=username)
                new_user.set_password(password)
                db.session.add(new_user)
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
                return render_template("register.html", apology="DB error")
            else:
                return redirect("/login")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/change_password", methods=["GET", "POST"])
def change_password():

    # If method POST
    if request.method == "POST":

        # If user is not log in
        if not session.get("username"):
            username = request.form.get("username")

            # Ensure username was submitted
            if not username:
                return render_template("change_password.html",  apology="Please, write an username")

            # Query database for user's information
            user = User.query.filter_by(username=username).first()

            # Ensure username exists
            if not user:
                return render_template("change_password.html",  apology="Please, write a correct username")
        
        else:
            user = User.query.filter_by(username=session["username"]).first()

            # Ensure username exists
            if not user:
                return render_template("change_password.html",  apology="Invalid user")

        old_password = request.form.get("old_password")
        new_password = request.form.get("new_password")
        confirmation = request.form.get("confirmation")

        # Ensure old password was submitted
        if not old_password:
            return render_template("change_password.html",  apology="must provide old password")

        # Ensure old password is correct
        elif not user.check_password(old_password):
            return render_template("change_password.html",  apology="invalid old password")

        # Ensure mew password was submitted
        elif not new_password:
            return render_template("change_password.html",  apology="must provide new password")

        # Ensure confirmation was submitted
        elif not confirmation:
            return render_template("change_password.html",  apology="must provide confirmation of new password")

        # Ensure new password and confirmation match
        elif new_password != confirmation:
            return render_template("change_password.html",  apology="new password and new password confirmation don't match")


        # Change password and commit the update
        try:
            user.set_password(new_password)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return render_template("change_password.html",  apology="DB error: " + str(e))
        else:
            # Logout user
            session.clear()
            # Redirect to login page
            return render_template("login.html", success="Password was changed! Please log in with your new password")

    # If method GET and user is logged in
    elif session.get("username"):
        return render_template("change_password.html")

    # If method GET and user is not logged in
    return render_template("change_password.html")


if __name__ == '__main__':
    app.run(debug=True)

