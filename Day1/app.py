from flask import Flask, make_response, request

app = Flask(__name__)

@app.route('/')
def home():
    print(request.headers)

    response_body = f'''
        <h1>Home Page</h1>
        <p>This is a simple Flask app</p>
    '''
    status_code = 200
    headers = {'Content-Language': 'ru'}

    return make_response(response_body, status_code, headers)

















@app.route('/about')
def about():
    return '<h1>About Page</h1>'

@app.route('/profile/<username>')
def profile(username):
    return f'<h1> Profile Page for {username}</h1>'


if __name__ == '__main__':
    app.run(port=8080, debug=True)
