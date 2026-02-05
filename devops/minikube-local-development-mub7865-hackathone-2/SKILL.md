---
name: minikube-local-development
description: >
  Complete guide for local Kubernetes development with Minikube: installation,
  configuration, image management, addons, networking, and troubleshooting
  for efficient local development workflows.
---

# Minikube Local Development Skill

## When to use this Skill

Use this Skill whenever you are:

- Setting up local Kubernetes development environment.
- Running Kubernetes clusters on your laptop for testing.
- Loading and testing local Docker images in Kubernetes.
- Debugging Kubernetes deployments locally.
- Learning Kubernetes without cloud costs.
- Testing Helm charts before deploying to production.

This Skill works for **any** Minikube project, not just a single repository.

## Core Goals

- Set up **reliable local Kubernetes** environment.
- Efficiently **load and test local Docker images**.
- Use **addons** for enhanced development experience.
- Implement **proper networking** for service access.
- **Troubleshoot common issues** quickly.
- Enable **fast development iteration** cycles.

## What is Minikube?

Minikube is **local Kubernetes** that makes it easy to learn and develop for Kubernetes.

```
Cloud Kubernetes:              Minikube:
┌──────────────────┐          ┌──────────────────┐
│  Cloud Provider  │          │  Your Laptop     │
│  (AWS/GCP/Azure) │          │  (Free!)         │
│  Multiple Nodes  │          │  Single Node     │
│  $100s/month     │          │  $0/month        │
└──────────────────┘          └──────────────────┘
```

**Key Features:**
- Single-node Kubernetes cluster
- Supports multiple drivers (Docker, Hyper-V, VirtualBox)
- Built-in addons (dashboard, ingress, registry)
- Local image loading (no registry needed)
- Cross-platform (Windows, macOS, Linux)

## Installation

### Prerequisites

| Platform | Requirements |
|----------|--------------|
| **Windows** | Docker Desktop or Hyper-V enabled |
| **macOS** | Docker Desktop or HyperKit |
| **Linux** | Docker or KVM |

### Windows Installation

#### Option 1: Using Chocolatey (Recommended)

```powershell
# Install Chocolatey first if not installed
# Then install minikube
choco install minikube

# Verify installation
minikube version
```

#### Option 2: Direct Download

```powershell
# Download installer
# https://minikube.sigs.k8s.io/docs/start/

# Or use winget
winget install Kubernetes.minikube
```

#### Option 3: Using Scoop

```powershell
scoop install minikube
```

### macOS Installation

```bash
# Using Homebrew
brew install minikube

# Verify
minikube version
```

### Linux Installation

```bash
# Download binary
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64

# Install
sudo install minikube-linux-amd64 /usr/local/bin/minikube

# Verify
minikube version
```

### Install kubectl

kubectl is required to interact with Kubernetes.

```bash
# Windows (Chocolatey)
choco install kubernetes-cli

# macOS
brew install kubectl

# Linux
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install kubectl /usr/local/bin/kubectl

# Verify
kubectl version --client
```

## Drivers

Minikube supports multiple drivers for running the cluster.

### Available Drivers

| Driver | Platform | Description |
|--------|----------|-------------|
| **docker** | All | Uses Docker containers (recommended) |
| **hyperv** | Windows | Uses Hyper-V VMs |
| **virtualbox** | All | Uses VirtualBox VMs |
| **kvm2** | Linux | Uses KVM VMs |
| **hyperkit** | macOS | Uses HyperKit VMs |
| **podman** | All | Uses Podman containers |

### Setting Default Driver

```bash
# Set Docker as default (recommended)
minikube config set driver docker

# View current config
minikube config view

# Or specify at start time
minikube start --driver=docker
```

### Docker Driver (Recommended)

```bash
# Requires Docker Desktop running
minikube start --driver=docker
```

**Advantages:**
- Fastest startup time
- Works on all platforms
- Easy image loading
- Lower resource usage

### Hyper-V Driver (Windows)

