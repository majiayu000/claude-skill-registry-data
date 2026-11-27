---
name: rubric-tune
description: >-
  Tune a classification rubric or taxonomy when you have labeled examples and need bounded, semi-supervised refinement with a blind holdout gate. Explicit invocation only. Use rubric-judge for one-shot classification and hoa-practice-mine for session/memory mining.
disable-model-invocation: true
metadata:
  revision: "1"
  areas: "software-development,work-management"
  targets: "runtime-agnostic"
  summary: "refine rubrics with bounded training trials, a blind promotion gate, and human labeling"
  summary_zh: "用有界训练试验、盲测晋升门槛和人工标注迭代分类准则"
  kind: "entry"
---

# rubric-tune

Produce a promotion diff backed by training comparisons, locked synthetic anchors,
and a blind holdout. The human decides whether to promote and how to label new data.

## Gates

- **Authorize the run.** Before starting, confirm the operator's approved endpoint,
  data scope (including what may be sent), budget, and scratch `--out-dir`. Explicit
  invocation does not authorize data transfer. Send only in-scope, redacted inputs.
- **Keep the holdout blind.** A custodian with separate file access runs `split` and
  `eval-holdout`. Give the rubric-editing agent only training data, anchors, and
  holdout aggregates. Keep the original labeled corpus and holdout outside the
  editor's readable directories, tool logs, and transcripts. Do not start a blind
  run if editor and evaluator cannot be isolated. The endpoint must be authorized
  for holdout text; no model response text may be returned to the editor.
- **Bound the unattended loop.** Set `max_iters` (default 8), `max_wall_minutes`
  (default 30), and `patience` (default 3 consecutive attempts without acceptance).
  Use a monotonic wall-clock deadline, including model calls. Cap each command by
  the remaining time and terminate an in-flight command at the deadline. Stop at
  the first limit or endpoint failure; reset patience only on an accepted step.
- **Lock both promotion gates.** Require zero anchor false negatives, false
  positives, and refusals, **and** strictly higher blind holdout `f_beta` than the
  original baseline. Keep the dataset split, anchors, `--beta`, `--threshold`,
  and endpoint fixed. Never select edits using holdout feedback.
- **Keep writes and labels separate.** Write only under an external or verified
  gitignored scratch `--out-dir`; never edit the production rubric. Unlabeled
  items may be sampled only after the loop. Never use model outputs as labels
  or include unlabeled items in training scores, loss, or candidate selection.

## Workflow

Use the Bash `hoa` function below to run the packaged CLI via `uvx`. In a local
checkout use `uv run hoa ...` instead, or omit the function if `hoa` is installed.
Replace the example paths with the authorized inputs and scratch directories.
Only if a command fails, read [references/troubleshooting.md](references/troubleshooting.md).

```bash
hoa() { uvx --from git+https://github.com/wxxb789/hoa hoa "$@"; }
```

1. **Freeze the inputs.** Save a scratch copy of the original rubric for the
   eventual promotion diff. Lock a separate synthetic anchor file with positive
   and negative examples. Give the custodian the labeled JSONL (`id`, `text`,
   `expected`: all booleans or all string labels). Deduplicate semantically
   equivalent items before splitting. The custodian runs:

   ```bash
   hoa hillclimb split --input corpus.jsonl --out-dir CUSTODIAN_SCRATCH --train-out train.jsonl --holdout-out holdout.jsonl
   ```

   The custodian transfers only `train.jsonl` to the editor. If a separate locked
   split already exists, use it instead of splitting again. Use `--stage` for
   stage-based rubrics; when comparing different stages, also supply
   `--baseline-stage` and `--candidate-stage` as needed.

