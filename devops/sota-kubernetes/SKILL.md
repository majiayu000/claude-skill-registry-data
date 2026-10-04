---
name: sota-kubernetes
description: >-
  State-of-the-art Kubernetes platform security and operations (2026) for
  cloud-managed (EKS/GKE/AKS) and self-hosted clusters (kubeadm, k3s/k0s,
  Talos). Use when building, operating, hardening, or auditing the cluster
  PLATFORM layer: control plane and etcd, API server/kubelet, RBAC, admission
  control and policy-as-code, GitOps controllers, operators/CRDs/admission
  webhooks, Helm/Kustomize supply chain, multi-tenancy, cluster
  lifecycle/upgrades/CVE response, and audit logging. Trigger keywords:
  Kubernetes, k8s, cluster, control plane, etcd, kube-apiserver, kubelet,
  RBAC, ClusterRole, ServiceAccount, admission controller, Pod Security
  Admission, PSA, Kyverno, Gatekeeper, OPA, ValidatingAdmissionPolicy, Argo
  CD, Flux, GitOps, operator, CRD, admission webhook, Helm, Kustomize,
  multi-tenancy, vCluster, Talos, k3s, k0s, kubeadm, EKS, GKE, AKS, CIS
  benchmark, kube-bench, audit log, version skew. NOT pod-level
  securityContext/seccomp (sota-sandboxing) or NetworkPolicy/CNI depth
  (sota-network-security).
---

# SOTA Kubernetes Platform Security & Operations

## Purpose

Engineer and audit the Kubernetes **platform** so that a compromised workload, a
hostile chart, a leaked token, or a malicious controller cannot pivot to cluster-admin,
read every Secret, or take the cluster down. This skill owns the layer above the pod:
control plane and etcd, API server and kubelet hardening, RBAC and ServiceAccount
identity, admission control and policy-as-code, GitOps controllers, operators/CRDs and
admission webhooks, Helm/Kustomize at admission, multi-tenancy boundaries, cluster
lifecycle, and K8s audit logging.

It does **not** re-teach pod isolation mechanics. Boundaries it defers:
- **Pod `securityContext`, seccomp, AppArmor, capabilities, PSA pod-level fields** → `sota-sandboxing` (rules/03 containers & microVMs; rules/01 boundaries). This skill owns the *admission-time enforcement* of those fields, not their internals.
- **NetworkPolicy semantics, CNI choice, service mesh, mTLS** → `sota-network-security`. This skill states only the *requirement* (default-deny per namespace, enforced at admission).
- **OIDC/SSO and RBAC-role *design* methodology** → `sota-identity-access`. This skill owns the K8s RBAC *mechanics and escalation traps*.
- **Runtime/audit-log detection content (Falco/Tetragon rules, detections)** → `sota-detection-engineering`. This skill owns *producing and shipping* the audit stream.
- **Workload identity, Secret storage backends (ESO, sealed-secrets, CSI)** → `sota-secrets-management` (rules/01, rules/02). This skill owns etcd encryption-at-rest.
- **Cloud IAM, managed-K8s selection, DR** → `sota-cloud-infrastructure` (rules/02, rules/04, rules/07).
- **CI/CD provenance, image signing, IaC/GitOps pipeline, runtime ops** → `sota-devsecops` (rules/02, rules/04, rules/06, rules/07).

Two modes. Pick one explicitly at the start of the task.

---

## BUILD mode

Use when provisioning a cluster, writing RBAC/policies/manifests, configuring a GitOps
controller, or installing an operator/chart.

1. **Name the cluster topology first**: managed (EKS/GKE/AKS) vs self-hosted (kubeadm,
   k3s/k0s, Talos), single- vs multi-tenant, who the threat actors are (workload →
   control plane? tenant → tenant? compromised CI → cluster?). Read the matching rules.
2. **Least privilege by default**: no wildcard RBAC verbs/resources, `automountService
   AccountToken: false` unless the pod calls the API, scoped AppProjects, operators get
   the narrowest RBAC that works. Loosen only with a comment stating why.
3. **Encrypt etcd at rest with a KMS provider** (`rules/01`) — Secrets are base64, not
   encrypted, by default. This is the single most common "we thought we were covered" gap.
4. **Admission is fail-closed and ENFORCING, not auditing.** A policy left in `audit`/
   `warn` forever is documentation, not a control (`rules/03`). Ship the AUDIT→ENFORCE
   rollout plan with the policy.
5. **GitOps is the only write path to the cluster.** Humans propose via PR; the
   controller reconciles. Scope the controller's own privileges and AppProjects tightly
   (`rules/04`).
