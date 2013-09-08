from django.conf import settings

from social_auth.models import UserSocialAuth

from pyklout import Klout
import twitter
import math

def get_klout_score(username):
    """ Get klout score based on twitter handle """
    api   = Klout(settings.API_KLOUT_KEY)
    data  = api.identity(str(username), 'twitter')
    score = api.score(data['id'])
    return score['score']


def get_twitter_user(username):
    """ 
    Get twitter user (properties like name, profile_image_url
    and the amazing _profile_background_color)

    """
    try:
        social_auth = UserSocialAuth.objects.get(user__username=username)
        token_json = social_auth.extra_data['access_token']
        splits = token_json.split('=')
        oauth_token = splits[-1]
        oauth_token_secret = splits[1].split('&')[0]
    except UserSocialAuth.DoesNotExist:
        oauth_token = settings.API_TWITTER_TOKEN_KEY
        oauth_token_secret = settings.API_TWITTER_TOKEN_SECRET

    api = twitter.Api(consumer_key=settings.API_TWITTER_KEY,
                      consumer_secret=settings.API_TWITTER_SECRET,
                      access_token_key=oauth_token,
                      access_token_secret=oauth_token_secret)
    try:
        return api.GetUser(screen_name=username)
    except:
        api = twitter.Api(consumer_key=settings.API_TWITTER_KEY,
                          consumer_secret=settings.API_TWITTER_SECRET,
                          access_token_key=settings.API_TWITTER_TOKEN_KEY,
                          access_token_secret=settings.API_TWITTER_TOKEN_SECRET)
        return api.GetUser(screen_name=username)

def get_twitter_followers(username):
    """ Get number of twitter followers """
    user = get_twitter_user(username)
    if user is not None:
        return user.followers_count
    else:
        return 1

def get_scores(username):
    scores = dict()
    scores['klout']   = get_klout_score(username)
    scores['twitter'] = get_twitter_followers(username)
    return scores
    

def get_price(buyer, victim):
    """ Determine price of introduction using patented formula """
    buyer_scores = get_scores(buyer)
    victim_scores = get_scores(victim)
    startup_price = 10
    klout_rate    = 1
    tweet_rate    = 250
    return startup_price \
           + klout_rate * max(0, victim_scores['klout'] - buyer_scores['klout']) \
           + tweet_rate * max(0, (math.log(victim_scores['twitter'], 10) - math.log(buyer_scores['twitter'], 10)) ** 1.4)
