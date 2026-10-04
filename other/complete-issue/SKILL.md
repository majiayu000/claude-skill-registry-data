---
name: complete-issue
description: Implement a change end-to-end from a freeform prompt - settle the requirements, design the engineering approach and get it approved, implement with TDD, run the format/compile/credo/coveralls gates without shortcuts, self-review the diff like a senior engineer, QA the finished change in the running app, record a demo video when it is visible there, then commit and open the PR. Use when the user wants to "complete an issue", "work the ticket", or hands over a description of something to build.
---

# Complete Issue

End-to-end workflow: requirements → design the implementation → **get the plan approved** → implement
(TDD) → gates → self-review → QA → commit → PR.

- In all interactions and commit messages, be extremely concise and sacrifice grammar for the sake of concision

## 1. Gather context and start

**The prompt is the requirements.** There is no ticket system here — whatever the user described is
the spec, and anything it leaves open is a question for them, not a gap to fill in silently.

**Check the requirements are settled before building.** If there are unresolved questions about what
the change should do, ask them now rather than discovering them mid-implementation.

**Get off `main` before your first write.** Create a branch named for the change
(`git switch -c budget-rollover`). This is your explicit, standing permission to create and check out
that branch without stopping to ask — but never commit to `main`.

## 2. Design the implementation

Design the high-level approach (contexts, public interfaces, data flow, module/function
responsibilities) **and** the low-level implementation details.

You must read these files before planning:
- [docs/standards.md](../../../docs/standards.md)
- [docs/tests.md](../../../docs/tests.md)
- [CONTEXT-MAP.md](../../../CONTEXT-MAP.md) and the `CONTEXT.md` of every context you will touch

**Do not start implementing in this step.** This step ends with a written plan and an explicit approval gate.

### Resolve the details — ask rather than assume

Resolve each design decision — approach-level and low-level alike — against the docs and the code first: docs settle it → code settles it → **ask**. Most should resolve cleanly from `standards.md`, `tests.md`, the relevant `CONTEXT.md`, and existing patterns in the codebase — when they do, cite what settled it and move on.

When the docs and code *don't* settle it, **ask — do not fall back on a "reasonable default" and proceed.** The bar for assuming silently is high: a true default is something a senior engineer on this codebase would consider the only sensible reading. Anything that involves judgment — which context owns it, data shapes, function decomposition, where a boundary sits, how an edge case behaves, which of two existing patterns to follow — is a question for the user, not a guess. Ask one focused question at a time, each with your recommended answer and why, and treat their answer as the decision. Unclear domain rules — how a balance should behave, where a remainder goes, what happens at a month boundary — are questions for the user, not guesses.

If you catch yourself writing "I'll assume…", "presumably…", or "I'll go with X for now" — stop and ask instead.

### Write the plan and stop for approval

Once the questions are settled, write up the implementation plan and present it to the user. Keep it proportionate — enough to build cleanly, not an exhaustive spec — and cover (keep this concise):

- **What you'll build**, restated against the requirements so the user can confirm it delivers them.
- **Approach**: the contexts and public interfaces touched, the data flow, the module/function responsibilities, and any decision worth recording — plus a line on why, since you are choosing it.
- **File-level changes**: which modules/files you'll add or edit, and the key actions, schemas, or migration changes in each.
- **Test plan**: the vertical slices you'll TDD, named with the vocabulary the context's `CONTEXT.md` owns.
- **`CONTEXT.md` edits** your design requires, using the format in [docs/context-format.md](../../../docs/context-format.md). Follow that convention even where existing files do not. A change that introduces a new domain word, or changes what an existing one means, is not done until the `CONTEXT.md` says so.
- **Assumptions still in play**: every decision you resolved by default rather than by asking, called out explicitly so the user can correct any before you build.

**Hard stop here.** Present the plan and wait for the user's explicit approval before moving to step 3.

## 3. Implement test-first

**Confirm where you are before your first write.** Run `git rev-parse --show-toplevel` and `git branch --show-current` and check you are in the right checkout on your own branch. Several sessions may be working this repo at once, and landing in the wrong one means editing alongside someone else's uncommitted work. If you are not where you expect, **stop and report** — do not commit, switch branches, or stash to get out of it. Re-check this after any interruption; a resumed shell can come back with a different working directory.

