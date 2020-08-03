from flask import Flask, render_template, url_for

app = Flask(__name__)

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

@app.route('/login')
def login():
    return render_template('login.html', title="Login Page")

@app.route('/register')
def register():
    return render_template('register.html', title="Register Page")

if __name__=='__main__':
    app.run(debug=True)