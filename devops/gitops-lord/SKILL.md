---
name: gitops-lord
description: Lord skill for GitOps continuous delivery — ArgoCD 3.5, Helm 4, Flux, Argo Rollouts, progressive delivery, and multi-cluster management.
triggers:
  - gitops lord
  - gitops
  - argocd
  - helm
  - flux
  - progressive delivery
  - argo rollouts
  - gitops sync
  - multi cluster
  - جيت اوبس
personas:
  - DEVOPS
  - SRE
  - ARCH
  - SEC
tech_stack:
  - kubernetes-1-36
  - helm-4
  - argocd-3
lord: true

---

# GitOps Lord

[OBJ] Implement GitOps continuous delivery for Kubernetes using ArgoCD 3.5, Helm 4, and progressive delivery patterns.

## Problem

Manual `kubectl apply` causes drift, lacks audit trail, and prevents rollback. GitOps makes Git the single source of truth — every deployment is a commit, every change is reviewable, every rollback is `git revert`. ArgoCD 3.5 (Aug 2026) adds impersonation, Source Hydrator, and ApplicationSet preview apps.

## Rules

1. [REQ] **Git is the single source of truth.** All manifests (Helm charts, Kustomize, raw YAML) live in Git. No `kubectl apply` outside of emergency break-glass procedures.
2. [REQ] **Use ArgoCD 3.5+ `ApplicationSet`** for multi-environment deployments. Matrix generators (git × cluster) auto-generate apps per environment. Avoid manual `Application` creation.
3. [REQ] **Use Helm 4 charts** (v3 is maintenance mode). `helm template` in CI for validation, `helm install --dry-run` before deploy. Never `helm install` without `--atomic --timeout 5m`.
4. [REQ] **Use Kustomize for environment overlays.** `base/` + `overlays/dev|staging|prod/`. Patch images, replicas, env vars per environment. Avoid duplicating manifests.
5. [REQ] **Enable `selfHeal: true`** on production apps. Manual `kubectl edit` causes drift — ArgoCD auto-reverts to Git state.
6. [REQ] **Enable `prune: true`** to remove resources deleted from Git. Without prune, deleted manifests leave orphaned resources.
7. [REQ] **Use ArgoCD impersonation (beta)** for RBAC. Service accounts per team, least-privilege `AppProject` restrictions (repos, clusters, namespaces).
8. [REQ] **Use Source Hydrator (beta)** for dry-source integrity verification. Validates manifests before sync, prevents malicious PRs from deploying.
9. [REQ] **Use Argo Rollouts** for progressive delivery. Canary (5% → 25% → 50% → 100%) or Blue-Green. Auto-rollback on SLO violation (error rate, latency).
10. [REQ] **Use `syncPolicy.automated`** for non-prod, **manual sync** for prod. Prod requires explicit `argocd app sync` after PR merge + review.
11. [REQ] **Use `argocd app diff`** before sync to review changes. Use `argocd app sync --dry-run` to validate.
12. [REQ] **Secrets management.** Use Sealed Secrets, External Secrets Operator, or SOPS — never commit plaintext secrets to Git. External Secrets syncs from Vault/AWS Secrets Manager.
13. [REQ] **Multi-cluster via ArgoCD.** Register clusters with `argocd cluster add`. Use `destinations` in ApplicationSet for cluster routing. Single ArgoCD instance manages multiple clusters.
14. [REQ] **Use `AppProject` for isolation.** Each team gets an `AppProject` with restricted `sourceRepos`, `destinations` (namespaces), and `clusterResourceWhitelist`.
15. [PROHIBIT] Never disable `selfHeal` in production — manual edits cause drift.
16. [PROHIBIT] Never use `--force` sync without understanding — deletes and recreates resources (downtime).
17. [PROHIBIT] Never store secrets in Git plaintext — use Sealed Secrets or External Secrets Operator.

## Commands

- `argocd app create <name> --repo <url> --path <path> --dest-server https://kubernetes.default.svc --dest-namespace <ns>`
- `argocd app sync <name> --dry-run` — validate before sync
- `argocd app diff <name>` — compare live vs desired
- `argocd app rollback <name> <revision>` — rollback to previous
- `argocd cluster add <context>` — register cluster
- `argocd proj create <name> --src <repo> --dest <ns>` — create project
- `helm template <chart> -f values.yaml | kubectl apply --dry-run=server -f -`
- `helm upgrade --install <name> <chart> --atomic --timeout 5m`

## References

- https://argo-cd.readthedocs.io/en/release-3.5/
- https://helm.sh/docs/
- https://argoproj.github.io/rollouts/
- https://github.com/argoproj/argo-cd/releases/tag/v3.5.2
