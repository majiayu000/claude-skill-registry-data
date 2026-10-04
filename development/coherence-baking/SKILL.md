---
name: coherence-baking
description: Use when an AI agent drives the coherence SDK's bake/schema/bindings workflow via Unity MCP. Covers triggering a bake, updating CoherenceSync bindings after a refactor, detecting stale baked code, recovering from bake failures, and modal popups MCP cannot dismiss.
metadata:
  topic: tooling
  engine: coherence
---

# Driving coherence bake/bindings/recovery via Unity MCP

## When to use this skill

- An agent is editing networked prefabs, `[Sync]` fields, `[Command]` methods, or `CoherenceInput` definitions and needs to re-bake before Play mode or tests will work.
- Compilation is fine but Play mode reports stale/missing baked code, or `CoherenceSyncSchemaOutdated` is true.
- A bake was attempted while scripts were failing to compile and Unity put up the *"Baking should always be performed on a successfully compiling state"* modal — MCP can't click it.
- The `Assets/coherence/baked` folder is in a bad state and needs to be wiped and regenerated.
- An agent renamed a CoherenceSync member (or refactored a behaviour) and needs to refresh bindings on existing prefabs.

## The core idea

coherence does **not** use reflection at runtime. The `Coherence.Editor` assembly walks every indexed `CoherenceSync` prefab, emits a schema, and generates per-prefab C# under `Assets/coherence/baked`. Anything that changes the synced surface (fields, commands, inputs, archetypes, prefab membership) makes the baked code stale, and stale baked code either fails to compile or fails to replicate.

The bake is a normal Unity editor operation, so an MCP-driven agent has three jobs:

1. **Trigger** the right operation (`coherence/Bake`, `Update Bindings`, or a manual clear).
2. **Wait for the editor to settle** (script compilation + domain reload) — bake completion happens across compile/reload boundaries, not in a single tool response.
3. **Verify via the console**, because MCP cannot dismiss Unity's modal dialogs. If the dialog appears, the agent has to work around it, not through it.

Backing types in the SDK (all in `Coherence.Editor`):

- `BakeUtil` — `Bake()`, `BakeAsync()`, `BakeAsyncNoReturn()`, `HasBaked`, `Outdated`, `CoherenceSyncSchemaOutdated`, `IsBakingInProcess`, `BakeOnEnterPlayMode`, `SchemaID`. See `sdk/Coherence.Editor/BakeUtil.cs`.
- `CodeGenSelector.Clear()` — internal, what the "Delete Baked Scripts" dialog button calls. Equivalent to deleting `Assets/coherence/baked`.
- `CoherenceSyncUtils.UpdateBindings(CoherenceSync)` — public API for refreshing one prefab's bindings.
- `EditorCache.UpdateBindingsAndNotify()` — what `coherence/Help/Troubleshooting/Update Bindings` calls; sweeps all prefabs and shows a results popup.
- Bake output folder: `Assets/coherence/baked` (`Paths.defaultSchemaBakePath`).
- Gathered schema: `Assets/coherence/Gathered.schema`.

## Pattern 1: Bake via MCP

The menu item is `coherence/Bake` (Mac shortcut `Cmd+Shift+Alt+M`). It calls `BakeUtil.BakeAsync(ShouldWait.Never)`, which forces a recompile when it finishes — meaning the tool response returns *before* the bake's effects are visible.

```jsonc
// 1. Pre-flight: nothing should be in a broken-compile state.
read_console({ "types": ["error"], "count": 20 })
// If there are compile errors, fix them BEFORE baking. See Pattern 4.

// 2. Trigger the bake.
execute_menu_item({ "menu_path": "coherence/Bake" })

// 3. Wait for compilation/domain reload to finish.
//    The bake triggers a domain reload mid-flight — most MCP calls (including
//    refresh_unity with wait_for_ready) will return a "Connection closed before
//    reading expected bytes" error during that window. That's expected, not a
//    failure. Wait ~5-10s and read mcpforunity://editor/state — wait until:
//      compilation.is_compiling == false
//      compilation.is_domain_reload_pending == false
//      advice.ready_for_tools == true

// 4. Verify by file evidence, not console.
//    The MCP console can return 0 entries even for a successful bake (logs are
//    dropped across the domain reload, and BakeUtil doesn't emit a success log
//    of its own — only errors). Confirm by checking that Assets/coherence/Gathered.schema
//    and the .cs files in Assets/coherence/baked have a recent mtime:
//      ls -lt Assets/coherence/baked/*.cs   # via the host shell
//    Do NOT rely on manage_asset get_info on the "Assets/coherence/baked" folder —
//    bake regenerates the files inside but leaves the folder's mtime untouched.
```

