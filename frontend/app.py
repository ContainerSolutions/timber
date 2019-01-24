import socket

import configuration
from backend import get_api
from flask import Flask, render_template

app = Flask(__name__, template_folder='.')

### Index page
@app.route('/')
def hello():

    my_hostname = socket.gethostname()
    # Description to return on the index page
    description = [
        f'Hello there! This is the frontend container. My hostname is {my_hostname}',
        'On the other hand, all this information comes from the backend:',
        get_api('redis_detection')['description'],
        get_api('metadata')['description'],
        get_api('configuration')['description'],
    ]

    # Transforming the list into an HTML-worthy text
    description = '\n\n'.join(description)

    # Let's render the template in `index.html` and return it.
    # Each `get_api()` does an HTTP call to the backend.

    # We do it separately so we call it only once
    state = get_api('state')

    return render_template(
        'index.html',
        description=description,
        hostname=get_api('metadata')['hostname'],
        hostname_color=get_api('colors')['hostname'],
        version=get_api('configuration')['version'],
        version_color=get_api('colors')['version'],
        state_image_link=state['image_link'],
        state_hits=state['state_hits'],
        state_color=get_api('colors')['state'],
    )

app.run(host='0.0.0.0', port=configuration.listen_port, debug=True)
print('Hello, this is frontend!')  # So we can see it in the `kubectl` logs.
