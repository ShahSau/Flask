from flask import Flask,request, render_template, flash, redirect, url_for, session, logging
from wtforms import Form, StringField,TextAreaField, PasswordField,validators
#from data import Articles
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime
from passlib.hash import sha256_crypt
from functools import wraps
from flask_ckeditor import CKEditor

app = Flask(__name__)
ckeditor = CKEditor(app)
app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db_app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'thisisasecret'
#Articles = Articles()

db = SQLAlchemy(app)
#user model
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


#article model
class Articles(db.Model):
    __tablename__ = 'articles'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    subtitle = db.Column(db.String(200))
    author = db.Column(db.String(200))
    body = db.Column(db.Text())
    create_date = db.Column(db.DateTime)

    def __init__(self, title, subtitle, author, body, create_date):
        self.title = title
        self.subtitle = subtitle
        self.author = author
        self.body = body
        self.create_date = create_date


@app.route('/')
def index():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/articles')
def articles():
    result = Articles.query.all()
    if result != 0:
        return render_template('articles.html',articles=result)
    else:
        message= 'No articles found'
        return render_template('articles.html', msg=message)

@app.route('/article/<string:id>/')
def article(id):
    fetched_article= Articles.query.filter_by(id = id).first()
    return render_template('article.html', article=fetched_article)


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
        flash('You are now registered and please login', 'success')
        redirect(url_for('login'))

    return render_template('register.html', form = form)

    #loging

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password_candided = request.form['password']
        if Users.query.filter_by(username = username).count !=0:

            data = Users.query.filter_by(username = username).first()
            password = data.password
            if sha256_crypt.verify(password_candided, password):
                #passed 
                session['logged_in'] = True
                session['username'] = username

                flash('You are now logged in', 'success')
                return redirect(url_for('dashboard'))
            else:
                return render_template('login.html',errors=['Invalid login'])
        else:
            return render_template('login.html',errors=['Username not found'])
    return render_template('login.html')

#check if user is logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, please login','danger')
            return redirect(url_for('login'))
    return wrap       
#logout
@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))

#dashboard
@app.route('/dashboard')
@is_logged_in
def dashboard():
    result = Articles.query.all()
    if result != 0:
        return render_template('dashboard.html',articles=result)
    else:
        message= 'No articles found'
        return render_template('dashboard.html', msg=message)

#article form class
class ArticleForm(Form):
    title= StringField('Title', [validators.Length(min=1,max=250)])
    subtitle = StringField('Subtitle', [validators.Length(min=5,max=250)])
    body= TextAreaField('Body', [validators.Length(min=30)])

#add article
@app.route('/add_article', methods=['GET', 'POST'])
@is_logged_in
def add_article():
    form = ArticleForm(request.form)
    if request.method == 'POST' and form.validate():
        new_article = Articles(
        title = form.title.data,
        subtitle = form.subtitle.data,
        author = session['username'],
        body = form.body.data,
        create_date = datetime.now()
        )
        db.session.add(new_article)
        db.session.commit()
        flash('Article created', 'success')
        redirect(url_for('dashboard'))
    return render_template('add_article.html', form =form)


#edit article
@app.route('/edit_article/<string:id>', methods=['GET', 'POST'])
@is_logged_in
def edit_article(id):
    edit_fetchedarticle= Articles.query.filter_by(id = id).first()
    #print(edit_fetchedarticle.title)
    
    #get the form
    form = ArticleForm(request.form)

    #populate the article
    #request.form.title= edit_fetchedarticle.title 
    #request.form.subtitle= edit_fetchedarticle.subtitle
    #request.form.body = edit_fetchedarticle.body

    if request.method == 'POST' and form.validate():
        edit_fetchedarticle.title = request.form['title'],
        edit_fetchedarticle.subtitle = request.form['subtitle'],
        edit_fetchedarticle.author = session['username'],########
        edit_fetchedarticle.body = request.form['body'],
        edit_fetchedarticle.create_date = datetime.now()
        #)
        db.session.update(new_article)
        db.session.commit()
        flash('Article updated', 'success')
        redirect(url_for('dashboard'))
    return render_template('edit_article.html',form=form)



if __name__ == '__main__':
    app.run()
