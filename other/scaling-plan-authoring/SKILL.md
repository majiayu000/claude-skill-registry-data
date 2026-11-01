---
name: scaling-plan-authoring
description: Scaling & Capacity Plan Authoring — Authors threshold-gated scaling strategies, capacity baselines, bottleneck analysis, auto-scaling policies, and tiered infrastructure cost models.
---

# SKILL: Scaling & Capacity Plan Authoring
## Domain: Performance Engineering, Capacity Planning, SDD Station 15 / 18

**Activation triggers:** scaling plan, capacity planning, traffic growth, horizontal scaling, bottleneck analysis, cloud infrastructure costs, SDD Station 15.

---

## 1. Role & Threshold Law

The Scaling Plan Authoring skill evaluates and plans system behavior under extreme concurrency and data volume.  
It enforces the **Scale Threshold Law**:
- The Scaling Plan is **MANDATORY** whenever:
  1. Traffic targets exceed 500 RPS or 10,000 DAU.
  2. Growth expectations anticipate > 10x scale within 12 months.
  3. Multi-region or multi-AZ active-active failover is required.
  4. The PRD contains explicit horizontal auto-scaling non-functional requirements.
- For internal tools or targets below these thresholds, the document may record a formal threshold exemption.

---

## 2. Document Structure & Required Sections

Every generated Scaling Plan must follow `.factory/specifications/templates/10_scaling_plan.template.md` and contain:
- **Header Metadata:** Document ID, Version, Status, Parent PRD/Architecture IDs, Lead Performance Engineer, Date.
- **Section 1: Applicability Threshold & Scale Trigger:** Explicit justification of why the plan is required or exempt.
- **Section 2: Capacity Baseline & Growth Projections:**
  - Table showing Baseline (Current/MVP), Stage 1 (10x), and Stage 2 (Enterprise Scale/50x) across DAU, Peak RPS, Data Volume, and WebSocket connections.
- **Section 3: Bottleneck Analysis by Architectural Layer:**
  - In-depth risk, symptom, and mitigation analysis for:
    - Database & Persistence Tier (connection exhaustion, read replicas, partitioning).
    - Backend API & Compute Tier (CPU saturation, stateless containers, HPA).
    - Network & Ingestion Tier (bandwidth, CDN caching, rate limiting).
- **Section 4: Horizontal vs. Vertical Scaling Strategy:**
  - Matrix detailing scaling triggers and instance limits per container component.
- **Section 5: Load Testing Benchmarks:**
  - Concrete stress limits and degradation thresholds referenced from `09_testing_plan.md`.
- **Section 6: Infrastructure Cost Projections by Scale Tier:**
  - Monthly cloud spend estimates and cost drivers across Baseline, Growth, and Enterprise tiers.
- **Section 7: Signoff & Verification.**

---

## 3. Validation Checklist (Quality Gate G11 & G15 Pre-Condition)

- [ ] Clear threshold justification documented.
- [ ] Bottleneck mitigations defined for database, compute, and network.
- [ ] Auto-scaling triggers and container limits specified.
- [ ] Tiered cloud infrastructure costs estimated.
- [ ] Document saved to `.factory/specifications/<project>/10_scaling_plan.md`.
