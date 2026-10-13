---
name: platform-engineering
description: Design, build, and operate an Internal Developer Platform (IDP) that reduces cognitive load for engineering teams. Covers platform team structure (Team Topologies), golden paths, self-service infrastructure, IDP components, DORA-based KPIs, platform maturity model, and the platform-as-product mindset.
triggers:
  - "platform engineering"
  - "internal developer platform"
  - "IDP"
  - "platform team"
  - "golden path"
  - "self-service infrastructure"
  - "reduce cognitive load for engineers"
  - "paved road"
  - "developer platform"
  - "platform as product"
audience: engineer, manager
---

# Platform Engineering

## Context

Platform engineering is the discipline of designing and building toolchains and workflows that enable self-service capabilities for software engineering organizations. The goal is to reduce cognitive load on stream-aligned teams (product squads) by providing opinionated, curated paths — "golden paths" — for building, deploying, observing, and operating software.

A platform team is not an ops team or an infra team. It is an **internal product team** whose customers are other engineers. Like any product team, it must understand its users, measure adoption, and iterate based on feedback.

Use this skill when:
- Your engineers spend too much time on undifferentiated infrastructure toil
- Onboarding new engineers or new services takes weeks
- Each team has invented its own CI pipeline, observability setup, or secrets strategy
- You want to scale engineering capacity without scaling headcount proportionally

---

## Core Concepts

### What Is an Internal Developer Platform (IDP)?

An IDP is the sum of all the technology and tools that a platform team builds and maintains. It is the product surface that stream-aligned teams consume. It is NOT a single tool — it is an integrated suite:

| Layer | Examples |
|---|---|
| **Service scaffolding** | Backstage, Cookiecutter, custom CLI (`acme new service`) |
| **CI/CD templates** | Reusable GitHub Actions workflows, Tekton pipelines |
| **Secrets management** | Vault, AWS SSM, external-secrets operator |
| **Container/runtime** | Kubernetes namespaces + Helm charts, ECS task templates |
| **Observability** | Pre-configured Grafana dashboards, Datadog APM templates |
| **Service catalog** | Backstage catalog, PagerDuty service registry |
| **Infrastructure as code** | Terraform modules, Pulumi components, CDK constructs |
| **Environments** | Ephemeral preview environments, dev/staging/prod parity |
| **Security guardrails** | Policy-as-code (OPA/Kyverno), vulnerability scanning in CI |

### The Golden Path

A golden path is the opinionated, pre-built route to doing something correctly at your company. It is:
- **Fast to follow** — lower friction than rolling your own
- **Secure by default** — guardrails baked in
- **Observable by default** — metrics and logs wired up automatically
- **Not mandatory** — but diverging from it has explicit costs

> "Paved road, not a prison. Teams can leave the path, but they carry the maintenance burden."

A golden path is defined once, maintained by the platform team, and consumed many times by product teams.

### Team Topologies Connection

Platform engineering maps directly onto Team Topologies (Skelton & Pais):

| Team Type | Role |
|---|---|
| **Platform team** | Builds and operates the IDP; reduces cognitive load for others |
| **Stream-aligned team** | Product squads that consume the platform; move fast on features |
| **Enabling team** | Coaches stream-aligned teams on adopting new platform capabilities |
| **Complicated-subsystem team** | Owns high-complexity components (ML infra, custom runtimes) |

The primary interaction mode between platform and stream-aligned teams is **X-as-a-Service**: the platform team provides stable, self-service capabilities that product teams consume without needing to coordinate.

---

## Platform Maturity Model (0 → 4)

Use this model to assess where your organization is today and what the next horizon looks like.

### Level 0 — No Platform
- Every team manages its own infrastructure from scratch
- No shared tooling, no shared CI templates
- Onboarding a new service takes 2–4 weeks
- **Signal**: Engineers copy-paste infrastructure from other repos

### Level 1 — Shared Scripts / Wiki
- Some shared bash scripts, Makefiles, or Confluence pages exist
- No versioning, no ownership, no SLA
- Hard to discover, frequently outdated
- **Signal**: "Ask Sarah, she knows how the deploy script works"

### Level 2 — Shared Library / Templates
- Versioned, published CI/CD templates (e.g., reusable GitHub Actions)
- Common Terraform modules in a shared registry
- No unified portal — discoverability is still poor
- **Signal**: Teams can copy a template and customize it; platform team fields many Slack questions

