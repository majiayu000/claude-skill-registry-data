---
name: k8s-coredns-troubleshooting
description: >-
  Use when cluster DNS itself misbehaves on Kubernetes: CoreDNS pods in CrashLoopBackOff
  ("Error during parsing: Unknown directive", "plugin/loop: Loop ... detected"), "reload
  failed" after a Corefile edit, external names failing while Service names resolve
  (";; connection timed out; no servers could be reached", SERVFAIL, "plugin/errors: 2
  ... i/o timeout"), one domain or stub domain failing, rewrite or hosts entries that do
  not work, "Plugins not ready: \"kubernetes\"", REFUSED or "concurrent queries exceeded
  maximum", slow lookups (ndots, 5 s delays), NodeLocal DNSCache (169.254.20.10), or the
  AKS coredns-custom, EKS add-on and GKE kube-dns ConfigMaps. Investigates with kubectl
  get and logs, and proposes fixes. Reads first and asks before changing anything.
license: Apache-2.0
metadata:
  verified-with: "kubernetes 1.37, coredns 1.14"
  verified-on: "2026-10-25"
---

# CoreDNS troubleshooting

Find out why CoreDNS does not answer a name the way it should, and propose a fix. **Read
first, ask before changing.** Run the investigation commands freely. Run a command under
an "Ask first" line only after the user approves that exact command; if your credentials
do not allow it, give it to the user to run. Never run a "Proposed fix"; hand it to the
user.

CoreDNS runs in `kube-system` as the Deployment `coredns` (label `k8s-app=kube-dns`),
behind the Service `kube-dns`, and reads its configuration, the **Corefile**, from the
ConfigMap `coredns`. Each server block (`.:53 { ... }`, or `example.com:53 { ... }` for
one domain) lists plugins: `kubernetes` answers names under `cluster.local`, `forward`
sends everything else upstream (by default to the node's `/etc/resolv.conf`), `cache`,
`rewrite` and `hosts` change answers, `errors` logs failures, `loop` stops CoreDNS when
it would query itself, and `reload` reads an edited Corefile about 30 seconds after the
ConfigMap reaches the pod. The default Corefile has no `log` plugin, so successful
queries and NXDOMAIN answers are not logged.

The commands use placeholders: `my-namespace`, `my-app` (a Service), `my-client` (a pod
whose lookups fail) and `my-coredns-pod`. Replace them with the real names. The CoreDNS
image has no shell, so test lookups from a client pod. Never read Secrets.

## When to use

- CoreDNS pods crash, restart or are not Ready.
- Names outside the cluster fail, or one domain fails, while Service names resolve.
- DNS broke right after someone edited the `coredns` ConfigMap.
- Lookups are slow, time out now and then, or get `REFUSED`.

Hand-offs, by skill name. When the evidence points elsewhere, continue with that skill;
if it is not installed, keep going with the steps here and tell the user which skill
would help:

- Only one client fails for a Service name (wrong namespace in the name, `dnsPolicy`, a
  Service with no endpoints) or an egress NetworkPolicy blocks DNS:
  `k8s-network-troubleshooting`. On Cilium, a DNS-aware policy:
  `k8s-cilium-troubleshooting`.
- The CoreDNS pods are Pending, evicted or OOMKilled because of their node:
  `k8s-node-troubleshooting`.
- `Failed to watch ... is forbidden` for the `coredns` ServiceAccount:
  `k8s-rbac-troubleshooting`.

## Investigate

Work through the steps in order. Stop when you have the cause and its evidence.

**1. See CoreDNS's pods, Deployment and Service.** A rollout that is stuck, a pod that
restarts, or no endpoints for `kube-dns` each change where to look next.

```bash
kubectl get deployment coredns -n kube-system
kubectl get pods -n kube-system -l k8s-app=kube-dns -o wide
kubectl get service kube-dns -n kube-system
kubectl get endpointslices -n kube-system -l kubernetes.io/service-name=kube-dns
kubectl get daemonset -n kube-system
```

A `node-local-dns` DaemonSet means NodeLocal DNSCache sits in front of CoreDNS (see the
second reference). On GKE there is a `kube-dns` Deployment and no `coredns` ConfigMap.

**2. Read CoreDNS's logs**, current and, after a crash, previous. `[ERROR]` lines come
from `errors`; `[INFO] Reloading` and `plugin/reload` lines show Corefile edits.

```bash
kubectl logs -n kube-system -l k8s-app=kube-dns --tail=50 --prefix
kubectl logs -n kube-system my-coredns-pod --previous --tail=20
kubectl get events -n kube-system --field-selector involvedObject.kind=Pod --sort-by=.lastTimestamp
```

**3. Read the Corefile** and any custom ConfigMap the cluster adds to it. Note the line
numbers: parse errors name them.

```bash
kubectl get configmap coredns -n kube-system -o jsonpath='{.data.Corefile}'
kubectl get configmap coredns -n kube-system -o yaml
kubectl get configmap -n kube-system | grep -E 'coredns|dns'
```

**4. Read the client's side**: its logs, its DNS policy, and which names fail.

```bash
kubectl logs -n my-namespace my-client --tail=30
kubectl get pod my-client -n my-namespace -o jsonpath='{.spec.dnsPolicy}{" "}{.spec.dnsConfig}{" node="}{.spec.nodeName}{"\n"}'
kubectl get service my-app -n my-namespace
```

**5. Look a name up from the client**, if its image has `nslookup` or `dig`: a Service
name, an external name, and the failing one. Try a fully qualified name with a trailing
dot to skip the search list.

> Ask first: the agent runs this only after the user approves it.

```bash
kubectl exec my-client -n my-namespace -- nslookup kubernetes.default.svc.cluster.local
kubectl exec my-client -n my-namespace -- nslookup my-app.my-namespace.svc.cluster.local
kubectl exec my-client -n my-namespace -- nslookup example.com.
kubectl exec my-client -n my-namespace -- cat /etc/resolv.conf
# Undo: none needed; these commands only read
```

**6. Open the matching reference** and follow its steps:

| What you see | Reference |
|---|---|
| A crash, `Error during parsing`, `reload failed`, a loop, `Plugins not ready`, upstream timeouts, SERVFAIL, `REFUSED`, stub domains, `rewrite`, `hosts`, metrics | [references/corefile-and-plugins.md](references/corefile-and-plugins.md) |
| Slow or intermittent lookups, `ndots`, NodeLocal DNSCache, scaling, AKS, EKS and GKE | [references/clients-nodelocal-managed.md](references/clients-nodelocal-managed.md) |

## Read the results

What the common findings mean (CoreDNS 1.14):

- **A new pod crashes with `/etc/coredns/Corefile:<line> - Error during parsing: Unknown
  directive '<word>'`** (no `[FATAL]` prefix; read it with `--previous`): the Corefile has
  a typo or a plugin this build does not have, on that line. Pods that were already
  running log **`[ERROR] plugin/reload: Corefile changed but reload failed: ...`** and keep
  serving their **old** configuration, so DNS still works until those pods are replaced:
  the ConfigMap and what is served are no longer the same.
- **`[FATAL] plugin/loop: Loop (127.0.0.1:<port> -> :53) detected for zone "."`**: CoreDNS
  forwards to itself, usually because the node's `/etc/resolv.conf` points at a local
  resolver such as `127.0.0.53` (systemd-resolved), or `forward` names a loopback address
  or the `kube-dns` Service.
- **`[ERROR] plugin/errors: 2 <name> A: read udp <pod>-><upstream>:53: i/o timeout`**:
  `2` is SERVFAIL; the upstream in `forward` does not answer (wrong address, firewall,
  upstream down). The client sees `;; connection timed out; no servers could be reached`
  or `SERVFAIL` for external names, while Service names, which CoreDNS answers itself,
  still resolve.
- **One name or domain gets NXDOMAIN and nothing is logged**: CoreDNS answered it on
  purpose: a `rewrite` to a name that does not exist, a `hosts` block without
  `fallthrough`, a server block for that zone forwarding to the wrong place, or a name
  under `cluster.local` that is not a Service (the `kubernetes` plugin never forwards
  those).
- **`[INFO] plugin/ready: Plugins not ready: "kubernetes"`** and the pod not Ready:
  CoreDNS cannot list Services and EndpointSlices from the API server (RBAC, network to
  the API server, an overloaded API server).
- **`5 <name> A: concurrent queries exceeded maximum 1000`** and `REFUSED` at the client:
  more queries are waiting on the upstream than `max_concurrent` allows; the upstream is
  slow or the load is too high.

State the cause in one sentence, then the evidence you saw (the log line, the Corefile
line, the client's result), then the proposed fix.

## Proposed fix

Show each fix to the user before running it: what it changes and how to undo it. The
Corefile serves every pod in the cluster: never change it yourself; hand it to the user as
a proposed fix, with the whole corrected Corefile and the current one saved for the undo.
On AKS change the `coredns-custom` ConfigMap instead, on EKS the add-on's
`configurationValues`, on GKE the `kube-dns` ConfigMap: the provider overwrites direct
edits of the `coredns` ConfigMap.

Save the Corefile before any change:

```bash
kubectl get configmap coredns -n kube-system -o jsonpath='{.data.Corefile}'
```

Apply the corrected Corefile (save it as `Corefile`). Running pods reload it within about
two minutes (up to a minute for the kubelet to update the mounted ConfigMap, then the
`reload` plugin's check every 30 seconds or so), and log `[INFO] Reloading complete`:

> Proposed fix: review before running. The agent does not run this.

```bash
kubectl create configmap coredns -n kube-system --from-file=Corefile --dry-run=client -o yaml | kubectl apply -f -
# Undo: the same command with the Corefile you saved before the change
```

Once the Corefile is valid again, pods in CrashLoopBackOff start at their next restart,
and a stuck rollout goes on by itself. To replace pods that still run an old
configuration:

> Ask first: the agent runs this only after the user approves it.

```bash
kubectl rollout restart deployment/coredns -n kube-system
# Undo: none needed; the restart only recreates the pods with the same template
```

Restart CoreDNS only after its Corefile is valid: with a broken Corefile, the new pods
crash and only the old ones that the rollout has not replaced yet keep DNS working.

## Sources

Checked against CoreDNS 1.14.6 (the version kubeadm 1.37 deploys) and Kubernetes 1.37:

- CoreDNS plugins: [kubernetes](https://coredns.io/plugins/kubernetes/),
  [forward](https://coredns.io/plugins/forward/), [reload](https://coredns.io/plugins/reload/),
  [loop](https://coredns.io/plugins/loop/), [errors](https://coredns.io/plugins/errors/),
  [log](https://coredns.io/plugins/log/), [cache](https://coredns.io/plugins/cache/),
  [rewrite](https://coredns.io/plugins/rewrite/), [hosts](https://coredns.io/plugins/hosts/),
  [ready](https://coredns.io/plugins/ready/), [health](https://coredns.io/plugins/health/) and
  [metrics](https://coredns.io/plugins/metrics/).
- Kubernetes: [Debugging DNS resolution](https://kubernetes.io/docs/tasks/administer-cluster/dns-debugging-resolution/),
  [Customizing DNS](https://kubernetes.io/docs/tasks/administer-cluster/dns-custom-nameservers/),
  [DNS for Services and Pods](https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/),
  [NodeLocal DNSCache](https://kubernetes.io/docs/tasks/administer-cluster/nodelocaldns/) and
  [autoscaling DNS](https://kubernetes.io/docs/tasks/administer-cluster/dns-horizontal-autoscaling/).
- Managed clusters: [AKS CoreDNS customization](https://learn.microsoft.com/en-us/azure/aks/coredns-custom),
  [EKS CoreDNS add-on](https://docs.aws.amazon.com/eks/latest/userguide/managing-coredns.html)
  and [GKE kube-dns](https://docs.cloud.google.com/kubernetes-engine/docs/concepts/kube-dns).
- Messages from the source:
  [kubeadm's Corefile](https://github.com/kubernetes/kubernetes/blob/v1.37.1/cmd/kubeadm/app/phases/addons/dns/manifests.go),
  [reload](https://github.com/coredns/coredns/blob/v1.14.6/plugin/reload/reload.go),
  [loop](https://github.com/coredns/coredns/blob/v1.14.6/plugin/loop/loop.go) and
  [forward](https://github.com/coredns/coredns/blob/v1.14.6/plugin/forward/forward.go). The
  parse, reload and upstream messages quoted here were seen on a Kubernetes 1.37 kind
  cluster with CoreDNS 1.14.6.
