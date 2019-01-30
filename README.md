# Timber - the Training companion app

Hey there! This is Timber.

Timber is a companion app for the  [ContainerSolutions trainings](https://training.container-solutions.com/?utm_source=timber_docs).

Its aim is to provide with engineers attending the trainings with a sample
application they can build upon and play with during the trainings.

It replicates a "traditional web app" setup where there is a frontend, a backend and a database (we'll use Redis).

Functionality is enabled & disabled mostly through environment variables.

Timber is written in Python 3. Fear not! It is, we hope, well-documented and fairly easy to understand.

- [Timber - the Training companion app](#timber---the-training-companion-app)
  - [💻 Running it locally](#%F0%9F%92%BB-running-it-locally)
  - [🚀 Running it on Kubernetes](#%F0%9F%9A%80-running-it-on-kubernetes)
  - [🐉 Backend](#%F0%9F%90%89-backend)
    - [`/api/v1/metadata`](#apiv1metadata)
    - [`/api/v1/configuration`](#apiv1configuration)
    - [`/api/v1/colors`](#apiv1colors)
    - [`/api/v1/redis_detection`](#apiv1redisdetection)
    - [`/api/v1/state`](#apiv1state)
  - [💎 Frontend](#%F0%9F%92%8E-frontend)
    - [`/`](#)
    - [`configuration.py`](#configurationpy)
    - [`backend.py`](#backendpy)

## 💻  Running it locally

Pretty straightforward! - `$ docker-compose up`

Editing any `.py` files will make the application reload with your changes.

## 🚀  Running it on Kubernetes

Some manifests are provided for you in the [`manifests/`](manifests/) folder.

There are different ways to set this up, namely, you could at least:

- Run the backend alone
- Run the backend and the frontend in the same pod
- Run the backend and the frontend in different pods, accessing each other with services
- Run the frontend, backend and redis in different pods, accessing each other with services
- Run the frontend, backend and redis in the same pod

And many more!

## 🐉  Backend

The backend is an API exposing data through HTTP endpoints.

They are all GET endpoints for simplicity.

Some endpoints have a `description` value to pass a human readable sentence to the frontend.

The entrypoint of the API is [`app.py`](backend/app.py).

### [`/api/v1/metadata`](backend/metadata.py)

The metadata is gathered mostly through the [Kubernetes downward API](https://kubernetes.io/docs/tasks/inject-data-application/environment-variable-expose-pod-information/).

These environment variables are read, defaulting to `unknown` if empty:

- `MY_POD_NAME`
- `MY_POD_IP`
- `MY_POD_NAMESPACE`
- `MY_NODE_NAME`

This API returns this data in JSON:
```
{
    description: <...>,
    hostname: <...>,  # container hostname
    ip: <...>,  # IP from the downward API
    namespace: <...>,  # namespace from the downward API
    node: <...>,  # node from the downward API
    pod: <...>  # pod from the downward API
}
```

### [`/api/v1/configuration`](backend/configuration.py)

This API endpoint returns the configuration of Timber.

This is set through environment variables.

| Environment Variable           | What it does      | Default |
|--------------------------------|-------------------|---------|
| `TIMBER_LIVENESS_PROBE_ENABLED`  | Set to any value to enable `/probe/liveness` | Disabled |
| `TIMBER_READINESS_PROBE_ENABLED` | Set to any value to enable `/probe/readiness` | Disabled |
| `TIMBER_VERSION`                 | Currently running application version | v1.0 |
| `TIMBER_REDIS_HOST`              | Redis server used if state is set to `redis` | `redis` |
| `TIMBER_STATE`                   | State storage: `inmemory`, `redis` | `inmemory` |
| `TIMBER_LISTEN_PORT`             | Set the port Timber listens on | 8080 |


```
{
    description: <...>,
    liveness_probe_enabled: <true/false>,
    readiness_probe_enabled: <true/false>,
    redis_host: <...>,
    state: <...>,
    version: <...>
}
```

### [`/api/v1/colors`](backend/colors.py)

This API endpoint returns deterministic hex colors.

Colors are generated based on the values of `TIMBER_VERSION`, `TIMBER_HOSTNAME`, `TIMBER_STATE`.

```
{
    hostname: <...>,
    state: <...>,
    version: <...>
}
```

### [`/api/v1/redis_detection`](backend/redis_detection.py)

This API endpoint tells you whether Redis is detected in the same pod.

It works by trying to connect to Redis on `localhost`, and since pods share networking, this would work if Redis is running alongside the backend.

```
{
    description: <...>,
    is_detected: <true/false>
}
```

### [`/api/v1/state`](backend/state.py)

This API returns informations about the state kept by the backend.

```
{
    type: <inmemory|redis>,
    image_link: <...>  # The picture we are keeping in state
    state_hits: <int>  # Number of times the state has been checked
}
```

## 💎  Frontend

The frontend shows all the data that the backend provides, and some more.

Data from all the backend APIs is used, as well as showing the frontend hostname.

### [`/`](frontend/app.py)

This is the frontend index. It uses [index.html](frontend/index.html) as a template,
and gets the data from the backend API.

### [`configuration.py`](frontend/configuration.py)

Frontend configuration, through environment variables

| Environment Variable           | What it does        | Default              |
|--------------------------------|---------------------|----------------------|
| `TINDER_BACKEND_API_URL`       | Set the backend URL | `http://backend:8080`
| `TINDER_LISTEN_PORT`           | Set the port Timber listens on | 8080 |

### [`backend.py`](frontend/backend.py)

This file contains a `get_api()` helper function to get data as dictionary from the backend API endpoints.
