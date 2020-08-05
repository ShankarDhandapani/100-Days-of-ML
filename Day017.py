from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from form import RegistrationForm, LoginForm
from datetime import datetime

app = Flask(__name__)

app.config['SECRET_KEY'] = '34e2ab4961bdc651b264268784f71b89'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    profile_picture = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.profile_picture}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


posts = [
    {
        'author' : 'Shankar Dhandapani',
        'title' : 'Portfolio',
        'content' : "I'm Shankar. I'm an freelancer and Developer.",
        'date_posted' : 'April 20, 2018'
    },
    {
        'author' : 'Shankar Dhandapani',
        'title' : 'My Blog 2',
        'content' : "Second Blog content",
        'date_posted' : 'April 20, 2018'
    }
]

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', posts=posts, title="Home Page")

@app.route('/about')
def about():
    return render_template('about.html', title="About Page")    

@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == "noreply@mysite.com" and form.password.data == "password":
            flash('Login Successful', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Failed. Please check you credentials.', 'danger')
    return render_template('login.html', title="Login Page", form=form)

@app.route('/register', methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title="Register Page", form=form)

if __name__=='__main__':
    app.run(debug=True)