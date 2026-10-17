---
name: cilium
description: >
  Cilium CNI operations: kube-proxy replacement, BPF configuration,
  Gateway API, Ingress Controller, LB-IPAM, L2 Announcements,
  upgrades, and troubleshooting on K3s/ARM64.
license: MIT
compatibility:
  - opencode
allowed-tools:
  - Bash(kubectl:*)
  - Bash(cilium:*)
  - Bash(helm:*)
metadata:
  author: dotfiles
  tags: [kubernetes, cilium, cni, networking, ebpf, k3s, gateway-api, ingress, lb-ipam, l2-announcements]
  scripts: scripts/connectivity-test.sh
---

# Cilium Skill

## Cluster Context

This cluster uses Cilium with **full kube-proxy replacement** (`--disable-kube-proxy` on K3s).
Node: Raspberry Pi CM4, ARM64, Ubuntu 24.04.
Helm release: `cilium` in namespace `kube-system`.
Chart version pinned in: `roles/install-cilium/defaults/main.yml`.

### Active Helm values

```yaml
kubeProxyReplacement: "true"
k8sServiceHost: "192.168.178.133"
k8sServicePort: "6443"
rollOutCiliumPods: true          # hash ConfigMap into pod template → auto rollout
operator.replicas: 1
operator.rollOutPods: true       # same for operator
envoy.rollOutPods: true          # same for envoy
bpf.masquerade: true             # required on ARM64
loadBalancer.acceleration: disabled   # no hardware offload on CM4
gatewayAPI.enabled: true
gatewayAPI.externalTrafficPolicy: Cluster   # REQUIRED for L2 Announcements (see below)
l2announcements.enabled: true              # Cilium handles ARP (MetalLB removed)
l2announcements.leaseDuration: 3s
l2announcements.leaseRenewDeadline: 1s
l2announcements.leaseRetryPeriod: 500ms
k8sClientRateLimit.qps: 32               # sized for L2 announcement leader election
k8sClientRateLimit.burst: 64
ingressController.enabled: true
ingressController.default: true
ingressController.enforceHttps: false   # flip to true once cert-manager is up
ingressController.loadbalancerMode: shared
ingressController.service.externalTrafficPolicy: Cluster   # REQUIRED for L2 Announcements
```

---

## Critical: rollOutPods flags

Always set these three values in the Cilium Helm chart:

```yaml
rollOutCiliumPods: true
operator.rollOutPods: true
envoy.rollOutPods: true
```

These inject a hash of `cilium-config` ConfigMap into pod template annotations.
Any `helm upgrade` that changes config triggers an automatic rolling restart of
all three components, making `wait: true` reliable.

**Without these flags:** `helm upgrade` updates the ConfigMap but pods keep
running with stale in-memory config. Silent deadlock — agent waits forever for
CRDs that the stale operator never registers. No obvious error message.

---

## Critical: Envoy CRDs

`ciliumenvoyconfigs.cilium.io` and `ciliumclusterwideenvoyconfigs.cilium.io`
are registered by the **operator** ONLY when `enable-envoy-config=true`, which
is set automatically when `gatewayAPI.enabled=true` or
`ingressController.enabled=true`.

If the operator pod started before those flags were set (stale pod), it will
**never** register the Envoy CRDs. The agent will then hang indefinitely:

```
Still waiting for Cilium Operator to register CRDs: [ciliumenvoyconfigs.cilium.io ...]
```

Fix: ensure `operator.rollOutPods: true` is set so the operator restarts on
every config change. If already stuck, delete the operator pod manually:

```bash
kubectl delete pod -n kube-system -l io.cilium/app=operator
# Wait for new pod, then check:
kubectl get crd | grep envoy
```

---

## Critical: Helm stuck in pending-upgrade

If a `helm upgrade` is interrupted (Ctrl+C, timeout, context canceled), the
release may be left in `pending-upgrade` state. All subsequent upgrades silently
hang — no error, no output, just blocks indefinitely.

