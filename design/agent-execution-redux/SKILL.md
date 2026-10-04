---
name: agent-execution-redux
description: "Redux state for agent execution and firing agent shortcuts. Use when editing features/agents/redux/, building agent UI, creating a conversation, touching assembleRequest or NDJSON stream state, wiring agent-state selectors, adding a per-conversation capability, or triggering a shortcut from a button, menu, or code (useShortcutTrigger, launchAgentExecution)."
---

# Agent Execution Redux — State Management

## Routing — read the companion that matches your task

Architecture, execution flow, design rules, and the where-does-state-belong table below apply to every run. Branch material lives beside this file:

- **Adding a field, action, or selector to a slice** → read [extending-slices.md](extending-slices.md) (the 5-step process + worked example).
- **Firing / engaging / triggering a shortcut from product code** (button, context menu, mounted component, programmatic — including `createInstanceFromShortcut`) → read [triggering-shortcuts.md](triggering-shortcuts.md) before writing the call site.
- **Reading or changing `instanceUIState` fields or actions** → read [instance-ui-state-reference.md](instance-ui-state-reference.md).

## Architecture

Four strict layers. Every slice, selector, and thunk belongs to exactly one.

### Layer 1 — Agent Source (`features/agents/redux/`)

Static definitions. What agents and shortcuts exist.

| Redux Key | Directory | Owns |
|-----------|-----------|------|
| `agentDefinition` | `agent-definition/` | All agent records (live + version snapshots). Dirty tracking, field-level undo, progressive fetch status, access metadata. |
| `agentShortcut` | `agent-shortcuts/` | Pre-configured launch configs: agentId + scope mappings + display prefs + variable overrides. |
| `agentConsumers` | `agent-consumers/` | Per-UI-instance filter/sort/search for agent list views. Multiple consumers browse independently. |

### Layer 2 — App Context (`lib/redux/slices/appContextSlice.ts`)

| Redux Key | Owns |
|-----------|------|
| `appContext` | Org, workspace, project, task IDs. Injected into every API call by `assembleRequest()`. |

### Layer 3 — Per-conversation slices (under `execution-system/`)

Ephemeral runtime state. Each conversation is self-contained.

> **Rename landed (2026-08):** the "execution instance" is now the **conversation**. Every
> per-conversation slice keys on `byConversationId: Record<string, T>` — `byInstanceId` no longer
> exists anywhere in `execution-system/`. The shell slice is `conversations`
> (`conversations/conversations.slice.ts`, "formerly 'execution instance'");
> `generateInstanceId` survives only as a `@deprecated` alias of `generateConversationId`
> (`utils/ids.ts`). The family has also grown well past the ten slices this doc originally
> listed — the table below shows the core request-assembly set; see the `execution-system/`
> directory listing for the full current set (messages, observability, run-sets,
> instance-working-document, inbox, durable-runs, …).

**Core invariant: `agentId` is read exactly ONCE at conversation creation. After that, the conversation owns all its data. The agent definition can change or be deleted — the running conversation is unaffected.**

| Redux Key | Sent to API? | What it owns |
|-----------|:------------:|-------------|
| `conversations` | No | Shell: agentId, origin, status (`draft → ready → running → streaming → paused → complete → error`) |
| `instanceModelOverrides` | `config_overrides` | Base LLM settings snapshot + user deltas (only deltas sent) |
| `instanceVariableValues` | `variables` | Definitions snapshot + three-tier resolution: defaults → scope → user |
| `instanceResources` | merged into `user_input` | Attached files/content with status tracking |
| `instanceContext` | `context` | Slot-matched + ad-hoc context entries |
| `instanceUserInput` | `user_input` | Text + multimodal content blocks |
| `instanceClientTools` | `client_tools` | Client-side tool IDs |
| `instanceUIState` | **Never** | Display mode, panels, variable focus, creator flags — purely visual |
| `messages` | No | The committed transcript (turn history) |
| `activeRequests` | No | Per-request stream state: accumulated text, data payloads, pending tool calls, client metrics |

### Layer 4 — Thunks + Cross-Cutting Selectors

| File | Role |
|------|------|
| `thunks/create-instance.thunk.ts` | Conversation factory. 5 creation paths. Reads agent once, dispatches `init*` to every sibling per-conversation slice. |
| `thunks/execute-instance.thunk.ts` | Convergence point. `assembleRequest()` reads all per-conversation slices → fetch → NDJSON stream → dispatches to `activeRequests` + `messages`. |
| `selectors/aggregate.selectors.ts` | Cross-cutting: conversationId → latest request → derived state (executing, streaming, text, errors, tools). |

