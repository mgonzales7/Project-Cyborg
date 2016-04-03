import json
import os
import time
from flask import Flask, Response, request
from cyborgapi import cyborg

app = Flask(__name__, static_url_path='', static_folder='public')
app.config["DEBUG"] = True
app.add_url_rule('/', 'root', lambda: app.send_static_file('index.html'))

global currentHandle
currentHandle = ''

@app.route('/current', methods=['GET'])
def tweets_handler():
    print 'in tweets_handler'
    tweets = []

    if currentHandle != '': #we generate some more tweets for the currentHandle
        tweets = addNewTweet()
    
    if currentHandle == '' and len(tweets)>1: #if we have leftover tweets reset the JSON file
        with open('tweets.json', 'w') as file:
            file.write('[\n]')

    return Response(json.dumps(tweets), mimetype='application/json', headers={'Cache-Control': 'no-cache', 'Access-Control-Allow-Origin': '*'})

@app.route('/generate/<handle>', methods=['GET'])
def cyborg_handler(handle):
    global currentHandle
    print 'currentHandle is', currentHandle
    print 'handle is', handle

    #reset the tweets list if new handle
    if str(handle) != str(currentHandle):
        currentHandle = handle
        with open('tweets.json','w') as file:
            file.write('[\n]')

    tweets = addNewTweet()

    return Response(json.dumps(tweets), mimetype='application/json', headers={'Cache-Control': 'no-cache', 'Access-Control-Allow-Origin': '*'})

def addNewTweet():
    with open('tweets.json', 'r') as file:
        tweets = json.loads(file.read())
        print 'tweets are', tweets

    newCyborgTweet = cyborg(currentHandle)
    tweets = [json.loads(newCyborgTweet)] + tweets

    with open('tweets.json', 'w') as file:
        file.write(json.dumps(tweets,indent=4, separators=(',',': ')))
        file.close()

    return tweets

if __name__ == '__main__':
    app.run(port=int(os.environ.get("PORT",3000)))