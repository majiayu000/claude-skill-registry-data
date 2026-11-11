---
name: wrap-it-up
description: >-
  End a long engineering session cleanly under token and attention pressure: freeze the in-flight set, delegate execution to subagents and judgement to an independent reviewer, and drive every item to one of three exits — merged, deferred with a record, or operator-blocked with a decision brief — then a clean baseline, a reconciled tracker, and a release-worthiness advisory. Use when the operator says "wrap it up", "clean baseline", "close out the session", "ready for the next iteration", or the context is filling. Not `get-it-done` (which grows the set); this closes a set frozen at invocation.
---

# Wrap it up

The iteration is ending. **Take what is already in flight, drive every item to a definite
exit, leave `main` a clean baseline, and tell the operator whether it is worth a tag.**

## Why you were invoked — read this before planning anything

This skill is a **session-economics** instruction as much as a delivery one. The operator
reaches for it when some combination of these is true, and they are the constraints you work
under from here:

- **The session is long and the context window is filling.** Every token spent re-reading a
  file you already summarised is a token not spent landing work.
- **They are not watching.** No question you ask will be answered in time. Bank decisions,
  never block on them, and never end a turn with "shall I".
- **They do not want to babysit an engineering session.** The value you deliver now is a
  clean trunk and a truthful tracker, not a demonstration of effort.

Three behaviours follow, and they are not optional:

1. **Delegate execution; keep orchestration.** Push implementation into subagents and worktrees
   so their file reads and failed attempts never enter this context. Read a subagent's **report**,
   never its transcript. Long-running commands go to the background and are polled, not watched.
2. **Delegate judgement to the council, not to more of your own thinking.** Audit, adversarial
   planning and PR review go to an independent fresh-context reviewer under the [Council contract](../pr-reviewer/references/independent-council.md), in the project's review
   order. One lane per question; a second lane only when the disagreement is worth paying for.
   You still re-derive the gate yourself — that never delegates.
3. **Spend the remaining budget on exits, not on polish.** An item that is 90% done and needs
   another design round is a **deferral with a record**, not a reason to keep going. Closing the
   session honestly beats landing one more thing badly.

## Focus is the point — the failure this skill exists to prevent

The operator's reason for reaching for this skill, in their words: sessions drift. The agent
starts on the ticket, then explores an adjacent area, an adjacent project, files nobody asked
about, and the scope it was given is still open hours later. **"Wrap it up" means: you already
have everything you need — the scope, the ticket, the definition of done, the tools. Work the
task in front of you until it is finished.**

So, for the duration of this skill:

- **The ticket's definition of done is the boundary.** If the work you are about to do is not
  named by it, you are not doing it. Curiosity about a neighbouring module is a ticket, not a
  detour.
- **Do not open adjacent files, projects or areas** to "check something related". If something
  adjacent looks broken, file it with evidence and carry on.
- **Cheaper is not the same as thinner.** Being pragmatic here means fewer items attempted, each
  finished properly — never the same items with the gate skipped. Every landed item is still
  tested, still proven by a regression you watched go red, still peer-reviewed by the council,
  still documented. **Scope is what flexes under time pressure; rigour is not.**

## The boundary — the one rule that makes this skill different

**The work set is frozen at invocation.** Whatever is in flight when the operator says "wrap
it up" is the whole job. Nothing new enters it. Every item leaves by exactly one of three
doors, and every item leaves by one of them before this skill is finished:

| Exit | Meaning |
|---|---|
| **merged** | proven, reviewed, on the trunk |
| **deferred** | not landing this iteration, with a reason code and the full deferral record below |
| **operator-blocked** | waiting on a judgement that is genuinely theirs, with a decision brief |

The commonest mistake is treating "deferred" as failure and pushing on. It is not. An item
carved out cleanly, with its evidence and its next action recorded, is a **completed exit** and
counts as much as a merge.

`get-it-done` is the opposite shape: it derives its work from a goal and **expects the set to
grow**, because pursuing a goal means discovering work. If you find yourself opening new scope
here, you have switched skills — say so out loud and switch deliberately, rather than sliding
between them. The check afterwards is mechanical: **did the work set grow? Then it was not a
wrap-up.**

