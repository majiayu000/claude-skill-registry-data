---
name: k8s-envoy-gateway-troubleshooting
description: >-
  Use when Envoy Gateway (the Gateway API implementation by the Envoy project) does not
  route traffic in Kubernetes: a Gateway that is not Programmed ("AddressNotAssigned"),
  an HTTPRoute that is not Accepted ("NoMatchingListenerHostname", "NotAllowedByListeners")
  or whose ResolvedRefs is False ("BackendNotFound", "RefNotPermitted" without a
  ReferenceGrant), clients getting 404, 500 or 503 "no healthy upstream" from the
  gateway, a GatewayClass that is not Accepted, or BackendTrafficPolicy,
  ClientTrafficPolicy, SecurityPolicy and EnvoyProxy resources that do not apply.
  Investigates with kubectl get, describe, events and logs, and proposes fixes. Reads
  first and asks before changing anything.
license: Apache-2.0
metadata:
  verified-with: "kubernetes 1.37, envoy-gateway 1.9, gateway-api 1.6"
  verified-on: "2026-10-24"
---

# Envoy Gateway troubleshooting

Find out why Envoy Gateway does not route a request, and propose a fix. **Read first,
ask before changing.** Run the investigation commands freely. Run a command under an
"Ask first" line only after the user approves that exact command; if your credentials
do not allow it, give it to the user to run. Never run a "Proposed fix"; hand it to the
user.

A **GatewayClass** with controller `gateway.envoyproxy.io/gatewayclass-controller`
belongs to Envoy Gateway. For each **Gateway** of that class, Envoy Gateway runs an
Envoy Deployment and Service (by default in `envoy-gateway-system`, labelled
`gateway.envoyproxy.io/owning-gateway-name`). **HTTPRoutes** (and GRPC, TLS, TCP and UDP
routes) attach to a Gateway's listeners and send traffic to backends. Every object
reports what Envoy Gateway made of it in its status conditions, so the status usually
names the cause. Envoy Gateway's own policies (**BackendTrafficPolicy**,
**ClientTrafficPolicy**, **SecurityPolicy**, **EnvoyProxy**, **EnvoyPatchPolicy**)
attach to Gateways or routes.

The commands use placeholders: `my-namespace`, `my-gateway`, `my-app` (the route and
its Service) and `my-app.example.com`. Replace them with the real names. The built-in
`view` role cannot read Gateway API or Envoy Gateway objects (neither ships a read
role); if they are forbidden, say so and ask the user for them. Never read Secrets: not
TLS certificates referenced by listeners, not SecurityPolicy credentials, not the
`envoy` Secret the proxies mount. The Envoy image has no shell, and its admin interface
listens only on localhost, so there is no kubectl path to it; `egctl config envoy-proxy`
needs a port-forward and is left to the user.

## When to use

- Requests through a Gateway get 404, 500 or 503, or time out.
- `kubectl get gateways` shows `PROGRAMMED False`, or a route does not take effect.
- A policy (rate limit, timeout, auth, CORS) has no effect.

Hand-offs, by skill name. When the evidence points elsewhere, continue with that skill;
if it is not installed, keep going with the steps here and tell the user which skill
would help:

- The backend Service has no ready endpoints, or its pods fail:
  `k8s-network-troubleshooting`, `k8s-workload-troubleshooting`.
- The listener's certificate comes from cert-manager and is not issued:
  `k8s-cert-manager-troubleshooting`.
- Another Gateway API implementation (Istio, Cilium, a cloud controller) owns the
  GatewayClass, or no controller claims it (`Waiting for controller`):
  `k8s-gateway-api-troubleshooting` and that implementation's skill.
- A listener, ListenerSet or Gateway API CRD problem that is not specific to Envoy
  Gateway: `k8s-gateway-api-troubleshooting`.
- What an Envoy response flag, reset reason or cluster statistic means in general:
  `k8s-envoy-troubleshooting` (the proxy itself; Envoy Gateway writes its config).

## Investigate

Work through the steps in order. Stop when you have the cause and its evidence.

**1. See the GatewayClass and the Gateway**: Accepted and Programmed, the listeners and
the address.

```bash
kubectl get gatewayclasses
kubectl get gateways -A
kubectl get gateway my-gateway -n my-namespace -o jsonpath='{range .status.conditions[*]}{.type}={.status} {.reason}: {.message}{"\n"}{end}{range .status.listeners[*]}{.name}{" routes="}{.attachedRoutes}{" "}{.conditions}{"\n"}{end}'
```

**2. Read the route's status for each parent**: Accepted (did it attach to the
listener?) and ResolvedRefs (are its backends usable?).

```bash
kubectl get httproutes -A
kubectl get httproute my-app -n my-namespace -o jsonpath='{range .status.parents[*]}{.parentRef}{"\n"}{range .conditions[*]}{"  "}{.type}={.status} {.reason}: {.message}{"\n"}{end}{end}'
kubectl get httproute my-app -n my-namespace -o yaml
```

**3. Compare the route with the Gateway and the backends**: hostnames, `parentRefs`
(name, namespace, `sectionName`), the listener's `allowedRoutes`, and the backend
Services and ReferenceGrants.

```bash
kubectl get gateway my-gateway -n my-namespace -o jsonpath='{range .spec.listeners[*]}{.name}{" "}{.protocol}{" "}{.port}{" "}{.hostname}{" "}{.allowedRoutes}{"\n"}{end}'
kubectl get services,endpointslices -n my-namespace
kubectl get referencegrants -A
```

