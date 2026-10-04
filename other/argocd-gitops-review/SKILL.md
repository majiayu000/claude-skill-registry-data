---
name: argocd-gitops-review
description: Use this skill for Argo CD GitOps review across Application, AppProject, ApplicationSet, sync windows, RBAC, sync impersonation, and Argo CD Agent multi-cluster topologies. Trigger when the user asks whether an Argo CD configuration is safe for production, whether automated sync should be enabled, whether prune+selfHeal is appropriate, whether AppProject scope is too wide, or how to enforce least-privilege sync identity.
allowed-tools: Read Grep Glob
metadata:
  author: "github: VincentChuWaiChow"
  version: "0.1.0"
  updated: "2026-05-05"
  category: delivery
---

# Argo CD GitOps Review

## Purpose

Review Argo CD `Application`, `AppProject`, `ApplicationSet`, sync windows, RBAC, and the central `argocd-cm` / `argocd-rbac-cm` configuration against blast radius, drift handling, and least-privilege sync identity. Argo CD's controller defaults to cluster-admin permissions on every destination cluster — the security posture lives in `AppProject` boundaries, sync impersonation, and explicit RBAC, not in the controller defaults.

## Lean operating rules

- Prefer live cluster evidence (`kubectl get applications,appprojects,applicationsets -n argocd -o yaml` plus the `argocd-cm` and `argocd-rbac-cm` ConfigMaps) when the active client exposes it; otherwise fall back to official Argo CD documentation and sanitized YAML from the user.
- Separate confirmed facts from inference. If sync history, current health, or RBAC binding state was not queried, say so.
- Treat `application.sync.impersonation.enabled: false` (default) in production as a critical finding — every sync runs as the controller's cluster-admin ServiceAccount.
- Treat `AppProject` with `sourceRepos: ['*']` and `destinations: ['*']` as a wide-blast-radius finding — any commit in any repo can deploy anywhere.
- Treat `automated.prune: true` + `automated.selfHeal: true` on production Applications as critical without an explicit allowlist of authorized Git refs and a tested rollback runbook — Git divergence becomes irreversible deletion.
- Challenge `ApplicationSet` generators that include unbounded clusters (`clusters: {}`) or label selectors with no exclusion — one mis-labeled cluster joins the rollout.
- Challenge `syncOptions: ['Replace=true']` and `syncOptions: ['ServerSideApply=false']` on stateful resources — Replace deletes-then-creates, breaking PVC bindings.
- Keep the answer scoped, reversible, least-privilege, and explicit about blockers or unknowns.

## References

Load these only when needed:

- [Evidence path and tooling](references/mcp-and-evidence.md) — use when choosing live cluster evidence, confirming Argo CD install state and version, or switching to documentation mode.
- [Workflow and output contract](references/workflow-and-output.md) — use when executing the full review, applying stress checks on Application / AppProject / ApplicationSet, or formatting the final answer.
- [Official sources](references/official-sources.md) — use when you need the detailed Argo CD documentation list, RBAC syntax, and grounded insights from the project.

## Response minimum

Return, at minimum:

- the scoped target (`Application`, `AppProject`, `ApplicationSet`, or `argocd-rbac-cm` policy) and evidence level,
- the sync identity (controller default cluster-admin, impersonated ServiceAccount, or `destinationServiceAccount`),
- the blast radius assessment (`sourceRepos`, `destinations`, `clusterResourceWhitelist`, `namespaceResourceBlacklist`),
- the drift handling posture (`automated`, `prune`, `selfHeal`, `syncWindows`),
- the safest next actions and rollback plan,
- the assumptions or blockers that prevent stronger conclusions.
