---
name: k8s-gateway-api-troubleshooting
description: >-
  Use when Gateway API objects in Kubernetes do not route, whatever the implementation:
  a GatewayClass stuck "Waiting for controller" or not Accepted, a Gateway with no
  address or PROGRAMMED Unknown or False ("ListenersNotValid", "AddressNotAssigned"), a
  listener that is not Programmed ("InvalidCertificateRef", "ProtocolConflict",
  "InvalidRouteKinds", "RefNotPermitted"), an HTTPRoute, GRPCRoute or TLSRoute that is
  not Accepted ("NoMatchingParent", "NotAllowedByListeners",
  "NoMatchingListenerHostname") or has no status at all, ResolvedRefs False
  ("BackendNotFound", "RefNotPermitted" without a ReferenceGrant), ListenerSets,
  BackendTLSPolicy, and Gateway API CRD versions or channels that do not match.
  Investigates with kubectl get and describe, and proposes fixes. Reads first and asks
  before changing anything.
license: Apache-2.0
metadata:
  verified-with: "kubernetes 1.37, gateway-api 1.6, envoy-gateway 1.9"
  verified-on: "2026-10-31"
---

# Gateway API troubleshooting

Find out why a Gateway API object does not route, from the objects' status, and propose
a fix. **Read first, ask before changing.** Run the investigation commands freely. Run a
command under an "Ask first" line only after the user approves that exact command; if
your credentials do not allow it, give it to the user to run. Never run a "Proposed fix";
hand it to the user.

Gateway API splits routing across roles, and each object reports what its controller
made of it in `status.conditions`:

- A **GatewayClass** (cluster-scoped) names a `controllerName`. The implementation whose
  controller claims that name accepts the class.
- A **Gateway** uses a class and has **listeners** (name, port, protocol, optional
  hostname, TLS, `allowedRoutes`). A **ListenerSet** adds listeners to a Gateway from
  another object, if the Gateway's `allowedListeners` admits it.
- **Routes** (HTTPRoute, GRPCRoute, TLSRoute, TCPRoute, UDPRoute) attach to a Gateway or
  one listener through `parentRefs`, and send traffic to `backendRefs`. A route reports
  its status per parent, under `status.parents`.
- A **ReferenceGrant** in a namespace lets objects in another namespace refer to its
  objects (a route to a backend Service, a listener to a certificate).
- A **BackendTLSPolicy** makes the Gateway use TLS to a backend Service.

This skill covers what the API says and works the same in every implementation. How the
data plane behaves is the implementation's part.

The commands use placeholders: `my-namespace`, `my-gateway`, `my-app` (the route and
its Service) and `my-app.example.com`. Replace them with the real names. The built-in
`view` role cannot read Gateway API objects (the project ships no read role); if they
are forbidden, say so and ask the user for them. Never read Secrets: not the TLS
certificates that listeners refer to, not CA bundles in Secrets. A listener's status
says whether its certificate resolves; that is enough.

## When to use

- A Gateway has no address, or `kubectl get gateways` shows `PROGRAMMED` `Unknown` or
  `False`.
- A route exists but requests for its host or path get 404, or one listener (often
  https) does not answer while another works.
- A route in another namespace, or a ListenerSet, does not attach to a shared Gateway.
- Applying Gateway API objects or CRDs fails (`no matches for kind`, a version not
  served, the `safe-upgrades` admission policy).

Hand-offs, by skill name. When the evidence points elsewhere, continue with that skill;
if it is not installed, keep going with the steps here and tell the user which skill
would help:

- The class belongs to Envoy Gateway (`gateway.envoyproxy.io/gatewayclass-controller`),
  and the objects are Accepted but traffic still fails, or its own policies are
  involved: `k8s-envoy-gateway-troubleshooting`.
- The class belongs to Istio (`istio.io/gateway-controller`):
  `k8s-istio-troubleshooting`. To Cilium (`io.cilium/gateway-controller`):
  `k8s-cilium-troubleshooting`.
- Everything is Accepted and resolved, but the backend Service has no ready endpoints
  or its pods fail: `k8s-network-troubleshooting`, `k8s-workload-troubleshooting`.
