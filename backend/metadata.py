import os
import socket

# We can get the system hostname ourselves
hostname = socket.gethostname()

# We get this information from the Kubernetes downward API
# https://kubernetes.io/docs/tasks/inject-data-application/environment-variable-expose-pod-information/
# Should these environment variables not be set, the default value will be `unknown`.
pod = os.getenv('MY_POD_NAME', 'unknown')
ip = os.getenv('MY_POD_IP', 'unknown')
namespace = os.getenv('MY_POD_NAMESPACE', 'unknown')
node = os.getenv('MY_NODE_NAME', 'unknown')

# We use this in `app.py`, to return on `/`
description = f'''Downward Kubernetes API:

Pod name is `{pod}`
Node is `{node}`
Namespace is `{namespace}`
IP is `{ip}`
'''