### Level 3 — Self-Service Portal (IDP)
- Developer portal (e.g., Backstage) with service catalog, templates, and docs
- New service scaffold takes < 30 minutes end-to-end
- Observability and secrets are wired in by default
- Platform team has an SLA for its services
- **Signal**: New engineers can create and deploy a new service on day one

### Level 4 — Platform as Product
- Platform team has a product roadmap, OKRs, and a feedback loop
- Developer satisfaction is measured regularly (surveys, NPS)
- DORA metrics and platform adoption are tracked as KPIs
- Platform evolves based on data, not gut feel
- Golden paths cover 80%+ of workloads
- **Signal**: Platform team proactively deprecates old patterns; stream-aligned teams rarely need platform team support for standard tasks

---

## How to Start a Platform Team

> **Don't boil the ocean.** Start with the single highest-friction pain point. Ship something small that works, then expand.

### Step 1: Identify the Pain
Run a developer survey or conduct 5–10 interviews with engineers. Ask:
- What do you spend the most time on that isn't writing product code?
- What took longest when you joined the team?
- What breaks most often in your deploy pipeline?
- What do you have to ask another team for?

Rank pain points by frequency × severity. Pick the #1 item.

### Step 2: Define the Scope of MVP
Resist the urge to build an IDP immediately. Your first deliverable should be a single golden path for the most common pattern. Examples:
- A standard GitHub Actions workflow for building and deploying a Node.js service
- A Terraform module for provisioning a standard RDS instance with best-practice security defaults
- A service scaffolding CLI that creates a new repo with all the right files

### Step 3: Establish a Feedback Loop
Before shipping broadly, embed with 1–2 stream-aligned teams. Watch them use what you built. Fix the sharp edges. This is user research, not QA.

### Step 4: Build Discoverability
A golden path nobody knows about is a golden path nobody uses. Put documentation in a developer portal. Send announcements. Hold office hours. Measure adoption.

### Step 5: Define an SLA
Platform services are not side projects. Define an SLA:
- P0 incident response time
- Planned maintenance windows
- Deprecation notice period for breaking changes
- Support channel (Slack channel, ticketing system)

### Step 6: Measure and Iterate
Track the KPIs below. Review quarterly. Retire what isn't adopted. Expand what reduces friction.

---

## Platform KPIs

### DORA Metrics (Primary)
| Metric | Definition | Elite Target |
|---|---|---|
| **Deployment frequency** | How often do teams deploy to production? | Multiple times/day |
| **Lead time for changes** | Time from first commit to production | < 1 hour |
| **Change failure rate** | % of deployments causing incidents | < 5% |
| **Time to restore service** | MTTR after an incident | < 1 hour |

### Platform-Specific KPIs
| Metric | Definition | Target |
|---|---|---|
| **Time to onboard new service** | Minutes from `git init` to first deploy | < 60 min |
| **Golden path adoption rate** | % of services using standard templates | > 80% |
| **Support ticket volume** | Platform-related tickets per team per week | Trending down |
| **Developer satisfaction (CSAT/NPS)** | Survey score | > 70 NPS |
| **Mean time to self-serve** | Time engineer spends before needing platform help | Trending up |
| **Time to onboard new engineer** | Days until new hire ships to production | < 5 days |

---

## Platform Team Charter Template

```
PLATFORM TEAM CHARTER
=====================

Team name: ___________
Date: ___________
Platform owner: ___________

MISSION
-------
We exist to reduce the cognitive load of [org name]'s engineering teams
by providing self-service infrastructure, golden paths, and opinionated
tooling — so product teams can focus on product, not plumbing.

INTERNAL CUSTOMERS
------------------
Primary: All stream-aligned engineering teams
Secondary: Enabling teams, security team, SRE

PLATFORM SCOPE (in/out)
-----------------------
In scope:
  - [ ] CI/CD templates and pipelines
  - [ ] Service scaffolding / new service CLI
  - [ ] Container runtime and Kubernetes templates
  - [ ] Secrets management
  - [ ] Observability stack (metrics, logs, traces)
  - [ ] Developer portal / service catalog
  - [ ] Infrastructure-as-code modules
  - [ ] Ephemeral environments

Out of scope (explicitly):
  - [ ] Application business logic
  - [ ] Database schema design
  - [ ] Product roadmap prioritization

SUCCESS METRICS (quarterly OKRs)
---------------------------------
Objective: [e.g., Reduce time to first deploy for new services]
  KR1: Time to onboard new service < 60 minutes (baseline: ___ min)
  KR2: Golden path adoption > 80% (baseline: __%)
  KR3: Platform CSAT > 70 NPS (baseline: ___)

SLA COMMITMENTS
---------------
- P0 incident response: < 15 minutes
- P1 incident response: < 1 hour
- Planned maintenance: 7-day advance notice
- Deprecation notice: 90 days minimum
- Support channel: #platform-help (Slack)

TEAM WORKING AGREEMENTS
------------------------
- We treat internal developers as customers
- We measure adoption before claiming success
- We do not build features without talking to at least 2 consuming teams first
- We maintain a public roadmap
- We version all public APIs and templates using semver
```