```bash
# Diagnose
helm history cilium -n kube-system
# Look for STATUS=pending-upgrade

# Fix: delete the stuck secret (vN = the pending-upgrade revision number)
kubectl delete secret sh.helm.release.v1.cilium.vN -n kube-system

# Verify state is clean (last revision should be "deployed")
helm history cilium -n kube-system

# Then re-run
ansible-playbook playbooks/bootstrap.yml -i inventory/hosts.ini \
  --start-at-task "Add Cilium Helm repository"
```

---

## Gateway API

Cilium 1.19 supports Gateway API v1.4.1 (standard channel).

**Prerequisites (all already met in this cluster):**
- `kubeProxyReplacement: true`
- `l7Proxy: true` (default)
- Gateway API CRDs installed BEFORE `gatewayAPI.enabled=true` is applied

**Role order in bootstrap.yml:**
```
install-gateway-api-crds  →  install-cilium  →  install-cilium-pools
```

**What gets created automatically:**
- `GatewayClass` named `cilium` (controller: `io.cilium/gateway-controller`)
- A `LoadBalancer` Service per `Gateway` resource (Cilium LB-IPAM assigns IP from pool)

**GatewayClass status meanings:**
- `Unknown` → operator/agent not yet running with new config, or no LB-IPAM pool defined
- `True` → fully operational

```bash
kubectl get gatewayclass
kubectl get gateway -A
kubectl get httproute -A
```

---

## LB-IPAM (Cilium Load Balancer IP Address Management)

MetalLB has been **removed**. Cilium's built-in LB-IPAM handles IP assignment.

LB-IPAM is always compiled in; it activates when the first `CiliumLoadBalancerIPPool` is created.
The pool lives in the `install-cilium-pools` role.

### CiliumLoadBalancerIPPool

```yaml
apiVersion: "cilium.io/v2alpha1"
kind: CiliumLoadBalancerIPPool
metadata:
  name: default-pool
spec:
  blocks:
    - cidr: "192.168.178.200/28"   # .200 – .215 (16 IPs)
```

### Pin a specific IP

```yaml
metadata:
  annotations:
    lbipam.cilium.io/ips: "192.168.178.203"
```

### Sharing an IP across multiple services (replaces metallb allow-shared-ip)

```yaml
metadata:
  annotations:
    lbipam.cilium.io/sharing-key: "shared-gateway"
```

### Verify pool and assignments

```bash
kubectl get ciliumloadbalancerippools
kubectl get svc -A | grep LoadBalancer
# Check EXTERNAL-IP column — should show assigned IP
```

---

## L2 Announcements (ARP)

Cilium's L2 Announcements replace MetalLB's speaker for ARP on the LAN.

Leader election uses Kubernetes `Lease` objects in `kube-system`:
```bash
kubectl -n kube-system get lease | grep cilium-l2announce
```

### CiliumL2AnnouncementPolicy

```yaml
apiVersion: "cilium.io/v2alpha1"
kind: CiliumL2AnnouncementPolicy
metadata:
  name: default-l2-policy
spec:
  interfaces:
    - ^eth.*$               # legacy wired NICs: eth0, eth1, etc.
    - ^en.*               # wired NICs: end1 / eno1 / ens* / enp* / enx*
    - ^wl.*               # Wi-Fi NICs: wlp4s0, wlan0, etc.
    - ^end.*
    - ^eno.*
    - ^ens.*
    - ^enp.*
    - ^enx.*
  externalIPs: false
  loadBalancerIPs: true
```

**Important:** if the host NIC changes (for example `end1` on newer nodes or a
Wi-Fi interface such as `wlp4s0`), the L2 announcement selector must include
it. A too-narrow `^eth[0-9]+` regex will leave the VIP advertised in Kubernetes
but unreachable from the LAN.

### Workflow note

For long-running cluster changes, prove the desired state manually or with Helm
first, then run Ansible in the background with redirected logs, and only after
that re-run the same Ansible command normally.

### Check the LAN side

