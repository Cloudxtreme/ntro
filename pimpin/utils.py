from django.conf import settings
from pyklout import Klout
import twitter
import math

def get_klout_score(username):
    """ Get klout score based on twitter handle """
    api   = Klout(settings.API_KLOUT_KEY)
    data  = api.identity(username, 'twitter')
    score = api.score(data['id'])
    return score['score']


def get_twitter_user(username):
    """ Get twitter user (properties like name, profile_image_url
        and the amazing _profile_background_color) """
    api   = twitter.Api(consumer_key=settings.API_TWITTER_KEY, \
                        consumer_secret=settings.API_TWITTER_SECRET, \
                        access_token_key=settings.API_TWITTER_TOKEN_KEY, \
                        access_token_secret=settings.API_TWITTER_TOKEN_SECRET)
    try:
        return api.GetUser(screen_name=username)
    except:
        return None

def get_twitter_followers(username):
    """ Get number of twitter followers """
    user = get_twitter_user(username)
    return user.followers_count


def get_price(buyer, victim):
    """ Determine price of introduction using patented formula """
    buyer_klout = get_klout_score(buyer)
    buyer_tweet = get_twitter_followers(buyer)
    victim_klout = get_klout_score(victim)
    victim_tweet = get_twitter_followers(victim)
    startup_price = 10
    klout_rate    = 2
    tweet_rate    = 1000
    return startup_price \
           + klout_rate * max(0, victim_klout - buyer_klout) \
           + tweet_rate * max(0, (math.log(victim_tweet, 10) - math.log(buyer_tweet, 10)) ** 1.4)