There is no MCP-friendly way to read `BakeUtil.Outdated`'s **value** at runtime:

- `unity_reflect get_member` returns the *signature* (e.g. `{property_type: "bool", can_read: true}`) — not the current value.
- `BakeUtil.IsBakingInProcess` is `internal`, so it's not visible via reflection from outside `Coherence.Editor` at all.

If you need a runtime decision based on `Outdated`, the cheap options are:

- **Just bake.** `BakeUtil.Bake*` is a no-op-ish when outputs match — the `GuardAgainstBakingInProgress` short-circuit and the `Outdated` checks downstream avoid wasted work. Idempotent enough to call defensively. (Caveat: even a no-op bake still triggers a domain reload, costing ~5–10 s.)
- **File-level proxies.** `Assets/coherence/baked` folder missing ⇒ `HasBaked` is false ⇒ outdated. `Assets/coherence/Gathered.schema` missing ⇒ `GatheredSchemaExists` is false ⇒ outdated. These don't cover the "schemas changed since last bake" case.
- **`unity_reflect search "Coherence.Generated"`.** If it returns 0 types, the project doesn't have a valid baked assembly loaded — bake is definitely needed. If it returns many types, baked code exists but you can't tell from this alone whether it's fresh.
- **Surface it from a one-shot script.** Add a menu item in the project (e.g. `Tools/coherence/Log Bake State`) that calls `Debug.Log(BakeUtil.Outdated)`, then invoke it via `execute_menu_item` and read the console. Heavy — only worth it for repeated automation.

## Pattern 2: Update bindings after a refactor

Renaming a `[Sync]` field, moving it to a different component, or removing a `[Command]` doesn't automatically update bindings cached on existing CoherenceSync prefabs — they keep pointing at the old member name and become invalid. Two scopes:

**All prefabs at once (project-wide sweep):**

```jsonc
execute_menu_item({ "menu_path": "coherence/Help/Troubleshooting/Update Bindings" })
```

What this actually does (`EditorCache.UpdateBindingsAndNotify` in `sdk/Coherence.Editor/Toolkit/EditorCache.cs:86`):

1. Runs `UpdateNetworkPrefabs` synchronously — **bindings are refreshed in memory immediately**.
2. If any prefab changed, queues `NotifyCoherenceSyncChanges` via `EditorApplication.delayCall`.
3. When that fires, it opens `EditorUtility.DisplayDialog("CoherenceSync Prefabs Updated", …, "Ok, save changes")` — a **blocking modal**.
4. **`AssetDatabase.SaveAssets()` runs only after the dialog is dismissed.**

That means from MCP: if any prefab actually needed an update, the edits are live in memory but **not on disk** until a human clicks OK. The editor main thread is blocked, and subsequent MCP calls will sit waiting. If nothing changed, no modal appears and the call is a no-op (no Debug.Log either — empirically, the trailing `Debug.Log("Trying to update bindings…")` from `CoherenceMainMenu.UpdateBindings` did not show up in the MCP console during testing, possibly suppressed across the asset-import).

**One prefab (when you know which one):** call `CoherenceSyncUtils.UpdateBindings(sync)` from a one-shot editor script via `manage_script` + the `script_apply_edits` path, or surface it through a project-side menu item. The public API does **not** show the dialog, so this is safer for automation than the project-wide menu item. There is no built-in MCP tool that takes a prefab path and refreshes its bindings directly.

After updating bindings, **re-bake** (Pattern 1). Updated bindings change the gathered schema.

## Pattern 3: Detecting and reacting to stale bake

The natural MCP pattern would be "read `BakeUtil.Outdated` before deciding". As noted in Pattern 1, **that doesn't work directly via `unity_reflect`** — the tool returns the property's *signature*, not its value. Pick one of the alternatives in Pattern 1's note (just bake; file-level proxy; one-shot menu item that logs the value).

Alternatively, the user setting `BakeUtil.BakeOnEnterPlayMode = true` means Unity will bake automatically when entering Play mode — but the agent should still wait for the resulting compile + domain reload before assuming the world will replicate. With `PortalUtil.UploadAfterBake` also on, the editor will *exit* play mode, bake, and re-enter — any in-memory script state is lost across that round trip.

