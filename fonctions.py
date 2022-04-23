from transformers import PegasusForConditionalGeneration, PegasusTokenizer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import re
import emoji
import unicodedata
import wikipedia
import tweepy

from Common import Credentials


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
    

def top_trends(ai_country: str, ai_credentials: Credentials) -> list:
    # Retrieve API with user credentials
    # *************************************
    w_auth = tweepy.OAuth1UserHandler(ai_credentials.user_key, ai_credentials.user_secret)
    w_auth.set_access_token(ai_credentials.access_token, ai_credentials.access_token_secret)
    w_api = tweepy.API(w_auth)
    w_top_10_trends = []

    for trend in w_api.available_trends():
        if trend['country'] == ai_country:
            w_top_10_trends = [w_value["name"] for w_value in w_api.get_place_trends(id=trend['woeid']).values()[:10]]
            break

    return w_top_10_trends