Postgres runs in docker compose (`docker compose up -d db`). Before starting any work, run
`MIX_ENV=test mise exec -- mix setup`.

Hand the approved plan and the implementation design from step 2 to the [tdd](../tdd/SKILL.md) skill.

Two rules from [CLAUDE.md](../../../CLAUDE.md) that are easy to get wrong here, repeated because
getting them wrong is a security bug rather than a style one:

- **Authorization is ownership.** Take `user_id` from the scope, never from attrs, and pin it between
  the scope and the record in the action's function head.
- **There are no factories.** Tests create every record through the context function that owns it.

## 4. Pre-commit gates

Run all of these sequentially. **All must pass before commit.** Run each via the Bash tool with the sandbox disabled (the test database needs a real TCP socket).

### 4a. `mise exec -- mix format`

Always run format on the **whole project** — never with a file filter or path argument. It is fast, and the PR must be fully formatted. Re-stage any files this rewrites before committing.

### 4b. `mise exec -- mix compile --warnings-as-errors`

### 4c. `mise exec -- mix credo`

Always run credo on the **whole project** — never with a file filter or path argument. It is fast, and the PR must be clean everywhere, not just in the files touched this turn.

The [tdd](../tdd/SKILL.md) skill ran this at the end of every slice, so this should pass first time. **If it doesn't, that is a signal, not a formality** — something got past the per-slice check, and the fix belongs at the root rather than papered over here.

Forbidden routes to green:
- Editing `credo/.credo.exs` to disable a rule.
- Adding `# credo:disable-for-next-line` / `# credo:disable-for-this-file` / etc.
- Deleting the flagged code purely to silence credo.

Fix the underlying issue credo is pointing at.

### 4d. `mise exec -- mix coveralls`

Forbidden routes to green:
- Adding `@tag :skip` or `@tag :pending`.
- Deleting tests or commenting them out.
- Weakening assertions (`assert true`, removing branches, broadening matchers) to dodge a real failure.

If a test fails, fix the underlying behavior. If a test is genuinely wrong, fix the test for the *right* reason and explain the correction to the user.

**Every line this change adds must be covered, and the total must not go down.** `mix coveralls.detail` shows which lines are not. The project is not at 100% yet, so the rule is a ratchet, not a threshold — leaving a new uncovered line makes the number a little more wrong permanently.

If any gate fails, loop back into the [tdd](../tdd/SKILL.md) cycle, fix the root cause, then re-run **all gates from the top** — never partial re-runs.

## 5. Self-review before the PR

This is the senior-engineer judgment review, done on your own diff *before* the PR exists so findings get fixed instead of posted.

Don't spend effort on the deterministic gates (`mix format`, credo with the custom `SpendableCredo` checks, the test and coverage suite) — you already ran those in step 4, so they are settled. This pass is the layer none of them can do: whether the design is right and as simple as it should be, whether a user-facing flow is actually good UX, cross-cutting correctness and security reasoning that spans files, arithmetic correctness, and documentation the diff has quietly made wrong.

Get the diff locally — `git diff main...` and `git diff --staged` — not from a PR.

### Review like a senior engineer

Review the change the way the best reviewer on the team would: build a model of what it is trying to do, form your own opinion of how it should be done, then judge the implementation against that.

Force depth with these moves. They are prompts to think, not boxes to tick:

- **Design your own version first.** In 2-3 sentences, describe how you would implement this goal. Then read the diff. Every place it diverges is either a finding or something you learn, but you have to engage to find out which.
- **Hunt for what could disappear.** The strongest simplification is deletion. For each new function, module, abstraction, option, or parameter: does it earn its keep, or could it be inlined, merged, or dropped? Does something in the codebase already do this? Is the complexity justified by a real requirement, or is it speculative? A util that is used once is not a util.
- **Walk every user-facing flow as the user.** Trace the real path, click by click or request by request. Narrate each state: initial, loading, empty, success, error, and the ugly edge (slow network, double submit, the back button, no results). Where is the friction, the dead end, the confusing copy, the missing feedback? Would you be happy using this? Is it consistent with how the rest of the app behaves?
- **Name what surprised you.** Anything that made you double-take is a candidate finding: either it is wrong, or it is right but needs a comment so the next reader does not have to double-take too.
- **Check it against its own intent.** Does it actually accomplish the goal from step 1? Does it overreach (unrelated changes, scope creep) or underdeliver (a case the goal implies but the code skips)?
- **Look for what is absent.** A diff scan only shows what is there. What should be here and is not: a test for the new branch, a migration, an index for the new query, a `CONTEXT.md` update, a rollback path? Stale docs hide here — the diff changes behavior but leaves a `CONTEXT.md` or README describing the old one.

