---
name: pair-capability-assess-observability
description: "Assess observability strategy using resolution cascade (Argument > Adoption > Assessment). Reads observability guidelines, proposes monitoring/logging/tracing choices, writes infrastructure.md observability section, composes /pair-capability-record-decision. Idempotent."
version: 0.4.1
author: Foomakers
---

# /pair-capability-assess-observability — Observability Assessment

Evaluate and decide on the observability strategy: monitoring platform, logging approach, tracing, alerting, and dashboards. Follows the resolution cascade.

## Arguments

| Argument  | Required | Description                                                                          |
| --------- | -------- | ------------------------------------------------------------------------------------ |
| `$choice` | No       | Override: skip assessment, use this observability platform directly (e.g. `grafana`, `datadog`) |

## Composed Skills

| Skill              | Type       | Required                                              |
| ------------------ | ---------- | ----------------------------------------------------- |
| `/pair-capability-record-decision` | Capability | Yes — records observability decision as ADR or ADL    |

## Proposal Target

The rendered adoption content is destined for this section — the caller writes it via `/pair-capability-record-decision`:

- **Target**: [adoption/tech/infrastructure.md](../../../.pair/adoption/tech/infrastructure.md) — **observability section only**
- **Ownership**: Observability section (shared file — /pair-capability-assess-infrastructure owns core sections)

## Adoption File

- **Target**: [adoption/tech/infrastructure.md](../../../.pair/adoption/tech/infrastructure.md) — **observability section only**
- **Ownership**: Observability section (shared file — /pair-capability-assess-infrastructure owns core sections)

## Algorithm

### Step 1: Resolution Cascade

#### Path A — Argument Override

1. **Check**: Is `$choice` provided?
2. **Skip**: If not provided, go to Path B.
3. **Act**: Confirm the choice. Check for conflicts with existing adoption.
4. **Verify**: Developer confirms. Proceed to Step 3.

#### Path B — Adoption Exists

1. **Check**: Does [adoption/tech/infrastructure.md](../../../.pair/adoption/tech/infrastructure.md) exist and contain a populated **observability** section?
2. **Skip**: If no observability section or empty, go to Path C.
3. **Act**: Read current observability adoption. Confirm it's valid.
4. **Check**: Does a corresponding decision record exist?
5. **Act**: If decision record missing, compose `/pair-capability-record-decision` to backfill.
6. **Verify**: Done — exit skill.

#### Path C — Full Assessment

1. **Act**: Proceed to Step 2.

### Step 2: Read Guidelines

1. **Act**: Read observability guidelines:
   - [Observability README](../../../.pair/knowledge/guidelines/observability/README.md) — tool comparison, decision matrix, decision tree
   - [Observability Principles](../../../.pair/knowledge/guidelines/observability/observability-principles/README.md) — three pillars, proactive monitoring
   - [Observability Tools](../../../.pair/knowledge/guidelines/observability/observability-tools.md) — platform options
   - [Structured Logging](../../../.pair/knowledge/guidelines/observability/structured-logging/README.md) — logging standards
   - [Metrics](../../../.pair/knowledge/guidelines/observability/metrics/README.md) — metrics strategy
   - [Alerting](../../../.pair/knowledge/guidelines/observability/alerting/README.md) — alerting strategy
2. **Act**: Read project context:
   - [adoption/product/PRD.md](../../../.pair/adoption/product/PRD.md) — scale, budget
   - [adoption/tech/infrastructure.md](../../../.pair/adoption/tech/infrastructure.md) — existing infrastructure choices (observability must integrate)
3. **Verify**: Guidelines and context loaded.

### Step 3: Evaluate Options

1. **Act**: Use the Observability Platform Options table and Decision Tree from guidelines:
   - Evaluate: DataDog, New Relic, Grafana Stack, ELK Stack, Prometheus/Grafana
   - Consider: budget, scale, AI features needed, self-hosted vs managed

2. **Act**: Also evaluate:
   - **Logging approach**: structured JSON, log levels, sensitive data handling
   - **Tracing**: distributed tracing needs based on architecture
   - **Alerting**: notification channels, escalation

3. **Act**: Present recommendation:

   > **Observability Recommendation:**
   > - Platform: [name] — [rationale]
   > - Logging: [approach] — [rationale]
   > - Tracing: [approach or "not needed"] — [rationale]
   > - Alerting: [strategy] — [rationale]

4. **Verify**: Developer approves.

### Step 4: Write Adoption File

1. **Act**: Write or update **only the observability section** of [infrastructure.md](../../../.pair/adoption/tech/infrastructure.md):
   - Platform, logging, tracing, alerting decisions
   - Preserve all other sections (owned by /pair-capability-assess-infrastructure)
2. **Act**: If infrastructure.md doesn't exist, create it with observability section. Warn: "Created infrastructure.md — core sections should be populated by /pair-capability-assess-infrastructure."
3. **Verify**: Observability section written. Other sections preserved.

### Step 5: Record Decision

1. **Act**: Compose `/pair-capability-record-decision`:
   - `$type`: `non-architectural` (observability tooling is typically a tool choice)
   - `$topic`: `observability-strategy`
   - `$summary`: "[Platform] adopted for observability with [logging approach]"
2. **Verify**: ADL created. Adoption consistent.

## Output Format

```text
ASSESSMENT COMPLETE:
├── Domain:    Observability
├── Path:      [Argument Override | Adoption Exists | Full Assessment]
├── Decision:  [platform + logging + tracing + alerting]
├── Adoption:  [infrastructure.md observability section — written | confirmed | updated]
├── Record:    [ADL path — created | exists | backfilled]
└── Status:    [Complete | Confirmed existing]
```

## Composition Interface

When composed by `/pair-process-bootstrap`:

- **Input**: `/pair-process-bootstrap` invokes during Phase 2, after /pair-capability-assess-infrastructure.
- **Output**: Returns decision summary and adoption file path.

When invoked **independently**:

- Full interactive flow. Developer commits changes.

## Edge Cases

- **Project doesn't need observability** (e.g. CLI tool, library): Write minimal section noting "observability not applicable — [reason]".
- **infrastructure.md exists but no observability section**: Add section, preserve all other content.
- **Multiple valid platforms score equally**: Present top 2 with trade-off analysis.

## Graceful Degradation

- If observability guidelines not found, use minimal assessment: ask developer for platform preference.
- If `/pair-capability-record-decision` not installed, warn and skip recording.
- If infrastructure.md doesn't exist, create it with observability section only.

## Notes

- Observability decisions are typically **non-architectural** → produce ADL. Exception: if the observability choice requires infrastructure changes (e.g. service mesh for tracing), use ADR.
- **Section ownership**: this skill writes ONLY the observability section of infrastructure.md.
- Educational content (observability principles, three pillars, WHY) stays in guidelines.
