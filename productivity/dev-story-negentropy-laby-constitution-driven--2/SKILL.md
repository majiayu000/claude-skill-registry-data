---
name: dev-story
description: "Read a story file and implement it. Loads the full context (story, CDD requirement, ADR guidelines, control manifest), routes to the right programmer agent for the system and technology stack, implements the code and required evidence, and confirms each acceptance criterion. The core implementation skill — run after /story-readiness, before /code-review and /story-done."
argument-hint: "[story-path]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Bash, Task, AskUserQuestion
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

- When to use: Read a story file and implement it. Loads the full context (story, CDD requirement, ADR guidelines, control manifest), routes to the right programmer agent for the system and technology stack, implements the code and required evidence, and confirms each acceptance criterion. The core implementation skill — run after /story-readiness, before /code-review and /story-done.
- Inputs: Command arguments: `/dev-story [story-path]`; project artifacts referenced below; user decisions and approvals before writes.
- Outputs: Primary artifacts, reports, or conversation guidance described below; write files only after user approval.
- Memory-bank writes: None.
- Next steps: Follow the workflow hand-off or next-step guidance below; recommendations do not auto-run and require explicit user command/approval.

# Dev Story

This skill bridges planning and code. It reads a story file in full, assembles
all the context a programmer needs, routes to the correct specialist agent, and
drives implementation to completion — including writing the test.

**The loop for every story:**
```
/qa-plan sprint           ← optional default planning; explicitly selected strict obligations apply
/story-readiness [path]   ← validate before starting
/dev-story [path]         ← implement it  (this skill)
/code-review [files]      ← review it
/story-done [path]        ← verify and close it
```

**After exact eligible Story closures:** consider optional `/team-qa sprint`; explicitly selected strict obligations apply to their actual scope. Required AC/evidence/phase checks are never waived by optional orchestration.

**Output:** Source code plus the story's required test, smoke, or evidence artifact.

---

## Phase 1: Find the Story

**If a path is provided**: read that file directly.

**If no argument**: check `production/session-state/active.md` for the active
story. If found, confirm: "Continuing work on [story title] — is that correct?"
If not found, ask: "Which story are we implementing?" Glob
`production/epics/**/*.md` and list stories with Status: Ready.

---

## Phase 2: Load Full Context

Before implementation resolve the actual CDD requirement, TR registry, decision
disposition and control manifest. Read required exact saved inputs/dependencies, not
headers alone. Missing required CDD/TR/manifest or Accepted evidence means BLOCKED
for affected implementation; report in conversation without a session/Story status
write unless that effect is authorized. Justified cdd-layer/no-adr needs no ADR file
but all other prerequisites remain. Required Proposed/adr-required/conflict waits
for exact acceptance or valid scoped exception; spawn no affected programmer.

Read all of the following simultaneously — these are independent reads. Do not start implementation until all context is loaded:

### The story file
Extract and hold:
- **Story title, ID, layer, type**:
  - Game types: Logic / Integration / Visual/Feel / UI / Config/Data
  - Product types: API / CLI / Data/Migration / Auth/Permission / Workflow / UI / Integration / Ops/Deployment / Config
- **TR-ID** — the CDD requirement identifier
- **Governing ADR** reference
- **Manifest Version** embedded in story header
- **Acceptance Criteria** — every checkbox item, verbatim
- **Implementation Notes** — the ADR guidance section in the story
- **Out of Scope** boundaries
- **Test Evidence** — the required test file path
- **Dependencies** — what must be DONE before this story

### The TR registry
Read `docs/architecture/tr-registry.yaml`. Look up the story's TR-ID.
Read the current `requirement` text — this is the source of truth for what the
CDD requires now. Do not rely on any inline text in the story file (may be stale).

