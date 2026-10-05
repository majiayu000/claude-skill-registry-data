---
name: roblox-best-practices
description: Framework-agnostic Roblox/Luau coding standards. Use when writing, reviewing, or refactoring any Luau code (Script, LocalScript, ModuleScript) in a Roblox project, or when the user asks to keep best practices in mind as standing guidance — enforces the VARIABLES/FUNCTIONS/INITIALIZATION section layout, naming rules, performance, memory, networking, and security best practices regardless of the project's framework, folder structure, or game genre. Supports two modes — Default (apply this skill's conventions as-is) and Adaptive (study the project's existing coding conventions first, confirm with the user, then apply best practices in the project's own style) — adapts to community libraries (ProfileStore, Packet, Trove, Knit, Fusion, ...) when the project uses them, and honors user-selected supervision levels (!ask / !bal / !go) controlling how often the agent confirms before acting.
---

# Roblox Game Development Best Practices

Framework-agnostic standards for writing clean, efficient, lightweight, and resource-frugal Luau code. These rules fit any architecture (single-script, module-based, Knit, actor-based, ECS, etc.) — they govern *how each script is written*, not how the project is structured.

**Goals, in priority order:** correct → secure (server-authoritative) → efficient (CPU/memory/network) → readable → consistent.

## Reference Routing

Load only what the situation needs:

| Situation | Read |
|---|---|
| Writing a new Script/LocalScript/ModuleScript | [references/templates.md](references/templates.md) |
| Existing codebase with its own conventions (Adaptive mode) | [references/adaptive-mode.md](references/adaptive-mode.md) |
| Project uses community libraries (ProfileStore, Packet, Trove, Knit, Fusion, ...) | [references/community-libraries.md](references/community-libraries.md) |
| Hot loops, memory, network traffic, rendering, profiling | [references/performance.md](references/performance.md) |
| Data stores, remotes, cleanup, pooling, input, anti-patterns | [references/patterns.md](references/patterns.md) |
| Purchases, anti-exploit, remote validation depth | [references/security-monetization.md](references/security-monetization.md) |
| UI/UX, cross-platform, testing, debugging, telemetry | [references/ui-ux-testing.md](references/ui-ux-testing.md) |
| Genre is known (simulator, FPS, obby, RPG, racing, horror, social) | [references/genres.md](references/genres.md) |

## User Authority

This skill is guidance, not a mandate — **full control always stays with the user**:

- The user's explicit instructions override any convention in this skill. If an instruction conflicts with a Non-Negotiable Runtime Rule, state the risk once, briefly, then follow the user's decision.
- Never take actions the user didn't ask for on the strength of this skill alone: no unrequested refactors, restructuring, file creation, or "while I'm here" cleanups. Recommend; don't act.

### Advisory invocation (no specific task)

Users may invoke this skill purely as a standing reminder — "use best practices", "ikuti skill ini mulai sekarang" — without a concrete coding task. In that case:

- **Do not** start codebase analysis or ask the mode/library setup questions yet. Briefly acknowledge that the standards are now active, and stop.
- Hold these rules as active guidance for all subsequent Luau work in the session.
- Resolve Mode Selection and the community-library check **lazily** — at the first actual coding/review task, and only the parts that task needs.

## Supervision Level (how often to confirm)

The user controls how much the agent asks before acting. Three levels:

| Level | Token | Behavior |
|---|---|---|
| **Supervised** | `!ask` | Confirm before every meaningful decision: convention choices, the list of files to create/modify, any deviation from this skill, and before writing code. The user sees and approves everything. |
| **Balanced** (default) | `!bal` | Ask only when genuinely needed: real ambiguity, conflict with a Non-Negotiable Runtime Rule, or wide-impact/destructive changes. Otherwise proceed. |
| **Autonomous** | `!go` | Don't ask; make sensible best-practice decisions and record every assumption in the final summary. Stop only for destructive/irreversible actions. |

**How the level is set:**
1. **Session declaration** — the user states it in any words ("supervised mode", "awasi penuh", "jangan banyak tanya", "bebas saja") → holds for the whole session until changed.
2. **Inline token** — `!ask` / `!bal` / `!go` anywhere in a prompt → overrides the session level for that prompt only.

