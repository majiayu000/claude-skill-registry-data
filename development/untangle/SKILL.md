---
name: untangle
description: Use when a codebase built quickly with AI coding tools has become hard to change or trust - competing ways of doing the same thing, duplicate or _v2/_final files, tests that pass but prove nothing, dead code, fixes that break unrelated features, code nobody can explain - or when asked to audit, clean up, untangle or de-slop a repository, or to make it safe for coding agents to keep working in.
argument-hint: "[audit|triage|refactor|sustain] [path]"
---

# Untangle

A tangled codebase is a pile of decisions nobody made. The AI wrote whatever the next prompt asked for, never refused, and never proposed a rethink, so the repo now holds three ways to do each thing and no record of why. Untangling means making each of those decisions once, writing it down, and making the code and its checks agree with it.

You do the mapping, the evidence and the edits. The human makes the decisions.

## Target state

The work is done when all five hold:

1. **One way** to do each thing: auth, data access, errors, config, logging.
2. **Tests fail when behaviour is wrong.**
3. **Every surviving piece has a reason** someone can state.
4. **Decisions are written down** where the next person or agent will read them.
5. **Automated checks** stop the tangle growing back.

If the codebase already meets these, say so and stop. Inventing work is a failed audit.

## Rules for every phase

- **The ledger is the state.** `UNTANGLE.md` at the repo root records coverage, findings, decisions and progress. Read it first and update it before your turn ends. A long cleanup outlives your context window; the ledger is what carries over. If it exists, resume from it instead of auditing again.
- **Evidence or it is not a finding.** Each finding carries `file:line` and the command or observation that shows it. "Smells messy" is not a finding.
- **You propose, the human decides.** Nothing is deleted, merged or declared the winner without an approved ledger row. Recommend a default for every decision so approval is cheap.
- **Structure and behaviour change in separate commits.** A refactor that also fixes a bug cannot be verified as either.
- **Report only what you ran.** Record commands with their real results. Record what you read closely, what you only mapped, and what you never opened.
- **Subtract.** No rewrite, no new dependency, no new abstraction layer, no compatibility shim. The line count should fall.
- **Secrets.** On finding a live credential, stop and tell the human to rotate it. Never print its value. Never rewrite history yourself.

## Phases

Audit → Triage → Refactor → Sustain, in that order. With no ledger, start at Audit. With a ledger, continue from the phase it records. An argument naming a phase or a path narrows the work. It never skips Audit, because Refactor acts only on approved findings.

**Scale to the scope.** When the work is one area or one change (such as removing an old feature), keep the ledger to Baseline, Test the tests, Findings, Decisions and Slices, and score only the scorecard checks the scope touches; mark the rest `out of scope`, not `n/v`.

### 1. Audit: read-only

Changes nothing except `UNTANGLE.md`. Start it from the template in `templates.md`.

1. **Baseline.** Find the real install, build, test, lint and typecheck commands and run them. Record the results verbatim. A repo that will not build from its README is finding one.
2. **Map before reading.** File listing, sizes, entry points, import direction, churn from git history. Then choose where to read closely, riskiest first: auth, money, data writes, infra. Record coverage per path.
3. **Hunt** using `catalog.md`. Run analysis tools ephemerally (`npx`, `uvx`, `go run`) so the project's dependencies stay untouched.
4. **Test the tests.** Pick three business rules. For each one, change the rule so it returns a wrong answer without raising, run the suite, restore the file with `git restore`, and confirm `git status` is clean. Record whether any test noticed.
5. **Score** the scorecard in `templates.md`. Each check is pass, fail, or "not verifiable from the repo" with the question the human must answer.
6. **Report and stop.** Top findings by risk, what is fine, what was not covered.

### 2. Triage: decide

1. Before listing fixes one by one, look for the single decision that dissolves several findings. Ask what this code would look like if its requirements had been known from the start.
2. For every concern with competing implementations, recommend a winner and give the reason: most call sites, best tested, matches the framework's convention.
3. Mark each finding keep, fix or remove. Rank by risk: chance of harm × how much depends on it. Before removing anything that still works because something else "replaced" it, list every capability it has that the replacement lacks. Those move first, in their own slices, and only then is the old code removed.
4. Order the slices. Safety net first, then removals (cheap, and they shrink everything after them), then consolidation, then restructuring.
5. Present one table, get approval in one pass, and stop until you have it. Record rejections as `wontfix` with the reason.

### 3. Refactor: one slice at a time

Work on a branch named `untangle/<topic>`. Never push. For each approved slice:

1. **Net.** Tests cover the behaviour this slice touches, and you have watched them fail under a deliberate break. If they do not, write characterization tests first: pin what the code does today, bugs included. Log each bug as a new finding instead of fixing it silently.
2. **Change** one concern.
3. **Verify** with the full baseline commands. Read the totals, not just the exit code: skipped, cancelled or errored tests count as red, and the test count must not fall below the baseline. On red, fix the change or revert the slice.
4. **Commit** with the finding IDs, update the ledger, and continue to the next slice without asking.

Stop and ask when a slice needs a decision the ledger does not hold.

"Dead" means proven unreachable: a static tool's verdict plus a search for dynamic reach through string lookups, reflection, routes, DI names, config, cron, templates, public API and callers outside the repo. Anything unproven is `suspect` and goes to the human.

### 4. Sustain: make it stick

1. For each decision, ask whether a machine can enforce it. If it can, add the lint rule, import boundary, CI step or test. Prose rules are for what machines cannot check.
2. Write `AGENTS.md` from the decisions: commands, the one way per concern with a pointer to an example file, and where new code goes. Keep it short enough to be read every session. If `CLAUDE.md`, `.cursorrules` or similar files exist, make one the source and have the rest point to it.
3. Write an ADR for each decision that picked a winner.
4. Make the README's clean-checkout setup true, and commit an env template.
5. CI runs the baseline commands and fails on red. Branch protection and alert routing live outside the repo, so list them for the human.
6. Re-score, record before and after, and leave unfinished items listed in the ledger.

## When you are tempted

| Thought | Do instead |
|---|---|
| "I'll fix this while I'm here" | Add a finding. Unapproved changes are how the tangle was made. |
| "The test is outdated, I'll adjust the assertion" | A red test after a structural change means the change altered behaviour. Fix the change or revert it. |
| "Nothing references this, it's dead" | Prove it against dynamic reach, or mark it `suspect`. |
| "A wrapper keeps the old callers working" | Update the callers. A shim is surplus with a new name. |
| "This should just be rewritten" | Slices. A rewrite discards every behaviour the tests do not cover. |
| "I've covered the codebase" | Coverage is what the ledger says you read. |
| "Context is getting long, I'll wrap up fast" | Write the ledger, say what remains, stop. |
| "The suite passes, so it works" | A pass proves only what audit step 4 showed the tests can catch. |
| "The runner says 0 failed" | Count skipped and cancelled tests. A stopped database can turn half the suite into silent skips. |
| "The new version replaced it, just delete the old one" | List what only the old one can do. Move that first. |
