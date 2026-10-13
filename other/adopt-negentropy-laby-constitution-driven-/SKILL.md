---
name: adopt
description: "Brownfield onboarding — audits existing project artifacts for template format compliance (not just existence), classifies gaps by impact, and produces a numbered migration plan. Run this when joining an in-progress project or upgrading from an older template version. Distinct from /project-stage-detect (which checks what exists) — this checks whether what exists will actually work with the template's skills."
argument-hint: "[focus: full | cdds | adrs | stories | infra]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, AskUserQuestion
agent: technical-director
---
Read and apply `docs/COLLABORATIVE-DESIGN-PRINCIPLE.md`,
`standards/evidence-lifecycle.md` and `standards/notes-adr-sync.md` for scoped
authority, exact evidence and decision ownership. Existing named authority
continues; analysis is read-only and report-only excludes input/index/state writes.


## User Guide

- When to use: Brownfield onboarding — audits existing project artifacts for template format compliance (not just existence), classifies gaps by impact, and produces a numbered migration plan. Run this when joining an in-progress project or upgrading from an older template version. Distinct from /project-stage-detect (which checks what exists) — this checks whether what exists will actually work with the template's skills.
- Inputs: Command arguments: `/adopt [focus: full | cdds | adrs | stories | infra]`; project artifacts referenced below; user decisions and approvals before writes.
- Outputs: Primary artifacts, reports, or conversation guidance described below; write files only after user approval.
- Memory-bank writes: None.
- Next steps: Follow the workflow hand-off or next-step guidance below; recommendations do not auto-run and require explicit user command/approval.

# Adopt — Brownfield Template Adoption

This skill audits an existing project's artifacts for **format compliance** with
the template's skill pipeline, then produces a prioritised migration plan.

**This is not `/project-stage-detect`.**
`/project-stage-detect` answers: *what exists?*
`/adopt` answers: *will what exists actually work with the template's skills?*

Existing CDDs/ADRs/Stories may lack required substantive contracts or exact
identity. Report the actual affected gap; do not claim already-repaired consumers
silently auto-pass, or certify runtime behavior from an artifact format.

**Output:** `docs/adoption-plan-[date].md` — a persistent, checkable migration plan.

**Argument modes:**

**Audit mode:** `$ARGUMENTS[0]` (blank = `full`)

- **No argument / `full`**: Complete audit — all artifact types
- **`cdds`**: CDD format compliance only
- **`adrs`**: ADR format compliance only
- **`stories`**: Story format compliance only
- **`infra`**: Infrastructure artifact gaps only (registry, manifest, sprint-status, stage.txt)

---

### Skill purpose before adoption

Apply the purpose rule to skills, independent agent/role definitions, native
configuration containing instruction bodies and their exclusive references/overlays.
A Target's development-only role stays local-only even without invoking a skill;
TOML, developer_instructions fields and native loading give no exception. Real
product-use agents follow actual product rules. Independent configuration must be
independent of development instructions/role packages and carry no such body;
a native loader of developer roles is not an independent configuration consumer.

Read `standards/skill-purpose.md` and identify the governed project/product. This
adoption workflow develops a Target and is a local-only template there. In relevant
modes classify product-use/development-only/mixed/unresolved from complete bodies
and references before Git selection. Bespoke names/prompts/overlays/full projections
give no exception. Split mixed content; preserve business documents, independent
configuration and minimal adaptations without developer procedures. Keep required
local packages complete; this audit grants no migration/untracking.

### Project boundary delivery in full and infra adoption

For `full` and `infra`, read the project's actual governing instructions or
law index and the complete installed `constitute` entry's "Reusable Project
Boundary Template". The reusable source is
`templates/memory-bank/t0_core/basic_law_index.md`; its boundary text is also
carried inside that installed entry, so a local maintenance kit or copied
general source tree is not an audit prerequisite.

