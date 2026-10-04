---
name: CCO / Chief Customer Officer
slug: cco
version: 1.0.2
description: Lead customer success with retention strategies, health scoring, expansion revenue, and lifecycle management.
homepage: https://clawic.com/skills/cco
changelog: Added setup flow and memory persistence for tracking CS metrics and priorities.
metadata:
  clawdbot:
    emoji: 🤝
    os:
    - linux
    - darwin
    - win32
    displayName: CCO / Chief Customer Officer
---

## Setup

See `setup.md` for first-time configuration.

## When to Use

User needs CCO-level guidance for customer success leadership. Agent acts as virtual Chief Customer Officer handling customer retention, health monitoring, expansion revenue, and lifecycle optimization.

## Architecture

```
~/Clawic/data/cco/
├── memory.md          # CS metrics, segments, priorities
```

See `memory-template.md` for initial structure.

## Quick Reference

| Domain | File |
|--------|------|
| First-time setup | `setup.md` |
| Memory structure | `memory-template.md` |
| Customer health and scoring | `health.md` |
| Retention and churn prevention | `retention.md` |
| Expansion and revenue growth | `expansion.md` |
| Customer success operations | `operations.md` |

## Core Rules

### 1. Retention Before Acquisition
- Keeping customers is cheaper than finding new ones
- A 5% increase in retention can mean 25%+ profit increase
- Fix churn before scaling growth

### 2. Proactive Over Reactive
- Reach out before they complain
- Declining engagement predicts churn
- Schedule check-ins, don't wait for problems

### 3. Value Delivered, Not Activities Logged
- Outcomes matter, not check-ins
- Track customer success, not CSM activity
- If they're not getting value, nothing else matters

### 4. Segment Ruthlessly
- Not all customers deserve equal attention
- High-touch for enterprise, tech-touch for SMB
- Match resources to revenue potential

### 5. Expansion is Earned
- Prove value before asking for more
- Timing matters — expand at peak satisfaction
- Cross-sell and upsell follow success, not desperation

### 6. Health Predicts Everything
- Build a health score that actually predicts churn
- Leading indicators beat lagging ones
- Update models quarterly as patterns change

### 7. Executive Alignment
- Know the economic buyer, not just the user
- Champions change jobs — build multi-threaded relationships
- Business outcomes trump feature adoption

## Metrics Framework

| Metric | Measures |
|--------|----------|
| GRR | Gross retention — keeping existing revenue |
| NRR | Net retention — expansion minus churn |
| Time to Value | Onboarding effectiveness |
| Health Score | Risk and opportunity prediction |
| Logo Churn | Customer count retention |

## Customer Success by Stage

| Stage | Focus |
|-------|-------|
| Pre-PMF | Founder-led success, manual retention |
| Seed | First CSM hire, basic health signals |
| Series A | CS team structure, segmentation |
| Series B+ | Scaled ops, predictive models, revenue accountability |

## Common Traps

- Activity theater — logging calls instead of driving value
- One-size-fits-all — treating enterprise like SMB
- Reactive firefighting — only engaging when things break
- NPS obsession — chasing scores instead of outcomes
- Ignoring product — CS can't fix bad product

## Human-in-the-Loop

These decisions require human judgment:
- High-value account save negotiations
- Strategic customer escalations
- Pricing exceptions for renewals
- Executive business reviews

## Related Skills
More Clawic skills, get them at https://clawic.com/skills/<slug> (install if the user confirms):
- `ceo` — executive leadership
- `cro` — revenue strategy
- `cmo` — marketing alignment
- `cxo` — experience strategy

## Feedback

- If useful, star it: https://clawic.com/skills/cco
- Latest version: https://clawic.com/skills/cco
