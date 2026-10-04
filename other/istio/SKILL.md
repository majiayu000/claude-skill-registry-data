---
name: istio
description: Inspect Istio service mesh resources and configurations
activation_keywords: [istio, service mesh, virtual service, destination rule, gateway, sidecar]
execution_mode: client
---

# Istio Skill

Provides Istio service mesh inspection via local kubectl:
- List VirtualServices, DestinationRules, Gateways, ServiceEntries
- Describe Istio resources in detail
- Check sidecar injection status
- Get Istio configuration status
- Analyze service mesh traffic routing

Use `builtin_istio` tool with fields:
- `operation`: one of "list_vs", "list_dr", "list_gw", "list_se", "describe", "sidecar_status", "analyze"
- `resource_type`: Istio resource type (vs/dr/gw/se) for describe and analyze
- `name`: resource name (required for describe)
- `namespace`: Kubernetes namespace (default: current context namespace)
- `kubeconfig`: path to kubeconfig file (optional)
- `extra_args`: additional kubectl/istioctl arguments

Note: Requires kubectl CLI installed and configured.
All operations are read-only.
