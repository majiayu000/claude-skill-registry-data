---
name: turbo-pipeline
description: Use when the user wants a feature built end to end after answering one round of questions and then being left alone — "turbo", "ask me once, then just build it", "I'll answer up front, don't come back to me", "decide the rest yourself". Not for a run that wants a spec approval and no tests (superb:fast-pipeline), one that approves plans and keeps durable run state (superb:pipeline), or one that needs resumable run files and a quorum (superb:pipeline-auto).
argument-hint: "[the feature request]"
---

# Turbo Pipeline

## Overview

Request → targeted exploration → **one batch of at most six questions** → spec
→ plan → subagent-driven implementation → whole-feature review/fix loop →
done. The user is consulted once, at the start. Everything after the batch is
decided from evidence, and where evidence runs out, by **two independent Turbo
Brains** whose higher-confidence answer wins.

This is a thin router over Superpowers skills plus `superb:bug-fix`. It adds no
run files, no controller, no phase plans, no quorum budgets — and it removes no
review seat: fresh implementers, a task review after every task, and a
mandatory final review of the integrated feature. Less bureaucracy, not worse
engineering. **The user's invocation of this skill is a standing instruction**:
where a composed skill's default says to ask, present, or wait, the overrides
below win — user instructions outrank skills, and violating an override to
follow a sub-skill default is violating the user.

## The gate contract

There is one human gate, stage 3. Once its answers are in:

**NORMAL QUESTION TO USER = FORBIDDEN.**

No "which do you prefer", "should I continue", "does this look right", "can you
confirm", "how should I handle this", no spec approval, no plan approval, no
executor choice, no status check, and no equivalent dressed up as a summary
that ends in a question mark. An engineering or product question goes down the
authority ladder and then to the Two-Brain Resolver.

The one exception is **authorization**, never engineering: an action the
runtime, the repository's rules, tool policy or safety require a human to
authorize — merging, pushing to a shared branch, publishing, deploying,
destructive external operations, credential changes, payments, irreversible
account actions. A Brain cannot grant those. During the run, leave such an
action undone and finish everything else. The single place a human is asked
for authorization is the stage-9 handover menu, after the report.

## The authority ladder

1. explicit answers from the stage-3 batch
2. explicit requirements in the original request
3. the specification
4. direct repository evidence
5. established repository convention
6. a Two-Brain decision
7. the smallest reversible engineering choice

A lower rung never overrides a higher one: a Brain cannot overrule a user
answer, a convention cannot overrule requested behaviour, the plan cannot
overrule the spec. Take the first rung that settles the question and move on;
the Brains are dispatched only when rungs 1–5 do not. Trivia — a name, an
import order, message wording — is rung 7 and your own judgement, never a
Brain's.

## Stages

1. **Understand.** Read the whole request: intended outcome, explicit
   requirements, explicit exclusions, constraints, what success means. Ask
   nothing yet.
2. **Explore.** Targeted and read-only: where the feature belongs,
   architecture, patterns to reuse, affected modules, interfaces, similar
   code, dependencies, data flow, integration points, the cheapest existing
   validation the repo has (build, typecheck, lint, syntax check, a quick
   targeted test run) — that becomes the **fast check** — and what the repo
   cannot answer. Two or more independent areas → **REQUIRED:**
   `superpowers:dispatching-parallel-agents`, one read-only explorer per area,
   all dispatched in the same turn; its verification step is skipped, since
   nothing was changed. One area stays one agent, or you. Stop as
   soon as the batch and the spec can be written; read the whole repository
   only when the request spans it.
3. **Ask — the only gate.** From exploration, list every decision that
   materially affects product behaviour, scope, UX, public interfaces,
   architecture, data handling, compatibility or an important constraint,
   **and** that the request, the conversation and the repository do not
   answer. At most six; fewer when fewer suffice; six because six exist is a
   wasted budget. Zero is allowed — say the gate is closed and continue. Lead
   each with a recommendation. Ask all of them **together, once**: through the
   runtime's structured question tool when it holds them all (Claude Code's
   `AskUserQuestion` holds four; Codex has `request_user_input` in plan mode
   and `request_user_input_async` otherwise — check your tool list), else as
   one plain numbered message. Then **wait for the answers**: on Codex the
   async tool returns at once and the answers arrive as the next user
   message, so the run resumes at stage 4 when they do. Never two rounds.
   Record the answers verbatim; they are rung 1 for the rest of the run. A
   question the user leaves unanswered is answered by the ladder, not
   re-asked. The gate is now closed.
