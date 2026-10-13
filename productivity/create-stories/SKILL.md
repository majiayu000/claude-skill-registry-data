---
name: create-stories
description: "Break a single epic into implementable story files. Reads the epic, its CDD, governing ADRs, and control manifest. Each story embeds its CDD requirement TR-ID, ADR guidance, acceptance criteria, story type, and test evidence path. Run after /create-epics for each epic."
argument-hint: "[epic-slug | epic-path] [--review full|lean|solo]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Task, AskUserQuestion
agent: lead-programmer
---

## Scope, decisions and exact evidence

Read `standards/evidence-lifecycle.md` and `standards/notes-adr-sync.md` from the
project root. Reuse original authorization only for its exact named paths, effects
and limits across roles/retries. Content agreement, writes, independent review,
ADR acceptance and Story/phase completion remain separate. Show a concrete draft
before asking about unresolved material choices or new effects; covered writes
need no repeated per-file or per-role permission.

Read/review-only never invokes a write entrypoint, including in memory. Report-only
may write its assigned new report, not inputs, indexes, session state, logs or T3
pointers. Each other effect needs existing scope or separate changeset authority.
No Memory Bank means the existing Story/review/conversation fallback, not activation.

Bind claims to original paths, full SHA-256 (64 hex), byte sizes, collection time
with timezone, source commit plus exact uncommitted/ignored/external identities.
Read actual bodies and minimum required direct/indirect evidence closure; retain
recoverable originals and disclose missing inputs. Resolve CDD DocKind/required
owner set and module semantic eight through `design/INSTRUCTIONS.md`, preserving
substantive aliases; headings, counts or existence cannot establish PASS.

Classify each meaningful choice as `covered`, `cdd-layer`, `no-adr`,
`documentation-update`, `adr-required` or `conflict`, with named requirement/owner,
existing TR-ID if assigned, exact Accepted ADR revision/section/scope or justified
no-ADR reason, affected paths/dependencies, evidence and action/owner/due phase.
Trust boundaries, public contracts, durable formats, state ownership and governing
architectural constraints require an Accepted decision or valid scoped exception
under existing governance before affected implementation starts/continues. Continue
independent work. Proposed, implemented, green tests, write approval and director
recommendations do not establish acceptance; historical approval needs exact input
and authority/scope match. Justified `cdd-layer`/`no-adr` waives no other readiness,
manifest or evidence prerequisite. The existing global Technical Setup minimum of
three Foundation ADRs in `workflow/workflow-catalog.yaml` remains a separate gate:
do not bypass it or manufacture ADRs to meet a count.

Absent, conflicting or ambiguous concept/domain evidence means Unknown. Continue
domain-independent checks; resolve the domain before applying its Game/Product
rules. Do not silently default to Game.

## User Guide

- When to use: Break a single epic into implementable story files. Reads the epic, its CDD, governing ADRs, and control manifest. Each story embeds its CDD requirement TR-ID, ADR guidance, acceptance criteria, story type, and test evidence path. Run after /create-epics for each epic.
- Inputs: Command arguments: `/create-stories [epic-slug | epic-path] [--review full|lean|solo]`; project artifacts referenced below; user decisions and approvals before writes.
- Outputs: Primary artifacts, reports, or conversation guidance described below; write files only after user approval.
- Memory-bank writes: None.
- Next steps: Follow the workflow hand-off or next-step guidance below; recommendations do not auto-run and require explicit user command/approval.

# Create Stories

A story is a single implementable behaviour — small enough to complete in one
focused session, self-contained, and fully traceable to a CDD requirement and
a justified decision disposition. Stories are what developers pick up. Epics are what architects
define.

**Run this skill per epic**, not per layer. Run it for Foundation epics first,
then Core, and so on — matching the dependency order.

**Output:** story files under `production/epics/[epic-slug]/`, named `story-NNN-[slug].md`

**Previous step:** `/create-epics [system]`
**Next step after stories exist:** `/story-readiness [story-path]` then `/dev-story [story-path]`

---

## 1. Parse Argument

Resolve review mode once: explicit `--review full|lean|solo`, else the actual
`production/review-mode.txt`, else lean when absent. Validate explicit/global values;
invalid values require correction and cannot silently fall back. This single mode
applies to all gate spawns under `standards/director-gates.md`.

- `/create-stories [epic-slug]` — e.g. `/create-stories combat`
- `/create-stories production/epics/combat/EPIC.md` — full path also accepted
- No argument — ask: "Which epic would you like to break into stories?"
  Glob `production/epics/*/EPIC.md` and list available epics with their status.

