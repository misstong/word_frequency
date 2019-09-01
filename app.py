from flask import Flask,render_template,request
import config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
import requests
import sys
import logging
import operator 
import re
import nltk
from stop_words import stops 
from collections import Counter 
from bs4 import BeautifulSoup
from flask import jsonify

from rq import Queue
from rq.job import Job 
from worker import conn

app = Flask(__name__)
#app.config.from_object(os.environ['APP_SETTINGS'])
app.config.from_object(config.DevelopmentConfig)
#app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
db = SQLAlchemy(app)
migrate = Migrate(app,db)

# q = Queue(connection=conn)

app.logger.setLevel(logging.INFO)
app.logger.info('Microblog startup')

def count_and_save_words(url):
    errors = []
 
    try:
        r = requests.get(url)
    except :
        errors.append("Unable to get URL.")
        return {'error':errors}
    if r:
        raw = BeautifulSoup(r.text,'html.parser').get_text()
        nltk.data.path.append('./nltk_data/')
        tokens = nltk.word_tokenize(raw)
        text = nltk.Text(tokens)
        nonPunct = re.compile('.*[A-Za-z].*')
        raw_words = [w for w in text if nonPunct.match(w)]
        raw_word_count = Counter(raw_words)

        no_stop_words = [w for w in raw_words if w.lower() not in stops]
        no_stop_words_count = Counter(no_stop_words)

        try:
            result = Result(
                url=url,
                result_all=raw_word_count,
                result_no_stop_words=no_stop_words_count
            )
            db.session.add(result)
            db.session.commit()
            return {'id':result.id}
        except:
            errors.append("Unable to add item to database.")
            return {'error':errors}
@app.route('/',methods=['GET','POST'])
def index():
    errors = []
    results = {}
    if request.method == 'POST':
        try:
            url = request.form['url']
            r = requests.get(url)
            # app.logger.info(r.text)
            # print(r.text, file=sys.stdout)
            # sys.stdout.flush()
        except :
            errors.append("Unable to get URL.")
            return render_template('index.html',errors=errors)
        if r:
            raw = BeautifulSoup(r.text,'html.parser').get_text()
            nltk.data.path.append('./nltk_data/')
            tokens = nltk.word_tokenize(raw)
            text = nltk.Text(tokens)
            nonPunct = re.compile('.*[A-Za-z].*')
            raw_words = [w for w in text if nonPunct.match(w)]
            raw_word_count = Counter(raw_words)

            no_stop_words = [w for w in raw_words if w.lower() not in stops]
            no_stop_words_count = Counter(no_stop_words)
            results = sorted(
                no_stop_words_count.items(),
                key=operator.itemgetter(1),
                reverse=True
            )[:10]
            try:
                result = Result(
                    url=url,
                    result_all=raw_word_count,
                    result_no_stop_words=no_stop_words_count
                )
                db.session.add(result)
                db.session.commit()
            except:
                errors.append("Unable to add item to database.")
    return render_template('index.html',errors=errors,results=results)
from models import Result
import json

@app.route('/start',methods=['POST'])
def start():
    url = json.loads(request.data.decode())['url']
    return  count_and_save_words(url)

@app.route('/results/<id>',methods=['GET'])
def get_results(id):
    result = Result.query.filter_by(id=id).first()
    if result:
        results = sorted(
            result.result_no_stop_words.items(),
            key=operator.itemgetter(1),
            reverse=True
        )[:10]
        return jsonify(results)
    else:
        return 'Nay!',202
# @app.route('/1')
# def index2():
#     results = {}
#     if request.method == "POST":
#         # get url that the person has entered
#         url = request.form['url']
#         if 'http://' not in url[:7]:
#             url = 'http://' + url
#         job = q.enqueue_call(
#             func=count_and_save_words, args=(url,), result_ttl=5000
#         )
#         print(job.get_id())

#     return render_template('index.html', results=results)

if __name__ == "__main__":
    app.run()