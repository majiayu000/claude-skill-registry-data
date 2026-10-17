---
name: metallb
description: >
  MetalLB bare-metal load balancer: L2 mode configuration, IP pool management,
  L2Advertisement, and troubleshooting on K3s clusters.
license: MIT
compatibility:
  - opencode
metadata:
  author: dotfiles
  tags: [kubernetes, metallb, loadbalancer, networking, k3s]
---

# MetalLB Skill

> **OBSOLETE — MetalLB has been removed from this cluster.**
>
> MetalLB was replaced by **Cilium LB-IPAM + L2 Announcements** due to a
> fundamental incompatibility: MetalLB requires the `kubernetes.io/service-name`
> label on EndpointSlices to elect a node for L2 announcements. Cilium's
> Gateway API creates EndpointSlices without this label, so MetalLB's speaker
> never announced the Gateway IPs via ARP, making the Gateway unreachable.
>
> See the **cilium** skill for the replacement implementation.
> See `roles/install-cilium-pools/` for the new `CiliumLoadBalancerIPPool` and
> `CiliumL2AnnouncementPolicy` resources.
>
> The `install-metallb` role still exists on disk but is no longer included in
> `playbooks/bootstrap.yml`.

---

## Quick Reference: Annotation Migration

| Old (MetalLB) | New (Cilium LB-IPAM) |
|---|---|
| `metallb.universe.tf/loadBalancerIPs: "x.x.x.x"` | `lbipam.cilium.io/ips: "x.x.x.x"` |
| `metallb.universe.tf/allow-shared-ip: "key"` | `lbipam.cilium.io/sharing-key: "key"` |
| `externalTrafficPolicy: Local` | `externalTrafficPolicy: Cluster` (**required**) |
