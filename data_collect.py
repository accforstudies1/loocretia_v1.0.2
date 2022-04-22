import tweepy
import pandas as pd
from fonctions import data_cleaning
from fonctions import summarization
import credentials

client = tweepy.Client(credentials.bearer_token)


def twitter_queries(param1, param3: int = 100):
    query = ""+param1+" lang:en -is:retweet"
    
    tweets = client.search_recent_tweets(query=query, max_results = param3)
    tweet_text = []
    
    for tweet in tweets.data:
        tweet_text.append(data_cleaning(tweet.text))
        
    tweets_df = pd.DataFrame(tweet_text, columns = ['text'])
    tweets_df.to_csv('out.csv') 
    
    result = ''.join(map(str, tweets_df['text'].tolist()))
    return summarization(result)