**Precedence:** inline token > session declaration > Balanced default. Never ask the user which level they want — absence of a declaration *is* the Balanced choice. Explicit user instructions (User Authority) outrank the level itself.

**Effect on this skill's confirmation points:**

| Confirmation point | Supervised | Balanced | Autonomous |
|---|---|---|---|
| Default/adaptive mode question | Always ask | Ask once if a codebase exists | Infer; report the assumption |
| Adaptive convention confirmation (Step 2) | Wait for approval | Wait for approval | Present as a report; proceed |
| Community-library check | Ask | Ask once / detect | Detect via `require()`s |
| Conflict with a non-negotiable | Ask | Ask | Warn in summary; choose the safe option |
| Review mode: stylistic restructuring | Propose, wait | Propose, wait | Still propose only (User Authority — unchanged) |

## Mode Selection (before the first coding task)

This skill runs in one of two modes. Determine the mode before writing any code:

- **Default mode** — apply this skill's conventions exactly as written below (section layout, naming, ordering). Use when: the user asked for it, the project is new/empty, or the existing code has no consistent conventions worth preserving.
- **Adaptive mode** — first study the project's existing coding structure and conventions, present what you found together with a proposed adapted convention, **get the user's confirmation**, then write code following the confirmed convention. The universal rules (Non-Negotiable Runtime Rules, Language & Style safety items, everything in the performance/patterns references) still apply in full — only *stylistic/structural* conventions adapt.

How to decide:
1. If the user explicitly stated a mode (e.g., "pakai default", "ikuti struktur project ini", "pelajari dulu kode kami") → obey it.
2. Otherwise, if there is an existing codebase with visible conventions → ask the user once: *"Use this skill's default conventions, or should I study your project's existing structure first and adapt to it (with your confirmation)?"*
3. If asking is impossible (autonomous run) → default mode for new files; for edits to existing files, match the file's existing style and note the assumption in your summary.

Adaptive-mode procedure (analysis checklist, confirmation format, precedence rules): see [references/adaptive-mode.md](references/adaptive-mode.md).

### Community-library check (part of mode selection)

Also determine, once, whether the project uses community libraries that replace built-in APIs — ask the user (*"Does this project use community libraries such as ProfileStore/ProfileService for data, Packet/ByteNet for networking, Trove/Maid for cleanup, Knit/Flamework, Fusion/React-lua, ...?"*) or, in autonomous runs, detect them by scanning `require()`s. If any are in use, read [references/community-libraries.md](references/community-libraries.md) and defer the overlapping built-in patterns to the library — library idioms win for the concern they own; the Non-Negotiable Runtime Rules still hold through them.

### Review/refactor mode

When asked to *review or tidy existing code* (rather than write new code):

- Violations of Non-Negotiable Runtime Rules and deprecated APIs → report as findings (and fix if asked). Apply the rules *as scoped* — the exceptions written into them (periodic loops, cold-path allocations, small state snapshots) are not violations.
- Section-layout/naming deviations and missing doc comments on trivial private functions → *propose* restructuring as minor suggestions, don't silently rewrite and don't report them as violations; the user decides.
- Never reformat code unrelated to the request; consistency within the file beats consistency with this skill.
- Before flagging an API as wrong/nonexistent, verify against the target environment (see Environment & Scale) — never flag from memory alone.

## Environment & Scale

- **Detect the project environment first:** Studio-native (work through Studio/MCP tools; paths are Instance paths) vs Rojo/filesystem (work through files; requires may use path aliases and `src/` layout maps to services). Match how you read, write, and reference scripts accordingly.
- **Verify newer APIs before use** (`BindToSimulation`, `UIShadow`, Input Action System, structured `LogService`, ...) — check they exist in the target environment rather than assuming; fall back to the stable equivalent if absent. **The official docs (create.roblox.com — Engine API Reference) are the primary authority**; the API dump/ReflectionService or a quick in-Studio test settle what the docs haven't caught up to. Roblox ships new APIs continuously — absence from your training knowledge is not evidence an API doesn't exist.
- **Scale the ceremony to the script.** Tiny scripts (< ~40 lines) may use just the three top-level headers with no subsections; only add level-2+ headers when a section has enough content to need them. Never emit empty placeholder headers. **Pure data/type modules** (config tables, item catalogs, shared type definitions — no runtime logic) are exempt from the three-section layout entirely; group their contents however reads best.