If the two owner scopes are missing, include an additive merge into the actual
project-owned instruction file, or into an already-authorized
`memory_bank/t0_core/basic_law_index.md`, in the migration plan. Preserve business
code, project design/QA/acceptance documents, histories and existing authorities.
Prepare required neutral templates/spec assets for authorized local use, following
their actual reference closure under `adapters/README.md`. Review Target Git
candidates separately: minimal adaptations, independent configuration, substantive
project documents and qualified product-use skills. None can carry development-instruction bodies
or exclusive overlays. Required local
inputs remain readable but do not become Git candidates. Missing/unread required
originals leave affected use incomplete. Exclude general CDD source mirrors and
template-maintenance materials from the target Git submission/publication set.
Local presence inside or outside the project is allowed; it does not justify
a move, deletion, log-path change or untracking. Review actual diffs/index and
delivery contents; ignore rules alone do not exclude already-tracked material.
Plan approval does not authorize that merge, activate Memory Bank or accept laws.
If the installed boundary text is missing, report that precise delivery gap.

## Phase 1: Detect Project State

Emit one line before reading: `"Scanning project artifacts..."` — this confirms the
skill is running during the silent read phase.

Then read silently before presenting anything else.

### Existence check
- `production/stage.txt` — read declared phase; verify relied-on transition evidence
  separately, without inferring qualification from the value/path
- `design/cdd/game-concept.md` or `design/cdd/product-concept.md` — concept exists?
- `design/cdd/module-index.md` — module index exists?
- Count CDD files: `design/cdd/*.md` (excluding game-concept.md, product-concept.md, module-index.md, and principles.md)
- Count ADR files: `docs/architecture/adr-*.md`
- Count story files: `production/epics/**/*.md` (excluding EPIC.md)
- `standards/technical-preferences.md` — technology stack configured?
- `docs/engine-reference/` or `docs/reference/` — reference docs present?
- Glob `docs/adoption-plan-*.md` — note the filename of the most recent prior plan if any exist

### Candidate phase
Read `standards/technical-preferences.md` domain/capability evidence and concept
bodies; missing/ambiguous concepts never default Game. Use advisory indicators
from `/project-stage-detect`, not completion proofs. Phase names are shown as
**[游戏专用] Game** / **[通用产品] Product**:

- Actual ongoing implementation evidence → candidate Production / Implementation;
  source counts indicate scale only
- Stories in `production/epics/` → Pre-Production / Pre-Implementation
- ADRs exist → Technical Setup / Architecture
- module-index.md exists → Systems Design / Specification
- game-concept.md or product-concept.md exists → Concept
- Nothing → Fresh (not a brownfield project — suggest `/constitute`)

If the project appears fresh (no artifacts at all), use `AskUserQuestion`:
- "This looks like a fresh project — no existing artifacts found. `/adopt` is for
  projects with work to migrate. What would you like to do?"
  - "Run `/constitute` — establish project governance and route to the right workflow"
  - "My artifacts are in a non-standard location — help me find them"
  - "Cancel"

Then stop — do not proceed with the audit regardless of which option the user picks
(each option leads to a different skill or manual investigation).

Report declared phase, observed artifacts, candidate phase and verified qualified
state separately, including CDD/ADR/Story counts. Missing qualification stays
unverified; this format audit does not execute runtime skills.

---

## Phase 2: Format Audit

For each artifact type in scope (based on argument mode), check not just that
the file exists but that it contains the internal structure the template requires.

Audit CDDs in `cdds` or `full`, and infrastructure in `infra` or `full`.
Other subset modes cover only their actual artifact types; a full audit includes
all applicable types. If the argument or applicability is unresolved, retain
Unknown; missing required inputs do not justify skipping their audit. Audit scope
grants no repair, status or runtime authority.

### 2a: CDD Format Audit

Resolve DocKind/owners under `design/INSTRUCTIONS.md`. Module CDDs use semantic
eight in `rules/design-docs.md`; concept/index/support documents use their own
contract. Read substantive bodies and valid historical aliases. Heading scans
locate content, not compliance. Preserved Game/Product heading examples follow:

**[游戏专用]** Game CDD sections:

| Required Section | Heading pattern to look for |
|---|---|
| Overview | `## Overview` |
| Player Fantasy | `## Player Fantasy` |
| Detailed Rules / Design | `## Detailed` or `## Core Rules` or `## Detailed Design` |
| Formulas | `## Formulas` or `## Formula` |
| Edge Cases | `## Edge Cases` |
| Dependencies | `## Dependencies` or `## Depends` |
| Tuning Knobs | `## Tuning` |
| Acceptance Criteria | `## Acceptance` |

