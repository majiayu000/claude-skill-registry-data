---
name: k8s-api-troubleshooting
description: >-
  Use when the Kubernetes API server itself refuses or fails a request, before any
  controller acts on it: "failed calling webhook", "admission webhook ... denied the
  request", "ValidatingAdmissionPolicy ... denied request", a ReplicaSet with
  FailedCreate and no pods, an APIService "False (ServiceNotFound)",
  "FailedDiscoveryCheck" or "MissingEndpoints", "unable to retrieve the complete list of
  server APIs", a namespace stuck in Terminating, "no matches for kind" or "ensure CRDs
  are installed first", "strict decoding error: unknown field", a conversion webhook
  failure, "You must be logged in to the server (Unauthorized)", 429 "too many
  requests", "etcdserver:" errors, "Request entity too large" or "metadata.annotations:
  Too long". Investigates with kubectl get, describe, events and the health endpoints,
  and proposes fixes. Reads first and asks before changing anything.
license: Apache-2.0
metadata:
  verified-with: "kubernetes 1.37"
  verified-on: "2026-10-25"
---

# API server troubleshooting

Find out why the API server refuses or fails a request, and propose a fix. **Read first,
ask before changing.** Run the investigation commands freely. Run a command under an "Ask
first" line only after the user approves that exact command; if your credentials do not
allow it, give it to the user to run. Never run a "Proposed fix"; hand it to the user.

Every request goes through the same steps in the API server: **authentication** (who is
asking: a 401 if nobody), **authorization** (may they: a 403 from RBAC), **admission**
(mutating webhooks, schema validation, then ValidatingAdmissionPolicies and validating
webhooks), then **storage** in etcd. Requests for an **aggregated API** (an APIService
such as `v1beta1.metrics.k8s.io`) are sent on to another server instead, and
**discovery** lists every group and version, including those. A failure at any step comes
back to the caller, so the error message usually names the step: the webhook, the
APIService, the kind and version, or the limit.

The commands use placeholders: `my-namespace`, `my-app`, `my-webhook` (a webhook
configuration and its Service in `my-webhook-system`), `v1beta1.my-api.example.com` (an
APIService) and `widgets.my-api.example.com` (a CRD). Replace them with the real names.
Never read Secrets. The built-in `view` role cannot read webhook configurations,
admission policies, APIServices, CRDs or FlowSchemas; if they are forbidden, say so, ask
the user for them, and work from the error text, which already names the webhook, the
group and version, or the APIService.

## When to use

- A Deployment, Job or ReplicaSet has no pods and its events say `FailedCreate`.
- kubectl apply, a CI job, Helm, Argo CD or Flux fails with an error from the server
  that is not a 403.
- A namespace or another object stays in `Terminating`.
- kubectl prints warnings about API groups, or the cluster is slow and requests time out.

Hand-offs, by skill name. When the evidence points elsewhere, continue with that skill;
if it is not installed, keep going with the steps here and tell the user which skill
would help:

- `Forbidden: User "..." cannot ...` (RBAC): `k8s-rbac-troubleshooting`.
- The webhook or policy belongs to Kyverno, Gatekeeper or cert-manager (its name or its
  Service says so): `k8s-kyverno-troubleshooting`, `k8s-gatekeeper-troubleshooting`,
  `k8s-cert-manager-troubleshooting`. A denial from Istio's or another tool's webhook
  goes to that tool's skill.
- `v1beta1.metrics.k8s.io` or `external.metrics.k8s.io` unavailable:
  `k8s-autoscaling-troubleshooting`.
- `violates PodSecurity`, or pods that are created but fail: `k8s-workload-troubleshooting`.
- Helm's own errors (`another operation is in progress`, ownership):
  `k8s-helm-troubleshooting`.

## Investigate

Work through the steps in order. Stop when you have the cause and its evidence.

