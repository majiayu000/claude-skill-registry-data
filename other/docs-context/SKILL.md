---
name: docs-context
description: |
  Super Base Context — project doc loader & synchronizer. Triggers even without explicit "load docs"/"sync docs."

  READ MODE — load architecture/modules/coding/decision docs when work references project state: code work (write/modify/remove); design (features/APIs/schemas/architecture); review (modules, past solutions); tech selection; ADR research; migration/refactor planning; performance/security analysis; tests; code reviews; any spec/plan/design/ADR referencing project.

  WRITE MODE — NET DELTA vs. last doc sync: additions/modifications/REMOVALS/deprecations of previously-synced code or decisions (docs revert: delete BCU file/ADR), AND rollbacks. User signals: sync docs/done/ready to commit/pre-commit/record decision. Auto-fires before final task-completion reply.

  WRITE MODE does NOT fire on: brainstorming, generic/read-only Q&A, in-session try-and-undo with no net change, already-synced.
---

# docs-context — Context Loader & Doc Synchronizer
Manages reading and writing of project documentation, ensuring correct contextual constraints during development and keeping docs in sync with code afterward.

## Contents
- Positioning, conflict priority, context correction taxonomy
- Document Paths (5 doc types under `docs/`)
- BCU Splitting Principle (decision flow + section-omission rule)
- Modes & Triggers (Read / Write criteria, Removal & Rollback Sync)
- Read Mode: always-load, task-type loading, BCU / ADR resolution, three context scenarios, post-load behavior
- Write Mode: doc sync checklist, slug selection, ADR write flow, sync execution steps
- Handling Missing Documents (scope, init flow, template mapping)
- Sync Summary Format (Updated / Created / Deleted / Declined / Skipped / No Update / Shared / Needs Confirmation)

### Positioning: Super Base Context
docs-context is the **Super Base Context** for Agent Coding — structured project docs, task-aware Read Mode, bidirectional Write Mode. The remainder of this file specifies each.

