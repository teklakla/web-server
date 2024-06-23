from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(999), unique=True, nullable=False)
    image = db.Column(db.String(999), nullable=True)
    genre = db.Column(db.String(999), nullable=True)
    desc = db.Column(db.String(500000), unique=False, index=True)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(999), unique=True, nullable=False)
    image = db.Column(db.String(999), nullable=True)
    desc = db.Column(db.String(500000), nullable=True)