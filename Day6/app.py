from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# third Parties
db = SQLAlchemy(app)
api = Api(app)

# create model
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    author = db.Column(db.String(200))
    genre = db.Column(db.String(200))

# Resource
class BookList(Resource):
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

    def post(self):
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


class BookDetail(Resource):
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