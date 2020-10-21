import redis

# We want to find out if Redis is running in our same pod.

try:
    # Try connecting to our Redis at localhost
    # Since containers in a pod share networking, this would work if Redis was here.
    r = redis.Redis(
        host='localhost', port=6379, db=0,
        socket_timeout=2, socket_connect_timeout=2,
    )
    r.ping()
except redis.ConnectionError:
    is_detected = False
else:
    is_detected = True

if is_detected:
    description = 'It looks like Redis is running next to me in a different container, but we are sharing this pod.'
else:
    description = ''
