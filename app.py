from twitter_sentiment import TwitterSentiment

def handler(event, context):
        COINS = ['BTC', 'MATIC', 'ETH', 'ADA', 'XLM']
        twitter = TwitterSentiment()
        
        for coin in COINS:
            twitter.gather_sentiment(coin, 100)