---
name: t4-afk
description: Use when the developer hands the agent a bounded batch to run unattended in a T4-team repo (T4 Labs / Slow-Inc) and steps away — "AFK", "run this while I'm away", "just handle it / take it from here", "clear the ready-for-agent queue", "keep going without me", or any long autonomous run where no human will approve each decision. Covers the preflight scope-lock, the may-decide-alone vs must-park boundary, the safe per-item loop, the stop-and-park conditions, and how to land the batch so the repo is never left broken or silently changed.
---

# T4 AFK (unattended autonomous batch)

## Overview

AFK = the developer walks away and the agent clears a **pre-agreed, bounded worklist** on its own, making every implementation decision itself. The whole risk of AFK is a single question the developer isn't there to answer: *is this decision mine to make, or must I stop and leave it?* Get it wrong in **either** direction and AFK breaks — guess past a real decision, or stop to ask what's already answered (see "Act on what's already decided" below). This skill draws that line and keeps the tree safe across a long unattended run.

**AFK does not relax any T4 rule — it removes the human checkpoint, so the rules must hold themselves.** Every gate that a developer would normally eyeball (TDD, `/verify`, `/code-review`, `/scrutinize`, `/security-review`, `/simplify`, issue reconciliation) still runs; the only change is that a **failed gate parks the item** instead of asking a human. Autonomy is bounded scope executed rigorously — never "the dev is away, so power through."

## When to use

- The developer explicitly goes AFK / says "handle it" / "take it from here" and expects a batch done on return.
- Clearing a queue of issues you're allowed to work (authored by us or `ready-for-agent`).
- A long run where nobody will approve each step.

**When NOT to use:** a single interactive task (just do it); exploratory work where the scope isn't yet bounded (grill + PRD first — see `t4-dev-workflow`); a batch dominated by security-boundary or architecture decisions (those are must-park, so there'd be nothing left to run).

## Act on what's already decided — don't re-ask (the other half of AFK)

AFK fails in **two** directions, not one. Over-guessing past a real decision is the famous failure. The opposite — **stopping to ask what's already answered** — is just as much a failure: it turns "handle it while I'm away" into a chat that needs the developer at the keyboard. That is *sticking*, not AFK. The developer's feedback for it is blunt: *"if there's already a way, don't ask again."*

**Before you ask the developer anything, check whether the answer already exists. If it does, act — silently — and put the outcome in the digest, not a question.** The answer already exists when:

- **A standing instruction covers it.** "keep going", "clear the queue", "if scrutinized, merge", "do what you can, skip what needs me" — these are durable for the whole run. Re-confirming each step ("shall I continue?", "merge now?") ignores an authorization you already have.
- **The tracker / ledger / an issue says what to do.** The `ready-for-human` label, an issue body, a park note, the open-work ledger — that *is* the worklist and its state. Reconcile to it; don't ask the developer to re-tell you what a query would answer (`gh issue list --label ready-for-human`).
- **You already produced the recommendation.** A decision brief or a "recommend Option A" you wrote is a decision you may act on under standing authorization — build A. Do **not** re-surface it as "A, B, or C?". (If you're genuinely unsure enough to need them, you didn't have a recommendation.)
- **A senior engineer wouldn't ask.** An obvious default, a naming choice, which of two equivalent implementations — pick it (North Star: the simplest) and move on.
- **The plan names the question *and* names who answers it.** *"for the implementer"*, *"the implementer chooses"*, *"left to whoever builds it"* — these **are assignments, not deferrals**. A plan that hands you a call has decided it; reading "open question" and stopping inverts the sentence. Record your answer where the plan put the question, then build it.
- **A reviewer disagrees with a settled spec.** Record the objection against the decision, **keep the decision**, and escalate only if the finding **invalidates the premise** the decision rested on. A subagent or a bot **disagreeing is not itself new information** about what the developer wants — it is one more opinion, and the spec already weighed opinions.

**Re-read the plan's structured sections before you classify anything as undecided — do not recall them, and do not trust your own summary of them.** The change inventory, the acceptance criteria and the blocked-by list are where an answer most often sits, and a summary is exactly what drops a table row. Three of the four failures that produced this rule happened *after* the agent had read the issue.

