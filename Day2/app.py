from flask import Flask, make_response, current_app, render_template, request
from flask_sqlalchemy import SQLAlchemy

# initialize flask
app = Flask(__name__)

# connect with db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///party.db'
app.config['SECRET_KEY'] = 'theElites'

# initialize Third Party Apps
db = SQLAlchemy(app)

# models / Class
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=True)
    fullname = db.Column(db.String(100), nullable=False)


# Routes and their Functions
@app.route('/')
def index():

    allUsers = User.query.all()

    response_body = '<h1>Welcome To Day2</h1>'
    for user in allUsers:
        response_body += f'<p> {user.username}</p>'

    
    status_code = 200
    headers = {}

    return make_response(response_body, status_code, headers)

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'GET':
        return render_template('register.html')

    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        fullname = request.form.get('fullname')

        new_user = User(username=username, email=email, fullname=fullname)
        db.session.add(new_user)
        db.session.commit()

        return render_template('register.html')





# run the application
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(port=8080, debug=True)

