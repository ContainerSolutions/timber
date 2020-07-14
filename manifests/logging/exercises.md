---
title: Cloud Native Logging Essentials
revealOptions:
    transition: 'none'
    slideNumber: 'true'
---

# Cloud Native Logging Essentials - Exercises

---

## Outline

1. Inspecting logs with `kubectl logs`

2. Centralized Log Aggregation with Fluentd, Elasticsearch and Kibana


---


## 1. Inspecting logs with `kubectl logs`


---


### Outline


* We will deploy a pod, deployment and service

* Inspect the logs

* Make changes and inspect the logs again


---


### Preparation

* Go to `manifests/logging`

* This directory contains this slide deck

* The directory also contains code, k8s manifests and a `Dockerfile`

* Edit `deployment.yaml` and replace the string `$YOUR_USERNAME` with your VM username

---


### Build the image


```
gcloud docker -- build -t eu.gcr.io/$YOUR_USERNAME/server -f Dockerfile .
```


---


### Push the image

```
gcloud docker -- push eu.gcr.io/$YOUR_USERNAME/server
```


---


###  Create a deployment


```
kubectl create -f deployment.yaml
```


---


### Check the logs

```
kubectl logs $POD_NAME
```

If the pod's `STATUS` is `ContainerCreating` you won't see logs yet

---


### Change the code

* Add **`console.log(request)`** to **`server.js`** inside the request loop

* Hack, hack


---


### Delete the deployment


```
kubectl delete deployment server
```


---


### Build & push again

```
gcloud docker -- build -t eu.gcr.io/$YOUR_USERNAME/server -f Dockerfile .
```

```
gcloud docker -- push eu.gcr.io/$YOUR_USERNAME/server
```

---


### Now deploy the deployment again


```
kubectl create -f deployment.yaml
```


---


### Now follow the logs


```
kubectl logs -f $POD_NAME
```


---

### Enable port forwarding

* SSH into the VM with another session

* Port forwarding in the background

```
kubectl port-forward $POD_NAME 8080:8080 &
```


---


### Hit the server with curl

```
curl localhost:8080
```

---


### Now check the logs in the other terminal


---


## 2. Centralized Log Aggregation 

#### with **Fluentd**, **Elasticsearch** and **Kibana**


---


### Outline


* In this exercise you will install Fluentd, Elasticsearch and Kibana

* Then you can experiment with the setup and search logs in Kibana


---

### Deploy Fluentd

* We will create a namespace for our logging deployment

```
kubectl create -f namespace.yaml
``` 
 
* We will deploy Fluentd with Elasticsearch config

```
kubectl create -f fluentd.yaml
```

* Check that it is running

```
kubectl --namespace=kube-logging get ds
```


---


### Deploy Elasticsearch

* Deploy the StatefulSet and Service

```
kubectl create -f elasticsearch.yaml
```

* Check if it is up
  
```
kubectl --namespace=kube-logging get pods
```  

---

### Deploy Kibana

* Deploy the Deployment and Service

```
kubectl create -f kibana.yaml
```

* Check if it is up
  
```
kubectl --namespace=kube-logging get pods
```  


### Login into Kibana and setup index

```
kubectl port-forward --namespace=kube-logging $KIBANA_POD_NAME 5601:5601
```
* Navigate to http://localhost:5601 to access Kibana

* You will need to add the elasticsearch index into kibana in order to view your application logs

* Navigate to http://localhost:5601/app/kibana#/management?_g=()
* ->  index patterns >  create index pattern (step 1: fill in  '*' , step 2 : select '@timestamp' )


---


### Check node server logs and experiment!

* Now deploy pods from the previous exercise or your own app

* Hit the server you deployed to generate some logs

* Navigate to the dashboard http://localhost:5601/app/kibana#/discover?_g=()

* Find your server logs
    ```kubernetes.container_name: $SERVER_NAME```

* Kibana Docs https://www.elastic.co/guide/en/kibana/current/index.html

* Experiment with the queries