---
name: team-collaboration
description: "Ownership models are usually inherited rather than chosen, and the inherited one"
---

# Team Collaboration (Verbose)

## Core Patterns

### Code Ownership: Choosing the Trade-off

Ownership models are usually inherited rather than chosen, and the inherited one
is usually strong ownership because it emerges naturally — whoever wrote it
reviews it. That default has a specific, measurable cost.

| Dimension | Strong ownership | Collective ownership |
|---|---|---|
| Defect rate in-area | Lower; owner knows the traps | Higher until tests mature |
| Bus factor | 1 | Team size |
| Cross-cutting change | Serialized across N owner queues | Anyone can land it |
| Review latency | Owner's calendar is the ceiling | Any qualified reviewer |
| Onboarding | Slow — newcomers cannot touch anything | Fast |
| Architectural coherence | High within an area, poor across | Requires explicit stewardship |

Strong ownership optimizes for the quality of each individual change. Collective
ownership optimizes for throughput and resilience. Neither is correct in the
abstract; the deciding question is whether your dominant pain is defects or
delay. Most teams over-index on defects because defects are visible and delay
is not.

**The practical middle: collective ownership with named stewards.**

- Anyone may change any file. There is no permission to seek.
- Each area has a named steward who is a required reviewer for changes there.
- The steward's job is trap knowledge, not gatekeeping. "This table is
  replicated to the warehouse, your column rename will break the ETL" is the
  value they add. Style preferences are not.
- **The 24-hour rule:** if the steward has not responded within one business
  day, any two other engineers may approve and merge. Without this escape
  hatch, stewardship silently becomes strong ownership again the first time
  someone takes a vacation.
- Stewardship rotates — roughly every two quarters — which is the only reliable
  way to spread trap knowledge before it becomes an emergency.

Record stewards in `CODEOWNERS` so it is enforced rather than remembered.

### Pairing and Mobbing: The Economics

Pairing costs two engineer-hours per elapsed hour. Treat it as an investment
with specific conditions for return, not as a cultural value.

**Where pairing reliably pays:**

- **Novel design work.** When the shape of the solution is genuinely unknown,
  two mental models explore more of the space than one, and the discussion
  surfaces assumptions that would otherwise show up in review a week later.
- **Onboarding.** A new engineer's first change in an unfamiliar area. The
  transfer of context is the product; the code is a byproduct.
- **Incidents.** A second person prevents the classic incident-response failure
  where a stressed engineer runs a destructive command. One drives, one reads
  the runbook and keeps the timeline.
- **Stuck debugging.** After roughly 3 hours of one person failing to make
  progress, a fresh model is worth more than another hour of the same one.
- **Knowledge that exactly one person holds.** Pair deliberately to destroy the
  single point of failure.

**Where it does not:**

- Routine CRUD, well-understood bug fixes, mechanical refactors.
- Work where one person already knows the answer — that is a tutorial with
  extra steps, and should be a 10-minute explanation plus solo work.
- Long sessions. Effectiveness falls off after about 2 hours; a full day of
  pairing produces roughly half a day of good work and two tired engineers.

**Mobbing (3+ people)** is expensive enough that it earns its keep in exactly
one situation: a decision that everyone must subsequently live with, made once,
with everyone present. Architecture selection, a codebase-wide convention, an
incident postmortem, or a first walkthrough of a system nobody understands.
Mobbing to write ordinary code is a way to turn four salaries into one output.

### Onboarding: A Real First Week

The purpose of week one is not knowledge transfer — that takes months. It is to
establish that the new engineer can independently move a change from their
laptop to production. Everything else follows from that.

```
Day 1 — Merge something.
  Access, laptop, repo cloned, and one merged PR before end of day.
  A typo in a README counts. The point is exercising the entire
  pipeline: clone → branch → change → CI → review → merge → deploy.
  If this takes more than a day, you have found your first bug, and
  it is in your onboarding, not in them.

Day 2 — One system, deeply, out loud.
  With the steward, trace one real endpoint end to end: HTTP entry,
  auth, service, database, response. The new engineer draws the
  diagram; the steward corrects it. Reversing this — steward draws,
  newcomer watches — produces nodding and no retention.

Day 3 — A real ticket, pre-selected.
  Chosen before they started. Small, genuinely useful, touching two
  or three files in the area they toured on day 2. Not a fake task;
  people can tell, and it signals you don't trust them yet.

Day 4 — Ship it.
  Pair on the review, not on writing the code. Let them struggle a
  little alone first — that struggle is where the codebase's shape
  actually gets learned.

Day 5 — Reverse retro.
  What was confusing? What did the docs get wrong? Fix the docs in
  that session. This person is the only one who will ever see your
  onboarding with fresh eyes, and the window closes in about two
  weeks.
```

