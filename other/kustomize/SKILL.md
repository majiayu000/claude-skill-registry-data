---
name: kustomize
description: Manage Kustomize overlays and Kubernetes resource customization
activation_keywords: [kustomize, overlay, k8s, kubernetes, patch, resource]
execution_mode: client
---

# Kustomize Skill

Provides Kustomize operations via local CLI:
- List kustomization overlays
- Build kustomization output (rendered YAML)
- List resources in a kustomization
- Show patches and transformers
- Edit kustomization (image tag, namespace, etc.)

Use `builtin_kustomize` tool with fields:
- `operation`: one of "build", "list_resources", "list_overlays", "show_patches", "edit_image", "edit_namespace"
- `path`: path to kustomization directory (default: current directory)
- `overlay`: overlay name (for list_overlays)
- `image`: image name:tag (for edit_image, e.g. "nginx:1.21")
- `name`: resource name (for edit_image)
- `namespace`: namespace name (for edit_namespace)
- `extra_args`: additional kustomize CLI arguments

Note: Requires kustomize CLI installed.
All operations are read-only except edit_image/edit_namespace.
