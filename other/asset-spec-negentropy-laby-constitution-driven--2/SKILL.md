---
name: asset-spec
description: "Generate artifact specifications from CDDs and related docs. Game: visual/audio/VFX asset specs and AI prompts. Product: API schema, CLI help, docs asset, config sample, migration, deployment, or package artifact specs."
argument-hint: "[system:<name> | level:<name> | character:<name> | api:<name> | cli:<name> | sdk:<name> | docs:<name> | config:<name> | migration:<name> | deployment:<name> | package:<name>] [--review full|lean|solo]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Edit, Task, AskUserQuestion
---

## User Guide

- When to use: Generate artifact specifications from CDDs and related docs. Game: visual/audio/VFX asset specs and AI prompts. Product: API schema, CLI help, docs asset, config sample, migration, deployment, or package artifact specs.
- Inputs: Command arguments: `/asset-spec [system:<name> | level:<name> | character:<name> | api:<name> | cli:<name> | sdk:<name> | docs:<name> | config:<name> | migration:<name> | deployment:<name> | package:<name>] [--review full|lean|solo]`; project artifacts referenced below; user decisions and approvals before writes.
- Outputs: Primary artifacts, reports, or conversation guidance described below; write files only after user approval.
- Memory-bank writes: None.
- Next steps: Follow the workflow hand-off or next-step guidance below; recommendations do not auto-run and require explicit user command/approval.

## Phase 0: Domain Routing

Detect the project domain before generating specs:
- `design/cdd/game-concept.md` -> **[Game]** keep the existing visual/game asset specification workflow for sprites, meshes, VFX, audio, UI assets, levels, and engine constraints.
- `design/cdd/product-concept.md` -> **[Product]** use this same command for product artifact specs: API schema files, CLI help output, SDK examples, docs assets, UI screenshots, config samples, migration artifacts, and deployment/package deliverables.
- If unclear, ask which artifact family is being specified.

Do not remove game asset examples. Product artifacts are an additional spec family.

## Dual-Domain Parity Contract

Keep both branches inside this command:

| Area | Game branch | Product branch |
|------|-------------|----------------|
| Context reads | `design/cdd/game-concept.md`, target CDD/level/character doc, `design/art/art-bible.md`, `standards/technical-preferences.md`, existing asset manifest/specs | `design/cdd/product-concept.md`, module CDD, `design/ux/interaction-patterns.md`, optional `design/brand/style-guide.md`, optional `design/design-system.md`, `standards/technical-preferences.md`, architecture/ADR docs, existing artifact manifest/specs |
| Steps | Identify visual/audio/VFX/UI/3D assets, confirm list, generate art and technical specs, resolve art/tech conflicts, write specs and manifest | Identify API/CLI/SDK/docs/config/migration/deployment/package/UI artifacts, confirm list, generate contract and operational specs, resolve implementation/docs/deploy conflicts, write specs and manifest |
| Outputs | `design/assets/specs/[target]-assets.md` plus `design/assets/asset-manifest.md` entries | `design/assets/specs/[target]-artifacts.md` plus `design/assets/asset-manifest.md` entries for product artifacts |
| Next steps | `/asset-spec [next-context]`, `/asset-audit`, `/team-polish` for asset quality | `/asset-spec [next-artifact]`, `/asset-audit`, `/test-evidence-review`, `/release-checklist` |

If no argument is provided, check whether `design/assets/asset-manifest.md` exists:
- If it exists: read it, find the first context (system/level/character) with any asset at status "Needed" but no spec file written yet, and use `AskUserQuestion`:
  - Prompt: "The next unspecced context is **[target]**. Generate asset specs for it?"
  - Options: `[A] Yes — spec [target]` / `[B] Pick a different target` / `[C] Stop here`
- If no manifest: fail with:
  > "Usage: `/asset-spec system:<name>` — e.g., `/asset-spec system:tower-defense`
  > Or: `/asset-spec level:iron-gate-fortress` / `/asset-spec character:frost-warden`
  > Product examples: `/asset-spec api:billing` / `/asset-spec cli:import` / `/asset-spec migration:accounts-v2`
  > Run after the relevant concept, CDD, and domain standards are approved."

---

## Phase 0: Parse Arguments

Extract:
- **Target type**: `system`, `level`, `character`, `api`, `cli`, `sdk`, `docs`, `config`, `migration`, `deployment`, `package`, or `ui`
- **Target name**: the name after the colon (normalize to kebab-case)
- **Review mode**: `--review [full|lean|solo]` if present

