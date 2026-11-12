---
name: ak-deep-swe
description: "Benchmark a coding model on DeepSWE through Pier and OpenRouter."
when_to_use: "Invoke for a costed external run, not repository-local optimization."
category: workflow
keywords: [benchmark, deepswe, pier, openrouter, evaluation]
license: Proprietary; includes MIT-licensed third-party material, see LICENSE.txt
argument-hint: "<OpenRouter model slug>"
metadata:
  author: agentkit
  version: "1.0.1"
  upstream: "Pinned MIT source archive: run-deep-swe@ce70edaa26247b84c2b9491a0cdb4964f65cf3a5"
---

# DeepSWE Benchmark

Run an independent coding-agent evaluation on the DeepSWE benchmark through
Pier. This skill handles benchmark setup and reporting. It does not evaluate a
repository metric or authorize model spend without the user's confirmation.

## Guardrails

- First confirm that uv, git, Docker, and the Docker daemon are available.
- Confirm OPENROUTER_API_KEY is set without printing its value. If it is absent,
  stop and ask the user to configure it.
- Never echo, persist, commit, or place the key in a command, report, prompt,
  or benchmark artifact.
- Run one task before a subset. Get explicit user confirmation before a full
  corpus run because it consumes time and model tokens.

## Setup

    git clone https://github.com/datacurve-ai/deep-swe
    uv tool install datacurve-pier
    pier --help
    pier run --help

Run the commands below from the directory that contains the cloned deep-swe
folder. If you change into deep-swe instead, use tasks or tasks/<task-id> as
the -p value.

Enumerate the cloned task roster and record its revision/count. Confirm current
flags and task paths with installed help before running because this toolchain changes:
https://github.com/datacurve-ai/deep-swe
https://pypi.org/project/datacurve-pier/
https://deepswe.datacurve.ai/

## Run Safely

1. Verify the exact OpenRouter model slug at openrouter.ai/models.
2. Run a single task first. The current native model form is:

       pier run -p deep-swe/tasks/<task-id> --agent mini-swe-agent \
         --model openrouter/<vendor/model>

3. For a deterministic subset, use the installed help to confirm the task-count
   and sample-seed flags, then run a small fixed sample:

       pier run -p deep-swe/tasks --agent mini-swe-agent \
         --model openrouter/<vendor/model> --n-tasks 10 --sample-seed 0
4. Use a separate model-class route only when the installed Pier help explicitly
   documents it; do not guess a version-specific flag.
5. Before a full corpus run, present the exact command, expected cost exposure,
   and stop condition. Continue only after explicit confirmation.

## Inspect and Report

Inspect the generated job directory with the current Pier commands. When the
installed version provides them, use pier view, pier analyze, and pier critique
to inspect the result. Report the exact command, Pier version, task count, model
slug, effective model/effort settings, prompt hash, attempted/completed/passed counts,
score or reward, cost when available, and blockers. Record cache telemetry only
when exposed; unknown is not zero. Compare configurations on a fixed task split,
keep held-out tasks separate from tuning, and distinguish these observed runs
from provider-published benchmark scores. Do not submit results
or contact a leaderboard without the user's request.

## Failure Handling

- For authentication failures, stop and have the user correct their environment.
- For provider or model mapping failures, verify the slug and consult current
  Pier help before changing the command.
- For unknown flags, do not retry a guessed syntax; inspect help first.
- Use ak-loop for iterative optimization of a metric in the user’s own
  repository rather than an external model benchmark.
