from flask import render_template, url_for, flash, redirect
from Day018.models import User, Post
from Day018.form import RegistrationForm, LoginForm
from Day018 import app

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
