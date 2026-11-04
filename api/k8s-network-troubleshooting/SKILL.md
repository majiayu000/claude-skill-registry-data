---
name: k8s-network-troubleshooting
description: >-
  Use when traffic does not reach a workload in Kubernetes although its pods are
  running: a Service with no endpoints, a wrong selector or targetPort, connection
  refused or time-outs between pods, DNS names that do not resolve (NXDOMAIN, "server
  can't find"), a NetworkPolicy blocking traffic, or an Ingress or Gateway API route
  that does not route. Investigates with kubectl get and describe, asks before checks
  inside a container, and proposes fixes. Reads first and asks before changing anything.
license: Apache-2.0
metadata:
  verified-with: "kubernetes 1.37, gateway-api 1.6"
  verified-on: "2026-10-24"
---

# Kubernetes network troubleshooting

Find out why traffic does not get from a client to a workload, and propose a fix.
**Read first, ask before changing.** Run the investigation commands freely. Run a
command under an "Ask first" line only after the user approves that exact command; if
your credentials do not allow it, give it to the user to run. Never run a "Proposed
fix"; hand it to the user.

Follow the path of a request: the client resolves the Service's name (DNS), connects
to the Service's port, the Service forwards to the `targetPort` of its ready endpoints,
and NetworkPolicies on both sides must allow it. Find the first step that fails.

The commands use placeholders: `my-namespace` and `my-app` (the target Service and its
workload), `my-other-namespace` and `my-web` (the client), and `my-pod`. Replace them
with the real names. Never read Secrets. If output contains passwords, tokens or keys,
do not repeat them.

## When to use

- A client gets `connection refused`, time-outs, `502`/`503`, or "no endpoints" when
  calling a Service, while the target pods are `Running`.
- A name does not resolve: `NXDOMAIN`, "server can't find", "bad address".
- Traffic stopped after a NetworkPolicy was added, or between namespaces.
- An Ingress, Gateway or HTTPRoute does not route to its backend.

Hand-offs, by skill name. When the evidence points elsewhere, continue with that skill;
if it is not installed, keep going with the steps here and tell the user which skill
would help:

- The target pods are not `Running` or not Ready (crash, probe, image, Pending):
  `k8s-workload-troubleshooting`.
- A node is `NotReady`, or the network plugin's pods fail on a node:
  `k8s-node-troubleshooting`.
- CoreDNS itself fails (its pods crash, its logs show errors, external names or one
  domain fail for every client, a Corefile edit): `k8s-coredns-troubleshooting`.
- On AKS, a LoadBalancer Service stays `<pending>` with `SyncLoadBalancerFailed`, or its
  IP does not take traffic: `k8s-aks-troubleshooting`.
- A GatewayClass, Gateway, listener or route is not Accepted or Programmed (a class
  waiting for its controller, a route that does not attach, a listener certificate that
  does not resolve), or the Gateway API CRDs do not match: `k8s-gateway-api-troubleshooting`.

## Investigate

Work through the steps in order. Stop when you have the cause and its evidence.

**1. Check the Service and its endpoints.** An EndpointSlice lists the ready pod
addresses behind the Service; none means the selector matches no ready pod.

```bash
kubectl get service my-app -n my-namespace -o wide
kubectl describe service my-app -n my-namespace
kubectl get endpointslices -n my-namespace -l kubernetes.io/service-name=my-app -o wide
```

**2. Compare the Service with the pods.** The selector must match the pod labels, and
the `targetPort` must be a port the container listens on (a number, or a port name from
the pod spec).

```bash
kubectl get pods -n my-namespace --show-labels -o wide
kubectl get service my-app -n my-namespace -o jsonpath='{.spec.selector}{"\n"}{.spec.ports}{"\n"}'
kubectl get pods -n my-namespace -l app=my-app -o jsonpath='{range .items[*]}{.metadata.name}{" "}{.spec.containers[*].ports}{"\n"}{end}'
```

Use the Service's real selector in place of `app=my-app`.

**3. Read the client's own errors**, in its logs or the user's report. `connection
refused` means something answered and refused (often a wrong port); a time-out means
nothing answered (often a NetworkPolicy, or no route); a name error means DNS.

```bash
kubectl logs deployment/my-web -n my-other-namespace --tail=50
```

**4. Look for NetworkPolicies** on both sides: ingress where the target runs, egress
where the client runs.

```bash
kubectl get networkpolicy -n my-namespace
kubectl get networkpolicy -n my-other-namespace
kubectl describe networkpolicy -n my-namespace
kubectl get namespace my-other-namespace --show-labels
```

**5. If a name does not resolve**, check CoreDNS (it keeps the `k8s-app=kube-dns`
label).

```bash
kubectl get pods -n kube-system -l k8s-app=kube-dns
kubectl logs -n kube-system -l k8s-app=kube-dns --tail=50
kubectl get endpointslices -n kube-system -l kubernetes.io/service-name=kube-dns
```

**6. Test from inside the client**, when the objects look right but the cause is still
open. This runs a program in the user's container, so ask first. It needs `wget` and
`nslookup` in the image (busybox has both; minimal images often have neither, and the
command then fails with "executable file not found"):

> Ask first: the agent runs this only after the user approves it.

```bash
kubectl exec deployment/my-web -n my-other-namespace -- nslookup my-app.my-namespace
kubectl exec deployment/my-web -n my-other-namespace -- wget -qO- -T 2 http://my-app.my-namespace:80/
```

To tell a Service problem from a pod problem, call one endpoint's address directly
(from step 1) on the target port, the same way.

**7. Open the matching reference** and follow its steps:

| What you see | Reference |
|---|---|
| No endpoints, wrong selector or `targetPort`, refused connections | [references/services.md](references/services.md) |
| `NXDOMAIN`, "server can't find", "bad address", CoreDNS errors | [references/dns.md](references/dns.md) |
| Time-outs, a NetworkPolicy in either namespace | [references/networkpolicy.md](references/networkpolicy.md) |
| Ingress, IngressClass, Gateway, HTTPRoute | [references/ingress-gateway.md](references/ingress-gateway.md) |

## Read the results

What the common findings mean (Kubernetes 1.37):

- **No endpoints** in the Service's EndpointSlices (or `Endpoints:` empty in `describe
  service`): no Ready pod matches the selector. Either the selector does not match the
  pod labels, or the matching pods are not Ready.
- **Endpoints with `ready: false`**: the pods match but are not Ready, so they get no
  traffic (unless the Service sets `publishNotReadyAddresses: true`). Hand over to
  `k8s-workload-troubleshooting`.
- **`targetPort` defaults to `port`** when it is not set. A Service on port 80 in front
  of an app on 8080 needs `targetPort: 8080`. A named `targetPort` must match a port name
  the pods actually declare.
- **A short name resolves only in the client's own namespace**: the pod's DNS search
  list starts with its own namespace. From another namespace use
  `my-app.my-namespace` or `my-app.my-namespace.svc.cluster.local`.
- **NetworkPolicy**: a pod is open until some policy selects it for a direction; then
  only what some policy allows gets through. Policies add up; they never deny. A
  connection needs both the client's egress and the target's ingress to allow it. A
  policy has no effect without a network plugin that enforces it.
- **An egress policy that isolates the client also blocks DNS** unless it allows traffic
  to the cluster's DNS service.

State the cause in one sentence, then the evidence you saw (the selector and labels,
the ports, the policy, the error), then the proposed fix.

## Proposed fix

Show each fix to the user before running it: what it changes and how to undo it.
Patching a Service's selector or port, or an Ingress or route field, is reversible, so
it goes under "Ask first" and runs only after the user says yes. Creating or deleting objects (a NetworkPolicy, a Service) and editing CoreDNS are
never run by you: hand them to the user as proposed fixes and say why. Prefer fixing
the source the objects are deployed from (manifest, Helm values, GitOps repository)
when there is one. Write each undo with the values you found.

Point a Service's selector at the labels the pods really have:

> Ask first: the agent runs this only after the user approves it.

```bash
kubectl patch service my-app -n my-namespace --type=merge -p '{"spec": {"selector": {"app": "my-app"}}}'
# Undo: kubectl patch service my-app -n my-namespace --type=merge -p '{"spec": {"selector": {"app": "my-app-v1"}}}'
```

A merge patch on `selector` replaces only the keys it names; to remove a key, set it to
`null` in the patch.

Send a Service's traffic to the port the container listens on:

> Ask first: the agent runs this only after the user approves it.

```bash
kubectl patch service my-app -n my-namespace --type=json -p '[{"op": "replace", "path": "/spec/ports/0/targetPort", "value": 80}]'
# Undo: kubectl patch service my-app -n my-namespace --type=json -p '[{"op": "replace", "path": "/spec/ports/0/targetPort", "value": 8080}]'
```

Allow a client namespace through a NetworkPolicy. This creates a new policy, which can
open traffic wider than intended, so a human reviews and applies it: see
[references/networkpolicy.md](references/networkpolicy.md).

## Sources

Checked against the Kubernetes 1.37 documentation and Gateway API 1.6:

- [Service](https://kubernetes.io/docs/concepts/services-networking/service/): selectors,
  `port` and `targetPort`, named ports, Services without selectors.
- [EndpointSlices](https://kubernetes.io/docs/concepts/services-networking/endpoint-slices/):
  the `kubernetes.io/service-name` label, the `ready`, `serving` and `terminating`
  conditions, `publishNotReadyAddresses`.
- [Connecting Applications with Services](https://kubernetes.io/docs/tutorials/services/connect-applications-service/):
  `describe service` output.
- [Debug Services](https://kubernetes.io/docs/tasks/debug/debug-application/debug-service/):
  the order of checks, testing from inside a pod.
- [DNS for Services and Pods](https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/)
  and [Debugging DNS Resolution](https://kubernetes.io/docs/tasks/administer-cluster/dns-debugging-resolution/):
  names, the search list, CoreDNS checks.
- [Network Policies](https://kubernetes.io/docs/concepts/services-networking/network-policies/):
  isolation, additive rules, both directions, DNS with egress policies,
  `kubernetes.io/metadata.name`.
- [Ingress](https://kubernetes.io/docs/concepts/services-networking/ingress/): controllers,
  IngressClass and the default class, backends.
- [Gateway API specification](https://gateway-api.sigs.k8s.io/reference/api-spec/1.6/spec/),
  [ReferenceGrant](https://gateway-api.sigs.k8s.io/reference/api-types/referencegrant/)
  and the condition reasons in
  [shared_types.go](https://github.com/kubernetes-sigs/gateway-api/blob/main/apis/v1/shared_types.go).
