---
name: kubernetes
description: Deployments, services, configmaps, secrets, and charts.
---

# Kubernetes

Deployments, services, configmaps, secrets, and charts.

## Core Guidelines

- **Resource Constraints**: Define CPU/Memory requests and limits on all container specs.
- **Config Management**: Store configuration parameters in ConfigMaps and sensitive keys in Secrets.
- **Probes**: Implement startup, liveness, and readiness probes on services.
