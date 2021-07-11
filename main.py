'''
------------------------------

Tutor Center

Authors: Jason, Evan, Raghav, Amogh

------------------------------
'''



from flask import Flask, render_template, url_for, request, redirect, session, flash
from flask_sqlalchemy import SQLAlchemy
import hashlib
import os
import random
import json



'''
App config
------------------------------
'''

app = Flask(__name__)
app.config['SECRET_KEY'] = 'a' # for testing purposes
# app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

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

class Tutor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    email = db.Column(db.String(64))
    phone_number = db.Column(db.String(64))
    pay = db.Column(db.Integer)
    description = db.Column(db.String(10000))
    subject = db.Column(db.String(100))
    grade = db.Column(db.Integer)
    average_stars = db.Column(db.Integer)
    image = db.Column(db.String(500))
    num_stars = db.Column(db.Integer)

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tutor_id = db.Column(db.Integer)
    title = db.Column(db.String(250))
    username = db.Column(db.String(64))
    rating = db.Column(db.Integer)
    content = db.Column(db.String(10000))

imageURLs = [
    'https://images.unsplash.com/photo-1513258496099-48168024aec0?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80',
    'https://images.unsplash.com/photo-1596496050755-c923e73e42e1?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1336&q=80',
    'https://images.unsplash.com/photo-1571260899304-425eee4c7efc?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80',
    'https://images.unsplash.com/photo-1531482615713-2afd69097998?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80',
    'https://images.unsplash.com/photo-1610008885395-d4b47c2f5c8c?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80',
    'https://images.pexels.com/photos/4308095/pexels-photo-4308095.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260',
    'https://images.pexels.com/photos/5538355/pexels-photo-5538355.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260',
    'https://images.unsplash.com/photo-1513258496099-48168024aec0?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1350&q=80',
    'https://images.unsplash.com/photo-1599687351724-dfa3c4ff81b1?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80',
    'https://images.pexels.com/photos/3769981/pexels-photo-3769981.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=750&w=1260',
    'https://images.unsplash.com/photo-1573496799652-408c2ac9fe98?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1050&q=80',
    'https://images.unsplash.com/flagged/photo-1559475555-b26777ed3ab4?ixid=MnwxMjA3fDB8MHxzZWFyY2h8Mjd8fHRlYWNoZXJ8ZW58MHx8MHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=60',
    'https://images.unsplash.com/photo-1551862253-ccddd3b67769?ixid=MnwxMjA3fDB8MHxzZWFyY2h8MTl8fHRlYWNoZXJ8ZW58MHx8MHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=60',
    'https://images.unsplash.com/photo-1597570889212-97f48e632dad?ixid=MnwxMjA3fDB8MHxzZWFyY2h8MjR8fHRlYWNoZXJ8ZW58MHx8MHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=60'
]
subjects = ["All", "Math", "English", "Physics", "French", "Science", "Spanish", "Computer Science"]
grades = ["All", "5", "6", "7", "8", "9", "10", "11", "12"]

def generateRandomTutor():
    '''
    Generates fake tutors and inserts into database
    For demonstration purposes
    '''
    with open('tutornames.json') as f:
        json_file = json.load(f)
        name = json_file[random.randint(0, 4946)]
    title = Tutor(name=name, email=f"{name.lower()}@fake_email.com", phone_number=random.randint(1000000000, 9999999999), pay=random.randint(10000, 99999), description="Hi! I like to tutor people.", subject=subjects[random.randint(1, len(subjects)-1)], grade=grades[random.randint(1, len(grades)-1)], average_stars=random.randint(0, 5), image=imageURLs[random.randint(0, 13)], num_stars=2)
    db.session.add(title)
    db.session.commit()

@app.route('/index.html')
@app.route('/')
def index():

    return render_template('index.html', session=session)

@app.route('/tutors', methods=['GET', 'POST'])
def tutors():

    if not "user" in session:
        return redirect(url_for('index'))

    tutors = []

    subject, grade = "All", "All"
    tutors = Tutor.query.order_by(Tutor.average_stars).all()

    if request.method == 'POST':
        subject = request.form["subject"]
        grade = request.form["grade"]

        if not subject and not grade:
            flash('Please enter a subject and grade.', 'danger')
        elif not subject:
            flash('Please enter a subject.', 'danger')
        elif not grade:
            flash('Please enter a grade.', 'danger')
        else:
            tutors = Tutor.query.filter_by(subject=subject, grade=grade).order_by(Tutor.average_stars).all()

    tutors.reverse()
    return render_template('tutors.html', tutors=tutors, subjects=subjects, grades=grades, grade_selected=grade, subject_selected=subject, session=session)

@app.route('/tutors/<id>', methods=['GET', 'POST'])
def tutorName(id):

    if not "user" in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        title = request.form['title']
        review = request.form['review']
        starsSelected = 0

        if title.strip() == '' or review.strip() == '': flash('Please enter a title and description.', 'danger')

        for i in range(1, 7):
            if f'star-{i}' in request.form: starsSelected = i
        
        user = User.query.filter_by(email=session['user']).first()
        review = Review(tutor_id=id, title=title.strip(), username=user.username, rating=starsSelected, content=review.strip())

        tutor = Tutor.query.filter_by(id=id).first()
        tutor.average_stars = round((tutor.num_stars * tutor.average_stars + starsSelected) / (tutor.num_stars + 1))
        tutor.num_stars += 1

        db.session.add(review)
        db.session.commit()
    

    tutor = Tutor.query.filter_by(id=id).first()
    reviews = Review.query.filter_by(tutor_id=id).all()
    salaryRounded = round(tutor.pay / 12 / 30)
    return render_template('specific_tutor.html', tutor=tutor, reviews=reviews, salaryRounded=salaryRounded, session=session)


@app.route('/login', methods=['GET', 'POST'])
def login():

    if "user" in session:
        return redirect(url_for('index'))

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
    
    return render_template('login.html', session=session)

@app.route('/register', methods=['GET', 'POST'])
def register():

    # if user already logged in redirect to home page
    if ("user" in session):
        return redirect(url_for('index'))


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
        if password != confirm_password:
            success = False
            flash("Passwords Don't match. Please try again.", 'danger')
        
        # if info isn't under required length return error
        if len(username) > 64:
            success = False
            flash('Username must be under 64 characters.', 'danger')
        if len(email) > 64:
            success = False
            flash('Email must be under 64 characters.', 'danger')
        if len(password) > 64:
            success = False
            flash('Password must be under 64 characters.', 'danger')

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
        except:
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

    return render_template('register.html', session=session)


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    '''
    Logout page
    '''
    # if user not logged in send to login page
    if not "user" in session:
        return redirect(url_for('login'))

    # Remove data from session
    session.pop("user", None)
    # Redirect to homepage
    return redirect(url_for('index'))



if __name__ == '__main__':
    db.create_all()

    # for i in range(0, 100):
    #     generateRandomTutor()

    app.run(debug=True, host='0.0.0.0')