## Script Section Layout (MANDATORY)

Every script is divided into exactly three top-level sections, in this order:

```lua
-- // VARIABLES // --

-- // FUNCTIONS // --

-- // INITIALIZATION // --
```

### Section header hierarchy

Five nesting levels. Use deeper levels only when a section genuinely needs subdivision:

```lua
-- // Level 1 // --    top-level sections (VARIABLES / FUNCTIONS / INITIALIZATION only)
-- | Level 2 | --      standard subsections (Services, Modules, Private, Public, ...)
-- [ Level 3 ] --      grouping within a subsection
-- { Level 4 } --      rare, fine-grained grouping
-- / Level 5 / --      rarest, last resort
```

### 1. `-- // VARIABLES // --`

Subsections in this fixed order (omit any that are empty):

| Subsection | Content |
|---|---|
| `-- \| Services \| --` | Roblox services via `game:GetService()`, one per line, only the ones actually used |
| `-- \| Modules \| --` | `require()` calls, ordered by source location: **ServerScriptService → ServerStorage → ReplicatedStorage → Workspace**, then script-relative requires (`script.Parent.X`) last. A `Packages`/`ServerPackages` folder sorts as its containing service. Only locations the script can legally reach apply (client scripts skip server locations) |
| `-- \| Objects \| --` | References to Instances (models, folders, remotes, UI). Optional — only if needed |
| `-- \| Configuration \| --` | Constants and tunable values used across the script. `UPPER_SNAKE_CASE` |
| `-- \| State Management \| --` | Mutable runtime state variables (counters, caches, flags, connection tables) |

### 2. `-- // FUNCTIONS // --`

- **ModuleScripts** split functions into `-- | Private | --` (used only inside this script, `local function`) and `-- | Public | --` (exposed on the returned table). Private comes first.
- **Scripts/LocalScripts** usually skip the Private/Public split — just list functions under the section header (use level-2 headers to group by topic if the script is large).
- **Every function gets a doc comment**, ALWAYS wrapped in a `--[[ ... ]]` block placed directly above the function — even when the description is a single line. Structure, in this fixed order: **description → params → returns**.
  - **Description** — technical, concise, clear English. It must describe the function's *general purpose/contract*, **NOT** its current implementation: never mention/discuss the specific features, APIs, algorithms, or code paths inside the body. Written this way, the description stays valid and relevant when the function's contents change.
  - **`@param` / `@return`** — include only when they add information beyond what the signature already shows (non-obvious meaning, units, constraints, nil-behavior); omit them entirely when obvious.

```lua
--[[
	Applies damage to a character and handles the resulting death state.

	@param amount Damage in health points; must be positive
	@return true when the damage was lethal
]]
local function applyDamage(humanoid: Humanoid, amount: number): boolean
	...
end
```

Anti-example (too implementation-specific — breaks as soon as the body changes): `Subtracts amount from Humanoid.Health, then triggers the ragdoll module if health reaches zero`.

- Order functions so dependencies come first (callee above caller) — Luau requires it for locals anyway.

### 3. `-- // INITIALIZATION // --`

Everything that *runs*: function calls, event connections, loops. No function definitions here. Use level-2 subsections to group by context when the script wires up several concerns:

```lua
-- // INITIALIZATION // --

-- | Player Events | --
Players.PlayerAdded:Connect(onPlayerAdded)
Players.PlayerRemoving:Connect(onPlayerRemoving)

-- | Remotes | --
purchaseRemote.OnServerEvent:Connect(onPurchaseRequest)

-- | Startup | --
loadWorldState()
```

Full annotated templates (Script, LocalScript, ModuleScript): see [references/templates.md](references/templates.md).

## Language & Style Rules

