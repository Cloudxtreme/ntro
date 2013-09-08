from pimpin.utils import *

def get_twitter_info(person):
    scores = get_scores(person.twitter_handle)
    person.score_klout = scores['klout']
    person.score_twitter = scores['twitter']
    person.save()

def calculate_price(connection):
    """ Calculates the score """
    buyer = connection.requested_by.username
    victim = connection.person.twitter_handle
    instance.price = get_price(buyer, victim)
    instance.save()
