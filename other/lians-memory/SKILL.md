---
name: lians-memory
description: Use Lians memory from Claude Code for durable recall, resuming unfinished work across agents or sessions, repository verification, point-in-time reconstruction, lineage inspection, lookahead checks, and explicitly confirmed erasure.
---

# Lians memory

Use the Lians MCP tools when the user wants persistent agent memory or needs to
inspect how a remembered fact changed over time.

## Connection

Prefer local SQLite mode when no hosted connection is configured. It requires no
API key and can be launched with:

```bash
uvx --from "lians-sdk[mcp]" lians-mcp
```

Use `LIANS_URL` and `LIANS_API_KEY` only when the user supplies or configures a
hosted or self-hosted endpoint.

## Operating rules

1. Use current recall for the latest non-superseded state.
2. Use point-in-time recall when the request contains an as-of date or asks what
   was known before a later event.
3. Report timestamps, sources, lineage, and verification results exactly as the
   tools return them.
4. Do not infer that a hash-chain check proves legal or regulatory compliance.
5. Require an explicit request reference and user confirmation before erasure.
6. Do not reconstruct content reported as erased or unreadable.
7. Run the lookahead check before relying on memory in a historical simulation.

## Continuity

For substantial work, use `start_task` once to record the goal, observable
success criteria, and constraints. Use `checkpoint_task` when verified progress
changes, including evidence, blockers, decisions with reasons, open questions,
and the next action. On a return or agent switch, use `continue_work`; when more
than one task is active, ask the user to choose instead of guessing. Use
`task_status` before claiming completion.

## State integrity

When a memory, artifact, test, document, analysis, or output materially depends
on a named current fact, use `track_dependencies` with explicit references. Use
`state_impact` before changing high-fanout state. After a change, use
`state_repair_brief`; never reuse memory it reports as invalidated, and preserve
unlisted work. Call `resolve_state_impact` only after repair evidence exists or
when the recorded dependency was demonstrably incorrect.

## Repository verification

For substantial repository work, call `configure_verification` after
`start_task` and before editing. Use repository-relative approved paths, map
every expected changed path to one or more task success criteria, and name the
checks the work requires. Before claiming completion, record real task evidence
and constraint results, then call `verify_work` with a concise summary and
redacted check results. Treat supplied check results as caller attestations,
not Lians-executed proof. Do not include credentials or raw secret-bearing logs.
If the receipt is blocked, fix the named issue and verify again. A clean receipt
is only ready for human ship review; never describe it as formal proof or
permission to merge or deploy.

When `formal_proofs` are configured, treat a `finite-model-v1` success as an
exhaustive proof only for the declared finite model and assumptions. Report any
counterexample exactly. Never claim that the bound application source
implements the model because the current backend binds source hashes but does
not prove that refinement. Project commands and external proof systems are not
executed by this backend.

For `python-finite-function-v1`, report success as a bounded proof of the actual
restricted pure function for every declared satisfying input. Do not broaden
that claim to other functions, inputs, runtime behavior, frameworks, or the
whole application. The checker parses and interprets supported AST nodes; it
does not import or execute the project file.

## Commands

Use the bundled commands for guided workflows:

- `/lians-remember`
- `/lians-recall`
- `/lians-audit`
- `/lians-integrate`
