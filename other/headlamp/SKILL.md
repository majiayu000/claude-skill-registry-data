---
name: headlamp
description: >
  Kubernetes Web UI with AI Plugins: Dynamic Official and Custom Plugins,
  in-cluster admin authentication, HolmesGPT integration, and Gateway API routing.
license: MIT
compatibility:
  - opencode
metadata:
  author: dotfiles
  tags: [kubernetes, headlamp, UI, holmesgpt, litellm, cluster-admin, plugins]
---

# Headlamp Kubernetes UI Skill

Headlamp is deployed in-cluster in the `headlamp` namespace and acts as the premium, unified control plane UI for both Kubernetes administrators and AI assistants.

## Deployment Details

- **Namespace**: `headlamp`
- **Port**: `80` (ClusterIP mapped via Gateway HTTPRoute to `headlamp.cluster.home`)
- **Gateway Domain**: `http://headlamp.cluster.home` and `https://headlamp.cluster.home` (routes work on both HTTP and HTTPS listeners).

## Authentication

Headlamp is deployed with a pre-configured `cluster-admin` ServiceAccount. To log in:

1. Retrieve the permanent login token:
   ```bash
   kubectl get secret headlamp-admin-token -n headlamp -o jsonpath='{.data.token}' | base64 -d
   ```
2. Paste this token into the Headlamp Login screen.

## AI Plugins Integration

Headlamp dynamically loads two AI-focused plugins in its pod lifecycle using a custom `initContainer` pipeline:

1. **Official `ai-assistant` Plugin**:
   - Downloads from Headlamp’s GitHub releases.
   - Automatically patched during deployment (`sed` in initContainer) to target the `ai` namespace (where HolmesGPT runs) instead of `default`.
2. **Custom `headlamp-holmes` Plugin**:
   - Compiled from React/TypeScript.
   - Mounted as a ConfigMap into the pod.
   - Configured dynamically via Ansible variables to point to our in-cluster LiteLLM proxy and route to local models (e.g. `rk1-npu-local` or fallback tiers).

## Useful Commands

```bash
# Deploy Headlamp stack
make headlamp

# Verify resources
kubectl get deploy,pods,svc,httproute -n headlamp

# Fetch setup logs (plugin downloads, config patching)
kubectl logs -n headlamp deploy/headlamp -c setup-plugins

# Fetch server logs
kubectl logs -n headlamp deploy/headlamp -c headlamp
```