2. **Iterate on training only.** Evaluate the current best in train mode; read
   the bounded `error_samples` and `confusion_pairs`. Make one rubric change
   per attempt and record its hypothesis. Use a fresh `--best-out` name per
   step. Use the resulting scratch best as the next baseline only if accepted;
   a reverted step preserves the previous best. Repeat until a bound is reached.

   ```bash
   hoa hillclimb eval --rubric CURRENT --dataset SCRATCH/train.jsonl --mode train --anchors SCRATCH/anchors.jsonl
   hoa hillclimb step --baseline CURRENT --candidate CANDIDATE --train SCRATCH/train.jsonl --anchors SCRATCH/anchors.jsonl --out-dir SCRATCH --best-out BEST_FOR_THIS_ITERATION --ledger rubric-ledger.jsonl --note HYPOTHESIS
   ```

   `step` compares only train `f_beta`, with the locked anchor gate. A reversion
   is a normal result, not an endpoint failure. For interpreting metrics and
   deciding whether a taxonomy overlap merits a merge, read
   [references/methodology.md](references/methodology.md).

3. **Run the blind promotion gate once.** Freeze the finalist; have the custodian
   evaluate the original and the finalist separately with the same holdout and
   endpoint. The original shows the reference `f_beta`; the finalist must also
   pass the locked anchor gate.

   ```bash
   hoa hillclimb eval-holdout --rubric ORIGINAL --dataset HOLDOUT
   hoa hillclimb eval-holdout --rubric FINALIST --dataset HOLDOUT --anchors LOCKED_ANCHORS
   ```

   The custodian shares the metrics and gate exit status only (`0` passed,
   `1` anchor failure, `2` evaluation failure). No item-level results are emitted
   by `eval-holdout` or `eval --mode holdout`. If either promotion condition fails,
   report no promotion and do not tune against or reuse this holdout for a new
   finalist. Otherwise produce a diff from original to finalist with training
   and holdout scores, anchor result, and ledger path. Do not apply it.

4. **Queue human labels.** If the operator supplied a separate unlabeled JSONL
   (`id`, `text`, no `expected`), run `sample` after the loop and save its JSON
   under `SCRATCH`. Use the original and the selected scratch candidate, marked
   unpromoted unless separately approved. The packet prioritizes disagreements,
   overlapping labels, and escape-hatch cases; its scores are not labels. Let
   the operator label the items and decide which to add to a future train set.

   ```bash
   hoa hillclimb sample --baseline ORIGINAL --candidate FINALIST --pool UNLABELED > SCRATCH/label-queue.json
   ```

## Configuration

Use [references/configuration.md](references/configuration.md) for lookup paths.
After the skill-specific lookup, each unset key falls back to `RUBRIC_HILLCLIMB_*` (legacy alias), `RUBRIC_JUDGE_*`, `GHC_DECISIONS_*`,
then `EVALS_*`, using the corresponding suffix; other skills' config files are
not read. Use the same backend throughout the run. `--api chat-completions`
selects the fallback explicitly if `/v1/decisions` is unavailable; the fallback
supplies hard answers, not calibrated choice distributions.

| Key | CLI flag | Environment variable | Default |
|---|---|---|---|
| `base_url` | `--base-url` | `RUBRIC_TUNE_BASE_URL` | None (required for model calls) |
| `model` | `--model` | `RUBRIC_TUNE_MODEL` | None (required for model calls) |
| `api` | `--api` | `RUBRIC_TUNE_API` | `decisions` (`decisions` or `chat-completions`) |
| `workers` | `--workers` | `RUBRIC_TUNE_WORKERS` | `16` |
| `api_key` | — | `RUBRIC_TUNE_API_KEY` | `dummy` |

## Additional resources

- [agents/openai.yaml](agents/openai.yaml) — explicit-only invocation policy for Codex.
- [references/methodology.md](references/methodology.md) — interpreting metrics and taxonomy overlap.
- [references/configuration.md](references/configuration.md) — configuration lookup order and file path.
- [references/troubleshooting.md](references/troubleshooting.md) — read only when a CLI command fails.
