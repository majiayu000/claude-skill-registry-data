---
name: mcp-tool-design
description: This skill should be used when the user mentions "MCP tool", "tool design", "tool schema", "inputSchema", "tool annotations", "readOnlyHint", "destructiveHint", "tool description", "resources vs tools", "MCP prompts", or designing the tools/resources/prompts an MCP server exposes to an agent. It provides the design rules for few, powerful, well-schematized tools with accurate annotations and safe errors.
---

# MCP Tool Design

## Purpose
An MCP server's tools are the API the model reasons over, its quality decides whether the agent uses the server well or thrashes. The failure mode is not usually a bug; it is **too many thin, ambiguous tools with loose schemas**, which burn context, invite wrong calls, and hide destructive actions behind innocent names. This skill is the design discipline: few powerful tools, complete schemas, honest annotations, safe errors, bounded output.

## Tools vs resources vs prompts
| Primitive | For | Example |
|---|---|---|
| **Tool** | an **action** the model invokes (may have side effects) | `create_issue`, `run_query`, `search_docs` |
| **Resource** | **readable content** addressed by URI, app-controlled | `file://…`, `db://schema`, a document the host attaches |
| **Prompt** | a **user-initiated** templated workflow | a `/summarize-pr` slash command |
Do not model a read as a destructive tool, or a user workflow as an always-on tool. Picking the right primitive removes whole classes of misuse.

## Few, powerful tools
- Prefer one `search_orders(status?, customer?, since?)` over `list_orders` + `filter_by_status` + `filter_by_customer`. Each extra tool is permanent context cost and another way to be called wrong.
- A powerful tool has a **clear verb-noun name**, does one coherent job, and exposes its variations through **parameters**, not through sibling tools.
- If two tools are almost always called in sequence, consider merging them; if one tool has a boolean that flips it into a different operation, consider splitting, judgment, but bias toward fewer.

## Complete input schemas
Every tool needs a full JSON Schema `inputSchema`:
- Type every field; use `enum` for closed sets; mark `required` accurately; set sane `default`s.
- Give **every** parameter a `description` written for the model ("ISO-8601 date; results on or after this instant"), the description is how the model knows what to pass.
- Constrain: `minimum`/`maximum`, `maxLength`, `format`, `pattern` where they prevent bad calls.
- Reject unknown fields (`additionalProperties: false`) so a hallucinated parameter fails loudly.
A tool whose **description invites** an action the **schema does not constrain** is a design bug (and a security one): the model may attempt the unconstrained thing.

## Honest annotations
Set tool annotations so the host can protect the user:
- `readOnlyHint: true` for tools with no side effects (the host can auto-approve).
- `destructiveHint: true` for tools that delete/overwrite/charge (the host can require confirmation).
- `idempotentHint: true` when repeating the call is safe.
- `openWorldHint` when the tool reaches external systems.
Annotations that lie are worse than none, a `delete_all` marked `readOnlyHint` defeats the host's guardrails. Make them match reality.

## Safe, structured errors
- Return failures as a tool result with `isError: true` and a **useful, non-leaky** message ("order 123 not found", not a stack trace or SQL).
- Never put credentials, internal hostnames, file paths, or raw exception text in a tool result, it goes straight into the model's context and any transcript.
- Distinguish "the model called me wrong" (fixable, tell it what was invalid) from "the upstream failed" (retryable / report).

## Bounded output
- Cap result size; paginate large collections (cursor preferred) rather than returning 10k rows.
- Return the **minimum** the agent needs; summarize, and offer a follow-up tool/resource for detail.
- Prefer structured content the model can act on over prose dumps.

## Golden rules
- **Fewer, more powerful tools.** Variation via parameters, not sibling tools.
- **Full schema, every field described.** The schema and descriptions are the contract the model reads.
- **Annotations must be true.** `readOnlyHint`/`destructiveHint` are safety features, not decoration.
- **Errors are structured and non-leaky.** `isError` + a clean message; no stack traces or secrets.
- **Bound the output.** Paginate and summarize; never dump unbounded data into context.
- **Right primitive.** Action → tool, content → resource, user workflow → prompt.

## Additional Resources
### Reference Files
- **`references/tool-schema-patterns.md`**: annotated tool definitions (TS + Python), the search-tool-with-parameters pattern, enum/constraint examples, annotation matrix, and structured-error shapes.
