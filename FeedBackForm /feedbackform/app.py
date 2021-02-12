from flask import Flask, render_template, request,url_for
from flask_fontawesome import FontAwesome
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
fa = FontAwesome(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        customer = request.form['customer']
        email=request.form['email']
        guest=request.form['guest']
        room=request.form['room']
        arrival=request.form['arrival']
        departure=request.form['departure']
        comments=request.form['comments']
        if customer == '' or guest == '' or arrival == '':
            return render_template('index.html', message= 'Please enter requird fields')
        return render_template('success.html')

if __name__ == '__main__':
    app.debug = True
    app.run()
