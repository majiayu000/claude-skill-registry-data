---
name: container-debugging
description: Use for Docker/Kubernetes issues. Inspect runtime state and logs before changing images/manifests.
---

## Workflow

1. Identify the failing component (image, container, pod, service).
2. Check logs and exit codes.
3. Verify env vars, mounts, network, and permissions.
4. Reproduce locally if possible.
5. Apply minimal fix and re-deploy.