```bash
# Requires Hyper-V enabled
minikube start --driver=hyperv

# With specific virtual switch
minikube start --driver=hyperv --hyperv-virtual-switch="Minikube Switch"
```

## Starting & Managing Cluster

### Start Cluster

```bash
# Basic start (uses default driver)
minikube start

# With specific driver
minikube start --driver=docker

# With custom resources
minikube start --cpus=4 --memory=8192 --disk-size=50g

# With specific Kubernetes version
minikube start --kubernetes-version=v1.28.0

# With multiple addons enabled
minikube start --addons=dashboard,ingress,metrics-server
```

### Check Status

```bash
# Cluster status
minikube status

# Expected output:
# minikube
# type: Control Plane
# host: Running
# kubelet: Running
# apiserver: Running
# kubeconfig: Configured

# Get cluster IP
minikube ip

# Get Kubernetes version
kubectl version
```

### Stop & Delete

```bash
# Stop cluster (preserves state)
minikube stop

# Delete cluster (removes everything)
minikube delete

# Delete all clusters and profiles
minikube delete --all

# Pause cluster (save resources)
minikube pause

# Unpause cluster
minikube unpause
```

### Resource Management

```bash
# View current config
minikube config view

# Set default CPUs
minikube config set cpus 4

# Set default memory (MB)
minikube config set memory 8192

# Set default disk size
minikube config set disk-size 50g

# Apply changes (requires restart)
minikube stop
minikube start
```

## Loading Docker Images

Minikube has its own Docker registry. Local images must be loaded into Minikube.

### Method 1: Use Minikube's Docker Daemon (Recommended)

```bash
# Point shell to Minikube's Docker
eval $(minikube docker-env)

# Now build directly in Minikube
docker build -t my-app:v1 .

# Verify image is in Minikube
docker images | grep my-app

# Reset to local Docker (when done)
eval $(minikube docker-env -u)
```

**Note:** For PowerShell on Windows:
```powershell
& minikube docker-env | Invoke-Expression
```

### Method 2: Load Pre-built Images

```bash
# Build locally first
docker build -t my-app:v1 .

# Load into Minikube
minikube image load my-app:v1

# Verify
minikube image ls | grep my-app
```

### Method 3: Build Directly in Minikube

```bash
# Build inside Minikube
minikube image build -t my-app:v1 .

# Or with specific Dockerfile
minikube image build -t my-app:v1 -f Dockerfile.prod .
```

### Image Commands

```bash
# List images in Minikube
minikube image ls

# Load image
minikube image load my-app:v1

# Remove image
minikube image rm my-app:v1

# Pull image from registry
minikube image pull nginx:latest
```

### Important: ImagePullPolicy

When using local images, set `imagePullPolicy` to prevent Kubernetes from trying to pull from remote registry.

```yaml
spec:
  containers:
  - name: my-app
    image: my-app:v1
    imagePullPolicy: Never  # or IfNotPresent
```

| Policy | Description | Use Case |
|--------|-------------|----------|
| `Never` | Never pull from registry | Local images only |
| `IfNotPresent` | Pull only if not local | Local first, then registry |
| `Always` | Always pull (default for :latest) | Always use registry |

## Accessing Services

### Method 1: minikube service (Easiest)

```bash
# Opens service in browser
minikube service my-service

# Get URL only
minikube service my-service --url

# With namespace
minikube service my-service -n my-namespace
```

### Method 2: kubectl port-forward

```bash
# Forward pod port
kubectl port-forward pod/my-pod 8080:80

# Forward service port
kubectl port-forward svc/my-service 8080:80

# Forward with specific address
kubectl port-forward svc/my-service 8080:80 --address='0.0.0.0'
```

### Method 3: NodePort Service

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-service
spec:
  type: NodePort
  selector:
    app: my-app
  ports:
  - port: 80
    targetPort: 80
    nodePort: 30000  # Fixed port 30000-32767
```

Access at: `http://$(minikube ip):30000`

