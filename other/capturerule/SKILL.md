---
name: captureRule
description: Maintain concise current instructions in AGENTS.md, preserving stable rule ids and archiving superseded context when The owner authorizes pruning.
---

# Capture and maintain a rule

## Current instructions first

AGENTS.md is the active implementation contract. Record durable constraints, scope and ownership there. Keep anecdotes, completed migrations, one-off messages and obsolete defaults in history or the relevant domain document.

## Procedure

1. Read the current task and current rules. Existing authorization is sufficient; do not ask again to prune rules The owner explicitly asked to prune.
2. Add or update a concise dated rule in The owner's meaning. Preserve stable active rule ids and the `## Hard rules (from the owner)` heading because the knowledge/MCP collectors parse them.
3. If The owner authorized removal or consolidation, preserve the prior text in the private workspace rule archive, outside this repository. Record old-to-current citations in the MCP generator's consolidated mapping. Never silently renumber a historical id to unrelated behavior.
4. Keep the native ownership/scope rules authoritative. A platform procedure or old generated field inventory cannot reintroduce a superseded architecture.
5. Update the affected skill/spec and generated MCP guidance when applicable. Generated guides are rebuilt from their sources. Do not load the full historical snapshot into active client instructions.
6. Check document links, parser-compatible rule formatting and citations. Do not add or run application tests unless The owner asks. Do not perform paid semantic review as routine rule maintenance.
7. When committing, include the rule, related source/docs and required AST-backed commit log entry together. Never bypass hooks. Report only checks actually performed.

## Scope

Without explicit instruction to prune or supersede, preserve the existing durable constraint and resolve a genuine unanswered conflict. Do not manufacture a confirmation requirement when the current task already resolves it.
