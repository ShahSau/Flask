from flask import Flask, render_template, request,url_for
from flask_fontawesome import FontAwesome


app = Flask(__name__,template_folder='../templates',static_folder='../static')
fa = FontAwesome(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        customer = request.form['customer']
        dealer = request.form['dealer']
        rating = request.form['rating']
        comments = request.form['comments']
        return render_template('success.html')

if __name__ == '__main__':
    app.debug = True
    app.run()
