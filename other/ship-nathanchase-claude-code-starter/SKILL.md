---
name: ship
description: "Take a work item — a freeform task, a GitHub issue (#N or URL), or a Jira ticket (KEY or URL) — all the way to a shipped PR. Resolves the item (text + images + comments), investigates, plans, adversarially vets the plan, implements, verifies, and opens a PR. Sets a /goal so it runs to completion across turns. Use when the user says implement / build / ship / deliver a task, issue, or ticket."
argument-hint: "[task description | #issue | github-url | JIRA-KEY | jira-url]"
disable-model-invocation: false
allowed-tools: Read Write Edit Grep Glob Bash Task
---

# Ship a work item

One pipeline, any input: **resolve → investigate → plan → vet → implement → verify → ship.** The two failure modes it guards against are *coding before the work is understood* and *coding more than the item asks for*.

This skill leans on three primitives instead of a hardcoded script:

- **`/goal`** carries the work across turns — set one measurable completion condition and Claude keeps going until an evaluator confirms it holds. This replaces fixed "max N iterations" budgets.
- **Subagents** keep investigation and review in separate context windows (they counter agentic laziness, self-preferential bias, and goal drift).
- **A dynamic Workflow** is the escalation for genuinely large items (many files, cross-cutting) — fan out investigators and adversarial verifiers. Most items don't need it: *ask whether it really needs more compute* before reaching for one.

> **Project setup:** substitute your **base branch** (`main`, or `develop`/your integration branch) and your project's **quality-gate commands** (typecheck / lint / test) wherever they appear — read them from `package.json` scripts / the build config. Git identity is assumed already configured.

---

## Step 1 — Resolve the work item (classify-and-act)

Detect the input type from `$ARGUMENTS` and pull everything before planning:

- **GitHub issue** (`#N`, or `github.com/<owner>/<repo>/issues/N`) → `gh issue view <N> --repo <owner>/<repo> --json title,body,labels,comments,state,url`. Default repo: `gh repo view --json nameWithOwner -q .nameWithOwner`.
- **Jira ticket** (`ABC-1234`, or `your-site.atlassian.net/browse/ABC-1234`) → fetch with the Atlassian MCP `getJiraIssue`; use the `jira-attachments` skill to download and **`Read` every image** (a ticket's real intent is often in the picture).
- **Freeform text** → use it directly as the work description.
- **Empty** → bail; ask what to ship.

**Ingest images either way.** Screenshots may be the desired end state, a bug repro, or a user-provided example. Read them — never plan from alt text.

**Done when:** you can state the goal in one paragraph and list the acceptance criteria as an explicit checklist. If criteria are missing or ambiguous, derive them from the evidence and flag the ambiguity before continuing.

## Step 2 — Pre-flight

```bash
git status                                      # if the base branch is dirty, ask to commit first (offer /focused-committer)
git checkout main && git pull origin main       # substitute your base branch
git checkout -b <type>/<kebab-slug>             # prefix by intent: fix/ feature/ chore/ refactor/
```

## Step 3 — Set the goal

Compose one completion condition from the acceptance criteria and set it. The evaluator judges from what you surface in the transcript, so make every clause demonstrable:

```
/goal <the item>'s acceptance criteria are all met (each shown satisfied in the transcript), the project's typecheck, lint, and tests pass (their output shown), and a PR is open against <base-branch> linked to the item — without modifying files unrelated to the plan; or stop after 25 turns
```

A good condition has **one measurable end state**, a **stated check** proving it, and **constraints that must not change**. The `or stop after N turns` clause bounds runaway loops (the old skill's iteration budgets, now expressed as the goal itself).

## Step 4 — Investigate & plan

Investigate with a subagent so the finding — not the file dump — returns to your context:

- **Straightforward item** → one `investigator` agent (Task), or the built-in `Explore` agent for a quick pattern search.
- **Large / cross-cutting item** → a dynamic **Workflow** that fans out investigators (and, if it crosses a client+service boundary, verifies the contract on both sides). Reach for this only when the scope warrants it.

Write the plan to `~/.claude/plans/ship-<slug>.md`: acceptance criteria → the **smallest** set of file changes that satisfies them → the existing repo patterns each change mirrors → test strategy. **YAGNI is the default** — no new dependencies, no speculative abstractions.

## Step 5 — Vet the plan (adversarial)

Hand the plan to a fresh subagent whose only job is to poke holes — a *lazy senior developer* walking the YAGNI ladder (necessity → reuse existing → native/stdlib → already-installed dep → one-liner → minimal code), stopping each proposed change at the first rung that works. Never simplify away validation, error handling, security, accessibility, or anything the item explicitly asks for.

Also run `/plan-analyzer` on the plan file to verify every file reference and assumption against the codebase. Fold both back in.

**Interactive checkpoint (default):** present the vetted plan and get a nod before implementing. Skip only if the user asked to run hands-off (auto mode + the active `/goal` will then carry it through delivery without pausing).

## Step 6 — Implement

Write the minimal, vetted change, mirroring the precedent files for structure and idiom. Follow **`.claude/rules/minimal-code.md`** (reuse before writing, root-cause over symptom, no unrequested abstractions) and the project's standards in `AGENTS.md`/`CLAUDE.md`. Change nothing outside the plan. If you delegate implementation to a subagent or Workflow, tell it to follow that rule — subagents don't inherit session rules.

## Step 7 — Verify

- Run the project's **quality gates** (typecheck, lint, tests) and surface the output — the `/goal` evaluator reads it.
- Run **`/code-review`** on the diff (built-in adversarial review). Fix every real finding, including pre-existing lint/type errors. Re-run until clean.
- Confirm each acceptance-criterion is actually satisfied, not merely attempted. For behavior changes, verify in the running app (`/verify` or `/browser-debug`).

## Step 8 — Ship

1. Group the diff into focused conventional commits and commit them directly (`git add` per logical group → `git commit`), one concern per commit — the logic of `/focused-committer`, done inline since that skill is user-invoked. Reference the item with a closing keyword (e.g. `Closes #N`) on the final commit.
2. `git push -u origin <branch>`
3. `gh pr create --base main` (substitute your base branch) — body is summary bullets + a Test Plan checklist.
4. Link back: comment on the issue/ticket with the PR URL.

When the PR is open and the gates are green, the `/goal` evaluator sees the condition met and clears the goal.

---

## Bail-out conditions

Stop and hand back if: the item doesn't exist or is empty; delivering requires changes to a separate repo the user hasn't authorized; the only viable path needs a new external dependency; or verification can't be made green after a genuine attempt. Run `/goal clear` when you bail so the loop doesn't keep firing.

## When NOT to use this

A one-line fix or an obvious change doesn't need the full pipeline — just make it and verify. Reserve `/ship` (and especially the dynamic-Workflow escalation) for substantial, multi-step work with a verifiable end state.
