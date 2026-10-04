---
name: argo-cd-read-only
description: Read-only Argo CD Applications and AppProjects via kubectl
activation_keywords: [argocd, argo cd, gitops, application, appproject, argoproj]
execution_mode: server
---

# Argo CD Read Only Skill

Uses `kubectl` against **argoproj.io** CRDs only (read-only):

- `list_apps` — `kubectl get applications.argoproj.io`
- `get_app` / `describe_app` — requires `name`
- `list_projects` — `kubectl get appprojects.argoproj.io`

Default namespace is `argocd`; override with `namespace`. Optional `kubeconfig`.

Tool: `builtin_argocd_readonly`.

Requires `kubectl` and Argo CD CRDs in the target cluster.