### Governing decision and CDD
Read actual CDD bodies under `design/INSTRUCTIONS.md` (correct DocKind/semantic
roles/aliases); confirm the registry requirement still matches its Target.
For covered, read actual ADR and acceptance original; verify exact revision/
section/authority/scope rather than a status label. For cdd-layer/no-adr read the
named owner/reason/evidence and configured VERSION/stack references.
Select the actual sources by disposition:
- For covered: extract the full ADR Decision and Implementation Guidelines;
  read Engine Compatibility (game) or Technology/Stack Compatibility (product),
  post-cutoff API verification, known risks and ADR Dependencies.
- For cdd-layer/no-adr: extract substantive CDD/local implementation contracts,
  owner dependencies and technology evidence from configured VERSION/stack
  references. ADR-only sections are N/A with a named reason, never fabricated.
- Unknown required technology risk/verification remains incomplete and blocks
  affected implementation; other CDD/TR/manifest/readiness checks still apply.

### The control manifest
Read `docs/architecture/control-manifest.md`. Extract the rules for this story's layer:
- Required patterns
- Forbidden patterns
- Performance guardrails

Read complete current manifest raw bytes; compare full `Manifest SHA-256`,
`Manifest Bytes` and original path with the Story identity. Readable version dates
cannot prove freshness, including same-day changes. Mismatch/date-only/absent hash
is `LegacyRecheck`: inspect rules and affected CDD/decision/dependency scope before
implementation. Reuse authorized Story update scope; otherwise show concrete diff
and obtain authority for that effect. Read back the exact identity. Do not merely
replace dates or invent old hashes. Old-rules exceptions need recoverable exact old
bytes/full hash/size, affected scope, authority and risks under existing governance.
Missing required inputs remain Blocked; independent authorized work may continue.

### Dependency validation

Read the selected Story's Dependencies list and classify which dependencies are
required. Resolve each actual nonempty required set using the checks below;
an explicitly empty or non-required list needs no dependency lookup. Unresolved
classification stays Unknown. An empty glob or Story status text cannot close a
real named dependency.

After extracting the **Dependencies** list from the story file, validate each:

1. Glob `production/epics/**/*.md` to find each required dependency Story; read
   its complete original body and exact identity. A missing required dependency
   means **BLOCKED** for affected implementation; spawn no affected programmer.
   Report path/action/owner and continue independent authorized work.
2. Read `Status:` plus the actual required closure evidence under its owning
   `/story-done` workflow. Complete/Done text or a user declaration alone cannot
   prove closure; missing/incomplete required evidence remains **BLOCKED**.
3. For a required unmet dependency, report actual status, evidence gaps and affected
   scope before using `AskUserQuestion`:
   - Prompt: "Required dependency '[title]' is unresolved: [actual gap]. How should
     we resolve it before affected implementation?"
   - Options:
     - `[A] Consider a scoped exception under existing governance`
     - `[B] Stop affected implementation — complete the dependency first`
     - `[C] Verify a claimed prior completion through the closure owner`
   - [A] permits only the exact paths/effects and limits of a valid evidenced
     exception allowed by existing governance. Record authority/time/scope, actual
     dependency identities, risks, owner and unresolved actions; preserve Incomplete
     facts. Mere risk acceptance is not an exception or completion. Without valid
     exception, affected implementation stays Blocked.
   - [B] keeps affected implementation Blocked; any session write needs its named scope.
   - [C] independently reads the dependency original and required closure evidence.
     Route `/story-done` to validate closure; only after actual checks pass may an
     independently authorized status effect record Complete. No update from a
     statement or file-write approval, and no implicit closure inside `/dev-story`.
4. Resume affected work only after verified required closure or within a valid exact
   scoped exception. Preserve actual findings in the implementation summary.

---

### Technology reference
Read `standards/technical-preferences.md`:
- **[游戏专用]** `Engine:` value — determines game programmer agents
- **[通用产品]** `Language:` and `Framework:` values — determines product specialists
- Naming conventions
- Performance budgets
- Forbidden patterns

For product stories, map the `Language:` field to the closest available specialist:

