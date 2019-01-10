# This file is for generating deterministic random colors to show on the index

import random

from configuration import state, version
from metadata import hostname

# Let's define which values we want to create random number generators for
inputs = {
    'version': version,
    'hostname': hostname,
    'state': state,
}

# Let's create a random color for each input
deterministic_colors = {}
for name, value in inputs.items():
    random.seed(value)  # Set the seed to be the hostname, version, ...
    deterministic_colors[name] = "%03x" % random.randint(0, 0xFFFFFF)  # Create the color
