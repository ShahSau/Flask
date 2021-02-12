from flask import Flask, render_template, request,url_for
from flask_fontawesome import FontAwesome
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

ENV = 'dev'

if ENV=='dev':
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///booking.db'
 
    app.config['SECRET_KEY'] = 'thisisasecret'
    app.debug=True
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = ''

fa = FontAwesome(app)
db = SQLAlchemy(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

class Feedback(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True)
    customer = db.Column(db.String(200), unique=True)
    email = db.Column(db.String(200), unique=True)
    guest = db.Column(db.Integer)
    room= db.Column(db.String(200))
    arrival = db.Column(db.String(200))
    departure=db.Column(db.String(200))
    comments = db.Column(db.Text())

    def __init__(self, customer, email, guest, room, arrival, departure, comments):
        self.customer = customer
        self.email = email
        self.guest = guest
        self.room = room
        self.arrival = arrival
        self.departure = departure
        self.comments = comments





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
        if db.session.query(Feedback).filter(Feedback.customer == customer).count() == 0:
            data = Feedback(customer, email, guest, room, arrival, departure, comments)
            db.session.add(data)
            db.session.commit()
            return render_template('success.html')
        return render_template('index.html', message= 'You have already reserved room at our hotel')

if __name__ == '__main__':
    app.debug = True
    app.run()