## Pattern 4: Recovering from a failed bake or stuck baked folder

There are two failure modes the agent will hit:

### 4a. Baked code itself won't compile

`BakeUtil` refuses to bake when `EditorUtility.scriptCompilationFailed` is true. In the editor UI, it pops the modal:

> **Coherence**
> Baking should always be performed on a successfully compiling state.
> *[Delete Baked Scripts]   [Cancel]*

The modal is only shown when `Watchdog.HasDiagnostics` is true and the editor is not in batch mode. Clicking **Delete Baked Scripts** calls `CodeGenSelector.Clear()` and requests a recompile.

**MCP cannot click this modal.** Workaround: do the same thing the button does, then bake again.

```jsonc
// Equivalent to clicking "Delete Baked Scripts". manage_asset handles
// both the directory and its .meta sidecar, and triggers an AssetDatabase refresh.
manage_asset({ "action": "delete", "path": "Assets/coherence/baked" })

// Bake immediately — don't wait for an intermediate compile that would fail.
execute_menu_item({ "menu_path": "coherence/Bake" })

// Wait ~5-10s for the bake's domain reload to settle, then verify
// by checking that Coherence.Generated.* types resolve again:
unity_reflect({ "action": "search", "query": "Coherence.Generated", "scope": "all" })
// Expected: many Coherence.Generated.Binding_* / CommandsFor_* / BakeInfo entries.
```

The clear-and-rebake path was exercised against the `integration-tests` project — all 274 files in `Assets/coherence/baked` were regenerated, the working tree returned to clean, and the generated types resolved in `Assembly-CSharp` afterwards. In practice the compile-error modal does **not** fire during this specific sequence: the bake writes the regenerated files via batched asset import before Unity attempts a recompile that could have failed against the now-missing types. The modal only fires when there's a *separate* persistent compile error in user code unrelated to the baked output.

### 4b. Bake "in process" flag is stuck

`BakeUtil.IsBakingInProcess` is true while a bake is running. If a previous bake crashed mid-flight, this flag can be left on and subsequent bake attempts silently no-op with a warning *"Coherence: a bake is already in progress."*

The flag is `internal` so MCP `unity_reflect` cannot read it (returns `not found` from outside the assembly). Symptoms instead: `coherence/Bake` returns successfully but `Assets/coherence/Gathered.schema`'s mtime does **not** advance, and the console (if it has any entries) contains the `EditorBakeUtilInProgress` warning.

The flag is reset by `OnBakeEndedActionsAsync` in the `finally` block — usually a domain reload (e.g. saving any script via `manage_script` or triggering a recompile) is enough to clear it. If not, restart the editor; there is no public reset API.

## Pattern 5: Bake-aware editor scripts

When orchestrating multiple sync/refactor passes, the cheapest thing the agent can do is subscribe to `BakeUtil.OnBakeEnded` from a tiny editor script and route the next step through it. But for one-shot operations from an MCP session, polling `is_compiling` and `BakeUtil.Outdated` is usually enough.

## Modal popups: what MCP can and can't do

The Unity MCP server runs C# inside the editor on the main thread but does not have a way to interact with `EditorUtility.DisplayDialog` modals. There are three coherence-specific modals to know about:

| Popup | Triggered by | Workaround |
|---|---|---|
| *"Baking should always be performed on a successfully compiling state"* | `BakeUtil.Bake*` when scripts are failing | Fix compile errors **before** baking; or delete `Assets/coherence/baked` via `manage_asset` and bake. |
| *"Are you sure you want to delete all the generated baked files?"* | `CodeGenSelector.Clear(warn: true)` — not triggered by `Bake` itself, only by tools that explicitly pass `warn: true`. Public menu items don't. | N/A — public bake paths use `warn: false`. |
| *"CoherenceSync Prefabs Updated"* | `coherence/Help/Troubleshooting/Update Bindings` (or any flow into `EditorCache.UpdateBindingsAndNotify`) when any prefab actually changed | **Not informational** — `AssetDatabase.SaveAssets()` runs only after dismissal, so changes won't persist to disk until a human clicks OK. Prefer the single-prefab `CoherenceSyncUtils.UpdateBindings(sync)` API for automation (no dialog). |