**Mode behavior:**
- **Game full** (default): spawn both `art-director` and `technical-artist` in parallel
- **Game lean**: spawn `art-director` only — faster, skips technical constraint pass
- **Game solo**: no agent spawning — main session writes specs from art bible rules alone. Use for simple asset categories or when speed matters more than depth
- **Product full** (default): spawn `lead-programmer`, `devops-engineer` when deployment/package/migration is involved, and `ux-designer` when API/CLI/UI/docs consumer behavior is involved
- **Product lean**: spawn only the primary owner (`lead-programmer` for contracts/code artifacts, `devops-engineer` for deployment/package/migration, `ux-designer` for docs/help/UI artifacts)
- **Product solo**: derive specs from CDD, architecture, interaction patterns, and technical preferences; flag missing specialist review in the output

---

## Phase 1: Gather Context

Read all source material **before** asking the user anything.

### Game Required Reads:
- **Art bible**: Read `design/art/art-bible.md` — fail if missing:
  > "No art bible found. Run `/art-bible` first — asset specs are anchored to the art bible's visual rules and asset standards."
  Extract: Visual Identity Statement, Color System (semantic colors), Shape Language, Asset Standards (Section 8 — dimensions, formats, polycount budgets, texture resolution tiers).

- **Technical preferences**: Read `standards/technical-preferences.md` — extract performance budgets and naming conventions.

### Product Required Reads:
- **Product concept**: Read `design/cdd/product-concept.md` — extract core promise, users, product surface profile, MVP scope, anti-goals, and public artifact categories.
- **Interaction patterns**: Read `design/ux/interaction-patterns.md` when the artifact affects API consumers, CLI users, SDK integrators, docs readers, or UI workflows. If missing, warn and recommend `/ux-design interaction-patterns`; do not fail internal headless artifacts solely for this.
- **Product style references**: Read `design/brand/style-guide.md` if present. For UI-heavy artifacts, read `design/design-system.md` if present.
- **Technical preferences**: Read `standards/technical-preferences.md` — extract language, framework, build system, package manager, naming conventions, deployment target, and test framework.
- **Architecture and ADRs**: Read `docs/architecture/architecture.md` and relevant `docs/architecture/adr-*.md` files when the artifact affects contracts, deployment, migrations, auth, data, or packaging.

### Source doc reads (by target type):
- **system**: Read `design/cdd/[target-name].md`. Extract the **Visual/Audio Requirements** section. If it doesn't exist or reads `[To be designed]`:
  > "The Visual/Audio section of `design/cdd/[target-name].md` is empty. Either run `/design-system [target-name]` to complete the CDD, or describe the visual needs manually."
  Use `AskUserQuestion`: `[A] Describe needs manually` / `[B] Stop — complete the CDD first`
- **level**: Read `design/levels/[target-name].md`. Extract art requirements, asset list, VFX needs, and the art-director's production concept specs from Step 4.
- **character**: Read `design/narrative/characters/[target-name].md` or search `design/narrative/` for the character profile. Extract visual description, role, and any specified distinguishing features.
- **api**: Read the owning module CDD and existing `docs/api/**/*`, `openapi.*`, `schema/**/*`, or API source contracts. Extract endpoint names, request/response bodies, error envelopes, auth, pagination, rate limits, idempotency, and examples.
- **cli**: Read the owning module CDD and existing CLI docs/source. Extract commands, flags, positional arguments, stdin/stdout/stderr behavior, prompts, exit codes, help text, config/env interactions, and examples.
- **sdk**: Read module CDD, architecture, package docs, and example snippets. Extract public functions/classes, typed errors, versioning, deprecation behavior, install/import shape, examples, and compatibility promises.
- **docs**: Read Product Concept, CDDs, UX specs, README/docs tree, and release notes. Extract pages, diagrams, screenshots, examples, tutorials, reference docs, and support/onboarding handoff.
- **config**: Read technical preferences, architecture, sample config files, and deployment docs. Extract required keys, defaults, validation rules, secrets policy, environment overrides, and examples.
- **migration**: Read data CDDs, architecture, ADRs, and existing migrations. Extract schema changes, forward/reverse behavior, dry-run requirements, data safety checks, rollback plan, and release sequencing.
- **deployment**: Read architecture, CI/CD config, infrastructure files, and release docs. Extract artifacts, environments, health checks, rollback, monitoring, secrets, smoke checks, and on-call handoff.
- **package**: Read package manifests, build config, release docs, and module CDDs. Extract package names, versioning, contents, install/upgrade behavior, signing, checksums, license files, and distribution targets.
- **ui**: Read UI module CDDs, UX specs, `design/ux/interaction-patterns.md`, and `design/design-system.md` if present. Extract screens, components, states, responsive constraints, accessibility, localization, and screenshot/docs artifacts.

