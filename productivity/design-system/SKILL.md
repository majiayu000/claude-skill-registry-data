---
name: design-system
description: "Use this skill when authoring or retrofitting the CDD for one module listed in design/cdd/module-index.md, including dependencies, behavior, data, edge cases, and acceptance criteria."
argument-hint: "<module-name> | retrofit <cdd-path> | sync <scope> [--review full|lean|solo]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Edit, Task, AskUserQuestion, TodoWrite
---

## Scope, evidence and effects

Read `standards/evidence-lifecycle.md` and `standards/notes-adr-sync.md` from the
project root. Reuse explicit existing authorization for its named paths, effects
and limits across roles and retries. Present unresolved material choices or new
effects for approval; a document/batch/synchronization authorization does not
require another question for each covered section or file. Content agreement,
write authority, independent review, ADR acceptance and workflow completion
remain separate.

Analysis defaults to read-only: no write entrypoint, input edits, status/index/
session/Memory Bank updates. Report-only may write one new assigned report with
authority; report approval does not authorize indexes or rolling logs. Other
writes need the named path/effect in existing authority or a concrete draft and
changeset approval. Unknown paths are findings, not permission to create them.
No Memory Bank means use the established report/conversation fallback. Next
steps are recommendations; execute only effects already authorized or explicitly
selected by the user. Tool availability determines the question interface.

Bind claims to a declared scope and minimum direct/indirect evidence closure:
record original paths, full SHA-256, byte sizes, source commit plus exact diff
and uncommitted/ignored/external identities, exclusions and recoverable originals.
Do not read sensitive local settings or secrets merely to complete discovery.
Read required inputs back from their actual paths, verify closure and report
missing inputs as incomplete affected checks. Keywords, timestamps, counts,
equal hashes at two collections and static checks do not certify semantic review,
continuous unchanged history, runtime behavior or independent approval.

Classify meaningful choices with the shared disposition record (`cdd-layer`,
`no-adr`, `covered`, `documentation-update`, `adr-required`, `conflict`). Significant
trust, public contract, durable format or state ownership changes require an
Accepted ADR/valid scoped exception before affected implementation continues.
Keep As-Is observations and their evidence separate from Target promises and
gaps; implemented behavior cannot lower a governing Target. Continue independent
work while blocking only affected dependants.

Trace observed defaults and behavior through the actual owning public entrypoint,
argument/configuration parsing and call flow. Record each entrypoint's effective
value and explicit overrides separately. A private helper's default argument is
not evidence of a different public default when the caller passes its own value;
do not invent a Target mismatch from that default alone.

## User Guide

- When to use: Guided, section-by-section CDD authoring for a single module. Gathers context from existing docs, walks through each required section collaboratively, cross-references dependencies, and writes incrementally to file. Supports both game and general product domains.
- Inputs: Command arguments: `/design-system <module-name> [--review full|lean|solo]`; project artifacts referenced below; user decisions and approvals before writes.
- Outputs: Primary artifacts, reports, or conversation guidance described below; write files only after user approval.
- Memory-bank writes: None.
- Next steps: Follow the workflow hand-off or next-step guidance below; recommendations do not auto-run and require explicit user command/approval.

When this skill is invoked:

**Domain detection.** The concept document reveals the domain:
- **游戏专用**: Read `design/cdd/game-concept.md` — concept contains game-specific sections (Core Loop, MDA analysis, player types) → use game CDD section names (Player Fantasy, Detailed Rules, Formulas, Tuning Knobs, Visual/Audio)
- **通用产品**: Read `design/cdd/product-concept.md` — concept contains product-specific sections (User Journey, JTBD, user personas) → use product CDD section names (User Promise, Detailed Design, Data Model, Configuration, Integration)

Sections below are marked **[通用场景]**, **[游戏专用]**, or **[通用产品]**.

## 1. Parse Arguments & Validate

