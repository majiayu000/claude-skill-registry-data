---
name: setup-engine
description: Use when you need to configure and safely activate one native Codex engine-specialist pack for Godot, Unity, or Unreal.
---

# Setup Engine

Use this skill when selecting, changing, refreshing, or upgrading the project's game engine. Engine selection is a material project decision. Keep it user-driven and make only one decision per turn.

## Supported packs

Exactly one of these packs may be active:

- Godot: `godot`
- Unity: `unity`
- Unreal Engine: `unreal`

Each immutable source pack contains exactly five Codex agent profiles under `.codex/agent-packs/<engine>/`. Activation copies those profiles into `.codex/agents/`; `.codex/active-engine.json` records their hashes and ownership. Never edit a source pack during setup.

## Utility boundary

No director gates apply. `$setup-engine` is a technical configuration utility.
No director agents participate; the workflow does not emit a gate ID or
gate-skip message in any review mode. The parent agent owns every question, approval request,
changeset, validation result, and final handoff.

## Gather decisions

Read `design/gdd/game-concept.md`, `AGENTS.md`, `.codex/studio.toml`,
`.codex/active-engine.json`, and `.codex/docs/technical-preferences.md` when
present.

**Supplied engine argument:** normalize a supplied `godot`, `unity`, or
`unreal` argument, use it as the Engine decision, and skip the Engine selection step;
do not ask the user to select an engine again. Reject any other argument with
the three supported values. The argument does not authorize
writes; all remaining missing decisions and the complete changeset still
require the normal approval flow.

Before asking missing decisions, detect whether engine configuration is
complete. Complete means the six-field studio authority is valid, the active
manifest and exactly five profiles validate, and the engine/version/language,
rendering/physics, platform/input, naming, specialist routing, testing, and
performance sections contain no placeholders. With no supplied engine argument,
report `Engine already configured as <engine/version> + <language>` and offer:

- **Reconfigure all** — gather all seven decisions and use the full activation
  and integration flow.
- **Reconfigure a specific section** — offer `Engine / Language`,
  `Rendering / Physics`, `Naming Conventions`, `Specialists / File Routing`,
  `Platform / Input`, `Testing`, or `Performance Budgets`.

For a specific section, read the complete pre-image; preserve every unselected field and path byte-for-byte.
Limit questions, the proposed diff, and writes to that section. Present one complete proposed changeset containing
every target path and material edit, then obtain fresh approval before
writing. A newly discovered dependent edit is scope expansion and requires a
new complete changeset and approval.

- **Performance Budgets only:** change only the performance-budget lines in
  `.codex/docs/technical-preferences.md`. Do not run pack activation, do not
  touch `AGENTS.md`, studio authority, the manifest, profiles, naming, routing,
  testing, platform/input, rendering, or physics.
- **Naming Conventions**, **Rendering / Physics**, **Platform / Input**, or
  **Testing:** change only the selected section of technical preferences. Do
  not run pack activation.
- **Specialists / File Routing:** change only specialist assignments and the
  routing table; every route must resolve to one of exactly the five active
  profiles. Do not run pack activation.
- **Engine / Language:** gather the exact engine/version/language delta. Use
  the activation transaction only when engine pack, version, language, or
  source-profile state changes; otherwise preserve the active profiles and use
  a configuration-only approved edit.

When configuration is incomplete or **Reconfigure all** was selected, gather
only missing information in this exact order:

1. **Engine** — Godot, Unity, or Unreal.
2. **Exact engine version** — verify the stable version against official engine documentation when the user has not supplied one.
3. **Primary language** — `gdscript` or `csharp` for Godot, `csharp` for Unity, and `cpp` or `blueprint` for Unreal.
4. **Target platform** — the concrete initial platform target.
5. **Primary input** — the dominant input method for that platform and game.
6. **Testing framework** — the engine-appropriate test framework to record.
7. **Performance budget** — accept defaults or gather the target frame/memory budget.