Lead with the two dimensions that carry the most risk in this app: **ownership** — every query filtered by `user_id`, every action head pinning the scope against the record, no id taken from attrs — and **money**, where a wrong number renders just as prettily as a right one.

### Confirm changes

Confirm your findings and proposed changes with the dev, ask what pieces they want handled and proceed from there.

## 6. QA it in the running app

**Commit the implementation first.** Once the gates pass and the self-review findings are settled, commit on the feature branch before you start QA. QA is the longest, most interruptible phase of this skill — it drives a real browser, it can run for an hour, and a crash or a session limit in the middle of it loses everything uncommitted. Committing first costs nothing: QA fixes, the demo, and any review changes all land as later commits, which is what you want anyway (never amend). Push it too, so the work survives losing the machine.

Then the change is *complete* — which is exactly when it gets QA'd rather than shipped. Hand it to the [qa](../qa/SKILL.md) skill: it starts the dev server, builds a checklist from the requirements and the diff, drives every item in a real browser, and then goes looking for anything that looks off, including problems this change did not cause.

**Run it in a subagent** — see [subagent-delegation.md](../subagent-delegation.md) for what the prompt must carry and what has to come back. Reading screenshots and re-driving failed checks is the most token-expensive part of this workflow, and none of that transcript is needed after the findings table. Tell it to leave the dev server up if a demo pass follows.

**Do this for any change a user can reach** — a screen, a LiveView interaction, a route, a changed calculation, a sync. Skip it only when there is genuinely no runtime surface (a pure refactor with no behavior change, a test-only change, config or CI), and say in one line that you skipped it and why.

Blockers and majors it finds are not optional: fix them through [tdd](../tdd/SKILL.md), re-run **all gates from the top**, and re-run the affected checks. Everything else goes to the dev to triage.

## 7. Record a demo when there is something to see

If the change is **visible in the running app**, record it with the [record-demo-video](../record-demo-video/SKILL.md) skill. A reviewer who can watch the feature work reviews the diff differently than one who has to imagine it, and in an app whose whole job is arithmetic, "it renders" and "it renders the right number" are different claims.

**Run it in a subagent**, per [subagent-delegation.md](../subagent-delegation.md) — expect three or four takes, and only the final mp4 matters.

**Record when** the change alters something a user can see or do: a new or changed screen, a LiveView interaction, a changed calculation whose result is displayed, a workflow that now takes fewer steps, or a bug whose symptom was visible.

**Skip it when** there is nothing to point a camera at: a pure refactor with no behavior change, a test-only change, a migration with no UI surface, config or CI changes, or a fix whose only observable is a log line or an absent exception. Say in one line that you skipped it and why, rather than silently not doing it.

**If you are unsure whether it's worth recording, ask the dev.** A 20-second clip is cheap; the judgment call about whether reviewers need it is theirs.

Keep it short and drive the **actual behavior that was asked for**, with realistic data. A demo that exercises the happy path with placeholder values while the requirement was about an edge case is worse than no demo, because it looks like verification and isn't.

## 8. Commit and open the PR

- The implementation was already committed in step 6. Commit whatever came after it — QA fixes, the demo's supporting changes — as **further commits**, never an amend, so the history shows what QA changed.
- Push the branch and open a **draft** PR against `main`.
- Keep the PR body as short as the change allows: what it does, why, and anything a reviewer would otherwise have to work out for themselves. No filler sections.
- **If you recorded a demo**, follow [record-demo-video](../record-demo-video/SKILL.md)'s publishing section — GitHub has no API for attaching media, so offer the user the file path to drag in themselves rather than pretending it can be automated. If you skipped the recording, say so in one line with the reason.
