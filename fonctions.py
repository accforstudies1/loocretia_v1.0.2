from transformers import PegasusForConditionalGeneration, PegasusTokenizer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import re
import emoji
import unicodedata
import wikipedia
import tweepy
import credentials


def summarization(data):
    tokenizer = PegasusTokenizer.from_pretrained("google/pegasus-xsum")
    model = PegasusForConditionalGeneration.from_pretrained("google/pegasus-xsum")
    tokens = tokenizer(data, truncation=True, padding="longest", return_tensors="pt")
    summary = model.generate(**tokens)
    text = tokenizer.decode(summary[0])
    return text

 
def give_emoji_free_text(ai_text: str) -> str:
    return emoji.get_emoji_regexp().sub(r"", ai_text)


def simplify(ai_text: str) -> str:
    return unicodedata.normalize('NFD', ai_text).encode('ascii', 'ignore').decode("utf-8")


def data_cleaning(ai_data: str):
    data = give_emoji_free_text(simplify(ai_data))
    return re.sub(r'''(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))''', " ", data)


def wiki_data(data):
    return wikipedia.summary(data, auto_suggest=False, sentences=2)


def sentiment_scores(sentence: str) -> dict:
    return SentimentIntensityAnalyzer().polarity_scores(sentence)
    

def top_trends(ai_country: str):

    # Retrieve API with user credentials
    # *************************************
    auth = tweepy.OAuth1UserHandler(credentials.consumer_key, credentials.consumer_secret)
    auth.set_access_token(credentials.access_token, credentials.access_token_secret)
    api = tweepy.API(auth)
    all_trends = api.available_trends()

    
    for trend in all_trends:
        if trend['country'] == country:
            woeid = trend['woeid']
            trends = api.get_place_trends(id = woeid)
            top_10_trends = []
            i = 0
            for value in trends:
                for trend in value['trends']:
                    if i >= 10:
                        exit
                    else:
                        top_10_trends.append(trend['name'])
                        i = i+1
            return top_10_trends