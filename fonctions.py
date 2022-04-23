import torch
from transformers import PegasusForConditionalGeneration, AutoTokenizer, AutoConfig
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import re
import emoji
import unicodedata
import wikipedia
import tweepy

from Common import Credentials


def simplify(ai_text: str) -> str:
    return unicodedata.normalize('NFD', ai_text).encode('ascii', 'ignore').decode("utf-8")


def data_cleaning(ai_data: str):
    data = emoji.get_emoji_regexp().sub(r"", simplify(ai_data))
    return re.sub(r'''(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))''', " ", data)


def wiki_data(data):
    return wikipedia.summary(data, auto_suggest=False, sentences=2)


def sentiment_scores(sentence: str) -> dict:
    return SentimentIntensityAnalyzer().polarity_scores(sentence)
    

def top_trends(ai_country: str, ai_credentials: Credentials) -> list:
    # Retrieve API with user credentials
    # *************************************
    w_auth = tweepy.OAuth1UserHandler(ai_credentials.user_key,
                                      ai_credentials.user_secret,
                                      ai_credentials.access_token,
                                      ai_credentials.access_token_secret)
    w_api = tweepy.API(w_auth)
    w_top_10_trends = []

    for trend in w_api.available_trends():
        if trend['country'] == ai_country:
            w_top_10_trends = [w_value["name"] for w_value in w_api.get_place_trends(id=trend['woeid']).values()[:10]]
            break

    return w_top_10_trends


def summarization(data) -> str:
    tokenizer = AutoTokenizer.from_pretrained("./models/tokenizer")
    model = PegasusForConditionalGeneration(AutoConfig.from_pretrained("./models/pegasus-quantized-config"))
    
    reconstructed_quantized_model = torch.quantization.quantize_dynamic(
        model, {torch.nn.Linear}, dtype=torch.qint8
    )
    reconstructed_quantized_model.load_state_dict(torch.load("./models/pegasus-quantized.pt"))
    
    tokens = tokenizer(data, truncation=True, padding="longest", return_tensors="pt")
    text = tokenizer.decode(reconstructed_quantized_model.generate(**tokens)[0])
    return text.replace("<pad>", "").replace("</s>", "")
