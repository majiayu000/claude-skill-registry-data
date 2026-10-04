---
name: roblox-best-practices
argument-hint: "[ask|bal|go]"
description: "Framework-agnostic Roblox/Luau coding standards. Use when writing, reviewing, or refactoring any Luau code (Script, LocalScript, ModuleScript) in a Roblox project, or when the user asks to keep best practices in mind as standing guidance — enforces the VARIABLES/FUNCTIONS/INITIALIZATION layout, naming, performance, memory, networking, and security rules regardless of framework, folder structure, or genre. Two modes: Default (apply these conventions as-is) and Adaptive (study the project's existing style first, confirm, then apply). Adapts to community libraries (ProfileStore, Packet, Trove, Knit, Fusion, ...) and honors supervision levels (!ask / !bal / !go). Not for non-Roblox Lua, Studio UI or asset questions that do not touch code, or game design discussion with no Luau to write or review."
---

# Roblox Game Development Best Practices

Framework-agnostic standards for writing clean, efficient, lightweight, and resource-frugal Luau code. These rules fit any architecture — they govern *how each script is written*, not how the project is structured.

**Goals, in priority order:** correct → secure (server-authoritative) → efficient (CPU/memory/network) → readable → consistent.

*Skill version 1.19.2. If behaviour here contradicts a newer release, the installed copy is stale — check [CHANGELOG.md](https://github.com/andrian-syh/roblox-best-practices-skill/blob/main/CHANGELOG.md).*


## Session Invariants (must survive compaction)

A summary that drops these rules silently downgrades every file written afterwards. Two standing obligations:

1. **Carry it forward verbatim** in any summary, handoff, plan, or task note. It is active instruction, never compressed into "follow the Roblox skill".
2. **Re-read this file before acting** whenever the card's full text is not visible in your context. Never reconstruct these rules from memory — a half-remembered layout rule looks deliberate and is worse than none.

```text
ROBLOX LUAU SKILL - INVARIANT CARD
1  Three sections, this order:
   -- // VARIABLES // --   Services > Modules > Objects > Configuration > State Management
   -- // FUNCTIONS // --   definitions only (ModuleScript: Private before Public)
   -- // INITIALIZATION // --   everything that runs
2  Documentation Comments (Luau Comments) - default style, adapts to the project.
   Default block: --[[ ]] above the function, desc > @param > @return.
   Moonwave --[=[ ]=] or --- is equally correct when that is the project's style.
   - Desc <= 3 lines and <= 250 chars, contract-level, states PURPOSE.
   - Desc never names what the body does to get there: no APIs, algorithms,
     collaborators, data structures, or code paths.
   - Desc carries NO volatile content: no numbers, thresholds, tunable names,
     feature names, or anything that needs editing when the body is retuned.
     When a detail cannot be avoided, state it at the most general level
     that stays true after the body changes.
   - Tags use Moonwave syntax: @param <name> <type> -- <description>
     and @return <type> -- <description>. Only when they add what the
     signature cannot show.
   - English preferred as the universal language. No em dashes or double-hyphen
     dashes as punctuation (the -- in a tag is a separator, not punctuation).
     No emoji.
   - IN-BODY COMMENTS: banned in code you write. Make names and
      structure say it; put the why in the block above. Never delete
      an existing one; propose removal once, Advisory only.
   - Self-documenting code outranks commentary everywhere.
   - Existing project comment style wins. Recommend this style when the user
     asks to restyle; never impose it.
3  Server is authoritative. Validate every remote arg: type, range, ownership, rate.
4  Clean up everything created. Every connection has an owner and a teardown path.
5  No avoidable per-frame garbage. Never poll what has a signal.
6  UpdateAsync + backoff. Save on PlayerRemoving. Flush on BindToClose.
7  Re-validate after every yield: player gone? instance dead? session changed?
8  Never add --!strict unbidden. Never make a [Beta] feature the production default.
9  Reuse before writing: project, then stdlib, then engine API. No wrapper or
   abstraction without a caller. But brevity has two hard limits:
   - It NEVER reduces what was asked for. Short because it does less = failed.
   - It NEVER costs readability. One statement per line, descriptive names,
     blank lines kept. Less code means less WORK, not less whitespace.
10 User authority outranks this skill. Recommend; never refactor unasked.
```

Everything below expands these; nothing below overrides them.

## Reference Routing

**Load only what the situation needs.** Each reference is self-contained; read one, not the set. Nothing below loads until a line matches the task at hand.

**Authoring**

- [templates.md](references/templates.md) — writing a new Script/LocalScript/ModuleScript
- [section-layout.md](references/section-layout.md) — layout detail, subsection contents, Documentation Comment rules, rejected examples
- [style-rules.md](references/style-rules.md) — naming, deprecated APIs, misremembered APIs, `const`, typing opt-in, module hygiene
- [adaptive-mode.md](references/adaptive-mode.md) — existing codebase with its own conventions
- [community-libraries.md](references/community-libraries.md) — ProfileStore, Packet, Trove, Knit, Fusion, ...
- [minimal-code.md](references/minimal-code.md) — about to write a helper that may already exist; keeping code dense
- [edge-cases.md](references/edge-cases.md) — nil, empty, stale, duplicate, reused, or departed state a function will meet
- [luau-language.md](references/luau-language.md) — truthiness and coercion, table copy semantics, `require` semantics, typing depth, `vector`/`buffer`/`math`, `task.spawn` vs `task.defer`, deferred events, error handling, time APIs, native codegen

**Implementing a known system** — read the one file whose domain matches; each gives assembly order and case-specific failure modes.

- [cases/data-economy.md](references/cases/data-economy.md) — player data, currency, inventory, trading
- [cases/monetization.md](references/cases/monetization.md) — Developer Products, passes/subscriptions, gacha/loot boxes
- [cases/progression.md](references/cases/progression.md) — leaderboards, daily rewards, streaks, offline progress
- [cases/combat.md](references/cases/combat.md) — damage/hit validation, abilities and cooldowns, projectiles, NPC/mob AI
- [cases/session-flow.md](references/cases/session-flow.md) — round/match lifecycle, matchmaking and reserved servers, cross-server events
- [cases/world-interaction.md](references/cases/world-interaction.md) — interactables and prompts, placement/building, pets and followers
- [cases/client-infra.md](references/cases/client-infra.md) — HUD/state sync, rate limiting and anti-cheat, analytics instrumentation

**Deepening a concern**

- [performance.md](references/performance.md) — hot loops, memory, network traffic, physics queries and contact detection, rendering, profiling
- [device-performance.md](references/device-performance.md) — frame budget in ms, low-end and "potato" devices, quality degradation, time-slicing, per-player bandwidth
- [patterns/data.md](references/patterns/data.md) — state ownership, data stores (+ version history), failure policy after the last retry, per-owner locks
- [patterns/network.md](references/patterns/network.md) — remotes, cross-server (MemoryStore, MessagingService, reserved servers), StreamingEnabled
- [patterns/lifecycle.md](references/patterns/lifecycle.md) — connection cleanup, character lifecycle (Humanoid vs CCL), object pooling
- [patterns/world.md](references/patterns/world.md) — CollectionService binding and attributes, client input, anti-patterns to reject on sight
- [patterns.md](references/patterns.md) — index of the four pattern files above
- [security.md](references/security.md) — anti-exploit, remote validation depth, movement sanity checks, text filtering
- [monetization-policy.md](references/monetization-policy.md) — `ProcessReceipt`, Developer Products and passes, PolicyService compliance
- [server-authority.md](references/server-authority.md) — anything touching movement, physics, input, camera, animation timing, `BindToSimulation`, network ownership
- [ui-crossplatform.md](references/ui-crossplatform.md) — UI construction, cross-platform and accessibility, input device handling
- [genres.md](references/genres.md) — simulator, FPS, obby, RPG, racing, horror, social, tower defense, battlegrounds

**Process**

- [workflow.md](references/workflow.md) — resolving a session-setup decision, supervision behavior, opening a review, the preflight before a non-trivial system
- [verification.md](references/verification.md) — proving a change works: playtests, multi-client sessions, test injection, testable architecture, telemetry, the command-bar VM pitfall
- [studio-mcp.md](references/studio-mcp.md) — Studio MCP connection: which tool, what is irreversible, how not to burn tokens
- [external-editors.md](references/external-editors.md) — the project is edited outside Studio: Script Sync, Rojo, Argon, Azul, and the toolchain around them
- [false-positives.md](references/false-positives.md) — reviewing code: whether a finding is real, how severe, what NOT to flag
- [review-checklist.md](references/review-checklist.md) — **finishing any task**: the completion gate before calling work done
- [evaluation-matrix.md](references/evaluation-matrix.md) — auditing a live project on request: how to scope it, gather the evidence, score 1–5 across security, lifecycle, and performance, and report it honestly
- [api-currency.md](references/api-currency.md) — whether a newer engine/Luau API is confirmed before relying on it or flagging it missing
- [limits-budgets.md](references/limits-budgets.md) — platform ceilings: DataStore size/requests, MemoryStore, messaging, attributes, animation tracks

**Lookup files** — `limits-budgets.md`, `genres.md`, `edge-cases.md` are tables, not narratives. Grep the row you need instead of reading them whole.

## User Authority

This skill is guidance, not a mandate — **full control always stays with the user**:

- The user's explicit instructions override any convention in this skill. If an instruction conflicts with a Non-Negotiable Runtime Rule, state the risk once, briefly, then follow the user's decision.
- Never take actions the user didn't ask for on the strength of this skill alone: no unrequested refactors, restructuring, file creation, or "while I'm here" cleanups. Recommend; don't act.
- Invoked with no task ("use best practices", "ikuti skill ini mulai sekarang"): acknowledge that the standards are active and stop — no codebase analysis, no setup questions ([references/workflow.md](references/workflow.md#advisory-invocation-no-specific-task)).

## Session Setup (decide once, then cache)

Five decisions govern every later task. Resolve each **once**, cache it, never re-ask per file — and resolve them **lazily**, at the first task that depends on one. How to resolve each, and how the supervision level modifies it: [references/workflow.md](references/workflow.md#session-setup-resolving-the-five-decisions).

| Decision | Default when unresolved |
|---|---|
| **Supervision level** — invocation argument `ask`/`bal`/`go`, or `!ask`/`!bal`/`!go` inline | **Balanced**; never ask which level the user wants, absence *is* the answer |
| **Default vs Adaptive mode** | **Default** for new files; for edits, match the file being edited and note the assumption |
| **Community libraries** | **None** — use the built-in patterns |
| **Server Authority** | **OFF** — most places are not server-authoritative, and assuming otherwise produces confidently wrong code |
| **Environment facts** — `SignalBehavior`, `StreamingEnabled`, rig type, strictness header | Assume none of them; each inverts correct guidance between values |

*Default* applies these conventions as written; *Adaptive* proposes an adaptation of the project's own style and waits for confirmation ([references/adaptive-mode.md](references/adaptive-mode.md)). Only style and structure ever adapt, and community libraries win for the concern they own. **Never migrate a project to Server Authority on this skill's initiative.**

### Review/refactor mode

One severity per finding (**Blocker / Correctness / Advisory**), after the confidence gate; Advisory is proposed, never forced, and unrelated code is never reformatted. Gate and calibration: [references/workflow.md](references/workflow.md#reviewrefactor-mode). What NOT to flag: [references/false-positives.md](references/false-positives.md).

## Environment & Scale

- **Detect the project environment first** — **Studio-native**, or a filesystem project synced by Script Sync, Rojo, Argon, or Azul. **Which side is the source of truth differs per tool**, and assuming wrong overwrites the user's work: [references/external-editors.md](references/external-editors.md). Never start, stop, or reconfigure a sync session unasked. On an MCP connection, [references/studio-mcp.md](references/studio-mcp.md) applies before any write.
- **Verify newer APIs, and state the basis for every engine fact.** Memory is never presented as fact. Two authorities, two questions: **does it exist** — the versioned API dump or an in-Studio probe; **what does it do** — the Engine API Reference. The docs site **lags the engine**, so a member missing from a reference page is undocumented, not unshipped; never call an API nonexistent on that basis. Cite the check, or say "unverified" and name the one that would settle it: [references/api-currency.md](references/api-currency.md#how-to-verify-the-toolbox).
- **Maturity tags:** **[GA]** safe as a default · **[Beta]** opt-in, may change · **[Undocumented]** shipped, but no reference page — probe its semantics · **[Verify]** confirm in the target place · **[UNVERIFIED]** unconfirmed by this skill. **Never make a [Beta] feature a production default** — offer it, state its status, recommend the stable path.
- **Scale the ceremony to the script.** Tiny scripts (< ~40 lines) may use the three top-level headers with no subsections; add deeper headers only when a section needs them, never empty placeholders. **Pure data/type modules** (config tables, item catalogs, shared types) are exempt from the three-section layout.

## Script Section Layout (MANDATORY)

Card items 1–2 hold the layout and Documentation Comment rules. Two things the card does not carry:

- **Module requires** are ordered by source: ServerScriptService → ServerStorage → ReplicatedStorage → Workspace → script-relative, counting only locations the script can legally reach.
- **Function order inside FUNCTIONS** and what belongs in each VARIABLES subsection are specified, not free.

**Full specification** — the five-level header hierarchy, subsection contents, the two description rules with worked rejections, and the self-documenting-code rule: [references/section-layout.md](references/section-layout.md). Annotated templates: [references/templates.md](references/templates.md).

## Language & Style Rules

The ones that apply on nearly every task:
- **Naming:** `PascalCase` services and module tables · `camelCase` locals, functions, Instance references · `UPPER_SNAKE_CASE` Configuration constants. Module publics `PascalCase`, privates `camelCase`.
- Always `game:GetService()`; never direct indexing (the `workspace` global is fine).
- **Never use deprecated APIs** — `wait`/`spawn`/`delay`, `tick`, lowercase `:connect`/`:wait`, `Body*` movers, `Humanoid:LoadAnimation`, `SetPrimaryPartCFrame`, and the rest of the list in [references/style-rules.md](references/style-rules.md). Discouraged-but-functional APIs (the `Instance.new` parent arg, `FireAllClients`) are **not** deprecated ones and are Advisory at most.
- **Type safety is opt-in.** Never add or raise `--!strict` unbidden; match what the file or project already declares.
- Guard external and yielding calls (`DataStore`, `MarketplaceService`, `HttpService`, `TeleportService`) with `pcall` plus a retry policy and a stated failure policy ([references/patterns/data.md](references/patterns/data.md#failure-policy-what-happens-after-the-last-retry)).
- **Reuse before writing, and keep it dense** — search the project, the standard library, then the engine API. Brevity never reduces what gets delivered and never costs readability.
- **Stay framework-agnostic by construction:** bind by tags and attributes, discover by service, assume no folder layout.

**Complete set** — `const` bindings, `CollectionService` binding, circular requires, one responsibility per module, the full deprecation list, and the commonly-misremembered-API table: [references/style-rules.md](references/style-rules.md).

## Non-Negotiable Runtime Rules

Card items 3-8 are the rules themselves and are always in context. Full statements, the scope that keeps each from being over-applied, and the domain file behind each: [references/runtime-rules.md](references/runtime-rules.md).

Server authority · cleanup with a teardown path · no per-frame garbage · react instead of poll · `UpdateAsync` with backoff and a `BindToClose` flush · batched, delta-shaped network traffic · re-validation after every yield.

These hold through every mode, level, and community library. Before flagging a violation in review, check the scoped exceptions in [references/false-positives.md](references/false-positives.md) — each rule has shapes that only look like violations.

## System Design Preflight

Before implementing any non-trivial system, settle five questions in order — which case is this · what are the ceilings · what is the server/client split and who owns each fact · does this already exist · how will it be proven to work: [references/workflow.md](references/workflow.md#system-design-preflight).

If the system touches movement, input, camera, animation timing, or simulation stepping, resolve the Server Authority decision first — it changes the answers.

## Review Checklist

Before calling any Luau work finished, run [references/review-checklist.md](references/review-checklist.md) — layout, comments, cleanup, hot loops, ownership, failure policy, locks, edge cases, validation, evidence for engine facts, delivery completeness. A **finishing gate**: read it at the end of the task, not the start.