---

## 2. Load Everything for This Epic

Read in full:

- `production/epics/[epic-slug]/EPIC.md` — epic overview, governing ADRs, CDD requirements table
- The actual CDD (`design/cdd/[filename].md`) — resolve DocKind under
  `design/INSTRUCTIONS.md`, read substantive owner bodies/references; module CDDs
  map semantic eight, preserving existing aliases
- All governing ADRs listed in the epic — read the Decision, Implementation Guidelines, and Technology Compatibility (Engine Compatibility for game, Technology/Stack Compatibility for product) sections
- `docs/architecture/control-manifest.md` — read complete raw bytes and layer rules;
  compute full SHA-256 and byte size, retaining the readable date separately
- `docs/architecture/tr-registry.yaml` — load all TR-IDs for this system

**ADR existence validation**: After reading the governing ADRs list from the epic, confirm each referenced ADR file exists on disk. Missing required ADRs block only
 their affected drafts before decomposition; independent stories may continue:

Resolve and read each actual required governing ADR from the Epic and affected Story decision disposition. A justified independent CDD-layer/no-adr Story has no ADR dependency, while all other required inputs remain binding. If the governing reference or disposition is unresolved, retain Unknown; missing or Proposed required ADRs keep affected drafts Blocked. Input resolution grants no acceptance or write authority.

> "Epic references [ADR-NNNN: title] but `docs/architecture/[adr-file].md` was not found.
> Check the filename in the epic's Governing ADRs list, or run `/architecture-decision`
> to create it. Affected drafts remain Blocked until required governing inputs are present and Accepted."

Existence does not establish acceptance. Verify exact Accepted revision/section/
scope for required decisions. Proposed/conflict/missing inputs keep affected drafts
Blocked; independent stories may be decomposed. CDD-layer/no-adr stories need no
invented ADR, but still satisfy CDD/TR/manifest and all other readiness checks.

Report actual inputs: epic/CDD paths and identities; ADRs found/missing, their
statuses and six dispositions; manifest readable date plus full raw SHA-256/size
or LegacyRecheck/incomplete identity; affected Draft/Blocked stories and independent
eligible scope. Say "all confirmed present" only when actually verified. Missing
required inputs remain visible throughout decomposition and the closing summary.

---

## 3. Classify Stories by Type

Before assigning Product test evidence paths, read the actual project test
configuration, configured test roots, runner discovery/naming conventions and
verification commands, including roots outside `tests/`. Choose exact future
paths for the owning module and required checks; the conventional directories
below are examples. Unresolved required configuration leaves affected evidence
planning incomplete, without inventing a runner or changing the project layout.

**Story Type Classification** — assign each story a type based on its acceptance criteria:

**[游戏专用]** Game story types:
| Story Type | Assign when criteria reference... |
|---|---|
| Logic | formulas, calculations, state machines, algorithms |
| Integration | cross-system data flow, signals, save/load round-trips between game systems |
| Visual/Feel | animations, VFX, shaders, feel, juice, timing, audio sync |
| UI | menus, HUD, player-facing displays, input handling |
| Config/Data | tuning values, item databases, level data, game constants |

**[通用产品]** Product story types:
| Story Type | Assign when criteria reference... |
|---|---|
| API | endpoint contracts, request/response shapes, status codes |
| CLI | command-line interface, argument parsing, output formatting |
| Data/Migration | schema changes, data transformations, migration scripts |
| Auth/Permission | authentication, authorization, role-based access |
| Workflow | multi-step business logic, state machines, process orchestration |
| UI | screens, components, user-facing interactions |
| Integration | external service calls, webhooks, message queues |
| Ops/Deployment | CI/CD, containerization, infrastructure, monitoring |
| Config | environment variables, feature flags, application settings |

Mixed stories: assign the type that carries the highest implementation risk.
The type determines what test evidence is required before `/story-done` can close the story.

---

## 4. Decompose the CDD into Stories

For each CDD acceptance criterion:

1. Group related criteria that require the same core implementation
2. Each group = one story
3. Order stories: foundational behaviour first, edge cases last, UI last

**Story sizing rule:** one story = one focused session (~2-4 hours). If a
group of criteria would take longer, split into two stories.

For each story, determine:
- **CDD requirement**: which acceptance criterion(ia) does this satisfy?
- **TR-ID**: verify the current active registry entry and exact CDD requirement.
  Reuse its stable ID. No match is an explicit unassigned requirement/registration
  action, never fabricated `TR-[system]-???`; affected draft stays Blocked.
