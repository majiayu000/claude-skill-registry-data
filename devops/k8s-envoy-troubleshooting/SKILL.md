---
name: k8s-envoy-troubleshooting
description: >-
  Use when an Envoy proxy on Kubernetes fails requests: clients get 503 "no healthy
  upstream", 503 "upstream connect error or disconnect/reset before headers. reset
  reason: remote connection failure", 404 with an empty body, or 504 "upstream request
  timeout", access logs show response flags (UH, UF, NR, NC, UT, UO, URX, UC), or Envoy
  crashes at start ("has unknown fields", "no such field", "route: unknown cluster").
  Covers Envoy run directly (a Deployment with its own bootstrap, a front proxy, a
  sidecar) and the proxy under Contour, Emissary or Gloo; reads the access log, the
  bootstrap and Envoy's read-only admin endpoints. Investigates with kubectl get and
  logs, and proposes fixes. Reads first and asks before changing anything.
license: Apache-2.0
metadata:
  verified-with: "kubernetes 1.37, envoy 1.40"
  verified-on: "2026-10-25"
---

# Envoy troubleshooting

Find out why Envoy does not pass a request on, and propose a fix. **Read first, ask
before changing.** Run the investigation commands freely. Run a command under an "Ask
first" line only after the user approves that exact command; if your credentials do not
allow it, give it to the user to run. Never run a "Proposed fix"; hand it to the user.

Envoy takes a request on a **listener**, matches a **route** by the Host header
(`domains`) and the path, and sends it to a **cluster**, whose **hosts** come from DNS
(`STRICT_DNS`, `LOGICAL_DNS`), a static list or a control plane (EDS). When it cannot,
it answers itself and records why: in the access log as a **response flag** (`UH`,
`UF`, `NR` ...) and `%RESPONSE_CODE_DETAILS%`, and in its stats. A standalone Envoy reads
its bootstrap once at start, so a config error stops it and an edited ConfigMap needs a
restart.

The commands use placeholders: `my-namespace`, `my-envoy` (the Envoy workload and its
ConfigMap), `my-envoy-admin` (a Service in front of the admin port, if there is one),
`my-app` (the backend) and `my-web` (a client). Replace them with the real names. Never
read Secrets. The bootstrap can hold TLS keys inline (`inline_string`): never repeat
them. Never fetch a full `/config_dump`, any `*_secrets` resource, or `/certs`; use
`config_dump` with `?resource=` for clusters, listeners and routes only.

## When to use

- Clients get 503, 504 or 404 from Envoy, or connections reset.
- Envoy pods crash at start or are not Ready.
- One backend gets no traffic through Envoy, or all of it.

Hand-offs, by skill name. When the evidence points elsewhere, continue with that skill;
if it is not installed, keep going with the steps here and tell the user which skill
would help:

- Envoy runs as an Istio sidecar or gateway: `k8s-istio-troubleshooting`; as Envoy
  Gateway's proxy: `k8s-envoy-gateway-troubleshooting`. Their control planes write the
  config, so start there.
- The backend Service has no endpoints, or a NetworkPolicy blocks Envoy:
  `k8s-network-troubleshooting`.
- The backend pods themselves fail: `k8s-workload-troubleshooting`.
- Contour: `kubectl get httpproxy -A` shows each HTTPProxy's status (`valid`, or
  `invalid` with the reason); invalid ones are ignored. Emissary and Gloo report errors
  in their resources' status and their controller logs.

## Investigate

Work through the steps in order. Stop when you have the cause and its evidence.

**1. See Envoy's pods and the client's result.**

```bash
kubectl get pods -n my-namespace -o wide
kubectl logs -n my-namespace deployment/my-web --tail=10
```

**2. Read Envoy's log**: the access log (if one is configured) with the response flag
and details for each request, and Envoy's own messages. After a crash, read the previous
container.

```bash
kubectl logs -n my-namespace deployment/my-envoy --tail=50
kubectl logs -n my-namespace deployment/my-envoy --previous --tail=20
```

**3. Read the bootstrap**: listeners, routes (`domains`, `match`, `cluster`) and clusters
(`type`, addresses, ports, timeouts). Do not repeat keys you see.

```bash
kubectl get deployment my-envoy -n my-namespace -o jsonpath='{.spec.template.spec.containers[0].args}{"\n"}{range .spec.template.spec.volumes[*]}{.name}{" "}{.configMap.name}{.secret.secretName}{"\n"}{end}'
kubectl get configmap my-envoy -n my-namespace -o yaml
kubectl get services,endpointslices -n my-namespace
```

**4. Ask Envoy's admin interface**, if it listens on a pod address and your credentials
allow `get` on `services/proxy` or `pods/proxy` (the built-in `view` role does not).
These are read-only: Envoy answers 405 to a GET on any endpoint that changes state. If
admin listens on `127.0.0.1` only (the docs' recommendation, Istio, Envoy Gateway,
Contour), there is no kubectl path to it; say so and work from the log.

```bash
kubectl get --raw /api/v1/namespaces/my-namespace/services/my-envoy-admin:admin/proxy/clusters
kubectl get --raw "/api/v1/namespaces/my-namespace/services/my-envoy-admin:admin/proxy/stats?filter=cluster.my-app."
kubectl get --raw "/api/v1/namespaces/my-namespace/services/my-envoy-admin:admin/proxy/config_dump?resource=static_route_configs"
kubectl get --raw /api/v1/namespaces/my-namespace/services/my-envoy-admin:admin/proxy/server_info
```

