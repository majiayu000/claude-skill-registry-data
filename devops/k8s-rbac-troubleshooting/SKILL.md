---
name: k8s-rbac-troubleshooting
description: >-
  Use when a Kubernetes request is refused by RBAC: "Error from server (Forbidden)",
  "User ... cannot list resource ... in the namespace" or "at the cluster scope", a
  ServiceAccount, controller, CI job or person getting 403, a RoleBinding that does not
  seem to apply (wrong namespace, wrong subject, a ClusterRole bound with a RoleBinding),
  "is attempting to grant RBAC permissions not currently held", "roleRef ... field is
  immutable", 401 Unauthorized versus 403 Forbidden, or a custom resource that `view`
  cannot read. Investigates with kubectl auth can-i, get and describe, and proposes
  fixes. Reads first and asks before changing anything.
license: Apache-2.0
metadata:
  verified-with: "kubernetes 1.37"
  verified-on: "2026-10-25"
---

# RBAC troubleshooting

Find out why Kubernetes refuses a request, and propose the smallest grant that fixes it.
**Read first, ask before changing.** Run the investigation commands freely. Run a
command under an "Ask first" line only after the user approves that exact command; if
your credentials do not allow it, give it to the user to run. Never run a "Proposed
fix"; hand it to the user.

Every request is made by a **subject**: a user, a group, or a ServiceAccount, which
authenticates as `system:serviceaccount:<namespace>:<name>`. RBAC allows a request only
when a **binding** gives the subject a **role** whose rules cover the verb, the API group,
the resource and the namespace. There are no deny rules: a 403 means that no binding
allowed it. A **RoleBinding** grants its role in its own namespace only; a
**ClusterRoleBinding** grants a ClusterRole everywhere, including cluster-scoped
resources such as nodes and namespaces.

The commands use placeholders: `my-namespace`, `my-app` (the ServiceAccount and its
workload), `my-binding` and `my-role`. Replace them with the real names. The built-in `view` role
cannot read Roles, ClusterRoles or their bindings; if they are forbidden, say so and ask
the user for them, or work from the error message alone. Never read Secrets, and never
read a ServiceAccount token, in a pod or anywhere else.

## When to use

- A log or an error says `Forbidden`, `cannot <verb> resource`, or `403`.
- A pod, Job or controller crashes or retries right after a call to the API server.
- A person or a CI pipeline cannot do what they expect with kubectl.
- A RoleBinding was created but changes nothing.

Hand-offs, by skill name. When the evidence points elsewhere, continue with that skill;
if it is not installed, keep going with the steps here and tell the user which skill
would help:

- The 403 message has no `User "..." cannot` part and names an admission webhook or a
  policy: `k8s-kyverno-troubleshooting`, `k8s-gatekeeper-troubleshooting`. (A webhook
  authorizer's refusal keeps the `User "..." cannot` text and adds its own reason after
  it.)
- `violates PodSecurity`: `k8s-workload-troubleshooting`.
- The workload fails for another reason once access works: `k8s-workload-troubleshooting`.

## Investigate

Work through the steps in order. Stop when you have the cause and its evidence.

**1. Read the exact refusal.** It names the subject, the verb, the resource with its API
group, and the namespace or "at the cluster scope". Everything else follows from it.

```bash
kubectl logs -n my-namespace deployment/my-app --tail=50
kubectl logs -n my-namespace deployment/my-app --previous --tail=50
kubectl get events -n my-namespace --sort-by=.lastTimestamp
```

**2. Check which identity the workload uses.** The pod's ServiceAccount (`default` if
none is set) and whether the API credentials are mounted at all.

```bash
kubectl get pods -n my-namespace -l app=my-app -o jsonpath='{range .items[*]}{.metadata.name}{" sa="}{.spec.serviceAccountName}{" automount="}{.spec.automountServiceAccountToken}{"\n"}{end}'
kubectl get serviceaccount my-app -n my-namespace -o yaml
```

**3. Ask the API server.** `auth can-i` with `--as` asks for another subject; it needs
the `impersonate` verb. If it is refused (`cannot impersonate`), give the command to the
user. Without `--as` it answers for you.

```bash
kubectl auth can-i list configmaps -n my-namespace --as=system:serviceaccount:my-namespace:my-app
kubectl auth can-i --list -n my-namespace --as=system:serviceaccount:my-namespace:my-app
kubectl auth whoami
```

**4. Find the bindings that name the subject**, and the role each one refers to. `-o
wide` shows the subjects; a ServiceAccount shows as `namespace/name`.

```bash
kubectl get rolebindings -n my-namespace -o wide
kubectl get clusterrolebindings -o wide | grep my-app
kubectl get rolebindings -A -o wide | grep my-app
kubectl describe rolebinding my-binding -n my-namespace
```

**5. Read the role's rules** and compare them with the refused request: verb, API group
(`""` is the core group), resource (with its subresource, such as `pods/log`), and
resource names.

```bash
kubectl get role my-role -n my-namespace -o yaml
kubectl describe clusterrole my-role
```

**6. Open the matching reference** and follow its steps:

| What you see | Reference |
|---|---|
| A binding that applies to nobody, a role that does not grant what it seems to, aggregated roles, escalation and `roleRef` errors | [references/bindings-and-roles.md](references/bindings-and-roles.md) |
| 401 instead of 403, `system:anonymous`, missing or expired credentials, impersonation, a 403 from admission | [references/authentication-and-admission.md](references/authentication-and-admission.md) |