**Conflict priority** (when this skill's guidance collides with other instructions in the same turn): explicit user instruction > docs-context.

### Context Correction, Completion, and Reconstruction
Three scenarios in which docs-context restores the agent's project context — combined documents + code/comment scanning fills the gap when docs alone are insufficient.

- **Correction** — Not limited to enforcing constraints on generated code. When context degrades due to long-conversation attention decay, context compression inaccuracies, or accumulated drift, the agent can re-read the relevant documents and scan the actual codebase to restore an accurate understanding. Documents act as the ground truth that pulls distorted context back on track.
- **Completion** — When the agent lacks context for the current task, documents provide the structural knowledge (architecture, module boundaries, dependencies, constraints), while code and comment scanning fills in the implementation specifics that documents may not cover.
- **Reconstruction** — When starting a new session or opening a project for the first time, the agent has zero knowledge of the project. By triggering this skill, the agent loads the relevant documents (backbone) and combines them with code and comment scanning to reconstruct a complete understanding of the project from scratch.

## Document Paths
All documents are located under the workspace `docs/` directory:
| Document | Path | Content |
|----------|------|---------|
| Architecture | `docs/architecture.md` | Workspace directory structure, project background, system architecture, service-level topology, constraints, future plans |
| Tech Stack | `docs/tech-stack.md` | Framework versions, dependency constraints, environment requirements, AI code generation limits |
| Coding Standards | `docs/coding.md` | Coding standards, naming conventions, API design standards, error handling, logging standards, testing standards |
| Module Registry | `docs/modules/<bcu-slug>.md` | **One file per Business Capability Unit (BCU).** Each BCU file holds a single business capability's implementation list (HTTP / RPC / MQ / scheduled tasks / third-party callbacks / DB tables / frontend pages), flow, state transitions, local upstream/downstream, external dependencies, related business flows. Slug names a business capability (e.g. `create-order`, `refund`, `consumer-pay`), NOT a microservice / Controller / package / table |
| Decision Records | `docs/decisions/ADR-<slug>.md` | One file per architecture decision (ADR). Slug-only filenames (no numeric prefix, no date prefix). Date lives in frontmatter |

> **No README / index files** under `docs/modules/` or `docs/decisions/`. Use `Glob` to enumerate; read frontmatter / first-line responsibility on demand.

## BCU Splitting Principle

A `docs/modules/<bcu-slug>.md` file represents **one Business Capability Unit (BCU)**. A BCU must satisfy all 7 conditions:

1. Has an explicit business goal
2. Has an independent business flow
3. Has a relatively stable context boundary
4. Can be developed, modified, and tested independently
5. Modifications primarily affect this single business chain
6. Impact scope can be analyzed independently
7. An independent development plan can be generated for it

**Do NOT split by**: microservice · Controller · API · technical module · database table.
**DO split by**: real business chain · actual development task boundary · parallel-development unit.

### BCU Splitting Decision Flow

When in doubt whether to merge or split, run this 3-question test:

| Q | If answer is "no" → |
|---|---------------------|
| Q1: When modifying A, do you usually NOT need to touch B/C/D? | merge into one BCU |
| Q2: Can A deliver business value standalone, decoupled from B/C/D? | merge |
| Q3: Does A have a separate owner / schedule / test suite? | merge |

**Any "no" → merge. All three "yes" → split.** Default to **conservative merging** — splitting later is cheap (BCU files are independent); splitting too early creates orphaned tiny files. Split only when independent-evolution signals show up: separate owner, separate schedule, separate test suite, modifications no longer cascade.

**Worked example — consumer-side payment**: a typical "consumer pay" BCU bundles {payment initiation API + sync order query + upstream async callback + scheduled / MQ status reconciliation} into ONE file (e.g. `consumer-pay.md`) — they share one business goal and one state machine, and they are almost always modified together. Split out to a separate BCU only when "reconciliation crosses multiple BCUs", "order query is independently productized", or "callback routing is independently maintained" — i.e. when the merge condition stops holding.

### Diagrams in BCU files

A BCU file uses **two layers** of diagrams, each with its own purpose. Both layers respect the section-omission rule — never draw a diagram for its own sake.

**Layer 1 — Per-entry tracing diagrams** (live inside `## Implementation`)

Each *entry-point* item — HTTP API (inbound), MQ Consumption, Scheduled Task, Third-party Callback — MAY carry a tracing diagram of this entry's full call chain (services / RPC / MQ Production / DB / external systems / resources).

**Format — primary: ASCII span tree, supplementary: Mermaid `sequenceDiagram`**:

- **Primary (default)** — ASCII **span tree** of the factual call chain, mirroring distributed-tracing UIs (SkyWalking / Jaeger / etc.): hierarchical indentation showing parent → child calls.
  - Compact, diff-friendly, readable in plain text and in any Markdown renderer.
  - Use box-drawing chars (`├── / └── / │`) or plain ASCII (`+--`).
  - Each line: one hop (service.method / DB op / RPC / MQ produce / external call) with its result if non-obvious.
- **Supplementary (optional)** — when the entry is async / multi-roundtrip / has callbacks that the tree shape can't naturally express, ADD a Mermaid `sequenceDiagram` BELOW the tree for global overview. **Don't replace the tree — add alongside.** The tree is the factual chain; the sequence diagram is the temporal overview.
- **Trivial entries** — omit both. Single read-and-return query, single SQL insert: no diagram.

**Two rules apply together — optional + complete-when-present**:
- **Optional** — not every entry needs a diagram. Trivial entries stay diagram-free.
- **Complete when present** — if a diagram (tree or sequence) is drawn, it MUST cover every real hop end-to-end. Half-drawn / placeholder / partial-chain diagrams are forbidden.

| Entry-point complexity | Format |
|---|---|
| Trivial single-step (read-and-return / single insert) | Omit |
| Linear / synchronous chain (any depth) | ASCII span tree |
| Async / multi-roundtrip / external callbacks where temporal order matters | ASCII span tree **+** supplementary Mermaid `sequenceDiagram` |

ASCII span tree shape:

```
ENTRY: [protocol/method] [name]
├── [Service.method] (this service)
│   ├── DB.[table] insert/update
│   └── [DownstreamService].[op] (RPC) → [result]
├── [ExternalGateway].[op] (HTTP/SDK) → [result]
└── MQ produce [topic]
```

**Non-entry items NEVER carry their own diagram**: outbound RPC, MQ Production, Database tables touched, Frontend page, State management. They appear as nodes inside the calling entry's tree. A separate diagram for these is redundant and is forbidden.

**Layer 2 — BCU business flow(s)** (the `## Flow` section, **0 / 1 / N diagrams**)

The business-level view: how front-end interactions, business steps, and state transitions weave through the entry points to deliver the BCU's value. This is the **business view**, NOT a technical hop trace.

A BCU may carry **0, 1, or N** business-flow diagrams (1-to-many relationship):

| BCU business-flow situation | Shape |
|---|---|
| Single-entry BCU, business flow already obvious from `## Implementation` | **0** — omit the entire `## Flow` section |
| One coherent business flow | **1** — one diagram directly under `## Flow` |
| Multiple distinct business sub-flows (e.g. passive-scan vs aggregated-scan vs refund) | **N** — `### <Sub-flow name>` headings, one diagram per sub-flow. Don't bloat one diagram with mutually exclusive branches. |

Format per diagram: Mermaid `sequenceDiagram` or `flowchart` describing business steps; numbered text when truly simple.

**Non-redundancy contract**:
- Layer 1 nodes = services / RPC / resources / externals (technical hops)
- Layer 2 nodes = business steps / user actions / state transitions
- Layer 2 references Layer 1 by **entry name** (e.g. "calls `POST /pay/passive-scan`"); it does NOT redraw the entry's internal hops

**Inclusion boundary** (both layers):
- IN: services / resources / externals that **this BCU itself** invokes during its chain
- OUT: services unrelated to this BCU's chain
- OUT: the system-wide service topology diagram — that belongs in `docs/architecture.md`

**Why this split**: a multi-entry BCU (e.g. consumer pay with passive-scan / aggregated-scan / async callback / reconciliation job) needs **per-entry tracing** for technical clarity AND **business-flow diagrams** for business clarity. Forcing both into one diagram either bloats it beyond reading or loses one of the two views. Splitting cleanly maps to "what each entry does technically" + "how the business strings them together".

### Section-Omission Rule (hard)

Inside a BCU file, only the skeleton sections are mandatory: title (`# <Capability Name>`), header lines (Status / Owning service), `## Business Goal`, `## Implementation` (with at least one entry). **All other sections are conditional**: `## Flow`, `## State Transitions`, `## Upstream / Downstream`, `## External Dependencies`, `## Related Business Flows`, `## Risks / Constraints`, `## Notes / Gotchas` — **omit the entire section if the BCU has no relevant content**. Do NOT keep empty headings, do NOT write `N/A` / `TBD`, do NOT leave placeholder bullets. Same rule applies to `## Implementation` sub-bullets — list only what actually exists.

## Modes & Triggers

### Two modes
| Mode | When | Responsibility |
|------|------|----------------|
| **Read** | Before any project-related work | Load relevant docs, establish constraints |
| **Write** | After code/decisions land / before commit | Sync affected docs (forward AND reverse) |

### Read Mode triggers
**Root criterion**: does the task need to reference how the project actually works today? If yes, trigger Read Mode.

Triggers on any of:
- **Code work**: write/modify/add/remove/delete/deprecate code, implement, develop, integrate
- **Bugfix / refactor**: fix bug, debug, refactor, optimize, improvement plan
- **Tests**: write tests, unit/integration tests, test strategy / plan
- **Database**: migration, schema, DDL, add/drop column, add/drop table
- **Design / review**: architecture design / review, microservice split, module boundary discussion, detailed spec, state-machine design, business-flow mapping, data-flow design
- **Selection / decisions**: tech selection, dependency choice, upgrade evaluation, ADR authoring, decision comparison
- **Research / inventory**: historical decision research ("why did we choose X"), past-solution analysis, current architecture inventory, current dependency inventory, code review
- **Performance / security**: performance design, capacity planning, security design, threat modeling, vulnerability fix
- **API / integration**: API design, integration, contract negotiation
- **Any spec / plan / design / ADR that references current project state** — regardless of detail level

> **Does NOT trigger Read Mode**: brainstorming with no project reference, generic-knowledge questions (e.g. "how does HashMap work in Java"), pure read-only code explanations.
> **When uncertain, default to Read Mode** (defensive).

### Write Mode triggers
**Single criterion**: current code/decision state has a **net delta** vs. the last-synced doc state.

**Net delta scope** (bidirectional):
- **Forward**: additions / modifications of landed content (code, config, SQL, build scripts, ADR decisions)
- **Reverse**: removals / deprecations of previously-synced code or decisions (docs must shrink to match)
- **Rollback**: rollbacks of previously-synced content (docs revert accordingly)

**When it fires**:
- **User signals**: sync docs / update docs / done / completed / ready to commit / feature done / pre-commit check / record this decision
- **`[auto]` Agent self-trigger**: MUST fire right before the agent's final task-completion reply — do not wait for the user

**Does NOT fire on** (any one match → skip):
1. Partial edits while the task is still in progress
2. Mid-task progress updates
3. Read-only / Q&A tasks
4. Brainstorming or generic-knowledge questions with no project state referenced
5. High-level plan with no code/decision landed (note: detailed spec still triggers Read Mode; this only excludes Write Mode)
6. In-session try-and-undo that left no net change
7. Already synced this round with no new changes after

### Removal & Rollback Sync (a first-class concept)

**docs-context syncs in both directions**: when code is added, docs grow; when code or decisions are **removed / rolled back**, docs **shrink** to match.

| Code or decision change | Doc action |
|------------|-----------|
| Delete a BCU's code entirely | Delete `docs/modules/<bcu-slug>.md` |
| Delete a single HTTP API / RPC / MQ producer-consumer / scheduled task / third-party callback inside a BCU | Update the BCU file's `## Implementation` section |
| Drop a database table or column | Update affected BCU file's `## Implementation` (Database tables touched line) and the header `**Database tables touched**` line |
| Overturn a previously-merged decision | Delete `docs/decisions/ADR-<old>.md` (history lives in git) |
| Roll back a previously-recorded refactor | Restore the affected sections (or whole BCU file) to the rolled-back state |
| Remove a cross-BCU dependency | Bidirectional sync: delete this BCU file's `## Upstream / Downstream` entry AND the counterpart BCU file's `## Upstream / Downstream` entry |

**Distinguishing removal from in-session try-and-undo**:

| Scenario | Net delta | Write Mode |
|------|-------|----------|
| Code was synced → now removed | Yes | **Triggers** (reverse sync) |
| In-session add → in-session delete → net delta zero | No | **Skips** |
| In-session add → in-session delete, but other parts still have net delta | Yes | **Triggers** (only for landed parts) |

**Detection method**: `git diff` against the last-synced commit; or working tree vs HEAD.

> **Do not maintain Deprecated / Superseded states.** Removal means the doc section is deleted (ADR file deleted, capability section deleted). History is recoverable via `git log -- docs/`.

# Read Mode: Context Loading

## Loading Context
### Always Load
Every time read mode is triggered, MUST load:
- `docs/coding.md` — Coding standards are the baseline constraint for all tasks

### Additional Loading by Task Type

`modules/*` and `decisions/*` shortcuts are resolved per the algorithms in §Module / ADR Resolution Strategy below.

| Task Type | Additional Docs | Trigger Criteria |
|-----------|----------------|-----------------|
| New feature/module | architecture.md + tech-stack.md + modules/* | add/create/implement new, creating new modules |
| Modify/optimize existing | modules/* + architecture.md | modify/adjust/optimize/refactor/update, or refactoring steps in a plan |
| Bug fix | modules/* | bug/fix/error/exception/debug, or during systematic-debugging flow |
| Tech selection/dependency change | tech-stack.md + decisions/* | introduce new lib/upgrade version/install/upgrade/migrate |
| Architecture discussion/design review | architecture.md + decisions/* + modules/* | architecture/design comparison/design review |
| API design/development | architecture.md + modules/* + tech-stack.md | design new API/modify API params/integration/API design |
| Testing/QA | modules/* + coding.md | writing tests/unit test/integration test/test/spec |
| Database migration | modules/* + tech-stack.md | add field/alter table/migration/schema/DDL/database change |
| Performance optimization | architecture.md + modules/* + tech-stack.md | slow query/performance/bottleneck/slow/perf/optimize query |
| Security fix/audit | coding.md + tech-stack.md + modules/* | security/XSS/injection/vulnerability/CVE/security audit |

### Multi-type Overlay
When a task spans multiple types (e.g., "add module and introduce new library"), merge and deduplicate all matching document sets.

## Module / ADR Resolution Strategy

Because `docs/modules/` and `docs/decisions/` have no README / index, the agent must resolve which BCU files to load. Use the algorithms below to keep loads precise and bounded — one BCU per file means each load corresponds to one business capability.

> **Upstream / Downstream Convention (mandatory, do not invert)**:
> - **Upstream (this BCU calls)** — outbound dependencies: APIs / RPCs / MQ topics this BCU invokes.
> - **Downstream (depends on this BCU)** — inbound consumers: callers, MQ consumers, frontend pages that depend on this BCU.
>
> When reading existing fixtures or projects, if a `## Upstream / Downstream` section appears to use the inverse convention, halt and ask the user to confirm direction before bidirectional sync — do not silently re-invert.

### Resolving a BCU file

1. `Glob docs/modules/*.md` to get the BCU slug list.
2. Match the task's keywords (business term, slug, trigger scenario, endpoint path, table name) against filenames first — BCU slug names should map naturally to business capabilities (`create-order`, `refund`, `consumer-pay`).
3. If filename match is ambiguous or zero, Grep across `docs/modules/*.md` for those keywords (title line / Business Goal section / Implementation entries).
4. Load 1–3 candidate BCU files **in full** — BCU files are intentionally bounded so reading the whole file is cheap.
5. If the task hits multiple BCU candidates, present the candidate list back to the user: "This task could target BCU X / Y / Z — which one?"
6. Last-resort fallback: read `docs/architecture.md` service topology to reverse-locate, then ask the user.

### Resolving an ADR

1. `Glob docs/decisions/ADR-*.md` to get the slug list.
2. Match the task's decision keywords against slug, frontmatter `tags`, and `title`.
3. Load 0–2 most relevant ADRs in full.
4. Before authoring a new ADR (write mode), Grep across `docs/decisions/` to detect a pre-existing decision on the same topic — see Write Mode §"ADR Write Flow".

### Three context scenarios

**A — Reconstruction (new session, project unfamiliar):** Fixed sequence, ≤ 6–8 files.
1. `docs/coding.md`
2. `docs/architecture.md`
3. `docs/tech-stack.md`
4. `Glob docs/modules/*.md` (BCU slug list only)
5. `Glob docs/decisions/ADR-*.md` (slug list only)
6. Match task keywords → load 1–2 matched BCU files in full
7. Match task keywords → load 0–1 most relevant `ADR-*.md`

After loading, **emit a Reconstruction Summary table** so the user (and future sessions) can see exactly what was loaded and why:

```
## Reconstruction Summary
| File | Why loaded |
|------|-----------|
| docs/coding.md | Mandatory standards |
| docs/architecture.md | Service topology |
| docs/tech-stack.md | Framework / version constraints |
| docs/modules/create-order.md | Owning BCU for this task |
| docs/decisions/ (Glob, none read) | No ADRs matched task keywords |
```

Keep the table compact (one row per file/Glob). If a Glob returned a list but no file was opened, state that explicitly — transparency about non-loads is as important as transparency about loads.

**B — Completion (already in a BCU, need upstream/downstream):**
1. Read the current BCU file's `## Upstream / Downstream` section (cheapest, most precise).
2. Load 1–2 referenced upstream / downstream BCU files in full. **Do not recurse** beyond one hop — avoid context blowout.
3. If still insufficient, Grep `docs/modules/*.md` for the business keyword or endpoint path.

**C — Correction (long-conversation attention drift):** Fastest restore path.
1. Re-read `docs/coding.md` (standards drift the fastest).
2. Re-read the active BCU file in full — BCU files are bounded, so a full re-read is cheap and complete.
3. If the task involves a recorded decision, re-read the single most relevant `ADR-*.md`.
4. **Do not** re-read `architecture.md` — it would re-blow the window.

## Post-load Behavior
1. Before generating code, confirm compliance with all constraints in `coding.md`
2. For modifications, combine the relevant BCU file (especially `## Upstream / Downstream`) with code scanning to confirm impact scope
3. For additions, confirm no conflict with existing BCU boundaries — check candidate BCU files' title + Business Goal sections, plus the slug list under `docs/modules/`
4. If the current task may violate documented constraints, proactively alert the user.

   **When to HALT and present an A/B/C menu (must meet at least one trigger):**
   - **HARD constraint** — the conflicting rule in `coding.md` (or other docs) is marked with strong language: `MUST`, `STRICTLY ENFORCED`, `PROHIBITED`, `MANDATORY`, `非强制例外` (e.g. type conventions for money / rate / time, security rules, error-handling contracts).
   - **NEW divergence** — the violation has **no precedent in existing project code**. The task would introduce a fresh, isolated deviation.

   **When to PROCEED without halting (note in Doc Sync Summary instead):**
   - **SOFT divergence** — the task's deviation matches a deviation that **existing code already exhibits** (response envelope shape, path-prefix style, naming patterns, etc.). Treat as pre-existing tech debt between code and docs, not a new violation introduced by this task. Record it under `Needs User Confirmation` in the Doc Sync Summary so the team can decide separately whether to update `coding.md`, write an ADR, or migrate the existing code.

   The A/B/C menu (used only when HALT is required):
   - **(A) Override the standard** — proceed as requested; user must explicitly confirm; consider whether `coding.md` should be updated or an ADR recorded.
   - **(B) Use the compliant alternative** — show the proposed compliant version (with code snippet) and proceed once the user accepts.
   - **(C) Pause for clarification** — when requirements are ambiguous (e.g. value sourced from external system that forces the prohibited type).
5. When loaded documents do not provide sufficient detail for the current task, scan relevant source code and comments to supplement context understanding. Documents serve as the backbone (architecture, boundaries, constraints); code and comments fill in implementation-level specifics.
6. When generating code, write thorough comments for interfaces, methods, and important logic to ensure that AI agents in future sessions can reconstruct business context by scanning code and comments alone. If `coding.md` defines specific comment standards, follow those standards as the primary guideline.

### Document Priority
When documents contain conflicting guidance, higher-priority documents take precedence:

`coding.md` (mandatory standards) > `architecture.md` (architecture constraints) > `tech-stack.md` (technology limits) > `modules/*` (module & capability descriptions) > `decisions/*` (decision rationale)

---

# Write Mode: Doc Synchronization

## Doc Sync Checklist
Check each item against the current code changes. Only update affected docs; skip unaffected ones.

### modules/* — route every change to the right BCU file
The unit of edit is **one BCU file**. Each BCU file represents one Business Capability Unit; one code change resolves to one or more BCU files (never to a sub-section of a multi-capability file, since each file is already one BCU).

**Identifying the owning BCU**: For each change, ask "which user-visible business capability does this code change support?" and locate the matching `docs/modules/<bcu-slug>.md` file. Three cases:
- **One existing BCU file matches** → edit that file's relevant section (Implementation / Flow / State Transitions / Upstream-Downstream / External Dependencies / Related Business Flows).
- **Multiple existing BCU files are involved** → edit each affected file; bidirectional Upstream/Downstream sync between them.
- **No existing BCU matches** (the change supports a brand-new business capability) → first run the **BCU Splitting Decision Flow** (3 questions above). If the answer is "merge into an existing BCU", confirm with the user and edit that file. If the answer is "split", ask the user to confirm a new slug and create a new BCU file from `assets/templates/module.md`. Never silently bury new business behavior inside an unrelated BCU.

> **Forward sync bullets only below.** Removals / rollbacks are covered in the **Removal & Rollback Sync** section earlier — do not duplicate here.

- [ ] Added a new BCU → create `docs/modules/<bcu-slug>.md` from `assets/templates/module.md` (slug must be Glob-deduplicated and user-confirmed first; see "Slug Selection" below). Apply the **section-omission rule**: only emit sections that have actual content this round.
- [ ] Promoting a `planned` BCU to live (the planned BCU's implementation just landed) → flip the file's `**Status**: planned` header line to `**Status**: live`, then fill in / update the now-real Implementation / Flow / State Transitions etc. Do NOT create a duplicate file.
- [ ] Added or modified an HTTP API, RPC, MQ producer/consumer, scheduled task, or third-party callback → update the `## Implementation` section of the owning BCU file
- [ ] Changed a business flow → update the `## Flow` section of the owning BCU file
- [ ] Changed status enums or state machines → update the `## State Transitions` section of the owning BCU file (create the section if it didn't exist before — it's a conditional section per the section-omission rule)
- [ ] Added or modified frontend pages or stores → update the `## Implementation` section of the BCU the page serves
- [ ] Added or modified database tables or fields → update the `**Database tables touched**` header line + the relevant `## Implementation` table-touch entry of affected BCU(s)
- [ ] Changed cross-cutting facts (technology, service name, core package) → update each affected BCU file's header lines
- [ ] Added or modified a dependency between BCUs → bidirectional sync: update **this** BCU file's `## Upstream / Downstream` AND the counterpart BCU file's `## Upstream / Downstream`. If either side previously omitted the section (no relationships before), create it now.
- [ ] Added or modified a third-party / external system integration → update `## External Dependencies` of the owning BCU file
- [ ] Added or modified a multi-BCU business chain relationship → update `## Related Business Flows` of each BCU on the chain

> **Section-omission rule reminder**: when writing or updating a BCU file, do NOT add sections that have no content. Conversely, when content first appears, create the section. Empty headings, `N/A`, and `TBD` placeholders are forbidden.

### architecture.md
- [ ] Added/removed service → update service topology (service-level only)
- [ ] Changed inter-service communication → update architecture description
- [ ] Adjusted directory structure → update directory structure description
- [ ] Described future plans → update future plans section

### tech-stack.md
- [ ] Introduced new framework/library → Add to tech stack list with version and purpose
- [ ] Upgraded framework/library version → Update version number
- [ ] Removed framework/library → Remove from list
- [ ] Changed AI code generation constraints → Update constraints section

### coding.md
- [ ] Added/modified coding standards → Update corresponding section
- [ ] Added/modified API design standards → Update API standards section
- [ ] Added/modified error handling approach → Update error handling section
- [ ] Added/modified naming conventions → Update naming section

### decisions/*

> **ADR sync follows the CODE, not the moment of decision.**
> A decision being made (in chat, doc, or planning) does NOT trigger ADR creation on its own. The ADR is recorded only when the decision **lands in code and changes behavior** — same threshold as a capability or module entry. This keeps `docs/decisions/` consistent with `docs/modules/` and the codebase. Pure planning / brainstorming about a future decision belongs in a plan or spec, not in `decisions/`.

- [ ] An important architecture/technical decision **lands in code** → create `docs/decisions/ADR-<slug>.md` from `assets/templates/decision.md` (slug user-confirmed; see "ADR Write Flow")
- [ ] A previous decision is **overturned in code** (the new approach is implemented) → **delete the old ADR file** AND create a new ADR file. Do not keep `Superseded` / `Deprecated` states. History remains accessible via `git log -- docs/decisions/`.
- [ ] A decision was discussed but NOT yet implemented → **do not write an ADR yet**. Note the decision in the relevant plan/spec and let Write Mode skip `decisions/` this round.

### Slug Selection (modules and ADRs)
Before creating any new file under `docs/modules/` or `docs/decisions/`:
1. Derive 1–3 candidate slugs from **business capability signals** — what the user / caller can do (verb-noun: `create-order`, `refund`, `consumer-pay`, `merchant-settle`). For ADRs use decision keywords. Do NOT name BCU slugs after a Controller, package, microservice, or table.
2. `Glob` the target directory and compare candidates against existing slugs — pay special attention to **synonyms** (e.g. `notify` vs `notification`) to avoid orphan files.
3. Present the chosen slug + the 3 most-similar existing slugs to the user for confirmation.
4. **Never silently create the file.**

### ADR Write Flow
1. Grep across `docs/decisions/` (frontmatter `tags`, `title`, Background section) using the decision's keywords. If a topic match is found, ask the user: "Topic already covered by `ADR-<old>.md` — replace or supplement?"
2. Propose slug + title. Wait for user confirmation.
3. If user chose **replace**: `rm docs/decisions/ADR-<old>.md`, then create `docs/decisions/ADR-<new>.md`.
4. If user chose **new**: just create `docs/decisions/ADR-<new>.md` with frontmatter.
5. The directory should only ever contain ADRs that match current code. Do not maintain superseded / deprecated states — that's what git history is for.

## Sync Execution Steps
1. Identify the scope of code changes to sync: inspect this-session edits plus, when needed, `git diff` / file state to detect prior unsynced landed changes
2. Filter to net delta: exclude changes that were tried and then reverted within this session (no net delta → skip to avoid false reporting)
3. Check against the above checklist item by item. For each modules change, resolve which BCU file owns the change. If no existing BCU file matches, follow the BCU Splitting Decision Flow + "Identifying the owning BCU" guidance — including asking the user before creating a new BCU file
4. For matched items, read the current content of the BCU file (BCU files are bounded; a full read is cheap)
5. Execute updates following existing doc format and style (maintain consistency)
6. Cross-document consistency check: verify that updates to one document are consistent with related content in other documents (e.g., a new service should also appear in `architecture.md` service topology; a cross-BCU dependency change must update both BCU files' `## Upstream / Downstream` sections)
7. Identify shared files touched in this round (`architecture.md`, multiple BCU files in cross-BCU changes) — list them explicitly in the sync summary so reviewers can preempt merge conflicts
8. Output a sync summary to inform the user

## Handling Missing Documents
When a required document is missing, initiate the template-based creation flow. **Silent creation is forbidden** — always confirm with the user first.

### Scope — only create what this task needs
Do NOT preemptively create the full 5-doc set when only one is needed. Create only the files this task actually touches:
- Read Mode finds `coding.md` missing → ask + create `coding.md` (it is the always-load gate).
- Write Mode targets a specific doc that is missing → ask + create that doc only.
- A task that does not change topology / dependencies / decisions → leave `architecture.md` / `tech-stack.md` / `decisions/` uncreated.

### Document Initialization Flow
1. Detect what is missing (file absent, directory absent, or both).
2. For each missing file or directory **relevant to this task**, confirm with the user once. Do NOT re-prompt for docs that already exist.
3. On approval: create directories as needed (`docs/`, `docs/modules/`, `docs/decisions/`), then create the UTF-8 file from the matching template populated with this task's content.
4. On refusal: do NOT create the file. The Doc Sync Summary MUST explicitly record "creation declined" under `### Declined / Skipped` — silent omission is dishonest.

### Document-to-Template Mapping
| File | Template |
|------|----------|
| `[workspace]/docs/architecture.md` | `[skills]/assets/templates/architecture.md` |
| `[workspace]/docs/tech-stack.md` | `[skills]/assets/templates/tech-stack.md` |
| `[workspace]/docs/coding.md` | `[skills]/assets/templates/coding.md` |
| `[workspace]/docs/modules/<slug>.md` | `[skills]/assets/templates/module.md` |
| `[workspace]/docs/decisions/ADR-<slug>.md` | `[skills]/assets/templates/decision.md` |

> The `docs/modules/` and `docs/decisions/` directories themselves are auto-created on first use (they have no README / index files of their own). Each new business module or decision is its own file derived from the corresponding template.

## Sync Summary Format
After completing sync, output in the following format:
```
## Doc Sync Summary

Code changes: [brief description of changes]

### Updated
- modules/<bcu-slug>.md → Implementation: [what was updated]
- modules/<bcu-slug>.md → Upstream/Downstream: [what was updated]
- modules/<bcu-slug>.md → External Dependencies: [what was updated]
- architecture.md: [what was updated]
- ...

> When a task ran but produced **no net delta** (e.g. tried-and-reverted, or only logging tweaks with zero doc-relevant impact), still emit the summary with `Updated: (none)` so reviewers can see the sync ran and consciously found nothing to change. Silence is not the same as a clean pass.

### Created / Deleted
- Created: docs/modules/<new-slug>.md (user-confirmed)
- Deleted: docs/decisions/ADR-<old-slug>.md (replaced by ADR-<new-slug>.md)

### Declined / Skipped
- docs/coding.md: creation offered, user declined — not synced this round

### No Update Needed
- tech-stack.md: Tech stack unchanged
- coding.md: Standards unchanged
- ...

### Shared files touched (watch for merge conflicts)
- docs/architecture.md
- docs/modules/<bcu-slug-A>.md (also touched by another change today)

### Needs User Confirmation
- decisions/: Chose xxx approach this time, should an ADR be recorded? Suggested slug: `ADR-...`
- modules/: New module candidate slug `notification`; closest existing slugs: [...]
```