4. **Spec.** **REQUIRED:** `superpowers:brainstorming`, fed the request, the
   answers and the exploration findings. Overrides: take its architectural
   path whatever it would classify the request as, with no classification
   announced and no write-back sent for correction — the understanding goes
   into the spec; exploration and questions are done, so do not repeat them
   and do not ask one at a time; always write the spec file
   (`docs/superpowers/specs/YYYY-MM-DD-<topic>-design.md`); choose one
   approach instead of presenting two or three; no section-by-section
   approval, no written-spec review, no visual companion; run its self-review
   and fix inline. Any decision it would put to the user → ladder → Resolver,
   and the decision is written into the spec. Content: behaviour, scope,
   non-goals, affected components, interfaces, data flow, integration, edge
   cases, constraints (including the fast check command), acceptance
   criteria, and a **Decisions after the gate** section that grows through
   the run. **The spec is approved the moment its self-review is done.**
   Commit it.
5. **Plan.** **REQUIRED:** `superpowers:writing-plans`, with the spec as its
   `Spec:`. Overrides: the executor is pre-chosen — the header names
   `superpowers:subagent-driven-development` — so no execution-handoff
   question, no plan review, no scope-check question; every task's steps end
   with `run <fast check command>` and then the commit, so the check reaches
   each implementer inside its own brief; tasks keep the tests its template
   gives them, and Turbo adds no test phase, suite task or verification
   controller of its own. Global Constraints carries the spec's values only,
   never a process rule. Planning exposes an open decision → ladder →
   Resolver. A plan that conflicts with the spec is corrected; the spec is
   not reinterpreted to save the plan. **The plan is approved when its
   self-review is done.** Commit it.
6. **Implement.** **REQUIRED:** `superpowers:subagent-driven-development`,
   as written: workspace and ledger, pre-flight conflict scan, a fresh
   implementer per task on an explicitly chosen model, a task review (spec
   compliance and quality) after every task, its fix loop, breaker and
   parking rules, its Codex `followup_task` resumes. Keep every review seat
   it dispatches; add none. Overrides:
   - **Workspace.** Set up through `superpowers:using-git-worktrees`; the
     invocation is the consent it asks for (native worktree tool if you have
     one, its git fallback otherwise). If the sandbox blocks worktree creation
     it works in place: then create a feature branch in place and never
     implement on main/master. A failing baseline suite is not a question —
     ledger each failure as pre-existing and continue; they are context for
     the stage-8 reviewer, not findings. Append `Base branch: <the branch
     this work forked from>` to the spec's Decisions after the gate and
     commit it; stage 9 reads it there, after the workspace is gone.
   - **Questions.** An implementer's question, a `NEEDS_CONTEXT`, or a
     reviewer finding that conflicts with the plan is answered by you from
     rungs 1–5; what they do not settle goes to the Resolver, and the
     decision is handed back as the answer or the ruling. Its `Ruling:` lines
     carry both confidences when a Brain decided.
   - **Stops.** Of its four stops only the authorization exception survives.
     A plan "so broken every path forward is a guess" goes to the Resolver
     as the smallest question that unblocks it, never to the user.
   - **End.** Stage 6 ends at the last task's `complete` ledger line. Its
     own final whole-branch review, single fix wave and Finish do not run —
     stages 7–9 replace them with a stricter loop. If its broad review did
     run anyway, stage 8 still runs; no earlier review ever waives it.
7. **Validate.** Run what exists, write nothing: the fast check over the
   whole branch, then the repo's existing tests for the touched areas (the
   whole suite when that is what the repo has). Stage 7 runs before every
   stage-8 round. A new failure is a stage-8 finding; a failure identical to
   one ledgered as pre-existing at the baseline is not.
