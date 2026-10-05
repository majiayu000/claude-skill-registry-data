---
name: cx-journey-mapping
description: Use to map support contacts onto the product lifecycle, interpret contact as a lifecycle signal, and avoid journey-map theatre. Trigger for "customer journey map support", "contact by lifecycle stage", onboarding support drivers, churn and support overlap, stage-specific contact reasons, or when journey mapping is worth doing.
metadata:
  author: rulebase
  version: "1.0.0"
  archetype: playbook
---

# Journey mapping with support contacts

Journey maps often die as wall art: sticky notes, generic emotions, no data link.
**Support contacts are timestamped, labelled evidence of where the product journey
 broke** — if you attach driver taxonomy and customer lifecycle stage.

The prize is not a prettier map. It is **knowing which lifecycle stages generate
which contacts**, and whether product fixes would remove them.

## When journey mapping is worth doing

| Worth doing | Theatre |
| --- | --- |
| Driver volume by lifecycle stage | Emotions without metrics |
| Repeat contacts at same stage | Generic "awareness → advocacy" |
| Cross-functional owners per stage | Workshop output never updated |
| Links to product metrics (activation, churn) | Map all personas at once |
| Decision on roadmap or policy | "Align stakeholders" as sole outcome |

If you cannot assign **stage per contact** from data, fix instrumentation before
facilitating a workshop.

## Define lifecycle stages (operational)

Use stages your product and CRM already recognise — examples:

| Stage | Typical support signal |
| --- | --- |
| **Evaluate / trial** | Limits, billing confusion, feature questions |
| **Onboard / activate** | Setup failures, integration, first-value blockers |
| **Use / grow** | How-to, permissions, edge cases |
| **Renew / expand** | Contract, seats, downgrade |
| **Problem / incident** | Outage, data loss, bug |
| **Leave / win-back** | Cancel flow, export, retention offer confusion |

Stages must be **mutually exclusive rules** in data — e.g. trial flag, days since
activation, subscription status — not agent guess.

## Map contacts to stages

For each stage, aggregate over a defined window:

| Metric | Use |
| --- | --- |
| Contact rate | Contacts / active customers in stage |
| Top drivers | Taxonomy tags ranked |
| Effort signals | Repeats, reopens, channel switches |
| Time to first contact | Days from stage entry |
| CSAT / complaint rate | Response-adjusted |

**Contact as signal:**

- Spike at **onboard** → activation friction, not "support needs more staff."
- Spike at **renew** → pricing, entitlement, or comms gap.
- Flat **use** but high volume → documentation or product complexity.
- **Problem** stage persistent outside incidents → quality or expectation issue.

## Stage-specific drivers

Build a table — the core deliverable:

| Stage | Top 3 drivers | Contact rate | Product vs ops owner |
| --- | --- | --- | --- |
| Onboard | … | … | … |
| … | … | … | … |

**Product-owned** drivers: bug, confusing UX, missing in-app guidance.
**Ops-owned** drivers: policy unclear, macro gap, staffing on seasonal renewals.
**Shared:** billing architecture, identity edge cases.

If every driver is "ops-owned," the map is blaming support for product shape.

## Overlay emotional journey (lightly)

Emotion sticks are optional **after** quantitative map. One row per stage:

- Expected goal (customer job-to-be-done).
- Typical friction from verbatims sample.
- Support role (prevent, fix, explain, recover).

Do not invent emotions stakeholders "think" customers feel. Sample tickets.

## When maps become theatre

| Symptom | Fix |
| --- | --- |
| Map older than one quarter | Refresh or retire |
| No owner per stage outcome | Assign DRI |
| Drivers not from taxonomy | Align tagging first |
| "Moments of delight" without cost | Cut |
| Map ignores self-service and bot | Include all contact routes |
| Workshop attendees ≠ decision makers | Short data brief instead |

**Retire the map** when stage contact rates flatline after product fixes — celebrate
and archive.

## Connect to action

Each stage should exit with **at most three bets**:

1. Product change (if driver is UX/defect).
2. Content/self-service (if driver is informational).
3. Policy or process (if driver is rules).

If bets exceed headcount, prioritise by **contact volume × repeat rate**.

## Traps

**Average journey across segments.** Enterprise and self-serve differ; split maps.

**Single channel view.** Stage pain may appear in chat while phone is quiet.

**Confusing incident drivers with lifecycle.** Tag incidents separately.

**Map without baseline.** "Lots of onboarding contacts" needs rate, not count.

## Present results to the user

1. **Lifecycle stage definitions** — rules used in data.
2. **Contact rate and volume by stage** — table with time window stated.
3. **Top drivers per stage** — with product vs ops ownership.
4. **Effort or repeat hotspots** — stages where customers come back.
5. **Recommended bets** — ≤3 per stage, prioritised cross-stage.
6. **Theatre check** — what to stop doing if map cannot drive decisions.
