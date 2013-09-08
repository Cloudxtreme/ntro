from celery import task

@task()
def get_twitter_info(person):
    person.score = 100
    person.save()

@task()
def calculate_score(instance):
    """ Calculates the score """
    instance.price= 100
    instance.save()
