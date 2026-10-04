---
name: workspace-orchestration
description: Use when orchestrating parallel subagents across workspace board cards for planning, review, implementation, and audit waves
---

# Workspace Orchestration

Orchestrate parallel subagents through workspace board columns: planning → review → implementation → audit → finished.

## Prerequisites

- AgentBoard cloud service reachable (call `agentboard_health_check` — the MCP server is hosted at `mcp.agent-board.app`)
- A workspace board with cards in `backlog` (created via `/foundation`)
- MCP tools loaded: `agentboard`, `codegraph`, `codebase-rag`

## Pipeline Overview

```
Wave 1: Planning    → parallel agents build plans per card     → cards advance to review
Wave 2: Review      → parallel agents validate plans           → cards advance to implementation (or back to planning)
Wave 3: Implementation → parallel agents write code            → build/lint check → cards advance to audit
Wave 4: Audit       → parallel read-only agents verify         → cards advance to finished
```

## Checkpoint Logic

Read the board's `auto_transitions` to determine pausing:

| Board Setting | Default Behavior | With `--auto` Flag |
|---|---|---|
| `review_blocking: true` | PAUSE after Wave 1 | PAUSE (blocking always wins) |
| `review_blocking: false` | PAUSE after Wave 1 | Auto-proceed |
| `audit_blocking: true` | PAUSE after Wave 3 | PAUSE (blocking always wins) |
| `audit_blocking: false` | PAUSE after Wave 3 | Auto-proceed |

**Default is always pause.** The `--auto` flag only skips pauses when blocking is OFF.

## Running a Wave

For each wave, follow this pattern:

### 1. Collect Cards

Query cards by status matching the wave's input column:
- Wave 1 (Planning): cards in `backlog`
- Wave 2 (Review): cards in `review`
- Wave 3 (Implementation): cards in `implementation`
- Wave 4 (Audit): cards in `audit`

Use `mcp__agentboard__agentboard_list_workspace_cards` filtered by status.

### 2. Spawn Parallel Subagents

Launch one Agent per card using `run_in_background: true`. Use the dedicated subagent for the wave by setting `subagent_type`:

| Wave | `subagent_type` |
|------|-----------------|
| 1 — Planning | `planning-agent` |
| 2 — Review | `review-agent` |
| 3 — Implementation | `implementation-agent` |
| 4 — Audit | `audit-agent` |

The subagents carry their own system prompts, tool allowlists, and model assignments. The Agent `prompt` only needs to pass the per-card variables — the agent's instructions cover the rest. Pass:

- `card_id` — the card's UUID
- `board_id` — the board UUID
- `agent_id` — the orchestrator's agent_id (e.g., `claude-opus-4-6`)
- `spec_path` — path to the spec document (planning and review agents only)
- `card_title` — the card's title (planning, implementation, audit — used in artifact headers)

Example prompt body:

```
card_id: 7f3c...
board_id: a91e...
agent_id: claude-opus-4-6
spec_path: /repo/docs/spec.md
card_title: Add chat tool registry
```

### 3. Wait for All Agents

All background agents must complete before proceeding. Report results:

```
## Wave [N] Complete: [Wave Name]
- Cards processed: [X]/[total]
- Passed: [N]
- Failed: [N] (list card titles)
- Time elapsed: [duration]
```

### 4. Handle Failures

**Review rejections (Wave 2):**
- Card sent back to `planning` with rejection notes
- Re-run Wave 1 for rejected cards only (max 2 retries per card)
- After 2 failures: report to user, do not retry

**Build/lint failure (after Wave 3):**
- Stop pipeline — do NOT proceed to Wave 4
- Report which files changed and likely culprit
- Wait for user intervention

**Audit failure (Wave 4):**
- Card stays in `audit` with audit report
- Report findings to user

### 5. Checkpoint (if applicable)

If this wave requires a pause (per checkpoint logic above):

```
## Checkpoint: [Wave Name] Complete

[Results table]

Proceed to [next wave]? (waiting for confirmation)
```

Wait for user confirmation before starting the next wave.

## Build Verification

After Wave 3 (Implementation), before Wave 4 (Audit). Pipe through a filter so only errors/warnings land in context — successful build/lint output is 5–10k tokens of compiler chatter that has no value once you know it passed:

```bash
npm run build 2>&1 | grep -E -i 'error|warning|fail|✘' || echo 'BUILD OK'
npm run lint --prefix client 2>&1 | grep -E -i 'error|warning|fail|✘' || echo 'LINT OK'
```

Both must pass. If either fails, stop and report. On success the only token cost is `BUILD OK` / `LINT OK`.

## Retry Policy

| Scenario | Action | Max Retries |
|---|---|---|
| Review rejects a plan | Re-plan with feedback | 2 per card |
| Build fails | Stop, report to user | 0 (user intervenes) |
| Audit fails | Report, card stays in audit | 0 (user reviews) |
| Agent crashes/times out | Report, card unchanged | 1 |

## Status Reporting

Between waves (and at checkpoints), show:

```
## Orchestration Status — Board: [name]

| Column | Count |
|--------|-------|
| backlog | 0 |
| planning | 0 |
| review | 2 |
| implementation | 0 |
| audit | 3 |
| finished | 5 |

Progress: 5/10 cards finished (50%)
```

## Subagents

Wave workers are dedicated subagents defined in `agents/` at the plugin root:
- `planning-agent` (opus) — produces implementation plans
- `review-agent` (opus) — validates plans against constraints
- `implementation-agent` (sonnet) — executes plans, writes code
- `audit-agent` (opus) — read-only verification of implementation

Each ships with a scoped tool allowlist matching its role. Update those files to change wave behavior.
