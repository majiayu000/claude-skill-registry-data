---
name: ouros-ai-security
description: "Audit Ouros AI, MIDAS, MCP and tool-calling security. Use when reviewing prompt-injection resistance, tool authorization, cross-user/thread isolation, MCP boundaries, guardrails, model-controlled arguments, or whether AI behavior can exceed the authenticated user's privileges."
---

# Ouros AI Security

Treat model output as untrusted input to privileged systems.

Read `../../references/ouros-security-model.md` for the Ouros AI/tool trust path.

## Security invariants

Verify these before chasing prompt cleverness:

1. A model cannot grant itself permissions.
2. Every privileged tool re-checks identity/authorization server-side.
3. User-controlled or model-generated resource IDs are checked against the authenticated principal.
4. Thread/history retrieval is principal-bound.
5. Tool responses expose only data the caller is authorized to receive.
6. Hidden/system instructions and secrets are not relied upon as the sole authorization boundary.
7. Guardrail failure does not become authorization failure.

## Audit order

### A. Tool authorization

Map each tool to required identity, role/scope, accepted resource identifiers, mutating vs read-only behavior, and server-side ownership checks.

Flag any tool where authorization depends primarily on the model choosing a safe argument.

### B. Cross-principal isolation

Using dedicated test principals, check whether thread IDs, farm/enterprise/resource IDs, cached context, or memory can cross ownership boundaries.

Use `../safe-runtime-testing/SKILL.md` for runtime probes.

### C. Prompt and indirect-injection boundary

Test whether untrusted content can influence tool selection or arguments **beyond the caller's existing permissions**.

The key question is not whether the model followed an instruction, but whether following it crossed a protected boundary.

### D. Data minimization

Review model context assembly, tool outputs, logs/traces, error messages, and telemetry for unnecessary secrets, identifiers, or personal data.

### E. Guardrails

Evaluate guardrails as policy/usability controls, not substitutes for authentication or authorization.

A guardrail bypass is security-relevant only when it produces concrete protected impact or violates an explicit safety requirement.

## Finding quality

Do not report vague claims such as `prompt injection possible`. Report the violated invariant, protected boundary, prerequisites, and observable impact.

Pass every candidate to `../finding-verifier/SKILL.md`.
