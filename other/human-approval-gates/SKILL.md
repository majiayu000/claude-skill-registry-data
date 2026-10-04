---
name: human-approval-gates
description: "Use when a proposed agent action can publish, delete, purchase, send, deploy, change access, expose data, or otherwise cause material external effects to classify risk, request specific human approval before gated actions, show exact scope, and verify the result. Trigger before irreversible, costly, sensitive, or third-party-impacting operations."
---

# Human Approval Gates

## Overview

This skill applies when a proposed agent action can publish, delete, purchase, send, deploy, change access, expose data, or otherwise cause material external effects. Its intended outcome is to classify risk, request specific human approval before gated actions, show exact scope, and verify the result.

## When to Use

### Preserved source section: When to Use

Use this skill before an action that is irreversible, expensive, sensitive, externally visible, or capable of affecting another person or system. Examples include deleting data, sending a message, making a purchase, publishing content, changing access, deploying to production, or sharing private information.

## Scope

**Does:** Follow the task boundary stated under When to Use and Instructions.

**Does not:** See the preserved source boundaries below and under Stop Conditions.

### Source boundary statements from: Procedure

4. **Request specific approval.** Ask the authorized person to approve that action. Do not infer approval from silence, an earlier unrelated approval, or a general request to complete the project.

### Source boundary statements from: Stop Conditions

Stop and ask when the target is ambiguous, the approval source is unclear, the risk exceeds the user's stated scope, or the operation cannot be rolled back safely. If a platform's tool call itself creates an external side effect, do not use it for a supposedly harmless preview.

## Inputs

**Required:** See the preserved source input guidance below.

**Optional:** Not specified in source skill.

**Prerequisites:** Not specified in source skill.

### Preserved source section: Inputs

- The exact proposed action and target.
- The data or resources affected and the likely consequences.
- Reversibility, blast radius, and available rollback method.
- Existing user authorization and its scope.
- The verification evidence available after the action.

## Instructions

### Preserved source section: Procedure

1. **Classify risk.** Assess impact, reversibility, privacy, financial cost, external visibility, and scope. Treat uncertainty as a reason to narrow the action or ask.
2. **Separate preparation from execution.** Draft, inspect, validate, and preview without crossing the gate. A prepared draft is not permission to send or publish it.
3. **Define the approval request.** Show the action, exact target, relevant content or amount, timing, consequence, and rollback option in concise language.
4. **Request specific approval.** Ask the authorized person to approve that action. Do not infer approval from silence, an earlier unrelated approval, or a general request to complete the project.
5. **Re-check scope.** Before executing, confirm the approved target and parameters still match the current plan. Ask again if the action materially changed.
6. **Execute narrowly.** Perform only the approved operation. Avoid bundling additional changes under the same approval.
7. **Verify and report.** Inspect the resulting state and report whether it succeeded, failed, or remains uncertain.

## Decision Rules

The following source conditional guidance is preserved verbatim; no unstated action is inferred.

### Source conditional guidance from: Procedure

5. **Re-check scope.** Before executing, confirm the approved target and parameters still match the current plan. Ask again if the action materially changed.

### Source conditional guidance from: Output and Acceptance

For gated work, provide a clear approval request and wait before execution. After approval, record the approved scope and the verified result. The gate is satisfied only by explicit authorization from the right person for the exact action; the action is complete only when post-action evidence confirms the expected state.

### Source conditional guidance from: Stop Conditions

Stop and ask when the target is ambiguous, the approval source is unclear, the risk exceeds the user's stated scope, or the operation cannot be rolled back safely. If a platform's tool call itself creates an external side effect, do not use it for a supposedly harmless preview.

## Output Format

### Preserved source section: Output and Acceptance

For gated work, provide a clear approval request and wait before execution. After approval, record the approved scope and the verified result. The gate is satisfied only by explicit authorization from the right person for the exact action; the action is complete only when post-action evidence confirms the expected state.

## Validation Checklist

- [ ] Verify the source-defined success criteria above.

## Edge Cases and Recovery

### Source edge/failure guidance from: Procedure

7. **Verify and report.** Inspect the resulting state and report whether it succeeded, failed, or remains uncertain.

## Stop Conditions

### Preserved source section: Stop Conditions

Stop and ask when the target is ambiguous, the approval source is unclear, the risk exceeds the user's stated scope, or the operation cannot be rolled back safely. If a platform's tool call itself creates an external side effect, do not use it for a supposedly harmless preview.

## Examples

Not specified in source skill. The original provided no input/output example, and none has been invented.

## Success Criteria

### Acceptance criteria from source: Output and Acceptance

For gated work, provide a clear approval request and wait before execution. After approval, record the approved scope and the verified result. The gate is satisfied only by explicit authorization from the right person for the exact action; the action is complete only when post-action evidence confirms the expected state.
