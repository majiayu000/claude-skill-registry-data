---
name: helm
description: Manage Helm charts and releases on Kubernetes
activation_keywords: [helm, chart, release, kubernetes, k8s, deployment]
execution_mode: client
---

# Helm Skill

Provides Helm chart and release management via local Helm CLI:
- List, search, and inspect Helm repositories and charts
- List releases, check release status and history
- Get release values and notes
- Install, upgrade, rollback, and uninstall releases

Use `builtin_helm` tool with fields:
- `operation`: one of "list_repos", "search", "list_releases", "status", "history", "get_values", "install", "upgrade", "rollback", "uninstall"
- `release`: release name (required for status/history/get_values/install/upgrade/rollback/uninstall)
- `chart`: chart reference (required for install/upgrade/search)
- `namespace`: Kubernetes namespace (default: "default")
- `repo`: Helm repo name (for search)
- `revision`: revision number (for rollback)
- `values`: YAML values content (for install/upgrade)
- `extra_args`: additional Helm CLI arguments

Note: Requires Helm CLI (helm) installed on the client machine.
Write operations (install/upgrade/rollback/uninstall) require user confirmation.
