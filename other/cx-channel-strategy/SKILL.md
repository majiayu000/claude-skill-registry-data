---
name: cx-channel-strategy
description: Use to decide which support channels to offer, add, or retire, and to audit channel mix against accessibility obligations and cost to serve. Trigger for "should we add chat", "which channels should we offer", channel strategy, cost to serve by channel, accessibility requirements for support, opening a new contact route, or retiring phone or email.
metadata:
  author: rulebase
  version: "1.0.0"
  archetype: playbook
---

# Channel strategy

The usual failure mode is **adding channels because customers ask for them**, without
a migration plan, a cost model, or a reason the existing channels failed. You end up
with five ways to reach support, the same backlog, and higher cost — because each new
channel is staffed, instrumented, and trained separately while demand never moved.

Channel strategy is not "be everywhere." It is **matching contact routes to customer
need, accessibility obligation, and what you can afford to run well.**

## Start with demand, not preference surveys

| Question | Why it matters |
| --- | --- |
| Where do contacts actually arrive today? | Volume and driver mix by channel |
| Where do customers go when channel A fails? | Leakage, not deflection |
| Which drivers are channel-specific vs universal? | Phone for complex; chat for quick |
| What is cost per contact by channel? | Async is cheap; voice is not |
| Who cannot use your current channels? | Accessibility gap, not "nice to have" |

A "customers want WhatsApp" survey without **why they want it** often means chat wait
times are bad or the help centre failed — not that WhatsApp is the right fix.

## Cost to serve by channel

Use **marginal** cost per contact — variable agent time and vendor per-contact fees —
not fully loaded cost that includes fixed overhead. Savings are realised only when
capacity or headcount changes.

| Channel | Typical cost driver | What "cheap" hides |
| --- | --- | --- |
| **Self-service / KB** | Content maintenance, search tooling | Contact-after-view failures |
| **Async (email, messaging)** | Handle time × concurrency | Slow resolution, repeat contacts |
| **Live chat** | Concurrent sessions + SLA pressure | Leakage to voice when queues spike |
| **Voice** | Agent time + telephony + occupancy | Highest cost; often legally required |
| **Social / DM** | Brand risk + manual triage | Public escalation, no identity |

**Rule:** If you cannot staff a channel to your SLA without stealing from another,
you do not have a channel — you have a queue that teaches customers to switch.

## Accessibility and reachability obligations

This is not legal advice. It is an operations checklist for **whether support is
actually reachable** by people with access needs.

| Need | Channel implications |
| --- | --- |
| Vision | Screen-reader-compatible help centre; no image-only instructions |
| Hearing | Text/chat/email; relay services for voice if offered |
| Speech | Text alternatives; do not force voice for identity |
| Motor | No drag-only widgets; keyboard-navigable contact forms |
| Cognitive | Plain language, predictable paths, callback instead of hold |
| Language | Human or quality MT in primary contact languages |

**Voice-only dead ends** — "call us to reset your password" — fail multiple needs at
once. If you offer voice, you still need an async path for people who cannot use it.

Hours matter as much as channels. **24/7 chat with 9–5 agents** is a channel on paper
and a bot-or-nothing experience in practice.

## When to add a channel

Add only when all of these are true:

1. **Documented failure** of existing routes for a specific driver segment — not
   anecdote.
2. **Migration plan** — how volume moves, what gets de-emphasised, timeline.
3. **Staffing and SLA model** — headcount or vendor line item, not "the team will
   absorb it."
4. **Instrumentation** — same customer identity across channels so leakage is visible.
5. **Content parity** — macros, KB, and bot flows updated before launch, not after.

## When NOT to open a channel

| Situation | Why not |
| --- | --- |
| Existing channel under-served | Fixes queue; adding routes splits demand |
| "Competitors have it" | Their cost base and customer mix differ |
| Bot containment looks low | Leakage may be to another channel you already pay for |
| No identity resolution | You cannot measure cross-channel repeats |
| BPO contract minimums | New volume may not reduce spend |
| Launch without suppression rules | Outbound + inbound on same issue doubles contacts |

**Retiring a channel** is valid when volume is low, cost is high, and an accessible
alternative exists — with a communicated migration period, not a overnight redirect.

## Channel-role matrix

Assign each channel a **primary job**. Overlap is expensive; gaps are worse.

| Role | Best fit | Poor fit |
| --- | --- | --- |
| Deflect simple, high-volume | KB, bot, async templates | Voice |
| Complex troubleshooting | Voice, screen-share, callback | Twitter DM |
| Account-sensitive | Authenticated chat/email | Public social |
| Status / incident | Status page, banner, macro | Individual ticket replies |
| Sales-adjacent | Chat with routing rules | General support inbox |

One channel should own **proactive outbound** for a given trigger; otherwise
customers get email and push and SMS about the same shipment.

## Traps

**Channel switching as success.** Chat "containment" rises while phone volume rises.
Measure **total contacts per customer per issue**, not per-channel metrics.

**Async as infinite buffer.** Email without a backlog cap becomes a warehouse of
delayed dissatisfaction. Worse CSAT than chat with a honest wait time.

**Social as support inbox.** Public channels attract performative escalation. Route
to private channels fast or pay twice — public reply plus ticket.

**Free tier chat widgets.** Unstaffed chat trains customers that support is
unavailable; they phone angry.

## Present results to the user

1. **Current channel mix** — volume, top drivers, and cost per contact by channel
   (with cost basis stated).
2. **Leakage map** — where customers go when a channel fails; quantify cross-channel
   repeats on the same issue.
3. **Accessibility gaps** — who cannot complete support journeys today; name the
   barrier (CAPTCHA, voice-only, hours, language).
4. **Recommendation** — add, fix, merge, or retire; each tied to a driver segment
   and a staffing or content dependency.
5. **What not to do** — channels or launches that would increase cost without
   migration, called out explicitly.
6. **Measurement plan** — identity resolution, SLA by channel, and total-contact
   metric alongside channel KPIs.
