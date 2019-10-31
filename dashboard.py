from eca import *
import eca.http
import json

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
    ctx.f = open("dashboard_static/sports.json", "r")

    ctx.count = 0
    fire('sample', {'previous': 0.0})


# define a normal Python function
def clip(lower, value, upper):
    return max(lower, min(value, upper))

@event('sample')
def generate_sample(ctx, e):
    try:
        line = ctx.f.readline()

        if line:
            tweet = json.loads(line)
        else:
            return
    except:
        print("Non-json.")
        # emit('message', {
        #     'text': "{}".format('Error')
        # })
        fire('sample', {'previous': 'Error'}, delay=0.05)
    else:
        ctx.tweetList.append(tweet)
        print(tweet['text'])
        # emit('message', {
        #     'text': "Tweet: {}".format(tweet['text'])
        # })
        emit('tweet', tweet)
        fire('sample', {'previous': tweet}, delay=0.05)


@event('order')
def order(ctx, e):
    # text = e.data['text']
    # time = e.data['time'].strftime('%Y-%m-%d %H:%M:%S')

    search_terms = e.data['keyword'].split(" ")
    search_hashtags, search_keywords = partition(lambda w: w[0] == "#", search_terms)
    print(hashtags, keywords)

    for tweet in ctx.tweetList:
        try:
            tweet_hashtags = tweet.retweeted_status.entities.hashtags
            if elm_in_list(search_hashtags, tweet_hashtags):
                emit('tweet', tweet)
                continue
        except ReferenceError as e:
            pass

        for kw in search_keywords:
            if kw in tweet['text']:
                emit('tweet', tweet)

    # emit('message',{
    #     'text': "{}".format("Test submit successed!")
    # })


# @event('tweet')
# def echo(ctx, e):
#     emit('tweet', e.data)


def partition(pred, iterable):
    trues = []
    falses = []
    for item in iterable:
        if pred(item):
            trues.append(item)
        else:
            falses.append(item)
    return trues, falses

def elm_in_list(elm_list, search_list):
    for e in elm_list:
        for s in search_list:
            if e == s:
                return True
    return False