**[通用产品]** Product CDD sections:

| Required Section | Heading pattern to look for |
|---|---|
| Overview | `## Overview` |
| User Promise / JTBD | `## User Promise` or `## User Promise / JTBD` |
| Detailed Behavior | `## Detailed Behavior`, `## Detailed Design` or `## Core Specification` |
| Contracts / Data Model | `## Contracts / Data Model`, `## Data Model` or `## Data` |
| Edge Cases | `## Edge Cases` |
| Dependencies | `## Dependencies` or `## Depends` |
| Configuration Knobs | `## Configuration Knobs` or `## Configuration` |
| Acceptance Criteria | `## Acceptance` |

For each CDD, record:
- Which sections are present
- Which sections are missing
- Whether it has any content in present sections or just placeholder text
  (`[To be designed]` or equivalent)

Also check: does each CDD have a `**Status**:` field in its header block?
Valid values: `In Design`, `Designed`, `In Review`, `Approved`, `Needs Revision`.

### 2b: ADR Format Audit

For each ADR file found, check for these critical sections:

| Section | Impact if missing |
|---|---|
| `## Status` | **BLOCKING** for relied-on coverage — decision status/acceptance unverified |
| `## ADR Dependencies` | HIGH — dependency ordering in `/architecture-review` breaks |
| **[游戏专用]** `## Engine Compatibility` / **[通用产品]** `## Technology Compatibility` or `## Stack Compatibility` | HIGH — post-cutoff API risk is unknown |
| `## CDD Requirements Addressed` | MEDIUM — traceability matrix loses coverage |
| `## Performance Implications` | LOW — not pipeline-critical |

Read the actual applicable ADR template and substantive compatibility body.
Established translated/numbered aliases remain valid when they cover the same
required domain, pinned-version and contract roles; a heading or placeholder alone
is not coverage. Preserve the original heading rather than mechanically renaming it.

For each ADR, record: which sections present, which missing, current Status value
if the Status section exists.

### 2c: module-index.md Format Audit

If `design/cdd/module-index.md` exists, read its complete body and the actual
installed `/map-systems` owner with `templates/module-index.md`. Apply their
required roles and preserve valid historical formats; an index is not a module CDD.

1. **Status meaning and downstream use** — read actual row status and provenance.
   Current workflow labels include `Not Started`, `In Progress`, `In Review`,
   `Designed`, `Approved` and `Needs Revision`. Owner-defined historical labels
   such as `In Design` or `Implemented` remain readable observations; they do not
   establish design approval, passing evidence or stage/Story completion. An
   unknown label needs owner clarification. If parenthetical notes or a legacy
   label break a selected downstream workflow's exact comparison, record that
   affected use as incomplete and propose a separately scoped migration; do not
   silently rewrite history or infer the required completion state.

2. **Column and semantic roles** — `Module Name`, `System name` or a substantive
   equivalent identifies the module. Read category, priority and status, plus
   layer information where the actual generating workflow requires it. `Category`
   is not automatically a layer; an actual layer may be recorded in the body's
   category/priority mapping. Missing required roles remain gaps even when all
   column headings exist. Preserve extra columns and valid owner aliases.

### 2d: Story Format Audit

For each story file found:

- Read actual governing requirements/AC, status and linked decisions, not patterns
  alone. Resolve assigned TR-IDs against the registry without manufacturing IDs.
- Bind manifest raw bytes/full digest/size; absent legacy identity needs current
  LegacyRecheck, not auto-pass from dates or missing fields.
- Apply `standards/notes-adr-sync.md`: Accepted ADR where required, named
  `cdd-layer` or justified `no-adr` where valid. Not every Story needs an ADR.
- Preserve in-progress/done Story content/history. Audit required evidence and
  authority separately; never regenerate or grant completion from format alone.

### 2e: Infrastructure Audit

