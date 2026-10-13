---
name: story-readiness
description: "Validate that a story file is implementation-ready. Checks for embedded CDD requirements, ADR references, technology notes, clear acceptance criteria, and no open design questions. Produces READY / NEEDS WORK / BLOCKED verdict with specific gaps."
argument-hint: "[story-file-path or 'all' or 'sprint']"
user-invocable: true
allowed-tools: Read, Glob, Grep, AskUserQuestion, Task
model: haiku
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

- When to use: Validate that a story file is implementation-ready. Checks for embedded CDD requirements, ADR references, technology notes, clear acceptance criteria, and no open design questions. Produces READY / NEEDS WORK / BLOCKED verdict with specific gaps.
- Inputs: Command arguments: `/story-readiness [story-file-path or 'all' or 'sprint']`; project artifacts referenced below; user decisions and approvals before writes.
- Outputs: Primary artifacts, reports, or conversation guidance described below; write files only after user approval.
- Memory-bank writes: None.
- Next steps: Follow the workflow hand-off or next-step guidance below; recommendations do not auto-run and require explicit user command/approval.

# Story Readiness

This skill validates that a story file contains everything a developer needs
to begin implementation — no mid-sprint design interruptions, no guessing,
no ambiguous acceptance criteria. Run it before assigning a story.

**This skill is read-only.** It never edits story files. It reports findings
and asks whether the user wants help filling gaps.

**Output:** Verdict per story (READY / NEEDS WORK / BLOCKED) with a specific
gap list for each non-ready story.

---

## Phase 0: Resolve Review Mode

Resolve the review mode once and store it for all gate spawns this run:
1. If `--review` was passed, require an explicit value of `full`, `lean` or `solo`.
2. Else read the actual `production/review-mode.txt` if present and require its
   value to be `full`, `lean` or `solo`.
3. Only when neither override nor global file is present, default to `lean`.

A missing/invalid explicit value or invalid selected global value requires correction
before gate dispatch. Report the actual source/value error; never silently fall back,
claim a skipped/completed gate, or infer approval from invalid mode input.
A valid explicit override takes precedence over the global file. Resolve only once.
See `standards/director-gates.md` for the full check pattern and mode definitions.

---

## 1. Parse Arguments

**Scope:** `$ARGUMENTS[0]` (blank = ask user via AskUserQuestion)

- **Specific path** (e.g., `/story-readiness production/epics/combat/story-001-basic-attack.md`):
  validate that single story file.
- **`sprint`**: read the current sprint plan from `production/sprints/` (most
  recent file), extract every story path it references, validate each one.
- **`all`**: glob `production/epics/**/*.md`, exclude `EPIC.md` index files,
  validate every story file found.
- **No argument**: ask the user which scope to validate.

If no argument is given, use `AskUserQuestion`:
- "What would you like to validate?"
  - Options: "A specific story file", "All stories in the current sprint",
    "All stories in production/epics/", "Stories for a specific epic"

Report the scope before proceeding: "Validating [N] story files."

---

## 2. Load Supporting Context

Before checking any stories, load reference documents once (not per-story):

- `design/cdd/module-index.md` — to know which systems have approved CDDs
- `docs/architecture/control-manifest.md` — to know which manifest rules exist
  (if the file does not exist, note it as missing once; do not re-flag per story)
  Read complete raw bytes/full SHA-256/byte size and retain the readable date
  separately. Missing required manifest means incomplete affected checks, not PASS.
- `docs/architecture/tr-registry.yaml` — index all entries by `id`. Used to
  validate exact current CDD requirements/active IDs. Missing required registry
  means incomplete affected checks, not assumed legacy success. Report owning repair/
  registration; do not fabricate IDs or provenance.
- All ADR status fields — for each unique ADR referenced across the stories being
  checked, read the ADR file and note its `Status:` field. Cache these so you
  don't re-read the same ADR for every story.
- The current sprint file (if scope is `sprint`) — to identify Must Have /
  Should Have priority for escalation decisions