### Method 4: minikube tunnel (LoadBalancer)

```bash
# Start tunnel (run in separate terminal)
minikube tunnel

# Now LoadBalancer services get external IPs
kubectl get svc
# NAME         TYPE           EXTERNAL-IP    PORT(S)
# my-service   LoadBalancer   127.0.0.1      80:31234/TCP
```

## Addons

Addons extend Minikube functionality.

### List & Manage Addons

```bash
# List all addons
minikube addons list

# Enable addon
minikube addons enable dashboard

# Disable addon
minikube addons disable dashboard

# Enable at start
minikube start --addons=dashboard,ingress
```

### Essential Addons

| Addon | Description | Command |
|-------|-------------|---------|
| **dashboard** | Web UI for Kubernetes | `minikube addons enable dashboard` |
| **ingress** | NGINX Ingress controller | `minikube addons enable ingress` |
| **metrics-server** | Resource metrics | `minikube addons enable metrics-server` |
| **registry** | Local Docker registry | `minikube addons enable registry` |
| **storage-provisioner** | Dynamic storage | Enabled by default |

### Dashboard

```bash
# Enable dashboard
minikube addons enable dashboard

# Open dashboard in browser
minikube dashboard

# Get dashboard URL only
minikube dashboard --url
```

### Ingress

```bash
# Enable ingress addon
minikube addons enable ingress

# Verify ingress controller is running
kubectl get pods -n ingress-nginx
```

Example Ingress:
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: my-ingress
spec:
  rules:
  - host: my-app.local
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: my-service
            port:
              number: 80
```

Add to hosts file:
```
# /etc/hosts (Linux/macOS) or C:\Windows\System32\drivers\etc\hosts (Windows)
192.168.49.2  my-app.local  # Use your minikube ip
```

### Metrics Server

```bash
# Enable metrics server
minikube addons enable metrics-server

# Now you can use:
kubectl top nodes
kubectl top pods
```

## Multi-Node Clusters

Minikube can create multi-node clusters for testing.

```bash
# Start with 3 nodes
minikube start --nodes 3

# Add node to existing cluster
minikube node add

# List nodes
kubectl get nodes

# Delete specific node
minikube node delete minikube-m02
```

## Profiles

Profiles allow multiple Minikube clusters.

```bash
# Create new profile
minikube start -p dev-cluster

# List profiles
minikube profile list

# Switch profile
minikube profile dev-cluster

# Delete profile
minikube delete -p dev-cluster
```

## SSH Access

```bash
# SSH into Minikube VM
minikube ssh

# Run command via SSH
minikube ssh -- ls -la /

# SSH to specific node (multi-node)
minikube ssh -n minikube-m02
```

## Logs & Debugging

### View Logs

```bash
# Minikube logs
minikube logs

# Follow logs
minikube logs -f

# Logs for specific node
minikube logs -n minikube-m02

# Verbose startup
minikube start --alsologtostderr -v=2
```

### Kubernetes Logs

```bash
# Pod logs
kubectl logs my-pod

# Follow logs
kubectl logs -f my-pod

# Previous container logs
kubectl logs my-pod --previous

# Logs from all pods with label
kubectl logs -l app=my-app
```

### Describe Resources

```bash
# Describe pod (shows events)
kubectl describe pod my-pod

# Describe service
kubectl describe service my-service

# Describe node
kubectl describe node minikube
```

## Troubleshooting

### Common Issues & Solutions

#### 1. Minikube Won't Start

```bash
# Delete and recreate
minikube delete
minikube start

# Try different driver
minikube start --driver=docker

# Check Docker is running
docker info
```

#### 2. ImagePullBackOff Error

**Cause:** Image not found in Minikube

**Solution:**
```bash
# Load image into Minikube
minikube image load my-app:v1

# Set imagePullPolicy to Never
# In deployment.yaml:
imagePullPolicy: Never
```

#### 3. Insufficient Resources

```bash
# Allocate more resources
minikube stop
minikube start --cpus=4 --memory=8192

