---
name: phase-1-context
description: Phase 1 — Enterprise Context Analysis (standalone)
version: 2.0.0
tags: [enterprise, context, stakeholders, regulatory, phase-1]
trigger_keywords: [context, stakeholders, regulatory, classification]
requires_approval: false
estimated_duration: 10-15 minutes
---

# Skill: Phase 1 — Enterprise Context Analysis

## Purpose

Execute Phase 1 independently: classify the system, map stakeholders, identify regulatory obligations, and list integration points.

## When to use

- When starting a new enterprise planning session
- When the user only needs context analysis (not the full 8-phase cycle)
- As a prerequisite before jumping to Phase 3 or Phase 5

## Steps

### 1. System Classification

Ask or infer the classification across 5 dimensions:

| Dimension | Options |
|---|---|
| Grade | Enterprise-grade / Standard |
| Criticality | Mission-critical / Business-critical / Non-critical |
| Availability | HA (99.9%+) / Standard |
| Security | Security-first / Standard |
| Transactions | ACID-required / Eventually consistent / Stateless |

**Output:**
```markdown
## System Classification
- [x] Enterprise-grade
- [x] Mission-critical
- [x] High-availability (99.999%)
- [x] Security-first
- [x] ACID-required
```

### 2. Stakeholder Map

Identify who cares about this system and what their primary concern is:

| Stakeholder | Role | Key concern |
|---|---|---|
| [Name/role] | End user / Internal / Compliance / Operations / Regulator | [Specific concern] |

### 3. Regulatory Environment

Map applicable regulations to specific obligations:

| Regulation | Scope | Key obligation |
|---|---|---|
| GDPR | EU personal data | Art. 32: Encryption; Art. 17: Erasure |
| PCI-DSS | Payment card data | Req. 3: No raw PAN; Req. 10: Audit logging |

If no regulations apply, state explicitly: "No regulated data — standard security practices apply."

### 4. Integration Points

List external systems with protocol and SLA dependency level:

| System | Protocol | SLA dependency |
|---|---|---|
| [System name] | gRPC / REST / Event / SQL | Critical / High / Medium / Low |

**Dependency levels:**
- **Critical:** Transaction cannot complete without it
- **High:** Significant degradation if unavailable
- **Medium:** Graceful degradation possible
- **Low:** Fire-and-forget, async

## Output artifact

Save as `docs/enterprise-context.md`. Use Antigravity's `createFile` operation or `@terminal` to write.

## Gate

Present the classification to the user and ask: "Does this classification match your expectations? Confirm before I proceed to Phase 2."
