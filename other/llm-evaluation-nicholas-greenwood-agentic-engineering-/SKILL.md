---
name: llm-evaluation
description: use when evaluating LLMs, prompts or workflows
---

evaluate the production workflow with frozen inputs and saved evidence

use paired arms for comparisons; for a single configuration, apply this workflow against frozen references, omitting comparator and pairing requirements

## choose the runner

search the repository for maintained evaluation runners and current workflow guidance before building another harness; treat archived evaluations as historical evidence

inspect the matching runner's executable entry point, fixtures and scoring, and read any associated protocol before invoking it. reuse or adapt it when it fits; old budgets and release gates do not authorise a new run

## freeze before running

save a short manifest and its artifacts in the task's evidence directory:

- question, evaluated configuration(s), baseline/candidate comparison when applicable, scoring rubric, analysis method, uncertainty handling and decision rule/threshold when applicable
- exact case ids, provenance, references/labels, target cohort, selection criteria/method and repetitions; label captured, synthetic and reconstructed inputs distinctly
- original messages (including judge prompts) with roles, personas and formatting intact, plus tool descriptions, response schemas and source snapshots; save intentional prompt changes separately
- commit and input/prompt/rubric hashes; include the evaluated patch for a dirty checkout
- model/provider, reasoning, sampling/token limits, tool/search settings, caching and retries per arm and judge; record effective settings where available and mark unknowns
- total budget for every arm, retries and judging, within current authorisation

done when each arm can be reconstructed from saved evidence without guessing or fetching mutable inputs

## run and score

- give each arm the same frozen cases and starting context; vary only the factor being evaluated and record unavoidable differences
- preserve repetitions and balance arm order where relevant to expose baseline variability and time effects
- retain requests, responses, tool traces, errors, usage, cost and latency keyed by `(case id, arm, repetition)`
- score against the frozen rubric and saved sources/labels; model agreement alone is not factual correctness
- when using model judges, blind arm identities and balance answer order; audit disputed decisions against sources or human labels

## reconcile and report

- report selected, attempted, returned and scored counts per arm, expected/observed `(case id, arm, repetition)` rows, and duplicate, missing, failed or empty rows
- keep failures and missing results visible in the planned denominator; state quality denominators separately rather than silently dropping rows
- compare aligned cases under the same rubric/settings except the evaluated factor; label exploratory subsets separately. incomplete coverage cannot establish a full-cohort win or pass its release gate
- aggregate repetitions within each case before estimating uncertainty, using paired case differences for comparisons; retain per-case/group regressions and hard failures
- link the manifest, raw evidence and scored outcomes; report paired differences, uncertainty/limitations, baseline variability and cost/latency with actual denominators
- separate observed results from inference and mark incomplete or inconclusive decisions explicitly

done when every conclusion traces to saved case ids, settings and scoring evidence, and follows any frozen decision rule
