---
name: cx-after-hours-coverage
description: Use to design overnight and follow-the-sun support — coverage models, handoff quality and measuring what is lost between shifts. Trigger for "after-hours coverage", "follow the sun", overnight support design, night shift vs defer async, handoff packet, shift handover quality, global coverage gaps, or when customers reopen tickets after every handoff.
metadata:
  author: rulebase
  version: "1.0.0"
  archetype: playbook
---

# After-hours coverage

Customers do not stop needing help at 17:00. **The common failure is choosing a coverage
model for cost and treating handoffs as free.** Follow-the-sun, overnight shifts and
deferred async each trade money, quality and speed differently — but all three fail the
same way when the receiving shift inherits opaque tickets, missing context and wrong
expectations. Design coverage and handoff together.

## Choose the model deliberately

Three patterns, often combined by channel:

### Follow-the-sun

Regional or global teams pass work across time zones — APAC → EMEA → Americas. Works when:

- You have **qualified staff in each region** on the languages and products you serve.
- **Handoff windows are short** and the ticket state is machine-readable.
- Product and policy are **stable enough** that regional interpretation does not diverge.

Fails when: only one region has depth, handoffs land in local morning peaks, or macros and
policy differ by site without documentation.

### Dedicated night / overnight shift

Same geography, off-hours hours. Works when:

- **Real-time channels** (voice, chat) need sub-hour response overnight.
- Volume justifies a roster; part-time overnight blocks are hard to recruit but cheaper
  than 24/7 follow-the-sun complexity.
- You can **staff to measured overnight volume**, not guess from daytime ratios.

Fails when: overnight is staffed for "presence" with no demand, or night team lacks
escalation paths and ships everything to the day shift anyway.

### Deferred async

No live coverage; queue until next business day with explicit promise. Works when:

- Channel SLA allows it (email, many ticket types).
- **Expectations are set in product** — status page, auto-reply, portal messaging — not
  implied by daytime responsiveness.
- Backlog at open is **staffed as a surge**, not absorbed into normal capacity invisibly.

Fails when: customers use async like chat, or marketing runs sends into a closed queue
without surge planning.

| Factor | Follow-the-sun | Night shift | Deferred async |
| --- | --- | --- | --- |
| Real-time voice/chat | Possible with regional pools | Natural fit | Not suitable alone |
| Cost at low volume | High coordination cost | Fixed roster cost | Lowest |
| Handoff count | High — daily by design | Lower — one AM handoff | One open-the-queue spike |
| Language / product depth | Risk of shallow regional pools | Single-site depth | Day team only |
| Customer expectation | "Always someone" | "Someone overnight" | "We respond next day" |

**Hybrid is normal:** defer L1 async, staff overnight for P1 and enterprise, follow-the-sun
for a global product line. Document which channel uses which model.

## Handoff design

Handoffs are where coverage models lose quality. **A handoff is a manufacturing step**, not
a status change.

### Handoff packet — minimum contents

Every ticket crossing a shift or region boundary should carry:

| Field | Purpose |
| --- | --- |
| Customer goal in one sentence | Stops re-discovery |
| Actions taken and systems checked | Prevents duplicate work and customer re-telling |
| Open questions and blockers | Names what the receiver must resolve |
| Promises made to the customer | Prevents contradiction |
| Priority and SLA clock state | Receiver knows urgency |
| Sensitive flags — billing, legal, VIP | Routes attention before volume |

Free-text alone is insufficient; **structured fields** survive language and skill variance
better than narrative essays.

### Process rules

- **Handoff window** — last 30 minutes of shift is stabilise-and-document, not new
  complex work unless P1.
- **No "pending customer" without documented ask** — vague pending states die overnight.
- **Escalation ownership follows the clock** — name who is on call for product, billing
  and engineering overnight; "escalate to day" is not an overnight escalation path.
- **Language match** — do not hand Spanish tickets to a region with no Spanish coverage
  without explicit translation workflow.

### Measuring handoff loss

Handoff quality is measurable without guessing:

| Signal | Likely handoff failure |
| --- | --- |
| Re-open or new message within one interval of shift start | Receiver restarted work |
| Repeat customer narrative in next message | Context not captured |
| Handle time spike on inherited tickets vs self-started | Re-work cost |
| First-response SLA miss on queue-open only | Opening surge understaffed |
| Escalation rate jump on handoff tags | Wrong skill or missing blocker note |
| CSAT drop on tickets touched by 3+ agents across shifts | Coordination tax |

Compare **inherited vs self-started** tickets within the same queue and skill — difference
is handoff tax. Track by sending site and receiving site if follow-the-sun.

## Opening the queue

The first hour of the day is a **coverage event**, not normal operations:

- Staff **opening separately** from steady-state requirement if backlog aged overnight.
- **Triage rules** — what gets auto-reply, auto-close, merge — published before peak
  season.
- **Do not count overnight deferral as "within SLA"** if the clock never stopped; be
  explicit which SLAs pause and which do not.

## Traps

- **Follow-the-sun without regional parity** — three shallow teams instead of one deep one.
- **Night shift handling only easy tickets** — complexity lands at 09:00 anyway.
- **Handoff tags without packet fields** — "handed to APAC" is not information.
- **Measuring only response time, not re-work** — fast wrong answers cost more than slow
  right ones.
- **Changing coverage model by channel without telling customers** — expectation mismatch
  drives repeat contact.
- **Ignoring daylight-saving and holiday calendars** — handoff gaps appear twice a year
  on predictable dates.

## Present results to the user

1. **Coverage model by channel** — follow-the-sun, night, defer — with rationale and
   customer promise stated plainly.
2. **Roster implication** — where volume was measured; gaps if overnight is assumed not
   staffed.
3. **Handoff packet spec** — required fields and who completes them.
4. **Escalation and on-call map** for off-hours — named paths, not "day team."
5. **Handoff loss metrics** — which signals you will track and baseline if available.
6. **Opening-queue plan** — surge staffing or triage rules for backlog at day start.
7. **Risks and unverified assumptions** — regional skill depth, SLA clock rules, language
   coverage.
