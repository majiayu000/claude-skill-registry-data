---
name: pair-capability-assess-infrastructure
description: "Assess infrastructure strategy using resolution cascade (Argument > Adoption > Assessment). Reads infrastructure guidelines, proposes cloud/CI/CD/deployment choices, writes infrastructure.md adoption, composes /pair-capability-record-decision. Idempotent."
version: 0.4.1
author: Foomakers
---

# /pair-capability-assess-infrastructure — Infrastructure Assessment

Evaluate and decide on infrastructure strategy: cloud provider, CI/CD pipeline, deployment patterns, IaC approach, and environments. Follows the resolution cascade.

## Arguments

| Argument  | Required | Description                                                                |
| --------- | -------- | -------------------------------------------------------------------------- |
| `$choice` | No       | Override: skip assessment, use this infrastructure choice directly (e.g. `github-actions`, `aws`) |

## Composed Skills

| Skill              | Type       | Required                                               |
| ------------------ | ---------- | ------------------------------------------------------ |
| `/pair-capability-record-decision` | Capability | Yes — records infrastructure decision as ADR or ADL    |

## Proposal Target

The rendered adoption content is destined for this file — the caller writes it via `/pair-capability-record-decision`:

- **Target**: [adoption/tech/infrastructure.md](../../../.pair/adoption/tech/infrastructure.md) — core infrastructure sections
- **Ownership**: Full file, except observability section (owned by /pair-capability-assess-observability)

## Adoption File

- **Target**: [adoption/tech/infrastructure.md](../../../.pair/adoption/tech/infrastructure.md) — core infrastructure sections
- **Ownership**: Full file, except observability section (owned by /pair-capability-assess-observability)

## Algorithm

### Step 1: Resolution Cascade

#### Path A — Argument Override

1. **Check**: Is `$choice` provided?
2. **Skip**: If not provided, go to Path B.
3. **Act**: Confirm the choice with the developer. Check for conflicts with existing adoption.
4. **Verify**: Developer confirms. Proceed to Step 3.

#### Path B — Adoption Exists

1. **Check**: Does [adoption/tech/infrastructure.md](../../../.pair/adoption/tech/infrastructure.md) exist and is it populated?
2. **Skip**: If not populated or missing, go to Path C.
3. **Act**: Read current adoption. Confirm it's valid.
4. **Check**: Does a corresponding decision record exist?
5. **Act**: If decision record missing, compose `/pair-capability-record-decision` to backfill.
6. **Verify**: Done — exit skill.

#### Path C — Full Assessment

1. **Act**: Proceed to Step 2.

### Step 2: Read Guidelines

1. **Act**: Read infrastructure guidelines:
   - [Infrastructure README](../../../.pair/knowledge/guidelines/infrastructure/README.md) — practice areas and decision framework
   - [CI/CD Strategy](../../../.pair/knowledge/guidelines/infrastructure/cicd-strategy) — pipeline design and automation
   - [Cloud Services](../../../.pair/knowledge/guidelines/infrastructure/cloud-services) — cloud platform selection
   - [Deployment Patterns](../../../.pair/knowledge/guidelines/infrastructure/deployment-patterns) — deployment strategies
   - [Infrastructure as Code](../../../.pair/knowledge/guidelines/infrastructure/infrastructure-as-code) — IaC practices
2. **Act**: Read project context:
   - [adoption/product/PRD.md](../../../.pair/adoption/product/PRD.md) — scale, budget, compliance
   - [adoption/tech/architecture.md](../../../.pair/adoption/tech/architecture.md) — architecture pattern (infra must support it)
3. **Verify**: Guidelines and context loaded.

### Step 3: Evaluate Options

1. **Act**: Evaluate infrastructure options using the Practice Selection Matrix from guidelines:
   - **Cloud provider**: AWS, GCP, Azure, self-hosted, or none (desktop/CLI projects)
   - **CI/CD**: GitHub Actions, GitLab CI, Jenkins, CircleCI
   - **Deployment**: Containers vs serverless vs static, blue-green vs canary vs rolling
   - **IaC**: Terraform, CDK, Pulumi, none (simple projects)
   - **Environments**: dev, staging, production setup

2. **Act**: Present recommendation:

   > **Infrastructure Recommendation:**
   > - CI/CD: [tool] — [rationale]
   > - Deployment: [strategy] — [rationale]
   > - Cloud: [provider or "none"] — [rationale]
   > - IaC: [tool or "not needed"] — [rationale]

3. **Verify**: Developer approves.

### Step 4: Write Adoption File

1. **Act**: Write or update [adoption/tech/infrastructure.md](../../../.pair/adoption/tech/infrastructure.md):
   - Concise, prescriptive statements
   - Preserve observability section if it exists (owned by /pair-capability-assess-observability)
2. **Verify**: Adoption file written and consistent.

### Step 5: Record Decision

1. **Act**: Compose `/pair-capability-record-decision`:
   - `$type`: `architectural` (infrastructure decisions affect system structure)
   - `$topic`: `infrastructure-strategy`
   - `$summary`: "[Summary of key infrastructure choices]"
2. **Verify**: ADR created. Adoption consistent.

## Output Format

```text
ASSESSMENT COMPLETE:
├── Domain:    Infrastructure
├── Path:      [Argument Override | Adoption Exists | Full Assessment]
├── Decision:  [key infrastructure choices]
├── Adoption:  [infrastructure.md — written | confirmed | updated]
├── Record:    [ADR path — created | exists | backfilled]
└── Status:    [Complete | Confirmed existing]
```

## Composition Interface

When composed by `/pair-process-bootstrap`:

- **Input**: `/pair-process-bootstrap` invokes during Phase 2.
- **Output**: Returns decision summary and adoption file path.

When invoked **independently**:

- Full interactive flow. Developer commits changes.

## Edge Cases

- **Project doesn't need infrastructure** (e.g. pure library, CLI tool): Write minimal infrastructure.md noting CI/CD only, no cloud deployment.
- **Adoption file partially exists**: Fill gaps, preserve existing content.
- **Observability section exists**: Preserve it — owned by /pair-capability-assess-observability.

## Graceful Degradation

- If infrastructure guidelines not found, use minimal assessment: ask developer for CI/CD and deployment preferences.
- If `/pair-capability-record-decision` not installed, warn and skip recording.
- If adoption directory doesn't exist, create it.

## Notes

- Infrastructure decisions are typically **architectural** → produce ADR.
- **Section ownership**: /pair-capability-assess-observability owns observability section of infrastructure.md if that section exists there; otherwise observability goes in its own section of way-of-working or a separate file.
- Educational content (cloud concepts, IaC principles) stays in guidelines.