- The listener's certificate comes from cert-manager and is not issued:
  `k8s-cert-manager-troubleshooting`.
- Applying a CRD or an object is refused by a webhook or an admission policy you did
  not expect: `k8s-api-troubleshooting`.

## Investigate

Work through the steps in order. Stop when you have the cause and its evidence.

**1. See the classes, the Gateways and the routes.**

```bash
kubectl get gatewayclasses
kubectl get gateways -A
kubectl get httproutes,grpcroutes -A
kubectl get listenersets,referencegrants,backendtlspolicies -A
```

If a kind is unknown to the cluster, see step 6.

**2. Read the GatewayClass**: its controller and whether that controller accepted it.

```bash
kubectl get gatewayclass my-class -o jsonpath='{.spec.controllerName}{"\n"}{range .status.conditions[*]}{.type}={.status} {.reason}: {.message}{"\n"}{end}'
```

**3. Read the Gateway and each listener**: Accepted and Programmed for the Gateway, then
per listener Accepted, Programmed, ResolvedRefs, Conflicted and the number of attached
routes.

```bash
kubectl get gateway my-gateway -n my-namespace -o jsonpath='{range .status.conditions[*]}{.type}={.status} {.reason}: {.message}{"\n"}{end}{range .status.listeners[*]}{.name}{" routes="}{.attachedRoutes}{"\n"}{range .conditions[*]}{"  "}{.type}={.status} {.reason}: {.message}{"\n"}{end}{end}'
kubectl get gateway my-gateway -n my-namespace -o jsonpath='{range .spec.listeners[*]}{.name}{" "}{.protocol}{" "}{.port}{" "}{.hostname}{" allowedRoutes="}{.allowedRoutes}{" tls="}{.tls}{"\n"}{end}'
```

**4. Read the route's status for each parent**: Accepted (did it attach?) and
ResolvedRefs (are its backends usable?). An empty `status` means no controller wrote
anything for it.

```bash
kubectl get httproute my-app -n my-namespace -o jsonpath='{range .status.parents[*]}{.parentRef}{"\n"}{range .conditions[*]}{"  "}{.type}={.status} {.reason}: {.message}{"\n"}{end}{end}'
kubectl get httproute my-app -n my-namespace -o jsonpath='{.spec.parentRefs}{"\n"}{.spec.hostnames}{"\n"}{range .spec.rules[*]}{.backendRefs}{"\n"}{end}'
```

**5. Check what the route points at**: the backend Services and their ports, and
ReferenceGrants in the backend's namespace for a cross-namespace reference.

```bash
kubectl get services -n my-namespace
kubectl get service my-app -n my-namespace -o jsonpath='{range .spec.ports[*]}{.name}{" "}{.port}{" "}{.appProtocol}{"\n"}{end}'
kubectl get referencegrants -n my-namespace -o yaml
```

**6. Check the CRDs**: which Gateway API version and channel is installed, and which API
versions are served.

```bash
kubectl api-resources --api-group=gateway.networking.k8s.io
kubectl get crd gateways.gateway.networking.k8s.io -o jsonpath='{.metadata.annotations.gateway\.networking\.k8s\.io/bundle-version}{" "}{.metadata.annotations.gateway\.networking\.k8s\.io/channel}{"\n"}'
kubectl get crd tlsroutes.gateway.networking.k8s.io -o jsonpath='{range .spec.versions[*]}{.name}{" served="}{.served}{" storage="}{.storage}{"\n"}{end}'
kubectl get validatingadmissionpolicies
```

**7. Open the matching reference** and follow its steps:

| What you see | Reference |
|---|---|
| A route not Accepted or with no status, ResolvedRefs False, ReferenceGrants, BackendTLSPolicy, GRPCRoute and TLSRoute | [references/routes.md](references/routes.md) |
| A GatewayClass or Gateway not Accepted or Programmed, listener conditions, TLS certificates, ListenerSets, CRD versions and channels | [references/gateways-and-listeners.md](references/gateways-and-listeners.md) |

## Read the results

Conditions and reasons are from the Gateway API 1.6 specification; the quoted messages
are Envoy Gateway 1.9's. Other implementations use the same reasons with their own
messages.

