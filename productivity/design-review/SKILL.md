---
name: design-review
description: "Reviews a CDD for completeness, internal consistency, implementability, and adherence to project design standards. Supports both game and general product domains. Run this before handing a design document to programmers."
argument-hint: "[path-to-design-doc] [--depth full|lean|solo]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Edit, Task, AskUserQuestion
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

## User Guide

- When to use: Reviews a CDD for completeness, internal consistency, implementability, and adherence to project design standards. Supports both game and general product domains. Run this before handing a design document to programmers.
- Inputs: Command arguments: `/design-review [path-to-design-doc] [--depth full|lean|solo]`; project artifacts referenced below; user decisions and approvals before writes.
- Outputs: Primary artifacts, reports, or conversation guidance described below; write files only after user approval.
- Memory-bank writes: Only with initialized Memory Bank and separately authorized `memory_bank/t3_archive/reviews/review-index.md` effect; none in read-only/report-only.
- Next steps: Follow the workflow hand-off or next-step guidance below; recommendations do not auto-run and require explicit user command/approval.

## Phase 0: Parse Arguments

Extract `--depth [full|lean|solo]` if present. Default is `full` when no flag is given.

Reject an invalid explicit depth with a corrective error; default full applies
only to an absent flag. Depth controls analysis delegation, not director mode
or write authority.

**Note**: `--depth` controls the *analysis depth* of this skill (how many specialist agents are spawned). It is independent of the global review mode in `production/review-mode.txt`, which controls director gate spawning. These are two different concepts — `--depth` is about how thoroughly *this* skill analyses the document.

- **`full`**: Complete review — all phases + specialist agent delegation (Phase 3b)
- **`lean`**: All phases, no specialist agents — faster, single-session analysis
- **`solo`**: Phases 1-4 only, no delegation, no Phase 5 next-step prompt — use when called from within another skill

---

## Phase 1: Load Documents

Read the target design document in full. Read CLAUDE.md for project context and
standards. Resolve document kind/domain/actual required-set owner through
`design/INSTRUCTIONS.md` using workflow/provenance and the substantive body.
Read that owner/template and required related references to closure. A concept,
Quick Spec or Module Index in design paths is not a module by filename alone;
unknown kind/owner remains incomplete until resolved.

**Dependency graph validation:** For every system listed in the Dependencies section, use Glob to check whether its CDD file exists in `design/cdd/`. Flag any that don't exist yet — these are broken references that downstream authors will hit.

**Concept alignment:** Read the appropriate concept context for the detected domain.
- **[游戏专用]** If `design/cdd/game-concept.md` or any file in `design/narrative/` exists, read it. Note any mechanical choices in this CDD that contradict established world rules, tone, or design pillars. Pass this context to `game-designer` in Phase 3b.
- **[通用产品]** If `design/cdd/product-concept.md` exists, read it. Note any module choices in this CDD that contradict the product principles, user promise, JTBD statement, or target workflow. Pass this context to `lead-programmer`, the language specialist, and `creative-director` in Phase 3b.

**Prior review check:** Read any prior bound review and its input manifest,
scope, rules, actor and unresolved findings. A new review of changed bytes or
changed dependency/rule closure is a re-review with a new baseline. Continuing
an interrupted review of the exact same bytes/closure is a continuation; preserve
completed checks and disclose pending ones. Equal hashes at collections do not
prove no intervening writes. A historical verdict is valid only for its exact
inputs and authority; an unbound latest-log entry is history, not current approval.

---

## Phase 2: Completeness Check

Evaluate the resolved kind's required roles under `design/INSTRUCTIONS.md`'s
owner routing: Module8 for Game/Product module CDDs; actual Game/Product concept
template sets, category-specific Quick Spec format or Module Index owner set for
those kinds. Map aliases to real substantive bodies/evidence, retaining headings.
List each required role as complete, missing, placeholder, contradictory or
incomplete dependency with path/section evidence and an actionable finding.
Do not demand module-only formulas/knobs from a concept. Extra sections do not
replace required roles; heading presence is discovery only. Unknown kind/owner
cannot default to Module8 or yield a completeness APPROVED.
Read the declared target and required related closure in full for this review;
missing inputs narrow affected conclusions and cannot yield APPROVED.

---

## Phase 3: Consistency and Implementability

