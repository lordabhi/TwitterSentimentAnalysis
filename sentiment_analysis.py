from twython import Twython
import json
import datetime
import boto3

def lambda_handler(event, context):
    APP_KEY = ''  # Customer Key here
    APP_SECRET = ''  # Customer secret here
    OAUTH_TOKEN = ''  # Access Token here
    OAUTH_TOKEN_SECRET = ''  # Access Token Secret here

    # Instantiate an object
    twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
    
    # Create our query
    query = {
        'q': '@your_twitter_handler',
        'result_type': 'recent',
        'count': 20,
        'lang': 'en',
    }
    
    for status in twitter.search(**query)['statuses']:
        print(status)
        timestamp = status['created_at']
        tweet = status['text']
        favourite_count = status['favorite_count']
        user = status['user']['screen_name']
        
        sentiment=json.loads(getSentiment(tweet))
        print('Tweet Sentiment:'+ sentiment['Sentiment'])
        
        #If the sentiment is positive or neutral, like(favourite) the tweet
        if sentiment['Sentiment'] == 'POSITIVE' or sentiment['Sentiment'] == 'NEUTRAL': 
            id = status['id']
            print('Sending Like/Favourite: '+ tweet)
            twitter.create_favorite(id=id)

    return ''
    
def getSentiment(tweet):
    comprehend = boto3.client(service_name='comprehend')
    return(json.dumps(comprehend.detect_sentiment(Text=tweet, LanguageCode='en'), sort_keys=True))    
