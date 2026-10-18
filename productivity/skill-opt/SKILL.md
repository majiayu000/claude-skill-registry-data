---
name: skill-opt
description: "Use to optimize/improve an existing agent skill against scored tasks. Ports Microsoft SkillOpt: treats the target SKILL.md as a trainable document and improves it via a rollout→reflect→edit→gate→memory loop with a held-out gate, while keeping the model frozen. Trigger when the user wants to tune, harden, or measurably improve a skill."
---

# skill-opt

## What This Does

One agent switches hats: **Setup → Rollout → Score → Reflect → Edit → Gate → Memory**, then repeats.
The run directory `.skill-opt/runs/<skill>-<n>/` is the message bus — every phase reads/writes files
there, making runs resumable from any point. The one-man-play is the backbone, **not a constraint**:
when `parallelism > 1`, rollouts and gating fan out to fresh subagents.

## Up-Front Questionnaire

Ask the user these questions, then write `config.yml` from `templates/config.yml`:

| Knob | Default | Notes |
|---|---|---|
| `target_skill` | — (required) | path to SKILL.md or skill dir |
| `edit_references` | `false` | also edit `references/`? |
| `feedback_source` | `proposed-ratified` | `proposed-ratified` \| `autonomous` \| `user-suite` \| `live` |
| `feedback_timing` | `autonomous` | `autonomous` \| `interactive` (pause at each gate) |
| `output_mode` | `save-as-new` | `save-as-new` \| `overwrite` (keeps v0 backup) |
| `max_iterations` | `12` | hard ceiling on loop iterations |
| `early_stop_patience` | `3` | stop after K gated rounds with no improvement |
| `edit_budget` | `{max_ops: 3, max_words: 80}` | "textual learning rate" per iteration |
| `minibatch_size` | `6` | train tasks per iteration |
| `holdout_fraction` | `0.3` | fraction of suite held for gating |
| `checkpoint_every` | `1` | iterations between checkpoint summaries |
| `parallelism` | `serial` | `serial` \| integer fan-out width |
| `edit_panel` | `1` | candidates per round; gate all, keep best |
| `gate_margin` | `0.0` | held-out margin to accept; passed to `ledger.py gate --margin` |
| `validation_depth` | `self-contained` | `map-only` \| `self-contained` \| `verifiers-env` \| `full-ablation` |

See `references/feedback-sources.md` for how each `feedback_source` builds the task suite.

## The Loop

```
SETUP: questionnaire→config.yml; build/ingest suite→tasks/{train,holdout}; snapshot skill/v0.md;
       ROLLOUT(v0) over holdout → baseline via `scripts/ledger.py record`.
LOOP iter=1..max (early-stop after `early_stop_patience` non-improving gates, or user stop):
  ROLLOUT  : for each train-minibatch task, dispatch a FRESH SUBAGENT given ONLY {current skill text, task};
             write rollouts/iter-NN/task-MM/trajectory.md.
  SCORE    : judge each trajectory (programmatic if available else LLM-judge subagent) → score.json;
             `ledger.py record --split train`.
  REFLECT  : split minibatch into SUCCESS and FAILURE; reflect on each SEPARATELY; read memory/rejected-edits.md.
  EDIT     : propose bounded add/del/replace ops within edit_budget → candidates/iter-NN/{candidate.md,edit.json}.
  GATE     : ROLLOUT(candidate) over tasks/holdout (fresh subagents); `ledger.py record --split holdout`;
             `ledger.py gate` decides. accept→skill/v(K+1).md & update current.md; reject→append memory/rejected-edits.md.
  MEMORY   : slow update — established rules need accumulated evidence to be overturned.
FINALIZE : emit per output_mode (overwrite w/ v0 backup, or save-as-new <skill>-opt/); write report.md.
```

## Disciplines (Non-Negotiable)

- **Frozen target via fresh subagent** — each rollout subagent receives only `{skill text, task}`; no
  contamination, no self-grading.
- **Gate only on held-out** — never use train scores for acceptance decisions.
- **Deterministic gate decision** — `scripts/ledger.py gate` does arithmetic on `ledger.csv`; an LLM
  never decides accept/reject.
- **Edits bounded by `edit_budget`** — caps ops and net words per iteration (the "textual learning
  rate"); prevents catastrophic overwrites.
- **Consult `memory/rejected-edits.md` before every edit proposal** — do not re-propose known-bad
  edits without new evidence.

## Run Directory Layout

```
.skill-opt/runs/<skill>-<n>/
  config.yml
  skill/          v0.md  v1.md ...  current.md
  tasks/          train/  holdout/  suite.json
  rollouts/       iter-NN/task-MM/  trajectory.md  score.json
  candidates/     iter-NN/          candidate.md   edit.json
  memory/         rejected-edits.md  accepted-log.md
  ledger.csv      (source of truth; columns: iter, kind, version, split, mean_score, n, decision)
  report.md
```

Each subagent writes to a unique leaf path — parallel writes never collide.

## Resume

Re-invoke on an existing run directory. Read `ledger.csv` to find the last completed phase, then
continue. No double-work: every phase appends to `ledger.csv` before proceeding.

## Reference Docs

- `references/loop.md` — phase mechanics, defaults, edit-budget enforcement, gate margin, memory/slow-update policy, parallelism and edit_panel
- `references/fidelity.md` — SkillOpt correspondence map (five mechanisms, any deviations justified)
- `references/feedback-sources.md` — the 4 signal modes: how Setup builds the suite and how Judge scores per mode
- `references/rubrics.md` — drafting task suites and scoring rubrics; programmatic vs LLM-judge; judge calibration
