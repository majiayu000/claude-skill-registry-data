---
name: lanekeeper-contract-change
description: 'The safe process for changing a Lanekeeper contract: crates/domain, crates/ports, proto/agent.proto, api/openapi.yaml, db/migrations, docs/mcp-tools.md, perf/budgets.toml or design/handoff. Covers compatibility rules for protobuf, OpenAPI and SQL migrations (expand then contract), keeping fakes and conformance tests in sync, regenerating clients, labelling the PR and notifying the affected prompts. Use this skill whenever a task needs a new field, endpoint, message, table, column, port method, MCP tool or budget entry, or when an interface doesn''t fit what you''re implementing. Contract changes made as side effects of feature work break parallel agents, so this process exists to prevent that.'
---

# Changing a contract

Contracts let parallel agents build against each other without waiting. A change made quietly inside a feature PR breaks every other agent working from the old shape. So a contract changes only through its own PR, labelled `contract-change` and approved by a human.

## Step 0: Is this really a contract change?

- **Yes:** anything under `crates/domain`, `crates/ports`, `proto/`, `api/openapi.yaml`, `db/migrations/`, `docs/mcp-tools.md`, `perf/budgets.toml` or `design/handoff/`.
- **No:** private types and modules inside your own crate. Change those freely.
- **Unsure:** treat it as a contract change. Splitting a PR costs little; breaking another agent costs a lot.

## Step 1: Write the change down first

In your plan, write down the proposed change, why your prompt needs it, and which prompts are affected (table below). Stop and wait for approval when the change removes or renames anything.

| Contract | Prompts that consume it |
|---|---|
| `crates/domain` | All |
| `crates/ports` | 02, 03a, 03b, 05, 06, 07, 14, 17 |
| `proto/agent.proto` | 02, 03b, 05, 17 |
| `api/openapi.yaml` | 05, 06, 08, 14, plus 03a for auth routes, problems and audit, 03b for events and refs |
| `db/migrations/` | 03a, 03b, 05, 06, 14, 17 |
| `docs/mcp-tools.md` | 07, 11 |
| `perf/budgets.toml` | 16, plus whoever owns the benchmark |
| `design/handoff/` | 08 |

## Step 2: Make it compatible by default

- **Protobuf:**
  - Add fields; never reuse or renumber them.
  - When removing a field, mark its number and name `reserved`.
  - New oneof variants must be ignorable by old readers.
- **OpenAPI:**
  - Additive changes only within a version: new optional fields, new endpoints.
  - Every operation keeps `x-required-role`.
  - Afterwards, regenerate the orval client and the MSW mocks in `web/`.
- **Migrations:**
  - Always a new file; never edit a merged one.
  - Expand, then contract: add the new column or table, backfill, switch readers, and drop the old one only in a later release.
  - No destructive DDL in the same release as the code change.
  - Keep `lanekeeper_app` grants least-privilege. `audit_events` stays INSERT and SELECT only, with its trigger intact.
- **Ports:**
  - Prefer new methods with sensible defaults over changed signatures.
  - Update the in-memory fake and `ports::conformance` in the same PR, so every implementation is tested against the new behaviour.
- **MCP tools:**
  - Add tools rather than changing their meaning.
  - Every write tool keeps `confirmation: required`.
- **Budgets:** add entries freely. Loosening a threshold needs a human decision recorded in `docs/decisions.md`.

## Step 3: Regenerate and verify

Run `just verify-01`, which covers buf lint, redocly lint, the migration and role tests, and port conformance. Then run `just verify`. Also run the gate of every prompt that consumes the contract and has already merged.

## Step 4: Open the PR

- Title it `contract: <what>`.
- Label it `contract-change`.
- The body states what changed, why, its compatibility, and the affected prompts.
- Keep it separate from feature code. The feature PR follows, and depends on it.
- After it merges, the owners of the affected prompts need notifying. Leave a note in each of their open plans in `plans/`.
