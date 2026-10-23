---
name: handoff
description: "Use when a task spills over a session and the context has to reach a fresh session or agent: compact the state into a handover that references the artefacts by path or URL."
---

# handoff

Cross-cutting step, at the boundary between two sessions on the same task: complements
the one-task-per-worktree rule: the worktree stays open, but the context of the session
that's ending has to survive cleanly into the next one.

## When
As soon as a session is coming to an end (context limit, end of day, change of who picks it up)
without the task being finished: never as a replacement for a plain end-of-task summary on a
completed task.

## Steps

1. **Write a handover document** (a dedicated temporary file, not mixed into the code), addressed to the
   incoming agent, who has not seen this session. It holds:
   - **the goal**, as the end state wanted, not the sub-task in hand;
   - **where we are**: what works, what is broken, the exact symptom with the error text verbatim;
   - **what was decided and why**, and what's blocking if there is a blocker;
   - **what was tried and set aside, with the reason each one failed** (see step 1b);
   - **the current best hypothesis**, with the evidence behind it, even if unproven;
   - **the next steps**, ordered, specific enough to start on the first one: a path, a function, a command;
   - **constraints that are not obvious**: environment specifics, what the operator said not to do, external
     dependencies, performance limits;
   - **findings versus premises**: what was verified in this session, marked as such, and what was assumed and
     must be re-checked before it is relied on.
1b. **The discarded-attempts rubric is the part that earns the handover.** For each approach that did not work:
   what was tried, what happened, why it failed (the mechanism, not just "it failed"), and which hypothesis it
   leaves standing. A fresh agent that skips it repeats the attempt; one that reads it starts from the surviving
   hypothesis. An empty list is written as "nothing tried yet", never omitted.
2. **Reference, never duplicate**: point at the artefacts already written by their exact path/URL
   (plan, ADR, Jira ticket, commit, diff in progress) rather than copying their content into the
   handover document: a handoff that duplicates inflates the next session's context for nothing.
3. **Suggest the relevant skills** for what follows (e.g. "resume at `tdd`, the `plan` is already
   done and referenced here"): the next session knows where to restart without having to
   rediscover the state on its own.
4. The next session reads the handover document first, before any other exploration: it saves the
   re-contextualisation time.
5. **The reading side: reconcile before any work.** A handover, a state file or a notes document says what was true
   when it was written. Before building on it, check the live state against it with the cheapest real check: the
   revision the environment is serving, the branch and its recent commits, the working tree, the open ticket.
   Where they disagree, say so first ("the document says X, the live system returns Y"), treat the live state as
   authoritative, and settle or confirm the difference before doing anything else. Mark what you inferred
   against what was recorded. A session that ended without writing its handover (a crash, a forced quit) is the
   same case: rebuild from the commits and the live state, and say that you did.
6. **Update by targeted edits and report old to new.** When the document is stale, change only the fields that
   changed, never rewrite the file, and state each change as old value to new value. Write the fields the moment
   the fact is confirmed, rather than batching everything for the end, and skip the write entirely when a session
   changed nothing.

## Output / checkpoint
A handover document exists, cites every artefact by its exact path/URL (no duplicated content),
and explicitly names the next step/skill to resume at. The six reboot questions (`when-stuck` §5.10) can each be answered
from it without the incoming agent asking anyone.

## Guardrails
**Never hand over a premise as a finding.** What was observed in this session and what was inferred or assumed
are marked apart, because the incoming agent will treat anything unmarked as settled.

**Never trust a state document over the live system.** The document is a claim; the check in step 5 is the fact.

Never duplicate content already written elsewhere: the whole principle of this block is
referencing, not copying. A handoff that ends up longer than the artefacts it references has
missed its goal.

## Origin
Rewrite of the `handoff` skill from a recognised market skill author: the rule "never duplicate,
reference by path" is taken as-is, rewritten to the mentis template and explicitly linked to
the one-task-per-worktree rule already in place in house.

The discarded-attempts rubric, the current-hypothesis section and the addressed-to-the-incoming-agent rule come
from the `handoff` skill of `claude-mem` (Apache-2.0, read 2026-10-02); the findings-versus-premises split from
the working method of `slopless` (MIT, same date). Rewritten in our words, no text copied, so the NOTICE
obligations of the Apache licence do not apply.

The reboot-checkpoint line in the output section comes from the six-question reboot test of `planning-with-files` (MIT, read 2026-10-19); its provenance is in `skills/when-stuck/references/origin.md`.

The reading-side reconciliation (steps 5 and 6: verify live state first, flag the mismatch, targeted edits, old-to-new report) was added 2026-10-20 from the session-start and session-end agents of the operating-kit plugin of `wshobson/agents` (MIT, root licence; the plugin manifest declares MIT for its author). Rewritten in our words, no text copied; its templated placeholders, model settings and briefing layout are not carried over. Not run on a real session.
