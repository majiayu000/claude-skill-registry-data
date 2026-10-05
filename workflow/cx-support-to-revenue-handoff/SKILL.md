---
name: cx-support-to-revenue-handoff
description: Use to design the process that gets a revenue signal out of support and to the account owner without turning agents into sellers or degrading support quality. Trigger for "route upsell leads from support to sales", "support-sourced pipeline process", "should agents flag opportunities", designing a CS-to-sales handoff, or a handoff programme where agents have stopped flagging.
metadata:
  author: rulebase
  version: "1.0.0"
  archetype: playbook
---

# Handing a revenue signal from support to the account owner

Detecting expansion and churn signal in support is the easy half. Almost every
programme fails on the other half, and it fails in one of two directions:

- **The handoff decays.** Agents flag for a month, hear nothing back, and stop. The
  queue goes quiet and everyone concludes there was no signal.
- **The handoff succeeds too well.** Flagging becomes a soft sales target, agents start
  qualifying and pitching, and support quality drops in a way that shows up two
  quarters later as churn.

The design below is mostly about preventing the second while fixing the first.

## The one structural rule

**Agents flag. Agents do not sell.**

Everything else follows from this. The agent's job in the handoff is a single
low-friction observation — "this account mentioned adding a team" — and then back to
the ticket. Qualification, timing, pricing and the conversation itself belong to
whoever owns the account.

This is not squeamishness about selling. It is that the two jobs need opposite
postures. Support works by being unambiguously on the customer's side; the moment a
customer suspects the person fixing their problem is also assessing them as a
prospect, the candour that makes support work goes away — and that candour is what
generated the signal in the first place.

## Never do these

Each of these has a specific failure attached:

- **Pitch inside an unresolved conversation.** Resolve first, always. A commercial
  mention while the customer's problem is open reads as extortion.
- **Pay agents commission, or set flag quotas.** The instant flagging is rewarded,
  volume rises and precision collapses — and the queue becomes worthless within weeks.
  Recognition is fine; variable pay tied to flags is not.
- **Route a complaint to sales.** Hard-block it. An account with an open complaint or
  escalation is excluded until it is resolved and closed out.
- **Route a customer showing vulnerability or financial difficulty** into any
  commercial motion.
- **Let sales see the transcript by default.** Send the signal, the account, and the
  evidence id — not the customer's conversation. If the account owner needs context,
  they can ask, and the request itself creates a record of why.
- **Make the flag mandatory.** A required field produces noise; an optional one
  produces signal.

## Make flagging cost nothing

The flag has to be cheaper than not flagging, or it will not happen on a busy day.

- **One action, no form.** A tag, a single button, a keyboard shortcut. If it takes more
  than a few seconds it will be skipped exactly when the queue is busy, which is when
  the signals are.
- **No qualification required.** Do not ask the agent for budget, timeline, or
  likelihood. They do not know, and asking teaches them the flag is a sales task.
- **Available at close.** The natural moment is while wrapping up, not as a separate
  workflow.
- **One free-text line, optional.** "They mentioned a second office" is worth more than
  any dropdown taxonomy you will design.

## Close the loop, or it dies

This is the fix for the decay failure, and it is the single highest-leverage part of
the design.

**Every flag gets an outcome back to the agent who raised it.** Accepted, not pursued,
already known, converted — and ideally a sentence of why. Agents keep flagging when
they see it mattered and stop within about a month when they do not.

- **Put an SLA on triage.** A flag not looked at within a few days is stale, and the
  agent has concluded nothing happens. Days, not weeks.
- **Report conversions back to the support team**, by name where someone's flag closed
  something. This costs nothing and does more for flag rate than any process change.
- **Tell them about the misses too.** "Not pursued, they're on a fixed contract until
  March" teaches the pattern and improves precision without a training session.

## Ownership and routing

- **Route to a person, not a channel.** An unowned queue is where flags go to die.
- **Define the fallback** for accounts with no owner — self-serve, small accounts, a new
  region. These are frequently the majority of flags and they are usually where the
  process silently drops everything.
- **State what the owner is expected to do**, including the option of doing nothing.
  "Reviewed and not pursuing" is a valid, loop-closing outcome.
- **Set an expiry.** An unactioned flag older than a few weeks is closed as stale rather
  than sitting in a backlog that makes the queue look busier than it is.

## Measure the programme, including its cost

Four numbers, and the fourth is the one that gets forgotten:

1. **Flag rate**, per agent and per team. Watch for the two failure shapes: near-zero
   (loop not closed) and suspiciously high from one person (misunderstanding, or
   gaming).
2. **Acceptance rate** by the account owner. **The health metric.** Below roughly half
   and the queue will stop being read.
3. **Conversion** — qualified and closed, reported as *influenced* rather than
   attributed, unless you ran a holdout.
4. **The guardrail: support quality of accounts that got a commercial approach.**
   Satisfaction, complaint rate and repeat-contact rate against comparable accounts
   that did not. If this moves the wrong way, the programme is net negative regardless
   of pipeline, and you want to know that before someone else finds it.

Also watch **agent-side effects**: handle time, quality scores, and whether flagging
correlates with anything worse. If flaggers' quality drops, the flag is costing more
attention than it should.

## When to shut it down

Say this up front, because it makes the programme safer to start:

- Acceptance rate stays low after a precision fix.
- The guardrail metric degrades and does not recover.
- Flag rate collapses despite a working feedback loop — meaning the signal was thinner
  than assumed.
- It cannot be staffed. An unowned triage step is worse than no programme, because
  agents flag into a void and lose trust in the next thing you ask them to do.

## Present results to the user

1. **The structural rule and the never-do list**, first — this is what makes the design
   safe rather than merely functional.
2. **The flag mechanism**, and the evidence it takes seconds rather than minutes.
3. **The loop** — who returns outcomes, on what SLA, and how agents hear about
   conversions.
4. **Routing and ownership**, including the fallback for unowned accounts and the
   expiry rule.
5. **The four metrics**, with acceptance rate as the health check and the support-quality
   guardrail stated as a stopping condition.
6. **The shutdown criteria**, agreed before launch.
7. **What is excluded and why** — complaints, vulnerability, notice given, regulated
   topics, consent.