Resolve the review mode (once, store for all gate spawns this run):
1. If `--review [full|lean|solo]` was passed → use that
2. Else read `production/review-mode.txt` → use that value
3. Else → default to `lean`

See `standards/director-gates.md` for the full check pattern.

Validate supplied/global values: only `full`, `lean` and `solo` are valid.
An invalid value is an error naming its source; request correction and do not
silently substitute a default. Lean is the fallback only when no value exists.

A module name or retrofit path is **required**. If missing:

1. Check if `design/cdd/module-index.md` exists.
2. If it exists: read it, find the highest-priority module with status "Not Started" or equivalent, and use `AskUserQuestion`:
   - Prompt: "The next module in your design order is **[module-name]** ([priority] | [layer]). Start designing it?"
   - Options: `[A] Yes — design [module-name]` / `[B] Pick a different module` / `[C] Stop here`
   - If [A]: proceed with that module name. If [B]: ask which module to design (plain text). If [C]: exit.
3. If no module index exists, fail with:
   > "Usage: `/design-system <module-name>` — e.g., `/design-system movement`
   > Or to fill gaps in an existing CDD: `/design-system retrofit design/cdd/[module-name].md`
   > No module index found. Run `/map-systems` first to map your modules and get the design order."

**Route dispatcher:** Choose exactly one route before file naming or authoring:
`sync <scope>`, existing-file `retrofit <cdd-path>`/CDD path, or new module.
`sync` without a nonempty concrete scope and `retrofit` without a path are usage
errors. Give legal usage/correction, then stop before spawn/write/verdict.
Accept documented `--review full|lean|solo` only; reject unknown explicit flags
before any default/route selection. Preserve existing valid invocations.

**Detect synchronization mode:** `/design-system sync <scope>` reconciles
implementation-first changes with existing CDDs as one bounded batch. Existing
module/`retrofit`/CDD-path invocations remain supported. Resolve the user's scope
to actual paths/effects before writing: implementation inputs, affected CDD
sections, Notes/ADRs, registry/traceability/module-index effects if authorized,
exclusions, writer and required independent reviewer.

1. Collect a fixed source commit and exact committed/staged/unstaged diffs plus
   full hashes/sizes/original-path identities for untracked, ignored and external
   relied-on inputs. A commit or `HEAD` alone is not the working-tree baseline.
   Retain recoverable before/after bytes for changed documents and evidence.
2. Read affected source, tests, governing CDDs, Accepted ADRs and their required
   indirect attachments to the minimum closure. Record unresolved or unknown
   paths without writing them. Do not read sensitive settings for discovery.
3. Map actual bodies to the resolved document kind's owner set in
   `design/INSTRUCTIONS.md` (semantic eight for module CDDs), including existing aliases. Separate As-Is behavior from Target requirements; show
   mismatches and evidence. Preserve unaffected content and original Game examples.
4. Classify decisions under `standards/notes-adr-sync.md`. Resolve material
   `adr-required`/`conflict` choices before affected implementation proceeds;
   documentation synchronization does not accept an ADR.
5. Show concrete old/new sections and the complete named path/effect list when
   approval is missing. Continue within existing approved batch scope; ask only
   unresolved material choices/new effects. Apply incremental edits; never
   replace existing files with new skeletons.
6. Read back exact resulting bytes and required closure. Record author self-checks
   separately from independent review. Bind a non-writing reviewer's required
   semantic review to the exact manifest/inputs; any repair changes the baseline
   and requires fresh review of affected inputs. Missing required review stays
   incomplete. Batch completion reports written paths, findings, dispositions,
   verification limits and remaining owners; no implicit Story/phase/publication
   completion or index/session updates.

After sync steps 1–6, report the batch result and **return from the skill**.
This independent route may reuse applicable Phase 2 reads and Phase 5 readback/
selected-mode validation for its bound existing files; it never falls through
to retrofit detection, module-name normalization, new skeleton creation or the
new-module section cycle below.