New defects you discover while closing the set are **filed, not fixed** — a ticket with
evidence, sorted into the tracker. Filing is not growth; fixing is.

## 0. The in-flight snapshot — the operator reads this first

Derive it live (`git worktree list`, `git branch -r --no-merged origin/main`, `gh pr list`).
One row per unit, no prose. This table IS the frozen set.

| Branch / PR / Issue | Scope | Gate | Review | Exit |
|---|---|---|---|---|
| `feat/…` #NN | one line | green / red / — | PASS / CONCERNS / pending / — | merged / deferred / operator-blocked / landing now |

If nothing is in flight, say "baseline already clean, nothing in flight" and go to §4; the tag
advisory still runs. Backlog tickets that are not on a branch are **not** in flight — list them
separately as "open, not started" so they are never confused with work about to land.

## 1. Triage every item before landing anything

Three lanes. Decide the lane first; the lane decides the work.

### Lane A — mine, and I land it

Ordinary work: the gate is green or can be made green, the design is settled, and the decision
left is implied by work the operator already approved. Run the `get-it-done` loop unchanged —
branch, prove it bites, council review (the writer never approves its own work; a changed
candidate voids the review), merge commit, prune only what the read-only
[lane hygiene report](../../scripts/lane_hygiene.py) shows integrated,
reconcile. Its **"Theirs, always"** list and its **substitute-the-missing-gate, never route
around a guard** rules apply exactly. Do not restate that loop; invoke it.

### Lane B — mine, but the design is complex enough that a wrong call is expensive

This is the lane that keeps work moving instead of escalating it. The action is inside an
approved scope, so it is not the operator's decision — but the design is intricate, the blast
radius is wide, or you are the author and therefore the worst judge of it. **Trigger the AI
council** (an independent fresh-context reviewer under the [Council contract](../pr-reviewer/references/independent-council.md)) at up to three points:

- **Audit** the existing design or defect before you touch it.
- **Plan** the approach, adversarially, before building.
- **Review** the outcome, as a PR review bound to the exact diff.

Disagreement between models is the signal worth paying for; agreement is not proof. Record
which lane answered, its verdict, and what it found — a council pass you cannot cite did not
happen.

**The two-strike rule — mechanical, not a judgement call.** Count review rounds per item. If a
second round blocks on **the same shape of defect** as the first, the item stops being an
implementation task at that moment. Do not send a third patch. Instead:

1. **Hand it to the delivery owner** (`delivery-orchestrator`) to
   re-classify it as needing a **planning and objective-reasoning phase**, not another fix.
2. **Comment on the ticket** with both review verdicts, the shape they share, and the invariant
   the next attempt must satisfy — a design brief, not a bug report.
3. **Place it in `ROADMAP.md`** in the deferred priority queue, with its phase and priority, and
   reference it from the status file with the ticket number.
4. **Leave the branch on the remote**, named in the ticket, so the next attempt starts from the
   evidence rather than from scratch.

Two rounds is the budget because the second failure is the information: one failure is a bug,
the same failure twice is the design telling you it was never a patch.

### Lane C — it defers, for one of three named reasons

Every deferral states which of these it is. An unlabelled deferral is a dropped item.

**C1 — the design loop.** Two review rounds blocked on the same shape of defect, per the
two-strike rule above. It returns as a planning task, not a fix.

**C2 — it needs a dedicated session.** This is the reason the operator most wants observed. An
item belongs in its own session, not in a wrap-up, when **any** of these is true:

- it is a **large epic or a large scope** that has not been broken down yet;
- it needs **several critical decisions from the operator**, not one;
- it requires **significant architecture rework** rather than a change inside the existing shape.

Such an item is not "the next thing to attempt with the time left". Bundling it alongside a
queue of small finished tasks costs the thing that makes a session worth anything: **clarity,
lucidity, and fidelity of outcome.** A session that carries one large architectural question
produces a decision you can trust. The same question wedged between six small merges produces a
tired judgement nobody can audit later. Defer it, say plainly that it needs its own session, and
name what that session should open with.

**C3 — the decision is genuinely the operator's.** A decision is theirs when **any** of these
hold:

