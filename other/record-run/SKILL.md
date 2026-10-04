---
name: record-run
description: Log an experiment run (training and/or eval) using this repo's manifest + notes + generated-index convention so results from different mechanisms and collaborators stay apples-to-apples. Use whenever a run finishes, before considering the work done, or when asked to compare past runs.
---

# Recording runs

**Every real run gets logged — pilot, sweep, failed or not.** Skip only throwaway smoke
tests (n < 10, just checking code runs); delete their output. A run on real data at a
meaningful n that produces a number anyone might compare against is a real run.

## Steps

1. **Save the record** with `RunRecord`:

   ```python
   from latentreasoning.runlog.manifest import RunRecord, ModelInfo, DatasetInfo, new_run_id
   from latentreasoning.utils import set_seed

   seed = set_seed(42)                       # before any training/generation
   ...
   record = RunRecord(
       run_id=new_run_id("filler_tokens", "budget-sweep-32"),
       mechanism="filler_tokens",            # latentreasoning.runlog.manifest.MECHANISMS, or "baseline_*"
       stage="pilot",                        # "smoke_test" | "pilot" | "full_run"
       model=ModelInfo(backbone="gpt2-edited", checkpoint="results/<run_id>/ckpt", n_params=124_439_808),
       dataset=DatasetInfo(name="gsm8k-aug", split="test", n_examples=200, seed=0),
       metrics={"final_answer_accuracy": 0.31, "unparseable_rate": 0.02, "compute_steps": 32,
                "extra": {"cot_tokens": 41}},  # mechanism-specific stuff goes under "extra"
       hyperparams={"lr": 5e-5, "epochs": 3, "batch_size": 16, "filler_token": "."},
       seed=seed,
       hardware="RunPod A40 x1",
       notes="one line on what this run asks",
   )
   record.save(predictions=eval_result.records)   # -> results/<run_id>/{manifest.json, predictions.jsonl, notes.md}
   ```

   Always pass `predictions` — per-example outputs are the error-analysis and
   decoder-training data later. Also drop `trainer.state.log_history` into
   `results/<run_id>/train_log.json` if you trained.

2. **Fill in `results/<run_id>/notes.md`** — `save()` created a template with the numbers
   pre-filled. Goal, command, interpretation, gotchas, caveats, next. A number without
   the story is hard to trust later.

3. **Regenerate the index:** `uv run python scripts/rebuild_index.py` rewrites
   `results/README.md` and `EXPERIMENTS.md`. Never hand-edit those two.

4. **Commit** `results/<run_id>/` + the two generated files. Checkpoints and other large
   artifacts stay on the pod volume (`.gitignore` drops everything in `results/<run_id>/`
   except manifest / notes / predictions / train_log); reference them by path in
   `model.checkpoint`.

Never rewrite a past run's numbers or notes. If it turns out flawed, append a correction
to its `notes.md` (or log a follow-up run) and rebuild.

## Merge conflicts

Run directories never conflict. `results/README.md` and `EXPERIMENTS.md` will — take
either side, rerun `rebuild_index.py`, commit. `tests/test_index.py` fails if they're stale.

## Comparing runs — the compute-budget rule

`metrics["compute_steps"]` is the budget knob: filler tokens emitted / loop iterations r /
continuous-thought tokens. `explicit_cot` is unbudgeted; it reports
`metrics["extra"]["cot_tokens"]` instead.

**Only compare `final_answer_accuracy` when `compute_steps`, `dataset.split`,
`dataset.n_examples`, `dataset.seed`, and `seed` match.** 32 filler tokens vs r=32 loops
is not automatically matched — say in `notes.md` what you matched on (extra forward
passes, FLOPs, ...) before quoting one against the other.

```python
from latentreasoning.runlog.manifest import load_all_runs
runs = [r for r in load_all_runs() if r["dataset"]["split"] == "test"
        and r["dataset"]["n_examples"] == 200 and r["metrics"].get("compute_steps") == 32]
```
Shell: `jq '[.mechanism, .metrics.final_answer_accuracy, .metrics.compute_steps]' results/*/manifest.json`

Runs on unmerged branches aren't in `main`'s index — check open branches before
concluding something wasn't tried.

## Canonical metric keys

`final_answer_accuracy`, `unparseable_rate` (don't let a high one hide inside a mediocre
accuracy), `compute_steps`, `train_loss`, `eval_loss`, `sec_per_example`. Anything else
under `metrics["extra"]`.

Reserved for the October milestones (`PROPOSAL.md` metrics) -- use these spellings when
you get there, and define exactly how you computed it in `notes.md`:
`decoding_accuracy`, `early_termination_necessity`, `intervention_accuracy`,
`transplant_success`. Note `early_termination_necessity` (truncate the scratchpad at
inference on a full-budget model) is a different measurement from a `compute_steps`
sweep (train + eval at each budget) -- don't quote one as the other.
