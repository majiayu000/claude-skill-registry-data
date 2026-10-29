---
name: gcp-gke
description: Deploy and manage Google Kubernetes Engine clusters. Configure node pools, networking, and workload identity. Use when running Kubernetes on GCP. 
category: AI & Agents
source: antigravity
tags: [node, api, ai, agent, template, image, security, docker, kubernetes, gcp]
url: https://github.com/sickn33/antigravity-awesome-skills/tree/main/skills/gcp-gke
---


# Google Kubernetes Engine (GKE)

Deploy, operate, and scale managed Kubernetes clusters on Google Cloud Platform.

## When to Use

- Running containerized microservices at scale with automatic scaling and healing
- Workloads requiring fine-grained orchestration, service mesh, or custom scheduling
- Teams already invested in Kubernetes tooling (Helm, Argo CD, Flux)
- When Cloud Run's request-based model does not fit (long-running, stateful workloads)

## Prerequisites

- Google Cloud SDK (`gcloud`) and `kubectl` installed
- APIs enabled: Kubernetes Engine, Compute Engine
- IAM role `roles/container.admin` for cluster management

```bash
gcloud services enable container.googleapis.com compute.googleapis.com
gcloud components install kubectl
```

## Standard vs Autopilot

| Feature | Standard | Autopilot |
|---------|----------|-----------|
| Node management | You manage node pools | Google manages nodes |
| Pricing | Pay per node (VM) | Pay per pod resource request |
| GPU/TPU | Full support | Supported (with limits) |
| DaemonSets | Allowed | Restricted |
| Best for | Full control, specialized HW | Hands-off, cost-optimized |

## Create a Standard Cluster

```bash
gcloud container clusters create prod-cluster \
  --region=us-central1 --num-nodes=2 \
  --machine-type=e2-standard-4 --disk-size=100 \
  --enable-autoscaling --min-nodes=1 --max-nodes=5 \
  --enable-autorepair --enable-autoupgrade \
  --release-channel=regular \
  --workload-pool=${PROJECT_ID}.svc.id.goog \
  --enable-ip-alias --enable-network-policy \
  --enable-shielded-nodes \
  --logging=SYSTEM,WORKLOAD --monitoring=SYSTEM,WORKLOAD \
  --labels=env=production,team=platform

gcloud container clusters get-credentials prod-cluster --region=us-central1
```

## Create an Autopilot Cluster

```bash
gcloud container clusters create-auto autopilot-prod \
  --region=us-central1 --release-channel=regular \
  --workload-pool=${PROJECT_ID}.svc.id.goog \
  --network=my-vpc --subnetwork=gke-subnet
```

## Node Pools

```bash
# High-memory pool with taint
gcloud container node-pools create highmem-pool \
  --cluster=prod-cluster --region=us-central1 \
  --machine-type=n2-highmem-8 --disk-size=200 --disk-type=pd-ssd \
  --num-nodes=1 --enable-autoscaling --min-nodes=0 --max-nodes=4 \
  --node-labels=workload=memory-intensive \
  --node-taints=dedicated=highmem:NoSchedule

# GPU pool
gcloud container node-pools create gpu-pool \
  --cluster=prod-cluster --region=us-central1 \
  --machine-type=n1-standard-8 \
  --accelerator=type=nvidia-tesla-t4,count=1 \
  --num-nodes=0 --enable-autoscaling --min-nodes=0 --max-nodes=4 \
  --node-taints=nvidia.com/gpu=present:NoSchedule

# Spot pool for batch workloads
gcloud container node-pools create spot-pool \
  --cluster=prod-cluster --region=us-central1 \
  --machine-type=e2-standard-4 --spot \
  --num-nodes=0 --enable-autoscaling --min-nodes=0 --max-nodes=20 \
  --node-taints=cloud.google.com/gke-spot=true:NoSchedule
```

## Workload Identity

```bash
# Create GSA and grant permissions
gcloud iam service-accounts create app-gsa
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
  --member="serviceAccount:app-gsa@${PROJECT_ID}.iam.gserviceaccount.com" \
  --role="roles/storage.objectViewer"

# Create KSA and bind to GSA
kubectl create namespace myapp
kubectl create serviceaccount app-ksa --namespace=myapp
gcloud iam service-accounts add-iam-policy-binding \
  app-gsa@${PROJECT_ID}.iam.gserviceaccount.com \
  --role=roles/iam.workloadIdentityUser \
  --member="serviceAccount:${PROJECT_ID}.svc.id.goog[myapp/app-ksa]"
kubectl annotate serviceaccount app-ksa --namespace=myapp \
  iam.gke.io/gcp-service-account=app-gsa@${PROJECT_ID}.iam.gserviceaccount.com
```

## Deploying Workloads

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-app
  namespace: myapp
spec:
  replicas: 3
  selector:
    matchLabels: { app: web-app }
  template:
    metadata:
      labels: { app: web-app }
    spec:
      serviceAccountName: app-ksa
      containers:
      - name: web
        image: us-central1-docker.pkg.dev/PROJECT_ID/repo/web-app:v1.2.0
        ports: [{ containerPort: 8080 }]
        resources:
          requests: { cpu: 250m, memory: 512Mi }
          limits: { cpu: 500m, memory: 1Gi }
        readinessProbe:
          httpGet: { path: /healthz, port: 8080 }
          initialDelaySeconds: 5
        livenessProbe:
          httpGet: { path: /healthz, port: 8080 }
          initialDelaySeconds: 15
      topologySpreadConstraints:
      - maxSkew: 1
        topologyKey: topology.kubernetes.io/zone
        whenUnsatisfiable: DoNotSchedule
        labelSelector:
          matchLabels: { app: web-app }
---
apiVersion: v1
kind: Service
metadata: { name: web-app, namespace: myapp }
spec:
  selector: { app: web-app }
  ports: [{ port: 80, targetPort: 8080 }]
  type: ClusterIP
```

## Ingress with Managed SSL

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: web-ingress
  namespa
