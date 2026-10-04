---
name: dispatch
description: Build queue triage and Codex dispatch. Reads UNIFIED-BUILD-QUEUE.md, triages items into Codex-safe vs Opus-only, writes handoff prompts, and auto-dispatches Codex tasks via CLI. Use when user says /dispatch, "what can Codex build", "send to Codex", "triage the queue", or wants to batch-assign work.
---

# DISPATCH (Queue Triage + Codex Auto-Dispatch)

## Purpose

Read the build queue. Decide what Codex can handle vs what needs Opus. Dispatch Codex work automatically. Write swarm handoffs for Opus work. Save tokens by offloading bulk to Codex.

## Phase 1: Read Queue State

1. Read `docs/UNIFIED-BUILD-QUEUE.md` in full
2. Filter to actionable items: `SPEC-READY`, `PARTIAL`, `DRAFT` with clear specs
3. Skip: `DONE`, `IN-FLIGHT` (already claimed), `BLOCKED`

## Phase 2: Triage (Apply These Rules)

### Codex-Safe (dispatch automatically)

Items matching ANY of these:

- Has a dedicated spec file in `docs/specs/codex-*.md`
- Single-file or single-concern change
- UI polish, styling, visual pass
- Test writing (unit, integration, regression)
- Mechanical wiring (connecting existing pieces)
- Migration writing (SQL only, no judgment)
- Bug fixes with clear reproduction steps
- Documentation, types, boilerplate

### Opus-Only (write swarm handoff)

Items matching ANY of these:

- Multi-system integration (3+ files with logic coupling)
- Architecture decisions or new patterns
- Security-sensitive code (auth, payments, data access)
- Debugging without clear reproduction
- Requires reading conversation context or making product decisions
- Cross-domain wiring with judgment calls
- Performance optimization requiring profiling
- Anything touching `lib/ai/`, payment flows, or auth middleware

### Gray Zone Resolution

If unclear, ask ONE question: "Does this need judgment about how systems connect, or is it following a spec mechanically?" Mechanical = Codex. Judgment = Opus.

## Phase 3: Present Triage

Output two tables:

```
## CODEX DISPATCH (auto-send)
| # | Item | Spec File | Complexity | Est |
|---|------|-----------|------------|-----|

## OPUS QUEUE (swarm handoff)
| # | Item | Why Opus | Spec File |
|---|------|----------|-----------|
```

Ask user: "Dispatch Codex batch? Move any items between lists?"

## Phase 4: Dispatch to Codex

For each approved Codex item, generate and execute:

```powershell
codex exec "Read [spec-file-path] and execute it. Constraints: [from spec]. Done when: [acceptance criteria]. Do not touch files outside scope."
```

**Dispatch rules:**

- One `codex exec` per item (isolation)
- Always reference the spec file path
- Always state file scope constraints
- Always state "done when" criteria
- Run dispatches sequentially (Codex handles one at a time)
- Log each dispatch to `docs/dispatch-log.md` with timestamp

**Prompt template:**

```
Read {spec_path} and execute it fully.

CONSTRAINTS:
- Only modify files listed in the spec
- Run `npx tsc --noEmit --skipLibCheck` after changes
- If type errors arise from YOUR changes, fix them
- Do not modify files outside scope
- Commit with conventional commit message when done

DONE WHEN:
- {acceptance_criteria_from_spec}
- Type check passes
- Changes committed
```

## Phase 5: Opus Swarm Handoff

For Opus items, generate a swarm handoff block (same format as `/swarm-handoff`):

```markdown
### Agent: [task name]

- **Model:** opus
- **Task:** [concrete description]
- **Read first:** [specific files]
- **Done when:** [verification criteria]
```

Group into waves by dependency. Output ready-to-paste orchestration prompt.

## Phase 6: Log Everything

Append to `docs/dispatch-log.md`:

```
## [date] Dispatch Batch

### Codex (dispatched)
- [item] -> codex exec at [time] | spec: [path]

### Opus (queued for swarm)
- [item] -> swarm handoff generated

### Skipped
- [item] -> reason
```

## Anti-Patterns

- Sending multi-system integration to Codex (will produce broken code)
- Sending simple spec-following to Opus (wastes expensive tokens)
- Dispatching without spec file reference (Codex hallucinates scope)
- Parallel Codex dispatches (they conflict on git state)
- Not logging dispatches (lose track of what's in flight)

## Model Hierarchy (Updated)

| Complexity                             | Who          | How                        |
| -------------------------------------- | ------------ | -------------------------- |
| Boilerplate, formatting                | Local Ollama | ollama-delegate MCP        |
| Single-file, spec-following, tests, UI | **Codex**    | `codex exec`               |
| Multi-file mechanical, clear wiring    | Haiku agent  | Agent tool, model: "haiku" |
| Multi-file with judgment, integration  | Opus agent   | Agent tool, model: "opus"  |
| Architecture, hard debugging           | Main session | Direct                     |

**Default bias: Codex first.** Only escalate when judgment needed.

## Quick Dispatch (No Full Triage)

If user points at specific items: skip Phase 1-3, go straight to dispatch.

```
/dispatch #23 #24 #25 to codex
/dispatch lifecycle items to opus
```
