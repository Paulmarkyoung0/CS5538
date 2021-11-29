import requests
import random
from flask import Flask, render_template
app = Flask(__name__)
from google.cloud import datastore
datastore_client = datastore.Client()

def store_fact(dt):
    entity = datastore.Entity(key=datastore_client.key('visit'))
    entity.update({
        'fact': dt
    })

    datastore_client.put(entity)


def fetch_facts(limit):
    query = datastore_client.query(kind='visit')
    query.order = ['-fact']

    facts = query.fetch(limit=limit)

    return facts

@app.route('/')
def root():
    response = requests.get("http://numbersapi.com/"+str(random.randint(1,100)))
    # Store the current fact in Datastore.
    store_fact(response.content.decode('utf-8'))
    
    # Fetch the most recent 10 facts from Datastore.
    facts = fetch_facts(10)

    return render_template(
        'index.html', facts=facts)

if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)