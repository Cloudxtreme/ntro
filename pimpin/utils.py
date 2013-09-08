from django.conf import settings
from pyklout import Klout
import twitter

def get_klout_score(username):
    """ Get klout score based on twitter handle """
    api   = Klout(settings.API_KLOUT_KEY)
    data  = api.identify(username, 'twitter')
    score = api.score(data['id'])
    return score['score']


def get_twitter_followers(username):
    """ Get number of twitter followers """
    api   = twitter.Api(consumer_key=settings.API_TWITTER_KEY \
                        consumer_secret=settings.API_TWITTER_SECRET \
                        access_token_key=settings.API_TWITTER_TOKEN_KEY \
                        access_token_secret=settings.API_TWITTER_TOKEN_SECRET)
    
    followers = api.GetFollowers(username)
    return len(followers)
