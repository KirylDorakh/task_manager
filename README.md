# Task Manager

A simple task manager application built with Flask.

## About the Project
Task Manager is a lightweight web application for creating, organizing, and tracking tasks across multiple projects. It includes user registration, login, project creation, task categorization, due dates, and status toggling between completed and active. This app was developed as part of the final project for Harvard's CS50 course.

## Features
- User authentication (register, login, logout)
- Create, update, and delete tasks
- Organize tasks by projects
- Set due dates
- Mark tasks as completed or undone (AJAX-based)
- Design with Bootstrap

## Tech Stack
- Python, Flask
- SQLAlchemy, SQLite (by default)
- Flask-Migrate for database migrations
- Jinja2 templating
- JavaScript (AJAX)
- Bootstrap 5
- dotenv for environment variables

## Local Installation
1. Clone the repository:

   git clone https://github.com/KirylDorakh/task_manager.git
   cd task_manager

2. Install dependencies

   pip install -r requirements.txt

3. Create a .env file with the following:

   SECRET_KEY=your_secret_key
   SQLALCHEMY_DATABASE_URI=sqlite:///task_manager.db

4. Set up the database

   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade

5.	Run the app

   flask run
   
