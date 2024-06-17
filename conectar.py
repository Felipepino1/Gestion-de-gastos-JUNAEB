from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson import ObjectId

app = Flask(__name__)
app.config['SECRET_KEY'] = '123456'

url = 'mongodb+srv://maria:maria123456@mlorca.ybae68s.mongodb.net/GDGJ?retryWrites=true&w=majority'

def conexion():
    cliente = MongoClient(url, server_api=ServerApi('1'))
    try:
        cliente.GDGJ.command('ping')
        db = cliente.GDGJ
        print("Conectado a MongoDB")
        return db
    except Exception as e:
        print(e)
        return None 


db = conexion()
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
