---
name: k8s-external-secrets-troubleshooting
description: >-
  Use when External Secrets Operator does not create or update a Kubernetes Secret: an
  ExternalSecret with SecretSyncedError ("could not get secret data from provider"),
  SecretOwnedByOther ("target is owned by another ExternalSecret"), SecretMissing or
  SecretImmutable, a SecretStore or ClusterSecretStore that is not Ready
  (InvalidProviderConfig, "unable to validate store"), a ClusterSecretStore not allowed
  from a namespace, a ClusterExternalSecret with failed namespaces, a value that does
  not refresh, or manifests on the removed v1beta1 API. Investigates with kubectl get,
  describe, events and controller logs, never reading the Secrets themselves, and
  proposes fixes. Reads first and asks before changing anything.
license: Apache-2.0
metadata:
  verified-with: "kubernetes 1.37, external-secrets 2.14"
  verified-on: "2026-10-24"
---

# External Secrets troubleshooting

Find out why External Secrets Operator (ESO) does not create or update a Secret, and
propose a fix. **Read first, ask before changing.** Run the investigation commands
freely. Run a command under an "Ask first" line only after the user approves that exact
command; if your credentials do not allow it, give it to the user to run. Never run a
"Proposed fix"; hand it to the user.

An **ExternalSecret** says which keys to fetch from an external store and which
Kubernetes Secret to write (`spec.target`). It uses a **SecretStore** (one namespace) or
**ClusterSecretStore** (any allowed namespace) that holds the provider configuration (a
cloud secret manager, Vault, and others). The ESO controller syncs on
`spec.refreshInterval` and reports the result on the ExternalSecret's `Ready` condition.

**Never read Secrets**, here least of all: not the target Secret ESO writes, not the
provider credentials a store references, not the webhook's certificate. You can tell
whether a sync worked from the ExternalSecret's status and events. If the user wants
to check a value, they look at it themselves.

The commands use placeholders: `my-namespace`, `my-app-config` (the ExternalSecret and
its target Secret), `my-app-store` (the store) and `external-secrets` (the namespace ESO
runs in; a Helm install usually uses `external-secrets`, the release manifest
`default`). Replace them with the real names.

## When to use

- A Secret that an ExternalSecret should create is missing, or has old values.
- `kubectl get externalsecrets` shows `SecretSyncedError`, `SecretOwnedByOther`,
  `SecretMissing` or `SecretImmutable`.
- A SecretStore or ClusterSecretStore is not Ready.
- A ClusterExternalSecret did not create its ExternalSecrets in some namespaces.

Hand-offs, by skill name. When the evidence points elsewhere, continue with that skill;
if it is not installed, keep going with the steps here and tell the user which skill
would help:

- The Secret exists and the app still fails (it does not read it, the pod is not
  restarted after a change, it crashes): `k8s-workload-troubleshooting`.
- The ESO pods crash or stay Pending: `k8s-workload-troubleshooting`.

## Investigate

Work through the steps in order. Stop when you have the cause and its evidence.

**1. List the ExternalSecrets** with their store, status and last sync.

```bash
kubectl get externalsecrets -n my-namespace
kubectl get clusterexternalsecrets
```

**2. Read the ExternalSecret**: its store reference, target, keys, and conditions and
events.

```bash
kubectl describe externalsecret my-app-config -n my-namespace
kubectl get externalsecret my-app-config -n my-namespace -o jsonpath='{.spec.secretStoreRef}{"\n"}{.spec.target}{"\n"}{.spec.data}{"\n"}{.spec.dataFrom}{"\n"}{.status.conditions}{"\n"}'
kubectl events -n my-namespace --for externalsecret/my-app-config
```

**3. Read the store** it points at.

```bash
kubectl get secretstores -n my-namespace
kubectl get clustersecretstores
kubectl describe secretstore my-app-store -n my-namespace
```

**4. Read the controller's logs.** Since ESO 2.14 the ExternalSecret's status and
events say only `could not get secret data from provider` for every store or provider
problem; the actual cause is in the controller's log, under `Reconciler error`.

```bash
kubectl get deployments -A -l app.kubernetes.io/name=external-secrets
kubectl logs -n external-secrets deployment/external-secrets --tail=200 | grep my-app-config
```

**5. Open the matching reference** and follow its steps:

| What you see | Reference |
|---|---|
| `SecretSyncedError` `could not get secret data from provider`: a missing key, a wrong store name, store not ready, namespace not allowed | [references/sync-errors.md](references/sync-errors.md) |
| A store not Ready: `InvalidProviderConfig`, `ProviderNotFound`, `ValidationUnknown` | [references/stores.md](references/stores.md) |
| `SecretOwnedByOther`, `SecretMissing`, `SecretImmutable`, values that do not refresh, ClusterExternalSecrets, removed `v1beta1` | [references/target-and-refresh.md](references/target-and-refresh.md) |

