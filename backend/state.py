import os
import random
import uuid

import requests
import redis

from configuration import redis_host, state


def get_cat_picture():  # Use the cat API and get a random image of the 100 returned
    r = requests.get('https://api.thecatapi.com/v1/images/search?limit=100')
    return r.json()[random.randint(0, 99)]['url']


inmemory_state_image_link = None
inmemory_state_hits = 0
def inmemory_state():
    global inmemory_state_image_link
    global inmemory_state_hits

    if not inmemory_state_image_link:
        inmemory_state_image_link = get_cat_picture()

    inmemory_state_hits += 1  # Increase the number of hits

    return (inmemory_state_image_link, inmemory_state_hits)  # Return URL and hits


def redis_state():
    state_keys = {
        'image_link': 'timber:state:image_link',
        'state_hits': 'timber:state:state_hits',
    }

    try:
        # Connect to redis
        r = redis.Redis(
            host=redis_host, port=6379, db=0,
            socket_timeout=2, socket_connect_timeout=2,
            decode_responses=True
        )

        # Increase the number of state_hits
        r.incr(state_keys['state_hits'])

        # If we don't have an image URL yet, let's fetch one.
        if r.get(state_keys['image_link']) is None:
            r.set(state_keys['image_link'], get_cat_picture())

        image_link = r.get(state_keys['image_link'])
        return
    except redis.exceptions.ConnectionError:
        return '', 0


state_options = {
    'inmemory': inmemory_state,
    'redis': redis_state,
}
state_function = state_options[state]  # We can easily call the state function then
