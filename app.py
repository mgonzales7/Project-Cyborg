import json
import os
import time
from flask import Flask, Response, request
from cyborgapi import cyborg

app = Flask(__name__, static_url_path='', static_folder='public')
app.add_url_rule('/', 'root', lambda: app.send_static_file('index.html'))

@app.route('/generate/<handle>', methods=['GET'])
def cyborg_handler():

    newCyborg = cyborg(handle)
    return Response(newCyborg, mimetype='application/json', headers={'Cache-Control': 'no-cache', 'Access-Control-Allow-Origin': '*'})

if __name__ == '__main__':
    app.run(port=int(os.environ.get("PORT",3000)))