---

## 3. Story Readiness Checklist

For each story file, evaluate every item below. A story is READY only if all
items pass or are explicitly marked N/A with a stated reason.

### Design Completeness

- [ ] **CDD requirement referenced**: The story includes a `design/cdd/` path
  and quotes or links a specific requirement, acceptance criterion, or rule from
  that CDD — not just the CDD filename. A link to the document without tracing
  to a specific requirement does not pass.
- [ ] **Requirement is self-contained**: The acceptance criteria in the story
  are understandable without opening the CDD. A developer should not need to
  read a separate document to understand what DONE means.
- [ ] **Acceptance criteria are testable**: Each criterion is a specific,
  observable condition — not "implement X" or "the system works correctly".
  Bad example: "Implement the jump mechanic." Game example: "Jump reaches
  max height of 5 units within 0.3 seconds when jump is held." Product example:
  "POST /invoices returns 201 with invoice_id and persists the invoice row."
- [ ] **No acceptance criteria require judgment calls**: Criteria like
  "feels responsive" or "looks good" are not testable without a defined
  benchmark. These must be replaced with specific observable conditions or
  **[游戏专用]** playtest protocols / **[通用产品]** user-test protocols.

### Architecture Completeness

- [ ] **Decision disposition justified**: classify actual planned choices under
  all six dispositions. No ADR link/N/A text alone is insufficient; read CDD/Notes/
  evidence. Valid CDD/local reason passes only ADR-specific checks, never the others.
- [ ] **Required governing decision Accepted**: verify retained original/revision,
  full SHA-256/size, acceptance authority/time and exact choice/scope. Required
  Proposed/missing/unevidenced acceptance, adr-required/conflict is BLOCKED unless a
  valid existing-governance scoped exception is evidenced; retain status/findings.
- [ ] **TR-ID valid and active**: verify current registry/CDD relation. Deprecated/
  superseded/unknown ID is NEEDS WORK; missing required registry or unassigned
  requirement keeps affected readiness incomplete/Blocked. No absent-field auto-pass.
- [ ] **Manifest identity current**: compare `Manifest SHA-256` (full 64 hex),
  `Manifest Bytes` and original path against complete current raw bytes. Same-date
  changes are stale too. Mismatch is NEEDS WORK pending current rules/decision/
  dependency recheck; material new constraints stay Blocked before implementation.
  Missing required bytes block affected checks. Date-only/absent hash is
  `LegacyRecheck`, not PASS: inspect rules/dependencies and recommend an authorized
  Story identity update. Do not invent old hashes or edit files in this skill.
  Old-rules exceptions require recoverable exact old bytes and explicit authority.
- [ ] **Technology notes present**: For any post-cutoff engine API (game) or
  stack/framework API (product) this story is likely to touch, implementation
  notes or a verification requirement are included. If the story clearly does
  not touch technology APIs (e.g., it is a
  pure data/config change), "N/A — no technology API involved" is acceptable.
- [ ] **Control manifest rules noted**: bind relevant layer rules to current bytes,
  or evidence governing-workflow scoped N/A. "Not yet created" is incomplete,
  not automatic success.

### Scope Clarity

- [ ] **Estimate present**: The story includes a size estimate (hours,
  points, or a t-shirt size). A story with no estimate cannot be planned.
- [ ] **In-scope / Out-of-scope boundary stated**: The story states what
  it does NOT include, either in an explicit Out of Scope section or in
  language that makes the boundary unambiguous. Without this, scope creep
  during implementation is likely.
- [ ] **Story dependencies listed**: If this story depends on other stories
  being DONE first, those story IDs are listed. If there are no dependencies,
  "None" is explicitly stated (not just omitted).

### Open Questions

- [ ] **No unresolved design questions**: The story does not contain text
  flagged as "UNRESOLVED", "TBD", "TODO", "?", or equivalent markers in
  any acceptance criterion, implementation note, or rule statement.