8. **Review and fix — the mandatory whole-feature gate.** **REQUIRED:**
   `superpowers:requesting-code-review` over the whole branch
   (merge-base..HEAD), fresh reviewer on the most capable model, handed the
   diff as a file (SDD's `review-package` script). `[PLAN_OR_REQUIREMENTS]`
   = original request, the stage-3 answers, spec path, plan path (its Review
   Focus lines are what to probe), and the ledger's deferred-minor and parked
   lines for triage. Never tell the reviewer what not to flag. Ask it to
   look hardest at cross-task integration, regressions, invalid assumptions,
   security, data loss and error handling — the defects task reviews cannot
   see. Every Critical and Important finding counts, at the reviewer's
   severity. Minors — cosmetic, stylistic, optional refactors — are listed
   in the report, never looped on. Each **Declined to judge** item is yours:
   settle it from rungs 1–5, else the Resolver; a confirmed gap is a
   finding. Classify every Critical or Important finding:
   - **A. Cause already clear** — wrong argument, missing call, an unmet spec
     line: fix it directly. Directly means without `superb:bug-fix`, not in
     your own context: dispatch **one** fresh fix subagent carrying every
     class-A finding of the round, the same way SDD's final fix wave does,
     and run the fast check; inline only when no subagent tool exists. A fix
     that raises a real question → Resolver.
   - **B. Genuine bug, cause unknown** — intermittent, state-dependent,
     "works sometimes", a regression nobody has traced: **REQUIRED:**
     `superb:bug-fix`, **one invocation per such finding** (its report has
     one symptom). Pre-fill its Step-0 report so it asks nothing: symptom
     from the finding; reproduction: the reviewer's steps, else `unknown`;
     error text, else `none surfaced`; affected surface; last known good:
     the merge-base commit when the behaviour existed before this branch,
     else `never worked`. Overrides: its Step-2 "genuinely the user's call"
     questions → Resolver, handed in as the agreed fix direction; its
     `writing-plans` run gets stage 5's overrides (executor pre-chosen, no
     plan review); its executor is `superpowers:subagent-driven-development`
     with stage 6's overrides, run where this run already works — skip
     worktree setup inside it, stay on this branch — and ending at the last
     task's `complete` line, since this run re-reviews and finishes once;
     if its investigation cannot pin the cause, it does not ask for a
     reproduction — record the finding as open and continue, because a fix
     on a hypothesis is the failure it exists to prevent. Everything else in
     it is unchanged: the proven `file:line` cause, the regression test that
     fails first, its verification task.
   Then review again. Loop while Critical or Important findings remain; not
   for Minors. A finding still open after three rounds is recorded as open in
   the report and the loop ends — still no question to the user.
9. **Finish.** This run's ledgers are the plan's and one per `bug-fix`
   plan it invoked; collect every line containing `Ruling:` from all of them
   into the report's decisions list before touching a workspace. Write the
   terminal report. Delete those workspaces only when stage 8 ended clean;
   findings left open keep them, and the report says where they are. Then
   **REQUIRED:** `superpowers:finishing-a-development-branch`, handed the
   base branch from the spec so its Step 3 never asks. Its Step-1 suite:
   failures identical to the baseline's pre-existing ones do not stop it —
   list them and go on; a new failure is reported open and the branch is
   kept as-is with no menu. Its integration menu (merge, push and PR, keep)
   is the authorization handover — the one question this run asks after the
   batch; the user is present again from that point and its own follow-up
   questions are theirs. Never merge or push on your own.

## The Two-Brain Resolver

**When.** A genuine decision that rungs 1–5 leave open and that you would
otherwise have asked the user: which of two established persistence patterns,
null or empty collection, API v1 or the internal router, extend the abstraction
or add beside it, which repair direction preserves the spec. Not for trivia —
that is rung 7. Not for authorization.

**Dispatch.** Exactly two fresh agents, Brain A and Brain B, in the same turn,
with the **identical** package. They share no transcript, do not see or message
each other, do not spawn, do not edit. Collect both before deciding.

- **Claude Code:** two `Agent` calls in one message, `subagent_type:
  superb:turbo-brain` when it is in your agent list; otherwise a
  general-purpose agent whose prompt is the text between the `SHARED BRIEF`
  markers of `../../agents/turbo-brain.md` (relative to this file) followed by
  the package. Never a fork.