**Detect retrofit mode (dispatcher selected retrofit only):**
If the argument starts with `retrofit` or the argument is a file path to an
existing `.md` file in `design/cdd/`, enter **retrofit mode**:

1. Read the existing CDD file.
2. Verify from workflow/provenance and the full body that the existing target
   is a **module CDD** under `design/INSTRUCTIONS.md`'s kind routing before any
   retrofit edit. For Concept, Module Index, Quick Spec or another non-module
   kind, report its actual owner route (/brainstorm, /map-systems, /quick-design
   or the resolved owner), show legal module retrofit usage and return without
   edits. Unknown kind requests clarification, never defaults to Module8.
   For a verified Game/Product module, map its substantive bodies to the semantic
   eight roles, retaining existing headings/aliases. The separate sync batch
   route may handle multiple kinds through their own resolved owner sets.
3. Identify missing/placeholder/unresolved roles through actual content and
   required evidence, not heading presence or single-line/length heuristics.
4. Present to the user before doing anything:
   ```
   ## Retrofit: [System Name]
   File: design/cdd/[filename].md

   Sections already written (preserved unless explicitly in the requested update):
   ✓ [section name]
   ✓ [section name]

   Missing or incomplete sections (will be authored):
   ✗ [section name] — missing
   ✗ [section name] — placeholder only
   ```
5. If authority is absent, show the named missing/selected sections and ask:
   "May I fill these gaps or revise these selected sections at [path]?" Reuse
   existing scope; preserve all other content.
6. Within approved scope, proceed to **Phase 2**; skip the existing-file
   skeleton in **Phase 3** and author only named missing/incomplete or explicitly
   selected substantive sections in **Phase 4**.
7. Preserve existing section content outside the authorized change. Fill
   placeholders or edit specifically approved substantive sections in place;
   never recreate a retrofit file as a skeleton.

Only when the dispatcher selected **new module**, normalize the system name to
kebab-case for its filename (e.g., "combat system" becomes `combat-system`).
This step is unreachable for sync and retrofit.

---

## 2. Gather Context (Read Phase)

Read all relevant context **before** asking the user anything. This is the skill's
primary advantage over ad-hoc design — it arrives informed.

### 2a: Required Reads

- **Concept document**: Read the appropriate concept document based on domain:
  - **游戏专用**: Read `design/cdd/game-concept.md`
  - **通用产品**: Read `design/cdd/product-concept.md`
  > If missing: "No concept document found. Run `/brainstorm` first."
- **Module index**: Read `design/cdd/module-index.md` — fail if missing:
  > "No module index found at `design/cdd/module-index.md`. Run `/map-systems` first to map your modules."
- **Target system**: Find the system in the index. If not listed, warn:
  > "[system-name] is not in the module index. Would you like to add it, or
  > design it as an off-index system?"
- **Entity registry**: Read `design/registry/entities.yaml` if it exists.
  Extract all entries referenced by or relevant to this system (grep
  `referenced_by.*[system-name]` and `source.*[system-name]`). Hold these
  in context as **known facts** — values that other CDDs have already
  established and this CDD must not contradict.
- **Reflexion log**: Read `docs/consistency-failures.md` if it exists.
  Extract entries whose Domain matches this system's category. These are
  recurring conflict patterns — present them under "Past failure patterns"
  in the Phase 2d context summary so the user knows where mistakes have
  occurred before in this domain.

### 2b: Dependency Reads

From the module index, identify:
- **Upstream dependencies**: Systems this one depends on. Read their CDDs if they
  exist (these contain decisions this system must respect).
- **Downstream dependents**: Systems that depend on this one. Read their CDDs if
  they exist (these contain expectations this system must satisfy).

For each dependency CDD that exists, extract and hold in context:
- Key interfaces (what data flows between the systems)
- Formulas that reference this system's outputs
- Edge cases that assume this system's behavior
- Tuning knobs that feed into this system

### 2c: Optional Reads

- **Game pillars**: Read `design/cdd/game-pillars.md` if it exists
- **Existing CDD**: Read `design/cdd/[system-name].md` if it exists (resume, don't
  restart from scratch)
