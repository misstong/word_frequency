from flask import Flask
import config
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
#app.config.from_object(os.environ['APP_SETTINGS'])
app.config.from_object(config.DevelopmentConfig)
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
db = SQLAlchemy(app)

#from models import Result

@app.route('/')
def hello():
    return "hello"


if __name__ == "__main__":
    app.run()