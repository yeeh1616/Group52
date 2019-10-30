from eca import *
import json
import eca.http
import datetime
import textwrap
import pprint
import re

# This function will be called to set up the HTTP server
def add_request_handlers(httpd):
    # add an event-generating request handler to fire 'order' events
    # This requires the POST method because the event generation handler only
    # understands POST requests.
    httpd.add_route('/api/order', eca.http.GenerateEvent('order'), methods=['POST'])

    # use the library content from the template_static dir instead of our own
    # this is a bit finicky, since execution now depends on a proper working directory.
    httpd.add_content('/lib/', 'template_static/lib')
    httpd.add_content('/style/', 'template_static/style')



# binds the 'setup' function as the action for the 'init' event
# the action will be called with the context and the event
@event('init')
def setup(ctx, e):
    ctx.tweetList = []
    ctx.f = open("data/sports.json", "r")
    ctx.count = 0
    fire('sample', {'previous': 0.0})
    ctx.words = {}
    
# simple word splitter
pattern = re.compile('\W+')

def clip(lower, value, upper):
    return max(lower, min(value, upper))

# sample stopword list, needs to be much more sophisticated
stopwords = ['the', 'for', 'and', 'http', 'you', 'what', 'why', 'where', 'are', 'not', 'www', 'com']

def words(message):
    result = pattern.split(message)
    result = map(lambda w: w.lower(), result)
    result = filter(lambda w: w not in stopwords, result)
    result = filter(lambda w: len(w) > 2, result)
    return result

@event('sample')
def generate_sample(ctx, e):
    try:
        line = ctx.f.readline()

        if line:
            tweet = json.loads(line)
        else:
            return

    except:
        fire('sample', {'previous': 0.0})
    else:
        for w in words(tweet['text']):
            emit('word', {
                'action': 'add',
            'value': (w, 1)
            })
            emit('taart', {
                'action': 'add',
                'value': (str(w[0]), 1)
            })
            emit('balk', {
                'action': 'add',
                'value': (str(w[0]), 1)
            })

    
        # nicify text
        text = textwrap.fill(tweet['text'],initial_indent='    ', subsequent_indent='    ')
        # parse date
        time = datetime.datetime.strptime(tweet['created_at'], '%a %b %d %H:%M:%S %z %Y')
        # generate output
        output = "[{}] {} (@{}):\n{}".format(time, tweet['user']['name'], tweet['user']['screen_name'], text)
        
        ctx.tweetList.append(tweet)
        emit('message', {'text': "{}".format(output) })
        fire('sample', {'previous': tweet}, delay=1)

@event('order')
def order(ctx, e):
    keyword = e.data['keyword']
    # text = e.data['text']
    # time = e.data['time'].strftime('%Y-%m-%d %H:%M:%S')

    for tweet in ctx.tweetList:
        if keyword in tweet['text']:
            emit('message', {
                'text': "Tweet: {}".format(tweet['text'])
            })

    # emit('message',{
    #     'text': "{}".format("Test submit successed!")
    # })