import tweepy
import pandas as pd
from fonctions import data_cleaning
from fonctions import summarization
from Common import Credentials


def twitter_queries(param1, max_results):
    query = ""+param1+" lang:en -is:retweet"
    w_credentials = Credentials()
    api = tweepy.API(tweepy.AppAuthHandler(w_credentials.user_key, w_credentials.user_secret))
    tweet_text = []

    for tweet in tweepy.Cursor(api.search_tweets, q=query).items(max_results):
        tweet_text.append(data_cleaning(tweet.text))
        
    tweets_df = pd.DataFrame(tweet_text, columns=['text'])
    # tweets_df.to_csv('out.csv')
    
    return summarization(''.join(map(str, tweets_df['text'].tolist())))
