---
name: k8s-cilium-troubleshooting
description: >-
  Use when networking fails on a Kubernetes cluster that runs Cilium as its CNI: traffic
  between pods dropped or timing out after a CiliumNetworkPolicy or
  CiliumClusterwideNetworkPolicy, "Policy denied" drops in Hubble, DNS that stops
  resolving after an egress policy, HTTP 403 "Access denied" from an L7 rule, toFQDNs
  rules that do not match, pods stuck ContainerCreating with "unable to connect to
  Cilium agent", Cilium agent or operator pods not ready, CiliumEndpoints not ready, or
  IPAM exhaustion. Investigates with kubectl get, describe, events and logs, asks before
  running cilium-dbg or hubble inside the agent, and proposes fixes. Reads first and asks
  before changing anything.
license: Apache-2.0
metadata:
  verified-with: "kubernetes 1.37, cilium 1.20"
  verified-on: "2026-10-24"
---

# Cilium troubleshooting

Find out why traffic fails on a cluster that runs Cilium, and propose a fix. **Read
first, ask before changing.** Run the investigation commands freely. Run a command under
an "Ask first" line only after the user approves that exact command; if your
credentials do not allow it, give it to the user to run. Never run a "Proposed fix";
hand it to the user.

Cilium gives each pod a **CiliumEndpoint** with a security **identity** derived from its
labels, and enforces Kubernetes NetworkPolicies, **CiliumNetworkPolicies** (one
namespace) and **CiliumClusterwideNetworkPolicies** by identity. Once any policy selects
an endpoint for a direction (ingress or egress), only what some policy allows gets
through in that direction. L7 rules (HTTP, DNS) send the traffic through Cilium's Envoy
proxy. **Hubble** records each flow with its verdict.

The commands use placeholders: `my-namespace`, `my-app` (the server) and `my-web` (the
client), `my-policy`, and `cilium-xxxxx` (the Cilium agent pod on the node of the pod
you investigate). Replace them with the real names. The built-in `view` role cannot read
`cilium.io` objects (Cilium adds nothing to it); if they are forbidden, say so and ask
the user for them. Never read Secrets (Cilium keeps its CA and Cluster Mesh credentials
in Secrets).

## When to use

- Pods cannot reach each other, or a Service, on a cluster with Cilium; often right after
  a policy change.
- DNS lookups fail (`bad address`, time-outs) after an egress policy.
- Requests get HTTP 403 `Access denied` although the app does not return that.
- Pods stay ContainerCreating with a Cilium CNI error, or Cilium's own pods are not
  ready.

Hand-offs, by skill name. When the evidence points elsewhere, continue with that skill;
if it is not installed, keep going with the steps here and tell the user which skill
would help:

- The Service has no endpoints, a wrong selector or port, or the target pods are not
  Ready: `k8s-network-troubleshooting` (Services and Kubernetes NetworkPolicies) and
  `k8s-workload-troubleshooting`.
- A node is NotReady: `k8s-node-troubleshooting`.
- Cilium's Gateway API support (the class `io.cilium/gateway-controller`) does not
  accept a Gateway or a route: `k8s-gateway-api-troubleshooting`.

## Investigate

Work through the steps in order. Stop when you have the cause and its evidence.

**1. Check Cilium itself**: the agent on each node, the operator, Envoy.

```bash
kubectl get pods -n kube-system -l k8s-app=cilium -o wide
kubectl get deployments,daemonsets -n kube-system | grep -i -E "cilium|hubble"
kubectl get ciliumnodes
```

**2. Read the client's error and the endpoints.** A time-out usually means a drop by
policy; `bad address` means DNS; a 403 with `Access denied` comes from an L7 rule.

```bash
kubectl logs -n my-namespace deployment/my-web --tail=20
kubectl get ciliumendpoints -n my-namespace
kubectl get pods -n my-namespace --show-labels -o wide
```

A CiliumEndpoint should be `ready`. Pods without one (hostNetwork pods, pods started
before Cilium) are not managed and get no policy.

**3. Find the policies that select the pods**, in both directions: ingress on the
server, egress on the client, and cluster-wide ones.

```bash
kubectl get ciliumnetworkpolicies,networkpolicies -n my-namespace
kubectl get ciliumclusterwidenetworkpolicies
kubectl get ciliumnetworkpolicy my-policy -n my-namespace -o yaml
kubectl describe ciliumnetworkpolicy my-policy -n my-namespace
```

Compare each policy's `endpointSelector` with the pods' labels, and its
`fromEndpoints`, `toEndpoints`, `toPorts` and `rules` with the traffic that fails.

