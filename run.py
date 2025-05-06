import os
from datetime import datetime
from flask import Flask, session, render_template, redirect, request, url_for

# Session
from flask_session import Session

# DB Migrations
from flask_migrate import Migrate

# ENV
from dotenv import load_dotenv

# For DB errors
from sqlalchemy.exc import IntegrityError

# Import db from extensions
from extensions import db

# Import models
from models import User, Task, Project
from enums import TaskStatus

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


@app.route("/")
def index():
    if session.get("username"):

        # Query database for user's information
        user = User.query.filter_by(username=session.get("username")).first()

        if user is None:

            # If the user is not found, clear the session and redirect to login
            session.clear()
            return redirect(url_for("login"))

        tasks = Task.query.filter_by(user_id=user.id).all()
        projects = Project.query.filter_by(user_id=user.id).all()

        print("Logged in user session:", dict(session))
        return render_template("index.html", tasks=tasks, projects=projects)
    else:   
        return render_template("index.html")


# User
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
        session["user_id"] = user.id

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
            return render_template("change_password.html", apology="must provide old password")

        # Ensure old password is correct
        elif not user.check_password(old_password):
            return render_template("change_password.html", apology="invalid old password")

        # Ensure mew password was submitted
        elif not new_password:
            return render_template("change_password.html", apology="must provide new password")

        # Ensure confirmation was submitted
        elif not confirmation:
            return render_template("change_password.html", apology="must provide confirmation of new password")

        # Ensure new password and confirmation match
        elif new_password != confirmation:
            return render_template("change_password.html", apology="new password and new password confirmation don't match")


        # Change password and commit the update
        try:
            user.set_password(new_password)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return render_template("change_password.html", apology="DB error: " + str(e))
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


# Tasks
@app.route("/create_task", methods=["GET", "POST"])
def create_task():
    user = User.query.get(session.get("user_id"))
    if not user:
        return redirect("/login")
    
    # user = User.query.filter_by(username=session.get("username")).first()
    projects = Project.query.filter_by(user_id=user.id).all()

    if request.method == "POST":
        # Data from form
        title = request.form.get("title")
        description = request.form.get("description")
        due_date = request.form.get("due_date")
        priority = request.form.get("priority")
        status = request.form.get("status")
        project_id = request.form.get("project_id")   

        user_id = user.id

        due_date = datetime.strptime(due_date, "%Y-%m-%d").date() if due_date else None

        # Prepare data and write to DB
        new_task = Task(title=title, 
                        description=description, 
                        user_id=user_id, 
                        due_date=due_date, 
                        priority=priority, 
                        status=TaskStatus.TODO.value,
                        project_id=project_id
                        )

        try:
            db.session.add(new_task)
            db.session.commit()
        except Exception as e:
            return render_template("create_task.html", apology=f'DB Error: {str(e)}')
        else:
            return redirect("/") 
    return render_template("create_task.html", projects=projects)


@app.route("/edit_task/<int:task_id>", methods=["GET", "POST"])
def edit_task(task_id):
    user = User.query.get(session.get("user_id"))
    projects = Project.query.filter_by(user_id=user.id).all()
    if not user:
        return redirect("/login")
    
    task = Task.query.get(task_id)

    return render_template("task/edit_task.html", task=task, projects= projects)

    

# Projects
@app.route("/create_project", methods=["GET", "POST"])
def create_project():
    user = User.query.get(session.get("user_id"))
    if not user:
        return redirect("/login")

    user = User.query.filter_by(username=session.get("username")).first()

    if request.method=="POST":

        # Data from form
        name = request.form.get("name")
        description = request.form.get("description")

        user_id = user.id

        # Prepare data and write to DB
        new_project = Project(name=name, description=description, user_id=user_id)

        try:
            db.session.add(new_project)
            db.session.commit()
        except Exception as e:
            return render_template("create_project.html", apology=f'DB Error: {str(e)}')
        else:
            return redirect("/") 

    return render_template("create_project.html")



if __name__ == '__main__':
    app.run(debug=True)

