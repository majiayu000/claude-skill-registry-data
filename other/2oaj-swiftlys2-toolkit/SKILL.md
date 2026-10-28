---
name: swiftlys2-toolkit
description: 'Plan, implement, audit, and review C#/.NET SwiftlyS2 plugins. Use when working with Commands, Core Events, Game Events, GameHooks Pre/Post, raw native hooks, Modules, Workers, Services, high-frequency runtime loops, NetMessages, Schema access, entity handling, thread safety, performance, or IPlayer lifecycle behavior.'
---

# swiftlys2-toolkit

This is a general-purpose toolkit entry for **SwiftlyS2 C# / .NET plugin development**.

Its goal is not to bind itself to any specific workspace, but to provide a **publicly reusable** workflow, rule set, template collection, and reference navigation system.

## Public reference allowlist

The public skill, workflow references, and templates in this toolkit should, by default, reference only the following public sources:

1. SwiftlyS2 official documentation: `https://swiftlys2.net/docs/`
2. sw2-mdwiki: `https://github.com/himenekocn/sw2-mdwiki`
3. SwiftlyS2 official repository: `https://github.com/swiftly-solution/swiftlys2`
4. SwiftlyS2 LLM-optimized full documentation: `https://swiftlys2.net/llms-full.txt` (last-resort full-text fallback only when targeted navigation is insufficient)

Keep workspace-specific mappings, private reference repositories, historical projects, credentials, and special rules in the nearest applicable `AGENTS.md` or in a project-local skill. Do not write them back into this public skill.

If the workspace includes a local `sw2-mdwiki` checkout, prefer it as a local public reference repository for faster, more accurate retrieval.

## Full-text documentation usage policy

- Prefer indexed and targeted sources first: `swiftlys2-kb-index.md`, `swiftlys2-official-docs-map.md`, local `sw2-mdwiki`, and the relevant official docs pages.
- Treat `https://swiftlys2.net/llms-full.txt` as a low-priority fallback because it is large and not indexed.
- Before reading the full-text document, ask the user whether it should be read.
- After approval, use keyword-guided or range-based partial reads only; do not scan the whole file by default.

## What this skill should produce

When using this skill, the preferred output should be one of the following:

- An implementation plan for a new plugin or new module
- A direct modification plan for an existing plugin
- A gap analysis for historical behavior alignment
- An audit of lifecycle, thread safety, high-frequency hooks, Schema, or Protobuf usage
- A method-level implementation plan

## Failure-mode-first rule writing

When the toolkit proposes workflow rules, audits, or checklists, prefer rules that map to concrete failure modes rather than abstract virtues.

Examples:

- Do not claim validation without direct evidence.
- Do not treat a successful build as proof of player-visible behavior.
- Do not add bridge/helper layers unless reuse, lifecycle isolation, or boundary clarity clearly requires them.

## Language policy

- Detect the language of the user's latest request before every response and mirror that language for analysis, plans, explanations, delivery notes, prompt text, and any generated code comments.
- If the user switches languages in a later message, the newest user message wins.
- If the user writes in Chinese, respond in Chinese.
- If the user writes in English, respond in English.
- Avoid mixed-language prose unless the user explicitly asks for bilingual output.
- Code comments generated or modified by the toolkit must use the same language as the response.

## Toolkit structure

### Entry documents

- `./SKILL.md`

### Reference documents

- `./references/swiftlys2-plugin-playbook.md`
- `./references/swiftlys2-performance-optimization-playbook.md`
- `./references/swiftlys2-kb-index.md`
- `./references/swiftlys2-official-docs-map.md`
- `./references/swiftlys2-asset-inventory.md`
- `./references/swiftlys2-current-capability-map.md`
- `./references/swiftlys2-custom-hud.md`
- `./references/plan-workflow.md`
- `./references/audit-workflow.md`
- `./references/edit-workflow.md`

### Templates and checklists