---

## IDP Component Checklist

Use this to audit your current platform coverage:

### Foundation (Must Have — Level 3)
- [ ] **Service scaffolding**: New service created from template in < 30 min
- [ ] **CI/CD templates**: Versioned, reusable pipelines; < 10 min build time
- [ ] **Container registry**: Automated image building and tagging
- [ ] **Deployment**: Repeatable deploy to at least dev + prod
- [ ] **Secrets management**: No secrets in code or CI env vars (use Vault / SSM)
- [ ] **Basic observability**: Logs aggregated; basic health metrics available
- [ ] **Service catalog**: Inventory of all services with owner, repo, runbook link

### Accelerators (Should Have — Level 3+)
- [ ] **Ephemeral environments**: PR-level preview environments
- [ ] **IaC modules**: Terraform/Pulumi modules for common resources (DB, queue, cache)
- [ ] **Developer portal**: Backstage or equivalent; searchable catalog + docs
- [ ] **Policy as code**: OPA or Kyverno guardrails in CI and cluster admission
- [ ] **Distributed tracing**: OpenTelemetry collector; traces in Jaeger/Tempo
- [ ] **SLO tooling**: SLO definitions and burn-rate alerting per service

### Differentiators (Nice to Have — Level 4)
- [ ] **Self-service databases**: Operator-provisioned DB with one-click UI
- [ ] **Cost attribution**: Per-service cloud cost visibility
- [ ] **Chaos engineering tooling**: Litmus / Chaos Monkey integrated in staging
- [ ] **Internal marketplace**: Reusable libraries, APIs, events discoverable in portal
- [ ] **Automated dependency upgrades**: Renovate bot with auto-merge for patch versions

---

## Paved Road Definition Template

For each golden path you create, document:

```
GOLDEN PATH: [Name, e.g., "Standard Python microservice"]
================================================

WHAT IT COVERS
--------------
Language/runtime: Python 3.12
Deployment target: Kubernetes (EKS)
CI/CD: GitHub Actions + ArgoCD
Observability: Datadog APM + structured JSON logging
Secrets: AWS SSM via external-secrets operator

WHAT YOU GET OUT OF THE BOX
----------------------------
- Dockerfile with multi-stage build
- GitHub Actions workflow: lint → test → build → push → deploy
- Helm chart template pre-configured for HPA and PodDisruptionBudget
- Datadog APM auto-instrumentation
- /health and /ready endpoints
- Pre-configured Dependabot for dependency updates
- CODEOWNERS pre-populated

HOW TO USE IT
-------------
1. Run: acme new service --type python-api --name my-service
2. Follow prompts (team name, PagerDuty service, Slack alert channel)
3. Push to main → auto-deploys to dev

LEAVING THE PATH
----------------
Teams may diverge from this path. If you do:
- Document why in your service's README
- You own the maintenance of any diverged components
- Platform team offers no SLA on non-standard configurations
- You must pass a platform review before production deployment

SUPPORTED VERSIONS
------------------
Version: 2.3.0
Supported until: 2026-01
Successor: python-api-v3 (migration guide: <link>)
```

---

## Developer Satisfaction Survey Template

Run quarterly. Keep it short (< 5 minutes). Send in Slack.

```
PLATFORM DEVELOPER SATISFACTION SURVEY
Quarter: Q[X] [YEAR]

1. How satisfied are you with the platform overall?
   [ ] Very dissatisfied  [ ] Dissatisfied  [ ] Neutral  [ ] Satisfied  [ ] Very satisfied

2. How easy is it to deploy a new service from scratch?
   [ ] Very hard  [ ] Hard  [ ] OK  [ ] Easy  [ ] Very easy

3. How often do you need to ask the platform team for help with standard tasks?
   [ ] Daily  [ ] Weekly  [ ] Monthly  [ ] Rarely  [ ] Never

4. Which platform component causes you the most friction? (pick one)
   [ ] CI/CD  [ ] Secrets  [ ] Observability  [ ] Environments  [ ] Service catalog
   [ ] IaC modules  [ ] Documentation  [ ] Other: ________

5. What one thing should the platform team build, fix, or improve next?
   [open text]

6. On a scale of 0-10, how likely are you to recommend the platform to
   a new engineer joining your team?
   [0–10 NPS score]

7. Anything else? [optional open text]
```

