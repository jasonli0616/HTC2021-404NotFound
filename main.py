'''
------------------------------

Name tbd

Authors: Jason, Evan, Raghav, Amogh

------------------------------
'''



from flask import Flask, render_template, url_for, request, redirect, session, flash
from flask_sqlalchemy import SQLAlchemy
import hashlib
import os



'''
App config
------------------------------
'''

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# Database config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

'''
------------------------------
'''



def toHash(value:str):
    '''
    Hashes string
    
    Parameters: string to hash
    Return: hashed string
    '''
    hash_obj = hashlib.sha256(bytes(value, 'utf8'))
    return hash_obj.hexdigest()

# Database models

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64))
    email = db.Column(db.String(64))
    password = db.Column(db.String(64))


@app.route('/index.html')
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():

    if ("user" in session):
        return redirect(url_for('home'))

    if request.method == 'POST':
        email = str(request.form["email"])
        password = str(toHash(request.form["password"]))

        if User.query.filter_by(email=email, password=password).first():
            # if username and password correct
            session["user"] = email
            flash('You are logged in!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Incorrect email or password', 'danger')
            return redirect(url_for('login'))
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():

    # if user already logged in redirect to home page
    if ("user" in session):
        return redirect(url_for('home'))


    if request.method == 'POST':
        req = request.form

        success = True

        # if error creating string flash invalid registration
        try:
            username = str(req.get("username"))
            email = str(req.get("email"))
            password = str(req.get("password"))
            confirm_password = str(req.get("confirm-password"))
        except:
            success = False
            flash('Invalid registration. Please try again.', 'danger')

        # if passwords don't match return flash error
        if (password != confirm_password):
            success = False
            flash("Passwords Don't match. Please try again.", 'danger')

        # if type of data isn't string return error
        try:
            if not type(username) == str:
                success = False
                flash('Invalid username.', 'danger')
            if not type(email) == str:
                success = False
                flash('Invalid email.', 'danger') 
            if not type(password) == str or not type(confirm_password) == str:
                success = False
                flash('Invalid password.', 'danger')
        except ValueError:
            success = False
            flash('Invalid registration. Please try again.', 'danger')

        if User.query.filter_by(username=username).first():
            # User already exists code here
            success = False
            flash('Username already exists. Please try with a different username.', 'danger')
        if User.query.filter_by(email=email).first():
            # Email already exists code here
            success = False
            flash('Email already exists. Please try with a different email.', 'danger')

        # if success then flash success message and take to login page
        if success:
            hashPass = toHash(password)

            user = User(username=username, password=hashPass, email=email)
            db.session.add(user)
            db.session.commit()

            flash('Your account has been created.', 'success')
            return redirect(url_for('login'))

    return render_template('register.html')

if __name__ == '__main__':
    db.create_all()

    app.run(debug=True)