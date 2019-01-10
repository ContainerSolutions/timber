from flask import Flask, render_template

import configuration
from backend import get_api

app = Flask(__name__, template_folder='.')

### Index page
@app.route('/')
def hello():
    # Description to return on the index page
    description = [
        'Hello there!',
        'I am a container in a pod!',
        get_api('redis_detection')['description'],
        '\n',
        get_api('metadata')['description'],
        get_api('configuration')['description'],
    ]

    # Transforming the list into an HTML-worthy text
    description = '\n'.join(description)

    # Let's render the template in `index.html` and return it.
    # Each `get_api()` does an HTTP call to the backend.
    return render_template(
        'index.html',
        description=description,
        hostname=get_api('metadata')['hostname'],
        hostname_color=get_api('colors')['hostname'],
        version=get_api('configuration')['version'],
        version_color=get_api('colors')['version'],
        state=get_api('state')['description'],
        state_color=get_api('colors')['state'],
        )

app.run(host='0.0.0.0', port=configuration.listen_port, debug=True)
print('Hello, this is frontend!')  # So we can see it in the `kubectl` logs.