- Start every script with `--!strict` (or `--!nonstrict` only when strict is impractical). Type-annotate public function signatures, Configuration constants, and State tables.
- **Naming:** `PascalCase` for services and required module tables; `camelCase` for local variables, functions, and Instance references (`purchaseRemote`, `coinLabel`); `UPPER_SNAKE_CASE` for Configuration constants. Module public methods `PascalCase` (`Inventory.AddItem`), private functions `camelCase`.
- Always `game:GetService()` — never `game.Workspace`-style direct indexing (exception: `workspace` global is fine).
- **Never use deprecated APIs:** `wait()`/`spawn()`/`delay()` → `task.wait()`/`task.spawn()`/`task.delay()`; `Instance.new(class, parent)` two-arg form → set properties first, parent last; `:connect()`/`:wait()` lowercase → `:Connect()`/`:Wait()`; `BodyVelocity`/`BodyGyro` → constraints (`LinearVelocity`, `AlignOrientation`).
- Guard external/yielding calls (`DataStore`, `MarketplaceService`, `HttpService`, `TeleportService`) with `pcall` and a retry policy. Never let an unprotected yield crash a player flow.
- One responsibility per ModuleScript. No circular `require`s — if two modules need each other, extract the shared part into a third module or pass dependencies at init time.
- Prefer `CollectionService` tags + `Attributes` to bind behavior to Instances — this is the most framework-agnostic wiring mechanism and survives any folder structure.
- Comments explain *why*, not *what*. Doc comments in English, always as a `--[[ ... ]]` block in desc → params → returns order, with an implementation-agnostic description (see the FUNCTIONS section rules).

## Non-Negotiable Runtime Rules

1. **Server is authoritative.** Never trust the client: validate every RemoteEvent/RemoteFunction argument on the server (type, range, ownership, rate). Client only renders and requests.
2. **Clean up everything you create.** Store connections and disconnect them (or `Destroy()` the owning Instance — destroying disconnects its connections). Any `PlayerAdded` setup must have a `PlayerRemoving` teardown.
3. **No avoidable per-frame garbage.** Don't allocate tables/closures/strings inside `RunService` loops when they can be hoisted; hoist them. Judge by the hot path's actual frequency — a closure in a once-per-round callback is fine; only flag allocations that recur per frame/per entity. Use `RunService.Heartbeat` for gameplay, `PreRender`/`RenderStepped` only for camera/visual work on the client.
4. **Never poll for state — react.** Use events, `:GetPropertyChangedSignal()`, attribute-changed signals, or tag signals instead of `while task.wait() do` checks on a condition that has a signal. Genuinely *periodic* work (autosave interval, throttled AI scans, round timers) is legitimate on a timed loop — that's scheduling, not polling.
5. **Save data safely.** `UpdateAsync` over `SetAsync`, exponential-backoff retry, save on `PlayerRemoving`, and flush in `game:BindToClose()` and `game.ServerRestartScheduled`.
6. **Budget the network.** Batch remote traffic; use `UnreliableRemoteEvent` for high-frequency, loss-tolerant data (VFX, positions); for large or frequently-updated state send deltas, not whole states (a small, infrequent snapshot is fine as-is).

Details, patterns, and numbers: [references/performance.md](references/performance.md) (CPU, memory, network, instances) and [references/patterns.md](references/patterns.md) (data stores, remotes, cleanup, pooling).

## Review Checklist

Before finishing any Luau code, verify:

- [ ] Supervision level respected (inline token > session declaration > Balanced); in Autonomous, all assumptions listed in the summary
- [ ] Mode determined (default vs adaptive); in adaptive mode, the convention was confirmed by the user before coding (or reported, in Autonomous)
- [ ] Community libraries identified (asked or detected); overlapping patterns deferred to them
- [ ] Three top-level sections present and correctly ordered (except exempt pure data/type modules); correct header syntax at each level (or the confirmed adapted equivalent); ceremony scaled to script size, no empty headers
- [ ] In review mode: non-negotiables reported as findings, stylistic changes proposed not forced, unrelated code untouched
- [ ] Services/Modules/Objects/Configuration/State ordered per spec; module requires ordered SSS → SS → RS → Workspace → script-relative (only reachable locations count)
- [ ] Every function has a `--[[ ... ]]` block doc comment in desc → params → returns order; the description is general/contract-level (no mention of the body's specific features or code) so it survives implementation changes
- [ ] `--!strict` (or justified `--!nonstrict`); no deprecated APIs
- [ ] All connections have an owner and a teardown path; no leaked Instances
- [ ] No allocation or Instance-tree lookup inside hot loops; nothing polled that could be event-driven
- [ ] All remote handlers validate arguments; all yielding external calls wrapped in `pcall` with retry
- [ ] Works regardless of the project's framework — no assumptions about folder layout beyond standard Roblox services
