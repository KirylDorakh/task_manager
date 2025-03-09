import os
from flask import Flask, session, render_template
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)

# Use environment variables
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/sset")
def set_session():
    session["user"] = "Kiryl"
    return "session data set"

@app.route("/sget")
def get_session():
    user = session.get("user", "No session found")
    return f"{user}"


if __name__ == '__main__':
    app.run(debug=True)