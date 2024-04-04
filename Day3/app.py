from flask import Flask, make_response, request
from flask_migrate import Migrate 

from models import db, Post, User, Comment

# initialize flask
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///igclone.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# initialize 3rd party libraries
migrate = Migrate(app, db)
db.init_app(app)

if __name__ == '__main__':
    app.run(port=8080, debug=True)