- `./assets/README.md`
- `./assets/development/getting-started/partial-plugin-template.cs.md`
- `./assets/development/using-attributes/attribute-registration-checklist.md`
- `./assets/development/swiftly-core/core-service-entrypoints.md`
- `./assets/development/commands/command-attribute-template.cs.md`
- `./assets/development/commands/command-service-template.cs.md`
- `./assets/development/commands/client-command-hook-template.cs.md`
- `./assets/development/menus/menu-template.cs.md`
- `./assets/development/netmessages/protobuf-handler-template.cs.md`
- `./assets/development/game-hooks/game-hooks-pre-post-guide.md`
- `./assets/development/native-functions-and-hooks/hook-handler-template.cs.md`
- `./assets/development/database/database-connection-template.cs.md`
- `./assets/development/entity/entity-key-values-guide.md`
- `./assets/development/sound-events/sound-event-guide.md`
- `./assets/development/steamworks/steamworks-server-guide.md`
- `./assets/development/memory/memory-service-guide.md`
- `./assets/development/configuration/README.md`
- `./assets/development/configuration/config-hot-reload-template.cs.md`
- `./assets/development/convars/convar-template.cs.md`
- `./assets/development/core-events/lifecycle-checklist.md`
- `./assets/development/core-events/precache-resource-template.cs.md`
- `./assets/development/game-events/game-events-usage-notes.md`
- `./assets/development/translations/README.md`
- `./assets/development/permissions/README.md`
- `./assets/development/shared-api/shared-interface-template.cs.md`
- `./assets/development/thread-safety/thread-sensitivity-checklist.md`
- `./assets/development/profiler/hotpath-gc-checklist.md`
- `./assets/development/entity/schema-write-checklist.md`
- `./assets/development/scheduler/scheduler-vs-worker-guide.md`
- `./assets/guides/dependency-injection/di-service-plugin-template.cs.md`
- `./assets/guides/dependency-injection/service-template.cs.md`
- `./assets/guides/terminologies/README.md`
- `./assets/guides/html-styling/README.md`
- `./assets/guides/porting-from-css/porting-checklist.md`
- `./assets/resources/runtime-configuration-guide.md`
- `./assets/patterns/background-workers/worker-template.cs.md`
- `./assets/patterns/per-player-state/player-state-management-guide.md`
- `./assets/patterns/async-patterns/async-safety-guide.md`
- `./assets/patterns/service-factory/service-factory-template.cs.md`
- `./assets/workflows/planning/method-level-plan-template.md`
- `./assets/workflows/audit/audit-report-template.md`

### Workflow references

- `./references/plan-workflow.md`
- `./references/audit-workflow.md`
- `./references/edit-workflow.md`

## Task routing

### If the task is mainly “should we do this / how should this be broken down”

Open these first:

- `./references/swiftlys2-plugin-playbook.md`
- `./references/plan-workflow.md`

### If the task is mainly “systematically find risks first”

Open these first:

- `./references/swiftlys2-plugin-playbook.md`
- If performance, GC, high-frequency hooks, worker queues, map initialization, or native interop are in scope: `./references/swiftlys2-performance-optimization-playbook.md`
- `./references/audit-workflow.md`
- `./assets/workflows/audit/audit-report-template.md`

### If the task is mainly “edit code directly”

Open these first:

- `./references/edit-workflow.md`
- `./assets/README.md`
- The template or checklist closest to the relevant subsystem
- For performance optimization work, also open `./references/swiftlys2-performance-optimization-playbook.md` before editing.
- For custom HUD work, also open `./references/swiftlys2-custom-hud.md` before editing.

### If the task is mainly “find reference entry points”

Open these first:

- `./references/swiftlys2-kb-index.md`
- `./references/swiftlys2-official-docs-map.md`
- `./references/swiftlys2-asset-inventory.md`
- `./references/swiftlys2-current-capability-map.md`

### If online docs are unavailable or a full-text API search is truly necessary

