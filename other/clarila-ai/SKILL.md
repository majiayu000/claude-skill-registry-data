---
name: clarila-ai
description: "Investigate and implement a scoped AI integration, model-workflow or evaluation issue. Use for AI-system behavior, not permission to switch providers, spend or expose private data."
---

# Improve the specified AI behavior

Read the [shared workflow contract](../clarila/references/contract.md) before substantive work. This skill is part of the locally installed Clarila suite. Its source is in `~/Developer/skills`; resolve sibling skills relative to this directory.

## Procedure

1. Read the issue, current integration, expected behavior, model/provider constraints and representative permitted examples.
2. Reproduce the failing request or evaluation. Separate deterministic integration defects, prompt behavior, provider errors and unsupported claims.
3. Implement the smallest change using the authorized model/provider and existing project conventions. Keep user data and credentials out of shared examples.
4. Evaluate realistic positive, negative and regression cases. Record stochastic limits, actual outputs, latency or cost only when measured.
5. Hand off source, representative results, evaluation coverage and independent review/verification requirements.

## Evaluate the integration boundary

Trace a permitted example through the caller, provider transport, response parser and consuming state. Write down the expected output or invariant at the failing boundary before changing it. For streaming or tool workflows, check terminal outcomes such as cancellation, replacement, timeout and malformed output, including late events from an older request.

Retain a compact case record with the input fixture, expected invariant, observed result, source and model/settings used. Deterministic fixture checks and sampled model behavior have different coverage. Compare stochastic results under the same permitted settings and state how many samples actually ran. A provider failure retains its own diagnosis and retry limit.

For streaming, structured output or tool execution, read [stream and tool-state decisions](references/stream-tool-state.md). Resolve `ai-tanstack` through the [expert catalog](../clarila/references/expertise.md) only when that SDK is actually installed; use the owning SDK's version-matched source otherwise. An expert example never authorizes a provider switch, installation or live model spend.

## Synchronization and handoff

Resolve the same issue/workspace/session association before substantive work, including direct invocation. Read and update the private handoff described in the shared contract using available native file tools. Record the actual stage, source, findings, evidence, outcome and next action. If no native session identity is available, retain an unbound record.

## Deliverable

Return integration changes, measured behavior, evaluation cases and uncertainty.

Load only the relevant specialist from the [catalog](../clarila/references/catalog.md). Missing tools change the available evidence, never its meaning.
