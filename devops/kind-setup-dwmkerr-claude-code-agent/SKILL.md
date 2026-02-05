---
name: Kind Setup
description: Create a Kind cluster in Docker-in-Docker environment
---

# Kind Setup

Create a Kind Kubernetes cluster inside a DinD (Docker-in-Docker) container.

## When to use

- Setting up Kubernetes for testing
- Need a Kind cluster inside this container

## Steps

1. **Verify Docker available**
   ```bash
   docker info
   ```
   If this fails, STOP. DinD is not available.

2. **Delete existing cluster**
   ```bash
   kind delete cluster --name ark-cluster 2>/dev/null || true
   ```

3. **Create cluster**
   ```bash
   kind create cluster --name ark-cluster
   ```

4. **Configure kubeconfig with container IP**
   ```bash
   CONTROL_PLANE_IP=$(docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' ark-cluster-control-plane)
   kind get kubeconfig --name ark-cluster --internal | sed "s/ark-cluster-control-plane/$CONTROL_PLANE_IP/g" > ~/.kube/config
   ```

5. **Verify connection**
   ```bash
   kubectl cluster-info
   ```

## Why the IP replacement?

This container connects to Kind via Docker networking. The default `127.0.0.1` or hostname won't work. Using the container's actual IP ensures connectivity.
