from flask import Flask,request, render_template, flash, redirect, url_for, session, logging
from wtforms import Form, StringField,TextAreaField, PasswordField,validators
from data import Articles
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime
from passlib.hash import sha256_crypt

app = Flask(__name__)
app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db_users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'thisisasecret'
Articles = Articles()

db = SQLAlchemy(app)
class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100),  unique=True)
    email = db.Column(db.String(200), unique=True)
    username = db.Column(db.String(200),unique=True)
    password = db.Column(db.String(200))
    register_date = db.Column(db.DateTime)


    def __init__(self, name, email, username, password, register_date):
        self.name = name
        self.email = email
        self.username = username
        self.password = password
        self.register_date = register_date


@app.route('/')
def index():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/articles')
def articles():
    return render_template('articles.html', articles=Articles)

@app.route('/article/<string:id>/')
def article(id):
    return render_template('article.html', id=id)


class RegisterForm(Form):
    name= StringField('Name', [validators.Length(min=1,max=50)])
    username= StringField('UserName', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password',[
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords donot match')
    ])
    confirm = PasswordField('Confirm Password')

@app.route('/register',methods=['GET','POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        new_user = Users(
        name = form.name.data,
        email = form.email.data,
        username = form.username.data,
        password = sha256_crypt.encrypt(str(form.password.data)),
        register_date = datetime.now()
        )
        db.session.add(new_user)
        db.session.commit()
        flash('You are now registered and log in', 'success')
        redirect(url_for('index'))

    return render_template('register.html', form = form)

    #loging

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password_candided = request.form['password']
        #if Users.query.filter(username == username).count() != 0:
        data = Users.query.filter_by(username=username).first()
        #password = data['password']
        print(data)
       # if sha256_crypt.verify(password_candided, password):
        #    print('PASSWORD MATCHED')
       # else:
        #    print('PASSWORD NOt MATCHED')
    return render_template('login.html')


if __name__ == '__main__':
    app.run()
