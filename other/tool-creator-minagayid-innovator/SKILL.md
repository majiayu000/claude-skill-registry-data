---
name: tool-creator
description: Design, scaffold, validate, and dry-run callable tools or functions with explicit JSON schemas, side-effect boundaries, and error contracts. Use when creating or reviewing an MCP/function-calling tool; do not deploy or invoke external mutations without action-time authorization.
---

# Tool Creator

Create a small, auditable tool package that another agent can call safely and predictably. Keep the model-visible contract separate from the implementation and never place credentials, hidden prompts, or arbitrary code execution in a tool manifest.

## Workflow

1. Define the operation in plain language: accepted inputs, output shape, failure modes, latency limits, authentication needs, idempotency, and whether it reads or changes external state.
2. Scaffold a portable JSON manifest with `scripts/scaffold_tool.py`, then edit the generated `function.parameters` and `result.schema` to match the real contract. Keep `additionalProperties: false` unless forward-compatible extras are deliberately justified.
3. Expose only the provider-neutral function definition to the model. The adapter must parse arguments, validate them against the input schema, normalize safe defaults, and reject unknown or malformed fields before execution.
4. Enforce the execution boundary outside the model. Read-only tools may run after validation; write/destructive tools must require explicit action-time approval and an idempotency key. A dry run must not contact the external service.
5. Return a stable envelope: success has `{ "ok": true, "tool_name": ..., "result": ... }`; failure has `{ "ok": false, "tool_name": ..., "error": { "code": ..., "message": ..., "retryable": ... } }`. Do not leak tokens, stack traces, or raw provider responses.
6. Validate the manifest and fixtures with `scripts/validate_tool.py`. Test at least one valid call, one invalid call, an unknown-field rejection, output-shape validation, and the approval gate for a mutating mode.
7. Report what was verified, what was only dry-run, and what still requires a real service or user approval.

Read [tool-manifest.md](references/tool-manifest.md) for the portable contract and [tool-manifest.schema.json](references/tool-manifest.schema.json) when integrating a JSON-schema-aware validator. The included example is intentionally local and side-effect-free.

## Boundaries

- Do not infer permission to send messages, make purchases, delete data, publish, or change accounts from a tool definition alone.
- Do not accept shell commands, executable source, unrestricted URLs, or arbitrary provider parameters as a substitute for a typed contract.
- Keep retries bounded and only retry errors explicitly marked `retryable`; never blindly retry a non-idempotent operation.
