---
name: ovstorage
description: >
  Deploy and develop against NVIDIA Omniverse Storage APIs on any Kubernetes cluster
  (MicroK8s, EKS, AKS, GKE, bare metal). Two storage adapters: (1) Example Storage Adapter —
  Python filesystem reference implementation + Discovery for learning and custom adapter
  development; (2) S3/Azure Production Storage Adapter — NVIDIA pre-built S3/Azure adapter +
  Discovery as minimum, expandable with Event Aggregation, Event Consumer, RabbitMQ,
  Envoy Auth Extension, Storage Navigator, and Contour ingress. Can deploy on the
  developer's behalf (generating scripts + .env) or guide manual deployment. Custom adapter
  development covers three APIs: Storage, Notifications, and Permissions. Use when a
  developer asks about deploying, configuring, validating, troubleshooting, or building
  any component of the Omniverse Storage APIs stack.
argument-hint: "[deployment task or question]"
---

Read `GUIDE.md` from the skill base directory shown above for the full decision tree,
starting points, and composability guide. Load additional reference files from
`references/` in that same base directory only as needed for the user's specific task.

## Workspace

All evaluations, iterations, and benchmarks for this skill are stored in
`storage-apis-workspace/` at the **repository root** (not inside `.claude/skills/`).
When running evals or creating new iterations, always use `storage-apis-workspace/`
as the workspace path.

$ARGUMENTS