| Artifact | Path | Impact if missing |
|---|---|---|
| TR registry | `docs/architecture/tr-registry.yaml` | HIGH — no stable requirement IDs |
| Control manifest | `docs/architecture/control-manifest.md` | HIGH — no layer rules for stories |
| Manifest version stamp | In manifest header: `Manifest Version:` | MEDIUM — staleness checks blind |
| Sprint status | `production/sprint-status.yaml` | MEDIUM — `/sprint-status` falls back to markdown |
| Stage file | `production/stage.txt` | MEDIUM — phase auto-detect unreliable |
| **[游戏专用]** Engine reference | `docs/engine-reference/[engine]/VERSION.md` | HIGH — ADR engine checks blind |
| **[通用产品]** Stack reference | `docs/reference/[stack]/VERSION.md` | HIGH — ADR stack checks blind |
| Architecture traceability | `docs/architecture/architecture-traceability.md` | MEDIUM — no persistent matrix |

### 2f: Technical Preferences Audit

Read `standards/technical-preferences.md`. Check each field for `[TO BE CONFIGURED]`:
- **[游戏专用]** Engine, Language, Rendering, Physics → HIGH if unconfigured (ADR skills fail)
- **[通用产品]** Language, Framework, Runtime, Database → HIGH if unconfigured (ADR skills fail)
- Naming conventions → MEDIUM
- Performance budgets → MEDIUM
- Forbidden Patterns, Allowed Libraries → LOW (starts empty by design)

---

## Phase 3: Classify and Prioritise Gaps

Organise every gap found across all audits into four severity tiers:

**BLOCKING** — An actual required contract/decision/evidence gap blocks its
dependent workflow or qualification; name the owner and affected scope.
Examples: ADR missing Status field, module-index parenthetical status values,
technology stack not configured when ADRs exist.