---

## Execution Flow

```
createManualInstance(agentId)
  ├── readAgentSnapshot() — reads agentDefinition ONCE
  ├── createInstance() — shell in `conversations`
  └── init* dispatches to every sibling per-conversation slice
       │
       ▼
executeInstance(conversationId)
  ├── assembleRequest(state, conversationId)
  │     reads: instanceUserInput, instanceResources,
  │            instanceVariableValues, instanceModelOverrides,
  │            instanceContext, instanceClientTools, appContext
  │     → snake_case payload
  │
  ├── Routing: no conversationId → POST /api/ai/agents/{agentId}
  │            has conversationId → POST /api/ai/conversations/{id}
  │
  ├── addUserTurn → optimistic UI (message appears immediately)
  ├── createRequest → row in activeRequests
  │
  └── NDJSON stream loop:
        chunk        → appendChunk (accumulated text)
        tool_delegated → addPendingToolCall (instance pauses)
        completion   → stats captured
        error        → status "error"
        end          → commitAssistantTurn to conversation history
```

---

## Design Rules

**Snapshot isolation** — Instances never read back from `agentDefinition`. The creation thunk copies what it needs; execution only touches instance slices.

**Request ≠ Conversation** — One conversation, multiple requests (multi-turn). `activeRequests` keyed by `requestId`, reverse-indexed by `conversationId`. Components only know `conversationId` — aggregate selectors bridge.

**Cleanup** — `activeRequests`, `messages`, and `instanceUIState` listen to `destroyInstance` via `extraReducers`. Other slices rely on the creation thunk for init and the shell for truth.

**Progressive fetch** — `AgentFetchStatus`: `list < execution < customExecution < full < versionSnapshot`. Never downgrades. `shouldUpgradeFetchStatus()` enforces this.

**Factory selectors** — `makeSelect*` creates per-component memoized instances. Use `useMemo(makeSelectFoo, [])` in components. See the `redux-selector-rules` skill for full selector guidelines.

---

## How to Extend This System

### Decision: where does new state belong?

| If the state describes... | It belongs in... |
|--------------------------|-----------------|
| How something is displayed (layout, panels, expanded, focus) | `instanceUIState` |
| What the user typed or attached | `instanceUserInput` / `instanceResources` |
| Agent config for this run (model, temperature, tokens) | `instanceModelOverrides` |
| Variable values for this run | `instanceVariableValues` |
| Contextual data sent to the agent | `instanceContext` / `instanceClientTools` |
| What happened during execution (stream, chunks, tools) | `activeRequests` |
| Conversation record (turns, mode) | `conversations` / `messages` |
| Agent definition itself (permanent, not per-run) | `agentDefinition` |
| How a list of agents is filtered/sorted | `agentConsumers` |
| Pre-configured launch config | `agentShortcut` |

### What you must never do

- **Local state for shared concerns.** `useState` for something that belongs in a slice means other components can't see it and shortcuts can't configure it.
- **Parallel systems.** Don't build a new store because the existing one "doesn't have what I need yet." Extend it.
- **Shape hacks.** Don't force data into a shape that works for your component but breaks the contract.
- **Abandon architecture.** A missing piece is a cue to strengthen the system, not bypass it.

**Adding new state → read [extending-slices.md](extending-slices.md)** for the 5-step process (field → `init*` default → setter → selector → barrel) and the variable-display-layout worked example.

---

## Triggering Shortcuts (Consumption Side)

Engaging a stored shortcut from product code: Rule Zero (read the working example first), the direct vs non-direct modes, the Golden Rules, the four trigger APIs, the shortcut registry, warm-up, `applicationScope` keys, resolution order, `jsonExtraction`, both examples, cleanup, and common mistakes.

**Firing any shortcut → read [triggering-shortcuts.md](triggering-shortcuts.md) before writing the call site.**

---

## Reference: Instance UI State

`InstanceUIState` fields, types, defaults, and available actions.

**Touching `instanceUIState` → read [instance-ui-state-reference.md](instance-ui-state-reference.md).**

For the full developer guide with pipeline details, see `features/agents/redux/AGENTS_OVERVIEW.MD`.