Assign **one named buddy** for the first month, with an explicit expectation
that interrupting them is correct behavior. "Ask anyone if you get stuck"
reliably produces asking no one, because a newcomer with no relationships cannot
judge whose time is interruptible.

### Handoff Hygiene

A handoff transfers state, not status. "Mostly done" is a status; it is worth
nothing to the person picking it up, who must now reconstruct everything you
knew by reading a diff.

```
❌ "Handing off the billing migration to Marcus — it's mostly done,
    ping me if you have questions."
    (The author is then on leave for two weeks.)
```

```
✅ Billing migration handoff → Marcus

   Branch:  pro-455-billing-migration (3 commits, CI green as of Oct 22)
   Ticket:  PRO-455

   Done:
     - Schema migration for billing_accounts
     - Backfill script, dry-run verified against a staging snapshot
       (1.2M rows, 4m 30s)

   Next step:
     Enable the read path behind the `billing_v2` flag, starting at 5%.
     The flag exists and defaults off; wiring is in
     services/billing/reader.py:88.

   Blocked on:
     Finance approval for a 15-minute write freeze. Asked Dana on
     Oct 21, no response yet — chase before Thursday or the cutover
     slips a week.

   Traps:
     - The backfill is NOT idempotent. Re-running double-counts
       credits. Make it idempotent before any production run.
     - staging billing data is 6 months stale; do not use it to
       validate amounts, only shapes.

   Decisions already made:
     Per-account batching rather than a single global transaction —
     the global version held locks for ~40s. Written up in PRO-455.

   Open question I did not resolve:
     Whether refunds issued during the freeze window need replaying.
     I lean yes. Ask Priya.
```

The traps section is the entire reason handoffs exist. Everything else is
recoverable from the branch and the ticket with an hour of reading; the traps
are recoverable only by causing the incident.

The same structure applies to end-of-day handoffs across time zones, at
one-tenth the length.

### Working Across Time Zones

The cost of distributed work is not the time-zone spread itself — it is the
number of sequential handoffs on the critical path. Each handoff across a
non-overlapping boundary costs approximately one full day of latency.

A task requiring four question-answer round trips between engineers with no
overlap takes four days regardless of how many hours of work it contains. The
mitigation is structural, not behavioral:

- **Split by vertical slice, not by layer.** Each zone owns something it can
  finish end to end without asking. See `problem-decomposition` for finding
  those seams — the seam-finding discipline is what makes distributed work
  tractable.
- **Protect the overlap window.** With 3 hours of overlap, spend it on the
  things that genuinely require conversation — design disagreements, incident
  response, pairing — and nothing that could have been a document.
- **Write questions to be answerable without you.** Not "should I use approach
  A or B?" but "I'm going with A because of X; if that's wrong, here's what I'd
  need to know. Proceeding unless I hear otherwise by your morning." This
  converts a blocking round trip into a non-blocking notification.
- **Default to written and durable.** Decisions in a call exclude everyone
  asleep. See `technical-communication` for the decision-record format.
- **Rotate meeting pain.** If a recurring meeting is at 07:00 for one region
  and 15:00 for another, alternate it. A standing meeting that is always
  painful for the same people is a slow attrition mechanism.

### Disagreeing in Writing Without Stalling

Written disagreement has a specific failure mode: it can continue indefinitely,
because each party can always write one more paragraph, and nothing forces
resolution. Teams then either stall for weeks or avoid disagreement entirely.

**The two-round rule.** State your objection once, completely: what you think is
wrong, what it will cost, and how confident you are. Let the other party
respond. If a second exchange does not converge, stop writing and pick one:

1. **Disagree and commit**, explicitly and in writing. "I still prefer the
   queue-based approach, but I'm not confident enough to block. Going with
   yours. I'd want to revisit if throughput exceeds 3k msg/s." This is not
   surrender — recording the dissent and its trigger condition is what makes it
   useful later.
2. **Escalate to 15 minutes synchronous.** Two failed written rounds is strong
   evidence that the medium is the problem. Post the outcome afterward.
3. **Escalate to a decider** — a tech lead or steward — with both positions
   stated fairly. If you cannot state the other position in a way its holder
   would accept, you have not understood it yet and are not ready to escalate.

Calibrate your objection's strength explicitly, because tone in text is
unreliable:

```
"Strong objection, would block: this loses writes on network partition."
"Moderate: I think this will be painful in 6 months, but I could be wrong."
"Weak preference, ignore freely: I'd have named it differently."
```