- **Decision disposition**: exact Accepted revision/scope for covered, named CDD/
  owner/evidence for cdd-layer, local reason/owner for no-adr. Required Proposed,
  adr-required/conflict means Blocked with action/owner. Draft writing is not readiness.
- **Story Type**: from Step 3 classification
- **Technology risk**: for covered, read the actual ADR Knowledge Risk and pinned
  compatibility evidence. For cdd-layer/no-adr, use the named CDD/local owner and
  configured VERSION/stack references; mark ADR-only fields N/A with reason.
  Unknown required technology risk/evidence is incomplete, never assumed LOW.

---

## 4b. QA Lead Story Readiness Gate

Resolve explicit required QA scope before consuming a mode skip; missing required assessment stays NotRun/Blocked/Pending for dependent readiness. Default optional orchestration creates no extra gate.

**Review mode check** — apply before spawning QL-STORY-READY:
- `solo` → skip. Note: "QL-STORY-READY skipped — Solo mode." Proceed to Step 5 (present stories for review).
- `lean` → skip (not a PHASE-GATE). Note: "QL-STORY-READY skipped — Lean mode." Proceed to Step 5 (present stories for review).
- `full` → spawn as normal.

After decomposing all stories (Step 4 complete) but before presenting them for write approval, spawn `qa-lead` via Task using gate **QL-STORY-READY** (`standards/director-gates.md`).

Pass: the full story list with acceptance criteria, story types, and TR-IDs; the epic's CDD acceptance criteria for reference.

Present the QA lead's assessment. For each story flagged as GAPS or INADEQUATE, revise the acceptance criteria before proceeding — stories with untestable criteria cannot be implemented correctly. Once all stories reach ADEQUATE, proceed.

**After ADEQUATE**: ask the qa-lead to produce concrete test case specifications
for every automated-evidence story type — Game: Logic / Integration; Product:
API / Data/Migration / Auth/Permission / Workflow / Integration. Produce one
test case per acceptance criterion in this format:

```
Test: [criterion text]
  Given: [precondition]
  When: [action]
  Then: [expected result / assertion]
  Edge cases: [boundary values or failure states to test]
```

For manual or smoke-evidence story types — Game: Visual/Feel / UI / Config/Data;
Product: CLI / UI / Ops/Deployment / Config — produce verification steps instead:
```
Manual check: [criterion text]
  Setup: [how to reach the state]
  Verify: [what to look for]
  Pass condition: [unambiguous pass description]
```

Embed test case specs actually produced in each Story's `## QA Test Cases` section,
with actual author/source identity and review run state. When qa-lead completed
this work, the developer implements against those cases. A skipped/NotRun QA
assessment does not create a QA-authored plan; record its absence and any outstanding
planning/evidence action under the applicable Story checks, without inventing execution.

Read actual catalog/selected QA scope: QA plan/team orchestration optional by
default; explicit strict obligations need source/authority/scope. Mode-skipped
QL-STORY-READY is not completed assessment. Actual-author planning cases can define
later verification, but draft/ADEQUATE/write approval is not executed PASS. Required
Story AC/DoD/evidence remains binding in every mode. Explicitly required assessment
cannot be waived by a mode skip; retain NotRun/Blocked/Pending and block only its
dependent readiness/closure. Preserve actual author/source/review-state fields.

---

## 5. Present Stories for Review

Before writing any files, present the full story list:

```
## Stories for Epic: [name]

Story 001: [title] — Logic — ADR-NNNN
  Covers: TR-[system]-001 ([1-line summary of requirement])
  Test required: tests/unit/[system]/[slug]_test.[ext]

Story 002: [title] — Integration — ADR-MMMM
  Covers: TR-[system]-002, TR-[system]-003
  Test required: tests/integration/[system]/[slug]_test.[ext]

Story 003: [title] — Visual/Feel — ADR-NNNN
  Covers: TR-[system]-004
  Evidence required: production/qa/evidence/[slug]-evidence.md

Product example (conventional layout shown; use actual configured paths):

Story 001: [title] — API — ADR-NNNN
  Covers: TR-[system]-001 ([1-line summary of requirement])
  Test required: tests/api/[slug]_test.[ext]

Story 002: [title] — Workflow — ADR-MMMM
  Covers: TR-[system]-002
  Test required: tests/integration/[module]/[slug]_test.[ext]

[N stories total, grouped by the domain-appropriate Story Type list]
```

