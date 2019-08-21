import traceback

import requests

from configuration import backend_api_url

# We get data from the backend here
# We timeout after 2 seconds in case we cannot get an answer
# We parse the JSON immediately so we can get going with using the data

# Helper function so we don't have to rewrite the same logic everywhere
def get_api(path):
	try:
	    r = requests.get(f'{backend_api_url}/api/v1/{path}', timeout=2)  # Let's get that page!
	    r.raise_for_status()  # In case we hit a 4xx-5xx response status, this will raise an exception.
	    return r.json()  # We parse the JSON so we can readily use it
	except:  # Something went wrong. We have nothing from the API.
		print('We have not been able to reach the backend.')
		print('This is the traceback:')
		traceback.print_exc()
		return {}