Ask exactly one unresolved decision, then stop and wait. Use `request_user_input` when it is available and appropriate. Ask a concise direct question otherwise. Never bundle independent decisions or silently choose an engine/version.

## Engine-specific configuration contract

Populate naming and routing explicitly for the selected engine. All routes
must name one of exactly the five active profiles recorded by the manifest.

- **Godot + GDScript:** GDScript uses `snake_case` for files, functions, and
  variables. Route `.gd` → `godot-gdscript-specialist`,
  `.gdshader` → `godot-shader-specialist`, and `.tscn` → `godot-specialist`.
  The active set is `godot-specialist`, `godot-gdscript-specialist`,
  `godot-csharp-specialist`, `godot-gdextension-specialist`, and
  `godot-shader-specialist`. For Godot C#, use C# naming and route `.cs` to
  `godot-csharp-specialist` without changing the five-profile set.
- **Unity + C#:** C# classes use `PascalCase`; fields use `camelCase`. Route
  `.cs` → `unity-specialist`, `.asmdef` → `unity-specialist`, and
  `.unity` → `unity-specialist` (and shader assets to `unity-shader-specialist`).
  The active set is `unity-specialist`,
  `unity-addressables-specialist`, `unity-dots-specialist`,
  `unity-shader-specialist`, and `unity-ui-specialist`.
- **Unreal + Blueprint:** record `Blueprint (Visual Scripting)` as the primary
  language. Route `.uasset` → `ue-blueprint-specialist` for Blueprint assets
  (otherwise `unreal-specialist`) and `.umap` → `unreal-specialist`. The active
  set is `unreal-specialist`, `ue-blueprint-specialist`, `ue-gas-specialist`,
  `ue-replication-specialist`, and `ue-umg-specialist`.

## Plan before mutation

This skill must run plugin-bundled utilities, not target-local Python modules.
First obtain the **physical installed SKILL.md path** supplied by Codex for this
invocation. Resolve it to an absolute regular file, then derive the absolute
`BUNDLE` directory from its installed setup-engine resource location. Resolve
the target project root independently. If the runtime cannot provide that
physical resource path, stop and report the missing plugin-resource capability;
do not fall back to CWD, search or guess for resources, inspect environment
hints, or copy plugin resources into the project.

`BUNDLE` is immutable read-only plugin material. `TARGET` is the only location
the transaction may lock, write, recover, or repair. For full configuration,
**Reconfigure all**, or an **Engine / Language** change that requires
activation, run a read-only plan with the chosen values:

```bash
python3 -B <resolved BUNDLE>/tools/codex_studio/engine_pack.py --root <resolved TARGET> --source-root <resolved BUNDLE> --engine <engine> --version <exact-version> --language <primary-language> --dry-run
```

Replace the example values with the user's selection. The command must exit successfully. Present its complete activation plan, including every install, every removal, and the configuration change. Also summarize the proposed `AGENTS.md`, `.codex/docs/technical-preferences.md`, build/test command, and bundled engine-reference provenance as one bounded changeset.

Request explicit approval for that complete changeset. No project write is allowed before this approval. Do not run the apply command, edit preferences, or update references before approval. A dry run is not approval.

For a non-authority section-specific update, replace the activation plan with
the complete selected-section diff and explicit preservation list. The same
approval rule applies: obtain fresh explicit approval, skip activation, and
proceed only with the approved edit.

## Apply the approved pack

After explicit approval, run the exact corresponding transaction only for the
full/engine-change branch. A non-authority section-specific update skips this
entire activation step.

```bash
python3 -B <resolved BUNDLE>/tools/codex_studio/engine_pack.py --root <resolved TARGET> --source-root <resolved BUNDLE> --engine <engine> --version <exact-version> --language <primary-language> --apply
```

