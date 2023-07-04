from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from datetime import datetime
from flask_moment import Moment

app = Flask(__name__)
bootstrap = Bootstrap(app)
moment = Moment(app)

@app.route('/')
def index():
    return render_template('index.html',the_current_time=datetime.utcnow())

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