---
name: cx-proactive-support
description: Use to design and measure proactive outbound support that prevents inbound contacts without creating new ones. Trigger for "proactive support", "prevent tickets with outbound", outage notifications, shipment alerts, eligibility and suppression rules, measuring prevented contacts, or proactive messaging opt-out.
metadata:
  author: rulebase
  version: "1.0.0"
  archetype: playbook
---

# Proactive support

Proactive support is outbound contact **before** the customer asks — delay alerts,
known-issue warnings, renewal reminders, fix confirmations. Done badly it **creates**
inbound: the customer replies "yes I have that problem" and opens a ticket you would
never have received.

The design question is not "what can we send?" It is **"what contact would this
customer otherwise have made, and does this message remove that reason?"**

## Eligibility: who gets a proactive touch

| Criterion | Include | Exclude |
| --- | --- | --- |
| **Known state** | Verified delay, outage, failed payment | Speculative "you might have issues" |
| **Actionable info** | ETA, workaround, credit applied | Marketing dressed as care |
| **Identity confidence** | Account matched to event | Broad blast on weak match |
| **Channel fit** | Same channel they use for support | SMS if they never opted in |
| **Recency** | One message per incident window | Stacked reminders across channels |

**Eligibility is a filter, not a segment for volume.** Smaller, precise sends beat
"everyone who might care."

## Suppression rules

Suppress when any of these apply:

- Customer already has an **open ticket** on the same driver.
- **Proactive message sent** in the last N hours for same incident.
- Customer **opted out** of non-transactional channels.
- **Incident already acknowledged** via status page subscribe or in-app banner click.
- **Issue resolved** before send job runs — stale proactive is worse than none.

Maintain a **suppression log** keyed by `customer_id` + `incident_id` (or equivalent).

## Measuring prevented contacts vs created contacts

You cannot observe the counterfactual directly. Use a disciplined proxy set:

| Method | Measures | Weakness |
| --- | --- | --- |
| **Contact rate vs holdout** | Causal prevention | Needs ethical holdout on harmful events |
| **Pre/post same cohort** | Association | Confounded by seasonality |
| **Driver rate vs baseline** | Incident-level drop | Product fix confounds |
| **Reply-to-proactive rate** | Created contacts | Direct count of failure mode |
| **Time-to-contact after send** | Acceleration vs delay | Needs matched control |

**Created contact** definitions to track explicitly:

- Inbound within 24h replying to proactive thread.
- New ticket with tag "proactive reply" or subject prefix.
- Call within window after SMS/email with no prior open issue.

**Prevented contact** is credible only when:

- Driver is historically stable pre-incident.
- Proactive reached before typical contact peak.
- Holdout or matched control shows lower contact rate.

Report **net effect**:

```
net = estimated_prevented − confirmed_created
```

If created is material, tighten eligibility or message copy before scaling sends.

## Message design that prevents rather than provokes

| Do | Don't |
| --- | --- |
| State facts and next step | Ask " experiencing issues?" |
| Link status page or self-serve fix | "Reply HELP for support" on blast |
| Include opt-out where required | Hide unsubscribe on "service" mail |
| One primary CTA | Three buttons to different queues |

**Transactional exemption** does not cover "we thought you'd want to know" marketing.
When in doubt, treat as promotional for consent purposes and consult policy owners —
this skill does not provide legal advice.

## Opt-out and consent

| Channel | Minimum operational standard |
| --- | --- |
| Email | List-unsubscribe; honour within SLA |
| SMS | STOP handling; separate marketing vs transactional where required |
| Push | In-app preference centre |
| Phone | Do not robocall without documented consent |

**Separate flags** for: transactional (receipt, security), service proactive (outage,
delay), and marketing. Suppression must respect the strictest applicable preference.

## Operating model

1. **Trigger** — event from product, logistics, or incident system.
2. **Eligibility job** — filter + suppression.
3. **Template** — pre-approved, variant-tested for reply rate.
4. **Send + log** — `customer_id`, `incident_id`, channel, timestamp.
5. **Monitor** — reply rate, inbound spike, opt-out spike.
6. **Kill switch** — one owner can halt all proactive for an incident.

## Traps

**Proactive as marketing channel.** Unsubscribe rises; real service mail gets filtered.

**Multi-channel pile-on.** Email + push + SMS about the same delay triples created
contacts.

**Wrong personalization.** "Your order" to wrong account drives security contacts.

**Measuring sends as success.** Volume sent is not prevention; track net contact effect.

## Present results to the user

1. **Programme inventory** — triggers, channels, templates, volume per month.
2. **Eligibility and suppression spec** — written rules, gaps, and failure stories.
3. **Created contact rate** — replies and tickets attributed to proactive sends.
4. **Prevention evidence** — method used, holdout or baseline, confidence limits stated.
5. **Net assessment** — whether programme reduces or increases inbound on net.
6. **Changes recommended** — suppress rules, copy, channel, or kill criteria.