Rule of thumb: **never rely on the agent being able to dismiss a coherence modal.** Either avoid the path that opens it, or do the underlying file operation directly.

## When it works / when it doesn't

- **Works:** routine "I added a `[Sync]` field, re-bake" workflows; refactoring binding member names; clean-slate recovery when `Assets/coherence/baked` is corrupted.
- **Doesn't work:** baking while the editor is mid-compile (it'll be guarded out); baking from inside an `AssetDatabase.StartAssetEditing` scope (see the warning in `BakeUtil.Bake` docs — causes an `m_DisallowAutoRefresh` assertion); baking in Clone Mode / ParrelSync clones (`CloneMode.Enabled` aborts the bake silently).
- **Doesn't work via MCP:** dismissing the compile-error modal or the bindings-results popup. Use the file-level workarounds above.

## Gotchas

- **Bake forces a recompile.** Any agent step that immediately follows `execute_menu_item("coherence/Bake")` must wait for `is_compiling == false` *and* `is_domain_reload_pending == false` before reading types or running tests. The bake's `BakeAsyncNoReturn` returns long before the world is ready.
- **The domain reload drops the MCP connection.** Calls in-flight during the reload return *"Connection closed before reading expected bytes"*. Treat that as "wait and retry editor/state", not as a failure. `refresh_unity(wait_for_ready=true)` is particularly prone to this.
- **`unity_reflect` returns signatures, not values.** Don't use it to read `BakeUtil.Outdated`, `HasBaked`, `SchemaIDShort`, etc. — it tells you the property exists and what type it is, nothing more. Use file-level proxies or a one-shot menu item that `Debug.Log`s the value.
- **`read_console` may show 0 entries for a successful bake.** Empirically, on a freshly reloaded domain the MCP console returns no rows even though `Gathered.schema` was just regenerated. Don't treat empty console as proof a bake didn't run — check file mtimes.
- **`manage_asset get_info` on `Assets/coherence/baked` reports a stale folder mtime.** The bake regenerates the files inside, not the folder. Inspect file mtimes (e.g. via host shell `ls -lt Assets/coherence/baked/*.cs`) instead.
- **`BakeUtil.IsBakingInProcess` is `internal` and not visible to MCP reflection.** Use absence of mtime advance on `Gathered.schema` as the proxy.
- **`HasBaked` only checks the folder.** It returns true as soon as `Assets/coherence/baked` exists, even if the contents are out of date. Use `Outdated` for the real "do I need to bake?" answer.
- **`BakeOnEnterPlayMode` triggers a bake on Play.** If an agent is automating play-mode entry while `Outdated` is true, expect a recompile + domain reload pause before play actually starts. With `PortalUtil.UploadAfterBake`, the editor will *exit* play mode, bake, and re-enter — script state is lost.
- **Schema ID is a hash of the schema files, not of baked code.** Two different bakes from the same schema produce the same `SchemaID`. Don't use it as a "did this bake just run" marker; use `BakeUtil.OnBakeEnded`.
- **Update Bindings is per-prefab cache work, not codegen.** Running it does not re-bake. If you renamed a synced field, you need *both* Update Bindings *and* Bake.
- **`Assets/coherence/baked` should never be hand-edited.** It's regenerated wholesale on every bake. Treat it as build output.
- **Don't edit `Assets/coherence/Gathered.schema` directly either** — it's the input to the next bake and gets overwritten by `GenerateSchema`.

## See also

- `sdk/Coherence.Editor/BakeUtil.cs` — entry point. Read `Bake`, `BakeAsync`, `ShouldCompilationErrorsStopBaking`, `Outdated`.
- `sdk/Coherence.Editor/CodeGenSelector.cs` — `Clear()` and how baked code is regenerated.
- `sdk/Coherence.Editor/CoherenceSyncUtils.cs` — `UpdateBindings`, `RemoveInvalidBindings`, `AddBinding` / `RemoveBinding`.
- `sdk/Coherence.Editor/MainMenu/CoherenceMainMenu.cs` — every menu item the MCP agent can call by path.
- `sdk/Coherence.Editor/Paths.cs` — `defaultSchemaBakePath`, `gatherSchemaPath`.
- [`unity-mcp-skill`](../../../../.claude/skills/unity-mcp-skill/SKILL.md) — generic Unity MCP patterns (resource-first reads, `batch_execute`, console verification).