| Language / stack hint | Specialist agent |
|---|---|
| Python, Django, Flask, FastAPI | `python-specialist` |
| TypeScript, JavaScript, Node, React, Vue | `typescript-specialist` |
| Rust, Cargo | `rust-specialist` |
| Go, Gin, Echo, Cobra | `go-specialist` |
| Unknown or mixed stack | `lead-programmer` |

---

## Phase 3: Route to the Right Programmer

Based on the story's **Layer**, **Type**, and **system name**, determine which
specialist to spawn via Task.

**[通用产品] Product routing** (when story type is API, CLI, Data/Migration, Auth/Permission, Workflow, UI, Integration, Ops/Deployment, or Config):
| Story Type | Agent(s) |
|---|---|
| API | `lead-programmer` + mapped language specialist |
| CLI | mapped language specialist |
| Data/Migration | mapped language specialist + `performance-analyst` |
| Auth/Permission | `security-engineer` + mapped language specialist |
| Workflow | `lead-programmer` + mapped language specialist |
| UI | `ui-programmer` + `ux-designer` |
| Integration | `lead-programmer` + `devops-engineer` |
| Ops/Deployment | `devops-engineer` |
| Config | mapped language specialist |

If the story matches a product type above, use this table and skip the game
primary routing table and game engine specialist step. Product routing examples:
- **API**: implement endpoint, request/response validation, and contract test.
- **Data/Migration**: implement schema or migration script plus fresh-instance
  migration test.
- **CLI**: implement command behavior plus smoke evidence for `--help` and the
  core command path.

**[游戏专用] Game routing** (when story type is Logic, Integration, Visual/Feel, UI, or Config/Data):

**Config/Data stories — skip agent spawning entirely:**
If the story's Type is `Config/Data`, no programmer agent or engine specialist is needed. Jump directly to Phase 4 (Config/Data note). The implementation is a data file edit — no routing table evaluation, no engine specialist.

### Primary agent routing table

| Story context | Primary agent |
|---|---|
| Foundation layer — any type | `engine-programmer` |
| Any layer — Type: UI | `ui-programmer` |
| Any layer — Type: Visual/Feel | `gameplay-programmer` (implements) |
| Core or Feature — gameplay mechanics | `gameplay-programmer` |
| Core or Feature — AI behaviour, pathfinding | `ai-programmer` |
| Core or Feature — networking, replication | `network-programmer` |
| Config/Data — no code | No agent needed (see Phase 4 Config note) |

### Game engine specialist — spawn as secondary for game code stories

Read the `Engine Specialists` section of `standards/technical-preferences.md`
to get the configured primary specialist. Spawn them alongside the primary agent
when the story involves engine-specific APIs, patterns, or the ADR has HIGH
engine risk.

| Engine | Specialist agents available |
|--------|----------------------------|
| Godot 4 | `godot-specialist`, `godot-gdscript-specialist`, `godot-shader-specialist` |
| Unity | `unity-specialist`, `unity-ui-specialist`, `unity-shader-specialist` |
| Unreal Engine | `unreal-specialist`, `ue-gas-specialist`, `ue-blueprint-specialist`, `ue-umg-specialist`, `ue-replication-specialist` |

**When engine risk is HIGH** (from the ADR or VERSION.md): always spawn the engine
specialist, even for non-engine-facing stories. High risk means the ADR records
assumptions about post-cutoff engine APIs that need expert verification.

---

## Phase 4: Implement

Spawn the chosen programmer agent(s) via Task with the full context package:

Provide the agent with:
1. The complete story file content
2. The current CDD requirement text (from TR registry)
3. Exact Accepted ADR Decision + Guidelines (verbatim), or justified CDD/local
   disposition/owner/evidence; original authority, input identities and blocked dependencies
4. The control manifest rules for this layer
5. The technology naming conventions and performance budgets:
   - Game: engine, signal/event names, frame and memory budgets
   - Product: language, framework, runtime, database, API/CLI naming conventions, latency or throughput budgets
