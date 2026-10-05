---
name: cx-transfer-protocol
description: Use to define handoff standards for support transfers and to measure whether context survives the handoff — cold vs warm, required fields, and re-ask rate after transfer. Trigger for "transfer protocol", "warm handoff", "customers repeat themselves after transfer", "ping-pong between teams", "what should agents include when transferring", handoff quality, or re-ask rate after escalation.
metadata:
  author: rulebase
  version: "1.0.0"
  archetype: playbook
---

# Transfer protocol

A transfer is not a routing event. It is a continuity test: does the customer have to
start again?

Most operations treat transfer as "move the ticket to another queue" and measure
success by whether the ticket moved. The customer experience is measured by whether
they repeat their story — and that is almost never on the dashboard.

**The prize is context survival.** A good transfer feels seamless to the customer; a
bad one adds handle time to two agents, extends wall-clock wait, and is one of the
strongest predictors of repeat contact and complaint.

## Cold vs warm transfer

| Type | What happens | When it is appropriate | Customer experience |
| --- | --- | --- | --- |
| **Cold** | Contact moves; receiving agent picks up with whatever is on the record | Async channels; well-documented cases; specialist queues with full read access | Customer may need to re-state if the record is thin |
| **Warm** | Transferring agent stays on until receiving agent confirms context | Voice and chat; high-emotion cases; authority or compliance handoffs | Customer hears one handoff, not a restart |
| **Scheduled warm** | Callback or appointment with context pre-loaded | Back-office work required before resolution | Customer waits once, with a promise |

Default rule: **real-time channels default to warm; async defaults to cold with a
complete record.** Cold transfer on voice when the record is incomplete is why customers
say they explained it four times.

Warm transfer fails when:

- the receiving queue is saturated and nobody answers the warm handoff,
- the transferring agent drops before confirmation to protect their own AHT,
- or there is no shared view of the case (different tools, no linked record).

Fix capacity and tooling before mandating warm transfer on paper.

## Required context fields

Define a minimum handoff payload per transfer type. Generic "add a note" fails because
agents do not know what complete looks like.

**Universal minimum** — every transfer, every channel:

- Customer identifier and verified contact method
- Stated issue in the customer's words (not only the category label)
- Actions already taken and systems checked
- Commitments made to the customer (callbacks, refunds promised, timelines stated)
- Urgency and emotional state if elevated

**Add for authority / escalation transfers:**

- What the customer is asking for that the sender could not approve
- Policy or limit that blocked resolution
- Recommended disposition if known

**Add for technical transfers:**

- Environment, error messages, reproduction steps
- Logs or ticket IDs already opened upstream

**Add for async cold transfer:**

- Summary written so the receiver needs no clarifying reply to start work

Completeness is measurable: sample transfers and score against the checklist. A transfer
with only "see above" or an empty note is a failed handoff regardless of queue movement.

## Ping-pong: when transfer becomes failure

Ping-pong is three or more routing hops, or a return to a queue that already had the
contact. It is always a failure mode, not a normal escalation path.

Common causes:

- **No owning queue** for the contact type — each hop is guesswork
- **Acceptance criteria unclear** — receiving team bounces anything that is not
  perfectly packaged
- **Skill taxonomy mismatch** — sender and receiver disagree on whose job it is
- **Cold transfer with no context** — receiver cannot act and sends it back

Protocol response:

1. Define **acceptance criteria** per receiving queue — what must be present, what can
   be incomplete and filled in later.
2. Define **reject reasons** — finite list; "not our queue" must map to the correct
   destination, not back to sender.
3. **Cap hops** — after two failed routing attempts, route to a named resolver or
   supervisor queue, not round-robin again.

Measure ping-pong rate separately from designed escalation. Escalation is a path;
ping-pong is a broken one.

## Measuring re-ask rate after transfer

Re-ask rate is the share of transferred contacts where the customer restates information
they already provided earlier in the same case.

Why it matters: it is the customer-visible outcome of handoff quality, and it correlates
with longer total handle time and repeat contact even when first-contact resolution on
the final handler looks fine.

**How to measure:**

1. **Identify transfers** in the event log — queue change, assignee change, warm
   transfer flag, or explicit transfer disposition. Establish what the system actually
   records before counting.
2. **Define the observation window** — from transfer completion until case closure or
   next transfer. Re-ask after a second transfer is still a handoff failure.
3. **Detect re-ask** — options in order of quality:
   - Structured: receiver tagged "customer restated issue" or quality rubric item
   - Conversation: customer repeats facts (order number, dates, prior promises) already
     present in the thread before transfer
   - Proxy: receiver handle time spike on the opening segment, or immediate outbound
     message asking for information already supplied
4. **Hand-label a sample** and report detection accuracy. Automated keyword matching
   over-counts polite confirmations and under-counts implicit re-asks.

Report re-ask rate **by sending queue, receiving queue, channel, and transfer type
(cold/warm)**. A high rate on one path names a specific protocol or training gap, not
"a transfer problem" in general.

Pair with **time-to-first-action after transfer** — a receiver who re-reads for five
minutes before asking may still be recovering context even without a visible re-ask.

## Protocol as operating standard

Document and publish:

- When cold vs warm is required
- Minimum fields with examples of good and bad notes
- Acceptance and reject rules per queue
- What the customer should hear on voice/chat during warm transfer
- Escalation when warm handoff cannot complete (queue full, no answer)

Train to the checklist, not to "use your judgement". Judgement without a standard
produces variance that shows up as re-ask rate spread across teams.

Review monthly: re-ask rate trend, ping-pong rate, share of transfers with empty or
below-minimum notes, and warm-transfer completion rate on voice.

## Traps

- **Blaming the receiving agent for re-ask.** They are working with what arrived. Fix
  the sender protocol or the record.
- **Blaming the sending agent for ping-pong.** They usually routed correctly given
  broken taxonomy. Fix the queue design.
- **Mandatory warm transfer without receiver capacity.** Agents will go cold in practice
  and lie about it, or customers wait on hold until they abandon.
- **Transfer notes in a field the receiver never sees.** Check the receiver's UI, not
  the sender's.
- **Measuring transfers without separating designed escalation from misroute.** Mixing
  them hides which paths need protocol work.
- **AI-generated summaries as handoff without human verification on high-risk cases.**
  Summaries drop commitments and tone.

## Present results to the user

1. **How transfers are identified** in this data, and what is not recorded (warm vs
   cold, notes visibility).
2. **Current protocol gap** — documented standard exists or not; minimum fields defined
   or not.
3. **Re-ask rate** overall and by path (sender queue → receiver queue, channel, cold/warm).
4. **Note completeness score** on a labelled sample — share meeting minimum fields.
5. **Ping-pong rate**, separated from designed escalation, with example paths.
6. **Warm-transfer completion rate** on real-time channels, if applicable.
7. **Draft protocol** — cold/warm rules, required fields, acceptance criteria, and
   customer-facing script where relevant.
8. **Ranked fixes** — by re-ask rate and volume on each path; each fix names tooling,
   training, or queue design, not individuals.
