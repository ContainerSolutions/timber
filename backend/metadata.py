import os
import socket

# We can get the system hostname ourselves
hostname = socket.gethostname()

# We get this information from the Kubernetes downward API
# https://kubernetes.io/docs/tasks/inject-data-application/environment-variable-expose-pod-information/
# Should these environment variables not be set, the default value will be `unknown`.
node = os.getenv('MY_NODE_NAME', 'unknown')
pod = os.getenv('MY_POD_NAME', 'unknown')
namespace = os.getenv('MY_POD_NAMESPACE', 'unknown')
ip = os.getenv('MY_POD_IP', 'unknown')

# We use this in `app.py`, to return on `/`
description = f'''This information comes from the Downward Kubernetes API:
    My pod name is `{pod}`, on node `{node}` in namespace `{namespace}`, with IP `{ip}`.
    Also, my hostname is `{hostname}`, but I knew that without asking the API!
    This code resides in `metadata.py`.
'''
