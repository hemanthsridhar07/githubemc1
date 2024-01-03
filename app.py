import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import ForeignKey
from dotenv import load_dotenv,dotenv_values
#from  .model import User,Notes

load_dotenv()
db_uri=os.getenv("DB_PASS")

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://postgres:{db_uri}@localhost/man' #config with the pgadmin database
db=SQLAlchemy(app)
migrate = Migrate(app, db)



class User(db.Model): #creating representation for database
    __tablename__= "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True,nullable=False)
    
class Notes(db.Model):
    __tablename__ = "notes"

    nid = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String, unique=True, nullable=False)
    #  Foreign key to reference the User model
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # # Relationship (for easier access to the User model from a Notes instance)
    #user = db.relationship('User', backref=db.backref('notes', lazy=True))

with app.app_context(): #creating the database without any value
    db.create_all()
    # sample_users = [
    #     {"username": "user1"},
    #     {"username": "user2"},
    # ]

    # sample_notes = [
    #     {"subject": "Note 1"},
    #     {"subject": "Note 2"},
    # ]

    # # Seed the User table if it's empty
    # if not User.query.first():
    #     for user_data in sample_users:
    #         user = User(**user_data)
    #         db.session.add(user)

    # # Seed the Notes table if it's empty
    # if not Notes.query.first():
    #     for note_data in sample_notes:
    #         note = Notes(**note_data)
    #         db.session.add(note)
    # # Commit the changes to the database
    
    
    # db.session.commit()

@app.route('/get_user_and_notes/<int:user_id>', methods=['GET'])
def get_user_and_notes(user_id):
    # Query to join User and Notes tables based on foreign key relationship
    user_and_notes = db.session.query(User, Notes).join(Notes).filter(User.id == user_id).all()


    result = []
    for user, note in user_and_notes:
        breakpoint()
        result.append({
            'user_id': user.id,
            'username': user.username,
            'note_id': note.nid,
            'subject': note.subject
        })

    return jsonify(result)

@app.route('/add-user', methods=["POST"]) #adding new user
def add_user():
    try:
        data = request.get_json() #getting the given json data
        username = data.get("username") #taking the data separately

        #adding the data to specific table
        added_data = User(username=username) 
        db.session.add(added_data)
        db.session.commit()


        return jsonify ({"message":"new user added"})
    except Exception as e:
        return str(e)


@app.route('/get-user',methods=['GET']) #getting all the user
def get_user():
    users=User.query.all() #getting the database
    val=[{'id':user.id,'username':user.username} for user in users] #returning the databse in dic form
    return jsonify(val)


@app.route('/gets-user/<username>',methods=['GET']) #getting single user
def gets_user(username):
    users=User.query.filter_by(username=username).first() #getting the specific row of the given username
    return jsonify({'id':users.id,'username':users.username})
    
    
@app.route('/update-user/<id>',methods=['PUT']) #updating a user
def update_user(id):
    data=request.get_json()
    new_user=data.get("new_username")

    user=User.query.get(id)
    user.username=new_user
    db.session.commit()
    return jsonify({"message":"user updated"})


@app.route('/delete-user/<id>',methods=['DELETE']) #deleting a user
def delete_user(id):
    user=User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message":"user deleted"})





@app.route('/add-notes',methods=['POST'])
def add_notes():
    data=request.get_json()
    subject=data.get("subject")
    user_id=data.get("user_id")

    added_data=Notes(subject=subject,user_id=user_id)
    db.session.add(added_data)
    db.session.commit()
    return jsonify({"message":"subject added"})


@app.route('/get-notes',methods=['GET'])
def get_notes():
    notes=Notes.query.all()
    val=[{"nid":note.nid,"subject":note.subject} for note in notes]
    return jsonify(val)


@app.route('/gets-notes/<nid>',methods=['GET'])
def gets_notes(nid):
    notes=Notes.query.filter_by(nid=nid).first()
    return jsonify({"nid":notes.nid,"subject":notes.subject})


@app.route('/update-notes/<nid>',methods=['PUT'])
def update_notes(nid):
    data=request.get_json()
    new_sub=data.get("new_sub")

    note=Notes.query.get(nid)
    note.subject=new_sub
    db.session.commit()
    return jsonify({"message":"notes updated"})


@app.route('/delete-notes/<nid>',methods=['DELETE'])
def delete_notes(nid):
    note=Notes.query.get(nid)
    db.session.delete(note)
    db.session.commit()
    return jsonify({"message":"notes deleted"})






@app.route('/')
def home():
    return "hello world"

if __name__ == "__main__":
    app.run(debug=True)