---
name: "tech-hiring-devops-platform-engineering"
description: "DevOps and Platform engineers build and maintain the systems that enable development teams to ship software reliably, safely, and quickly. This includes CI/CD infrastructure, container orchestration, cloud resource management, observability"
---

# DevOps & Platform Engineering — Hiring Guide

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

## DevOps & Platform Engineering

### What This Role Does
DevOps and Platform engineers build and maintain the systems that enable development teams to ship software reliably, safely, and quickly. This includes CI/CD infrastructure, container orchestration, cloud resource management, observability, and increasingly the "internal developer platform" that reduces toil for application engineers. The lines between DevOps, SRE, and Platform Engineering are blurring.

### Titles & Synonyms

| Level | Common titles |
|---|---|
| Junior | DevOps Engineer, Junior SRE, Infrastructure Engineer, Cloud Engineer |
| Mid | DevOps Engineer, SRE, Platform Engineer, Cloud Infrastructure Engineer |
| Senior | Senior DevOps Engineer, Senior SRE, Senior Platform Engineer |
| Staff+ | Staff Platform Engineer, Principal SRE, Head of Platform/Infrastructure |
| Specialist | Release Engineer, Build Engineer, Developer Experience Engineer |

### Skill Tiers

**Tier 1 — Must-have:**
- Linux administration: shell scripting, systemd, file systems, networking
- Containers: Docker — building, optimising, and debugging images
- CI/CD: GitHub Actions, Jenkins, CircleCI, or GitLab CI — pipeline design and maintenance
- At least one major cloud: AWS, GCP, or Azure (certifications are a useful signal, not a requirement)
- Infrastructure as Code: Terraform or Pulumi

**Tier 2 — Differentiator:**
- Kubernetes: deployment, scaling, networking (ingress, services), Helm charts
- Observability: Prometheus, Grafana, Datadog, OpenTelemetry — not just setting up dashboards, but designing meaningful alerts
- GitOps: ArgoCD, FluxCD
- Secrets management: Vault, AWS Secrets Manager
- Service mesh: Istio, Linkerd (senior+)
- Cost engineering / FinOps

**Tier 3 — Bonus:**
- Custom Kubernetes operators or controllers
- Multi-cloud or hybrid cloud architecture
- Chaos engineering (Chaos Monkey, LitmusChaos)
- Open source contributions to CNCF projects
- Platform product thinking — treating internal tooling as a product

### Sourcing Strings

```bash
# LinkedIn X-Ray
site:linkedin.com/in/ ("DevOps engineer" OR "SRE" OR "platform engineer" OR "site reliability") (Kubernetes OR Terraform OR AWS OR GCP OR "GitHub Actions") -recruiter -talent

# Kubernetes specialist
site:linkedin.com/in/ ("platform engineer" OR "DevOps" OR "SRE") (Kubernetes OR "K8s" OR ArgoCD OR Helm OR Terraform) -recruiter

# GitHub
language:go topic:kubernetes followers:>25 pushed:>2025-01-01
site:github.com "joined on" (Kubernetes OR Terraform OR "CI/CD" OR ArgoCD) "platform" OR "DevOps" OR "infrastructure"
```

### Seniority Signals

- **Junior → Mid:** Can debug a broken CI pipeline or failing pod without step-by-step guidance
- **Mid → Senior:** Designs infrastructure that development teams can self-service; treats reliability as a feature with SLOs and error budgets
- **Senior → Staff:** Builds platforms that accelerate engineering org-wide; drives adoption through documentation, tooling, and internal advocacy
- **SRE vs. DevOps vs. Platform:** SRE is operations with software engineering principles (reliability focus); DevOps is CI/CD and deployment culture; Platform Engineering is building internal products for developers. Overlap is significant.

### Interview & Assessment Loop

| Stage | Format | What you're assessing |
|---|---|---|
| Technical screen | Linux/shell questions + cloud fundamentals | Baseline hands-on competency |
| Live debugging | Broken Kubernetes cluster or failing pipeline to fix | Real-world problem-solving |
| System design | Design CI/CD for a 50-engineer org or a multi-region deployment | Scale and reliability thinking |
| IaC review | Review a Terraform module they've written | Code quality, security awareness |
| Behavioural | STAR — incident response, on-call experience, developer relationships | On-call culture, communication under pressure |

**Best live exercise:** Give them a broken `kubectl` environment and watch how they debug. The best candidates narrate their thinking, check logs systematically, and recognise multiple failure modes.

### Red Flags
- "I just use the cloud console" — no IaC experience
- Kubernetes experience is only `kubectl apply` — no understanding of scheduling, networking, or failure modes
- No on-call experience or no structured incident response approach
- Over-indexes on tools without understanding the underlying Linux/networking fundamentals
- No SLO/SLI thinking — "the system is either up or down"

### Compensation (2025, US, Growth-Stage)

| Level | Base salary range |
|---|---|
| Junior | $95k – $135k |
| Mid | $135k – $175k |
| Senior | $160k – $220k |
| Staff | $200k – $270k |
| Principal | $240k – $315k+ |
