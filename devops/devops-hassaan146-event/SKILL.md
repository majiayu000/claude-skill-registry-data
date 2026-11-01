---
name: devops
description: >-
  Use when the user needs to deploy, operate, secure, or scale running infrastructure — cloud
  architecture (multi-region, VPC, FinOps), CI/CD and deployment strategies, secrets/IAM/supply-chain
  security, observability and SLO alerting, SRE and incident response, Kubernetes vs ECS and autoscaling,
  Terraform/Pulumi/CDK, or platform engineering and DORA metrics. Also for generating runbooks, pipeline
  configs, Terraform modules, or Kubernetes manifests. For choosing the system's architecture or stack
  before it runs (monolith vs microservices, which database), use software-architect.
---

# DevOps & Infrastructure Best Practices

Practitioner-grounded advisor covering eight domains with opinionated best practices, failure patterns, corrective heuristics, and decision frameworks. Sourced from DORA research, AWS Well-Architected Framework, Google SRE, and practitioners including Nicole Forsgren, Charity Majors, Kelsey Hightower, and Jez Humble.

## Output discipline

Deliver only what the user will actually use. Never leak internal scaffolding into the output:
- No reference citations the reader can't see ("§3.2", "per the knowledge base", "KB §1.4").
- No mode or process narration ("Mode: Generate", "I have everything I need", "following the skill's methodology").
- No skill-handoff chatter inside the deliverable.

Apply frameworks silently — name one only when it helps the reader, not to show your work. When context is missing, state your assumption in one line and proceed; don't interrogate.

## How to Use This Skill

### 1. Identify the Domain

Map the user's question to one or more domains. **Read the corresponding reference file(s) before responding.**

| Domain | Reference File | Trigger Topics |
|--------|---------------|----------------|
| Cloud Architecture | `references/cloud-architecture.md` | Multi-region/AZ, VPC, subnets, service mesh networking, FinOps, cell-based architecture, vendor lock-in, landing zones |
| CI/CD Pipelines | `references/cicd-pipelines.md` | Trunk-based dev, feature flags, monorepo/polyrepo, build caching, deployment strategies, GitOps, ArgoCD, artifact security, SLSA |
| Security & Compliance | `references/security-compliance.md` | Secrets management, Vault, IAM, RBAC/ABAC, supply chain security, SBOM, zero trust, compliance-as-code, OPA, shift-left |
| Observability | `references/observability.md` | Three pillars, OpenTelemetry, alerting, SLO-based alerts, alert fatigue, observability pipelines, cardinality |
| Incident & Reliability | `references/incident-reliability.md` | SLOs, SLIs, error budgets, incident response, postmortems, chaos engineering, SRE |
| Container Orchestration | `references/container-orchestration.md` | Kubernetes, ECS, Fargate, HPA, VPA, KEDA, autoscaling, service mesh, cluster topology |
| Infrastructure as Code | `references/infrastructure-as-code.md` | Terraform, Pulumi, CDK, OpenTofu, state management, drift, policy-as-code, Checkov |
| Developer Experience | `references/developer-experience.md` | IDP, Backstage, golden paths, platform engineering, DORA metrics, platform team models |

### 2. Adapt to Expertise Level

- **Executive/founder**: Lead with business impact and decision frameworks. Minimize jargon. Use quick-reference heuristics.
- **Engineering leader**: Balance strategy with technical depth. Include failure patterns and corrective heuristics.
- **Practitioner/engineer**: Go deep on implementation — concrete configs, commands, tool comparisons, code.

### 3. Response Structure

**Advisory questions** (reviews, tool selection, best practices):
1. State the principle
2. Present the decision framework or heuristic
3. Call out the most common failure pattern
4. Give the corrective heuristic
5. Quick-reference decision table if applicable

**Artifact generation** (runbooks, configs, manifests, pipelines):
1. Read relevant reference file for constraints
2. Generate artifact following the principles (least privilege, digest pinning, affected-only builds, etc.)
3. Annotate with comments explaining *why* each decision was made
4. Call out failure patterns the artifact prevents

### 4. Cross-Domain Routing

Common multi-domain queries:
- "Set up a new service" → CI/CD + Containers + Observability + Security
- "Review our infrastructure" → Cloud Architecture + IaC + Security + Cost
- "Improve deployment speed" → CI/CD + Developer Experience + DORA
- "Production incident process" → Incident & Reliability + Observability

Read all relevant reference files before responding.

## Quick-Reference Decision Heuristics

### When to go multi-region
- Contractual RTO < 30 min for full regional failure, OR
- Data sovereignty requiring geographic separation, OR
- Sub-50ms latency for globally distributed users
- **Default**: Three-AZ in one region + documented failover runbooks

### When to adopt a service mesh
- ≥15 services with cross-service mTLS, AND
- Dedicated platform team, AND
- Need for L7 traffic-weighted canary routing
- **Default**: API gateway mTLS + cloud-native private connectivity

### IaC tool selection
- Multi-cloud or compliance-heavy → Terraform/OpenTofu
- Complex logic, general-purpose language preference → Pulumi
- AWS-only, tight construct ecosystem → AWS CDK

### Kubernetes vs ECS/Fargate
- <20 services, AWS-native, no K8s expertise → ECS/Fargate
- Multi-cloud, platform team available → EKS/GKE/AKS
- K8s without node management (AWS) → EKS on Fargate

### Autoscaling selector
- CPU/memory-driven stateless → HPA
- Optimize resource allocation → VPA (recommendation mode first)
- Event-driven (queues, topics, cron) → KEDA

### Deployment strategy
- Stateless, double capacity budget → Blue-Green
- Progressive validation → Canary (1% → 25% → 50% → 100%)
- Cost-sensitive, slower rollback OK → Rolling Update

### DORA elite benchmarks
- Deploy frequency: multiple/day
- Lead time: <1 hour
- Restore time: <1 hour
- Change failure rate: 0-15%
