import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from Day020.models import User, Post
from Day020.form import RegistrationForm, LoginForm, UpdateAccountForm
from Day020 import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required

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
@login_required
def home():
    return render_template('home.html', posts=posts, title="Home Page")

@app.route('/about')
def about():
    return render_template('about.html', title="About Page")    

@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Failed. Please check you credentials.', 'danger')
    return render_template('login.html', title="Login Page", form=form)

@app.route('/register', methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f"Hi {form.username.data}, you're account is ready to use.", 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title="Register Page", form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, "static/profile_pictures", picture_fn)
    output_size = (125,125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn

@app.route("/account", methods=['GET','POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.profile_picture = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Your account has been updated!", "success")
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pictures/' + current_user.profile_picture)
    return render_template('account.html', title="Account", image_file=image_file, form=form)