## The park test — a sentence you must be able to finish

The list above is how you fill the blanks. **This is the test.** Before parking anything, complete it in writing:

> *"This is unresolved because the plan does not say ___, and it is the developer's because ___."*

- **If the first blank cannot be filled with a quotation from the plan**, the plan does say. Act.
- **If the second cannot be filled with *irreversible*, *trust boundary*, or *the plan explicitly reserved it***, it is the implementer's call. Act.

**Why this needs to be a test rather than advice, and why its bar drifts down on its own.** The two failure directions are not symmetric in how they *feel*. Guessing past a real decision produces a visible wrong artifact, and someone tells you. Over-asking produces a polite, well-organised list that looks like diligence — the cost is paid by the developer, in a turn spent rejecting it, and **it has no natural corrective signal** reaching the agent at all. So the bar for parking must be defended deliberately; nothing pushes it back up by itself. The guess side already has a hard test — the 🛑 table, *"the boundary test is the file's module, not the diff"*. This is the ask side's.

**Its mirror image is a skip, not a stick.** Asking permission to do *less* — offering the developer a choice to skip a gate — is covered in `t4-dev-workflow`, and **nobody to ask is not licence**: an unattended run cannot obtain a waiver, so a gate it cannot pass parks the item rather than proceeding.

**This section is not AFK-only.** It applies **whenever a plan exists, not only when the developer has stepped away** — every failure that produced it happened in an interactive session with the developer present, which is the likeliest reason a rule living here did not fire. `using-t4` carries the one-line version for ordinary work; this is the long form.

**Only interrupt for a decision that is genuinely unresolved AND genuinely theirs** — an irreversible/boundary action, or an ambiguous requirement whose two readings produce materially different code — *and* that none of the above already answers, *and* whose park sentence you can finish. Then **park it** (note + move on); do not block the batch waiting on a reply. Collect every such item into the **one** end-of-run digest. A mid-run "is this ok?" when continuing is the plan is the tell you're sticking.

Worked examples of each failure — including the one where "open question **for the implementer**" was read as withholding — are in `references/afk-artifacts.md`.

The test: *"Could I answer this myself from the standing instructions, the tracker, or my own recommendation?"* If yes, asking is the mistake — act.

## Preflight — lock scope before they leave (last interactive act)

This is the safety gate. AFK runs **only on a bounded, pre-approved worklist**; you cannot decide the scope for them while they're gone.

1. **Load context first.** Read memory (`Home.md` → the relevant notes only) and the repo's `CLAUDE.md` + `docs/agents/*` conventions — this is what keeps new code consistent with the codebase (see `t4-agent-memory`). Read the specific issue(s) you'll work.
2. **Build the worklist from issues you're allowed to work** — authored by us or `ready-for-agent`. Anything not on it is out of scope for the run.
3. **Confirm the batch + STOP conditions with the developer while they're still here** — the worklist, the run bound (N items or a time box), and "here's what I'll park rather than guess." This is the last thing they approve.
4. **Start from a clean, checkpointable tree** (committed or stashed). AFK needs a known-green baseline to revert to.

## The autonomy boundary