- **GatewayClass `Accepted` `Unknown`, reason `Pending`** (`Waiting for controller`): no
  running controller claims its `controllerName`. A typo in the name, an implementation
  that is not installed or not running, or a class meant for another cluster. Every
  Gateway of the class then shows `Accepted` and `Programmed` `Unknown`, `Pending`, and
  gets no address.
- **GatewayClass `Accepted` `False`, `InvalidParameters`**: its `parametersRef` points at
  an object that does not exist or is malformed.
- **Gateway `Accepted` `False`, `ListenersNotValid`** (`No listeners are valid: ...`):
  every listener is invalid; read their conditions. When only some are invalid, the
  Gateway stays Accepted and Programmed and only those listeners fail.
- **Gateway `Programmed` `False`, `AddressNotAssigned`**: the implementation could not
  give it an address, for example a LoadBalancer Service with no load balancer, or no
  valid listener to serve.
- **Listener `ResolvedRefs` `False`, `InvalidCertificateRef`** (`No valid secrets exist:
  certificate refs 0: Secret my-namespace/my-app-tls does not exist.`): the TLS
  certificate the listener names does not exist or is not a valid TLS Secret. The
  listener is `Programmed` `False` and nothing serves its port. Do not read the Secret;
  the condition is the evidence.
- **Listener `Conflicted` `True`, `ProtocolConflict`** or `HostnameConflict`: listeners
  on the same port disagree on protocol, or share a hostname.
- **Listener `ResolvedRefs` `False`, `InvalidRouteKinds`**: `allowedRoutes.kinds` names a
  route kind the implementation does not support on that protocol.
- **Route `Accepted` `False`, `NoMatchingParent`** (`No listeners match this parent
  ref`): the parent ref's `sectionName` or `port` matches no listener of the Gateway.
- **Route `Accepted` `False`, `NotAllowedByListeners`** (`No listeners included by this
  parent ref allowed this attachment.`): the listener's `allowedRoutes` does not admit
  the route's namespace or kind. The default, which the API server fills in, is
  `namespaces.from: Same`: only routes from the Gateway's own namespace attach.
- **Route `Accepted` `False`, `NoMatchingListenerHostname`**: the route's `hostnames`
  and the listener's `hostname` do not intersect.
- **A route with no `status.parents` at all**: no controller considers itself
  responsible. The `parentRefs` name a Gateway that does not exist (a typo, the wrong
  namespace), or one whose class nobody accepts.
- **Route `ResolvedRefs` `False`, `BackendNotFound`** or **`RefNotPermitted`**: the
  backend does not exist, or is in another namespace without a ReferenceGrant there.
- **Route Accepted and resolved, but requests still fail**: the API side is done; look
  at the backend's endpoints and at the implementation (hand-offs above).

State the cause in one sentence, then the evidence you saw (the object, the condition,
its reason and message, the spec fields that disagree), then the proposed fix.

## Proposed fix

Show each fix to the user before running it: what it changes and how to undo it. Fix
the object that is wrong, and prefer fixing it in its source (Git, a Helm chart), since a
controller or a GitOps tool may set it back.

A route belongs to the team that publishes the app, so correcting a route's
`parentRefs`, hostnames or backend is reversible and goes under "Ask first". A Gateway,
its listeners and `allowedRoutes`, a GatewayClass, a ReferenceGrant and the CRDs are
shared: changing them changes who can route what for every team on the Gateway. Never
run those yourself; hand them to the Gateway's owners as proposed fixes. A
GatewayClass's `controllerName` cannot be changed after it is created. Write each undo
with the values you found.

Attach a route to the listener that exists (use the index of the parent ref you found):

> Ask first: the agent runs this only after the user approves it.

```bash
kubectl patch httproute my-app -n my-namespace --type=json -p '[{"op": "replace", "path": "/spec/parentRefs/0/sectionName", "value": "http"}]'
# Undo: kubectl patch httproute my-app -n my-namespace --type=json -p '[{"op": "replace", "path": "/spec/parentRefs/0/sectionName", "value": "web"}]'
```

