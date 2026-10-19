---
name: gke-ipam
description: GKE IP Address Management — VPC subnet planning, secondary range allocation, PSC NAT sizing, and IP conflict validation. Use when designing GKE network topology, planning cluster IP ranges, validating 1.0→2.0 migration衝突, or auditing GKE ipAllocationPolicy.
---

# GKE IPAM

## When to Load This Skill

- Designing new GKE clusters and need subnet/secondary-range CIDR planning
- Validating that new GKE clusters won't conflict with existing VPC allocations
- Migrating or co-locating GKE clusters across versions (e.g., 1.0 → 2.0)
- Auditing GKE ipAllocationPolicy in existing clusters
- Planning PSC NAT subnet capacity

## Core Principle

GKE uses **four independent IP dimensions**. All four must be validated independently for conflicts — never assume that because one dimension (e.g., Node) is clear, the others are too.

| Dimension | GKE API Field | Scope |
|---|---|---|
| Node subnet (primary) | `subnetwork` | VPC primary subnet |
| Pod secondary range | `clusterSecondaryRangeName` / `pods-xxx` | VPC secondary range |
| Service secondary range | `servicesSecondaryRangeName` / `svc-xxx` | VPC secondary range |
| Control plane (private) | `masterIpv4CidrBlock` | GCP-managed, separate from VPC |

## IP Conflict Validation Pattern

Always use Python `ipaddress` module for definitive overlap checking. Never rely on manual CIDR arithmetic.

```python
import ipaddress

def check_overlap(name, cidr, against_name, against_cidr):
    net = ipaddress.ip_network(cidr)
    ref = ipaddress.ip_network(against_cidr)
    overlaps = net.overlaps(ref)
    return {
        "item": name,
        "cidr": cidr,
        "against": against_name,
        "against_cidr": against_cidr,
        "overlaps": overlaps,
        "status": "❌ CONFLICT" if overlaps else "✅ OK"
    }

# Example: 1.0 existing allocations
one_node = "192.168.64.0/19"
one_pod  = "100.64.0.0/14"
one_svc  = "100.68.0.0/17"
one_mp   = "192.168.224.0/28"

# Example: 2.0 proposed cluster-03
checks = [
    ("cluster-03 Node",   "192.168.96.0/20",    one_node),
    ("cluster-03 Pod",    "100.72.0.0/18",       one_pod),
    ("cluster-03 Service","100.76.0.0/18",       one_svc),
    ("cluster-03 Master",  "192.168.224.64/28",  one_mp),
]

for row in checks:
    r = check_overlap(*row)
    print(f"  {r['item']:20s} {r['cidr']:20s} vs {r['against_cidr']:20s} {r['status']}")
```

Key trap: a /27 block that *contains* a /28 is a conflict. `overlaps()` catches this correctly — a manual check might miss it.

## Planning Thresholds

| Range type | Common prefix | Max clusters before exhaustion |
|---|---|---|
| Node subnet (/20) | 192.168.X.0/20 | ~40 per /16 VPC |
| Pod secondary (/18) | 100.X.0.0/18 | ~16 per /14 pool |
| Service secondary (/18) | 100.X.0.0/18 | ~16 per /14 pool |
| Control plane (/28) | 192.168.224.0/28 | ~256 per /16 (but GCP limited) |

## PSC NAT Subnet Sizing

PSC NAT IP consumption = number of **connected endpoints/backends**, not TCP connections. Monitor `private_service_connect/producer/used_nat_ip_addresses`.

| Subnet CIDR | Usable NAT IPs |
|---|---|
| /26 | 60 |
| /25 | 124 |
| /24 | 252 |

## Common Conflict Patterns in 1.0→2.0 Migration

- **Node**: 1.0 often uses /19 or /18 for nodes; 2.0 /20 clusters starting at low offsets conflict
- **Pod**: 1.0 commonly uses 100.64.0.0/x for pods; 2.0 /18 blocks inside that range conflict
- **Service**: 1.0 commonly uses 100.68.0.0/x; verify 2.0 blocks are outside
- **Control Plane**: 1.0 often uses 192.168.224.0/28; 2.0 master blocks at 192.168.224.0/27 contain this

## GKE Creation Notes

- `--master-ipv4-cidr` uses `/28` (not `/27`) in the actual create command
- `/27` can be documented as the management reservation block but must not be passed to `--master-ipv4-cidr`
- Existing cluster secondary ranges (Pod/Service) are **immutable** for existing node pools — to change them, create a new node pool with the new range or rebuild the cluster
- Adding additional Pod ranges to an existing cluster is supported, but the default range for existing node pools cannot be changed

## References

- `references/ip-conflict-1.0-2.0.md` — Session data: 1.0/2.0 IP tables, Python validation output, corrected allocation table
