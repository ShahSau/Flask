from flask import render_template, url_for, flash, redirect
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm
from flaskblog.models import User, Post




posts =[
    {
        'author': 'Shah',
        'title': 'post 1',
        'content': 'Content fisrt post',
        'date_posted': 'April 20,2020'
    }, 
     {
        'author': 'Sau',
        'title': 'post 2',
        'content': 'Content second post',
        'date_posted': 'June 20,2020'
    }
]

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", posts=posts)

@app.route("/about")
def about():
    return render_template("about.html", title="about")

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!','success')
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        #####
        return redirect(url_for('home'))
    return render_template('register.html', title="Register", form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash("You have been logged in!!", 'success')
            return redirect(url_for('home'))
        else:
            flash("Login unsuccessful, please check username and password", 'danger')
    return render_template('login.html', title="Login", form=form)