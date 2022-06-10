from config import TWITTER_BEARER_TOKEN
import re, string
import tweepy
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import numpy as np
from textblob import TextBlob

class TwitterSentiment:

    def __init__(self):
        self.bearer_token = TWITTER_BEARER_TOKEN
    
    def percentage(self, part, whole):
        return 100 * float(part)/float(whole)

    def clean_tweet(self, text):
        # remove numbers
        text_nonum = re.sub(r'\d+', '', text)
        # remove punctuations and convert characters to lower case
        text_nopunct = "".join([char.lower() for char in text_nonum if char not in string.punctuation]) 
        # substitute multiple whitespace with single whitespace
        # Also, removes leading and trailing whitespaces
        text_no_doublespace = re.sub('\s+', ' ', text_nopunct).strip()
        emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags=re.UNICODE)
        no_emoji_text = emoji_pattern.sub(r'', text_no_doublespace)
        return no_emoji_text

    def gather_sentiment(self, keyword, noOfTweets):
        client = tweepy.Client(bearer_token=self.bearer_token)
        query = f'#{keyword} -is:retweet lang:en'
        tweets = client.search_recent_tweets(query=query, max_results=noOfTweets)
        positive = 0
        negative = 0
        neutral = 0
        polarity = 0
        tweet_list = []
        neutral_list = []
        negative_list = []
        positive_list = []
        compound_list = []

        
        for tweet in tweets.data:
            clean_tweet = self.clean_tweet(tweet.text)
            tweet_list.append(clean_tweet)
            score = SentimentIntensityAnalyzer().polarity_scores(tweet.text)
            analysis = TextBlob(tweet.text)
            neg = score['neg']
            neu = score['neu']
            pos = score['pos']
            comp = score['compound']
            compound_list.append(comp)
            polarity += analysis.sentiment.polarity
            
            if neg > pos:
                negative_list.append(tweet.text)
                negative += 1
            elif pos > neg:
                positive_list.append(tweet.text)
                positive += 1
            elif pos == neg:
                neutral_list.append(tweet.text)
                neutral += 1
        #end of for loop, python indents are hella lame sometimes
        positive = self.percentage(positive, noOfTweets)
        negative = self.percentage(negative, noOfTweets)
        neutral = self.percentage(neutral, noOfTweets)
        polarity = self.percentage(polarity, noOfTweets)
        positive = format(positive, '.1f')
        negative = format(negative, '.1f')
        neutral = format(neutral, '.1f') 
        avg_compound = np.average(compound_list)  

    def upload_to_db(self):
        pass
    