```bash
ip neigh show 192.168.178.200
ip neigh show 192.168.178.203
arp -n 192.168.178.200
arp -n 192.168.178.203
```

`.203` is the Pi-hole DNS VIP and `.200` is the shared HTTP/HTTPS Gateway VIP.
If `.203` answers but `.200` does not, DNS is healthy and only the Gateway path is broken.
If `.203` times out, fix the Pi-hole L2 announcement path first.

If the lease exists but ARP is `FAILED` or `(incomplete)`, the policy is too
narrow or the wrong interface family is advertised. Update the interface regexes
and reapply the policy.

### CRITICAL: externalTrafficPolicy must be Cluster

Cilium L2 Announcements are **incompatible** with `externalTrafficPolicy: Local`.
The L2 announcement leader may not be the same node as the endpoint — with `Local`,
traffic would be dropped. Always use `Cluster` on all LoadBalancer services.

Set in Helm values:
```yaml
gatewayAPI.externalTrafficPolicy: Cluster
ingressController.service.externalTrafficPolicy: Cluster
```

Set on individual services:
```yaml
spec:
  externalTrafficPolicy: Cluster
```

### Verify ARP is working

```bash
# From macOS/Linux laptop on the same LAN:
arp -n 192.168.178.200   # should show node MAC, not "(incomplete)"
arp -n 192.168.178.203
```

### Why MetalLB was removed

MetalLB requires the `kubernetes.io/service-name` label on EndpointSlices to
associate slices with a service for L2 leader election. Cilium's Gateway API
creates EndpointSlices with gateway-specific labels but WITHOUT this label.
This is a fundamental incompatibility — MetalLB's speaker never elected a node
for the Gateway service, so ARP was never announced and traffic never reached
the node. Cilium LB-IPAM + L2 Announcements have no such requirement.

---

## Ingress Controller

Cilium handles `networking.k8s.io/v1 Ingress` resources via Envoy.

**shared mode** (configured here): one `cilium-ingress` LoadBalancer Service
for all Ingress resources — saves LB-IPAM IPs. Use in homelab.

**dedicated mode**: one LB Service per Ingress — use only if per-Ingress IP
assignment is required.

```bash
kubectl get ingressclass
kubectl get ingress -A
kubectl get svc cilium-ingress -n kube-system
```

---

## externalTrafficPolicy

Both `gatewayAPI` and `ingressController` create `LoadBalancer` Services.

| Policy | Source IP | Notes |
|--------|-----------|-------|
| `Cluster` | Lost (SNAT) | **Required for L2 Announcements** |
| `Local` | Preserved | **Incompatible with L2 Announcements** |

Always use `Cluster` on this cluster. L2 Announcements docs explicitly state
incompatibility with `Local` — the announcement leader may differ from the
endpoint node, causing traffic to be dropped silently.

---

## ztunnel — NOT for Cilium

`ztunnel` is the **Istio Ambient Mesh** L4 proxy. It is NOT part of Cilium.
Cilium has its own integrated service mesh via `cilium-envoy` + `CiliumEnvoyConfig`.
Never install ztunnel alongside Cilium.

---

## Upgrade Procedure

1. Check current version: `helm list -n kube-system`
2. Check release notes: https://github.com/cilium/cilium/releases
3. Update `cilium_version` in `roles/install-cilium/defaults/main.yml`
4. Diff before applying:
   ```bash
   helm diff upgrade cilium cilium/cilium --version <new> -n kube-system
   ```
5. Re-run:
   ```bash
   ansible-playbook playbooks/bootstrap.yml -i inventory/hosts.ini \
     --start-at-task "Add Cilium Helm repository"
   ```
6. Verify:
   ```bash
   kubectl rollout status ds/cilium -n kube-system
   kubectl rollout status deploy/cilium-operator -n kube-system
   kubectl get gatewayclass
   ```

---

## Health Checks

