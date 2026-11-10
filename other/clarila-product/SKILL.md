---
name: clarila-product
description: "Define expected user behavior, product scope and acceptance criteria for a feature or ambiguous issue. Not for queue priority, implementation or code review."
---

# Define the user outcome

Read the [shared workflow contract](../clarila/references/contract.md) before substantive work. This skill is part of the locally installed Clarila suite. Its source is in `~/Developer/skills`; resolve sibling skills relative to this directory.

## Procedure

1. Read the original request, existing product behavior and relevant decisions. Identify who needs what outcome and why.
2. Describe the intended flow, edge cases, negative behavior and explicit scope. Resolve contradictory requirements from evidence or a focused owner question.
3. Express observable acceptance criteria and suitable fixtures. Separate requirements from design suggestions and implementation choices.
4. Identify UX, data, privacy or rollout dependencies that genuinely affect the outcome. Avoid adding unrelated improvements.
5. Hand off a concise product specification with evidence, decisions and unresolved questions.

Use the project's existing domain terms. For each material acceptance case, identify the actor and starting state, the action, and the observable result, including any protected data or side effect. Make a current owner decision distinguishable from an assumption or an older proposal. Locate the existing user/API boundary where that result can be observed so engineering can choose a suitable implementation.

This behavior-first specification method is informed by the public [specification reference](https://github.com/mattpocock/skills/blob/4ae2317ddb22b046e26455e4f9c9b3aaaf62212d/skills/engineering/to-spec/SKILL.md). Clarila retains the current user's publication scope and issue ownership.

## Synchronization and handoff

Resolve the same issue/workspace/session association before substantive work, including direct invocation. Read and update the private handoff described in the shared contract using available native file tools. Record the actual stage, source, findings, evidence, outcome and next action. If no native session identity is available, retain an unbound record. Use the current host’s native tools during the invoked workflow.

## Deliverable

Return expected behavior, scope, acceptance cases, decisions and remaining product questions.

Load only the relevant specialist from the [catalog](../clarila/references/catalog.md). Missing tools change the available evidence, never its meaning.
