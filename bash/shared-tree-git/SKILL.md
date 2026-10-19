---
name: shared-tree-git
description: "Operates a shared git working tree where many agents commit concurrently: commits by path with the task-id prefix, never switches/resets/stashes, handles index.lock recovery, and diagnoses and repairs divergence without touching other agents' files. Use when committing in a multi-agent tree, hitting index.lock, or verifying commit isolation."
license: MIT-compat
compatibility: "framework-agnostic; git CLI; Ottili shared-tree workflow"
metadata: {}
allowed-tools: []
---

Standard: name/description/length rules — [agentskills.io standard](../references/agentskills-standard.md).
# Shared Tree Git Skill — Quick Reference (body <500 lines; full procedure in references/shared-tree-git-procedure.md)

## When to use this skill (trigger)
- Multiple agents/lanes share one git working tree (Ottili, Biest host).
- You need to commit only your own paths with a task-id prefix.
- You hit `index.lock` and need to diagnose whether another agent holds it.
- Someone else's uncommitted change blocks your checkout/merge.
- You must verify your commit did not disturb other lanes.

## Disambiguation
- Fires: multiple agents/lanes share one working tree, committing only own paths with a task-id prefix, diagnosing index.lock, another agent's uncommitted change blocking you, verifying your commit disturbed no other lane.
- Does NOT fire for: a solo developer's personal repo, or a normal git push/pull to a private remote.

## When NOT to use this skill
- Single-developer repos with normal git workflow.
- Repos where `git reset --hard`, `git checkout`, or `git stash` are permitted.
- Situations where you can simply push to a private branch.
- A commit that touches only one file you own — the skill still applies (explicit paths + task-id prefix), but the checklist is a 30-second pass, not a ceremony.
- Amending a commit you made this session that no one has seen — still run `git show --stat HEAD` after; the rule is about the shared tree, not about you.

## Decision table — git operation
| Operation | Safe? | When to pick | Pitfall |
|-----------|-------|-------------|---------|
| `git add <paths>` + `git commit -m "id: msg" -- <paths>` | Always safe | Every commit of your own paths | `git add -A` / `add .` / `commit -a` are blocked |
| `git status --porcelain` | Always safe | Check what you are about to commit | Does not tell you about lock holders |
| `git diff -- <paths>` | Always safe | Review your own staged changes | |
| `git log --oneline -n 20 -- <paths>` | Always safe | History of your own paths | Never rewrite history for others' paths |
| `git show --stat HEAD` | Always safe | Verify isolation of last commit | |
| `scripts/check_shared_tree.py` subcommands | Always safe | Pre-commit gate | |

## Numbered procedure (summary; full recipe in references/shared-tree-git-procedure.md)
1. **Check the lock** — `ls .git/index.lock` and `ps` to see who holds it; never remove a live lock.
2. **Stage only your paths** — `git add <your-paths>`; never `add -A`/`.`/`-a`/`.`.
3. **Commit with the task-id prefix** — `git commit -m "skills-engineering-r3-03: msg" -- <your-paths>`.
4. **Verify isolation** — `git show --stat HEAD` must list only your paths.
5. **Handle divergence** — if your commit fails due to a conflicting update, re-fetch only your paths and rebase mentally (never rebase/merge/pull).

## Worked examples
Good (explicit paths, task-id prefix, verified isolation):
```bash
$ git add skills/engineering/honest-status/SKILL.md skills/engineering/honest-status/references/honest-status-procedure.md
$ git commit -m "skills-engineering-r3-01: add worked examples" -- skills/engineering/honest-status/SKILL.md skills/engineering/honest-status/references/honest-status-procedure.md
$ git show --stat HEAD
skills-engineering-r3-01: add worked examples
 ... skills/engineering/honest-status/SKILL.md  | 12 ++++++++++++
 ... skills/engineering/honest-status/references/honest-status-procedure.md | 8 +++++++++
 2 files changed, 20 insertions(+)
# only MY paths listed — isolation verified
```
Bad (blocked form — stages another agent's accidental edit and your commit owns their file):
```bash
$ git add -A            # AGENTS.md forbids this; blocked technically
$ git commit -a        # same; blocked
```
Bad (commit message without the task-id prefix — rejected by policy):
```bash
$ git commit -m "fix typo" -- skills/engineering/honest-status/SKILL.md
# error: commit message missing task-id prefix; got: 'fix typo'
```
Bad (checkout of a path you do not own — silently overwrites another agent):
```bash
$ git checkout main -- skills/business-de/webhooks-safe/SKILL.md
# overwrites the business-de agent's uncommitted work; never do this
```

## Pitfalls from research (real incidents)
- `index.lock` left by a killed CI job looks stale but is still live; removing it corrupts the index for the other agent ([git index docs](references/SOURCES.md#primary-sources)).
- `git add -A` stages another agent's accidental edit and your commit owns their file ([shared-tree policy](references/SOURCES.md#primary-sources)).
- A checkout of a path you do not own silently overwrites another agent's work ([git checkout semantics](references/SOURCES.md#primary-sources)).
- Committing with `--amend` rewrites history that another agent may have based work on ([history rewriting](references/SOURCES.md#primary-sources)).

## Near-miss trigger prompts (act on these immediately)
- "I hit index.lock" — run `scripts/check_shared_tree.py locks` before touching it.
- "I need to commit everything" — run `scripts/check_shared_tree.py staged` first.
- "The commit message is just a fix" — run `scripts/check_shared_tree.py message -- "<msg>"`.
- "I want to clean up this script" — run `scripts/check_shared_tree.py scan -- <file>`.

## Verification checklist (all must pass before you finish)
- [ ] No `index.lock` present, or held by a known process
- [ ] `git add` used explicit paths only
- [ ] Commit message starts with the task-id prefix
- [ ] `git show --stat HEAD` lists only your owned paths
- [ ] No `reset --hard`/`checkout`/`stash`/`rebase`/`merge`/`pull` run

## References
- Full procedure, policy table and worked examples: `references/shared-tree-git-procedure.md`.
- Eval prompts with expected behaviour and failure signs: `references/EVALS.md`.
- Primary sources with URLs and retrieval dates: `references/SOURCES.md`.

## Related skills

`shared-tree-git` is the foundation every other skill in this playbook builds on
(every skill's artefacts are committed here with a task-id prefix), so it has no
outgoing dependencies. It appears only as the *target* of other skills' links:

- module-contract-first — snapshot and boundary doc are committed with a task-id prefix.
- honest-status — status buckets keep the shared tree readable across agents.
- long-test-discipline — commit the wrapper script with explicit paths only.
- problem-json-contracts — the catalogue and schema are committed with a task-id prefix.
- acceptance-harness — the scenario file, evidence and outcome are committed with a task-id prefix.
- outbox-idempotency — the outbox migration and leak-test evidence are committed with a task-id prefix.
- pg-rls-multitenant — the migration and leak-test evidence are committed with a task-id prefix.
- playwright-a11y-e2e — the evidence artifacts and the test script are committed with a task-id prefix.
- foundation-v2-conformance — the conformance report and the fresh-consumer test are committed with a task-id prefix.

These are informational mentions only (no outgoing dependency): the one-way graph
keeps the Related-section graph acyclic.