Let a listener admit routes from a team's namespace as well as its own. A selector
replaces `Same`, so it must also match the Gateway's namespace, or the routes already
attached there are dropped; the `kubernetes.io/metadata.name` label is on every
namespace. This changes who can attach routes to a shared Gateway, so the agent does not
run it:

> Proposed fix: review before running. The agent does not run this.

```bash
kubectl patch gateway my-gateway -n my-namespace --type=json -p '[{"op": "replace", "path": "/spec/listeners/0/allowedRoutes", "value": {"namespaces": {"from": "Selector", "selector": {"matchExpressions": [{"key": "kubernetes.io/metadata.name", "operator": "In", "values": ["my-namespace", "my-other-namespace"]}]}}}}]'
# Undo: kubectl patch gateway my-gateway -n my-namespace --type=json -p '[{"op": "replace", "path": "/spec/listeners/0/allowedRoutes", "value": {"namespaces": {"from": "Same"}}}]'
```

Move a Gateway to the class whose controller runs. Its implementation then takes the
Gateway over, so the agent does not run it:

> Proposed fix: review before running. The agent does not run this.

```bash
kubectl patch gateway my-gateway -n my-namespace --type=merge -p '{"spec": {"gatewayClassName": "my-working-class"}}'
# Undo: kubectl patch gateway my-gateway -n my-namespace --type=merge -p '{"spec": {"gatewayClassName": "my-class"}}'
```

A missing listener certificate is fixed by creating or issuing it (for example a
cert-manager Certificate whose `secretName` is the Secret the listener names), never by
reading or copying another Secret. Give the user the name and namespace from the
listener's condition.

## Sources

Checked against the Gateway API 1.6 specification and source (v1.6.3), and on a
Kubernetes 1.37 kind cluster with Envoy Gateway 1.9.2 (Gateway API CRDs v1.6.1,
experimental channel):

- [API specification 1.6](https://gateway-api.sigs.k8s.io/reference/api-spec/1.6/spec/):
  the condition types and reasons.
- Their definitions in the source:
  [shared_types.go](https://github.com/kubernetes-sigs/gateway-api/blob/v1.6.3/apis/v1/shared_types.go)
  (route conditions),
  [gateway_types.go](https://github.com/kubernetes-sigs/gateway-api/blob/v1.6.3/apis/v1/gateway_types.go)
  (Gateway and listener conditions) and
  [gatewayclass_types.go](https://github.com/kubernetes-sigs/gateway-api/blob/v1.6.3/apis/v1/gatewayclass_types.go)
  (GatewayClass conditions, `SupportedVersion`).
- [Gateway](https://gateway-api.sigs.k8s.io/reference/api-types/gateway/),
  [HTTPRoute](https://gateway-api.sigs.k8s.io/reference/api-types/httproute/),
  [ReferenceGrant](https://gateway-api.sigs.k8s.io/reference/api-types/referencegrant/),
  [ListenerSet](https://gateway-api.sigs.k8s.io/reference/api-types/listenerset/) and
  [BackendTLSPolicy](https://gateway-api.sigs.k8s.io/reference/api-types/policy/backendtlspolicy/).
- [Cross-namespace routing](https://gateway-api.sigs.k8s.io/guides/multiple-ns/) and
  [Security model](https://gateway-api.sigs.k8s.io/concepts/security-model/): the roles,
  `allowedRoutes` and ReferenceGrants.
- [Versioning](https://gateway-api.sigs.k8s.io/docs/concepts/versioning/) and the
  [v1.6.3 release](https://github.com/kubernetes-sigs/gateway-api/releases/tag/v1.6.3):
  channels, the `bundle-version` and `channel` CRD annotations, the
  `safe-upgrades.gateway.networking.k8s.io` admission policy in the install files.
- The [v1.7.0 release notes](https://github.com/kubernetes-sigs/gateway-api/releases/tag/v1.7.0):
  HTTPRoute retries move to the Standard channel; nothing here changes.
- The messages quoted are Envoy Gateway 1.9.2's, seen on the kind cluster; its
  [source](https://github.com/envoyproxy/gateway/tree/v1.9.2/internal/gatewayapi) has
  them too.
