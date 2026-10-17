---
name: eval-harness
description: Design and analyze controlled coding-agent experiments when comparing skills, prompts, models, or agent configurations using independently verified task outcomes.
license: MIT
metadata:
  source: affaan-m/everything-claude-code
  source-commit: 846ffb75da9a5f4e677d927af1ad4a1951652267
  revision-status: experimental-unbenchmarked
---

# Objective agent evaluation

Define the decision the experiment should support: a skill's benefit over the
same agent without it, a regression between revisions, or a model comparison.
Changing the model and skill simultaneously cannot isolate either effect.

## Define the experiment

- Choose tasks from real pinned issues, workflows, or independently authored
  user requirements. Record source provenance, environment, and task coverage.
- Define graders before reading the exact candidate instructions. Score actual
  behavior with executable acceptance checks, including relevant regressions.
  A function name, code pattern, plausible explanation, or agent self-report is
  not proof of correctness. Use blinded review only for criteria that need it.
- Keep development cases separate from final holdouts. Any case used to tune
  instructions becomes a development case, even if originally called a holdout.
- Run the original input through the grader to prove the task's failing behavior;
  check a known valid outcome and plausible wrong outcomes to test the grader.
  Keep oracle artifacts outside the agent's accessible task environment.

## Execute matched trials

Use fresh workspaces and sessions with the same task input, tool permissions,
model version, reasoning effort, limits, and dependency versions. Declare which
instructions each condition loads; record effective configuration and instruction
hashes. Development history, memory, prior patches, and unrelated skills can
contaminate a baseline. If isolation cannot be verified, label that limitation.

Rotate condition order across repeated tasks. Preserve each attempt's transcript,
patch, grader output, exit status, actual usage, and elapsed time. Record failures,
timeouts, environment errors, and unavailable measurements rather than deleting
them or substituting zero. Validate inputs and grader files against their frozen
hashes after execution, and detect changes outside the permitted patch scope.

## Analyze and iterate

Report the number of planned, attempted, validly graded, successful, and failed
trials for each condition. Distinguish task failure from harness failure. Show
paired task results and uncertainty before claiming superiority; disclose
category coverage, exclusions, repeat count, and any contaminated tasks.

For one independent attempt per task, report successes / evaluated tasks as the
observed pass rate. For best-of-k sampling, retain all n samples and use the
estimator `1 - C(n-c, k) / C(n, k)` with `n >= k`, where c is successful samples.
Do not relabel retry success or a selected best attempt as pass@1. Report the
budget and selection procedure; dependent adaptive retries are a different setup.

Compare quality first, then tokens, latency, tool use, and cost for comparable
outcomes. Do not infer speed gains from host-load noise or efficiency from shorter
answers alone. Keep package readiness and harness smoke checks separate from
agent task performance.

Revise against demonstrated development failures, rerun affected matched cases
and regressions, then evaluate untouched holdouts. Preserve negative results and
version each iteration. If measured gains are absent, report that outcome.
