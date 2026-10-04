---
name: skill-eval-optimizer
description: Test, evaluate, harden, and optimize Codex skills from SKILL.md folders, run traces, eval prompts, failure reports, and user feedback. Use when Codex needs to validate skill structure, check trigger behavior, build codex exec JSONL evals, compare before/after skill behavior, diagnose skill failures, improve skill descriptions or bundled resources, test or add native goal-mode contracts, or close optional API/MCP setup loops through external-api-onboarding.
---

# Skill Eval Optimizer

## Overview

Use this skill to turn skill maintenance from "it seems better" into an evidence loop: static validation, trigger tests, trace capture, deterministic grading, targeted edits, and forward-testing.

The base workflow requires no external API key. If the eval depends on live web search, provider docs, GitHub/Hugging Face/Kaggle evidence, browser automation, or remote MCP access, invoke `$external-api-onboarding` and follow `references/external-api-closure.md` before making live calls.

## Goal Mode

Use native goal mode when the user asks Codex to carry a skill improvement through repeated validation, resume a multi-case eval, or add and test goal-mode support for another skill. Goal mode is useful only when the work has a durable target, evidence artifacts, and a clear completion or blocked condition.

Good goal objectives are narrow and evidence-based:

- "Harden `<skill-name>` until static validation and the agreed eval pack pass."
- "Add goal-mode guidance to `<skill-name>` and prove it with one positive and one negative eval."
- "Diagnose this skill failure from traces, patch the smallest contract issue, and rerun the failing case."

When goal tools are active:

1. Create or update `evals/skill-eval/<skill-name>/goal-status.md` unless the repo already has a stronger status convention.
2. Record the objective, target skill path, eval cases, current phase, last validation command, artifacts, residual risks, and next action.
3. Work in bounded loops: validate, run or inspect the smallest relevant eval, patch only evidence-backed issues, rerun, and update the status file.
4. Mark complete only after the requested validation evidence exists and the final report names the exact commands, traces, artifacts, and remaining risks.
5. Mark blocked only after the same external blocker repeats across bounded attempts, such as missing credentials, unavailable provider access, unavailable subagent/runtime support, or a user confirmation gate.

Do not use goal mode to skip human gates, hide failed eval cases, or declare a skill stable from prose review alone.

## Workflow

1. Define the target.
   - Identify the skill directory, expected users, trigger examples, negative examples, bundled scripts, references, and output contract.
   - Separate structure problems, trigger problems, execution problems, output-quality problems, and external-provider problems.
   - If the task is goal-mode work, define the objective shape, state artifact, completion criteria, blocked criteria, and human gates before editing.
   - Preserve user changes. Do not rewrite unrelated skills or docs while improving one skill.

2. Run static validation.
   - Run the canonical validator when available:

```powershell
python C:\Users\Administrator\.codex\skills\.system\skill-creator\scripts\quick_validate.py <skill-dir>
```

   - Also run the bundled lightweight check:

```powershell
python skills\skill-eval-optimizer\scripts\skill_eval_harness.py static-check <skill-dir>
```

   - Fix frontmatter, stale scaffold markers, `agents/openai.yaml`, broken references, placeholder examples, unsafe secret patterns, and missing smoke-test guidance before deeper evals.
   - If the skill claims native goal-mode support, run:

```powershell
python skills\skill-eval-optimizer\scripts\skill_eval_harness.py goal-check <skill-dir>
```

3. Build an eval pack.
   - Use realistic user prompts, not only direct `$skill-name` invocations.
   - Include negative controls for adjacent tasks that should not trigger the skill.
   - Keep the first pack small: usually 10-20 prompts are enough to expose regressions.

```powershell
python skills\skill-eval-optimizer\scripts\skill_eval_harness.py init-eval `
  --skill-dir <skill-dir> `
  --out-dir evals\skill-eval\<skill-name>
```

4. Run behavior tests.
   - Prefer isolated scratch workspaces or disposable branches.
   - Use the least permission that still lets the target task run.
   - For automated runs, capture JSONL traces:

```powershell
codex exec --json --full-auto "Use $<skill-name> to <realistic task>" > evals\skill-eval\<skill-name>\artifacts\case-01.jsonl
```

   - If the task requires authenticated providers, paid APIs, OAuth, or browser login, pause and use `$external-api-onboarding` first.

5. Grade the run.
   - Use deterministic checks first: expected commands, generated files, exit status, repo cleanliness, unwanted files, loop count, token use, and artifacts.
   - Summarize a trace:

```powershell
python skills\skill-eval-optimizer\scripts\skill_eval_harness.py summarize-trace `
  evals\skill-eval\<skill-name>\artifacts\case-01.jsonl `
  --require-command quick_validate.py `
  --require-file <expected-output>
```

   - For qualitative output, run a read-only rubric pass with `codex exec --output-schema` using the generated `style-rubric.schema.json`.

6. Optimize with evidence.
   - Trigger misses: edit `description` first. Front-load the scenario, target artifacts, and negative boundaries.
   - Wrong process: tighten the workflow, add required commands, or move fragile logic into scripts.
   - Bad output quality: add a rubric, example, reference file, or final evidence contract.
   - External-provider failures: move credentials and login setup into an `$external-api-onboarding` route; never hide setup assumptions inside the skill.
   - Rerun only the smallest eval set needed to prove the change, then run a wider set before declaring the skill stable.

7. Forward-test when useful.
   - If native subagents are available and the task is safe, use fresh subagents with minimal context.
   - Prompt them as normal users: `Use $skill-name at <path> to solve <task>`.
   - Do not leak your diagnosis, intended fix, or expected answer unless the test explicitly requires it.

8. Close with an evidence report.
   - Report the skill inspected, files changed, validation commands, eval prompts, trace/artifact paths, before/after findings, remaining risks, and whether a restart is needed for discovery.
   - If goal mode was active, include the final `goal-status.md` path and state whether the goal is complete, blocked, or intentionally left open for human review.

## External API Closure

Read `references/external-api-closure.md` whenever a skill eval depends on an external provider, remote MCP server, provider CLI login, or browser-authenticated surface.

Default rule: no secret in chat, no committed `.env`, no copied cookie or token values, no paid or write-capable request without explicit user approval.

## References

- `references/checklist.md`: compact static, trigger, execution, output, and closure checklist.
- `references/eval-loop.md`: eval pack structure, goal-mode status layout, `codex exec --json` trace pattern, deterministic checks, and rubric grading.
- `references/external-api-closure.md`: how to invoke `$external-api-onboarding` for optional providers and smoke tests.

## Output Shape

Use this structure unless the user asks for another format:

```text
Summary
- Target skill:
- Evidence used:
- Main diagnosis:
- Highest-impact fix:

Validation
| Check | Result | Evidence |

Eval Results
| Case | Prompt type | Pass | Evidence | Notes |

Optimizations
1. Trigger/description
2. Workflow/body
3. Scripts/resources
4. External API/MCP closure

Goal Mode
- Goal status:
- Completion criteria:
- Blocked criteria:
- Human gates:

Residual Risk
- ...
```
