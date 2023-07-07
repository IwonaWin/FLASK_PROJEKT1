from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from datetime import datetime
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_pyfile('config.cfg')
bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)

class NameForm(FlaskForm):
    name = StringField('Jakie jest Twoje imię?', validators=[DataRequired()])
    submit = SubmitField('Wyślij')
    
class User(db.Model): #Class which represents all people in school
    id = db.Column(db.Integer, primary_key=True, unique=True) #unique key
    firstname = db.Column(db.String(30)) #firstname user
    lastname = db.Column(db.String(30)) #lastnameuser
    role = db.Column(db.String(15)) #role uf user: director/student/teacher
    group = db.Column(db.String(5)) #name of group students
    subject = db.Column(db.String(20)) #for teacher, subjecht which it's learning
    supervising = db.Column(db.String(5)) #if teacher have own group add here name of this group
    active = db.Column(db.Boolean) #if user is login or logout on the page
    

@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(firstname=form.name.data).first()
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Wygląda na to, że teraz nazywasz się inaczej!')
        if user is None:
            user = User(firstname=form.name.data)
            db.session.add(user)
            db.session.commit()
            session['known'] = False
        else:
            session['known'] = True    
        session['name'] = form.name.data
        return redirect(url_for('index'))
    return render_template('index.html',the_current_time=datetime.utcnow(), the_form=form,the_name=session.get('name'), the_known=session.get('known', False))

@app.route('/kontakt')
def kontakt():
    return render_template('kontakt.html')


@app.route('/user/<name>')
def user(name):
    return render_template('user.html', the_name=name)

@app.route('/people')
def people():
    db.create_all()
    uzytkownicy = User.query.all()   
    return render_template('people.html', the_uzytkownicy=uzytkownicy)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template('404.html'), 500


if __name__ == "__main__":
    app.run()