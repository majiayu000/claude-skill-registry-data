---
description: |
    Use when the user asks Codex to set or run a goal for iterative self-improvement, skill improvement, prompt optimization, eval-driven refinement, plateau-based loops, or bounded autonomous runs such as "improve this skill over 20 runs", "goal - write yourself a goal", "keep benchmarking until plateau", or "use /goal to evolve this skill". Do not use for one-shot edits without metrics.
metadata:
    category: agentic
    targets:
        - antigravity
name: self-evolve-codex_KM
---
# Self-Evolve Codex

Use this when the user wants Codex to improve a skill, prompt, plugin, or agent workflow through repeated measured attempts instead of one manual rewrite.

The core pattern is autoresearch for Codex skills: define one editable target, one metric suite, one run log, and one stopping rule. Codex should try focused changes, benchmark each attempt, keep winners, discard losers, and stop at the agreed goal, plateau, budget, or safety boundary.

## First Read

Load only what you need:

- `references/loop-contract.md` for the run protocol, safety boundaries, and `/goal` integration.
- `references/metrics-and-plateau.md` when defining metrics, scoring, plateau rules, or benchmark artifacts.
- `references/source-notes.md` when you need the rationale from plugin-eval, self-evolve-skills, autoresearch, or Codex docs.
- `templates/GOAL.md` when drafting a user-visible `/goal` objective.
- `templates/RUNLOG.md` when starting a durable run folder.

## When To Use A Goal

If the user asks for `goal`, `/goal`, a maximum number of runs, a timebox, "until plateau", "keep going", or "benchmark results", treat the task as a goal-driven loop.

If a goal tool is available in this environment, create one with the concrete improvement objective before editing. If only the CLI slash command is available, draft a `/goal ...` command or `GOAL.md` file the user can launch. Either way, write the same objective to the run folder so it survives compaction.

## Setup

Before changing the target:

1. Identify the target file or folder and the canonical source path.
2. Create a run root outside the live target, usually:

   ```text
   ~/.codex/evolution-runs/self-evolve-codex/YYYYMMDD-HHMMSS/<target-name>/
   ```

3. Snapshot the original into `original/`.
4. Write `GOAL.md`, `RUNLOG.md`, `metrics.jsonl`, and `DECISIONS.md` from the templates.
5. Run the baseline benchmark before the first edit.

Do not edit live Skillshare or plugin source until the baseline is recorded and the run contract is written.

## Improvement Loop

For each iteration:

1. Inspect the latest benchmark failures and artifacts.
2. Make one focused change to the candidate copy.
3. Run the metric command or plugin-eval analysis.
4. Record scores, token/runtime data when available, and a short change note in `metrics.jsonl` and `RUNLOG.md`.
5. Keep the candidate only if it improves the primary metric, fixes an auto-reject issue, or preserves score while materially reducing complexity.
6. Stop when the goal is met, the run hits max iterations/time, plateau is detected, or further progress needs user/product judgment.

Prefer plugin-eval for Codex skill structure checks:

```bash
plugin-eval analyze <skill-path> --brief-out <run-root>/brief.json
```

For skills, use `$skill-creator` principles: compact `SKILL.md`, heavy details in `references/`, deterministic helpers in `scripts/`, and trigger evals in `evals/`.

For GPT/Codex prompt text, use `$gpt-prompt-architect`: outcome-first instructions, explicit success criteria, evidence rules, stopping rules, and no personality padding.

## Safety Boundaries

Keep experiments reversible:

- Work in a candidate copy unless the user explicitly asked for live edits.
- Do not change eval scripts, metric definitions, or benchmark fixtures mid-run unless the run log records why and preserves the prior metric.
- Do not publish, push, sync Skillshare, or overwrite canonical source until final review passes.
- Do not chase unbounded improvement. A bounded loop is the product.

## Finalize

When the loop stops:

1. Compare original versus finalist.
2. Apply only approved hunks to the canonical target.
3. Re-run the benchmark and any structural validator.
4. If the target is a Skillshare skill, run the relevant `skillshare` validation/sync command and report exactly what changed.
5. Mark the active goal complete only after the requested artifacts, metrics, and validation are done.

Final report: name the target, run root, best score, iteration count, stop reason, files changed, validation commands, and remaining risks.
