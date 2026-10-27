---
name: incident-commander
description: "Production incident response protocol, blameless post-mortem authoring, root-cause triage, and mitigation runbooks."
---

# Incident Commander & Production Triage Protocol

When investigating live service disruptions or responding to production outages, follow this structured incident lifecycle.

---

## 1. Triage & Stabilization Phase

1. **Assess Severity (P1-P4)**:
   - P1: Complete service outage or data loss affecting all users.
   - P2: Major feature failure without acceptable workaround.
   - P3: Minor degradation with available workaround.
2. **Mitigate First, Debug Later**:
   - Roll back to the previous stable release commit or toggle feature flags before attempting complex code surgery in production.

---

## 2. Blameless Post-Mortem Structure

Document all P1/P2 incidents in docs/incidents/YYYY-MM-DD-title.md:
- **Executive Summary**: Impact duration, affected users, and revenue/reputation blast radius.
- **Timeline**: Chronological sequence from trigger event, detection, triage, mitigation, to resolution.
- **Root Cause (5 Whys)**: Deep structural cause, not superficial operator error.
- **Action Items**: Preventative engineering tasks with assigned owners and due dates.
