from config import TWITTER_BEARER_TOKEN, DB, PW, HOST, USER, PORT
import re, string
import tweepy
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import numpy as np
from textblob import TextBlob
import pandas as pd
from datetime import datetime
import psycopg2

class TwitterSentiment:

    def __init__(self):
        self.bearer_token = TWITTER_BEARER_TOKEN
        self.database = DB, 
        self.user = USER, 
        self.password = PW, 
        self.host = HOST, 
        self.port = PORT
    
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
        avg_compound = np.average(compound_list)
        
        #Number of Tweets (Total, Positive, Negative, Neutral)
        tweet_list = pd.DataFrame(tweet_list)
        neutral_list = pd.DataFrame(neutral_list)
        negative_list = pd.DataFrame(negative_list)
        positive_list = pd.DataFrame(positive_list)
        self.upload_to_db(len(positive_list), len(negative_list), len(neutral_list), avg_compound, keyword)  

    def upload_to_db(self, positive, negative, neutral, compound, coin):
        now = datetime.now()
        print('Coin: ', coin)
        print('positive number: ', positive)
        print('negative number: ', negative)
        print('neutral number: ', neutral)
        print('average compound: ', compound) 
        print('time: ', now)
        
        # why are my environment variables being loaded as tuples? I have no idea
        try:
            conn = psycopg2.connect(
                database = self.database[0], 
                user = self.user[0], 
                password = self.password[0], 
                host = self.host[0], 
                port = self.port
            )
            cur = conn.cursor()
            cur.execute('''INSERT INTO sentiment 
                        (date_created, positive, negative, neutral, compound, coin) 
                        VALUES (%s, %s, %s, %s, %s, %s)''', 
                        (now, positive, negative, neutral, compound, coin))
            conn.commit()
            conn.close()
            cur.close()
        except Exception as e: 
            print('error with database...', e)
        

#For testing, main function is run in app.py   
if __name__ == "__main__":
    COINS = ['BTC', 'MATIC', 'ETH', 'ADA', 'XLM']
    twitter = TwitterSentiment()  
    for coin in COINS:
        twitter.gather_sentiment(coin, 100)