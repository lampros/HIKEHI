from flask import Flask, render_template, flash
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Email
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Create a Flask Instance
app = Flask(__name__)

#Add Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
#Secret Key
app.config['SECRET_KEY'] = "my super secret key that no one is supposed to know"
# Initialize the Database
db = SQLAlchemy(app)

# Create Model

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique =True, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

with app.app_context():
    db.create_all()

# Create a User Form Class
class UserForm(FlaskForm):
    name = StringField("Name", validators = [DataRequired()])
    email = StringField("Email", validators = [DataRequired()])
    age = IntegerField("Age", validators = [DataRequired()])
    submit = SubmitField("Submit") 


# Create a Form Class
class NamerForm(FlaskForm):
    name = StringField("What's Your Name", validators = [DataRequired()])
    email = StringField("What's Your Email", validators = [DataRequired()])
    age = IntegerField("What's Your Age", validators = [DataRequired()])
    submit = SubmitField("Submit") 




@app.route('/user/add', methods=['GET', 'POST'])
def add_user():
    name = None
    email = None
    age = None
    form = UserForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            user = Users(name=form.name.data, email=form.email.data, age=form.age.data)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        email = form.email.data
        age = form.age.data
        form.name.data = ''
        form.email.data = ''
        form.age.data = ''  
        flash("User Added Successfully!") 
    our_users = Users.query.order_by(Users.date_added)     
    return render_template('add_user.html', 
                           form = form,
                           name=name,
                           email=email, 
                           age=age,
                           our_users=our_users)

# create an index route decorator
@app.route('/')
def index():
    first_name = "<b>Lampros</b>"
    return render_template("index.html", first_name=first_name)

@app.route('/user/<name>')
def user(name):
    return render_template("user.html", user_name = name)

# Create Custom Error Pages

# Invalid URL
@app.errorhandler(404)
def page_no_found(e):
    return render_template('404.html'), 404

# Internal Server Error
@app.errorhandler(500)
def page_no_found(e):
    return render_template('500.html'), 500

# Create Name Page
@app.route('/name', methods=['GET','POST'])
def name():
    name = None
    email = None
    age = None
    form = NamerForm()
    # Validate Form 
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        email = form.email.data
        form.email.data = ''
        age = form.age.data
        form.age.data = ''

        flash("Form Submitted Successfully, User added Successfully!")
    return render_template("name.html",
                           name = name,
                           email = email,
                           age = age,
                           form = form)

if __name__ == "__main__":
    app.run(debug=True)