**4. Ask Cilium what it drops.** Find the agent pod on the node of the client or server
(step 1 and the pod's node), then read the recent dropped flows and the endpoints'
policy state. These run a reading command inside the agent, so ask first:

> Ask first: the agent runs this only after the user approves it.

```bash
kubectl exec cilium-xxxxx -n kube-system -c cilium-agent -- hubble observe --last 50 --namespace my-namespace --verdict DROPPED
kubectl exec cilium-xxxxx -n kube-system -c cilium-agent -- cilium-dbg endpoint list
```

`hubble observe` needs Hubble, which is on by default. Without it,
`cilium-dbg status` and the agent's logs are the fallback.

**5. Open the matching reference** and follow its steps:

| What you see | Reference |
|---|---|
| Time-outs, `Policy denied` drops, a policy that allows the wrong peer, default deny surprises, DNS blocked by an egress policy, L7 403s, toFQDNs | [references/policies.md](references/policies.md) |
| Cilium pods not ready, `unable to connect to Cilium agent`, endpoints not ready, IPAM exhausted, kube-proxy replacement, MTU | [references/agent-and-datapath.md](references/agent-and-datapath.md) |

## Read the results

What the common findings mean (Cilium 1.20):

- **Client time-outs, and Hubble shows `Policy denied DROPPED` with `INGRESS DENIED`**
  from the client to the server: a policy selects the server for ingress and none
  allows this client. Compare the policy's `fromEndpoints` labels with the client's
  labels.
- **The same with `EGRESS DENIED`**: a policy selects the client for egress and does
  not allow the destination.
- **`bad address` or DNS time-outs right after an egress policy on the client**: the
  policy put the client in default-deny for egress and does not allow DNS to kube-dns
  (UDP and TCP 53, `k8s-app: kube-dns` in `kube-system`).
- **HTTP 403 with the body `Access denied`**: an L7 HTTP rule allows the connection but
  not that method or path; Cilium's Envoy answers instead of the app.
- **`cilium-dbg endpoint list` shows `Enabled` for a direction**: some policy selects
  that endpoint there, so default deny applies to it. `Disabled` means no policy
  selects it in that direction.
- **A CiliumNetworkPolicy with `VALID` `False`**: Cilium rejected it; `describe` shows
  why.

State the cause in one sentence, then the evidence you saw (the policy and its
selectors, the pods' labels, the drop verdict, the client's error), then the proposed
fix.

## Proposed fix

Show each fix to the user before running it: what it changes and how to undo it.
Creating, changing or deleting a network policy changes what traffic is allowed, often
for more pods than the one that fails: never run it yourself; hand the change to the
user as a proposed fix, with the narrowest rule that allows the traffic. Changing
Cilium's configuration (`cilium-config`, Helm values) and restarting Cilium are for the
cluster's administrators. Prefer fixing the policy in the source it is deployed from.
Write each undo with the values you found.

Allow my-web into my-app on port 80, next to the existing rule (the user applies it):

> Proposed fix: review before running. The agent does not run this.

```bash
kubectl apply -f my-app-ingress-from-my-web.yaml
# Undo: kubectl delete -f my-app-ingress-from-my-web.yaml
```

with `my-app-ingress-from-my-web.yaml` a CiliumNetworkPolicy in `my-namespace` whose
`endpointSelector` is `app: my-app` and whose ingress allows `fromEndpoints` `app:
my-web` on `toPorts` port `80/TCP`. Policies add up, so the existing rule stays.

## Sources

Checked against the Cilium 1.20 documentation and source (v1.20.4):

- [Troubleshooting](https://docs.cilium.io/en/stable/operations/troubleshooting/) and
  [policy troubleshooting](https://docs.cilium.io/en/stable/security/policy/troubleshooting/).
- [Policy enforcement and default deny](https://docs.cilium.io/en/stable/security/policy/intro/)
  and the [policy language](https://docs.cilium.io/en/stable/security/policy/language/):
  selectors, L7 rules, DNS and toFQDNs.
- [DNS-based policies](https://docs.cilium.io/en/stable/security/dns/) and
  [Hubble](https://docs.cilium.io/en/stable/observability/hubble/).
- [Installation on kind](https://docs.cilium.io/en/stable/installation/kind/) and the
  [upgrade notes](https://docs.cilium.io/en/stable/operations/upgrade/).
- Drop reasons and endpoint states from the source:
  [drop.go](https://github.com/cilium/cilium/blob/v1.20.4/pkg/monitor/api/drop.go),
  [endpoint_state.go](https://github.com/cilium/cilium/blob/v1.20.4/api/v1/models/endpoint_state.go).
  The client errors and Hubble output quoted here were seen on a Kubernetes 1.37 kind
  cluster with Cilium 1.20.4.
