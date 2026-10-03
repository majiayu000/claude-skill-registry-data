---
name: tool-use-design
description: Design model-facing tools with narrow capability boundaries, clear schemas and descriptions, safe side effects, explicit failure semantics, observability, and task-level evaluation.
---
# Tool Use Design

Use when an AI feature can call functions, APIs, commands, connectors, browsers, databases, or other external capabilities.

## Procedure
1. Define the capability the model needs before defining a tool. Prefer a small operation that maps cleanly to user intent over a generic escape hatch with broad power.
2. Separate reads, simulations/previews, and writes when their risk differs. Make side effects obvious from the tool name, description, arguments, and returned result.
3. Design the input schema to make valid calls easy and invalid calls difficult. Use meaningful field names, constrained enums or types where appropriate, explicit required/optional fields, units, identifier formats, and defaults only when the default is genuinely safe.
4. Write the description for selection and correct use: what the tool does, when to use it, important preconditions, what it does not do, and how its result should be interpreted. Do not bury essential rules in examples alone.
5. Return structured results that expose the outcome the model needs, including stable identifiers, status, errors, partial results, and follow-up handles. Avoid returning enormous raw payloads when a compact truthful representation is sufficient.
6. Define timeout, cancellation, retry, idempotency, and duplicate-call behavior. A model may repeat a call after uncertainty; writes must tolerate or explicitly guard against that risk.
7. Enforce authorization and invariants in the tool implementation, not in the model prompt. Least privilege applies to the credentials, filesystem paths, network scope, data rows, and actions reachable through the tool.
8. Treat tool output from external systems as untrusted data. Preserve source/provenance where relevant and prevent instruction-like content in results from gaining higher authority merely because a tool returned it.
9. Design recoverable failures. Give the model enough structured information to decide whether to correct arguments, retry later, choose another tool, ask the user, or stop. Do not leak credentials or internal secrets through errors.
10. Instrument calls sufficiently to debug selection, arguments, latency, failure, retries, side effects, and downstream outcomes while redacting sensitive data.
11. Evaluate tool use at the task level: whether the model selected the correct tool, supplied valid arguments, avoided unnecessary calls, handled failures correctly, and produced the intended real-world result.

## Decision rules
- Prefer narrow tools over shell-like or arbitrary-execution tools when the task can be represented directly.
- The model chooses; the implementation enforces.
- A tool should not require the model to reconstruct hidden protocol trivia that can be encoded in the tool itself.
- Separate irreversible or high-impact actions from information gathering so the model can reason before committing.
- Do not add a tool when ordinary context or deterministic application logic is simpler and safer.

## Quality gate
The tool interface is ready when the model can reliably select and call it from its description and schema, invalid or unauthorized actions are blocked by implementation, retries and side effects are safe, failures are recoverable, outputs preserve trust boundaries, and evaluations prove useful task completion rather than mere syntactic tool calls.