from flask import request, jsonify
from app import app,db
from app.model import User,Notes

@app.route('/get_user_and_notes/<int:user_id>', methods=['GET'])
def get_user_and_notes(user_id):
    # Query to join User and Notes tables based on foreign key relationship
    user_and_notes = db.session.query(User, Notes).join(Notes).filter(User.id == user_id).all()


    result = []
    for user, note in user_and_notes:
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
        firstname=data.get("firstname")

        #adding the data to specific table
        added_data = User(username=username,firstname=firstname) 
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