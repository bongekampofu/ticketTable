from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.mysql import TIME
from flask import Flask, flash, request, redirect, url_for
from sqlalchemy.exc import IntegrityError
from datetime import datetime as dt
from flask import Flask, render_template, url_for, redirect, request



app = Flask(__name__, static_folder='static')

# see http://bootswatch.com/3/ for available swatches
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:\\Users\\Bongeka.Mpofu\\DB Browser for SQLite\\function.db'

app.config['SECRET_KEY'] = 'this is a secret key '
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


UPLOAD_FOLDER = 'static'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



class Tickets(db.Model):
    __tablename__ = "tickets"
    ticketID = db.Column(db.Integer, primary_key=True)
    functionName = db.Column(db.String(80), nullable=False)
    ticketsLeft = db.Column(db.Integer , nullable=False)
    generalPrice = db.Column(db.Numeric(10, 2), )
    royalPrice = db.Column(db.Numeric(10, 2), )
    platinumPrice = db.Column(db.Numeric(10, 2), )
    type = db.Column(db.String(80), nullable=False)
    date = db.Column(db.Date, nullable=False)
    endDate = db.Column(db.Date, nullable=False)
    description = db.Column(db.String(80), nullable=False)
    venueID = db.Column(db.Integer)
    adminID = db.Column(db.Integer)
    startTime = db.Column(TIME(), nullable=False)
    endTime = db.Column(TIME(), nullable=False)


class Transactions(db.Model):
    __tablename__ = "transactions"
    transactID = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer)
    eventID = db.Column(db.Integer)
    tickets = db.Column(db.Integer)
    transTime = db.Column(db.DateTime, default=dt.now)
    dateBooked = db.Column(db.DateTime, nullable=False)

@app.route('/')
def index():
    tickets = db.session.query(Tickets).all()
    return render_template('index.html', tickets=tickets)


@app.route('/process_booking', methods=['POST'])
def process_booking():
    data = request.form
    valid_quantities = {}

    for key, value in data.items():
        function_name, quantity_type = key.split('_')
        quantity = int(value)
        if quantity > 0:
            # Save quantities in a dictionary
            if function_name not in valid_quantities:
                valid_quantities[function_name] = {}
            valid_quantities[function_name][quantity_type] = quantity

    # Print quantities
    for function_name, quantities in valid_quantities.items():
        print(f"Function Name: {function_name}")
        for quantity_type, quantity in quantities.items():
            print(f"- {quantity_type}: {quantity}")

    return "Valid quantities processed successfully"


if __name__ == "__main__":
    #app_dir = op.realpath(os.path.dirname(__file__))
    with app.app_context():
        db.create_all()
    app.run(debug=True)
