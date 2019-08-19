import os

# If any of these environment variables are set, enable these features
liveness_probe_enabled = bool(os.getenv('TIMBER_LIVENESS_PROBE_ENABLED') is not None)
readiness_probe_enabled = bool(os.getenv('TIMBER_READINESS_PROBE_ENABLED') is not None)

# Port the webserver should listen on - defaults to 8080
listen_port = int(os.getenv('TIMBER_LISTEN_PORT', '8080'))

# Redis host, for keeping state
redis_host = os.getenv('TIMBER_REDIS_HOST', 'redis')

# State
# Should the application keep the state anywhere?
# The state saving is set to `inmemory` by default.
# The possible options are `inmemory`, `storage`, `redis`
state = os.getenv('TIMBER_STATE', 'inmemory')

# Version
# This will be shown on the homepage.
version = os.getenv('TIMBER_VERSION', '1.3')

liveness_probe_text = 'enabled and reachable at `/probe/liveness`'
readiness_probe_text = 'enabled and reachable at `/probe/readiness`'
description = '''Here's the configuration details for Timber right now:
    `TIMBER_LIVENESS_PROBE_ENABLED` - The liveness probe is {liveness_probe}
    `TIMBER_READINESS_PROBE_ENABLED` - The readiness probe is {readiness_probe}
    `TIMBER_STATE` - The state management is set to `{state}`
    `TIMBER_VERSION` - The version is `{version}`.

    You can change all of these through environment variables.
    Take a look at `configuration.py` to see how this works.'''.format(
        # Format it so it doesn't say True or False, but enabled or disabled
        liveness_probe=liveness_probe_text if liveness_probe_enabled else 'disabled',
        readiness_probe=readiness_probe_text if readiness_probe_enabled else 'disabled',
        state=state,
        version=version,
    )