Without calibration, a mild preference reads as a veto, and a serious concern
gets waved through as a style note.

### RFC Processes That Terminate

An RFC process exists to surface objections before implementation and to leave a
record of why. Most RFC processes fail by never ending.

What makes one work:

- **A decision deadline on the document itself.** "Comments by Thu Nov 6;
  I start Fri with whatever we have." Open-ended RFCs collect comments
  indefinitely and decide nothing.
- **A named decider**, not a committee. Consensus is a preference, not a
  requirement. The decider's job is to make the call after hearing objections,
  and to say why.
- **A size threshold.** Not everything needs an RFC. A reasonable bar: anything
  that changes a public interface, adds a runtime dependency, or costs more
  than two weeks. Below that, just build it — RFC-ing small things trains
  people to ignore RFCs.
- **A visible outcome section**, appended when the decision is made: what was
  chosen, what was rejected and why, and what would trigger revisiting.
- **An accessible archive.** An RFC nobody can find has not documented
  anything. The most common reader is someone six months later asking "why is
  it like this?"

If your RFCs routinely sit open for three weeks, the problem is almost always a
missing deadline, a missing decider, or both.

## Common Anti-Patterns

❌ **De facto strong ownership** — one person is the only reviewer for a
directory, and their vacation blocks four teams.
✅ Collective ownership with named, rotating stewards plus a 24-hour escape
hatch to two alternate approvers.

❌ **"Ask anyone if you get stuck"** — a newcomer with no relationships asks
nobody and loses two days to something answerable in five minutes.
✅ One named buddy for the first month, with explicit permission to interrupt.

❌ **Onboarding as reading** — two weeks of documentation and architecture
decks before touching the repo.
✅ A merged PR on day one, however trivial. Real ticket by day three.

❌ **Pairing by policy** — a mandate that all work is paired, regardless of
whether the work is novel.
✅ Pair on novel design, onboarding, incidents, and stuck debugging. Solo the
routine work.

❌ **Mobbing to write ordinary code** — four people, one keyboard, one
engineer's worth of output.
✅ Mob only for decisions everyone must live with, then disperse.

❌ **Handoffs that transfer status** — "mostly done, ping me" from someone
about to be unreachable.
✅ Branch, done, next step, blockers, traps, decisions made, open questions.

❌ **Sequential cross-zone dependencies** — four round trips means four days,
regardless of the work involved.
✅ Split so each zone owns a vertical slice; write questions that can be
answered without a round trip.

❌ **Unbounded written disagreement** — six paragraphs each, three days, no
resolution, and eventually silence that everyone reads differently.
✅ Two rounds, then disagree-and-commit or 15 minutes synchronous.

❌ **Uncalibrated objections** — a naming preference phrased with the same
force as a data-loss concern.
✅ Label the strength: blocking, moderate, or weak preference.

❌ **RFCs with no deadline or decider** — open for three weeks, quietly
abandoned, implemented anyway.
✅ Named decider, comment deadline, appended outcome section with rejected
alternatives.

❌ **Standup as status reporting to a manager** — fifteen minutes of people
narrating yesterday to someone who is not blocked by any of it.
✅ Standup answers one question: who is blocked, and who can unblock them.
Everything else goes in writing.

## Collaboration Checklist

**Ownership**
- [ ] Stewards named in `CODEOWNERS`, with rotation on a stated cadence
- [ ] 24-hour escape hatch documented and actually used
- [ ] No directory has exactly one qualified reviewer

**Onboarding**
- [ ] New engineer merges a PR on day one
- [ ] Named buddy assigned for month one
- [ ] A real ticket pre-selected before their start date
- [ ] Reverse retro in week one, with doc fixes made in the session

**Handoffs**
- [ ] Branch name, CI state, and ticket link included
- [ ] Explicit next step, not a general description of the area
- [ ] Blockers named with who was asked and when
- [ ] Traps and non-obvious failure modes written down
- [ ] Decisions already made, with reasoning, recorded

**Distributed work**
- [ ] Each zone owns at least one vertical slice end to end
- [ ] Overlap window reserved for things that need conversation
- [ ] Questions written to be answerable without a round trip
- [ ] Recurring-meeting pain rotated between regions

**Disagreement and decisions**
- [ ] Objections labeled by strength
- [ ] Two-round rule applied before escalating or committing
- [ ] Disagree-and-commit recorded with its revisit trigger
- [ ] RFCs carry a named decider and a comment deadline
- [ ] RFC outcomes appended, including rejected alternatives
