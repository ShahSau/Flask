from flask import Flask, render_template, url_for
from forms import RegistrationForm, LoginForm
app = Flask(__name__)
app.config['SECRET_KEY'] = '2009088dd19a730694a7ca00309b03bb'


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

@app.route("/register")
def register():
    form = RegistrationForm()
    return render_template('register.html', title="Register", form=form)

@app.route("/login")
def login():
    form = LoginForm()
    return render_template('login.html', title="Login", form=form)


if __name__ == '__main__':
    app.run(debug=True)