Use `AskUserQuestion`:
- Prompt (for uncovered effects): "May I write these [N] stories to `production/epics/[epic-slug]/` and the described EPIC table?"
- Options: `[A] Yes — write all [N] stories` / `[B] Not yet — I want to review or adjust first`

---

## 6. Write Story Files

For each story, write a file under `production/epics/[epic-slug]/` named `story-[NNN]-[slug].md`:

```markdown
# Story [NNN]: [title]

> **Epic**: [epic name]
> **Status**: [Draft / Ready after all applicable readiness checks / Blocked with reason]
> **Layer**: [Foundation / Core / Feature / Presentation]
> **Type**: [one Story Type from the game or product list]
> **Manifest Version**: [readable header date; legacy compatibility]
> **Manifest SHA-256**: [full 64-hex digest of complete saved raw bytes]
> **Manifest Bytes**: [exact byte size]
> **Manifest Path / Collected At**: [original path / time with timezone]

## Context

**CDD**: `design/cdd/[filename].md`
**CDD / TR Registry Identity**: [exact paths, full SHA-256, sizes, collection time]
**CDD Requirement Section**: [named requirement/criterion; preserve aliases]
**Requirement**: `TR-[system]-NNN`
*(Requirement text lives in `docs/architecture/tr-registry.yaml` — read fresh at review time)*

**Decision Disposition**: [covered / cdd-layer / no-adr / documentation-update / adr-required / conflict]
**ADR Governing Implementation**: [exact path/revision/section/Accepted scope OR justified CDD/local owner/reason]
**Decision Identity / Evidence**: [full hashes/sizes, retained original, acceptance authority/time/scope if applicable]
**ADR Decision Summary**: [governing Accepted choice or named CDD/local rationale]

**Technology**: [engine or stack name + version] | **Risk**: [LOW / MEDIUM / HIGH]
**Technology Notes**: [covered: actual ADR Engine Compatibility or Technology/Stack Compatibility; cdd-layer/no-adr: exact CDD/local owner + configured VERSION/stack references]
**ADR-only Fields**: [actual values for covered / N/A with no-ADR reason]
**Required Technology Gaps**: [None with evidence / unknown risk or missing verification; affected Draft/Blocked scope]

**Control Manifest Rules (this layer)**:
- Required: [relevant required pattern]
- Forbidden: [relevant forbidden pattern]
- Guardrail: [relevant performance guardrail]

---

## Acceptance Criteria

*From CDD `design/cdd/[filename].md`, scoped to this story:*

- [ ] [criterion 1 — directly from CDD]
- [ ] [criterion 2]
- [ ] [performance criterion if applicable]

---

## Implementation Notes

*Source selected by disposition: covered — actual Accepted ADR Implementation
Guidelines; cdd-layer/no-adr — named substantive CDD/local owner contract.
Record the actual path/section/identity and justified N/A ADR-only fields.*

[Specific guidance from actual Accepted ADR/CDD-owned contract, without changing
meaning. Programmers read current exact owner inputs too; embedded notes do not
replace that check. No-ADR rationale must not fabricate a decision.]

---

## Out of Scope

*Handled by neighbouring stories — do not implement here:*

- [Story NNN+1]: [what it handles]

---

## QA Test Cases

*Actual author/source: [identified qa-lead output or authorized plan owner/source].
QA review state: [Completed / Skipped with mode / NotRun / Blocked with reason].
Use the actual approved cases; absent cases remain a declared planning/evidence action,
never a claim that qa-lead already authored or reviewed them.*

**[For automated-evidence stories — Game Logic/Integration; Product API/Data-Migration/Auth-Permission/Workflow/Integration]:**

- **AC-1**: [criterion text]
  - Given: [precondition]
  - When: [action]
  - Then: [assertion]
  - Edge cases: [boundary values / failure states]

**[For manual or smoke-evidence stories — Game Visual/Feel/UI/Config/Data; Product CLI/UI/Ops-Deployment/Config]:**

- **AC-1**: [criterion text]
  - Setup: [how to reach the state]
  - Verify: [what to look for]
  - Pass condition: [unambiguous pass description]

---

## Test Evidence

**Story Type**: [type]
**Required evidence**:

**[游戏专用] Game evidence**
- Logic: `tests/unit/[system]/[story-slug]_test.[ext]` — must exist and pass
- Integration: `tests/integration/[system]/[story-slug]_test.[ext]` OR playtest/session log doc
- Visual/Feel: `production/qa/evidence/[story-slug]-evidence.md` + sign-off
- UI: `production/qa/evidence/[story-slug]-evidence.md` or interaction test
- Config/Data: smoke check pass (`production/qa/smoke-*.md`)

**[通用产品] Product evidence**
**Test configuration**: [actual configured roots, runner discovery/naming rules, verification command and source]
**Exact evidence paths**: [resolve each required file for this Story; valid roots outside `tests/` are supported]

Planned files are future outputs at Story creation. Before closure, every required
automated test must exist, be discovered by the configured runner and have matching
actual PASS evidence. Conventional paths below are examples, not required layouts.

- API: contract test at [exact configured path], e.g. `tests/api/[story-slug]_test.[ext]`
- CLI: command smoke evidence in `production/qa/evidence/smoke/[story-slug].md`
- Data/Migration: migration test at [exact configured path], e.g. `tests/integration/[story-slug]_test.[ext]`
- Auth/Permission: permission test at [exact configured path] covering the Story's actual role, token or access boundary; e.g. `tests/unit/auth/` or `tests/api/`
- Workflow: integration test at [exact configured path], e.g. `tests/integration/[module]/[story-slug]_test.[ext]`
- UI: walkthrough doc or screenshot in `production/qa/evidence/[story-slug]-evidence.md`
- Integration: integration test or API contract test at [exact configured path]
- Ops/Deployment: deployment smoke report in `production/qa/smoke-*.md`
- Config: config validation test or smoke check report

**Status**: [ ] Not yet created

---

## Dependencies

- Depends on: [Story NNN-1 must be DONE, or "None"]
- Unlocks: [Story NNN+1, or "None"]
```

