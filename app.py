from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:hemanth.01@localhost/flask_pgdb'
db=SQLAlchemy(app)
migrate = Migrate(app, db)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True,nullable=False)

class Notes(db.Model):
    nid=db.Column(db.Integer,primary_key=True)
    subject=db.Column(db.String,unique=True,nullable=False)




with app.app_context():
    db.create_all()

'''@app.route('/<username>')
def add_user(username):
    new_user = User(username=username)
    db.session.add(new_user)
    db.session.commit()
    return f"User {username} added." '''

@app.route('/')
def home():
    return "hello world"

if __name__ == "__main__":
    app.run(debug=True)