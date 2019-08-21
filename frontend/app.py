import socket

import configuration
from backend import get_api
from flask import Flask, render_template

app = Flask(__name__, template_folder='.')

### Index page
@app.route('/')
def hello():

    my_hostname = socket.gethostname()

    # Let's fill this dictionary with the data from the API we need
    api_data = {
        key: get_api(key) for key in
        ('metadata', 'colors', 'configuration', 'state', 'redis_detection')
    }

    # Description to return on the index page
    description = [
        f'Hello there! This is the frontend container. My hostname is {my_hostname}',
        'On the other hand, all this information comes from the backend:',
        api_data['redis_detection'].get('description', 'Unable to reach the backend.'),
        api_data['metadata'].get('description', 'Unable to reach the backend.'),
        api_data['configuration'].get('description', 'Unable to reach the backend.'),
    ]

    # Transforming the list into an HTML-worthy text
    description = '\n\n'.join(description)

    # Let's render the template in `index.html` and return it.
    return render_template(
        'index.html',
        description=description,
        hostname=api_data['metadata'].get('hostname'),
        hostname_color=api_data['colors'].get('hostname'),
        version=api_data['configuration'].get('version'),
        version_color=api_data['colors'].get('version'),
        state_image_link=api_data['state'].get('image_link'),
        state_hits=api_data['state'].get('state_hits'),
        state_color=api_data['colors'].get('state'),
    )

app.run(host='0.0.0.0', port=configuration.listen_port, debug=True)
print('Hello, this is frontend!')  # So we can see it in the `kubectl` logs.