**1. Read the exact error**: where the request came from (a controller's events, a Job's
log, the user's command) and its full text. A controller retries, so its events show the
same message many times.

```bash
kubectl get events -n my-namespace --sort-by=.lastTimestamp
kubectl get deployment,replicaset -n my-namespace
kubectl describe replicaset -n my-namespace -l app=my-app
kubectl logs -n my-namespace job/my-deploy --tail=50
```

**2. Check the API server's health.** Everyone, even without RBAC rights, may read these;
`[-]... failed` names a failing check.

```bash
kubectl get --raw '/readyz?verbose'
kubectl get --raw '/livez?verbose'
kubectl version
```

**3. Check the aggregated APIs.** Any line that is not `True` is an API that discovery,
namespace deletion and garbage collection cannot reach.

```bash
kubectl get apiservices
kubectl get apiservice v1beta1.my-api.example.com -o jsonpath='{.spec.service.namespace}/{.spec.service.name}:{.spec.service.port}{"\n"}{range .status.conditions[*]}{.type}={.status} {.reason}: {.message}{"\n"}{end}'
```

**4. Find the webhook named in the error**, if there is one. The quoted name is the
webhook's own name (`webhooks[].name`), not its configuration's; list both to match them.

```bash
kubectl get validatingwebhookconfigurations,mutatingwebhookconfigurations
kubectl get validatingwebhookconfigurations -o jsonpath='{range .items[*]}{.metadata.name}{"\n"}{range .webhooks[*]}{"  "}{.name}{" policy="}{.failurePolicy}{" timeout="}{.timeoutSeconds}{" svc="}{.clientConfig.service.namespace}{"/"}{.clientConfig.service.name}{" url="}{.clientConfig.url}{"\n"}{end}{end}'
kubectl get mutatingwebhookconfigurations -o jsonpath='{range .items[*]}{.metadata.name}{"\n"}{range .webhooks[*]}{"  "}{.name}{" policy="}{.failurePolicy}{" timeout="}{.timeoutSeconds}{" svc="}{.clientConfig.service.namespace}{"/"}{.clientConfig.service.name}{" url="}{.clientConfig.url}{"\n"}{end}{end}'
```

**5. For a stuck namespace, read its conditions**: they name what blocks it.

```bash
kubectl get namespace my-namespace -o jsonpath='{.status.phase}{"\n"}{range .status.conditions[*]}{.type}={.status} {.reason}: {.message}{"\n"}{end}'
```

**6. Open the matching reference** and follow its steps:

| What you see | Reference |
|---|---|
| `failed calling webhook`, `denied the request`, a ValidatingAdmissionPolicy, `FailedCreate` with no pods | [references/admission.md](references/admission.md) |
| An APIService not `True`, discovery errors, `no matches for kind`, unknown fields, CRD versions and conversion, `Terminating` that never ends | [references/discovery-crds-deletion.md](references/discovery-crds-deletion.md) |
| 401, 429, timeouts, `etcdserver:` errors, size limits, a failing `/readyz` | [references/auth-load-storage.md](references/auth-load-storage.md) |

## Read the results

What the common findings mean (Kubernetes 1.37):

- **`Internal error occurred: failed calling webhook "<name>": failed to call webhook:
  Post "https://<service>.<namespace>.svc:443/<path>?timeout=<n>s": <cause>`**: the API
  server could not reach a webhook whose `failurePolicy` is `Fail` (the default), so it
  refused the request. The cause names why: `service "..." not found`; `connect:
  connection refused` when the Service has no ready endpoints; `context deadline
  exceeded` for a slow webhook; `x509: ...` for a wrong `caBundle`. A Deployment is still
  created when only pods are matched: its ReplicaSet shows the error as `FailedCreate`.
- **`admission webhook "<name>" denied the request: ...`** or **`ValidatingAdmissionPolicy
  '<policy>' with binding '<binding>' denied request: ...`**: the check ran and said no.
  That is a policy decision, not an outage; the message says which rule.
- **An APIService `False (ServiceNotFound)`, `False (MissingEndpoints)` or `False
  (FailedDiscoveryCheck)`**: its backend is gone, has no ready pods, or answers badly.
  Its group's resources cannot be used, and **every** namespace deletion in the cluster
  waits for it.
- **A namespace in `Terminating` with `NamespaceDeletionDiscoveryFailure=True`**
  (`Discovery failed for some groups, 1 failing: unable to retrieve the complete list of
  server APIs: <group/version>: stale GroupVersion discovery: ...`): an unavailable
  APIService. With `NamespaceContentRemaining` or `NamespaceFinalizersRemaining`, objects
  with finalizers are still waiting for their controller.
- **`no matches for kind "<Kind>" in version "<group/version>"`** and **`ensure CRDs are
  installed first`**: the API server serves no such kind in that version. Either the CRD
  is not installed, or it is and that version is `served: false` or was removed; read the
  CRD's versions before you believe the hint.
- **`strict decoding error: unknown field "spec.foo"`**: the field does not exist in that
  version's schema (often a typo, or a field from a newer version).
- **`You must be logged in to the server (Unauthorized)`**: the credentials are missing,
  expired or for another cluster; 403s are RBAC, not this.
- **`the server has received too many requests`** (429): API Priority and Fairness
  rejected the request; some client is sending too many.
- **`etcdserver: ...`**, **`Request entity too large: limit is 3145728`** or
  **`metadata.annotations: Too long: may not be more than 262144 bytes`**: storage or size
  limits; the third is usually a client-side kubectl apply storing a large object in its
  last-applied annotation.

State the cause in one sentence, then the evidence you saw (the exact message, the
webhook, APIService or CRD fields, the namespace conditions), then the proposed fix.

## Proposed fix

Show each fix to the user before running it: what it changes and how to undo it.
Webhook configurations, admission policies, APIServices, CRDs and API Priority and
Fairness objects act on the whole cluster: never change or delete them yourself; hand
them to the user as proposed fixes. Prefer the fix that restores the broken part (the
webhook's or the API's backend) over one that turns a check off. Never remove
finalizers by hand or force a namespace's deletion through `/finalize`: that skips the
cleanup and leaves objects behind. Save an object before a fix changes it, so the undo
can restore it:

```bash
kubectl get validatingwebhookconfiguration my-webhook -o yaml
kubectl get apiservice v1beta1.my-api.example.com -o yaml
```

Bring a webhook's or an aggregated API's backend back, when it was scaled down. Note
its current replica count first (`kubectl get deployment my-webhook -n
my-webhook-system`), so the undo puts that number back:

> Ask first: the agent runs this only after the user approves it.

```bash
kubectl scale deployment my-webhook -n my-webhook-system --replicas=2
# Undo: kubectl scale deployment my-webhook -n my-webhook-system --replicas=0 (the count you noted)
```

If the webhook is no longer wanted, or must let requests through while it is fixed (its
checks stop until it is restored):

> Proposed fix: review before running. The agent does not run this.

```bash
kubectl patch validatingwebhookconfiguration my-webhook --type=json -p '[{"op": "replace", "path": "/webhooks/0/failurePolicy", "value": "Ignore"}]'
# Undo: kubectl apply -f my-webhook-before.yaml (the configuration you saved above)
```

If an aggregated API is no longer used, remove its registration; namespaces then finish
deleting on their own:

> Proposed fix: review before running. The agent does not run this.

```bash
kubectl delete apiservice v1beta1.my-api.example.com
# Undo: kubectl apply -f my-apiservice-before.yaml (the APIService you saved above)
```

Fix a manifest that uses an unserved version or unknown fields in its source (the chart,
the Git repository), then let its pipeline apply it again. Do not test it with
`--dry-run=server` yourself: that is still an apply, sent through admission and its
webhooks; give it to the user to run.

## Sources

Checked against the Kubernetes 1.37 documentation and source (v1.37.1):

- [Dynamic admission control](https://kubernetes.io/docs/reference/access-authn-authz/extensible-admission-controllers/),
  [admission webhook good practices](https://kubernetes.io/docs/concepts/cluster-administration/admission-webhooks-good-practices/),
  [ValidatingAdmissionPolicy](https://kubernetes.io/docs/reference/access-authn-authz/validating-admission-policy/)
  and [manifest-based admission control](https://kubernetes.io/docs/reference/access-authn-authz/manifest-admission-control/).
- [The aggregation layer](https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/apiserver-aggregation/)
  and [configuring it](https://kubernetes.io/docs/tasks/extend-kubernetes/configure-aggregation-layer/).
- [CustomResourceDefinitions](https://kubernetes.io/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definitions/),
  [CRD versions](https://kubernetes.io/docs/tasks/extend-kubernetes/custom-resources/custom-resource-definition-versioning/),
  [field validation](https://kubernetes.io/docs/reference/using-api/api-concepts/#field-validation)
  and the [deprecated API migration guide](https://kubernetes.io/docs/reference/using-api/deprecation-guide/).
- [Finalizers](https://kubernetes.io/docs/concepts/overview/working-with-objects/finalizers/),
  [namespaces](https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/)
  and [garbage collection](https://kubernetes.io/docs/concepts/architecture/garbage-collection/).
- [Authenticating](https://kubernetes.io/docs/reference/access-authn-authz/authentication/),
  [API Priority and Fairness](https://kubernetes.io/docs/concepts/cluster-administration/flow-control/),
  [debugging it](https://kubernetes.io/docs/reference/debug-cluster/flow-control/),
  [health endpoints](https://kubernetes.io/docs/reference/using-api/health-checks/) and
  [operating etcd](https://kubernetes.io/docs/tasks/administer-cluster/configure-upgrade-etcd/).
- Messages from the source:
  [webhook dispatcher](https://github.com/kubernetes/kubernetes/blob/v1.37.1/staging/src/k8s.io/apiserver/pkg/admission/plugin/webhook/validating/dispatcher.go),
  [APIService availability](https://github.com/kubernetes/kubernetes/blob/v1.37.1/staging/src/k8s.io/kube-aggregator/pkg/controllers/status/remote/remote_available_controller.go),
  [namespace deletion conditions](https://github.com/kubernetes/kubernetes/blob/v1.37.1/pkg/controller/namespace/deletion/status_condition_utils.go)
  and [default roles](https://github.com/kubernetes/kubernetes/blob/v1.37.1/plugin/pkg/auth/authorizer/rbac/bootstrappolicy/policy.go)
  (who may read `/readyz` and `/livez`). The webhook, APIService, namespace and CRD
  messages quoted here were seen on a Kubernetes 1.37 kind cluster.
