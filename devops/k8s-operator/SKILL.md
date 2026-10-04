---
name: k8s-operator
description: Kubernetes read-only operations for cluster inspection and monitoring
activation_keywords: [kubernetes, k8s, kubectl, pod, deployment, service, namespace, cluster]
---

# K8s Operator Skill

Provides read-only Kubernetes cluster operations:
- List and describe pods, deployments, services, namespaces
- View pod logs and events
- Check cluster health and resource usage
- Inspect configmaps and secrets (metadata only)

Use `builtin_k8s_operator` tool with fields:
- `operation`: one of "get", "describe", "logs", "events", "top"
- `resource`: Kubernetes resource type (pod, deployment, service, etc.)
- `name`: (optional) specific resource name
- `namespace`: (optional) target namespace (default: all)
- `kubeconfig`: (optional) path to kubeconfig file

Note: Write operations (create, delete, apply, edit) are disabled by default for safety.
