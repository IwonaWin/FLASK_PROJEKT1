from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from datetime import datetime
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config.from_pyfile('config.cfg')
bootstrap = Bootstrap(app)
moment = Moment(app)

class NameForm(FlaskForm):
    name = StringField('Jakie jest Twoje imię?', validators=[DataRequired()])
    submit = SubmitField('Wyślij')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Wygląda na to, że teraz nazywasz się inaczej!')
        session['name'] = form.name.data
        return redirect(url_for('index'))
    return render_template('index.html',the_current_time=datetime.utcnow(), the_form=form,the_name=session.get('name'))

@app.route('/kontakt')
def kontakt():
    return render_template('kontakt.html')


@app.route('/user/<name>')
def user(name):
    return render_template('user.html', the_name=name)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template('404.html'), 500

if __name__ == "__main__":
    app.run()