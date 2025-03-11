import os
from flask import Flask, session, render_template, redirect
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


if __name__ == '__main__':
    app.run(debug=True)