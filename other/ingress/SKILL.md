---
name: ingress
description: Diagnose Kubernetes Ingress resources and configurations
activation_keywords: [ingress, nginx, kubernetes, k8s, ingress controller, tls, route]
execution_mode: client
---

# Ingress Skill

Provides Kubernetes Ingress diagnostics via local kubectl:
- List all Ingress resources across namespaces
- Describe Ingress details (rules, TLS, annotations)
- Check Ingress controller status
- Verify Ingress endpoints and services
- Check TLS certificate details from Ingress

Use `builtin_ingress` tool with fields:
- `operation`: one of "list", "describe", "controller_status", "check_endpoints", "check_tls"
- `name`: Ingress resource name (required for describe/check_endpoints/check_tls)
- `namespace`: Kubernetes namespace (default: current context namespace)
- `kubeconfig`: path to kubeconfig file (optional)
- `extra_args`: additional kubectl arguments

Note: Requires kubectl CLI installed and configured.
All operations are read-only.
