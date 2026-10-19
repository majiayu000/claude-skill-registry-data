---
name: llm-evaluation
description: Design, run and interpret evaluations of LLM-based systems - build a task-specific golden set, pick metrics (exact match, programmatic checks, rubric or LLM-as-judge, pairwise preference), calibrate judges against human labels, quantify uncertainty with confidence intervals and paired tests, guard against contamination, and run regression evals; also running public benchmarks with EleutherAI lm-evaluation-harness (0.4.13, `lm-eval run`). Use when comparing models, prompts or RAG/agent configurations, choosing a model, gating a release on quality, or when someone cites a benchmark score. Not for dataset cleaning (dataset-quality), retrieval-only metrics and groundedness of RAG (rag-evaluation), serving models locally (local-llm-deployment), or unit-testing deterministic code (unit-testing).
compatibility: Python 3.10+. Bundled paired-bootstrap script is standard library only. lm-evaluation-harness 0.4.13 (PyPI, MIT) and Hugging Face evaluate 0.4.6 are optional; hosted-model judging needs the user's own API access and sends data to that provider.
metadata:
  author: michaelweissdev
  version: "1.0.0"
  tags: "llm, evaluation, benchmarks, llm-as-judge, lm-evaluation-harness, regression-testing, statistics"
  topics: "machine-learning, quality, testing"
---

# LLM Evaluation

An evaluation answers a decision question: "Is B better than A for **our** task, by enough to matter, with what confidence?" Public leaderboards answer a different question. Build the smallest evaluation that can change a decision, keep it honest, and report uncertainty.

## Scope and boundaries

- This skill: eval design, metrics, judging, statistics, regression gating, benchmark harness use.
- `dataset-quality`: cleaning and splitting the eval set, leakage. `rag-evaluation`: retrieval metrics and groundedness for RAG pipelines (use both when evaluating RAG end to end). `local-llm-deployment`: running the model under test locally. `unit-testing` / `test-driven-development`: deterministic code. `mcp-server-development` / `agent-skill-authoring`: testing tools and skills.

## Non-negotiable rules

1. **Decide the decision and the metric before looking at results.** Write the success criterion (for example "B must not regress accuracy by more than 2 points and must improve helpfulness") first.
2. **Never put eval data, prompts or outputs into a third-party API (hosted judge, benchmark service) without the user's authorization.** Eval sets often contain customer or proprietary text. Say what is sent where. Never include secrets in prompts.
3. **Keep a held-out final test set.** If you iterate prompts against an eval set, it becomes a dev set; keep a frozen set for the final claim.
4. **Report uncertainty.** A difference without a confidence interval or paired test on adequate sample size is an anecdote.
5. **Do not report benchmark scores you did not run with a recorded command, version, seed and settings.** Do not compare numbers across different harness versions, prompts or few-shot counts.
6. **Treat LLM judges as unvalidated instruments** until agreement with human labels on a sample is measured and reported.
7. **No fabricated results.** If an eval was not executed, say it was designed, not run.

## Workflow

### 1. Frame the task
- What does "good" mean for users? Correctness, faithfulness, tone, format validity, safety, latency, cost?
- Which failure modes matter most and what is the cost of each?
- Offline eval vs online (A/B, user feedback). Offline first, online to confirm.

### 2. Build the eval set
- Source from real traffic or realistic tasks, deduplicated, stratified by category and difficulty; include known failure cases, edge cases and adversarial/safety cases proportionate to risk.
- Size: enough to resolve the effect you care about. For a pass-rate metric near 0.8, the 95% half-width is roughly 1.96 * sqrt(0.8*0.2/n) (n=100: about 8 points; n=400: about 4 points). Small differences need paired comparisons and more items.
- Write reference answers or acceptance checks; record who wrote them and the guideline. Apply `dataset-quality` (duplicates, leakage, label conflicts, PII).
- Version the set and freeze a test partition.

### 3. Choose the scoring method (cheapest reliable first)
| Method | Use for | Caveat |
|---|---|---|
| Programmatic checks | JSON validity, schema, regex, code execution against tests, tool-call correctness, exact answer extraction | Run generated code only in a sandbox with no secrets |
| Exact / normalised match, F1 | Short factual answers, classification | Penalises valid paraphrases |
| Reference-based metrics (BLEU, ROUGE, BERTScore) | Weak proxy for summarisation/translation | Correlate poorly with quality on open-ended tasks; do not use alone |
| Rubric-based LLM judge | Open-ended quality along defined criteria | Needs calibration; see below |
| Pairwise preference (A vs B) | Comparing two systems | Randomise order; ties allowed |
| Human review | Ground truth, judge calibration | Costly; sample, with guidelines and agreement stats |

