from flask import Flask, render_template
from flask_jwt_extended import JWTManager, jwt_required  # Assuming you're using Flask-JWT-Extended

app = Flask(__name__)

app.config['SECRET_KEY'] = '123'
app.config['JWT_SECRET_KEY'] = '456'  # Replace with your JWT secret key

jwt = JWTManager(app)  # Initialize the JWTManager

app = Flask(__name__)

@app.route('/')

def hello_world():
    return render_template('service2.html')

if __name__ == '__main__':
    app.run(debug=True,port=8000)
