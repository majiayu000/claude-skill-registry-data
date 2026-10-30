---
name: verify-completion
description: Verify a completion, progress, or success claim against current direct evidence before it is made or accepted, especially after context compaction, resume, or a long task, and keep advice separate from compliance. Use when the user asks to verify or audit whether work is really complete, when a task resumes or continues after compaction with unfinished mutations, or when a completion claim rests on recalled or summarized facts. Classifies each fact as observed, recalled, or summarized, rebuilds a short evidence ledger for every completion criterion, re-derives the task state from files, commands, and records instead of summaries, and states advice and risks before complying when evidence conflicts with the request. Do not use for ordinary status questions, routine continuation of an unfinished task, reviewing an identified Axiom task's routing and authorization, or supervised multi-session progress.
---

# Verify Completion

Rebuild a completion, progress, or success claim from current direct evidence
before it is made or accepted. This skill gives direction and reasoning; the
host's model decides what to check, how deep, and what to recommend. It exists
because long tasks and repeated compaction let summaries stand in for
evidence, and a summary that says "done" is a claim, not a fact.

Defaults you may adapt, saying so: Direction step order where no gate depends on it, and ledger and report layout. Every other rule here and in the references this skill loads binds.

## Apply When

- The user asks to verify, audit, or double-check whether work is complete.
- A task resumes or continues after compaction, a fork, or a handoff while
  mutations are unfinished, before the next report or mutation.
- A completion claim about to be made rests on recalled or summarized facts.

## Do Not Apply When

- The user asks for an ordinary status update or routine continuation.
- The request is to review an identified Axiom task's routing, authorization,
  or evidence; that is `review-axiom-task`.
- The request is to supervise progress across sessions; that is
  `continuous-progress`.

## Fact Classes

- Observed: produced in this session by a file read, command, test, or service
  response that is still current after the last mutation.
- Recalled: remembered from earlier turns and not re-checked.
- Summarized: carried by a compaction summary, handoff note, plan, or task
  record.

Only observed facts support a completion claim. Recalled and summarized facts
are claims to re-verify. Observed facts expire when a later mutation touches
their subject; re-observe after mutating.

## Direction

1. Freeze the criteria. Restate the user's original request and acceptance
   criteria from the earliest available source: the task record, the first
   turns, or the user's own words. Never from the latest summary alone.
   Record the user's latest explicit decisions; they govern, and settled
   choices are not reopened.
2. Re-ground. For each criterion, name the direct check that would prove it
   now (file contents, command output, test result, remote state, record
   entry) and run it. Scale depth to risk: a mutated surface needs a fresh
   observation; an untouched one may keep an earlier observed fact with its
   timestamp.
3. Build the ledger. Follow `references/evidence-ledger.md`: one line per
   criterion with its check, observed result, verdict, and source.
4. Reconcile. Compare the ledger with the pending claim. Name every criterion
   the claim covered without an observed fact, and every observed result that
   contradicts the claim or the plan.
5. Advise before complying. Follow `references/advisory-stance.md`: when
   evidence conflicts with the request, the plan, or safety, state the
   conflict, its consequence, and a recommendation first; then act within the
   user's authority. An irreversible or unauthorized action stops instead.
6. Report. Give the ledger, the gaps, the remaining work, and the next action.
   Use `met`, `not met`, or `unverifiable` per criterion; never write "done"
   for an unverifiable criterion, and never present an unrun check as passed.

After compaction, a fork, or a handoff, follow
`references/regrounding-after-compaction.md` before step 2: treat the summary
as an index of what to check, re-read the recorded artifacts, and reselect
routes from current evidence before any new mutation.

## Boundaries

- Verification observes. It reads files, runs tests and read-only commands,
  and queries state within existing permissions. It does not fix, commit,
  push, deploy, or delete; a fix is a separate request with its own authority.
- Routing here grants nothing. Existing authorization keeps its scope; a
  verified gap does not authorize closing it.
- Never fabricate, infer, or backfill evidence. A check that cannot run is
  `NOT-RUN` with the reason, and the criterion stays `unverifiable`.
- Report in the user's language; keep ledger terms in English.

## Report

State the criteria source, the ledger, the fact class of every input the
claim relied on, each `NOT-RUN` check, the advice given and whether the user's
instruction was then followed, and the next action. Keep it short enough to
read before the next step.

## References

- `references/evidence-ledger.md`
- `references/regrounding-after-compaction.md`
- `references/advisory-stance.md`