6. **Plan the upgrade before you build**: version skew, EOL date, CVE-response runbook,
   tested etcd restore (`rules/01`, `rules/07`).

Deliverables: topology + threat statement, the concrete manifests/configs, the
AUDIT→ENFORCE rollout, and the residual-risk/assumptions list (cloud-managed control
plane internals you cannot see, org IAM, CNI behavior).

## AUDIT mode

Use when reviewing an existing cluster, its RBAC, policies, GitOps config, or operators.

Procedure: inventory the cluster surface (control plane flags or managed equivalent,
RBAC graph, admission policies, GitOps controllers, operators/CRDs, namespaces/tenancy);
for each, walk the relevant rules-file Audit checklist; verify empirically with
`kubectl`, `kubectl auth can-i`, krane, kube-bench, and `helm template` where
possible; report findings in the format below. Do not report style nits as security
findings.

### Severity conventions

| Severity | Meaning | Examples |
|---|---|---|
| **Critical** | Cluster-admin, all-Secrets read, or cluster takedown reachable now | `anonymous-auth` enabled on API server/kubelet; etcd unencrypted AND reachable; ClusterRoleBinding granting `cluster-admin` to a workload SA or `system:authenticated`; wildcard `*/*` ClusterRole bound broadly; Argo CD AppProject `clusterResourceWhitelist: [{group: '*', kind: '*'}]` with broad SSO; unpatched control plane on a known-RCE CVE |
| **High** | Escalation/secret-read by an in-cluster or contributor principal, or a single event from it | `escalate`/`bind`/`impersonate` verbs granted; secret-reader → token-mint → privilege chain; admission policy in `audit` mode for a control that should enforce; image-verification policy only `Audit`s signatures; operator with cluster-wide `secrets:*`; kubelet `read-only-port` open; no etcd backup or untested restore |
| **Medium** | Weakens defense in depth or detection | PSA not enforced (only `warn`/`audit`); `automountServiceAccountToken` defaulted on for non-API pods; no default-deny NetworkPolicy (requirement-level; depth → network-security); audit policy missing, `None` for Secret access, or Secret/ConfigMap bodies captured at `Request`/`RequestResponse`; aggregated ClusterRole accreting verbs; no PDB on critical workloads |
| **Low** | Hygiene, hardening headroom | RBAC subjects for departed users; unused ClusterRoles; namespaces without resource quotas; `:latest` image tags admitted; missing PolicyException expiry |

Severity is judged by **reachability** (anonymous > workload/tenant > contributor > admin)
× **yield** (cluster-admin/all-Secrets > namespace compromise > info leak > availability).

### Finding format

```
file:line | rule | severity | effort | fix
```
Where `effort` is one of trivial / small / medium / large, `rule` is the rules-file
section (e.g. `02 §RBAC-wildcards`), and `fix` is the concrete change. Expand below the
line with: what is wrong, who exploits it and how (concrete attack path), and a snippet
when short. Example:

```
clusterrole-ci.yaml:14 | 02 §escalate-verbs | Critical | small | remove the bind/escalate grant; scope to the 3 named ClusterRoles the controller actually applies
  Issue: ClusterRole bound to the CI ServiceAccount grants rbac.authorization.k8s.io/{bind,escalate} on clusterroles.
  Attack path: anyone who can run a job as this SA (any merged PR) can bind themselves cluster-admin.
```

End every audit with: counts per severity, top 3 fixes by risk-reduction-per-effort, and
an explicit OUT-OF-SCOPE list (managed control-plane internals, org IAM, CNI/mesh,
runtime detection content).

## Rules index

