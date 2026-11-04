---
name: k8s-istio-troubleshooting
description: >-
  Use when traffic fails in an Istio service mesh on Kubernetes: HTTP 403 "RBAC: access
  denied" from an AuthorizationPolicy, 503 "no healthy upstream" or "upstream connect
  error or disconnect/reset before headers", 404 from a route that does not match,
  "Connection reset by peer" after PeerAuthentication STRICT, sidecars that are not
  injected, VirtualService, DestinationRule, Gateway or ServiceEntry rules that do not
  apply, or istiod and proxy problems. Reads Envoy's access log and response flags
  (UH, NR, UF, URX, filter_chain_not_found), covers sidecar mode and ambient mode, and
  proposes fixes. Investigates with kubectl get, describe, events and logs, asks before
  reading Envoy's admin API inside a proxy. Reads first and asks before changing
  anything.
license: Apache-2.0
metadata:
  verified-with: "kubernetes 1.37, istio 1.31"
  verified-on: "2026-10-24"
---

# Istio troubleshooting

Find out why requests fail or behave unexpectedly in an Istio mesh, and propose a fix.
**Read first, ask before changing.** Run the investigation commands freely. Run a
command under an "Ask first" line only after the user approves that exact command; if
your credentials do not allow it, give it to the user to run. Never run a "Proposed
fix"; hand it to the user.

In **sidecar mode** every meshed pod has an Envoy container, `istio-proxy`, injected when
its namespace has `istio-injection=enabled` (or an `istio.io/rev` label). The client's
sidecar routes by **VirtualServices** and **DestinationRules** (subsets, load balancing,
TLS); the server's sidecar enforces **PeerAuthentication** (mTLS) and
**AuthorizationPolicies**. Each sidecar writes an access log line per request with a
**response flag** that says what Envoy did. In **ambient mode** the node's `ztunnel`
handles L4 and mTLS and an optional **waypoint** proxy handles L7.

The commands use placeholders: `my-namespace`, `my-app` (the server and its Service),
`my-web` (the client) and `my-pod`. Replace them with the real names. The built-in
`view` role cannot read Istio's resources (Istio adds nothing to it, and its own reader
role also grants Secrets); if they are forbidden, say so and ask the user for them.
Never read Secrets: not certificates, not `istio-ca-secret`, not gateway TLS Secrets.
For that reason do not run `istioctl analyze` against the cluster (it reads Secrets), do
not use `istioctl proxy-config secret`, and do not fetch Envoy's full `config_dump` or
`/certs`.

## When to use

- A request inside the mesh, or through an Istio gateway, returns 403, 404, 503 or a
  reset, while the app itself is fine.
- Routing rules (weights, subsets, headers) or policies do not take effect.
- A pod has no `istio-proxy` container although its namespace is in the mesh.
- istiod is down, or proxies do not get configuration.

Hand-offs, by skill name. When the evidence points elsewhere, continue with that skill;
if it is not installed, keep going with the steps here and tell the user which skill
would help:

- The Service has no endpoints, or the pods are not Ready: `k8s-network-troubleshooting`
  and `k8s-workload-troubleshooting`.
