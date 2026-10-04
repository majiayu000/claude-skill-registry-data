---
name: plan-enterprise
description: Complete 8-phase enterprise software planning cycle for mission-critical systems
version: 2.0.0
tags: [enterprise, planning, architecture, mission-critical, high-availability]
trigger_keywords: [enterprise, mission-critical, plan, architect, design, build, high-availability, acid, compliance]
requires_approval: true
estimated_duration: 60-120 minutes
---

# Skill: Plan Enterprise

## Purpose

Orchestrate the full METHOD-ENTERPRISE-BUILDER-PLANNING 8-phase cycle for enterprise-grade, mission-critical, and high-availability software systems.

## When to use

Activate this skill when the user requests:
- "Plan an enterprise system..."
- "Design a mission-critical [component]..."
- "Build a high-availability [module] with [SLA]..."
- "Architect a security-first [system] with [compliance]..."

Or when the user mentions regulated data (PCI-DSS, GDPR, HIPAA, SOC2, ISO 27001).

## Workflow

### Phase 1: Enterprise Context Analysis

**Actions:**
1. Classify system (enterprise-grade, mission-critical, high-availability, security-first, ACID-required)
2. Build stakeholder map (end users, compliance officer, operations, regulators)
3. Map regulatory environment (applicable standards with obligations)
4. List integration points (protocol, SLA dependency level)

**Output artifact:**
- Create `docs/enterprise-context.md` (use `createFile` operation)
- Artifact type: `implementation_plan`

**Gate:** Ask user to confirm system classification before proceeding.

---

### Phase 2: Non-Functional Requirements

**Actions:**
1. Define Performance SLOs: throughput (TPS), latency p95/p99
2. Define Availability SLA: % uptime, RTO, RPO, deploy strategy
3. Define Scalability: initial, peak, growth rate
4. Define Security baseline: auth, authz, encryption at rest/transit
5. Define Compliance per standard

**Gate:** All SLOs must be numeric and measurable (not "fast" or "secure" — "p95 ≤ 500ms", "99.9% SLA").

---

### Phase 3: Risk Matrix

**Actions:**
1. STRIDE analysis on primary API surface (Spoofing, Tampering, Repudiation, Info Disclosure, DoS, Elevation of Privilege)
2. Technical risk catalog (probability, impact, mitigation)
3. Flag any CRITICAL unmitigated risk — blocks Phase 4

**Output:** `docs/risk-matrix.md`

**Gate:** No CRITICAL risk may be unmitigated; all HIGH risks must have mitigations.

---

### Phase 4: Micro-task Decomposition

**Actions:**
1. Identify business domains
2. Map domains to layers (infrastructure → domain → application → interface)
3. Create one micro-task per file/unit, each ≤50 effective lines
4. Assign task IDs (DOMAIN-LAYER-NNN)
5. Define dependency order (topological sort)

**Validation per micro-task:**
After implementing each task, load `@skill lint-microtask` to validate effective line count.

**Output:** Backlog table in Phase 4 section

---

### Phase 5: Architecture Decisions (ADR)

**Actions:**
1. Apply architecture decision tree
2. Create one ADR per significant decision
3. Each ADR must have: Context, Decision, ≥2 Alternatives with rejection reasons, Consequences, Compliance Impact
4. Generate C4 diagrams (L1 System Context + L2 Container)

**Validation:**
After generating each ADR, load `@skill validate-adr` to check against 11 enterprise rules.

**Output:** `docs/adr/ADR-NNN-title.md` (one file per decision)

**Gate:** ADR cannot be marked Accepted if validation fails.

---

### Phase 6: Security & Compliance Mapping

**Actions:**
1. Define ACID transaction boundaries for all write operations
2. Map each compliance requirement to a concrete control
3. Define RBAC roles and ABAC ownership rules
4. Define audit event schema (what, where, retention)

---

### Phase 7: Test Strategy

**Actions:**
1. Define test pyramid allocation (Unit 70%, Integration 20%, E2E 7%, Chaos 3%)
2. List Critical User Journeys for E2E
3. Define load test scenarios (baseline, spike, soak) with numeric pass criteria
4. Define CI/CD quality gates

**Coverage requirement:** ≥99% line + branch (floor — assertions must verify behavior).

---

### Phase 8: Delivery Report

**Actions:**
Generate delivery report with:
- Micro-tasks completed/total
- Test results (unit/integration/E2E/load)
- Coverage % per layer
- STRIDE status
- Critical/High vulnerabilities: 0
- ADR status
- Compliance matrix
- STATUS: READY FOR PRODUCTION or BLOCKED

**Artifact type:** `delivery_report`

---

## Progressive skill loading

Do not load all phase skills at once. Load only the skill for the current phase:

```
Phase 1 in progress → load @skill phase-1-context
Phase 5 in progress → load @skill phase-5-adr
Validation needed   → load @skill validate-adr or @skill lint-microtask
```

This prevents context saturation while maintaining full capability.
