from flask import Flask, render_template,url_for

app = Flask(__name__)
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

if __name__ == '__main__':
    app.run(debug=True)