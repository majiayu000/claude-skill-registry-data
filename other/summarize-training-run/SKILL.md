---
name: summarize-training-run
description: Summarize a completed ML training/fine-tune run into a markdown report at .docs_claude/training/<run-name>.md — what happened, bugs found, and per-dataset eval results. Use after a training run finishes and you want a durable, findable record. Writes into the same .docs_claude/ tree that the scaffold-project skill creates and owns.
user_invocable: true
argument-hint: "<run-name-or-run-dir> — e.g. odise-jun18-2026-102am or runs/odise-jun18-2026-102am"
allowed-tools: Read, Write, Bash(mkdir:*), Bash(ls:*), Bash(grep:*), Bash(awk:*), Bash(tail:*), Bash(cat:*), Glob, Grep
---

# Summarize Training Run

Write a durable post-run report to `.docs_claude/training/<run-name>.md`. The filename **is** the run name.

`training/` is a sibling of `plans/` and `style-and-beliefs/` inside the `.docs_claude/` tree that the
**`scaffold-project`** skill creates and owns — this skill extends that tree with one file per training run,
and follows its `## Keywords / Tags` convention (see "When Applying"). If `.docs_claude/` doesn't exist yet,
run `/scaffold-project` first (or just `mkdir -p .docs_claude/training`).

Put the doc in the repo that **owns the run** (where `runs/<run-name>/` lives), which may not be the cwd.

## Core Recipe

1. **Resolve the run.** `<arg>` → run dir `runs/<run-name>/` and output path `.docs_claude/training/<run-name>.md`.
2. **Gather facts** (don't invent — read them):
   - `runs/<run-name>/config.yaml` — hyperparams: data paths, lr, epochs, arch, what it warm-started from.
   - `runs/<run-name>/git_commit.txt` — repo SHAs (reproducibility); note the code/seam commit.
   - `runs/<run-name>/metrics.csv` — val trajectory: best epoch, best val/loss, final-epoch loss, convergence
     signal (e.g. a warm-start's epoch-0 val should be far below chance).
   - **Per-dataset eval results** — precision/recall/loss for EACH eval set, not just the pooled val. Pull from
     this session's `veval`/eval output, or `logs/*eval*`. Separate **held-out** from **trained-on** dirs.
   - **Bugs / surprises this session** — crashes, asserts, config gotchas, data issues, methodology traps.
3. **`mkdir -p .docs_claude/training`** and **Write** the doc using the template below.
4. **Report** the path; leave it unstaged for the user to review.

## Template

```markdown
## Keywords / Tags
- training-run
- <model/stage, e.g. verifier, sam-finetune, ufm>
- <domain, e.g. optflow, in-domain>
- finetune | from-scratch
- results
- gotchas

# <Task> — `<run-name>`

**Date:** <date> · **Run dir:** `runs/<run-name>/` · **GPU:** <n> · **Code/seam commit:** `<sha>` (`<branch>`)

One-line: <what was attempted and the headline outcome>.

## Goal
<the problem; the baseline numbers that motivated the run>

## Approach
<config deltas vs the baseline: data mix, lr, epochs, arch; any code seam added and why>

## What happened
<launch issues, epochs completed, warm-start/convergence signals, timing, slow spots>

## Bugs / issues found
<numbered. Each: symptom, root cause with file:line, fix. Include methodology traps, not just crashes.>

## Results
| Eval set | Pre | Post |
|---|---|---|
<one row per dataset — precision / recall / loss. Mark held-out vs trained-on; flag memorization-inflated rows.>

**Verdict:** <did it work? generalize? at what cost?>
**Caveats:** <leakage, baseline apples-to-apples gaps>

## Artifacts
<checkpoint paths, config snapshot, eval CSVs, viz dir, wandb run>

## Next steps
<numbered follow-ups>
```

## When Applying This Skill

1. **Filename = run name exactly** (e.g. `odise-jun18-2026-102am.md`) — matches the `runs/<run-name>/` dir.
2. **Lead with `## Keywords / Tags`** as the very first content (the scaffold-project convention for every
   `.docs_claude/` doc — makes the run findable via "what did we learn about X?" queries). 5–12 lowercase
   kebab-case tags spanning model/stage, domain, doc type (`results`, `gotchas`), and key concepts.
3. **Report per-dataset eval numbers, never only the pooled val** — a pooled holdout masks per-domain
   regression when one dataset dominates the mix. This is the single most common way a run looks better than
   it is.
4. **Separate held-out from trained-on** eval dirs and label memorization-inflated numbers; the held-out
   number is the honest one.
5. **Record bugs with root cause + `file:line` + fix**, including methodology traps (misleading metric,
   masked regression), not just stack traces.
6. **Ground every number in an artifact** (config.yaml, metrics.csv, an eval table) — don't paraphrase from
   memory.
7. **Never stage or commit** — leave the doc for the user to review.