# Or permanently set
minikube config set cpus 4
minikube config set memory 8192
```

#### 4. kubectl Connection Refused

```bash
# Check cluster status
minikube status

# Update kubeconfig
minikube update-context

# Or set context manually
kubectl config use-context minikube
```

#### 5. Service Not Accessible

```bash
# Use minikube service
minikube service my-service

# Or start tunnel
minikube tunnel
```

#### 6. DNS Issues

```bash
# Check CoreDNS pods
kubectl get pods -n kube-system | grep coredns

# Restart CoreDNS
kubectl rollout restart deployment coredns -n kube-system
```

#### 7. Clean Start

```bash
# Complete reset
minikube delete --all --purge
rm -rf ~/.minikube
minikube start
```

### Diagnostic Commands

```bash
# Full status check
minikube status

# System info
minikube ssh -- cat /etc/os-release

# Disk usage
minikube ssh -- df -h

# Memory usage
minikube ssh -- free -m

# Kubernetes component status
kubectl get componentstatuses

# All pods in all namespaces
kubectl get pods -A
```

## Development Workflow

### Recommended Workflow

```bash
# 1. Start Minikube
minikube start --driver=docker

# 2. Point to Minikube Docker
eval $(minikube docker-env)

# 3. Build images
docker build -t my-backend:v1 ./backend
docker build -t my-frontend:v1 ./frontend

# 4. Deploy
kubectl apply -f k8s/

# 5. Access service
minikube service frontend-service

# 6. View logs if needed
kubectl logs -l app=backend

# 7. Make changes, rebuild, redeploy
docker build -t my-backend:v1 ./backend
kubectl rollout restart deployment/backend

# 8. When done
minikube stop
```

### Fast Iteration Cycle

```bash
# Build and deploy in one command
docker build -t my-app:dev . && kubectl rollout restart deployment/my-app

# Or create a script: dev.sh
#!/bin/bash
eval $(minikube docker-env)
docker build -t $1:dev ./$1
kubectl rollout restart deployment/$1
echo "Deployed $1"
```

## Complete Example: Deploy Full-Stack App

### Step 1: Start Minikube

```bash
minikube start --driver=docker --cpus=4 --memory=4096
```

### Step 2: Build Images

```bash
eval $(minikube docker-env)

cd phase2/backend
docker build -t todo-backend:v1 .

cd ../frontend
docker build -t todo-frontend:v1 .
```

### Step 3: Create Namespace

```bash
kubectl create namespace todo-app
```

### Step 4: Deploy

```bash
kubectl apply -f k8s/ -n todo-app
```

### Step 5: Verify

```bash
kubectl get all -n todo-app
```

### Step 6: Access

```bash
minikube service frontend-service -n todo-app
```

## Best Practices

### Do

- Use Docker driver for fastest startup.
- Set `imagePullPolicy: Never` for local images.
- Use `eval $(minikube docker-env)` for direct builds.
- Enable metrics-server for resource monitoring.
- Use namespaces to organize deployments.
- Stop Minikube when not in use (save resources).

### Don't

- Don't use `:latest` tag with local images.
- Don't forget to load images into Minikube.
- Don't ignore resource limits in deployments.
- Don't leave tunnel running when not needed.
- Don't use excessive resources for simple tests.

## References

- [Minikube Official Documentation](https://minikube.sigs.k8s.io/docs/)
- [Minikube Start Guide](https://minikube.sigs.k8s.io/docs/start/)
- [Pushing Images to Minikube](https://minikube.sigs.k8s.io/docs/handbook/pushing/)
- [Minikube Addons](https://minikube.sigs.k8s.io/docs/handbook/addons/)
- [Troubleshooting Guide](https://minikube.sigs.k8s.io/docs/handbook/troubleshooting/)
- [Hello Minikube Tutorial](https://kubernetes.io/docs/tutorials/hello-minikube/)
