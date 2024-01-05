from app import db,app


class User(db.Model): #creating representation for database
    __tablename__= "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80),nullable=False)
    firstname=db.Column(db.String,nullable=False)
    lastname=db.Column(db.String,nullable=True)
    
class Notes(db.Model):
    __tablename__ = "notes"

    nid = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String,nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
with app.app_context(): #creating the database without any value
    db.create_all()
    sample_users = [
        {"username": "user1","firstname":"user1first","lastname":"user1last"},
        {"username": "user1","firstname":"user2first"},
    ]

    sample_notes = [
        {"subject": "Note 1","user_id":1},
        {"subject": "Note 2","user_id":1},
    ]
    # breakpoint()
    # Seed the User table if it's empty
    #if not User.query.first():
    for user_data in sample_users:
        user = User(**user_data)
        db.session.add(user)
        #db.session.commit()

    # Seed the Notes table if it's empty
    #if not Notes.query.first():
    for note_data in sample_notes:
        note = Notes(**note_data)
        db.session.add(note)
        # Commit the changes to the database
    db.session.commit()