## Read the results

What the common findings mean (Kubernetes 1.37):

- **`User "system:serviceaccount:my-namespace:my-app" cannot list resource "configmaps"
  in API group "" in the namespace "my-namespace"`**: no binding gives that subject
  `list` on `configmaps` there. The verb matters: `kubectl get` of one object is `get`,
  of all objects `list`, `--watch` also needs `watch`. A role with only `get` refuses
  the list.
- **`... at the cluster scope`**: the request is for a cluster-scoped resource (nodes,
  namespaces, PersistentVolumes, CRDs) or across all namespaces. Only a
  ClusterRoleBinding grants that; a ClusterRole bound with a RoleBinding grants its rules
  inside that one namespace only.
- **A binding that names the right role but the wrong subject**: a ServiceAccount subject
  in another namespace (`default/my-app` instead of `my-namespace/my-app`), kind `User`
  with a group's name, or a misspelled name match nobody, without any error.
- **A RoleBinding in another namespace**: it grants nothing in `my-namespace`.
- **The refusal ends with `rbac: RBAC: role.rbac.authorization.k8s.io "..." not
  found`**: a binding for this subject names a role that does not exist (often a typo in
  `roleRef.name`).
- **`auth can-i` answers `yes` but the request still fails**: the request is made by
  another identity (check step 2), or a webhook authorizer or admission refuses it (see
  the second reference).
- **`cannot impersonate-on:...`** or **`cannot impersonate resource`** when you run
  `auth can-i --as`: your own identity may not impersonate; it says nothing about the
  subject. Give the command to the user.

State the cause in one sentence, then the evidence you saw (the exact refusal, the
binding's subjects and role, the role's rules), then the proposed fix.

## Proposed fix

Show each fix to the user before running it: what it changes and how to undo it. Every
change to a Role, ClusterRole or binding grants or removes access, for this workload and
for anyone else bound to the same role: never run them yourself; hand them to the user
as proposed fixes, granting the narrowest verbs, resources and namespace that fix the
refusal. Prefer fixing the source (the Helm chart, the manifests in Git). Write each
undo with the values you found.

Add the missing verbs to the role, in its source, for example `verbs: [get, list,
watch]` on `configmaps`:

> Proposed fix: review before running. The agent does not run this.

```bash
kubectl apply -f my-app-role.yaml
# Undo: kubectl apply -f my-app-role-before.yaml (the role as it was, with verbs: [get])
```

Bind the subject that the workload really uses (a ServiceAccount needs its own
namespace), or bind a ClusterRole for cluster-scoped resources with a ClusterRoleBinding
instead of a RoleBinding:

> Proposed fix: review before running. The agent does not run this.

```bash
kubectl create clusterrolebinding my-app-node-reader --clusterrole=my-app-node-reader --serviceaccount=my-namespace:my-app
# Undo: kubectl delete clusterrolebinding my-app-node-reader
```

A binding's `roleRef` cannot be changed (`field is immutable`); to point it at another
role, delete it and create it again, which removes the access for a moment. Save the
binding first, so the undo can restore it:

```bash
kubectl get rolebinding my-binding -n my-namespace -o yaml
```

> Proposed fix: review before running. The agent does not run this.

```bash
kubectl delete rolebinding my-binding -n my-namespace
kubectl create rolebinding my-binding -n my-namespace --role=my-app-config-reader --serviceaccount=my-namespace:my-app
# Undo: kubectl delete rolebinding my-binding -n my-namespace && kubectl apply -f my-binding-before.yaml
```

Once access is fixed, a pod in CrashLoopBackOff recovers at its next restart. To retry
at once:

> Ask first: the agent runs this only after the user approves it.

```bash
kubectl rollout restart deployment/my-app -n my-namespace
# Undo: none needed; the restart only recreates the pods with the same template
```

## Sources

Checked against the Kubernetes 1.37 documentation and source (v1.37.1):

- [Using RBAC Authorization](https://kubernetes.io/docs/reference/access-authn-authz/rbac/):
  roles, bindings, `roleRef`, subjects, default and aggregated roles, escalation.
- [Authorization](https://kubernetes.io/docs/reference/access-authn-authz/authorization/):
  verbs per request, `kubectl auth can-i`, authorizer verdicts, admission after
  authorization.
- [Authenticating](https://kubernetes.io/docs/reference/access-authn-authz/authentication/)
  and [User impersonation](https://kubernetes.io/docs/reference/access-authn-authz/user-impersonation/):
  ServiceAccount usernames and groups, 401 and anonymous requests, `--as`.
- [Service accounts](https://kubernetes.io/docs/concepts/security/service-accounts/):
  default permissions, token checks and rotation.
- Messages from the source:
  [responsewriters/errors.go](https://github.com/kubernetes/kubernetes/blob/v1.37.1/staging/src/k8s.io/apiserver/pkg/endpoints/handlers/responsewriters/errors.go)
  (the Forbidden text) and
  [rbac/validation/rule.go](https://github.com/kubernetes/kubernetes/blob/v1.37.1/pkg/registry/rbac/validation/rule.go)
  (escalation and subject matching). The refusals quoted here were seen on a
  Kubernetes 1.37 kind cluster.
