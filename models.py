import datetime
from sqlalchemy import Enum as SQLEnum
from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from enums import TaskStatus

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    password_hash = db.Column(db.String(128), nullable=False)

    # Relationships with tasks and projects
    tasks = db.relationship('Task', backref='user', lazy=True)
    projects = db.relationship('Project', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'
    

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now(datetime.timezone.utc))

    # Relationships
    tasks = db.relationship('Task', backref='project', lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<Project {self.name}>'  
    

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    due_date = db.Column(db.Date, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now(datetime.timezone.utc))
    updated_at = db.Column(db.DateTime, 
                           default=datetime.datetime.now(datetime.timezone.utc), 
                           onupdate=datetime.datetime.now(datetime.timezone.utc))
    completed = db.Column(db.Boolean, default=False)
    priority = db.Column(db.Integer, default=3)
    status = db.Column(SQLEnum(TaskStatus, name="task_status_enum"), default=TaskStatus.TODO.value, nullable=False)

    # Relationships
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<Task {self.title}>'
    

