import os
import uuid

import redis
from configuration import redis_host, state

inmemory_state_uuid = None
def inmemory_state():
    global inmemory_state_uuid
    if not inmemory_state_uuid:
        inmemory_state_uuid = uuid.uuid4()  # Generate a new UUID
        return f'I am keeping state! I generated this UUID and I am keeping it in memory: {inmemory_state_uuid}'
    return f'I am keeping state! The UUID was in memory already, here it is: {inmemory_state_uuid}'

def storage_state():
    # First off, let's make the /state directory if it doesn't exist
    os.makedirs('/state', exist_ok=True)

    file_path = '/state/uuid'
    state_exists = os.path.isfile(file_path)  # Do we already have a state UUID file?
    if state_exists:
        state_uuid = open(file_path).read()  # Let's read the uuid and use that one!
        return f'I am keeping state! I found this UUID in `{file_path}`: {state_uuid}'

    # State file does not exist. Let's create it.
    with open(file_path, 'w+') as f:
        f.write(str(uuid.uuid4()))
    state_uuid = open(file_path).read()  # Let's read the uuid and use that one!
    return f'I am keeping state! I have generated this UUID and I am keeping it in `{file_path}`: {state_uuid}'


def redis_state():
    state_key = 'timber:state:uuid'
    try:
        # Connect to redis
        r = redis.Redis(
            host=redis_host, port=6379, db=0,
            socket_timeout=2, socket_connect_timeout=2,
            decode_responses=True
        )

        if r.get('timber:state:uuid') is None:  # If we have to set state for the first time
            r.set(state_key, str(uuid.uuid4()))
            redis_uuid = r.get(state_key)
            return f'I am keeping state! I generated this UUID and I am keeping it in Redis: {redis_uuid}'

        # If state already exists, we get it and display it
        redis_uuid = r.get(state_key)
        return f'I am keeping state! I got this UUID from Redis: {redis_uuid}'
    except redis.exceptions.ConnectionError:
        return 'Connecting to Redis failed. I cannot keep state.'

state_options = {
    'storage': storage_state,
    'inmemory': inmemory_state,
    'redis': redis_state,
}

if state not in state_options:
    # We are using lambda just to keep the type of the variable consistent.
    description_func = lambda: f"You have set Timber's state to {state}, but I don't know how to handle it!"
if state is None:
    description_func = lambda: 'I am not keeping state.'
else:
    description_func = state_options[state]
