from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# create model
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    author = db.Column(db.String(200))
    genre = db.Column(db.String(200))

    @validates(title)

# Get all the Boooks
@app.route('/', methods=['GET'])
def get_books():
    books = Book.query.all()
    
    arr_books = []
    for book in books:
        book_obj = {
            'id': book.id,
            'title': book.title,
            'author': book.author,
            'genre': book.genre,
        }

        arr_books.append(book_obj)

    return jsonify(arr_books), 200

@app.route('/createbooks', methods=['POST'])
def create_book():
    data = request.json
    new_book = Book(title=data.get('title'), author=data.get('author'), genre=data.get('genre'))
    db.session.add(new_book)
    db.session.commit()

    response_data = {
        'message': 'Book created successfully'
    }
    return jsonify(response_data), 201

@app.route('/book/<id>', methods=['PATCH'])
def update_book(id):
    # get book
    book = Book.query.filter_by(id=id).first()

    if not book:
        return jsonify({'Error': 'Book not found'}, 404)
    
    data = request.json
    book.title = data.get('title', book.title)
    book.author = data.get('author', book.author)
    book.genre = data.get('genre', book.genre)
    db.session.commit()
    return jsonify({'Message': "Book Updated Successfully"}), 200

@app.route('/book/<id>', methods=['DELETE'])
def delete_book(id):
    # get book
    book = Book.query.filter_by(id=id).first()

    if not book:
        return jsonify({'Error': 'Book not found'}, 404)
    
    db.session.delete(book)
    db.session.commit()
    return jsonify({'Message': "Book Deleted Successfully"}), 200


if __name__ == '__main__':
    with app.app_context():
        # create the database table
        db.create_all()
    app.run(port=8080, debug=True)