The transaction rejects unmanaged collisions, symlinks/reparse points, modified generated profiles, malformed state, stale plans, source changes, and path traversal. It is serialized for cooperating writers and recoverable, not magically atomic to lock-ignorant readers or across arbitrary power-loss/filesystem behavior. Before mutation it persists the original agent tree, manifest, and studio configuration under `.codex/engine-pack-recovery`. It attempts byte-for-byte logical rollback on failure; if rollback itself fails, it preserves the only good backup and journal for explicit recovery:

```bash
python3 -B <resolved BUNDLE>/tools/codex_studio/engine_pack.py --root <resolved TARGET> --recover
```

If activation fails:

1. Stop all remaining setup writes.
2. Show the error and rollback evidence (engine, manifest presence/hash, config hash, managed-profile validation, and persistent journal state).
3. Never claim setup succeeded.
4. Resolve the safety issue only with the user; never delete or overwrite an unmanaged/modified file.

## Complete approved integration

For full configuration or **Reconfigure all**, apply the complete approved write scope below only after activation succeeds.
These full-configuration bullets do not apply to section-specific branches.

For a section-specific branch where activation is not required, apply only the approved selected-section diff and its preservation list after approval.

- Update the Technology Stack and bundled engine-reference provenance in `AGENTS.md`.
- Populate `.codex/docs/technical-preferences.md`, including **Active Engine Pack**, exact build/test commands, naming conventions, platform/input choices, and routing to the five active profiles.
- Read the selected bundled engine `VERSION.md` using the resolved BUNDLE resource path and record its stable Codex Game Studios provenance label in project-owned configuration. The bundled engine references are read-only; never create, refresh, or edit them during project setup.
- Do not add speculative libraries or dependencies.

## Post-apply validation

Run all of the following before reporting success:

```bash
python3 -B <resolved BUNDLE>/tools/codex_studio/validate.py --mode plugin-native --root <resolved TARGET> --source-root <resolved BUNDLE> --phase final
python3 -B <resolved BUNDLE>/tools/codex_studio/engine_pack.py --root <resolved TARGET> --source-root <resolved BUNDLE> --engine <engine> --version <version> --language <language> --dry-run
```

Confirm that:

- `.codex/studio.toml` names the selected engine and pack.
- `.codex/active-engine.json` validates.
- The five active profiles exist and match their recorded hashes.
- Plugin-native validation accepts the six-field project authority and selected five-profile activation without requiring target-local packs, skills, tools, or references.
- The final dry run reports a no-op.
- The approved `AGENTS.md` and technical-preference updates exist, and the bundled engine reference remains readable and unchanged.

Report the engine/version/language, the five active profiles, build/test commands, bundled reference provenance/status, and test results. Never claim success without post-apply validation.

## Completion and handoff

After every approved write is present, plugin-native validation passes, the
five-profile manifest is valid, and the final dry run is a no-op, report
`Verdict: COMPLETE`. Do not use COMPLETE for a failed, rolled-back, unapproved,
or partially applied configuration.

Include a **Contextual next step**:

- If project initialization is incomplete, hand back to `$start`.
- If no approved game concept exists, offer `$brainstorm`.
- If an approved concept exists but systems are not mapped, offer
  `$map-systems`.
- After a section-specific reconfiguration, return to the invoking workflow
  and name the preserved configuration; do not invent unrelated work.

## Refresh and upgrade

For a bundled reference refresh, report that installed engine references are
read-only and stop without writing. Only an explicit, verified canonical studio source checkout may target its repository-root engine-reference source files;
that maintenance requires a separate approved source changeset. Do not
reactivate the project pack unless the pack or engine selection changes.

For an engine upgrade, first audit breaking/deprecated APIs and present the
migration impact. Obtain approval for the project-owned configured-version and
source-migration scope. Bundled references remain read-only; any canonical
reference maintenance requires the verified source-checkout workflow above.
Re-run the transactional activation only when its recorded version/language or
source profiles must change, then complete the same validation gate.