- **Related CDDs**: Glob `design/cdd/*.md` and read any that are thematically related
  (e.g., if designing a system that overlaps with another in scope, read the related CDD
  even if it's not a formal dependency)

### 2d: Present Context Summary

Before starting design work, present a brief summary to the user:

> **Designing: [System Name]**
> - Priority: [from index] | Layer: [from index]
> - Depends on: [list, noting which have CDDs vs. undesigned]
> - Depended on by: [list, noting which have CDDs vs. undesigned]
> - Existing decisions to respect: [key constraints from dependency CDDs]
> - Pillar alignment: [which pillar(s) this system primarily serves]
> - **Known cross-system facts (from registry):**
>   - [entity_name]: [attribute]=[value], [attribute]=[value] (owned by [source CDD])
>   - [item_name]: [attribute]=[value], [attribute]=[value] (owned by [source CDD])
>   - [formula_name]: variables=[list], output=[min–max] (owned by [source CDD])
>   - [constant_name]: [value] [unit] (owned by [source CDD])
>   *(These values are locked — if this CDD needs different values, surface
>   the conflict before writing. Do not silently use different numbers.)*
>
> If no registry entries are relevant: omit the "Known cross-system facts" section.

If any upstream dependencies are undesigned, warn:
> "[dependency] doesn't have a CDD yet. We'll need to make assumptions about
> its interface. Consider designing it first, or we can define the expected
> contract and flag it as provisional."

### 2e: Technical Feasibility Pre-Check

Before asking the user to begin designing, load technology context and surface
any constraints or knowledge gaps that will shape the design. Use the detected
domain from Phase 2.

**[游戏专用] Step 1 — Determine the engine domain for this system:**
Map the system's category (from `module-index.md`) to an engine domain:

| System Category | Engine Domain |
|----------------|--------------|
| Combat, physics, collision | Physics |
| Rendering, visual effects, shaders | Rendering |
| UI, HUD, menus | UI |
| Audio, sound, music | Audio |
| AI, pathfinding, behavior trees | Navigation / Scripting |
| Animation, IK, rigs | Animation |
| Networking, multiplayer, sync | Networking |
| Input, controls, keybinding | Input |
| Save/load, persistence, data | Core |
| Dialogue, quests, narrative | Scripting |

**[通用产品] Step 1 — Determine the stack domain for this module:**
Map the module's category (from `module-index.md`) to a stack domain:

| Module Category | Stack Domain |
|----------------|--------------|
| Foundation/Infrastructure, config, logging, error handling | Framework / Runtime |
| API, web services, request handling | API Design / Framework |
| Data models, schemas, storage | Data Storage / ORM |
| Auth, permissions, security | Auth / Security |
| UI, frontend, user-facing interfaces | Frontend / UI |
| CLI, tooling, developer-facing | CLI / Distribution |
| Data pipelines, ETL, analytics | Data Pipeline / Analytics |
| Integration, webhooks, third-party APIs | Integration / Messaging |
| Performance, caching, optimization | Performance / Caching |

**[游戏专用] Step 2 — Read engine context (if available):**
- Read `standards/technical-preferences.md` to identify the engine and version
- If engine is configured, read `docs/engine-reference/[engine]/VERSION.md`
- Read `docs/engine-reference/[engine]/modules/[domain].md` if it exists
- Read `docs/engine-reference/[engine]/breaking-changes.md` for domain-relevant entries
- Glob `docs/architecture/adr-*.md` and read any ADRs whose domain matches
  (check the Engine Compatibility table's "Domain" field)

**[通用产品] Step 2 — Read stack context (if available):**
- Read `standards/technical-preferences.md` to identify the language, framework,
  runtime, database, and pinned versions
- If stack reference docs are configured, read `docs/reference/[stack]/VERSION.md`
- Read `docs/reference/[stack]/modules/[domain].md` if it exists
- Read `docs/reference/[stack]/breaking-changes.md` for domain-relevant entries
- Glob `docs/architecture/adr-*.md` and read any ADRs whose domain matches
  (check the Technology Compatibility table's "Domain" field)

**Step 3 — Present the Feasibility Brief:**

**[游戏专用]** If engine reference docs exist, present before starting design:

```
## Technical Feasibility Brief: [System Name]
Engine: [name + version]
Domain: [domain]

### Known Engine Capabilities (verified for [version])
- [capability relevant to this system]
- [capability 2]

### Engine Constraints That Will Shape This Design
- [constraint from engine-reference or existing ADR]

### Knowledge Gaps (verify before committing to these)
- [post-cutoff feature this design might rely on — mark HIGH/MEDIUM risk]

### Existing ADRs That Constrain This System
- ADR-XXXX: [decision summary] — means [implication for this CDD]
  (or "None yet")
```

**[通用产品]** If stack reference docs exist, present before starting design:

```
## Technical Feasibility Brief: [Module Name]
Stack: [language] + [framework/runtime] [version]
Domain: [domain]

### Known Stack Capabilities (verified for [version])
- [capability relevant to this module]
- [capability 2]

### Stack Constraints That Will Shape This Design
- [constraint from stack reference or existing ADR]

### Knowledge Gaps (verify before committing to these)
- [post-cutoff framework/API behavior this design might rely on — mark HIGH/MEDIUM risk]

### Existing ADRs That Constrain This Module
- ADR-XXXX: [decision summary] — means [implication for this CDD]
  (or "None yet")
```

**[游戏专用]** If no engine reference docs exist (engine not yet configured), show a short note:
> "No engine configured yet — skipping technical feasibility check. Run
> `/setup-engine` before moving to architecture if you haven't already."

**[通用产品]** If no stack reference docs exist (stack not yet configured), show a short note:
> "No technology stack configured yet — skipping technical feasibility check. Run
> `/setup-engine` before moving to architecture if you haven't already."

**Step 4 — Ask before proceeding:**

Use `AskUserQuestion`:
- "Any constraints to add before we begin, or shall we proceed with these noted?"
  - Options: "Proceed with these noted", "Add a constraint first", "I need to check the technology docs — pause here"

---

Use `AskUserQuestion`:
- "Ready to start designing [system-name]?"
  - Options: "Yes, let's go", "Show me more context first", "Design a dependency first"

---

## 3. Create File Skeleton

Route guard: **new module only**. Retrofit skips this phase; sync returns from
its independent batch route and cannot enter Phases 3–4.

For a new CDD only, create the skeleton once its concrete output path/effect is
authorized. Existing CDDs use retrofit/sync and retain their bodies.

Use the inline skeleton below. Do not read an external CDD template file here;
the former external game design document template has been folded into this skill.

```markdown
# [System Name]

> **Status**: In Design
> **Author**: [user + agents]
> **Last Updated**: [today's date]
> **Implements Pillar**: [from context]

## Overview

[To be designed]

## Player Fantasy

[To be designed]

## Detailed Design

### Core Rules

[To be designed]

### States and Transitions

[To be designed]

### Interactions with Other Systems

[To be designed]

## Formulas

[To be designed]

## Edge Cases

[To be designed]

## Dependencies

[To be designed]

## Tuning Knobs

[To be designed]

## Visual/Audio Requirements

[To be designed]

## UI Requirements

[To be designed]

## Acceptance Criteria

```

[Product] For product CDDs, use this skeleton instead of the game skeleton above:

```markdown
# [Module Name]

> **Status**: In Design

## Overview
[To be designed]

## User Promise
[To be designed]

## Detailed Design
### Core Specification
[To be designed]
### States and Transitions
[To be designed]
### Interactions with Other Modules
[To be designed]

## Data Model
[To be designed]

## Edge Cases
[To be designed]

## Dependencies
[To be designed]

## Configuration
[To be designed]

## Integration Requirements
[To be designed]

## UI Requirements
[To be designed]

## Acceptance Criteria

[To be designed]

## Open Questions

[To be designed]
```

If the new-file effect is not already authorized, show the skeleton and ask:
"May I create the skeleton file at `design/cdd/[system-name].md`?"

After writing, choose one checkpoint branch from the existing exact path/effect
authorization for `production/session-state/active.md`:

- **Authorized checkpoint write:** only in this branch, use Glob to check whether
  the checkpoint exists. If it exists, Read it and use Edit for the authorized
  fields. If it does not exist, use Write only when creation is also covered by
  the existing scope; never Edit a missing file. If only an existing-file update
  was authorized, present the creation draft and obtain that new effect first.
- **No checkpoint write authority:** present the progress below in conversation
  only. Do not enter the checkpoint Glob/Write/Edit branch or create session
  state as a side effect of permission to write the CDD.

Progress fields (for either branch):
- Task: Designing [system-name] CDD
- Current section: Starting (skeleton created)
- File: design/cdd/[system-name].md

---

## 4. Section-by-Section Design

Walk through each section in order. For **each section**, follow this cycle:

### The Section Cycle

```
Context  ->  Questions  ->  Options  ->  Decision  ->  Draft  ->  Approval  ->  Write
```

1. **Context**: State what this section needs to contain, and surface any relevant
   decisions from dependency CDDs that constrain it.

2. **Questions**: Ask clarifying questions specific to this section. Use
   `AskUserQuestion` for constrained questions, conversational text for open-ended
   exploration.

3. **Options**: Where the section involves design choices (not just documentation),
   present 2-4 approaches with pros/cons. Explain reasoning in conversation text,
   then use `AskUserQuestion` to capture the decision.

4. **Decision**: User picks an approach or provides custom direction.

5. **Draft**: Write the section content in conversation text for review. Flag any
   provisional assumptions about undesigned dependencies.

6. **Approval**: Confirm that the draft/section write is within existing scope.
   Ask about unresolved material choices, uncovered writes or an explicit
   section-by-section preference, using `AskUserQuestion` when available:
   - Prompt: "Approve the [Section Name] section?"
   - Options: `[A] Approve — write it to file` / `[B] Make changes — describe what to fix` / `[C] Start over`
   Present the draft before requesting a new approval; covered incremental
   sections proceed without repeating the same authorization.

****

7. **Write**: Use Edit to fill the placeholder or apply the named scoped revision
   to an existing body; preserve other content and examples.
   **CRITICAL**: Always include the section heading in the `old_string` to ensure
   uniqueness — never match `[To be designed]` alone, as multiple sections use the
   same placeholder and the Edit tool requires a unique match. Use this pattern:
   ```
   old_string: "## [Section Name]\n\n[To be designed]"
   new_string: "## [Section Name]\n\n[approved content]"
   ```
   Confirm the write.

8. **Registry conflict check** (Sections C and D only — Detailed Design and Formulas):
   After writing, scan the section content for entity names, item names, formula
   names, and numeric constants that appear in the registry. For each match:
   - Compare the value just written against the registry entry.
   - If they differ: **surface the conflict immediately** before starting the next
     section. Do not continue silently.
     > "Registry conflict: [name] is registered in [source CDD] as [registry_value].
     > This section just wrote [new_value]. Which is correct?"
   - If new (not in registry): flag it as a candidate for registry registration
     (will be handled in Phase 5).

Record completed sections in conversation. Update `production/session-state/active.md`
only if that path/effect is authorized; create it only when creation is in scope.

### Section-Specific Guidance

Before drafting each Phase 4 section, read the matching heading in [section guidance](references/section-guidance.md). Load only the current section and detected domain branch. Its delegation, cross-reference and section-content guidance apply. Resolve its
approval/skeleton/ADR wording through this skill's continuing-scope contract and
`standards/notes-adr-sync.md`; an Integration section alone does not require an ADR.

## 5. Post-Design Validation

After all sections are written:

### 5a: Self-Check

Read back the complete CDD from file (not from conversation memory — the file is
the source of truth). Verify:
- Map all eight semantic roles to substantive Game/Product bodies under
  `design/INSTRUCTIONS.md`, retaining existing aliases; unresolved roles remain incomplete
- Formulas reference defined variables
- Edge cases have resolutions
- Dependencies are listed with interfaces
- Acceptance criteria are testable

### 5a-bis: Creative Director Pillar Review

**Review mode check** — apply before spawning CD-GDD-ALIGN:
- `solo` → skip. Note: "CD-GDD-ALIGN skipped — Solo mode." Proceed to Step 5b.
- `lean` → skip (not a PHASE-GATE). Note: "CD-GDD-ALIGN skipped — Lean mode." Proceed to Step 5b.
- `full` → spawn as normal.

Before finalizing the CDD, spawn `creative-director` via Task using gate **CD-GDD-ALIGN** (`standards/director-gates.md`).

Pass: completed CDD file path, project pillars/principles (from `design/cdd/game-concept.md`, `design/cdd/product-concept.md`, or `design/cdd/principles.md` if present).
- **[游戏专用]** MDA aesthetics target.
- **[通用产品]** User promise target from product concept.

Handle verdict per `standards/director-gates.md`. With authority for the CDD
header effect, record the verdict after resolution (this is a gate verdict,
not write authority, ADR acceptance or independent author approval):
`> **Creative Director Review (CD-GDD-ALIGN)**: APPROVED [date] / CONCERNS (accepted) [date] / REVISED [date]`

---

### 5b: Update Entity Registry

Scan the completed CDD for cross-system facts that should be registered:
- Named entities (enemies, NPCs, bosses) with stats or drops
- Named items with values, weights, or categories
- Named formulas with defined variables and output ranges
- Named constants referenced by value in more than one place

For each candidate, check if it already exists in `design/registry/entities.yaml`:
```
Grep pattern="  - name: [candidate_name]" path="design/registry/entities.yaml"
```

Present a summary:
```
Registry candidates from this CDD:
  NEW (not yet registered):
    - [entity_name] [entity]: [attribute]=[value], [attribute]=[value]
    - [item_name] [item]: [attribute]=[value], [attribute]=[value]
    - [formula_name] [formula]: variables=[list], output=[min–max]
   ALREADY REGISTERED (referenced_by update proposed):
    - [constant_name] [constant]: value=[N] ← matches registry ✅
```

If the named registry effect is not covered, show the concrete entries and ask:
"May I update `design/registry/entities.yaml` with these [N] new entries
and update `referenced_by` for the existing entries?"

If yes: append new entries and update `referenced_by` arrays. Never modify
existing `value` / attribute fields without surfacing it as a conflict first.

### 5c: Offer Design Review

Present a completion summary:

> **CDD Drafting Result: [System Name]**
> - Semantic roles/evidence: [complete/incomplete mapping]
> - Independent review: [bound result or pending]
> - Sections written: [list]
> - Provisional assumptions: [list any assumptions about undesigned dependencies]
> - Cross-system conflicts found: [list or "none"]

> **To validate this CDD, recommend an independent reviewer and run when authorized:** `/design-review design/cdd/[system-name].md`
>
> A non-writing reviewer must inspect exact bound inputs independently of the
> author's conclusions. A new window alone does not prove independence; record
> actor, input baseline and actual review performed. An author self-check remains
> a self-check. If independent execution is unavailable, disclose the limitation
> and keep required review pending.

### 5d: Update Module Index

After the CDD drafting is complete, update the module index only within its
separately authorized effect (or show the concrete draft and obtain authority):

- Read the module index
- Update the target system's row:
  - If a current exact-input design review passed and the user/governance approved
    the status effect: Status → "Approved"
  - If design-review was run and verdict is NEEDS REVISION: Status → "In Review"
  - If design-review was skipped: Status → "Designed" (pending review)
  - If the user chose "I'll review it myself first": Status → "Designed"
  - Design Doc: link to `design/cdd/[system-name].md`
- Update the Progress Tracker counts

If this exact effect is not covered, ask: "May I update the module index at
`design/cdd/module-index.md`?"

### 5d: Update Session State

If its path/effect is authorized, update `production/session-state/active.md` with:
- Task: [system-name] CDD
- Status: Complete (or In Review if design-review was run)
- File: design/cdd/[system-name].md
- Sections: [actual substantive roles complete / incomplete roles and reasons]
- Next: [suggest next system from design order]

### 5e: Suggest Next Steps

Use `AskUserQuestion`:
- "What's next?"
  - Options:
    - "Run `/consistency-check` — verify this CDD's values don't conflict with existing CDDs (recommended before designing the next system)"
    - "Design next system ([next-in-order])" — if undesigned systems remain
    - "Fix review findings" — if design-review flagged issues
    - "Stop here for this session"
    - "Run `/gate-check`" — if enough MVP systems are designed

---

## 6. Specialist Agent Routing

Before delegating a section, read the matching domain and module category in [specialist routing](references/specialist-routing.md). Load only the applicable routing row. Specialists return proposals to the main session and never write project files directly.

## 7. Recovery & Resume

If the session is interrupted (compaction, crash, new session):

1. If `production/session-state/active.md` exists and belongs to this task, Read
   it for the recorded system and progress. Otherwise recover the actual module,
   CDD path and scoped approvals from the existing conversation and saved project
   decisions. Clarify an ambiguous target before dependent work; recovery does not
   authorize creating or repairing session state.
2. Read the actual module CDD, such as `design/cdd/[system-name].md` after binding
   the known module name. Retain substantive sections; placeholders and unresolved
   required content still need work. Content presence alone does not establish
   approval or completion; keep unresolved approvals pending.
3. Resume within the existing scope from the next incomplete section, preserving
   approved content and separate review/status authority.

This is why incremental writing matters: every approved section survives any
disruption.

---

## Collaborative Protocol

This skill follows the collaborative design principle at every step:

1. **Question -> Options -> Decision -> Draft -> Approval** for unresolved choices;
   reuse existing approved document/batch scope for covered sections
2. **AskUserQuestion** at every decision point (Explain -> Capture pattern):
   - Phase 2: "Ready to start, or need more context?"
   - Phase 3: "May I create the skeleton?"
   - Phase 4 (each section): Design questions, approach options, draft approval
   - Phase 5: "Run design review? Update module index? What's next?"
3. **"May I write to [filepath]?"** for writes not covered by existing authority
4. **Incremental writing**: Each section is written to file immediately after approval
5. **Session state updates**: Only with authority for that path/effect
6. **Cross-referencing**: Every section checks existing CDDs for conflicts
7. **Specialist routing**: Complex sections get expert agent input, presented to
   the user for decision — never written silently

**Never** auto-generate the full CDD and present it as a fait accompli.
**Never** write outside user-approved scope.
**Never** contradict an existing approved CDD without flagging the conflict.
**Always** show where decisions come from (dependency CDDs, pillars, user choices).

## Context Window Awareness

This is a long-running skill. After writing each section, check if the status line
shows context at or above 70%. If so, append this notice to the response:

> **Context is approaching the limit (≥70%).** Your progress is saved — all approved
> sections are written to `design/cdd/[system-name].md`. When you're ready to continue,
> open a fresh Claude Code session and run `/design-system [system-name]` — it will
> detect which sections are complete and resume from the next one.

---

## Recommended Next Steps

- Run `/design-review design/cdd/[system-name].md` in a **fresh session** to validate the completed CDD independently
- Run `/consistency-check` to verify this CDD's values don't conflict with other CDDs
- Run `/map-systems next` to move to the next highest-priority undesigned system
- Run `/review-all-gdds`, then `/gate-check systems-design` when all MVP CDDs are authored and reviewed