**Internal consistency (apply to the resolved kind's actual claims):**
- Do the formulas produce values that match the described behavior?
- Do edge cases contradict the main rules?
- Are dependencies bidirectional (does the other system know about this one)?

**Implementability / concept feasibility (apply the actual owner scope):**
- Are the rules precise enough for a programmer to implement without guessing?
- Are there any "hand-wave" sections where details are missing?
- Are performance implications considered?

**Cross-system consistency:**
- **[游戏专用]** Does this conflict with any existing mechanic?
- **[游戏专用]** Does this create unintended interactions with other game systems?
- **[游戏专用]** Is this consistent with the game's established tone and pillars?
- **[通用产品]** Does this conflict with any existing workflow, module contract, API contract, schema, or permission boundary?
- **[通用产品]** Does this create unintended interactions with other modules, data flows, integrations, or user states?
- **[通用产品]** Is this consistent with the product's established principles, user promise, and JTBD?

---

## Phase 3b: Adversarial Specialist Review (full mode only)

**Skip this phase in `lean` or `solo` mode.**

**This phase is MANDATORY in full mode.** Do not skip it.

**Before spawning any agents**, print this notice:
> "Full review requires the actual specialist reviews below. Use `--depth lean`
> for a single-session review; unavailable delegation is disclosed as incomplete,
> without inventing specialist verdicts or claiming the full workflow completed."

### Step 1 — Identify all domains the CDD touches

Read the CDD and identify every domain present. A CDD can touch multiple domains simultaneously — be thorough. Common signals:

| If the CDD contains... | Spawn these agents |
|------------------------|-------------------|
| Costs, prices, drops, rewards, economy | `economy-designer` |
| Combat stats, damage, health, DPS | `game-designer`, `systems-designer` |
| AI behaviour, pathfinding, targeting | `ai-programmer` |
| Level layout, spawning, wave structure | `level-designer` |
| Player progression, XP, unlocks | `economy-designer`, `game-designer` |
| UI, HUD, menus, player-facing displays | `ux-designer`, `ui-programmer` |
| Dialogue, quests, story, lore | `narrative-director` |
| Animation, feel, timing, juice | `gameplay-programmer` |
| Multiplayer, sync, replication | `network-programmer` |
| Audio cues, music triggers | `audio-director` |
| Performance, draw calls, memory | `performance-analyst` |
| Engine-specific patterns or APIs | Primary engine specialist (from `standards/technical-preferences.md`) |
| Acceptance criteria, test coverage | `qa-lead` |
| Data schema, resource structure | `systems-designer` |
| Any gameplay system | `game-designer` (always)
[Product] Product domain mapping:
| If the CDD contains... | Spawn these agents |
|------------------------|-------------------|
| API endpoints, request/response contracts | `lead-programmer`, language specialist |
| Data models, schemas, storage | `lead-programmer`, language specialist |
| Auth, permissions, security | `security-engineer` |
| Deployment, CI/CD, infrastructure | `devops-engineer` |
| UI, UX, user-facing interfaces | `ux-designer`, `ui-programmer` |
| Performance-critical paths | `performance-analyst` |
| Third-party integrations, APIs | `lead-programmer` |
| Acceptance criteria, test coverage | `qa-lead` |
**[游戏专用]** **Always spawn `game-designer` and `systems-designer` as a baseline minimum.** Every game CDD touches their domain.

**[通用产品]** **Always spawn `lead-programmer` and the appropriate language specialist as a baseline minimum for product CDDs.**

### Step 2 — Spawn all relevant specialists in parallel

**CRITICAL: Task in this skill spawns a SUBAGENT — a separate independent Claude session**
with its own context window. It is NOT task tracking. Do NOT simulate specialist
perspectives internally. Do NOT reason through domain views yourself. You MUST issue
actual Task calls. A simulated review is not a specialist review.

****

Issue all Task calls simultaneously. Do NOT spawn one at a time.

**Prompt each specialist adversarially:**
> "Here is the CDD for [system] and the main review's structural findings so far.
> Your job is NOT to validate this design — your job is to find problems.
> Challenge the design choices from your domain expertise. What is wrong,
> underspecified, likely to cause problems, or missing entirely?
> Be specific and critical. Disagreement with the main review is welcome."

**Additional instructions per agent type:**

- **`game-designer`**: Anchor your review to the Player Fantasy stated in Section B of this CDD. Does this design actually deliver that fantasy? Would a player feel the intended experience? Flag any rules that serve implementability but undermine the stated feeling.

- **`systems-designer`**: For every formula in the CDD, plug in boundary values (minimum and maximum plausible inputs). Report whether any outputs go degenerate — negative values, division by zero, infinity, or nonsensical results at the extremes.

- **`lead-programmer`**: For product CDDs, challenge whether the module contract is implementable, whether API/data boundaries are explicit, and whether the design creates hidden coupling or operational risk.

- **Language specialist**: For product CDDs, validate that the proposed data model, integration shape, and configuration approach are idiomatic for the pinned language/framework stack. Flag framework-specific pitfalls, stale assumptions, or missing constraints.

- **`qa-lead`**: Review every acceptance criterion. Flag any that are not independently testable — phrases like "feels balanced", "works correctly", "performs well" are not ACs. Suggest concrete rewrites for any that fail this test.

### Step 3 — Senior lead review

After all specialists respond, spawn `creative-director` as the **senior reviewer**:
- Provide: the CDD, all specialist findings, any disagreements between them
- Ask: "Synthesise these findings. What are the most important issues? Do you agree with the specialists? What is your overall verdict on this design?"
- The creative-director's synthesis becomes the **final verdict** in Phase 4.

### Step 4 — Surface disagreements

If specialists disagree with each other or with the creative-director, do NOT silently pick one view. Present the disagreement explicitly in Phase 4 so the user can adjudicate.

Mark every finding with its source: `[game-designer]`, `[economy-designer]`, `[lead-programmer]`, `[language-specialist]`, `[creative-director]`, etc.

---

## Phase 4: Output Review

```
## Design Review: [Document Title]
Specialists consulted: [list agents spawned]
Re-review: [Yes — prior verdict was X on YYYY-MM-DD / No — first review]

### Document kind and required-set owner
[Resolved kind/domain, workflow/provenance and actual owner/template identity]

### Completeness: [X/Y required roles substantively covered; Y=8 for module CDDs]
[Owner role → actual heading/body/evidence; missing/placeholder/unresolved roles]

### Evidence and review scope
[Exact input manifest, depth, authors/reviewers, full/partial reading,
required/completed/skipped/unavailable checks; historical/continuation/re-review]

### Dependency Graph
[List each declared dependency and whether its CDD file exists on disk]
- ✓ enemy-definition-data.md — exists
- ✗ loot-system.md — NOT FOUND (file does not exist yet)

### Required Before Implementation
[Numbered list — blocking issues only. Each item tagged with source agent.]

### Recommended Revisions
[Numbered list — important but not blocking. Source-tagged.]

### Specialist Disagreements
[Any cases where agents disagreed with each other or with the main review.
Present both sides — do not silently resolve.]

### Nice-to-Have
[Minor improvements, low priority.]

### Senior Verdict [creative-director]
[Creative director's synthesis and overall assessment.]

### Scope Signal
Estimate implementation scope based on: dependency count, formula count,
systems touched, and whether new ADRs are required.
- **S** — single system, no formulas, no new ADRs, <3 dependencies
- **M** — moderate complexity, 1-2 formulas, 3-6 dependencies
- **L** — multi-system integration, 3+ formulas, may require new ADR
- **XL** — cross-cutting concern, 5+ dependencies, multiple new ADRs likely
Label clearly: "Rough scope signal: M (producer should verify before sprint planning)"

### Verdict: [APPROVED / NEEDS REVISION / MAJOR REVISION NEEDED]
```

This skill is read-only — no files are written during Phase 4.

---

## Phase 5: Next Steps

Present next steps in conversation. Use `AskUserQuestion` when a decision/new
effect is required and the interface is available; covered scope needs no repeat ask.

**First widget — what to do next:**

If the semantic review is APPROVED, present separately the optional module-index,
review-log and handoff effects below. Execute only authorized effects; read-only
ends with findings, while report-only writes only its new assigned report.

If NEEDS REVISION or MAJOR REVISION NEEDED, options:
- `[A] Revise the CDD now — address blocking items together`
- `[B] Stop here — revise in a separate session`
- `[C] Accept as-is and move on (only if all items are advisory)`

**If user selects [A] — Revise now:**

A selected revise action makes this actor a writer. Resolve actual file/section
changes and obtain authority if absent. Ask unresolved design choices together
when practical. Preserve original findings/bytes, repair only scoped inputs and
collect a fresh baseline for any required independent review.

After all revisions are complete, show a summary table (blocker → fix applied) and use `AskUserQuestion` for a **post-revision closing widget**:

- Prompt: "Revisions complete — [N] blockers resolved. What next?"
- Note current context usage: if context is above ~50%, add: "(Recommended: /clear before re-review — this session has used X% context. A full re-review runs 5 agents and needs clean context.)"
- Options:
  - `[A] Re-review in a new session — run /design-review [doc-path] after /clear`
  - `[B] Accept revisions for writing — required re-review remains pending`
  - `[C] Move to next system — /design-system [next-system] (#N in design order)`
  - `[D] Stop here`

A closing decision does not establish independent review of revised inputs.

**Optional module-index effect — separately authorize if uncovered:**

Use a second `AskUserQuestion`:
- Prompt if uncovered: "May I update `design/cdd/module-index.md` to mark
  [system] as [In Review / Approved]?" Approval status must bind current review
  inputs and governance authority; repairs leave required fresh review pending.
- Options: `[A] Yes — update it` / `[B] No — leave it as-is`

**Optional review-log effect — separately authorize if uncovered:**

Use a third `AskUserQuestion`:
- Prompt: "May I append this review summary to `design/cdd/reviews/[doc-name]-review-log.md`? This creates a revision history so future re-reviews can track what changed."
- Options: `[A] Yes — append to review log` / `[B] No — skip`

With explicit rolling-log authority, retain prior entries and append a uniquely
identified review revision binding exact inputs. Report-only instead writes a
new assigned report and leaves the log unchanged. Include these fields:
```
## Review — [YYYY-MM-DD] — Verdict: [APPROVED / NEEDS REVISION / MAJOR REVISION NEEDED]
Scope signal: [S/M/L/XL]
Specialists: [list]
Blocking items: [count] | Recommended: [count]
Summary: [2-3 sentence summary of key findings from creative-director verdict]
Prior verdict resolved: [Yes / No / First review]
Review ID/input manifest: [exact full hashes, sizes, source commit+diff/other identities]
Scope/depth/checks/actors: [reading closure and verification limitations]
```

When `memory_bank/` exists, update
`memory_bank/t3_archive/reviews/review-index.md` only with authority for that
specific index effect. Log/report approval alone does not grant it.

Update the Memory Bank index only after the report is saved and only with authority
for that named index effect. Initialization alone, read-only scope and report-only
scope do not authorize it. If initialization or the intended effect is unresolved,
retain Unknown and leave the index unchanged. Before an authorized update, read
the saved immutable report revision and its exact input/evidence identities;
a proposed report or an INFO result is insufficient. This step does not initialize
Memory Bank.

- Review Type: `design-review`
- Source Artifact: `design/cdd/reviews/[doc-name]-review-log.md`
- Use `Source Artifact` as the dedupe key.
- If the same source artifact already exists, update Date, Verdict, and
  Follow-up Owner instead of adding a duplicate row.
- If `memory_bank/` does not exist, do not create it from `/design-review`;
  keep the authorized report/conversation fallback and disclose the absent
  optional index; do not require initialization for this review.

---

**Optional closing decision after authorized effects:**

After optional authorized effects, check actual project state and recommend
applicable next steps; ask a new decision only when needed.

Build the optional closing choices only when Phase 5 is entered in full or lean
mode. Solo skips Phase 5, and a read-only or report-only run ending at its assigned
findings/report does not continue here solely because the analysis depth is full.
If the intended next step is unresolved, retain Unknown. When offering these
choices, read the actual project state below.

Before building options, read:
- `design/cdd/module-index.md` — find any system with Status: In Review or NEEDS REVISION (other than the one just reviewed)
- Count `.md` files in `design/cdd/` (excluding game-concept.md, product-concept.md, module-index.md, principles.md) to determine if `/review-all-gdds` is worth offering (≥2 CDDs)
- Find the next system with Status: Not Started in design order

Build the option list dynamically — only include options that are genuinely next:
- `[_] Run /design-review [other-cdd-path] — [system name] is still [In Review / NEEDS REVISION]` (include if another CDD needs review)
- `[_] Run /consistency-check — verify this CDD's values don't conflict with existing CDDs` (always include if ≥1 other CDD exists)
- `[_] Run /review-all-gdds — holistic design-theory review across all designed systems` (include if ≥2 CDDs exist)
- `[_] Run /design-system [next-system] — next in design order` (include only if an actual undesigned system remains)
- `[_] Stop here`

Assign letters A, B, C… only to included options. Mark the most pipeline-advancing option as `(recommended)`.

Recommendations do not invoke a workflow or perform its file/status effects.
