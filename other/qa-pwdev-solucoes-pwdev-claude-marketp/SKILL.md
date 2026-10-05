---
name: qa
description: Use when a user asks for QA planning, execution, review, release assessment, reporting, status, or test-tool recommendations and the correct PWDEV QA workflow must be selected safely.
---

# Route PWDEV QA work

Select one installed `qa-*` workflow without expanding the user's authority. The router does
not perform the selected workflow itself.

Read [workflow](../../references/workflow.md), [safety](../../references/safety.md), and
[artifacts](../../references/artifacts.md) before routing.

## Inputs

- The user's explicit objective and requested operation.
- Existing project context, requirements, criteria, approvals, target, and constraints.
- The observed testing surface and risk when the explicit objective does not identify a
  workflow.
- The QA skills actually present in the active plugin installation.

## Procedure

1. Identify the explicit intent first. Do not reinterpret `review`, `status`, or another named
   workflow from the tools that happen to be available.
2. If explicit intent is absent, use the observed surface to narrow the choice, then use risk to
   choose the smallest workflow that answers the objective. Never infer authorization from risk.
3. Select the candidate from this routing table:

| Intent | Candidate |
|---|---|
| initialize | `qa-init` |
| strategy | `qa-strategy` |
| execute tests | `qa-test` |
| explore | `qa-explore` |
| regression | `qa-regression` |
| bug | `qa-bug` |
| review | `qa-review` |
| release | `qa-release` |
| report | `qa-report` |
| status | `qa-status` |
| tooling | `qa-tooling` |

4. Validate the selected route before returning it: the plugin-relative path
   `skills/<candidate>/SKILL.md` must exist and be a regular file. A missing, non-regular, or
   unreadable target is an error; never claim that an unavailable skill ran.
5. State why the selected candidate applies. Identify close alternatives as not applicable and
   explain why. If no installed candidate fits, stop with an explicit routing error.
6. Preserve external requirements, criteria, states, and approvals. The selected workflow may
   consume them but cannot silently replace their authority.
7. Hand off to exactly one selected workflow and apply its authorization and stop conditions.

## Output

Return this compact routing record before entering the selected skill:

```text
ROUTE: <installed qa-* skill>
WHY: <explicit intent, or observed surface and risk>
NOT_APPLICABLE: <nearby candidates and reasons, or none>
LIMITATIONS: <missing context or tools, or none>
NEXT: <selected workflow entry>
```

If criteria required by the selected workflow are absent, do not invent them. Record the
limitation and let the common workflow contract produce `BLOCKED`.

## Failure modes

- No explicit intent and insufficient surface or risk context: ask one focused question.
- Selected skill path is absent, unreadable, a directory, or a symlink: return a routing error.
- Required criteria are absent: preserve the absence; the QA result is `BLOCKED`, never `PASS`.
- A requested operation exceeds authorization: stop before execution and identify the exact
  authorization needed.
- A tool is missing or unverified: report the limitation; never fabricate an execution.

## Safety

- Routing never authorizes load, penetration testing, production access, or external effects.
- `qa-review` and `qa-status` remain read-only even if the project has writable tools.
- Never install tools, change personal configuration, publish, push, merge, or correct product
  code automatically.
- Follow the evidence boundary and sanitization requirements before any artifact is accepted.

## Related skills

The workflow candidates are the installed `qa-*` skills in the table above. `qa-tooling` is the
tool recommendation entry. Specialist guidance uses installed `qa-specialist-*` skills only
after a workflow requests the relevant surface; absence is a limitation, not an invented route.