- [ ] **Dependency stories are not in DRAFT**: For each story listed as a
  dependency, check if the file exists and does not have a DRAFT status. A
  story that depends on a DRAFT or missing story is BLOCKED, not just
  NEEDS WORK.

### Asset References Check

- [ ] **Referenced assets exist**: Scan the story text for asset path patterns
  (paths containing `assets/`, or file extensions `.png`, `.jpg`, `.svg`,
  `.wav`, `.ogg`, `.mp3`, `.glb`, `.gltf`, `.tres`, `.tscn`, `.res`).
  - For each asset path found: use Glob to check whether the file exists.
  - If any referenced asset does not exist: **NEEDS WORK** — note the missing
    path(s). (The story references assets that have not been created yet.
    Either remove the reference, create a placeholder, or mark it as an
    explicit dependency on an asset creation story.)
  - If all referenced assets exist: note "Referenced assets verified:
    [count] found."
  - If no asset paths are referenced in the story: note "No asset references
    found in story — skipping asset check." This item auto-passes.
  - This is an existence-only check. Do not validate file format or content.

### Definition of Done

- [ ] **At least 3 testable acceptance criteria**: Fewer than 3 suggests
  the story is either trivially small (should it be a story?) or under-specified.
- [ ] **Performance budget noted if applicable**: If this story touches a
  latency-sensitive path, rendering loop, physics/gameplay loop, API endpoint,
  data migration, background job, or high-volume workflow, a performance budget
  or a "no performance impact expected — [reason]" note is present.
- [ ] **Story Type declared**: The story includes a `Type:` field in its header.
  **[游戏专用]** Game types: Logic / Integration / Visual/Feel / UI / Config/Data.
  **[通用产品]** Product types: API / CLI / Data/Migration / Auth/Permission / Workflow / UI / Integration / Ops/Deployment / Config.
  Without this, test evidence requirements cannot be enforced at story close.
  Fix: Add `Type: [domain-appropriate type]` to the story header.
- [ ] **Test evidence requirement is clear**: If the Story Type is set, the story
  includes a `## Test Evidence` section stating where evidence will be stored
  (for example: unit/integration/API contract test path, migration test path,
  command smoke evidence, deployment smoke report, or manual evidence doc).
  Fix: Add `## Test Evidence` with the expected evidence location for the story's type.

  Expected evidence by domain:
  - Game Logic / Integration: unit or integration test path
  - Game Visual/Feel / UI / Config/Data: evidence doc, interaction test, or smoke report
  - Product API / Data/Migration / Auth/Permission / Workflow / Integration: contract, migration, permission, or integration test path
  - Product CLI / UI / Ops/Deployment / Config: command evidence, walkthrough, deployment smoke, or config validation evidence

---

## 4. Verdict Assignment

Assign one of three verdicts per story:

**READY** — All checklist items pass or have explicit N/A justifications.
The story can be assigned immediately.

**NEEDS WORK** — One or more checklist items fail, but all dependency stories
exist and are not DRAFT. The story can be fixed before assignment.

**BLOCKED** — One or more dependency stories are missing or in DRAFT state,
OR required decision acceptance/manifest/TR inputs are incomplete, unresolved
adr-required/conflict affects the Story, or a critical UNRESOLVED question has no owner. The story cannot be assigned until the blocker is resolved. Note:
a story that is BLOCKED may also have NEEDS WORK items — list both.

---

## 5. Output Format

### Single story output

```
## Story Readiness: [story title]
File: [path]
Verdict: [READY / NEEDS WORK / BLOCKED]

### Passing Checks (N/[total])
[list passing items briefly]

### Gaps
- [Checklist item]: [exact description of what is missing or wrong]
  Fix: [specific text needed to resolve this gap]

### Blockers (if BLOCKED)
- [What is blocking]: [story ID or design question that must resolve first]
```

### Multiple story aggregate output

