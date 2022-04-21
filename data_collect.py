import tweepy
import pandas as pd
from fonctions import data_cleaning
from fonctions import summarization
import credentials

auth = tweepy.AppAuthHandler(credentials.consumer_key, credentials.consumer_secret)
api = tweepy.API(auth)


def twitter_queries(param1, max_results):
    query = ""+param1+" lang:en -is:retweet"  
    auth = tweepy.AppAuthHandler(credentials.consumer_key, credentials.consumer_secret)
    api = tweepy.API(auth)
    tweet_text = []
    for tweet in tweepy.Cursor(api.search_tweets, q=query).items(max_results):
        tweet_text.append(data_cleaning(tweet.text))
        
    tweets_df = pd.DataFrame(tweet_text, columns = ['text'])
    #tweets_df.to_csv('out.csv') 
    
    result = ''.join(map(str, tweets_df['text'].tolist()))
    return summarization(result)