6. Exact technology notes/risk/verification sources selected by disposition:
   - Covered Game: actual ADR Engine Compatibility
   - Covered Product: actual ADR Technology Compatibility or Stack Compatibility
   - Cdd-layer/no-adr: substantive CDD/local owner and configured VERSION/stack
     references, ADR-only fields N/A with reason; unknown required risk stays Blocked
7. The required test, smoke, or evidence path from the story's Test Evidence section
8. Explicit instruction: **implement this story and produce the required evidence**

Agents inherit original named paths/effects/limits and exact input identities.
Reuse covered authority without per-role questions; delegation never expands scope.
New significant trust/public-contract/durable-format/state-ownership/governing
choices stop affected implementation and route `/architecture-decision` immediately.
Resume only with exact Accepted scope or valid exception; independent work continues.

The agent should:
- Create or modify files in `src/` following the ADR guidelines
- Respect all Required and Forbidden patterns from the control manifest
- Stay within the story's Out of Scope boundaries (do not touch unrelated files)
- Write clean, doc-commented public APIs

### Config/Data stories (no agent needed)

For Type: Config/Data stories, no programmer agent is required. The implementation
is editing a data file. Read the story's acceptance criteria and make the specified
changes to the data file directly. Note which values were changed and what they
changed from/to.

### Visual/Feel stories

Spawn `gameplay-programmer` to implement the code/animation calls. Note that
Visual/Feel acceptance criteria cannot be auto-verified — the "does it feel right?"
check happens in `/story-done` via manual confirmation.

---

## Phase 5: Write the Test

For story types with blocking automated evidence, the test must be written as
part of this implementation — not deferred to later.

- Game: Logic / Integration
- Product: API / Data/Migration / Auth/Permission / Workflow / Integration

Remind the programmer agent:

> "The required evidence for this story is at: `[path from Test Evidence section]`.
> The story cannot be closed via `/story-done` without it. Write the test
> or evidence alongside the implementation, not after."

Test requirements (from coding-standards.md):
- **[游戏专用]** File name: `[system]_[feature]_test.[ext]` (example:
  `combat_damage_test.gd`)
- **[通用产品]** File name: `test_[module]_[feature].py`,
  `[feature].test.ts`, `[feature]_test.rs`, or `[feature]_test.go` (example:
  `test_invoice_approval.py`)
- Function names: `test_[scenario]_[expected_outcome]`
- Each acceptance criterion must have at least one test function covering it
- No random seeds, no time-dependent assertions, no external I/O
- Test formula bounds, state transitions, schema constraints, API contracts, or
  permission boundaries from the CDD section that owns the story.

The Game Visual/Feel and UI instructions below plan future manual evidence.
The reminder identifies that obligation; it neither executes the observations nor
satisfies `/story-done`. Do not infer a pre-existing manual sign-off for Logic or
Config/Data work merely from the Game domain.

For **Visual/Feel** and game **UI** stories: no automated test is required unless
the story's Test Evidence section names one. Remind the agent to note what manual
evidence will be needed:
"Game playtest/sign-off evidence required at `production/qa/evidence/[slug]-evidence.md`."

For **Config/Data**, product **CLI**, product **Ops/Deployment**, and product
**Config** stories: create or update the smoke/evidence artifact named by the
story's Test Evidence section when the implementation changes behavior.

---

## Phase 6: Collect and Summarise

After the programmer agent(s) complete, collect:

- Files created or modified (with paths)
- Test, smoke, or evidence artifact created (path and number of tests/checks written)
- Any deviations from the story's Out of Scope boundary (flag these)
- Any questions or blockers the agent surfaced
- Any technology-specific risks the specialist flagged

Present a concise implementation summary:

```
## Implementation Complete: [Story Title]

**Files changed**:
- `src/[path]` — created / modified ([brief description])
- `tests/[path]` — test file ([N] test functions)

**Acceptance criteria covered**:
- [x] [criterion] — implemented in [file:function]
- [x] [criterion] — covered by test [test_name]
- [ ] [criterion] — DEFERRED: requires playtest, user test, deployment smoke, or manual evidence

**Deviations from scope**: [None] or [list files touched outside story boundary]
**Technology risks flagged**: [None] or [specialist finding]
**Blockers**: [None] or [describe]

Ready for: `/code-review [file1] [file2]` then `/story-done [story-path]`
```