**4. Check Envoy Gateway and the proxy for the Gateway.**

```bash
kubectl get deployments,pods,services -n envoy-gateway-system -l gateway.envoyproxy.io/owning-gateway-name=my-gateway
kubectl logs -n envoy-gateway-system deployment/envoy-gateway --tail=100
kubectl get backendtrafficpolicies,clienttrafficpolicies,securitypolicies,envoyproxies,envoypatchpolicies -A
```

**5. Open the matching reference** and follow its steps:

| What you see | Reference |
|---|---|
| A route not Accepted, ResolvedRefs False, 404 or 500 responses, ReferenceGrants | [references/routes.md](references/routes.md) |
| GatewayClass or Gateway not Accepted or Programmed, no address, listener conflicts, policies without effect, the proxy | [references/gateways-and-policies.md](references/gateways-and-policies.md) |

## Read the results

What the common findings mean (Envoy Gateway 1.9, Gateway API 1.6):

- **Route `Accepted` `False`, reason `NoMatchingListenerHostname`** (`There were no
  hostname intersections between the HTTPRoute and this parent ref's Listener(s)`): the
  route's `hostnames` and the listener's `hostname` share no name; the route is not
  attached and requests for that host get 404.
- **`Accepted` `False`, `NotAllowedByListeners`**: the listener's `allowedRoutes` does
  not admit routes from the route's namespace or of its kind.
- **`ResolvedRefs` `False`, `BackendNotFound`** (`... service <ns>/<name> not found`):
  the backend Service does not exist. Envoy Gateway answers that rule with **500**.
- **`ResolvedRefs` `False`, `RefNotPermitted`** (`Backend ref to Service <ns>/<name> not
  permitted by any ReferenceGrant`): the backend is in another namespace and no
  ReferenceGrant there allows it. Also **500**.
- **Accepted and ResolvedRefs `True`, but 503 `no healthy upstream`**: the Service
  exists but has no ready endpoints (`BackendsAvailable` `False`, `EndpointsNotFound`).
- **Gateway `Programmed` `False`, `AddressNotAssigned`**: its Service is a LoadBalancer
  that got no address (no load balancer in the cluster, a quota, a cloud error).

State the cause in one sentence, then the evidence you saw (the condition, reason and
message, the spec fields), then the proposed fix.

## Proposed fix

Show each fix to the user before running it: what it changes and how to undo it.
Patching a route's hostnames or backend reference is reversible, so it goes under "Ask
first" and runs only after the user says yes. Creating ReferenceGrants (they let one
namespace's routes reach another's Services), changing Gateways, listeners, GatewayClasses
and Envoy Gateway policies change traffic and access for others: never run them
yourself; hand them to the user as proposed fixes. Prefer fixing the source. Write each
undo with the values you found.

Point a route at the Service that exists:

> Ask first: the agent runs this only after the user approves it.

```bash
kubectl patch httproute my-app -n my-namespace --type=json -p '[{"op": "replace", "path": "/spec/rules/0/backendRefs/0/name", "value": "my-app"}]'
# Undo: kubectl patch httproute my-app -n my-namespace --type=json -p '[{"op": "replace", "path": "/spec/rules/0/backendRefs/0/name", "value": "my-app-svc"}]'
```

Give a route the hostname its listener accepts (use the index of the hostname you
found):

> Ask first: the agent runs this only after the user approves it.

```bash
kubectl patch httproute my-app -n my-namespace --type=json -p '[{"op": "replace", "path": "/spec/hostnames/0", "value": "my-app.example.com"}]'
# Undo: kubectl patch httproute my-app -n my-namespace --type=json -p '[{"op": "replace", "path": "/spec/hostnames/0", "value": "app.example.com"}]'
```

## Sources

Checked against the Envoy Gateway 1.9 documentation and source (v1.9.2) and Gateway API
1.6:

- [Envoy Gateway troubleshooting](https://gateway.envoyproxy.io/docs/troubleshooting/)
  and the [quickstart](https://gateway.envoyproxy.io/docs/tasks/quickstart/).
- [Customize EnvoyProxy](https://gateway.envoyproxy.io/docs/tasks/operations/customize-envoyproxy/):
  the Service type and other proxy settings.
- [egctl](https://gateway.envoyproxy.io/docs/tasks/operations/egctl/).
- The v1.9.2 `install.yaml` release asset: it carries the Gateway API CRDs with the
  annotations `gateway.networking.k8s.io/bundle-version: v1.6.1` and
  `gateway.networking.k8s.io/channel: experimental`.
- Gateway API [HTTPRoute](https://gateway-api.sigs.k8s.io/reference/api-types/httproute/),
  [ReferenceGrant](https://gateway-api.sigs.k8s.io/reference/api-types/referencegrant/) and the
  [API specification](https://gateway-api.sigs.k8s.io/reference/api-spec/1.6/spec/):
  conditions and reasons.
- Status messages from the source:
  [route.go](https://github.com/envoyproxy/gateway/blob/v1.9.2/internal/gatewayapi/route.go)
  and [validate.go](https://github.com/envoyproxy/gateway/blob/v1.9.2/internal/gatewayapi/validate.go).
  The conditions and responses quoted here were seen on a Kubernetes 1.37 kind cluster
  with Envoy Gateway 1.9.2.
