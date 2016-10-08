import flask
from wtforms import Form, FloatField

app = flask.Flask(__name__)

class SubmitForm(Form):
    F = FloatField()
    

@app.route('/')
def main_view():
    return flask.render_template('main.html')

if __name__ == '__main__':
    app.run(port=8080)