---
name: "tech-hiring-infrastructure-cloud-engineering"
description: "Infrastructure and cloud engineers design, build, and operate the foundational systems that everything else runs on: networking, storage, compute, cloud architecture, security boundaries, and cost management. More architectural than DevOps "
---

# Infrastructure & Cloud Engineering — Hiring Guide

## How to Use This Guide

- **Sourcing:** Use the title synonyms and Boolean strings in each section
- **Screening:** Skill tiers: T1 = must-have, T2 = differentiator, T3 = rare upside
- **Interviewing:** Use the assessment approach to design your interview loop
- **Benchmarking:** Comp ranges are US market, growth-stage (Series B–D). Adjust for location, company stage, and current market

---

## Universal Seniority Framework

Applies across all disciplines. Use as a baseline — teams vary on exact year ranges.

| Level | Typical YoE | What they own | Mentorship | Scope |
|---|---|---|---|---|
| **Junior (L3 / IC1)** | 0–2 years | Defined tasks, bug fixes, small features | Needs daily guidance | Self |
| **Mid (L4 / IC2)** | 2–5 years | Features end-to-end, moderate ambiguity | Occasional junior support | Feature / component |
| **Senior (L5 / IC3)** | 5–8 years | Projects, technical decisions, cross-team coordination | Active mentorship | Team / project |
| **Staff (L6 / IC4)** | 8–12 years | Technical strategy, cross-team systems, org-wide standards | Multiplies teams | Org |
| **Principal / Distinguished** | 12+ years | Company-wide technical direction, external influence | Defines engineering culture | Company |

**Promotion-readiness signal:** Consistently operating at the *next* level before the title, not just meeting current-level expectations.

---

## Infrastructure & Cloud Engineering

### What This Role Does
Infrastructure and cloud engineers design, build, and operate the foundational systems that everything else runs on: networking, storage, compute, cloud architecture, security boundaries, and cost management. More architectural than DevOps — focused on the environment teams deploy into, not the deployment pipelines themselves.

### Titles & Synonyms

| Level | Common titles |
|---|---|
| Junior | Cloud Engineer, Infrastructure Engineer, Network Engineer |
| Mid | Cloud Infrastructure Engineer, Solutions Architect (associate), Cloud Architect |
| Senior | Senior Cloud Architect, Senior Infrastructure Engineer, Solutions Architect |
| Staff+ | Principal Architect, Distinguished Engineer, Head of Infrastructure |
| Specialist | FinOps Engineer, Network Architect, Storage Engineer |

### Skill Tiers

**Tier 1 — Must-have:**
- Deep proficiency in at least one major cloud (AWS, GCP, or Azure) — not surface-level
- Networking fundamentals: TCP/IP, DNS, HTTP/HTTPS, VPC/VNet, subnets, routing, firewalls
- IAM and security primitives: roles, policies, least-privilege design
- Storage: object storage (S3/GCS), block storage, lifecycle policies
- Load balancing, CDN, DNS management

**Tier 2 — Differentiator:**
- Multi-account/multi-project cloud governance
- Private networking: VPN, Direct Connect, peering, Transit Gateway
- Container networking (advanced Kubernetes networking, Cilium, Calico)
- Disaster recovery: RTO/RPO design, backup strategy, multi-region failover
- FinOps: reserved instances, spot/preemptible, cost allocation tagging
- Compliance in cloud: PCI-DSS, SOC2, HIPAA control mapping

**Tier 3 — Bonus:**
- Multi-cloud architecture
- Edge computing, CDN engineering (Cloudflare Workers, Lambda@Edge)
- Custom network hardware experience (for very large scale)
- Cloud provider certifications (AWS Solutions Architect Professional, GCP Professional)

### Sourcing Strings

```bash
# LinkedIn X-Ray
site:linkedin.com/in/ ("cloud architect" OR "infrastructure engineer" OR "solutions architect" OR "cloud engineer") (AWS OR GCP OR Azure OR Terraform OR "cloud architecture") -recruiter -talent

# Network/security focus
site:linkedin.com/in/ ("network engineer" OR "cloud network" OR "infrastructure") (VPC OR "zero trust" OR "network architecture" OR BGP) -recruiter

# GitHub
site:github.com "joined on" (AWS OR Terraform OR "cloud infrastructure" OR GCP) "architect" OR "infrastructure" followers:>20
```

### Seniority Signals

- **Mid → Senior:** Designs for failure by default; raises blast radius, dependency, and recovery concerns unprompted
- **Senior → Staff:** Defines cloud governance policy; enables teams to build self-service infrastructure safely; leads cost governance
- **Key signal:** Ask them to design a multi-region, highly available system for a realistic workload. Great candidates immediately ask about RTO, RPO, and budget constraints before drawing anything.

### Red Flags
- "I just spin up EC2 instances" — no architectural thinking
- No understanding of IAM or security boundaries
- Has never thought about network egress costs
- Cannot explain the tradeoffs between single-region and multi-region deployments
- Cloud certifications only — no hands-on production experience

### Compensation (2025, US, Growth-Stage)

| Level | Base salary range |
|---|---|
| Junior | $90k – $130k |
| Mid | $130k – $175k |
| Senior | $160k – $215k |
| Staff | $200k – $270k |
| Principal / Architect | $240k – $320k+ |