Only after the indexed references above are insufficient, ask the user whether `https://swiftlys2.net/llms-full.txt` may be read. If the user agrees, use it as a low-priority fallback and prefer keyword/range-based partial reads rather than whole-document scanning.
## Architecture categories

### 1. Modular gameplay plugins

Suitable when:

- A single plugin contains a large amount of gameplay logic
- It needs `Commands + Events + Hooks + Modules + Workers + Models`
- It needs per-player runtime state, state synchronization, persistence, and multi-module coordination

### 2. DI / service-oriented plugins

Suitable when:

- The plugin is medium or large in size
- It needs clear interface / implementation / install / uninstall lifecycles
- It needs `ServiceCollection`, dependency injection, self-owned listeners, and command registration inside services

### 3. Hybrid architecture

Suitable when:

- The plugin is mainly gameplay-module-oriented, but some subsystems fit services better
- The modular core needs to be augmented with a small number of installable and uninstallable services

## Core operating rules

### 1. Historical implementations are only temporary experience sources

- If the task requires behavior alignment, historical implementations may be referenced.
- But historical implementations must not become long-term dependencies of the future solution.

### 2. Silent drift is forbidden

- If the user explicitly requires historical alignment, legacy compatibility, or player-visible consistency, every difference must be explicitly explained or explicitly fixed.
- Do not add backward-compatibility branches, aliases, adapters, fallback routes, or duplicate data paths unless the current user explicitly requests compatibility. If active legacy callers or data are discovered, report the evidence and impact before implementing a compatibility layer.

### 3. Lifecycle closure is a hard requirement

At minimum, explicitly check:

- map load / unload
- player connect / disconnect

### 4. Main-thread / async boundaries must be explicit

According to the official SwiftlyS2 `Thread Safety` documentation, the following operations should be treated as main-thread-sensitive by default:

- Many message and entity operations on `IPlayer`
- `ICommandContext.Reply`
- `IGameEventService.Fire*`
- `IEngineService.ExecuteCommand*`
- `CEntityInstance.AcceptInput / DispatchSpawn / Despawn`
- `CBaseModelEntity.SetModel / SetBodygroupByName`
- `CCSPlayerController.Respawn`
- `CPlayer_ItemServices.*`
- `CPlayer_WeaponServices.*`

When in an async context, prefer the corresponding `Async` APIs instead of mechanically wrapping everything in `NextTick` / `NextWorldUpdate`.

### 5. For high-frequency hooks, prioritize safety before speed

- Filter irrelevant objects as early as possible
- Control allocations and logging
- Avoid JSON, IO, blocking waits, and unbounded lock contention
- Prefer a producer / consumer separation mindset
- Keep a 64-tick frame-budget mindset
- Decide whether the Hook should exist at all before optimizing its body; avoid the finest-grained Hook when a lower-frequency movement stage, scheduler, or state-diff path is sufficient
- Use a stable early-return shape: feature disabled / no current runtime / invalid player or pawn / fake client / no registered subscribers

### 5.1 Choose the current hook surface before optimizing it

- Framework lifecycle / tick / ordinary core notifications: `Core.Event`
- Generated Source 2 game events: `Core.GameEvent`
- Typed controller/entity/item/movement/pawn/weapon hooks: `Core.GameHooks`
- Only typed API gaps: `Core.GameData` + `Core.Memory` with an exact delegate
- Do not introduce `DynamicHook`, `[HookCallback]`, or old `Core.Event.On*Hook` paths for a new implementation.
- For dynamic registration, declare the owner, precise unregistration route, `Pre` / `Post` behavior, and whether temporary/ref context can escape.

### 6. `IPlayer` lifecycle has extremely high priority

- `IPlayer` objects may be destroyed after disconnect
- Delayed tasks, async callbacks, menu callbacks, and background worker writebacks must revalidate or reacquire the object
- Do not assume bots / fakeclients can reuse the same identity-key strategy as real players
- When bots and real players are stored together, prefer `SessionId` as the runtime lookup key
- Bot `SteamID` values are not reliable and should, in practice, be treated as fixed `0`; do not use them as stable bot lookup keys
- Use `GetPlayerFromSessionId` for current-session relookup; use `GetPlayerFromSteamId` only for confirmed real-player identity flows.

