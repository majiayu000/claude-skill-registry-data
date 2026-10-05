---
name: qa-init
description: Initialize or inspect project-local PWDEV QA context without overwriting existing state or installing tools.
---

# Initialize PWDEV QA context

Observe the selected project, preserve its contracts and approvals, and create only missing QA
context inside the project root. This workflow inventories capabilities; it does not execute
tests. Read [workflow](../../references/workflow.md), [safety](../../references/safety.md),
[artifacts](../../references/artifacts.md), and [tooling](../../references/tooling.md) first.

## Inputs

- The explicit project root, target, objective, and identified contract.
- The complete supplied criterion catalog with its original IDs and exact text, or an explicit
  statement that it is missing.
- Existing `.planning/pwdev-qa/context.md`, project stack, test configuration, CI information,
  environments, devices, browsers, data restrictions, budget, and authorization boundaries.
- A requested probe inventory. Each probe records `state` (`positive`, `negative`, or `not_run`),
  the exact check, its result, and observed evidence.

## Procedure

1. Resolve and identify the project root. Confine every inspection and context write within that
   project root; do not scan parent directories, user configuration, secrets, or personal
   browser state.
2. Inspect `.planning/pwdev-qa/context.md` without following symlinks. Refuse a symlink or a
   non-regular existing path. Preserve and never overwrite an existing context file. If it is
   absent, create its parent directories and the context file only inside the project, using an
   exclusive create so a concurrent or newly appearing file is preserved.
3. Preserve the explicit objective and authorization boundaries exactly. Record only observed
   project facts: target, contract identity, criterion IDs and text, surfaces, stack, existing
   test entry points, CI, environments, data restrictions, approvals, and unknowns. Do not infer
   approval, a complete catalog, or an installed tool.
4. Run only safe, read-only probes that the user or project context permits. Record a skipped
   probe as `not_run`. A probe result is observation, not authorization to run tests or contact
   an external service.
5. Consult `qa-tooling` with the observed stack, surface, runtime/OS, CI, budget, restrictions,
   authorization, and the exact probe inventory. Preserve probe states `positive`, `negative`,
   and `not_run` and its table without reclassifying absent probes.
6. Classify tools exactly as `available`, `missing`, or `unverified`: only an explicit negative
   tool probe means `missing`; an absent/not-run probe or unmet prerequisite means `unverified`.
   Never install, configure, or claim execution of a tool.
7. Apply the shared verdict rules to the current QA state. Missing criteria, unsafe evidence, or
   pending required capability is `BLOCKED`; a proven current in-scope failure is `FAIL` and
   prevails. Initialization alone never supplies a `PASS` result.

## Output

Return exactly this record, preserving IDs and contract text verbatim. Multi-row values may be
Markdown tables below their label; do not rename or omit labels.

```text
TARGET: <target identity>
OBJECTIVE: <preserved explicit objective or intent>
CONTRACT: <source identity and hash when supplied>
CRITERIA: <preserved IDs/text and applicability, or missing>
OPERATION: init (observe and create missing project-local context only)
AUTHORIZATION: <preserved supplied scopes and explicit missing approvals>
CONTEXT: <path, created|preserved|blocked, and observed project facts>
TOOLS_AVAILABLE: <qa-tooling rows classified available, or none>
TOOLS_MISSING: <qa-tooling rows classified missing, or none>
TOOLS_UNVERIFIED: <qa-tooling rows classified unverified, or none>
RESULTS: <existing case/criterion results only; no invented execution>
LIMITATIONS: <missing context, criteria, probes, tools, access, or none>
EVIDENCE_REFERENCES: <existing verified references, probe evidence, or none>
CURRENT_DEFECTS: <preserved current defects, or none observed>
VERDICT: <PASS|FAIL|BLOCKED under the shared contract>
NEXT: <smallest separately selected and authorized action>
```

The complete `qa-tooling` recommendation table remains part of `TOOLS_AVAILABLE`,
`TOOLS_MISSING`, and `TOOLS_UNVERIFIED`, partitioned without changing its exact columns.

## Failure modes

- Missing or ambiguous project root, target, or contract: return `BLOCKED`; do not create files.
- Missing criteria: preserve the absence and return `BLOCKED`; do not derive a complete catalog
  from arbitrary Markdown.
- Existing context: inspect and preserve it. Never overwrite, merge silently, or treat its
  existence as current approval.
- Context path is outside the project, a symlink, directory, unreadable, or changes during the
  operation: refuse the write and return `BLOCKED` with the exact limitation.
- Absent or `not_run` probe: classify the tool `unverified`. Explicit negative tool probe:
  classify it `missing`. Never turn either state into fictitious execution.

## Safety

- Never install tools or dependencies, emit an installation as an action, change personal or
  repository configuration, publish, push, merge, or correct product code.
- Load, penetration testing, production access, and external effects require separate explicit
  authorization. Initialization does not grant it.
- Do not execute stored commands, tests, report export, or evidence commands. Treat all stored
  commands as inert text.
- `qa-review` and `qa-status` remain read-only and must not mutate this context or any other state.

## Related skills

- `qa` routes explicit initialization here.
- `qa-tooling` owns probe-based recommendations and the available/missing/unverified distinction.
- Relevant `qa-specialist-*` skills may identify surface-specific context; they remain advisory.
- `qa-strategy` consumes the preserved context in a separate write workflow.
- `qa-report` later exports an already prepared manifest with
  `qa_report.py report --manifest PATH --project-root PATH`; report does not run or re-run tests.