**HIGH** — Will cause stories to be generated with missing safety checks, or
infrastructure bootstrapping will fail.
Examples: ADRs missing Technology Compatibility section, CDDs missing Acceptance Criteria
(stories can't be generated from them), tr-registry.yaml missing.

**MEDIUM** — Degrades quality and pipeline tracking but does not break functionality.
Examples: CDDs missing Tuning Knobs or Formulas sections, stories missing TR-IDs,
sprint-status.yaml missing.

**LOW** — Retroactive improvements that are nice-to-have but not urgent.
Examples: Stories missing Manifest Version stamps, CDDs missing Open Questions section.

Count totals per tier. If zero BLOCKING and zero HIGH gaps: report that the project
meets the selected format checks with only advisory gaps; runtime/project
qualification remains separately unverified.

---

## Phase 4: Build the Migration Plan

Compose a numbered, ordered action plan. Ordering rules:
1. BLOCKING gaps first (must fix before any pipeline skill runs reliably)
2. HIGH gaps next, infrastructure before CDD/ADR content (bootstrapping needs correct formats)
3. MEDIUM gaps ordered: CDD gaps before ADR gaps before story gaps (stories depend on CDDs and ADRs)
4. LOW gaps last

For each gap, produce a plan entry with:
- A clear problem statement (one sentence, no jargon)
- The exact command to fix it, if a skill handles it
- Manual steps if it requires direct editing
- A time estimate (rough: 5 min / 30 min / 1 session)
- A checkbox `- [ ]` for tracking

**Special case — module-index parenthetical status values:**
This is always the first item if present. Show the exact values that need changing
and the exact replacement text. Offer to fix this immediately before writing the plan.

**Special case — ADRs missing Status field:**
For each affected ADR, the fix is:
`/architecture-decision retrofit docs/architecture/adr-[NNNN]-[slug].md`
List each ADR as a separate checkable item.

**Special case — CDDs missing sections:**
For each affected CDD, list which sections are missing and the fix:
`/design-system retrofit design/cdd/[filename].md`

**Infrastructure bootstrap ordering** — include only applicable missing effects,
after checking actual owners and authority, in this sequence:
1. Fix ADR formats first (registry depends on reading ADR Status fields)
2. Run `/architecture-review` → bootstraps `tr-registry.yaml`
3. Run `/create-control-manifest` → creates manifest with version stamp
4. Run `/sprint-plan update` → creates `sprint-status.yaml`
5. Run `/gate-check [phase]` → evaluate actual required evidence; stage writes
   need separately covered transition authority

**Existing stories** — note explicitly:
> Preserve in-progress/done bodies and historical labels. Missing TR/manifest
> identity needs owning-workflow legacy recheck; it never automatically passes.
> Repair approved gaps only, preserving exact reviewed baselines.

---

## Phase 5: Present Summary and Ask to Write

Present a compact summary before writing:

```
## Adoption Audit Summary
Phase detected: [phase]
Domain / engine or stack: [evidence-backed; configured / NOT CONFIGURED]
CDDs audited: [N] ([X] fully compliant, [Y] with gaps)
ADRs audited: [N] ([X] fully compliant, [Y] with gaps)
Stories audited: [N]

Gap counts:
  BLOCKING: [N] — template skills will malfunction without these fixes
  HIGH:     [N] — unsafe to run /create-stories or /story-readiness
  MEDIUM:   [N] — quality degradation
  LOW:      [N] — optional improvements

Estimated remediation: [X blocking items × ~Y min each = roughly Z hours]
```

Before asking to write, show a **Gap Preview**:
- List every BLOCKING gap as a one-line bullet describing the actual problem
  (e.g. `module-index.md: 3 rows have parenthetical status values`,
  `adr-0002.md: missing ## Status section`). No counts — show the actual items.
- Show HIGH / MEDIUM / LOW as counts only (e.g. `HIGH: 4, MEDIUM: 2, LOW: 1`).

This gives the user enough context to judge scope before committing to writing the file.

If a prior adoption plan was detected in Phase 1, add a note:
> "A previous plan exists at `docs/adoption-plan-[prior-date].md`. The new plan will
> reflect current project state — it does not diff against the prior run."

When exact plan authority is absent, use `AskUserQuestion` after the summary:
- "Ready to write the migration plan?"
  - "Yes — write `docs/adoption-plan-[date].md`"
  - "Show me the full plan preview first (don't write yet)"
  - "Cancel — I'll handle migration manually"

If the user picks "Show me the full plan preview", output the complete plan as a
fenced markdown block. Then request only missing write authority; matching named plan scope continues.

---

## Phase 6: Write the Adoption Plan

If approved, write `docs/adoption-plan-[date].md` with this structure:

```markdown
# Adoption Plan

> **Generated**: [date]
> **Project phase**: [phase]
> **Domain / Engine or Stack**: [actual source + configured reference; installed state unverified]
> **Template version**: v0.2.0

Work through these steps in order. Check off each item as you complete it.
Re-run `/adopt` anytime to check remaining gaps.

---

## Step 1: Fix Blocking Gaps

[One sub-section per blocking gap with problem, fix command, time estimate, checkbox]

---

## Step 2: Fix High-Priority Gaps

[One sub-section per high gap]

---

## Step 3: Bootstrap Infrastructure

### 3a. Register existing requirements (creates tr-registry.yaml)
Run `/architecture-review` — even if ADRs already exist, this run bootstraps
the TR registry from your existing CDDs and ADRs.
**Time**: 1 session (review can be long for large codebases)
- [ ] tr-registry.yaml created

### 3b. Create control manifest
Run `/create-control-manifest`
**Time**: 30 min
- [ ] docs/architecture/control-manifest.md created

### 3c. Create sprint tracking file
Run `/sprint-plan update`
**Time**: 5 min (if sprint plan already exists as markdown)
- [ ] production/sprint-status.yaml created

### 3d. Verify proposed project transition
Run `/gate-check [current-phase]`
**Time**: 5 min
- [ ] Required transition evidence/authority verified; only covered stage effects written

---

## Step 4: Medium-Priority Gaps

[One sub-section per medium gap]

---

## Step 5: Optional Improvements

[One sub-section per low gap]

---

## What to Expect from Existing Stories

Preserve existing bodies and historical status. Missing legacy TR/manifest fields
need current owning-workflow recheck, not automatic PASS or regeneration. Format
audits cannot certify qualified Story/project state.

---

## Re-run

Run `/adopt` again after completing Step 3 to verify all blocking and high gaps
are resolved. The new run will reflect the current state of the project.
```

---

## Phase 6b: Set Review Mode

Only when review-mode setup is in requested scope, check whether
`production/review-mode.txt` exists.

**If it exists**: Read/trim its actual value. Valid `full`/`lean`/`solo` may be
reused without another prompt; an empty/invalid value is reported for correction
before dependent mode claims, never silently skipped, defaulted or rewritten.

**If it does not exist**: Use `AskUserQuestion`:

- **Prompt**: "One more setup step: how much design review would you like as you work through the workflow?"
- **Options**:
  - `Full` — Director specialists review at each key workflow step. Best for teams, learning the workflow, or when you want thorough feedback on every decision.
  - `Lean (recommended)` — Directors only at phase gate transitions (/gate-check). Skips per-skill reviews. Balanced for solo devs and small teams.
  - `Solo` — No director reviews at all. Maximum speed. Best for game jams, prototypes, or if reviews feel like overhead.

Review preference is content agreement, not a hidden write effect. Reuse authority
naming `production/review-mode.txt`; otherwise show that path/effect and ask
"May I write this review mode?" before persisting:
- `Full` → write `full`
- `Lean (recommended)` → write `lean`
- `Solo` → write `solo`

Create the `production/` directory if it does not exist.

---

## Phase 7: Offer First Action

After writing the plan, don't stop there. Pick the single highest-priority gap
and offer to handle it immediately using `AskUserQuestion`. Choose the first
branch that applies:

**If there are parenthetical status values in module-index.md:**
Use `AskUserQuestion`:
- "The most urgent fix is `module-index.md` — [N] rows have parenthetical status
  values (e.g. `Needs Revision (see notes)`) that break /gate-check,
  /create-stories, and /architecture-review right now. I can fix these in-place."
  - "Fix it now — edit module-index.md"
  - "I'll fix it myself"
  - "Done — leave me with the plan"

**If ADRs are missing `## Status` (and no parenthetical issue):**
Use `AskUserQuestion`:
- "The most urgent fix is adding `## Status` to [N] ADR(s): [list filenames].
  Without it, required decision status/acceptance remains unverified. Start with
  [first affected filename]?"
  - "Yes — retrofit [first affected filename] now"
  - "Retrofit all [N] ADRs one by one"
  - "I'll handle ADRs myself"

**If CDDs are missing Acceptance Criteria (and no blocking issues above):**
Use `AskUserQuestion`:
- "The most urgent gap is missing Acceptance Criteria in [N] CDD(s):
  [list filenames]. Without them, /create-stories can't generate stories.
  Start with [highest-priority CDD filename]?"
  - "Yes — add Acceptance Criteria to [CDD filename] now"
  - "Do all [N] CDDs one by one"
  - "I'll handle CDDs myself"

**If no BLOCKING or HIGH gaps exist:**
Use `AskUserQuestion`:
- "No blocking gaps in the audited format scope. Runtime/project qualification is
  separate. What next?"
  - "Walk me through the medium-priority improvements"
  - "Run /project-stage-detect for a broader health check"
  - "Done — I'll work through the plan at my own pace"

---

## Collaborative Protocol

1. **Read silently** — complete the full audit before presenting anything
2. **Show the summary first** — let the user see scope before asking to write
3. **Scoped writes** — reuse named plan authority; ask only for missing/new effects.
   Plan-only excludes repairs, review mode and state.
4. **Offer, don't force** — the plan is advisory; the user decides what to fix and when
5. **One action at a time** — after handing off the plan, offer one specific next step,
   not a list of six things to do simultaneously
6. **Preserve existing bodies/history** — repair named approved gaps only;
   do not silently regenerate CDDs/ADRs/Stories or destroy unique prior content.

Read stack/version context when the selected Product audit evaluates
infrastructure, applicable ADR compatibility, or a CDD/Story contract that names
that stack. Resolve the actual stack key from configuration. Do not limit this
to infrastructure or require it for every Product subset; unresolved applicability
stays Unknown.

Read actual Product user promise/API/CLI/SDK/data/auth/workflow contracts, surface
profile and `docs/reference/[stack]/VERSION.md` as applicable. Retain Game Player
Fantasy/formulas/tuning/engine/playtest examples. Missing inapplicable infrastructure
gets justified N/A. Diagnose/offer repairs independently of plan saving; zero
BLOCKING/HIGH counts do not certify runtime/template qualification.