| File | Read this when... |
|---|---|
| [rules/01-control-plane-etcd.md](rules/01-control-plane-etcd.md) | HA control plane, API server flags (anonymous-auth, authz modes, audit), etcd encryption-at-rest with KMS v2 + backup/defrag/restore, kubelet hardening, node + immutable-distro hardening (Talos no-SSH/machine-config/SecureBoot+TPM, k3s/k0s), CIS benchmark + kube-bench |
| [rules/02-rbac-serviceaccounts.md](rules/02-rbac-serviceaccounts.md) | Roles/ClusterRoles least-privilege, the escalation traps (wildcards, `bind`/`escalate`/`impersonate`, cluster-admin bindings, aggregated roles, secret-reader chains), ServiceAccount hygiene (automount off, bound/projected/audience-scoped tokens, no long-lived token Secrets), RBAC auditing (`auth can-i --list`, krane; who-can/rbac-tool unmaintained), the harmless-looking grants (`nodes/proxy`, PV create, CSR approval, namespace patch) |
| [rules/03-admission-policy.md](rules/03-admission-policy.md) | Pod Security Admission (restricted/baseline/privileged, enforce/audit/warn) and its limits, Kyverno vs Gatekeeper/OPA vs ValidatingAdmissionPolicy/MutatingAdmissionPolicy, the AUDIT→ENFORCE rollout discipline, image verification at admission (cosign/Kyverno `ImageValidatingPolicy`), PolicyException discipline |
| [rules/04-gitops-controllers.md](rules/04-gitops-controllers.md) | Argo CD / Flux security: AppProject scoping (the `clusterResourceWhitelist:[{*,*}]` trap), project/RBAC/SSO, the controller's own privileges and self-management, repo/SSH creds, ApplicationSet injection, auto-sync vs approval, drift, recent Argo CD CVEs, promotion/rollback as git ops |
| [rules/05-operators-crds-webhooks.md](rules/05-operators-crds-webhooks.md) | The operator privilege problem (broad RBAC → CRD-mediated escalation), vetting operator RBAC, CRD validation/security, trusted controllers (ESO, cert-manager), admission webhooks as attack surface (failurePolicy, timeout, TLS, namespaceSelector) |
| [rules/06-workloads-tenancy.md](rules/06-workloads-tenancy.md) | Resource requests/limits as availability+QoS, PodDisruptionBudget, topology spread, anti-affinity, priorityClass/preemption, namespace-as-SOFT-boundary reality, hard multi-tenancy (vCluster/separate clusters/node isolation), Secrets in K8s (etcd encryption + ESO/sealed-secrets pointer) |
| [rules/07-supply-chain-audit.md](rules/07-supply-chain-audit.md) | Helm/Kustomize review before apply (`helm template`, RBAC-in-charts trap, privilege-granting values), OCI chart signing/provenance, only-signed-images enforcement, digest pinning at the manifest layer, K8s audit policy (what/levels), shipping audit logs, detection + runtime-security pointers |

When a task spans layers (most do), read every matching file. For a full cluster audit,
read all seven plus the referenced sibling skills.

## Top 10 non-negotiables

Violations are at minimum **High** in AUDIT mode and must never be introduced in BUILD mode:

1. **`anonymous-auth=false` on the API server AND kubelet; kubelet `read-only-port=0`,
   kubelet authz mode `Webhook` (not `AlwaysAllow`).** Anonymous or unauthenticated
   access to either is cluster-game-over (`01`).
2. **etcd encrypted at rest with a KMS v2 provider** (envelope DEK/KEK), not the default
   base64. Secrets are NOT encrypted out of the box (`01`, `06`).
3. **No wildcard RBAC.** No `*` verbs/resources in Roles/ClusterRoles bound to workloads
   or users; no `cluster-admin` bound to a ServiceAccount, `system:authenticated`, or
   `system:unauthenticated` (`02`).
4. **`bind`, `escalate`, `impersonate` are privilege-escalation verbs** — grant only to
   a named, audited admin path, never to a workload or CI SA (`02`).
5. **`automountServiceAccountToken: false`** is the default; opt in only for pods that
   call the API. No long-lived Secret-based SA tokens — use bound/projected tokens (`02`).
6. **Pod Security Admission `restricted` ENFORCED** on workload namespaces (label
   `pod-security.kubernetes.io/enforce: restricted`), not merely `warn`/`audit`. PSA is
   stable; PSP is gone (`03`). Pod-level field internals → sota-sandboxing.
7. **Admission policies enforce, with a documented AUDIT→ENFORCE rollout.** A policy
   parked in `Audit`/`warn` indefinitely is a real, recurring finding (`03`).
8. **GitOps is the only cluster write path; the controller and its AppProjects are
   tightly scoped.** Never `clusterResourceWhitelist: [{group:'*',kind:'*'}]` with broad
   project access; pin Argo CD/Flux versions and patch known CVEs (`04`).
9. **Operators get least-privilege RBAC; admission webhooks have correct
   `failurePolicy`/`timeoutSeconds`/`namespaceSelector` and TLS** — a webhook is both a
   control and a single point of failure/attack (`05`).
10. **API server audit logging enabled** (RequestResponse for RBAC/admission changes;
    Secrets/ConfigMaps at Metadata only, since a body-level rule logs their values),
    shipped to tamper-resistant storage; etcd backups taken AND restore-tested (`07`,`01`).
    Detection content on the stream → sota-detection-engineering.

If the user asks for something that violates a non-negotiable, implement the secure
alternative and explain the delta; comply only after they acknowledge the risk explicitly.