---

## Phase 7: Update Session State

Append to `production/session-state/active.md` only within its existing named
path/append authority; otherwise show the proposed extract without writing:

```
## Session Extract — /dev-story [date]
- Story: [story-path] — [story title]
- Files changed: [comma-separated list]
- Evidence written: [test/smoke/evidence path, or "None — manual evidence deferred"]
- Blockers: [None, or description]
- Next: /code-review [files] then /story-done [story-path]
```

Create `active.md` only when creation is authorized; confirm actual writes only.
Implementation summaries do not mark Stories Done/Complete, publish evidence,
update indexes or advance phases. Code review and Story closure remain separate
owning workflows/effects.

---

## Error Recovery Protocol

If any spawned agent (via Task) returns BLOCKED, errors, or cannot complete:

1. **Surface immediately**: Report "[AgentName]: BLOCKED — [reason]" to the user before continuing to dependent phases
2. **Assess dependencies**: Check whether the blocked agent's output is required by subsequent phases. If yes, do not proceed past that dependency point without user input.
3. **Offer options** via AskUserQuestion with choices:
   - Skip this agent and note the gap in the final report
   - Retry with narrower scope
   - Stop here and resolve the blocker first
4. **Always produce a partial report** — output whatever was completed. Never discard work because one agent blocked.

Common blockers:
- Input file missing (story not found, CDD absent) → redirect to the skill that creates it
- ADR status is Proposed → do not implement; run `/architecture-decision` first
- Scope too large → split into two stories via `/create-stories`
- Conflicting instructions between ADR and story → surface the conflict, do not guess
- Manifest identity mismatch/LegacyRecheck → inspect exact current rules/dependencies;
  old rules need recoverable bytes and an explicit valid scoped exception

## Collaborative Protocol

- **Delegated write scope** — agents inherit exact authorization. Ask "May I write
  to [path]?" only for uncovered effects after a concrete draft; no repeated per-role
  permission. Preserve the documented direct Config/Data route within the same scope.
- **Load before implementing** — do not start coding until all context is loaded
  (story, TR-ID, ADR, manifest, technology preferences). Incomplete context produces code
  that drifts from design.
- **Governing decisions** — follow exact Accepted guidance or CDD-owned contracts.
  Surface conflicts immediately before affected implementation continues; final
  summaries do not substitute for resolving material choices.
- **Stay in scope** — the Out of Scope section is a contract. If implementing
  the story requires touching an out-of-scope file, stop and surface it:
  "Implementing [criterion] requires modifying [file], which is out of scope.
  Shall I proceed or create a separate story?"
- **Required evidence is not optional** — do not mark implementation complete
  without the story type's required test, smoke, or evidence artifact
- **Unexecuted manual criteria stay NotRun/Pending** — required ACs prevent Story closure until actual `/story-done` verification. Implementation/planning summaries do not establish QA PASS.
- **Material choices before affected implementation** — classify uncovered
  patterns, present concrete options and route significant adr-required/conflict
  through `/architecture-decision`. A casual proceed/write approval is not Accepted
  scope; resolve acceptance or a valid governance exception before continuing.

---

## Recommended Next Steps

- Run `/code-review [file1] [file2]` to review the implementation before closing the story
- Run `/story-done [story-path]` to verify acceptance criteria and mark the story complete
- After exact eligible closures: consider `/team-qa sprint`, actual strict obligations and `/gate-check` for phase readiness

## Exact-byte check availability

Use available read-only tools to collect complete raw-file SHA-256/byte size without
normalizing line endings. If exact bytes/digest or a required dependency cannot be
read, report the affected check incomplete; do not substitute a date, text rendering,
short hash or file existence. Analysis invokes no write entrypoint.