- **Codex:** two `spawn_agent` calls in the same turn, each with its own
  `task_name`, `fork_turns: "none"`, an explicit `model` from your spawn
  allowlist (the most capable) and `reasoning_effort`, and `message` = that
  same brief followed by the package. Plugin agents are not `agent_type` roles
  on Codex, so the brief travels in the message. Then `wait_agent` until both
  have reported (`list_agents` to check). Children can `send_message` each
  other and spawn on Codex; the brief forbids both — do not give them a reason.
- **No subagent tool:** treat both Brains as failed (below).

**Package**, the same bytes for both: the question verbatim; the stage-3
answers and request lines that bear on it; the spec excerpts; the repository
evidence as paths; the plan context when a plan exists; the constraints. No
preferred answer, no options ranked, no hint of which Brain is which.

**Selection.** A response is valid when it is the six-key object the brief
names (a fenced JSON block counts — strip the fence), `confidence` is an
integer 0–100 and `answer` is non-empty.

| Outcome | Decision |
| --- | --- |
| Both valid, materially the same answer | Adopt it; record the higher confidence |
| Both valid, different answers | Higher confidence wins, even at 42 vs 37; record low numbers as a risk |
| Different answers, equal confidence | Rungs 1–5, then smaller blast radius, easier reversibility, less complexity; still tied → smallest reversible choice |
| One invalid or failed | Re-fill that seat once: a fresh agent, the same package. Still invalid → the valid answer alone. Never re-run the valid Brain |
| Both invalid or failed | Rungs 1–5, then the smallest reversible choice |
| Winner contradicts rung 1–5 | The rung wins; the question was mis-routed. Record the contradiction |

A re-filled seat is not a third opinion: two answers are ever compared. Never a
third Brain, never a re-vote because the numbers differ, never the user. Then
continue immediately.

**Record.** Each decision — question, both answers with confidence, the
choice, the risk — goes into the spec's Decisions after the gate (stages 4–5)
or the ledger as a `Ruling:` line (stage 6 onward).

## Terminal report

What was built; spec, plan, branch, base branch and worktree paths; every
decision made after the gate with both answers and confidences, lowest
confidence first, plus every other `Ruling:` line; validation commands and
results; review rounds and what each fixed; deferred minors; findings left
open; actions left undone for want of authorization.

## Red flags — STOP

- A question mark aimed at the user after stage 3 → ladder, then Resolver.
- "This one is important enough to ask" → importance routes to the Resolver,
  not to the user. Only authorization is exempt.
- Presenting the spec or plan "for a quick look" → both are auto-approved.
- Skipping a task review, or the stage-8 review because tasks were reviewed →
  different levels; both run.
- Fixing a finding in your own context while a subagent tool exists → one
  fix dispatch.
- One Brain, three Brains, or a re-vote → exactly two, once.
- Different packages, or a hint, to A and B → identical bytes.
- Brains for a variable name → rung 7.
- `superb:bug-fix` for a finding whose cause the reviewer already named → A.
- A direct patch for an intermittent bug nobody has explained → B.
- Writing a test phase, a suite task or a verification controller of your
  own → you run what exists; what gets written is the sub-skills' business.
- A process rule in Global Constraints or a reviewer prompt → spec values
  only; process rules pre-judge findings.
- Loading `superb:pipeline-auto`'s stages, quorum or run files → different
  skill, different trade.

## Rationalizations

| Excuse | Reality |
| --- | --- |
| "brainstorming requires the user's approval" | Overridden by the invocation. Approval is automatic here. |
| "writing-plans asks which executor to use" | Pre-answered: `superpowers:subagent-driven-development`. |
| "SDD says stop and ask when the plan is broken" | Ask the Resolver the smallest unblocking question. |
| "SDD already reviewed the whole branch, stage 8 is redundant" | Stage 8 replaces that review with a converging loop; it is never waived. |
| "The Brains only reached 45; I should check with the user" | 45 beats the other number or it does not. Record the risk, continue. |
| "bug-fix asks for the missing report fields" | You fill them in before invoking it; `unknown` for the reproduction is a value it accepts and skips re-reproduction on. |
| "bug-fix could not find the cause, so it asks for a repro" | Nobody is there to give one. Record the finding open; never fix a hypothesis. |
| "The user would want to know about this" | They will — in the terminal report. |
