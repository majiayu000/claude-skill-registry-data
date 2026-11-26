---
name: devops-lord
always: true
description: End-to-end authority on containers, Kubernetes, Podman, Helm, Terraform, Pulumi, Ansible, CI/CD, GitOps, observability.
triggers:
  - devops lord
  - devops
  - containers

---
[SKILL] devops-lord
[OBJ] Design, build, and operate delivery pipelines and runtime platforms.
[RULES]
1. [CMD] IDs: Docker `/docker/docs`, Kubernetes `/kubernetes/website`, Podman `/websites/podman_io_en`, Helm `/helm/helm-www`, Terraform `/websites/developer_hashicorp_terraform`, Pulumi `/pulumi/docs`, Ansible `/websites/ansible_projects_ansible`.
2. [REQ] Pillar coverage: images/layers/registries, runtimes (Docker/Podman rootless), orchestration, packaging (Helm/OCI), IaC (Terraform/Pulumi), config-mgmt (Ansible), CI/CD/GitOps, observability/reliability, security/cost.
3. [REQ] Query relevant ID with full question + topic (Dockerfile, kubernetes, helm, terraform, ansible).
4. [REQ] Compare tools by concrete differences: daemon vs rootless, state backend, language support.
5. [REQ] Prefer current docs; container/K8s APIs change fast.
6. [REQ] Images: multi-stage builds, minimal/distroless bases, non-root USER, .dockerignore, pinned digests, SBOM + Cosign sign, scan in CI (Trivy/Grype). Never ship `:latest` to prod.
7. [REQ] Kubernetes production baseline: resource requests AND limits (requests=reservation, limits=safety net), liveness ≠ readiness probes (crash-loop risk if conflated), PodDisruptionBudgets, NetworkPolicy default-deny, namespaces as tenancy boundaries, Helm/Kustomize for packaging — no raw kubectl-apply snowflakes.
8. [REQ] Workload placement: Deployments for stateless, StatefulSets for identity/storage-bound, DaemonSets for node agents, Jobs/CronJobs for batch. HPA on real metrics (CPU only as fallback); VPA recommendations reviewed not auto-applied.
9. [REQ] IaC doctrine: state remote + locked + versioned; modules for repeated patterns with versioned releases; `plan` output is the PR description; drift detection scheduled; secrets NEVER in state-visible values (use data sources/refs).
10. [REQ] GitOps: cluster desired state in git (ArgoCD/Flux), app-of-apps for multi-env, image updaters or CI-driven manifest PRs, sync waves + health gates for ordering, drift = alert not manual fix.
11. [REQ] Config management (Ansible): idempotent plays (check mode clean), roles for reuse, vault for secrets, immutable infra preferred over long-lived managed hosts where possible.
12. [REQ] Pipeline supply chain: OIDC keyless cloud auth, pinned action SHAs, artifact provenance (SLSA), deploy only scanned+signed artifacts, environment protection rules + approvals for prod.
13. [REQ] Observability stack: Prometheus + Grafana (or cloud-native), Loki/ELK for logs, OTel traces; alerts on symptoms/SLOs; every service ships with health endpoints + dashboards.
14. [REQ] Cost: requests right-sized from actual usage (not guesses), spot/preemptible for interruptible work, autoscaling both directions, cluster/storage sprawl cleaned on schedule.
15. [PROHIBIT] Privileged containers without justification, hostPath mounts on multi-tenant clusters, `apply -f` against prod without review, secrets in ConfigMaps/env literals, or IaC applied outside the pipeline.
