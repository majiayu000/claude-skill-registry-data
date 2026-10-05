---
name: cx-incident-comms
description: Use to run customer support communications during an outage or major incident — banners, macros, status page, volume planning, and postmortem inputs. Trigger for "incident comms playbook", "support during outage", status page and help centre banner, macro for widespread issue, staffing surge, or freeze non-incident work.
metadata:
  author: rulebase
  version: "1.0.0"
  archetype: playbook
---

# Incident communications for support

During an outage, support becomes **repeat explanation at scale**. Without a playbook,
every agent improvises, macros diverge, the status page says one thing and chat says
another, and backlog grows while leaders debate wording.

The job is **one source of truth**, frozen non-incident work, and a volume plan — not
heroics.

## Incident phases and support actions

| Phase | Support focus |
| --- | --- |
| **Detect** | Confirm customer impact; do not announce unverified fixes |
| **Respond** | Banner, status, macro live; surge staffing |
| **Stabilise** | Update every N minutes until clear; merge duplicate tickets |
| **Recover** | All-clear messaging; watch reopen spike |
| **Review** | Ticket sample + volume curve for postmortem |

## One source of truth

Assign a **single comms owner** (often incident commander delegate) who publishes:

- Customer-visible **impact statement** — what is broken, who is affected, what is not.
- **Workaround** — if any; "none yet" is valid.
- **Next update time** — even if "in 30 minutes."

Every customer-facing surface reads from that text:

| Surface | Purpose |
| --- | --- |
| **Status page** | Subscribers and power users |
| **Help centre banner** | Self-service and SEO landers |
| **In-app banner** | Active users |
| **Chat bot / IVR** | First line deflection |
| **Agent macro** | Human replies — same words |

**Drift detection:** If agents are editing macro text locally, comms is failing. Macro
should be centrally updated; agents pick variant by language only.

## Macros and replies

Macro structure (short):

1. We are aware of [issue affecting X].
2. Impact: [plain language].
3. Workaround: [step or none].
4. Updates: [status page URL].
5. No need to contact again for updates — optional but reduces volume.

**Do not** promise compensation in first macro unless policy pre-approved.

**Merge strategy:** Tag all related tickets; link to master incident ticket; close
duplicates with macro pointing to status page when policy allows.

## Volume plan

Estimate surge from:

- Historical similar incidents (contacts per hour vs baseline).
- User counts in affected region or feature flag.
- Whether login or payment is blocked — multipliers are steep.

| Lever | When |
| --- | --- |
| **Surge staffing** | Pull trainers, QA, back-office with macro training |
| **Extend hours** | Global incidents crossing time zones |
| **Disable non-critical queues** | Freeze callbacks on unrelated products |
| **Bot / IVR message** | Before humans; must match status text |
| **Proactive outbound** | Known account-level impact only; see suppression rules |

**Freeze non-incident work:** QA calibrations, coaching, KB projects, migrations —
anything that steals attention from the queue or changes agent behaviour mid-incident.

## What support should feed postmortem

Export for engineering and leadership — not narrative blame:

| Input | Source |
| --- | --- |
| Contact volume curve | Ticketing timestamps vs incident timeline |
| Top customer phrasings | Tags or sampled verbatims (redacted) |
| Macro version timeline | When customers were told what |
| Misinformation episodes | Agent replies diverging from status |
| Reopen / repeat rate | After all-clear |
| Drivers misclassified as incident | Noise masking real bugs |

**First customer report time** vs **internal detect time** is a critical gap metric
when ticket text is searchable.

## Traps

**Premature resolution macro.** All-clear before confirm spikes reopens and trust loss.

**Silent incidents.** Customers flood support while status says operational.

**Splitting by channel.** Chat told to email; email told to call.

**Continuing SLAs meant for normal ops.** Publish incident SLA: "we are prioritising
 widespread issue tickets."

**Individual refunds in macro** without policy — agents create irreversible promises.

## Present results to the user

1. **Active incident pack** — banner text, macro(s), bot/IVR line, status page link.
2. **RACI** — comms owner, support lead, macro publisher, staffing approver.
3. **Volume plan** — expected surge, staffing actions, freeze list.
4. **Update cadence** — next customer update time and channel checklist.
5. **Duplicate / merge rules** — how agents handle repeat reports.
6. **Postmortem data pull spec** — what to export when incident closes.