### 7. For long-lived entity tracking, think in handles first

- Across frames, delays, or maps, do not hold raw entity wrappers long-term
- Prefer storing entities as `CHandle<T>` and validate before access

### 8. `Span` / `stackalloc` / `ref` should only be used when there is evidence

- Suitable for synchronous hot paths and small data transfers
- Must not cross `await`
- Must not cross threads
- Must not be captured by closures or escape the synchronous stack frame
- Do not introduce dangling references or shared-buffer risks just to avoid one copy

### 9. Treat menu callbacks as async contexts

- Review `Click`, `ValueChanged`, and `Submenu` callbacks as async-context code by default
- Prefer `BindingText` for dynamic display text

### 10. JSON and synchronous blocking are high-risk by default

- `.Wait()`, `.Result`, synchronous joins, and blocking IO should be treated as high-risk by default
- JSON serialization / deserialization should, by default, run in the background rather than inside hooks, runtime loops, menu callbacks, or main-thread periodic tasks

### 11. Performance optimization must map to a concrete hotspot category

When asked to optimize performance, first classify the code as one or more of:

- high-frequency Hook / movement path
- per-player runtime state
- sampling buffer / replay-like data
- background worker / queue
- map-level async initialization
- periodic HUD / menu text
- native interop / binary layout

Then use `./references/swiftlys2-performance-optimization-playbook.md` to choose an implementation pattern. Do not add micro-optimizations such as `AggressiveInlining`, object pools, or binary layout unless the code is demonstrably small/hot, allocation-heavy, or native/binary-bound.

## Recommended reading order

### For planning

1. `./SKILL.md`
2. `./references/swiftlys2-plugin-playbook.md`
3. `./references/swiftlys2-current-capability-map.md` when SDK surface selection matters
4. `./references/plan-workflow.md`
5. `./assets/workflows/planning/method-level-plan-template.md`

### For auditing

1. `./SKILL.md`
2. `./references/swiftlys2-kb-index.md`
3. `./references/swiftlys2-current-capability-map.md`
4. `./references/swiftlys2-performance-optimization-playbook.md` when performance or hot paths are in scope
5. `./references/audit-workflow.md`
6. `./assets/workflows/audit/audit-report-template.md`

### For direct code edits

1. `./SKILL.md`
2. `./references/edit-workflow.md`
3. Relevant subsystem templates / checklists

## Output requirements

### If the user wants a plan

The output must include at least:

- Task classification
- Target plugin / subsystem
- Whether historical behavior alignment is involved
- A method-level plan
- Thread / lifecycle boundaries
- A regression matrix

### If the user wants an audit

The output must include at least:

- Risk levels
- File / method-level locations
- Evidence
- Repair directions
- Regression recommendations

### If the user requests direct editing

The output must include at least:

- Files and methods changed
- Why the change was made this way
- Validation results
- Which requirements were directly validated and which still need additional validation

## Verification quality bar

- Prefer evidence-backed verification statements over narrative confidence.
- When validation status matters, distinguish `PASS`, `FAIL`, and `PARTIAL` in audits or delivery notes.
- Use `PARTIAL` only for objective environment limits or missing external dependencies, not for uncertainty or skipped checks.
- For high-risk lifecycle / hook / runtime work, add at least one adversarial or regression-oriented check in addition to build success.

## Examples

- “Add a DI-based state synchronization module for a SwiftlyS2 plugin.”
- “Audit a plugin’s RuntimeLoop and hook hot paths.”
- “Migrate player-visible behavior from a historical SwiftlyS2 plugin into the current architecture.”
- “Fix thread-sensitive calls inside menu callbacks and land the code directly.”