## Read the results

What the common findings mean (ESO 2.14):

- **`Ready` `False`, reason `SecretSyncedError`, `could not get secret data from
  provider`**: the generic message. The controller log for that ExternalSecret has the
  real error, for example `error processing spec.data[0] (key: <key>), err: Secret does
  not exist` (the key is not in the store) or `could not get SecretStore "<name>"`
  (no store of that name in the namespace).
- **Reason `SecretOwnedByOther`, `target is owned by another ExternalSecret: ... secret
  is owned by another ExternalSecret: <name>`**: two ExternalSecrets write the same
  target Secret. The first one owns it; the other cannot sync.
- **A store `Ready` `False`, `InvalidProviderConfig`** (`unable to create client` or
  `unable to validate store`): ESO cannot reach or authenticate to the provider with
  the store's configuration. Credentials are in Secrets: the user checks them.
- **`Ready` `True`, `secret synced`, but the app sees an old value**: ESO wrote the
  Secret; either the external value changed after the last refresh
  (`spec.refreshInterval`, `refreshPolicy`), or the app reads the Secret only at
  start.
- **A store event `StoreUnmaintained`** (`store isn't currently maintained`): the
  provider is marked unmaintained in this ESO version; it may still work.

State the cause in one sentence, then the evidence you saw (the condition, the event,
the log line, the spec field), then the proposed fix.

## Proposed fix

Show each fix to the user before running it: what it changes and how to undo it.
Patching an ExternalSecret's store reference or remote key, and asking ESO to sync now,
are reversible, so they go under "Ask first" and run only after the user says yes.
Creating or changing Secrets (provider credentials, the target), changing stores, and
deleting ExternalSecrets or their target Secrets are never run by you: hand them to the
user as proposed fixes. Prefer fixing the source the ExternalSecret is deployed from.
Write each undo with the values you found.

Point an ExternalSecret at the store that exists (to test before fixing the source):

> Ask first: the agent runs this only after the user approves it.

```bash
kubectl patch externalsecret my-app-config -n my-namespace --type=merge -p '{"spec": {"secretStoreRef": {"name": "my-app-store"}}}'
# Undo: kubectl patch externalsecret my-app-config -n my-namespace --type=merge -p '{"spec": {"secretStoreRef": {"name": "my-store"}}}'
```

Ask ESO to sync now instead of waiting for the refresh interval (use the current time
as the value; any new value triggers a sync):

> Ask first: the agent runs this only after the user approves it.

```bash
kubectl annotate externalsecret my-app-config -n my-namespace force-sync=2026-10-24T12:00:00Z --overwrite
# Undo: nothing to undo; the annotation only asks for one sync
```

## Sources

Checked against the External Secrets Operator 2.14 documentation and source (v2.14.0):

- [Getting started](https://external-secrets.io/latest/introduction/getting-started/)
  and the [FAQ](https://external-secrets.io/latest/introduction/faq/), whose last debug
  step reads the created Secret, which this skill leaves to the user.
- [ExternalSecret](https://external-secrets.io/latest/api/externalsecret/),
  [SecretStore](https://external-secrets.io/latest/api/secretstore/),
  [ClusterSecretStore](https://external-secrets.io/latest/api/clustersecretstore/) and
  [ClusterExternalSecret](https://external-secrets.io/latest/api/clusterexternalsecret/):
  fields, policies, refresh and force-sync.
- [Lifecycle](https://external-secrets.io/latest/guides/ownership-deletion-policy/):
  creation and deletion policies, ownership.
- [Fake provider](https://external-secrets.io/latest/provider/fake/).
- [v0.17.0 release notes](https://github.com/external-secrets/external-secrets/releases/tag/v0.17.0):
  `v1beta1` no longer served.
- Conditions, messages and the 2.14 change that keeps provider errors out of status
  (PR #7149), from the source:
  [externalsecret_types.go](https://github.com/external-secrets/external-secrets/blob/v2.14.0/apis/externalsecrets/v1/externalsecret_types.go),
  [externalsecret_controller.go](https://github.com/external-secrets/external-secrets/blob/v2.14.0/pkg/controllers/externalsecret/externalsecret_controller.go),
  [statuserr.go](https://github.com/external-secrets/external-secrets/blob/v2.14.0/pkg/controllers/util/statuserr.go).
  The messages quoted here were also seen on a Kubernetes 1.37 kind cluster with ESO
  2.14.0.
