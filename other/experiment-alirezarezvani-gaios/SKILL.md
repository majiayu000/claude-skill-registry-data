---
name: experiment
description: Use to run an autoresearch-style experiment loop — improve a measurable artifact by trying changes, measuring against one objective metric, keeping if better and reverting if not, on an isolated git branch with a logged trail. Trigger on "/experiment", "run an experiment loop", "autoresearch X", "tune/optimize X against a metric", "hill-climb X". Follows references/sops/experiment-loop.md. Enforces the autonomy gate (objective metric + reversible sandbox + no PHI/external) before any unsupervised looping.
---

# Experiment loop (autoresearch)

Hill-climb a measurable artifact: **try → measure → keep-or-revert → log**, on a branch, with a trail. Full procedure: `references/sops/experiment-loop.md`. Existing examples + use-case cards: `experiments/`.

## First, the autonomy gate
Before looping unsupervised, confirm **all three**:
1. **Objective, cheap, automatable metric** (code computes it in seconds–minutes).
2. **Reversible sandbox** (git branch / throwaway data / `.tmp`).
3. **No PHI, no confidential data, no external send, no prod deploy.**

If any fails → **human-in-the-loop**: propose each change, get approval, no overnight run. Regulated/production outcomes feed the human-reviewed change process — never auto-deploy. This is `CLAUDE.md`'s scale-caution-to-stakes rule.

## Run it
1. Pick or write the experiment's `CARD.md` (objective, metric+direction, the one mutable surface, budget, autonomy, owner). New ones can copy `experiments/forecast-tuning/`.
2. `git checkout -b experiments/<tag>`.
3. Baseline run → `tools/experiment_log.py add <results.tsv> --id ... --metric ... --status keep --note baseline`.
4. Loop: edit the **one** mutable surface → run the **read-only** harness → log → keep (commit) if improved, else `git reset`. Simpler-and-equal = keep.
5. Stop on interrupt or the budget. Hand the winner + trail to the human.

## Guardrails
- The eval harness is read-only ground truth — never edit it to game the metric.
- One mutable surface only (reviewable diffs).
- Run artifacts (`results.tsv`, `run.log`, `data/`) are git-ignored; the harness + surface + CARD are the tracked blueprint.
- Don't ship regulated/production changes from the loop.