### Optional reads:
- **Existing manifest**: Read `design/assets/asset-manifest.md` if it exists — extract already-specced assets for this target to avoid duplicates.
- **Related specs**: Glob `design/assets/specs/*.md` — scan for assets that could be shared (e.g., a common UI element specced for one system might apply here too).

### Present context summary:
> **Asset Spec: [Target Type] — [Target Name]**
> - Source doc: [path] — [N] asset types identified
> - Art bible: found — Asset Standards at Section 8
> - Existing specs for this target: [N already specced / none]
> - Shared assets found in other specs: [list or "none"]

---

## Phase 2: Asset Identification

From the source doc, extract every asset type mentioned — explicit and implied.

**For systems**: look for VFX events, sprite references, UI elements, audio triggers, particle effects, icon needs, and any "visual feedback" language.

**For levels**: look for unique environment props, atmospheric VFX, lighting setups, ambient audio, skybox/background, and any area-specific materials.

**For characters**: look for sprite sheets (idle, walk, attack, death), portrait/avatar, VFX attached to abilities, UI representation (icon, health bar skin).

**For product artifacts**:
- API: schema files, request/response examples, error examples, auth docs, OpenAPI fragments, contract tests, generated clients.
- CLI: help output, command examples, shell completion, manpage/reference docs, install scripts, config samples, golden output snapshots.
- SDK/library: package metadata, typed examples, docs snippets, compatibility matrix, deprecation notes, generated docs, test fixtures.
- Docs/onboarding: diagrams, screenshots, tutorials, reference pages, release note snippets, support handoff docs.
- Config/migration/deployment/package: sample files, migration scripts, rollback notes, health checks, package manifests, checksums, release bundles.

Group assets into categories:
- **Sprite / 2D Art** — character sprites, UI icons, tile sheets
- **VFX / Particles** — hit effects, ambient particles, screen effects
- **Environment** — props, tiles, backgrounds, skyboxes
- **UI** — HUD elements, menu art, fonts (if custom)
- **Audio** — SFX, music tracks, ambient loops *(note: audio specs are descriptions only — no generation prompts)*
- **3D Assets** — meshes, materials (if applicable per engine)

Present the full identified list to the user. Use `AskUserQuestion`:
- Prompt: "I identified [N] assets across [N] categories for **[target]**. Review before speccing:"
- Show the grouped list in conversation text first
- Options: `[A] Proceed — spec all of these` / `[B] Remove some assets` / `[C] Add assets I didn't catch` / `[D] Adjust categories`

Do NOT proceed to Phase 3 without user confirmation of the asset list.

---

## Phase 3: Spec Generation

Spawn specialist agents based on review mode. **Issue all Task calls simultaneously — do not wait for one before starting the next.**

### Full mode — spawn in parallel:

**`art-director`** via Task:
- Provide: full asset list from Phase 2, art bible Visual Identity Statement, Color System, Shape Language, the source doc's visual requirements, and any reference games/art mentioned in the art bible Section 9
- Ask: "For each asset in this list, produce: (1) a 2–3 sentence visual description anchored to the art bible's shape language and color system — be specific enough that two different artists would produce consistent results; (2) a generation prompt ready for use with AI image tools (Midjourney/Stable Diffusion style — include style keywords, composition, color palette anchors, negative prompts); (3) which art bible rules directly govern this asset (cite by section). For audio assets, describe the sonic character instead of a generation prompt."

**`technical-artist`** via Task:
- Provide: full asset list, art bible Asset Standards (Section 8), technical-preferences.md performance budgets, engine name and version
- Ask: "For each asset in this list, specify: (1) exact dimensions or polycount (match the art bible Asset Standards tiers — do not invent new sizes); (2) file format and export settings; (3) naming convention (from technical-preferences.md); (4) any engine-specific constraints this asset type must respect; (5) LOD requirements if applicable. Flag any asset type where the art bible's preferred standard conflicts with the engine's constraints."

### Lean mode — spawn art-director only (skip technical-artist).

### Solo mode — skip both. Derive specs from art bible rules alone, noting that technical constraints were not validated.