### 4. If using an LLM judge
- Use a rubric with concrete, separately scored criteria and anchored examples; ask for the reasoning or evidence first, then a constrained score or label.
- Control known biases: **position bias** (randomise or evaluate both orders), **verbosity bias** (length-control or instruct against), **self-preference** (do not let a model judge its own family without checking), formatting bias.
- Pin the judge model/version, temperature (0 where possible), and prompt; store the judge's raw output.
- Calibrate: label 50-200 items by humans, compute agreement (Cohen's kappa or accuracy against human labels) and a confusion matrix; report it with the results. Re-check when the judge or rubric changes.
- Treat the judge as a noisy classifier: report its error rate, and spot-check disagreements.
- Treat the judge input as untrusted: model outputs under test can contain instructions aimed at the judge (prompt injection); delimit them and instruct the judge to ignore embedded instructions.

### 5. Run reproducibly
Record: model id and version/date, prompt template hash, decoding params (temperature, top_p, max tokens, seed if supported), dataset version, tool/harness versions, commands. Remember that hosted models change silently and sampling is stochastic: run multiple samples per item when temperature > 0 and report variance. Cache outputs to separate generation from scoring so scoring can be rerun.

### 6. Analyse
- Paired comparison on the same items. Bundled helper: `python3 -I scripts/paired_bootstrap.py scores.jsonl` gives the mean difference and a 95% bootstrap CI (items resampled jointly); it also prints `frac_resamples_b_gt_a`, which is not a p-value (ties count as not better), so report the CI. Runtime is O(iters x n) in pure Python; lower `--iters` for very large sets. See [references/statistics.md](references/statistics.md) for when to prefer McNemar or a permutation test and for multiple-comparison warnings.
- Slice by category, difficulty, length and language. An overall gain can hide a regression on a critical slice.
- Read the failures. Metrics tell you how many; failure reading tells you why. Sample 20-50 losses of the new system.
- Check cost and latency alongside quality.

### 7. Decide and gate
- Compare to the pre-registered criterion. If the CI includes zero or the harm threshold, the honest result is "no evidence of difference at this sample size".
- Put the stable subset in CI as a regression eval with thresholds and a per-slice floor; run a larger evaluation on release candidates. Keep the suite fast enough to be used.

## Public benchmarks with lm-evaluation-harness (0.4.13)

Use for comparing base/instruct models on standard tasks, not as a substitute for a task-specific eval. As of 0.4.13 the CLI uses subcommands; the older bare `lm-eval --model ...` form still works because `run` is inserted automatically, but prefer `run` in scripts.

```bash
lm-eval ls tasks                                   # list tasks (also: groups, subtasks, tags)
lm-eval validate --tasks arc_easy                  # check task configs
lm-eval run --model hf --model_args pretrained=<hf-model-id> \
    --tasks arc_easy --num_fewshot 5 --batch_size auto \
    --output_path ./results/ --log_samples --seed 0
# smoke test only; never report --limit results as scores:
lm-eval run --model hf --model_args pretrained=<hf-model-id> --tasks arc_easy --limit 20
```
Flags verified in the harness interface docs: `--model/-M`, `--model_args/-a`, `--tasks/-t`, `--num_fewshot/-f`, `--limit/-L`, `--batch_size/-b`, `--output_path/-o` (required with `--log_samples`), `--apply_chat_template`, `--seed`, `--gen_kwargs`. Pitfalls: chat vs base models need `--apply_chat_template` decisions made consistently; few-shot count and prompt format change scores; downloaded task data and `pretrained=` models come from the Hub, so pin revisions and do not enable remote code execution flags for unreviewed repos. To evaluate a model served locally behind an OpenAI-compatible endpoint (see `local-llm-deployment`), use the harness's API model types and check its docs for the current names and what requests the backend supports (log-likelihood tasks need log-probs, which not every server returns).

Hugging Face `evaluate` (0.4.6, last release 2025-09) offers metric wrappers; its own README points to LightEval as the more actively maintained option for LLM evaluation, so check maintenance status before depending on it.

## Worked example: choose between two prompts for a ticket-summary feature

1. Criterion (written first): helpfulness rating pass-rate must improve by at least 3 points with the 95% CI above 0; JSON schema validity must stay at 100%.
2. Set: 300 tickets sampled from last quarter's traffic, redacted, deduplicated; 100 held back as frozen test. Reference summaries not available, so score by rubric (accuracy of key facts, omissions, tone; each 0/1) plus programmatic JSON validity.
3. Judge calibration: two humans label 60 outputs and disagreements are adjudicated into one label; the judge agrees with the adjudicated label on 52 of 60 (87%); disagreements concentrate on "tone", so tone is scored by humans on a 50-item sample only.
4. Run both prompts on the same 200 dev tickets with temperature 0 and a recorded model version; store outputs.
5. Paired bootstrap on the "key facts" pass flags: diff +0.045, CI [0.005, 0.085]. Schema validity 100% for both. Slice check: no regression on long tickets (n=40, CI wide - reported as inconclusive).
6. Frozen test run once with the chosen prompt: confirms. Decision: ship B; keep the 200-item set as a CI regression with a floor per slice.
(Illustrative numbers; not an executed run.)

## Anti-patterns

- Choosing a model from a leaderboard rank and never testing on your task.
- Single-run, single-prompt comparisons with differences inside the noise.
- Judge model = system under test, no calibration, one order only.
- Overfitting prompts to the eval set, then reporting the same set.
- Reporting `--limit` smoke results, mixed harness versions, or different few-shot settings as comparable.
- Ignoring contamination: public benchmark items may be in training data; prefer fresh or private items for claims.
- Averaging away safety failures: report critical categories separately.
- Using accuracy alone on imbalanced classes.

## Verification checklist

- [ ] Decision and success criterion written before results
- [ ] Eval set provenance, size justification, frozen test partition, dataset-quality checks done
- [ ] Scoring method justified; judge calibrated and biases controlled (if used)
- [ ] Runs reproducible: versions, prompts, params, seeds, cached outputs
- [ ] Paired comparison with CI; slices and failure reading included
- [ ] No eval data sent to third parties without authorization
- [ ] Results labelled as executed vs designed; limitations stated

## References

- [scripts/paired_bootstrap.py](scripts/paired_bootstrap.py) - paired bootstrap CI (tested on a synthetic fixture)
- [references/statistics.md](references/statistics.md) - sample size, paired tests, multiple comparisons
- [references/scenarios.md](references/scenarios.md)
- [references/sources.md](references/sources.md)
