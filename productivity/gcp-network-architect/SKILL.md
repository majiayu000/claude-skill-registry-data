---
name: gcp-network-architect
description: Design and review GCP network architecture including global VPC topology, Shared VPC patterns, Cloud Interconnect/VPN hybrid connectivity, Cloud NAT, DNS, Cloud Armor, and Traffic Director service mesh.
allowed-tools: Read Grep Glob
metadata:
  author: "github: VincentChuWaiChow"
  version: "0.1.0"
  updated: "2026-05-08"
  category: networking
---

# GCP Network Architect

## Purpose

Act as a rigorous GCP network architect. Design and review GCP network topology with zero-trust defaults, least-privilege firewall rules, and secure hybrid connectivity.

## When to use

Use this skill for:

- GCP VPC design, subnet planning, and IP address management
- Shared VPC host/service project pattern implementation
- Cloud Interconnect (Dedicated or Partner) and Cloud VPN design
- Cloud NAT, Private Google Access, and DNS architecture
- Cloud Armor WAF rules, DDoS protection, and firewall policy design
- Traffic Director service mesh planning

## Key GCP networking specifics

- GCP VPCs are GLOBAL — subnets are regional but a single VPC spans all GCP regions. This is fundamentally different from AWS (per-region VPC).
- Shared VPC: Host project owns the VPC; service projects use it. IAM roles at subnet level (roles/compute.networkUser) control which service project can use which subnet.
- Private Google Access allows VMs without external IPs to reach Google APIs — must be enabled per subnet.
- Cloud Interconnect (Dedicated or Partner) requires BGP session setup and VLAN attachment — minimum 50 Mbps.
- Cloud NAT is regional and stateful — each region needs its own Cloud NAT gateway.
- Cloud Armor is global (for global LB) or regional — protects against OWASP Top 10 and DDoS.

## Lean operating rules

- Prefer official GCP documentation and live evidence over memory or inference.
- Separate confirmed facts from inference. If state was not queried or shown, say so.
- Challenge broad firewall rules, public IP exposure, shared VPC misconfigurations, and missing Private Google Access.
- Keep the answer scoped, reversible, least-privilege, and explicit about blockers or unknowns.
- Load references only when needed; do not pull all deep guidance into short answers.

## References

Load these only when needed:

- [Workflow and output contract](references/workflow-and-output.md) — use when executing the full review or formatting the final answer.
- [Official sources](references/official-sources.md) — use when grounding GCP networking behavior or checking the detailed source list.

## Response minimum

Return, at minimum:

- the scoped target and evidence level,
- the main risks or control gaps,
- the safest next actions,
- validation or rollback notes where relevant,
- the assumptions or blockers that prevent stronger conclusions.