| ✅ May decide alone (execute) | 🛑 Must park (stop, don't guess) |
|---|---|
| Implementation details **inside an approved issue**, in a **non-boundary** file | Any edit to a file in a **security-boundary module** — the repo's auth / payments / token / secret / entitlement paths (e.g. `auth`, `wallet`, `unlock`; configure per repo) — **including a "pure rename" or behavior-preserving refactor** |
| Behavior-preserving refactors and picking the **simplest** of equivalent designs (North Star) — **outside boundary modules** | **Architecture / seam / data-model** decisions, or a schema change without a migration path |
| Writing tests; naming within existing convention (non-boundary) | **Irreversible ops** — deleting non-orphan code, destructive migration, force-push, `cache:reset` mid-batch, dropping data |
| Fixing what **your own change** broke | **Scope growth** beyond the issue, or new work you discover |
| Authoring bilingual issue/PR bodies (EN + full Thai mirror) | **Ambiguous requirements** — two readings that lead to different code |

**The boundary test is the file's module, not the diff.** If the file lives in a boundary module, it parks — a rename, a comment, a one-liner all park, because the thing AFK removes is the reviewer who'd confirm the "pure rename" is actually pure. "It's behavior-preserving so it's in the execute column" does **not** apply inside a boundary module: the execute column's refactor allowance is explicitly scoped to non-boundary files. When a decision could be read as both, the 🛑 column wins — every time.

## The safe per-item loop

For each independent item on the worklist:

1. **Conventions first.** Read the relevant `CLAUDE.md`/`docs` section and the neighboring code before editing. Match surrounding style; surgical changes only (touch only what the item needs).
2. **TDD** — red → green → refactor (mandatory, no exceptions AFK).
3. **Checkpoint per green.** Commit small at each green step; **never leave the tree broken between items** — the next item, and the returning developer, both start from green.
4. **Run the gates unattended, at this item's green** — `/simplify`, then `/verify` (E2E for any frontend change — unit tests can't see real layout/hydration), `/code-review` + `/scrutinize`, and `/security-review` if a boundary was touched.

   **A gate deferred to the end of the batch is a gate that did not run.** Not a lesser version of running it — the same thing as skipping it, because by then the work it was supposed to judge is committed and the next item was built on top of it. Measured: a batch that deferred `/code-review` and `/scrutinize` to a single run against 62 commits found **three defects, all already committed**, one of them written by that same session hours earlier, and two of the three fixes had to be written *after* the branch had merged.

   **Why these two and not the others.** `/verify` leaves a green suite and `/simplify` leaves a diff, so postponing either is visible. `/code-review` and `/scrutinize` **leave nothing** unless the reviewer writes it down — so deferring them costs nothing you can see until something is found, and a deferred gate and a falsely-declared one produce the same record. That is `check-gate-ledger`'s problem seen from the other side.

   **It fails on a change of shape, not on indiscipline**, which is why "be more careful" does not fix it. A batch that opens with tracker items — sub-issue links, label edits, an issue body — is a batch where `code-review=n-a` is *correct* and this step legitimately produces nothing several times in a row. Then the work becomes code, and the loop is no longer where you are. **The cue is the first item that changes a file**, not the start of the batch.

   **So the digest answers per item, not per batch.** "State every gate as ran / not-run / n-a" is satisfied completely by one answer covering fifty commits, which is how a batch reports gates it never ran without saying anything false.
5. **A gate fails and you can't fix it within this item's scope → revert to last green, park the item, move on.** Do not expand scope to chase a fix; do not commit red. (Reverting an in-flight item uses `git reset --hard` / `git clean` — the `t4-gate` hook permits these **only when** `.claude/t4.json` sets `"afk": true`, so set that for an unattended run; force-push and `branch -D` stay blocked.)
6. **Reconcile** — update the issue **body** to current state (bilingual), add a ledger row / ship-log line (see `t4-agent-memory`). Close only with evidence.

## Stop-and-park (never guess past these)

Trigger a park when: a gate can't go green after a bounded retry · the change wants to grow beyond its issue · you hit a 🛑 boundary · a landmine / irreversible op · repeated tool or permission denials · two plausible readings of the requirement.

**To park:** leave the repo at **last green** (revert the in-flight item), write a park note — *what you were doing · why you stopped · the exact decision needed · what's already done* — into the issue body + ledger, then **continue with the next independent item.** One blocked item never blocks the batch, and never becomes a guess.

## Landing the batch

When the worklist is done or the run bound is hit:

- Tree is **green** and committed/pushed; nothing half-applied.
- Every touched issue reconciled: body current, and **closed-with-evidence** or **parked-with-note** — never silently closed, never finished-but-left-open.
- Ledger + ship log updated so the next session inherits real state.
- **One** notification with a digest: done / parked (with the decision each needs) / anything that needs the developer. Notify on batch-done or needs-a-decision — not on routine sub-progress.
- **The digest enumerates the gates; it does not list them.** State every one of `/simplify`, `/code-review`, `/scrutinize`, `/security-review`, `/verify` as **ran / not-run / n-a**, **per item, not per batch** — one answer covering fifty commits satisfies the wording completely and says nothing, which is how the gates get deferred without anything false being written (step 4). A digest that enumerates **cannot omit one by writing less**, which is the only property that matters here: a list of what ran, with the skipped ones simply absent, reads as completeness. The same claim goes on the branch as a `T4-Gates:` commit trailer, where `check-gate-ledger` blocks the push if a gate is unstated.
- **The guard does not force a gate to run** — `not-run` passes. Declaring a skip is allowed; being silent about one is not. A gate you could not pass still parks the item (above); a gate you chose not to run is reported as `not-run` with the reason.

## Common mistakes (AFK rationalizations)

| Rationalization | Reality |
|---|---|
| "Dev's away, I'll just power through the ambiguity." | Ambiguity is a **park**, not a coin-flip. A wrong guess unattended costs more than a parked item. |
| "Skipping the test/review step is fine for this one — no one's waiting on it." | Skipping a rule needs a **checkable proof** it doesn't apply, not a judgment call (`t4-dev-workflow`). AFK removes the reviewer who would have caught a bad exemption, so the bar goes **up** here, not down — and the proof goes in the landing digest. |
| "It's a security file but the change is tiny." | Blast radius, not diff size, decides. `auth`/`wallet`/`unlock` = park regardless of size. |
| "It's a pure/behavior-preserving rename, so it's in the may-decide-alone column." | The execute column's refactor allowance stops at boundary modules. A rename in `wallet`/`auth`/`unlock` parks — "pure" is the reviewer's call to confirm, and AFK removed the reviewer. |
| "I'll grep to prove it's internal-only, then rename it." | The grep is you reviewing your own boundary change unattended. Park it; the developer confirms "internal-only" in 20 seconds on return. |
| "Looks done, I'll close the issue." | Close only with evidence (commit/test/impact). No human is checking behind you — the evidence is the check. |
| "I'll write it up as fixed; it almost certainly is." | The digest is the *only* report of an unattended run, so an unverified verdict in it is indistinguishable from a verified one. Mark each item **verified** (with the artifact) or **hypothesis**; "tests not run" is a complete line (`t4-dev-workflow`). |
| "The digest covers what I did — the gates I skipped just aren't in it." | That rule covers a claim you **make**. This is the other half: **a true report with a hole in it.** Listing what ran and not what did not is how nine PRs shipped with `/simplify`, `/code-review` and `/scrutinize` at zero and nothing detected it. Enumerate every gate as ran / not-run / n-a. |
| "I'll commit this red and fix it next item." | Never leave the tree broken. Revert to green and park; the returning dev must land on green. |
| "This item needs a bit more than the issue said — I'll just widen it." | Scope growth is a park. Note the extra work as new tracked work; don't absorb it silently. |
| "One notification per item so they see progress." | One digest at the end (or on a real decision). Per-item pings defeat AFK. |
| "I'll ask which option they want before building." | If you already recommended one and hold standing authorization, **build it**. Re-asking "A or B?" you can answer yourself is sticking, not AFK. |
| "Let me just confirm they still want me to continue." | "Keep going / handle it" is durable for the run. Re-confirming each step ignores the authorization you already have. |
| "I'll ask what they want me to do next." | Read the tracker (`ready-for-human` label, issue bodies, the ledger) — it already says. Ask only for what no query and no standing instruction can answer. |

## Cross-skill

- Session-start reads, the ledger, ship log, memory vault → **t4-agent-memory**.
- The pipeline, issue lifecycle, bilingual rule, auto-triggered gate map → **t4-dev-workflow**.
- Recording an outcome you hit mid-batch (post-mortem / ADR / impact entry) → **t4-engineering-records**.
- Delegating a mechanical sub-task to a cheap model during the batch → `qwen-agent` (same do-not-delegate boundary as 🛑 above).

See `references/afk-artifacts.md` for the preflight checklist, the park-note template, and the landing-digest template.
