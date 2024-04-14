from sqlite3 import IntegrityError
from flask import Flask, jsonify, request, session, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource, reqparse
from sqlalchemy.orm import validates
from sqlalchemy import CheckConstraint, func
from flask_cors import CORS

# import flask_session and login
from flask_session import Session
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'the_Elites'
app.config['SESSION_TYPE'] = 'filesystem' # store session data in file system
app.config['SESSION_COOKIE_NAME'] = 'book_session' # name of the session cookie


# third Parties
db = SQLAlchemy(app)
api = Api(app)
Session(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
CORS(app, supports_credentials=True, origins='*')

# setup login manager
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#----------------------------------------------------------------
# create model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), db.CheckConstraint("LENGTH(title) <= 20", name="title_length_constraint")) # length of the title max of 20
    author = db.Column(db.String(200)) # should have 2 names
    genre = db.Column(db.String(200)) # should check from a list 

    @validates('genre')
    def validate_genre(self, key, genre):
        valid_genre = ['anime', 'fiction', 'romance', 'poetic', 'historical', 'autobiography', 'mystery']

        if genre.lower() not in valid_genre:
            raise ValueError(f'Genre Not Valid!! - Allowed {valid_genre}')
        return genre


# authenication Routes and functions
@app.route('/login', methods=['POST'])
def login():
    
    username = request.json.get('username')
    password = request.json.get('password')

    # check user exist
    user = User.query.filter_by(username=username).first()

    if user:
        if user.password == password:
            login_user(user)
            
            # Prepare response with user data
            user_data = {
                'id': user.id,
                'username': user.username,
            }
            response = {'message': 'Login Success', 'user': user_data}
            statusCode = 200
            
            return make_response(response, statusCode)

        else:
            response = {'Error': 'Password not correct'}
            statusCode = 401
            return make_response(response, statusCode)
    else:
        return jsonify({'Error': 'User not found'})


@app.route('/register', methods=['POST'])
def register():
    username = request.json.get('username')
    password = request.json.get('password')

    # check user exist
    user = User.query.filter_by(username=username).first()
    if user:
        return jsonify({'Error': 'User already exist'})
    
    # create new user
    new_user = User(username=username, password=password)

    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User Registered Successfully'})


@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logout Success'})



#----------------------------------------------------------------
# Resource
class BookList(Resource):
    @login_required
    def get(self): # getting all books
        books = Book.query.all()
        print(books)
        arr_books = []
        for book in books:
            book_obj = {
                'id': book.id,
                'title': book.title,
                'author': book.author,
                'genre': book.genre,
            }

            arr_books.append(book_obj)

        return jsonify(arr_books)

    # @login_required
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('title', type=str)
            parser.add_argument('author', type=str)
            parser.add_argument('genre', type=str)
            data = parser.parse_args()

            new_book = Book(title=data.get('title'), author=data.get('author'), genre=data.get('genre'))

            db.session.add(new_book)
            db.session.commit()

            response_data = {
                'message': 'Book created successfully'
            }
            return jsonify(response_data)
        except Exception as e:
            return jsonify({'Error': str(e)})

class BookDetail(Resource):
    @login_required
    def get(self, id):
        book = Book.query.filter_by(id=id).first()

        if not book:
            return {'message': 'Book not found'}
        
        response_data = {
            'id': book.id,
            'title': book.title,
            'author': book.author,
            'genre': book.genre,
        }
        return jsonify(response_data)

    @login_required 
    def patch(self, id):
        book = Book.query.filter_by(id=id).first()
        
        if not book:
            return {'message': 'Book not found'}
        
        parser = reqparse.RequestParser()
        parser.add_argument('title', type=str)
        parser.add_argument('author', type=str)
        parser.add_argument('genre', type=str)
        data = parser.parse_args()
        
        if 'title' in data and data['title'] != None:
            book.title = data.get('title', book.title)
        
        if 'author' in data and data['author'] != None:
            book.author = data.get('author', book.author)

        if 'genre' in data and data['genre'] != None:
            book.genre = data.get('genre', book.genre)
       
        db.session.commit()

        return jsonify({'message': 'Book Updated successfully'})

    @login_required
    def delete(self, id):
        book = Book.query.filter_by(id=id).first()
        
        if not book:
            return {'message': 'Book not found'}
        
        db.session.delete(book)
        db.session.commit()

        return jsonify({'message': 'Book Deleted successfully'})

# Routes
api.add_resource(BookList, '/books')
api.add_resource(BookDetail, '/books/<int:id>')






if __name__ == '__main__':
    with app.app_context():
        # create the database table
        db.create_all()
    app.run(port=8080, debug=True)