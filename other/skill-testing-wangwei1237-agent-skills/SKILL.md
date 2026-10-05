---
name: skill-testing
description: Test Agent Skills from tests/skill_cases.yaml files. Use when validating whether a Skill triggers correctly, produces a dry-run plan, satisfies output contracts, handles edge/failure cases, or when asked to run Skill Test cases, judge Agent responses against YAML expectations, or produce Skill test reports.
---

# Skill Testing

Use this skill to evaluate another Skill from its `tests/skill_cases.yaml` file. The test target is Skill behavior, not real business execution. Keep every case in dry-run mode unless the YAML explicitly says otherwise.

Default behavior is end-to-end. A user request to test a Skill or run a `tests/skill_cases.yaml` file authorizes isolated sub-agent capture for the test cases: generate dry-run prompts, run each rewritten prompt in a fresh isolated sub-agent, capture the actual dry-run response, format it, score it, and return the final Skill Test Report in the same turn.

## Inputs

Accept either:

- A Skill directory containing `SKILL.md` and `tests/skill_cases.yaml`.
- A direct path to a `skill_cases.yaml` file.
- A YAML case file plus Agent responses captured from a separate harness.

The default response directory is the target Skill's `tests/tmp/response/` directory. For example, `skills/my-skill/tests/skill_cases.yaml` uses `skills/my-skill/tests/tmp/response/`.

If the user provides a response directory explicitly, consume those response files instead of generating new responses. Otherwise, create or replace response files in the default response directory with sub-agent outputs and continue to final scoring.

## Workflow

1. Load the YAML test file.
2. Validate required top-level fields: `version`, `skill.name`, `defaults.mode`, `defaults.execution`, and `cases`.
3. Validate every case has `id`, `type`, `title`, `query`, `inputs.files`, `inputs.context`, `expected.skill`, `expected.must_include`, `expected.must_not_include`, `expected.artifacts`, `expected.routing`, and `assertions`.
4. Build one dry-run prompt per case from the original `query`.
5. Unless an explicit response directory was provided, dispatch each rewritten prompt to a fresh sub-agent in dry-run mode and capture the sub-agent's final response text. The sub-agent must receive only the rewritten prompt plus the dry-run restriction, not the YAML expected fields, assertions, scoring rubric, or report from other cases.
6. Save the raw response under `<target-skill>/tests/tmp/raw_response/<case_id>.md`.
7. Format the raw response into the Skill Test response contract and save one scorer-facing response file per case in `<target-skill>/tests/tmp/response/<case_id>.md`.
8. Run the scorer against the formatted response directory.
9. Output a deterministic final report with case-level status and an overall result.

Never execute the target Skill's real workflow during Skill testing. Do not run tools, mutate target Skill files, call external services, or claim that execution succeeded unless the test harness provides evidence. Writing response files under `tests/tmp/response/` and optional report files under `tests/tmp/` is allowed because they are test artifacts.

## Sub-Agent Response Capture

When no explicit response directory is provided, capture responses this way:

1. Use the rewritten prompt exactly as the case input.
2. Spawn a fresh sub-agent for that single case. Do not fork the full testing context unless the platform requires it; the sub-agent should not see `expected`, `assertions`, scoring rules, or other case responses.
3. Give the sub-agent only the rewritten prompt and an instruction to return only its dry-run answer as plain text.
4. Capture the sub-agent's final message verbatim as the raw response. Do not edit this raw evidence.
5. Respect the rewritten prompt's dry-run boundary: the sub-agent must not call tools, mutate files, call external services, or perform the original business task.
6. Save the raw response as UTF-8 Markdown named `<case_id>.md` under `tests/tmp/raw_response/`.
7. Produce a separate formatted response for scoring under `tests/tmp/response/`. Formatting is required even when the raw response is plain prose.
8. Preserve evidence integrity: the formatted response may normalize structure, extract fields, translate obvious synonyms, and quote or summarize the raw response, but it must not invent facts, add missing workflow steps, claim the sub-agent selected a skill it did not mention, or hide dry-run violations.

## Response Formatting Contract

After receiving a raw sub-agent response, rewrite it into a stable Markdown response before scoring. This is a normalization step, not a repair step. The goal is to make the response consumable by Agent, Hook, Workflow, and the deterministic scorer described in the Skill Test Case Specific format.

Use this template for every formatted response:

```markdown
selected_skill: <skill-name-or-empty>
status: PASS|FAIL|BLOCKED|NEEDS_CONFIRMATION|UNKNOWN
artifacts:
- <artifact-name>
routing:
- <route-key>: <route-target>
next_action: <next concrete action or empty>

## Summary
<one or two sentences describing what the sub-agent said>

## Plan Or Decision
<normalized trigger decision or dry-run plan, preserving the raw meaning>

## Contract Evidence
- must_include: <terms or semantic requirements visibly satisfied by the raw response>
- must_not_include: <forbidden actions avoided, or violations observed>
- artifacts: <artifacts named or clearly implied by the raw response>
- routing: <success, failure, blocked, or handoff route named or clearly implied>

## Raw Response
<verbatim raw sub-agent response>
```

Formatting rules:

- `selected_skill`: extract the Skill name when the raw response explicitly names it or uses an unambiguous phrase such as "use X", "选择 X", or "`X` 技能". For negative trigger cases, leave it empty or use the non-skill workflow named by the raw response; never set it to the forbidden Skill just to make an assertion pass.
- `status`: set `PASS` only when the raw response satisfies the case intent in dry-run terms. Set `FAIL` when it misses required behavior, violates dry-run mode, or routes incorrectly. Set `BLOCKED` or `NEEDS_CONFIRMATION` when the raw response correctly asks for missing information instead of fabricating. Use `UNKNOWN` only when the raw response is too ambiguous to judge.
- `artifacts`: list artifacts the raw response names or explicitly plans to produce, such as `Skill Test Report`. Leave the list empty when no artifact is present.
- `routing`: list explicit or clearly implied routes such as `on_success: finish`, `on_failure: skill-author`, `on_blocked: human_confirm`, or `on_case_failure: testcase-agent`. Do not invent a route if the raw response has no equivalent.
- `next_action`: extract the next concrete action from the raw response. For failure cases, this must be the repair or handoff action if present; otherwise leave it empty so the scorer can fail it.
- `Summary` and `Plan Or Decision` may translate between Chinese and English and may compress wording, but must preserve the raw response's meaning.
- `Contract Evidence` should map the raw response to the YAML expectations using visible evidence, not the hidden `expected` fields as instructions for what the sub-agent should have said.
- Keep `Raw Response` verbatim so reviewers can distinguish the black-box sub-agent output from the formatter's normalization.

If a response directory is provided explicitly by the user, treat those files as already captured responses. If they are raw prose rather than formatted responses, create a sibling formatted directory under `tests/tmp/response/` or a user-specified output directory before running the scorer, and record the source path in the final report.

If sub-agent tools are unavailable, fall back to answering the rewritten prompts in the current Agent only when the user wants the test to continue. Mark the report or final notes with `response_source: current-agent-fallback` because those responses are not isolated black-box samples.

Do not stop at prompt generation unless the user explicitly asks for prompts only or forbids creating test artifact files.

## Prompt Rewriting

Rewrite `cases[].query` based on `cases[].type`:

- For `trigger` cases, use:

```text
If the user's query is: ${query}, which skill will you use to handle it?
Do not actually execute tools or modify files. Only output the name of the skill you select along with a brief reason.
```

- For `plan`, `contract`, `edge`, and `failure` cases, use:

```text
If the user's query is: ${query}, what steps will you take?
Do not execute any tools or modify files in reality; output only your plan.
```

When useful, append the case `inputs.files` and `inputs.context` as test context, but keep the dry-run restriction at the end of the prompt.

## Response Judging

Judge each Agent response with the YAML first:

- `expected.skill.should_use`: pass when the selected Skill matches, or for plan-like cases when the response explicitly says it will use that Skill.
- `expected.skill.should_not_use`: fail when the response selects one of these Skills.
- `expected.must_include`: fail for any missing required term, field, step, or equivalent semantic content.
- `expected.must_not_include`: fail for any forbidden action or content, including tool execution, file modification, hallucinated facts, or out-of-scope implementation.
- `expected.artifacts`: pass when the response names the expected artifact or defines how it would be produced in dry-run mode.
- `expected.routing`: pass when success, failure, blocked, or handoff paths are present when required.
- `assertions`: evaluate simple assertions directly when possible; use LLM judgment only for semantic assertions that cannot be parsed mechanically.

Treat these as automatic failures:

- The response says it executed commands, edited files, called services, or generated real artifacts during a dry-run case.
- The response ignores the requested Skill choice or plan-only format.
- The response invents unavailable files, schemas, API fields, logs, or test results.
- The response omits a failure route for `failure` cases or a confirmation path for blocked `edge` cases.

## Scoring

Score each case on a 100-point scale:

| Dimension | Points |
|---|---:|
| Skill selection correct | 15 |
| Workflow steps complete | 20 |
| Output contract matches | 20 |
| Edge handling reasonable | 15 |
| Failure routing clear | 15 |
| No overreach or hallucination | 10 |
| Expression clear | 5 |

Use this result threshold:

- `PASS`: score >= 85 and no automatic failure.
- `REVIEW`: score 70-84 and no automatic failure.
- `FAIL`: score < 70 or any automatic failure.

For `trigger` cases, focus the score on Skill selection and non-trigger behavior. For cases where a rubric dimension is not applicable, assign its points based on whether the response stays within that case's expected responsibility.

## Report Format

Return Markdown with this structure:

```markdown
## Skill Test Report

- Skill: <skill.name>
- Cases: <total>
- Passed: <pass_count>
- Review: <review_count>
- Failed: <fail_count>
- Overall: PASS|REVIEW|FAIL

| Case | Type | Score | Result | Key Findings |
|---|---|---:|---|---|
| trigger_001 | trigger | 95 | PASS | selected expected skill |

## Failures

- <case_id>: <specific failed expectation or assertion>

## Next Actions

- <actionable fix for the target Skill or its tests>
```

Keep findings specific enough to edit the target Skill or case YAML.

## Helper Script

Use `scripts/skill_test_runner.py` when you need deterministic prompt generation or basic response checks:

```bash
python3 skills/skill-testing/scripts/skill_test_runner.py path/to/skill/tests/skill_cases.yaml --emit-prompts
python3 skills/skill-testing/scripts/skill_test_runner.py path/to/skill/tests/skill_cases.yaml --markdown
python3 skills/skill-testing/scripts/skill_test_runner.py path/to/skill/tests/skill_cases.yaml --responses path/to/responses --markdown
python3 skills/skill-testing/scripts/skill_test_runner.py path/to/skill/tests/skill_cases.yaml --write-report path/to/skill/tests/tmp/skill-test-report.md
python3 skills/skill-testing/scripts/skill_test_runner.py path/to/skill/tests/skill_cases.yaml --markdown --response-source current-agent-fallback
```

The response directory should contain one text file per case named `<case_id>.txt` or `<case_id>.md`. When `--responses` is omitted, the runner reads from `tests/tmp/response/`.