```bash
# Pod status
kubectl get pods -n kube-system -l k8s-app=cilium
kubectl get pods -n kube-system -l io.cilium/app=operator

# Helm state
helm history cilium -n kube-system
helm get values cilium -n kube-system

# CRDs
kubectl get crd | grep -E "cilium|gateway"

# GatewayClass
kubectl get gatewayclass

# LB-IPAM pools and assignments
kubectl get ciliumloadbalancerippools
kubectl get svc -A | grep LoadBalancer

# L2 Announcement leases (leader election)
kubectl -n kube-system get lease | grep cilium-l2announce

# ARP (from laptop on same LAN)
arp -n 192.168.178.200
arp -n 192.168.178.203

# Connectivity test
kubectl run -it --rm pingtest --image=nicolaka/netshoot -- ping <pod-ip>
```

---

## Troubleshooting

### Agent stuck: "Still waiting for Cilium Operator to register CRDs"
→ Operator pod is stale. See **Critical: Envoy CRDs** section above.

### helm upgrade hangs with no output
→ Stuck pending-upgrade. See **Critical: Helm stuck** section above.

### GatewayClass stays `Unknown`
1. Check operator is running with new config: `kubectl logs -n kube-system -l io.cilium/app=operator --tail=20`
2. Check Envoy CRDs exist: `kubectl get crd | grep envoy`
3. Check LB-IPAM pool exists: `kubectl get ciliumloadbalancerippools`

### LoadBalancer service stays `<pending>` for EXTERNAL-IP
- Check `CiliumLoadBalancerIPPool` exists and pool has free IPs
- Check `lbipam.cilium.io/ips` annotation matches an IP in the pool range
- Check for conflicting `lbipam.cilium.io/sharing-key` annotations

### ARP not resolving / IP not reachable from LAN
- Check L2 announcement lease exists: `kubectl -n kube-system get lease | grep cilium-l2announce`
- Verify `CiliumL2AnnouncementPolicy` exists and `interfaces` regex matches the node NIC
- Verify `CiliumL2AnnouncementPolicy` exists and `interfaces` regex matches the node NIC (on this cluster it must include `end1`)
- Confirm `externalTrafficPolicy: Cluster` on the service — `Local` silently breaks L2
- Check Cilium agent logs for L2 announcement errors: `kubectl logs -n kube-system -l k8s-app=cilium --tail=50 | grep -i l2`
- Run `tcpdump -i eth0 arp` on the node to see if ARP replies are being sent

### BPF programs: using TCX not legacy tc filter
Cilium uses **TCX** (BPF links) on `eth0`, NOT legacy `tc filter`.
`tc filter show dev eth0 ingress` returns nothing even when BPF is active.
Check actual attachment via: `ls /sys/fs/bpf/cilium/devices/eth0/links/`

### Node stays `NotReady` after Cilium install
```bash
kubectl describe node | grep NetworkUnavailable
# Should flip to False with reason CiliumIsUp once agent is Running
kubectl delete pod -n kube-system -l k8s-app=cilium  # force restart if stuck
```

### kube-proxy replacement issues
```bash
sudo systemctl cat k3s | grep kube-proxy   # verify --disable-kube-proxy is set
kubectl -n kube-system exec ds/cilium -- cilium status | grep KubeProxyReplacement
```

### BPF masquerade not working (ARM64)
- Ensure `loadBalancer.acceleration: disabled` — hardware offload not available on CM4
- Kernel must be 5.10+ (Ubuntu 24.04 ships 6.x — fine)

---

## Useful Commands

```bash
# Live agent logs
kubectl logs -n kube-system -l k8s-app=cilium -f

# Live operator logs
kubectl logs -n kube-system -l io.cilium/app=operator -f

# Full helm diff before upgrade
helm diff upgrade cilium cilium/cilium --version <ver> -n kube-system

# ConfigMap (what the agent reads at runtime)
kubectl get configmap cilium-config -n kube-system -o yaml

# Inside cilium pod
kubectl -n kube-system exec ds/cilium -- cilium status
kubectl -n kube-system exec ds/cilium -- cilium monitor
```
