---
name: cloud-networking-design
description: "A VPC is a private IP space you own inside a region."
---

# Cloud Networking Design (Verbose)

## Core Patterns

### VPC and Subnet Topology

A VPC is a private IP space you own inside a region. Everything else — routing,
isolation, egress control — is built from how you subdivide it. Two rules pay off
for years: choose a CIDR big enough that you never renumber, and never let two
networks you might one day connect share an address range.

```
VPC 10.20.0.0/16                         (one per region per account)

  AZ-a                        AZ-b                        AZ-c
  public  10.20.0.0/20        public  10.20.16.0/20       public  10.20.32.0/20
  private 10.20.64.0/20       private 10.20.80.0/20       private 10.20.96.0/20
  data    10.20.128.0/20      data    10.20.144.0/20      data    10.20.160.0/20
```

Three subnet tiers, spread across the AZs the region offers:

- **public** — a route to the internet gateway. Load balancers and, if you must,
  bastions. Nothing stateful.
- **private** — application/compute. Egress via NAT; no inbound from the internet.
- **data** — databases, caches. No internet route at all, reached only from the
  private tier via security-group references.

Availability zones are the failure domain. Spreading subnets across AZs is what
lets a load balancer survive a zone outage — but see the cost pattern below,
because that same spread is where inter-AZ charges accrue.

### Routing and Egress

"Public" and "private" are not attributes of a subnet; they are consequences of
its route table.

```
public route table                 private route table
  10.20.0.0/16 -> local              10.20.0.0/16 -> local
  0.0.0.0/0    -> igw                0.0.0.0/0    -> nat-gw
                                     s3-prefix    -> vpce (gateway endpoint)
```

A NAT gateway lets private instances reach out (package installs, third-party
APIs) while blocking all unsolicited inbound. It is also metered on both
throughput and hours, which makes it a quiet cost center. Route provider-managed
services (object storage, etc.) through a VPC endpoint so that traffic bypasses
the NAT path entirely.

### Security Groups vs NACLs

Two mechanisms, deliberately different, and best used together.

| | Security group | Network ACL |
|---|---|---|
| State | Stateful (return traffic auto-allowed) | Stateless (open both directions) |
| Scope | ENI / instance | Whole subnet |
| Rules | Allow only | Allow and deny |
| Ordering | All rules evaluated | Numbered, first match wins |

Security groups are the workhorse. Reference other groups instead of IP ranges so
the policy tracks the topology, not addresses:

```
lb-sg:    inbound 443 from 0.0.0.0/0
app-sg:   inbound 8080 from lb-sg          # only the LB may reach the app
data-sg:  inbound 5432 from app-sg         # only the app may reach the DB
```

Reserve NACLs for coarse, subnet-wide statements — "this data subnet never talks
to the internet" — where a deny rule adds a guardrail a security group cannot
express. Do not try to run fine-grained policy in NACLs; the stateless return-port
bookkeeping will bite you.

### Connecting Networks

Non-transitivity is the concept people rediscover painfully. If A peers with B and
B peers with C, A still cannot reach C. Peering is a point-to-point relationship,
and n VPCs fully meshed need n(n-1)/2 connections.

| Pattern | When it fits | Watch for |
|---|---|---|
| VPC peering | 2–3 VPCs, stable relationships | Non-transitive; mesh explodes |
| Transit gateway / Cloud Router | Hub-and-spoke across many VPCs/accounts | Central chokepoint; per-attachment + data cost |
| PrivateLink / PSC | Expose or consume *one* service privately | One service per endpoint, unidirectional |
| Site-to-site VPN / Direct Connect | On-prem hybrid | VPN over internet vs dedicated circuit trade-off |

Move to a transit gateway before the peering mesh grows past a handful of VPCs.
PrivateLink is not a network join — it publishes a single service endpoint into a
consumer VPC, so the consumer reaches exactly that service and nothing else, with
no CIDR coordination required. That property makes it the clean answer for
overlapping-CIDR situations peering cannot solve.

### Private Access to Managed Services

Every hop to a managed service over a public endpoint is a hop over the internet
(or through NAT) that you are paying for and exposing. Two private paths:

- **Gateway endpoint** — a route-table entry for storage-class services. No ENI,
  typically no hourly charge, keeps that traffic on the backbone.
- **Interface endpoint / PSC** — an ENI with a private IP in your subnet fronting
  the service. Hourly + data cost, but private and DNS-integrated.

The payoff is threefold: data never traverses the public internet, you drop the
NAT hop, and you usually avoid the egress charge that the public path would incur.

### The Cross-AZ and Egress Cost Trap

This is the pattern that surprises teams at scale. Three costs compound:

1. **Inter-AZ traffic** is billed, generally in both directions, even inside one
   VPC. A service whose replicas gossip across three AZs pays per hop.
2. **NAT gateway** charges per hour and per gigabyte processed.
3. **Internet egress** dwarfs everything else — data leaving the cloud is the
   expensive direction; inbound is usually free.

The tension is real: spreading across AZs buys availability, and concentrating in
one AZ buys cheapness and latency. Resolve it deliberately. Keep high-volume,
latency-sensitive chatter (cache reads, replica sync) zone-local with
topology-aware routing, while still placing enough capacity in each AZ to survive
losing one. See **cloud-cost-optimization** for turning these into budgets and
alerts, and **cloud-provider-tradeoffs** for how the billing shapes differ.

## Common Anti-Patterns

❌ **Overlapping CIDR ranges across VPCs or with on-prem.** Peering and VPN both
refuse to route between overlapping ranges, and you cannot fix it without
renumbering a live network.
✅ Allocate non-overlapping blocks from a central plan (an IPAM) up front.

❌ **Databases in public subnets "behind a security group".** One misordered rule
and the data tier is internet-reachable.
✅ Data tier in subnets with no internet route at all; reach it only from the app
tier via group references.

❌ **Security groups written with `0.0.0.0/0` or wide CIDRs internally.** The
policy no longer reflects who actually talks to whom.
✅ Reference source security groups by id, so rules track topology.

❌ **A full mesh of peering connections.** It grows quadratically and becomes
unauditable.
✅ Hub-and-spoke through a transit gateway once past a few VPCs.

❌ **Routing managed-service and inter-service traffic over public endpoints/NAT.**
You pay egress and NAT for traffic that could stay on the backbone.
✅ Private endpoints for managed services; keep intra-cloud traffic private.

❌ **Ignoring which AZ traffic lands in.** Chatty cross-AZ paths bill silently.
✅ Make placement and routing topology-aware; measure inter-AZ bytes.

## Network Design Checklist

- [ ] VPC CIDRs allocated from a non-overlapping, room-to-grow plan
- [ ] Three-tier subnets (public / private / data) across multiple AZs
- [ ] Only load balancers and bastions have an internet-gateway route
- [ ] Stateful and application workloads sit in private/data subnets
- [ ] Security groups reference source groups, not IP ranges, internally
- [ ] NACLs used only for coarse, subnet-wide guardrails
- [ ] Peering vs transit gateway chosen by VPC count; non-transitivity understood
- [ ] Managed services reached via VPC/interface endpoints, not the internet
- [ ] Inter-AZ, NAT, and egress traffic measured and budgeted
- [ ] Latency-sensitive high-volume traffic kept zone-local where safe
- [ ] Hybrid links (VPN vs dedicated) chosen against throughput/latency needs
