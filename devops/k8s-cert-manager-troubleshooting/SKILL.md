---
name: k8s-cert-manager-troubleshooting
description: >-
  Use when cert-manager does not issue or renew a certificate in Kubernetes: a
  Certificate that stays READY False, a CertificateRequest that is Pending, Denied or
  Failed, an Issuer or ClusterIssuer that is not Ready ("Error getting keypair for CA
  issuer"), "Referenced \"Issuer\" not found", ACME Orders or Challenges stuck pending
  (HTTP-01, DNS-01, rate limits), a certificate that expired or did not renew, or
  "failed calling webhook \"webhook.cert-manager.io\"" when applying resources.
  Investigates with kubectl get, describe, events and logs, and proposes fixes. Reads
  first and asks before changing anything.
license: Apache-2.0
metadata:
  verified-with: "kubernetes 1.37, cert-manager 1.21"
  verified-on: "2026-10-24"
---

# cert-manager troubleshooting

Find out why cert-manager does not issue or renew a certificate, and propose a fix.
**Read first, ask before changing.** Run the investigation commands freely. Run a
command under an "Ask first" line only after the user approves that exact command; if
your credentials do not allow it, give it to the user to run. Never run a "Proposed
fix"; hand it to the user.

cert-manager works in a chain. A **Certificate** says what is wanted. cert-manager
creates a **CertificateRequest** for each issuance, which an **Issuer** (one namespace)
or **ClusterIssuer** (whole cluster) signs. For ACME issuers (Let's Encrypt and others)
the request also gets an **Order** with one **Challenge** per domain. Follow the chain
from the Certificate and stop at the first object that is not Ready.

The commands use placeholders: `my-namespace`, `my-app-tls` (the Certificate),
`my-issuer` and `my-cluster-issuer`. Replace them with the real names. The `cert-manager`
namespace and Deployment names are those of the default install; a Helm install may use
other names (find them with the first command of step 5).

Never read Secrets: not the certificate's Secret, not the key pair of a CA issuer, not
an ACME account key, not DNS provider credentials. The status of the cert-manager
resources says whether a Secret is missing or wrong. For the same reason do not use
`cmctl status certificate` or `cmctl inspect secret`: both read the certificate's Secret.

## When to use

- A Certificate shows `READY False`, or an Ingress or Gateway still serves an old or
  self-signed certificate.
- A CertificateRequest is Pending, Denied or Failed; an Order or Challenge stays pending.
- An Issuer or ClusterIssuer is not Ready.
- A certificate expired or did not renew.
- Creating or changing any cert-manager resource fails with
  `failed calling webhook "webhook.cert-manager.io"`.

Hand-offs, by skill name. When the evidence points elsewhere, continue with that skill;
if it is not installed, keep going with the steps here and tell the user which skill
would help:

- The cert-manager pods themselves crash or stay Pending: `k8s-workload-troubleshooting`.
- An HTTP-01 challenge cannot be reached through the Ingress, Gateway or Service, or a
  NetworkPolicy blocks it: `k8s-network-troubleshooting`.

## Investigate

Work through the steps in order. Stop when you have the cause and its evidence.

**1. See the Certificate**: Ready, the issuer it points at, and its conditions and
events. `Issuing` `True` means an issuance is in progress.

```bash
kubectl get certificate -n my-namespace
kubectl describe certificate my-app-tls -n my-namespace
kubectl get certificate my-app-tls -n my-namespace -o jsonpath='{.spec.issuerRef}{"\n"}{.status.conditions}{"\n"}'
```

**2. See its CertificateRequests.** The newest one says why issuance waits or failed:
the `Ready` condition's reason and message, and `Approved` or `Denied`.

```bash
kubectl get certificaterequest -n my-namespace
kubectl describe certificaterequest -n my-namespace
kubectl events -n my-namespace
```

**3. See the issuer** the request names. An Issuer lives in the Certificate's
namespace; a ClusterIssuer has no namespace. The built-in `view` role cannot read
ClusterIssuers; if the command is forbidden, say so, and read the issuer's state from
the CertificateRequest message ("Referenced issuer does not have a Ready status
condition" means it exists and is not Ready).

```bash
kubectl get issuer -n my-namespace
kubectl describe issuer my-issuer -n my-namespace
kubectl get clusterissuer
kubectl describe clusterissuer my-cluster-issuer
```

**4. For an ACME issuer, see the Order and the Challenges.** A Challenge's `State` and
`Reason` say what the ACME server or cert-manager's own self-check saw.

```bash
kubectl get orders -n my-namespace
kubectl describe order -n my-namespace
kubectl get challenges -n my-namespace
kubectl describe challenge -n my-namespace
```

**5. If nothing progresses, or creating a resource fails, check cert-manager itself**:
its three Deployments, the webhook's endpoints and the controller's logs.

```bash
kubectl get deployments -A -l app.kubernetes.io/instance=cert-manager
kubectl get pods -n cert-manager -o wide
kubectl get endpointslices -n cert-manager -l kubernetes.io/service-name=cert-manager-webhook
kubectl logs -n cert-manager deployment/cert-manager --tail=100 | grep my-app-tls
kubectl logs -n cert-manager deployment/cert-manager-webhook --tail=50
```

**6. Open the matching reference** and follow its steps:

| What you see | Reference |
|---|---|
| `IssuerNotFound`, `IssuerNotReady`, `ErrGetKeyPair`, `Denied`, `Failed`, a request that never comes | [references/issuers-and-requests.md](references/issuers-and-requests.md) |
| Order or Challenge `pending`, `invalid` or `errored`, HTTP-01 or DNS-01 self-check errors, rate limits | [references/acme.md](references/acme.md) |
| `failed calling webhook "webhook.cert-manager.io"`, `x509` errors from the webhook, cainjector | [references/webhook.md](references/webhook.md) |
| Expired or not renewed, `Renewing`, a Certificate that reissues again and again | [references/renewal.md](references/renewal.md) |

## Read the results

What the common findings mean (cert-manager 1.21):

- **`Issuing certificate as Secret does not exist`** on a new Certificate is the normal
  first step, not the cause. Look one step down the chain: the CertificateRequest.
- **`Referenced "Issuer" not found: issuer.cert-manager.io "<name>" not found`** (reason
  `Pending`, event `IssuerNotFound`): no Issuer of that name in the Certificate's
  namespace. `issuerRef.kind` defaults to `Issuer`, so a Certificate meant for a
  ClusterIssuer that leaves out `kind: ClusterIssuer` gets this message. Compare
  `spec.issuerRef` with the issuers that exist.
- **`Referenced issuer does not have a Ready status condition`** (event
  `IssuerNotReady`): the issuer exists but is not Ready. Its own condition says why.
- **A CA Issuer with `Error getting keypair for CA issuer: secrets "<name>" not found`**
  (reason `ErrGetKeyPair`): the Secret named in `spec.ca.secretName` does not exist in
  the issuer's namespace (for a ClusterIssuer, in the cluster resource namespace, by
  default `cert-manager`). Confirm with the user rather than reading Secrets.
- **`Denied`**: an approval policy (for example approver-policy) refused the request;
  cert-manager's own approver only approves. Fix the policy or the request.
- **A failed request** is retried with a backoff that starts at one hour, so a fixed
  cause can look unfixed for a while. `Issuing` `False` with "has failed to complete and
  will be retried" says so.
- **`failed calling webhook "webhook.cert-manager.io"`** on create or update: the API
  server cannot reach cert-manager's webhook. Nothing in that namespace is wrong yet;
  see [references/webhook.md](references/webhook.md).

State the cause in one sentence, then the evidence you saw (the condition reason and
message, the issuerRef, the issuer's state), then the proposed fix.

## Proposed fix

Show each fix to the user before running it: what it changes and how to undo it.
Patching a Certificate's `issuerRef` and scaling a cert-manager Deployment are
reversible, so they go under "Ask first" and run only after the user says yes. Creating
or changing Secrets, issuers and webhook configurations, and deleting resources, are
never run by you: hand them to the user as proposed fixes and say why. Prefer fixing
the source the resources are deployed from (manifest, Helm values, GitOps repository):
the next sync would undo a patch. Write each undo with the values you found.

Point a Certificate at the ClusterIssuer it was meant to use:

> Ask first: the agent runs this only after the user approves it.

```bash
kubectl patch certificate my-app-tls -n my-namespace --type=merge -p '{"spec": {"issuerRef": {"kind": "ClusterIssuer"}}}'
# Undo: kubectl patch certificate my-app-tls -n my-namespace --type=json -p '[{"op": "remove", "path": "/spec/issuerRef/kind"}]'
```

cert-manager replaces the waiting CertificateRequest with a new one right after the
change.

Bring back a webhook that was scaled to zero (write the undo with the replicas you
found):

> Ask first: the agent runs this only after the user approves it.

```bash
kubectl scale deployment/cert-manager-webhook -n cert-manager --replicas=1
# Undo: kubectl scale deployment/cert-manager-webhook -n cert-manager --replicas=0
```

A CA Issuer whose key pair is missing needs that Secret created from the CA's
certificate and key, in the issuer's namespace, under the name in `spec.ca.secretName`.
Only the user has the CA files, and you never handle Secrets, so the user creates it
with their usual tooling; or, if the issuer names the wrong Secret, the user fixes
`spec.ca.secretName` in the source. cert-manager retries the issuer by itself once the
Secret exists.

## Sources

Checked against the cert-manager 1.21 documentation and source (v1.21.3):

- [Troubleshooting](https://cert-manager.io/docs/troubleshooting/) and
  [Troubleshooting ACME](https://cert-manager.io/docs/troubleshooting/acme/): the
  resource chain and the commands to follow it.
- [Troubleshooting the webhook](https://cert-manager.io/docs/troubleshooting/webhook/):
  the `failed calling webhook` errors and their causes.
- [Certificate resource](https://cert-manager.io/docs/usage/certificate/),
  [CertificateRequest](https://cert-manager.io/docs/usage/certificaterequest/) and
  [Issuer configuration](https://cert-manager.io/docs/configuration/): `issuerRef`,
  conditions, approval, renewal.
- [CA issuer](https://cert-manager.io/docs/configuration/ca/): `spec.ca.secretName` and
  the cluster resource namespace.
- [Release notes 1.18 to 1.21](https://cert-manager.io/docs/releases/): renewal policy,
  HTTP-01 path type, retry backoff.
- Condition reasons and messages from the source:
  [certificaterequests/sync.go](https://github.com/cert-manager/cert-manager/blob/v1.21.3/pkg/controller/certificaterequests/sync.go),
  [issuer/ca/setup.go](https://github.com/cert-manager/cert-manager/blob/v1.21.3/pkg/issuer/ca/setup.go),
  [policies/checks.go](https://github.com/cert-manager/cert-manager/blob/v1.21.3/internal/controller/certificates/policies/checks.go).
  Messages quoted here were also seen on a Kubernetes 1.37 kind cluster with
  cert-manager 1.21.3.
- `cmctl status certificate` reads the certificate's Secret
  ([certificate.go](https://github.com/cert-manager/cmctl/blob/v2.6.1/pkg/status/certificate/certificate.go)),
  which is why this skill does not use it.
