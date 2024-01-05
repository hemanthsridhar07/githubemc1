import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv


load_dotenv()
db_pass=os.getenv("DB_PASS")
db_username=os.getenv("DB_USERNAME")
db_database=os.getenv("DB_DATABASE")


app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_username}:{db_pass}@localhost/{db_database}' #config with the pgadmin database
db=SQLAlchemy(app)
migrate = Migrate(app, db)

from app import route

