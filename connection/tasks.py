from pimpin.utils import get_scores, get_price

def get_twitter_info(person):
    print "IM HERE"
    scores = get_scores(person.twitter_handle)
    person.klout_score= int(scores['klout'])
    person.tweet_score = int(scores['twitter'])
    person.score = person.klout_score + person.twitter_score
    user = get_twitter_user(person.twitter_handle)
    person.first_name = user.name
    # TODO: use user.profile_image_url to upload image
    person.save()

def calculate_price(connection):
    """ Calculates the score """
    buyer = connection.requested_by.username
    victim = connection.person.twitter_handle
    connection.price = get_price(buyer, victim)
    connection.save()
