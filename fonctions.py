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

 
def give_emoji_free_text(text):
    allchars = [str for str in text]
    emoji_list = [c for c in allchars if c in emoji.UNICODE_EMOJI]
    clean_text = ' '.join([str for str in text.split() if not any(i in str for i in emoji_list)])
    return clean_text
 
def simplify(text):
	try:
		text = unicode(text, 'utf-8')
	except NameError:
		pass
	text = unicodedata.normalize('NFD', text).encode('ascii', 'ignore').decode("utf-8")
	return str(text)
   
 
def data_cleaning(data):
    data = simplify(data)
    data = give_emoji_free_text(data)
    data = re.sub(r'''(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))''', " ", data)
    return data


def wiki_data(data):
    definition  = wikipedia.summary(data, auto_suggest=False, sentences=2)
    return definition
        
def sentiment_scores(sentence):
    sid_obj = SentimentIntensityAnalyzer()
    sentiment_dict = sid_obj.polarity_scores(sentence) 
    return sentiment_dict
    

def top_trends(country):
    
    auth = tweepy.OAuthHandler(credentials.consumer_key, credentials.consumer_secret)
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