**5. Open the matching reference** and follow its steps:

| What you see | Reference |
|---|---|
| A response flag, an error body, `/clusters` and stats, DNS clusters, health checks, timeouts, circuit breakers | [references/responses-and-upstreams.md](references/responses-and-upstreams.md) |
| A crash at start, bootstrap errors, the admin interface and what it may show, images | [references/bootstrap-and-admin.md](references/bootstrap-and-admin.md) |

## Read the results

What the common findings mean (Envoy 1.40):

- **503 `no healthy upstream`, flag `UH`, details `no_healthy_upstream`**: the cluster has
  no healthy host. With `STRICT_DNS`, a name that does not exist counts as a successful
  lookup with no addresses: `/clusters` shows no host lines for the cluster,
  `membership_total` is 0, and `update_success` keeps rising, so the DNS name is the
  first thing to check against the Services.
- **503 `upstream connect error or disconnect/reset before headers. reset reason: remote
  connection failure`, flag `UF`**: Envoy reached a host but the connection was refused
  (a wrong port, nothing listening). The access log's
  `%UPSTREAM_TRANSPORT_FAILURE_REASON%` adds `delayed connect error: Connection refused`;
  since 1.39 it is no longer in the response body. `reset reason: connection timeout`
  means no answer within `connect_timeout` (a NetworkPolicy, a dropped port).
- **404 with an empty body, flag `NR`, details `route_not_found`**: no virtual host's
  `domains` match the request's Host header, or no route matches the path.
- **504 `upstream request timeout`, flag `UT`**: the backend did not answer within the
  route timeout (15s by default).
- **Envoy exits at start** with `Protobuf message (type envoy.config.bootstrap.v3.Bootstrap
  reason INVALID_ARGUMENT: ... no such field: '...') has unknown fields`: a misspelled or
  misplaced field; the `@ <path>` names where. `route: unknown cluster '...'` means a
  static route names a cluster that is not defined.

State the cause in one sentence, then the evidence you saw (the client's status and
body, the access-log flag and details, the bootstrap field, `/clusters`), then the
proposed fix.

## Proposed fix

Show each fix to the user before running it: what it changes and how to undo it.
Envoy's bootstrap serves every route and backend behind it: never change it yourself;
hand it to the user as a proposed fix. Prefer fixing the source (the Helm values, the
manifest in Git, or the control plane's resources). Never use the admin endpoints that
change state (`/quitquitquit`, `/healthcheck/fail`, `/drain_listeners`, `/logging`,
`/reset_counters`, `/runtime_modify`).

Fix the bootstrap in its source, apply it and restart Envoy so it reads it:

> Proposed fix: review before running. The agent does not run this.

```bash
kubectl apply -f my-envoy-configmap.yaml
kubectl rollout restart deployment/my-envoy -n my-namespace
# Undo: kubectl apply -f my-envoy-configmap-before.yaml, then restart my-envoy again
```

If an edited ConfigMap is already in place but Envoy still runs the old bootstrap,
restart it:

> Ask first: the agent runs this only after the user approves it.

```bash
kubectl rollout restart deployment/my-envoy -n my-namespace
# Undo: none needed; the restart only recreates the pods with the same template
```

## Sources

Checked against the Envoy 1.40 documentation and source (v1.40.1):

- [Admin interface](https://www.envoyproxy.io/docs/envoy/v1.40.1/operations/admin)
  and [command line options](https://www.envoyproxy.io/docs/envoy/v1.40.1/operations/cli).
- [Access logging](https://www.envoyproxy.io/docs/envoy/v1.40.1/configuration/observability/access_log/usage)
  and [response flags](https://www.envoyproxy.io/docs/envoy/v1.40.1/configuration/advanced/substitution_formatter).
- [Service discovery](https://www.envoyproxy.io/docs/envoy/v1.40.1/intro/arch_overview/upstream/service_discovery),
  [circuit breaking](https://www.envoyproxy.io/docs/envoy/v1.40.1/intro/arch_overview/upstream/circuit_breaking),
  [outlier detection](https://www.envoyproxy.io/docs/envoy/v1.40.1/intro/arch_overview/upstream/outlier),
  [cluster statistics](https://www.envoyproxy.io/docs/envoy/v1.40.1/configuration/upstream/cluster_manager/cluster_stats)
  and [timeouts](https://www.envoyproxy.io/docs/envoy/v1.40.1/faq/configuration/timeouts).
- [Installing Envoy](https://www.envoyproxy.io/docs/envoy/v1.40.1/start/install): image
  variants.
- Messages from the source:
  [router.cc](https://github.com/envoyproxy/envoy/blob/v1.40.1/source/common/router/router.cc),
  [admin.cc](https://github.com/envoyproxy/envoy/blob/v1.40.1/source/server/admin/admin.cc)
  and the [1.39 changelog](https://github.com/envoyproxy/envoy/blob/v1.40.1/changelogs/1.39.0.yaml)
  (transport failure reason out of the body). The docs say a GET to a mutating admin
  endpoint gets 400; the source returns 405.
- Contour [fundamentals](https://projectcontour.io/docs/main/config/fundamentals/),
  Emissary [debugging](https://emissary-ingress.dev/docs/4.0/topics/running/debugging/) and
  Gloo [debugging](https://docs.solo.io/gloo-edge/latest/operations/debugging_gloo/).
- The responses and log lines quoted here were seen on a Kubernetes 1.37 kind cluster with
  Envoy 1.40.1.