- it sets or changes doctrine — an ADR, a policy or quality bar, a target others will be held to;
- it is one-way or expensive to unwind;
- it spends money, consent, credentials, or reputation;
- reasonable experts would disagree, and the disagreement is about **values or priorities**
  rather than facts you could go and check.

It is **not** theirs merely because it is difficult, and **not** theirs when it is the last
step of work they already approved and the implementation implies the answer. Rubber-stamping
is not judgement; do not manufacture approval requests out of work you could finish.

Every C item defers the same way: a **comment on the ticket** carrying the evidence and the
brief, a **row in the status file** referencing that ticket, and a **place in the roadmap's
deferred queue** with its priority. The operator revisits it from the tracker, so the tracker
must carry enough that they never need this session's transcript to understand it.

## 2. The deferral contract — four artefacts or it is not a deferral

A deferred item costs something to defer, or the lane becomes a dumping ground. Every deferral
carries **all four plus its reason code (C1, C2 or C3)**, and an item missing any of them has
been dropped, not deferred:

1. **A comment on the ticket** with the evidence: what was attempted, what blocked it, the
   file and line, the review verdicts. Enough that the next attempt does not re-derive it.
2. **A tracker entry** — `ROADMAP.md` and the status file — with a priority and the sprint or
   milestone it now belongs to.
3. **A named next action**, shaped by the reason code. **C1**: the invariant the next attempt
   must satisfy, and why patching failed twice. **C2**: what the dedicated session should open
   with — the decomposition needed, the decisions it must reach, the architecture question it
   exists to answer. **C3**: a decision brief — the recommendation as a verb and an object, what
   it unblocks, what it costs if called wrong, and whether it is `cheap`, `costly`, or `one-way`.
4. **What it blocks**, so the cost of leaving it is visible rather than implied.

## 3. Hand the tracker to the delivery owner

Do not reconcile the plan freehand. **Trigger the project's delivery owner** —
`delivery-manager` where it exists, otherwise `delivery-orchestrator` — to own the reconcile
and verify it against the Definition of Done. It re-derives, rather than inherits:

- milestone burndown and whether any milestone slipped enough to be re-planned rather than
  re-dated;
- `STATUS.md`, `ROADMAP.md`, `CHANGELOG.md` and any ADR or HLD the iteration touched, brought
  into line with what actually merged;
- the deferrals from §2, placed and prioritised in the plan rather than listed in a chat
  message;
- issues closed with their ruling recorded, and cross-links running both ways.

Every figure comes from a command run now. A number you did not derive this session is
labelled unverified.

## 4. Clean the baseline

- Prune every branch and worktree the read-only [lane hygiene report](../../scripts/lane_hygiene.py)
  lists as a removal candidate (merge, rebase and squash aware; `--pr-state` asks `gh`). A ref
  it cannot show integrated, or whose patch was reworked, stays — keep it and say why.
- End state, with evidence: `main` in sync with origin, worktrees back to main, the gate green
  on `main`, and `git branch -r --no-merged origin/main` empty apart from refs you have
  explicitly left for the operator and named.
- **Never** delete an unmerged ref, force-push, or route around a guard to make the tree look
  clean. Clean means merged, not hidden. When matching push output, match the success line
  itself — a substring that also appears in an abort or failure line will prune a live branch.

## 5. The release-worthiness advisory

State, in order:

1. **What landed since the last tag**, by SHA, grouped: feature / fix / security / docs.
2. **SemVer call** — MAJOR / MINOR / PATCH / none yet, justified in one line against the
   project's own definitions, not the general ones.
3. **Tag-worthy?** A verdict, not a hedge. "Not yet, these N commits accumulate toward
   v1.(X+1)" is a common and valid answer. **The operator cuts the tag; you propose it.**
4. **Maturity delta** — did the iteration move the project's own instrument or a milestone?
   Measured, not felt. "Infrastructure that shipped nothing a user sees" is a legitimate answer.
5. **Clean-baseline confirmation** from §4, so the next scope starts from a known-good point.
6. **The operator's queue** — the Lane C items, sorted so the compounding ones are first.

## What stays theirs

Cutting the tag, publishing the release, accepting an ADR, spending money, one-way doors:
draft and propose, never execute. `wrap-it-up` gets the work ready to tag; the operator tags.