### Product full mode — spawn applicable owners in parallel:

**`lead-programmer`** via Task:
- Provide: product artifact list, module CDD requirements, architecture/ADR constraints, interaction patterns, technical preferences, and any existing contracts.
- Ask: "For each product artifact, produce an implementation-ready contract specification: file path, public shape, schema/help/example requirements, validation behavior, compatibility/versioning notes, tests required, and traceability to CDD/ADR requirements. Flag contradictions between docs, code, and architecture."

**`devops-engineer`** via Task when target type is `deployment`, `package`, `migration`, `config`, or release bundle:
- Provide: artifact list, deployment target, CI/CD/build system, architecture constraints, rollback requirements, and release checklist expectations.
- Ask: "For each operational artifact, specify exact file/output shape, environment assumptions, secrets policy, health/smoke checks, rollback or dry-run behavior, packaging/signing/checksum requirements, and evidence required before release."

**`ux-designer`** via Task when target type is `api`, `cli`, `sdk`, `docs`, or `ui`:
- Provide: interaction patterns, product concept, target user/integrator, artifact list, and docs/help requirements.
- Ask: "For each consumer-facing artifact, specify examples, help/error copy, onboarding path, empty/error/recovery states, accessibility/docs handoff, and how a user or integrator validates success."

### Product lean mode — spawn only the most relevant owner for the selected target type.

### Product solo mode — skip agents and derive the artifact specs from CDDs, architecture, interaction patterns, and technical preferences. Mark missing specialist review explicitly.

**Collect both responses before Phase 4.** If any conflict exists between art-director and technical-artist (e.g., art-director specifies 4K textures but technical-artist flags the engine budget requires 512px), surface it explicitly — do NOT silently resolve.

---

## Phase 4: Compile and Review

Combine the agent outputs into a draft spec per asset. Present all specs in conversation text using this format:

```
## ASSET-[NNN] — [Asset Name]

| Field | Value |
|-------|-------|
| Category | [Sprite / VFX / Environment / UI / Audio / 3D] |
| Dimensions | [e.g. 256×256px, 4-frame sprite sheet] |
| Format | [PNG / SVG / WAV / etc.] |
| Naming | [e.g. vfx_frost_hit_01.png] |
| Polycount | [if 3D — e.g. <800 tris] |
| Texture Res | [e.g. 512px — matches Art Bible §8 Tier 2] |

**Visual Description:**
[2–3 sentences. Specific enough for two artists to produce consistent results.]

**Art Bible Anchors:**
- §3 Shape Language: [relevant rule applied]
- §4 Color System: [color role — e.g. "uses Threat Blue per semantic color rules"]

**Generation Prompt:**
[Ready-to-use prompt. Include: style keywords, composition notes, color palette anchors, lighting direction, negative prompts.]

**Status:** Needed
```

After presenting all specs, use `AskUserQuestion`:
- Prompt: "Asset specs for **[target]** — [N] assets. Review complete?"
- Options: `[A] Approve all — write to file` / `[B] Revise a specific asset` / `[C] Regenerate with different direction`

If [B]: ask which asset and what to change. Revise inline and re-present. Do NOT re-spawn agents for minor text revisions — only re-spawn if the visual direction itself needs to change.

If [C]: ask what direction to change. Re-spawn the relevant agent with the updated brief.

For product artifacts, use this equivalent draft format:

```markdown
## ARTIFACT-[NNN] — [Artifact Name]

| Field | Value |
|-------|-------|
| Category | [API schema / CLI help / SDK example / Docs asset / Config sample / Migration / Deployment / Package / UI screenshot] |
| Output Path | [expected path] |
| Owner | [lead-programmer / devops-engineer / ux-designer / docs owner] |
| Source Requirement | [CDD/ADR/story ID] |
| Validation Evidence | [contract test / CLI golden output / migration dry-run / deployment smoke / docs review] |
| Compatibility Notes | [versioning, deprecation, rollback, platform, package manager] |

**Specification:**
[Implementation-ready artifact requirements.]

**Acceptance Checks:**
- [check 1]
- [check 2]

**Status:** Needed
```

---

## Phase 5: Write Spec File

After approval, ask:
- Game: "May I write the spec to `design/assets/specs/[target-name]-assets.md`?"
- Product: "May I write the spec to `design/assets/specs/[target-name]-artifacts.md`?"

Write the file with:

```markdown
# Asset Specs — [Target Type]: [Target Name]

> **Source**: [path to source GDD/level/character doc]
> **Art Bible**: design/art/art-bible.md
> **Generated**: [date]
> **Status**: [N] assets specced / [N] approved / [N] in production / [N] done

[all asset specs in ASSET-NNN format]
```

For product projects, write:

```markdown
# Product Artifact Specs — [Target Type]: [Target Name]

> **Source**: [path to source CDD/ADR/UX/release doc]
> **Interaction Patterns**: design/ux/interaction-patterns.md if applicable
> **Technical Preferences**: standards/technical-preferences.md
> **Generated**: [date]
> **Status**: [N] artifacts specced / [N] approved / [N] implemented / [N] verified

[all artifact specs in ARTIFACT-NNN format]
```

Then update `design/assets/asset-manifest.md`. If it doesn't exist, create it:

```markdown
# Asset Manifest

> Last updated: [date]

## Progress Summary

| Total | Needed | In Progress | Done | Approved |
|-------|--------|-------------|------|----------|
| [N] | [N] | [N] | [N] | [N] |

## Assets by Context

### [Target Type]: [Target Name]
| Asset ID | Name | Category | Status | Spec File |
|----------|------|----------|--------|-----------|
| ASSET-001 | [name] | [category] | Needed | design/assets/specs/[target]-assets.md |
```

If the manifest already exists, append the new context block and update the Progress Summary counts.

Ask: "May I update `design/assets/asset-manifest.md`?"

---

## Phase 6: Close

Use `AskUserQuestion`:
- Prompt: "Asset specs complete for **[target]**. What's next?"
- Options:
  - `[A] Spec another system — /asset-spec system:[next-system]`
  - `[B] Spec a level — /asset-spec level:[level-name]`
  - `[C] Spec a character — /asset-spec character:[character-name]`
  - `[D] Spec a product artifact — /asset-spec api:[name] or /asset-spec cli:[name]`
  - `[E] Run /asset-audit — validate delivered assets/artifacts against specs`
  - `[F] Run /test-evidence-review — verify contract, migration, package, or docs evidence`
  - `[G] Stop here`

---

## Asset ID Assignment

Asset IDs are assigned sequentially across the entire project — not per-context. Read the manifest before assigning IDs to find the current highest number:

```
Grep pattern="ASSET-" path="design/assets/asset-manifest.md"
```

Start new assets from `ASSET-[highest + 1]`. This ensures IDs are stable and unique across the whole project.

If no manifest exists yet, start from `ASSET-001`.

---

## Shared Asset Protocol

Before speccing an asset, check if an equivalent already exists in another context's spec:

- Common UI elements (health bars, score displays) are often shared across systems
- Generic environment props may appear in multiple levels
- Character VFX (hit sparks, death effects) may reuse a base spec with color variants

If a match is found: reference the existing ASSET-ID rather than creating a duplicate. Note the shared usage in the manifest's referenced-by column.

> "ASSET-012 (Generic Hit Spark) already specced for Combat system. Reusing for Tower Defense — adding tower-defense to referenced-by."

---

## Error Recovery Protocol

If any spawned agent returns BLOCKED or cannot complete:

1. Surface immediately: "[AgentName]: BLOCKED — [reason]"
2. In `lean` mode or if `technical-artist` blocks: proceed with art-director output only — note that technical constraints were not validated
3. In `solo` mode or if `art-director` blocks: derive descriptions from art bible rules — flag as "Art director not consulted — verify against art bible before production"
4. Always produce a partial spec — never discard work because one agent blocked

---

## Collaborative Protocol

Every phase follows: **Identify → Confirm → Generate → Review → Approve → Write**

- Never spec assets without first confirming the asset list with the user
- Always anchor game specs to the art bible — a game asset spec that contradicts the art bible is wrong
- Always anchor product specs to the Product Concept, interaction patterns, architecture/ADRs, and technical preferences — a product artifact spec that contradicts those sources is wrong
- Surface all agent disagreements — do not silently pick one
- Write the spec file only after explicit approval
- Update the manifest immediately after writing the spec

---

## Recommended Next Steps

- Run `/asset-spec [next-context]` to continue speccing remaining systems, levels, or characters
- Run `/asset-spec api:[name]`, `/asset-spec cli:[name]`, `/asset-spec migration:[name]`, or another product target to continue product artifact coverage
- Run `/asset-audit` to validate delivered assets/artifacts against the written specs and identify gaps or mismatches
- Run `/test-evidence-review` for product contract, migration, package, deployment, and docs evidence before release