```
## Story Readiness Summary — [scope] — [date]

Ready:      [N] stories
Needs Work: [N] stories
Blocked:    [N] stories

### Ready Stories
- [story title] ([path])

### Needs Work
- [story title]: [primary gap — one line]
- [story title]: [primary gap — one line]

### Blocked Stories
- [story title]: Blocked by [story ID / design question]

---
[Full detail for each non-ready story follows, using the single-story format]
```

### Sprint escalation

If the scope is `sprint` and any Must Have stories are NEEDS WORK or BLOCKED,
add a prominent warning at the top of the output:

```
WARNING: [N] Must Have stories are not implementation-ready.
[List them with their primary gap or blocker.]
Resolve these before the sprint begins or replan with `/sprint-plan update`.
```

---

## 6. Collaborative Protocol

This skill is read-only. It never proposes edits or asks to write files.

After reporting findings, offer:

"Would you like help filling in the gaps for any of these stories? I can
draft the missing sections for your approval."

If the user says yes for a specific story, draft only the missing sections
in conversation. Do not use Write or Edit tools — the user (or
`/create-stories`) handles writing.

**Redirect rules:**
- If a story file does not exist at all: "This story file is missing entirely.
  Run `/create-epics [layer]` then `/create-stories [epic-slug]` to generate stories from the CDD and ADR."
- If a story has no CDD reference and the work appears small: "This story has
  no CDD reference. If the change is small (under ~4 hours), run
  `/quick-design [description]` to create a Quick Design Spec, then reference
  that spec in the story."
- If a story's scope has grown beyond its original sizing: "This story appears
  to have expanded in scope. Consider splitting it or escalating to the producer
  before implementation begins."

---

## 7. Next-Story Handoff

After completing a single-story readiness check (not `all` or `sprint` scope):

1. Read the current sprint file from `production/sprints/` (most recent).
2. Find stories that are:
   - Status: READY or NOT STARTED
   - Not the story just checked
   - Not blocked by incomplete dependencies
   - In the Must Have or Should Have tier

If any are found, surface up to 3:

```
### Other Ready Stories in This Sprint

1. [Story name] — [1-line description] — Est: [X hrs]
2. [Story name] — [1-line description] — Est: [X hrs]

Run `/story-readiness [path]` to validate before starting.
```

If no sprint file exists or no other ready stories are found, skip this section silently.

---

## Phase 8: Director Gate — Story Readiness Review

Apply the review mode resolved in Phase 0 before spawning QL-STORY-READY:

- `solo` → skip. Note: "QL-STORY-READY skipped — Solo mode." Proceed to close.
- `lean` → skip. Note: "QL-STORY-READY skipped — Lean mode." Proceed to close.
- `full` → spawn as normal.

Spawn `qa-lead` via Task using gate **QL-STORY-READY** (`standards/director-gates.md`).

Pass the following context:
- Story title
- Acceptance criteria list (all items from the story's acceptance criteria section)
- Dependency status (all dependencies listed and their current state: exist / DRAFT / missing)
- Overall verdict (READY / NEEDS WORK / BLOCKED) from Phase 4

Handle the verdict per standard rules in `director-gates.md`:
- **ADEQUATE** → QA assessment passes; preserve overall readiness and remaining prerequisites. Proceed to the read-only report.
- **GAPS [list]** → surface the specific gaps to the user via `AskUserQuestion`:
  options: `Update story with suggested gaps` / `Accept and proceed anyway` / `Discuss further`.
- **INADEQUATE** → surface the specific gaps; ask user whether to update the story or proceed anyway.

---

## Recommended Next Steps

- Run `/dev-story [story-path]` to begin implementation once the story is READY
- Run `/story-readiness sprint` to check all stories in the current sprint at once
- Run `/create-stories [epic-slug]` if a story file is missing entirely

## Exact-byte check availability

Use available read-only tools to collect complete raw-file SHA-256/byte size without
normalizing line endings. If exact bytes/digest or a required dependency cannot be
read, report the affected check incomplete; do not substitute a date, text rendering,
short hash or file existence. Analysis invokes no write entrypoint.