---

## Platform KPI Dashboard Template

Track these metrics monthly. Review in platform team retro and with engineering leadership quarterly.

```
PLATFORM KPI DASHBOARD — [Month] [Year]
=========================================

DORA METRICS
------------
Deployment frequency (org avg):    ___/day   (target: multiple/day)
Lead time for changes (p50):        ___ hrs   (target: < 1 hr)
Lead time for changes (p95):        ___ hrs
Change failure rate:                ___%      (target: < 5%)
Time to restore (MTTR p50):         ___ hrs   (target: < 1 hr)

PLATFORM ADOPTION
-----------------
Services using CI template:         ___%      (target: > 80%)
Services using IaC modules:         ___%
Services in service catalog:        ___%
Services with SLO defined:          ___%

ONBOARDING
----------
Avg time to onboard new service:    ___ min   (target: < 60 min)
Avg time new engineer first deploy: ___ days  (target: < 5 days)

SUPPORT LOAD
------------
Platform Slack questions this month: ___       (trend: ↑ / ↓ / →)
Platform tickets opened:             ___
Tickets resolved within SLA:         ___%

DEVELOPER SATISFACTION
----------------------
CSAT survey score (last quarter):   ___/5
NPS score:                          ___       (target: > 70)
Top pain point cited:               ___

PLATFORM HEALTH
---------------
Platform P0 incidents:              ___
Mean time to detect:                ___ min
Mean time to restore:               ___ min
SLA met this month:                 Yes / No
```

---

## Common Pitfalls

### 1. Building for Hypothetical Use Cases
Platform teams often over-engineer for flexibility no one needs. Start with what 3+ teams need today. Refactor when you have the second real use case.

### 2. No Developer Feedback Loop
A platform without users is a hobby project. Embed with product teams. Watch them struggle. Fix that. Repeat.

### 3. Paved Road as Prison
Mandating golden paths without allowing deviation kills trust. Teams will route around you. Make the path easy to follow and transparent about costs of leaving it — never block teams from leaving.

### 4. Platform Team as Gatekeeper
If every deploy requires a ticket to the platform team, you have built a bottleneck, not a platform. Self-service is the goal. Human intervention should be the exception.

### 5. Measuring Output, Not Outcomes
"We shipped 12 features" is not a platform KPI. "Time to onboard a new service decreased from 4 hours to 25 minutes" is.

### 6. Ignoring Deprecation
Old golden paths accumulate. Define a deprecation policy at the start. Publish migration guides. Sunset with 90-day notice minimum.

---

## Output Format

When applying this skill, the agent should:

1. **Assess the current state** using the Platform Maturity Model (0–4). Ask what pain points engineers report before recommending solutions.
2. **Recommend the smallest viable next step**, not the full IDP. Identify the single highest-friction item.
3. **Produce artifacts on request**: charter template, IDP component checklist, golden path definition, KPI dashboard, developer survey.
4. **Call out anti-patterns** if the conversation reveals them (gatekeeper behavior, no feedback loop, mandatory-only path).
5. **Reference Team Topologies** when discussing team structure or interaction modes.
6. Format checklists as Markdown task lists `- [ ]`. Format KPI dashboards and templates as code blocks.

---

## References

- Evan Bottcher — ["What is Platform Engineering?"](https://martinfowler.com/articles/platform-engineering.html) (martinfowler.com)
- Skelton & Pais — *Team Topologies* (IT Revolution, 2019)
- CNCF — [Platform Engineering Whitepaper](https://tag-app-delivery.cncf.io/whitepapers/platforms/) (tag-app-delivery.cncf.io)
- LeadDev — ["How to implement platform engineering at scale"](https://leaddev.com/platform-engineering)
- Humanitec — [Platform Engineering Report](https://humanitec.com/platform-engineering-report) (annual survey)
- Gartner — Platform Engineering Hype Cycle (2023/2024)
- DORA — [State of DevOps Report](https://dora.dev) (annual)