- A Kubernetes Gateway API route that Istio does not accept:
  `k8s-gateway-api-troubleshooting` (the objects' status) and the reference here.
- What an Envoy response flag, reset reason or cluster statistic means in general:
  `k8s-envoy-troubleshooting` (the proxy itself; Istio writes its config).

## Investigate

Work through the steps in order. Stop when you have the cause and its evidence.

**1. Check the mesh membership** of the client and the server: the namespace labels,
and whether each pod has an `istio-proxy` container.

```bash
kubectl get namespace my-namespace --show-labels
kubectl get pods -n my-namespace -o jsonpath='{range .items[*]}{.metadata.name}{" "}{.spec.containers[*].name}{" "}{.spec.initContainers[*].name}{"\n"}{end}'
kubectl get pods -n istio-system
```

**2. Read the client's error and both sidecars' access logs.** The response flag after
the status code says what went wrong.

```bash
kubectl logs -n my-namespace deployment/my-web -c istio-proxy --tail=20
kubectl logs -n my-namespace deployment/my-app -c istio-proxy --tail=20
```

A log line reads `"GET / HTTP/1.1" 503 UH no_healthy_upstream ... outbound|80|v2|my-app...`:
status, response flag, details, and the Envoy cluster (direction, port, subset, host).
Access logs must be on (`meshConfig.accessLogFile`, or a Telemetry resource); if they
are empty, say so.

**3. Read the Istio resources for the host and the server.**

```bash
kubectl get virtualservices,destinationrules,gateways,serviceentries,sidecars -A
kubectl get authorizationpolicies,peerauthentications,requestauthentications -A
kubectl get virtualservice my-app -n my-namespace -o yaml
kubectl get destinationrule my-app -n my-namespace -o yaml
kubectl get pods -n my-namespace --show-labels
```

**4. If the cause is still open, ask the proxy itself** through its admin API, with GET
only, on the pod that logs the error. This runs a program in the user's pod, so ask
first:

> Ask first: the agent runs this only after the user approves it.

```bash
kubectl exec my-pod -n my-namespace -c istio-proxy -- pilot-agent request GET clusters
kubectl exec my-pod -n my-namespace -c istio-proxy -- pilot-agent request GET stats
```

`clusters` lists each Envoy cluster with its endpoints and their health. Never send any
method other than GET, and never request `config_dump` without a `resource` filter or
`certs`.

**5. Open the matching reference** and follow its steps:

| What you see | Reference |
|---|---|
| 503 `UH`, `UF`, `URX`, 404 `NR`, `upstream connect error`, routing that does not apply, subsets, ServiceEntries, gateways | [references/routing.md](references/routing.md) |
| 403 `RBAC: access denied`, `Connection reset by peer`, `filter_chain_not_found`, mTLS, injection, istiod, ambient | [references/security-and-injection.md](references/security-and-injection.md) |

## Read the results

What the common findings mean (Istio 1.31):

- **403 with the body `RBAC: access denied`, and the server's sidecar logs `403 -
  rbac_access_denied_matched_policy[...]`**: an AuthorizationPolicy denies it.
  `[none]` means an ALLOW policy selects the workload and no rule matched this request
  (a principal, namespace, path or method that is not listed).
- **503 `UH` `no_healthy_upstream`** on the client's sidecar, with a subset in the
  cluster name (`outbound|80|v2|...`): the route points at a DestinationRule subset
  whose labels match no ready pod.
- **404 `NR`** (no route) on the client or a gateway: no VirtualService or route matches
  the host, path or port.
- **`upstream connect error or disconnect/reset before headers. reset reason: ...`**
  (with `UF` or `URX`): Envoy could not connect to, or keep, the upstream: the app is
  down, the port is wrong, or the mTLS settings of client and server disagree.
- **The client gets `Connection reset by peer`, and the server's sidecar logs `NR
  filter_chain_not_found`**: the server requires mTLS (PeerAuthentication `STRICT`) and
  the client sent plaintext, usually because it has no sidecar.

State the cause in one sentence, then the evidence you saw (the access log line and its
flag, the resource and the field), then the proposed fix.

## Proposed fix

Show each fix to the user before running it: what it changes and how to undo it. Istio
resources change traffic for every client of a host, and policies change who may talk
to whom: never create, change or delete them yourself; hand the change to the user as
a proposed fix, in the source they are deployed from. Restarting a workload so it gets
a sidecar is reversible, so it goes under "Ask first". Write each undo with the values
you found.

Restart a workload after its namespace was added to the mesh, so its pods get a
sidecar:

> Ask first: the agent runs this only after the user approves it.

```bash
kubectl rollout restart deployment/my-web -n my-namespace
# Undo: kubectl rollout undo deployment/my-web -n my-namespace
```

## Sources

Checked against the Istio 1.31 documentation and source (1.31.3):

- [Common problems](https://istio.io/latest/docs/ops/common-problems/network-issues/),
  [security problems](https://istio.io/latest/docs/ops/common-problems/security-issues/)
  and [injection problems](https://istio.io/latest/docs/ops/common-problems/injection/).
- [Diagnostic tools](https://istio.io/latest/docs/ops/diagnostic-tools/) and
  [Envoy access logs](https://istio.io/latest/docs/tasks/observability/logs/access-log/).
- [Traffic management](https://istio.io/latest/docs/concepts/traffic-management/),
  [security](https://istio.io/latest/docs/concepts/security/) and
  [authorization policy](https://istio.io/latest/docs/reference/config/security/authorization-policy/).
- [Protocol selection](https://istio.io/latest/docs/ops/configuration/traffic-management/protocol-selection/)
  and [ambient mode](https://istio.io/latest/docs/ambient/overview/).
- [Helm installation](https://istio.io/latest/docs/setup/install/helm/).
- Envoy's [response flags](https://www.envoyproxy.io/docs/envoy/latest/configuration/observability/access_log/usage#command-operators)
  and [admin interface](https://www.envoyproxy.io/docs/envoy/latest/operations/admin).
- `istioctl analyze` reads Secrets (its gateway analyzer:
  [secret.go](https://github.com/istio/istio/blob/1.31.3/pkg/config/analysis/analyzers/gateway/secret.go)),
  which is why this skill does not run it. The log lines quoted here were seen on a
  Kubernetes 1.37 kind cluster with Istio 1.31.3 in sidecar mode.