### Also update `production/epics/[epic-slug]/EPIC.md`

Only with named EPIC update authority, replace "Stories: Not yet created" with a
table retaining actual Draft/Blocked/readiness states. Story-set approval does not
implicitly authorize this adjacent file; report its pending action otherwise:

```markdown
## Stories

| # | Story | Type | Status | ADR |
|---|-------|------|--------|-----|
| 001 | [title] | Logic | [actual Draft/Blocked/Ready] | ADR-NNNN |
| 002 | [title] | Integration | [actual Draft/Blocked/Ready] | ADR-MMMM |
```

---

## 7. After Writing

Use `AskUserQuestion` to close with context-aware next steps:

Check:
- Are there other epics in `production/epics/` without stories yet? List them.
- Is this the last epic? If so, include `/sprint-plan` as an option.

Widget:
- Prompt: "[N] stories written to `production/epics/[epic-slug]/`: [D] Draft,
  [B] Blocked, [R] Ready after applicable checks. Pending inputs/actions: [actual list].
  What next?"
- Options (include all that apply):
   - `[A] Check readiness — run /story-readiness [first-eligible-story-path]`
     (only for eligible scope; resolve listed blockers before affected implementation)
  - `[B] Create stories for [next-epic-slug] — run /create-stories [slug]` (only if other epics have no stories yet)
  - `[C] Plan the sprint — run /sprint-plan` (only if all epics have stories)
  - `[D] Stop here for this session`

Note in output: "Work through stories in order — each story's `Depends on:` field tells you what must be DONE before you can start it."

---

## Collaborative Protocol

1. **Read before presenting** — load all inputs silently before showing the story list
2. **Ask once** — present all stories for the epic in one summary, not one at a time
3. **Warn on blocked stories** — flag any story with a Proposed ADR before writing
4. **Scope before writing** — reuse exact approved story-set/EPIC effects; show the
   full qualified draft and ask only for uncovered paths/effects
5. **No invention** — acceptance criteria come from CDDs, implementation notes from ADRs, rules from the manifest
6. **Never start implementation** — this skill stops at the story file level

After writing (or declining):

- **Write operation: COMPLETE** — [N] stories written to `production/epics/[epic-slug]/`;
  report [D] Draft / [B] Blocked / [R] Ready, actual findings and pending actions.
  This operation verdict grants no Story readiness or implementation authority.
  Run `/story-readiness` for eligible scope before `/dev-story`; resolve affected blockers.
- **Verdict: BLOCKED** — user declined. No story files written.

## Exact-byte check availability

Use available read-only tools to collect complete raw-file SHA-256/byte size without
normalizing line endings. If exact bytes/digest or a required dependency cannot be
read, report the affected check incomplete; do not substitute a date, text rendering,
short hash or file existence. Analysis invokes no write entrypoint.
