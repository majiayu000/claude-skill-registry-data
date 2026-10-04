---
name: ipl-customize
version: 1.0.0
description: Tailor the IP-LEGAL sub-plugin to one organization by capturing its risk tolerance, jurisdictions, and default playbook positions.
author: matrixx0070
tags: [customize, configuration, playbook, house-rules, risk-tolerance, policy, escalation]
capabilities: []
---

## When to use

Use this once per organization to set house rules so every other IP skill applies consistent positions instead of ad-hoc judgment. Capture risk tolerance, jurisdictions, industry, brand/product portfolio, standard positions, preferred counsel, and dockets, then store the profile for reuse.

**Not for:** intake or routing of a single new matter (`ipl-cold-start-interview`), organizing one matter's files and deadlines (`ipl-matter-workspace`), or running a specific analysis like clearance or OSS review (`ipl-clearance`, `ipl-oss-review`).

## Method

1. **Interview for the org profile.** Industry, jurisdictions of operation, risk tolerance (conservative/balanced/aggressive), brand and product portfolio.
2. **Define default playbook positions per domain.** Contractor IP-assignment default, acceptable OSS license tiers, C&D tone ladder, trademark clearance risk threshold, patent-vs-trade-secret default.
3. **Record escalation thresholds:** the conditions under which a matter MUST go to named counsel.
4. **Decision point:** for each position decide whether it is fixed policy (applied automatically) or case-by-case (flagged for human judgment). Fix only what is genuinely settled.
5. **ATTORNEY-ESCALATION GATE:** setting risk thresholds and approving any position that waives rights or accepts liability must be signed off by an attorney or GC. You capture and structure preferences — you do not set legal policy, and nothing here is legal advice.
6. **Store versioned.** Save as a reusable profile with an owner and a review date; re-review on a set cadence.

## Example

A B2B SaaS company, balanced risk, US + EU. Positions set: contractors sign IP-assignment by default (fixed); OSS permissive tier auto-approved, copyleft case-by-case (fixed); C&D starts at a soft "friendly notice" rung (fixed); trademark clearance escalates to counsel above a "moderate confusion" threshold (case-by-case). GC signs off on the thresholds. Profile v1.0, review in 12 months.

## Pitfalls

- **Fixing positions that should stay case-by-case.** Over-automation applies the wrong rule to an edge case.
- **No named counsel or owner.** A profile no one owns drifts stale and gets ignored.
- **Copying another org's tolerance.** Risk appetite is specific to industry and stage — capture it fresh.
- **Skipping GC sign-off on rights-waiving positions.** Any default that waives rights or accepts liability needs attorney approval.

## Output format

```
ORG IP PROFILE — <company> | v<n> | owner: <name> | review: <date>
Industry / jurisdictions / risk tolerance:
Trademark clearance risk threshold: <fixed|case-by-case>
Patent vs trade-secret default: <fixed|case-by-case>
Acceptable OSS license tiers: <permissive auto | copyleft ...>
C&D tone ladder: <rungs>
Contractor IP-assignment default:
Escalation thresholds (→ named counsel):
Preferred counsel / dockets:
Attorney/GC sign-off:
```

## Reference

Customizable levers per domain: trademark clearance risk thresholds (tie to likelihood-of-confusion factors); patent filing vs trade-secret defaults (tie to patentability bars, §§101/102/103/112); acceptable OSS license tiers, permissive vs copyleft obligations; and DMCA/takedown response SLAs (tie to §512 elements).

These levers feed the sibling skills — a profile set here is what `ipl-clearance`, `ipl-fto-triage`, `ipl-oss-review`, and `ipl-takedown` read as house rules. Keep the profile versioned and attorney-reviewed; nothing here is legal advice.
