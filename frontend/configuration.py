import os

# We configure where the API is here
backend_api_url = os.getenv('TIMBER_BACKEND_API_URL', 'http://backend:8080')

# Port the webserver should listen on - defaults to 8080
listen_port = int(os.getenv('TIMBER_LISTEN_PORT', '8080'))
