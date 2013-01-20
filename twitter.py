import os
import time

import tweepy
import config

class TwitterAPI:
    """
    Class for accessing the Twitter API.

    Requires API credentials to be available in environment
    variables. These will be set appropriately if the bot was created
    with init.sh included with the heroku-twitterbot-starter
    """

    def __init__(self):
        auth = tweepy.OAuthHandler(config.TWITTER_CONSUMER_KEY,
                                   config.TWITTER_CONSUMER_SECRET)
        auth.set_access_token(config.TWITTER_ACCESS_TOKEN,
                              config.TWITTER_ACCESS_TOKEN_SECRET)
        self.api = tweepy.API(auth)

    def tweet(self, message):
        """Send a tweet"""
        self.api.update_status(message)

if __name__ == "__main__":
    twitter = TwitterAPI()
    twitter.tweet(sys.argv[1])
#    twitter.tweet("Hello, again, world!")
#    while True:
#        #Send a tweet here!
#        time.sleep(60)
