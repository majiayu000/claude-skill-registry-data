---
name: ux-design
description: "Guided, section-by-section UX spec authoring for a screen, flow, or HUD. Supports both game projects (player journey, HUD, game screens) and product projects (user flows, CLI interaction, API consumer journey). Reads concept doc and relevant CDDs for context-aware design guidance."
argument-hint: "[screen/flow name] or 'hud' or 'patterns'"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Edit, AskUserQuestion, Task
agent: ux-designer
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

- When to use: Guided, section-by-section UX spec authoring for a screen, flow, or HUD. Supports both game projects (player journey, HUD, game screens) and product projects (user flows, CLI interaction, API consumer journey). Reads concept doc and relevant CDDs for context-aware design guidance.
- Inputs: Command arguments: `/ux-design [screen/flow name] or 'hud' or 'patterns`; project artifacts referenced below; user decisions and approvals before writes.
- Outputs: Primary artifacts, reports, or conversation guidance described below; write files only after user approval.
- Memory-bank writes: None.
- Next steps: Follow the workflow hand-off or next-step guidance below; recommendations do not auto-run and require explicit user command/approval.

When this skill is invoked:

**Domain detection.**

Read `standards/technical-preferences.md`, existing scoped domain decisions,
and the substantive bodies of any `design/cdd/game-concept.md` and
`design/cdd/product-concept.md` before selecting a branch. Filenames, placeholder
or copied concept text and shared extensions do not establish a domain. Read
actual configured values in `Product Stack` or the populated legacy
`Language & Framework`, `Platform & Deployment`, and `Agent Routing` /
`File Extension Routing`
sections in their owning domain context; missing new sections or a concept do
not erase configured legacy Product facts. A placeholder Game concept does not
override a configured Product.

Resolve Game from consistent substantive Game concept/decision or actual
configured engine/domain and Game behavior evidence; resolve Product from
consistent substantive Product concept/decision or actual Product configuration.
Two substantive concepts, conflicting concept/configuration values or mixed scope
leave the affected branch **Unknown** until a scoped decision resolves the conflict.
With no consistent substantive concept/scoped decision or sufficient actual
configuration evidence, the domain is also Unknown; a valid concept alone can
establish the domain before stack configuration.
Record the supporting sections and values. For Unknown, use an existing matching
scoped decision or clarify with the user/configured project lead before
domain-specific delegation or writes; resolved configured facts need no new vote.
Independent neutral reads may continue. Domain selection does not waive required
branch inputs: read their actual originals and leave missing inputs Incomplete.
Never silently default to Game.

Use **[游戏专用]** Game modes only for resolved Game; use **[通用产品]**
Product modes only for resolved Product.

## 1. Parse Arguments & Determine Mode

**[游戏专用]** Game modes:

| Argument | Mode | Output file |
|----------|------|-------------|
| `hud` | HUD design | `design/ux/hud.md` |
| `patterns` | Interaction pattern library | `design/ux/interaction-patterns.md` |
| Any other value | UX spec for a screen or flow | `design/ux/[argument].md` |
| No argument | Ask the user | (see below) |

**[通用产品]** Product modes:

| Argument | Mode | Output file |
|----------|------|-------------|
| `patterns` | Interaction pattern library | `design/ux/interaction-patterns.md` |
| `workflow` or flow name | UX spec for a user workflow | `design/ux/[argument].md` |
| `cli` | CLI interaction design | `design/ux/cli-interaction.md` |
| `api` | API consumer journey | `design/ux/api-consumer-journey.md` |
| Any other value | UX spec for a screen or flow | `design/ux/[argument].md` |
| No argument | Ask the user | (see below) |

**If no argument is provided**, do not fail — ask instead. Use `AskUserQuestion`:
- **[游戏专用]** "What are we designing today?"
  Options: "A specific screen or flow", "The game HUD", "The interaction pattern library", "I'm not sure"
- **[通用产品]** "What are we designing today?"
  Options: "A specific screen or user flow", "CLI interaction design", "API consumer journey", "The interaction pattern library", "I'm not sure"

If the user selects a screen or flow name, normalize it to kebab-case
for the filename (e.g., "Main Menu" becomes `main-menu`).

---

## 2. Gather Context (Read Phase)

Read all relevant context **before** asking the user anything. The skill's value
comes from arriving informed.

### 2a: Required Reads

**[通用场景]** Read the concept document for the detected domain:
- **[游戏专用]** Read `design/cdd/game-concept.md` — if missing, warn and continue
- **[通用产品]** Read `design/cdd/product-concept.md` — if missing, warn and continue

### 2b: User Journey

**[游戏专用]** Read `design/player-journey.md` if it exists. Extract:
- Which journey phase(s) does this screen appear in?
- What is the player's emotional state on arrival?
- What player need is this screen serving?
- What critical moments does this screen deliver?

**[通用产品]** Read the User Journey section of the product concept doc. Extract:
- Which workflow step(s) does this screen/flow belong to?
- What is the user's goal at this point?
- What user need is this screen/flow serving?
- What is the primary JTBD (Job to Be Done) at this interaction point?

If no journey information exists, note the gap and proceed with assumptions.

### 2c: CDD UI Requirements

Glob `design/cdd/*.md` and grep for `UI Requirements` sections. Read any CDD whose
UI Requirements section references this screen by name or category.

These CDD UI Requirements are the **requirements input** to this spec. Collect them
as a list of constraints the spec must satisfy.

If designing the HUD, read ALL CDD UI Requirements sections — the HUD aggregates
requirements from every system.

### 2d: Existing UX Specs

Glob `design/ux/*.md` and note which screens already have specs. For screens that
will link to or from the current screen, read their navigation/flow sections to
find the entry and exit points this spec must match.

### 2e: Interaction Pattern Library

If `design/ux/interaction-patterns.md` exists, read the pattern catalog index
(the list of pattern names and their one-line descriptions). Do not read full
pattern details — just the catalog. This tells you which patterns already exist
so you can reference them rather than reinvent them.

### 2f: Visual / Product Style References

For game projects, check for `design/art/art-bible.md`. If found, read the
visual direction section. UX layout must align with the aesthetic commitments
already made.

For product projects, check for `design/brand/style-guide.md`. If found, read
brand tone, visual standards, docs imagery rules, and accessibility-constrained
color/typography commitments. For UI-heavy products, also check
`design/design-system.md`; if it exists, read component patterns and state
standards before writing screen or workflow specs.

### 2g: Accessibility Requirements

Check for `design/accessibility-requirements.md`. If found, read it. The spec
must satisfy the accessibility tier committed to there.

### 2h: Input Method (from Project Config)

**[Product]** Read actual surface and input constraints from the owning CDD,
API/CLI contract, existing surface profile where applicable, and populated
Product/legacy configuration. CLI argument/stdin/stdout interaction and API
request/response workflows do not require Game input, gamepad or safe-zone
fields. For actual web/native UI, retain its configured keyboard, pointer, touch
and accessibility constraints. Unresolved applicable input constraints need
clarification; do not use unconfigured Game fields to ask a Product what this
game targets. Continue with 2i after recording the Product constraints.

**[Game]** Read `standards/technical-preferences.md` and extract the `## Input & Platform`
section. Store these values for use throughout the skill — they drive the
Interaction Map and inform accessibility requirements:

- **Input Methods** — e.g., Keyboard/Mouse, Gamepad, Touch, Mixed
- **Primary Input** — the dominant input for this game
- **Gamepad Support** — Full / Partial / None
- **Touch Support** — Full / Partial / None
- **Target Platforms** — for safe zone and aspect ratio decisions

If the section is unconfigured (`[TO BE CONFIGURED]`), ask once:
> "Input methods aren't configured yet. What does this game target?"
> Options: "Keyboard/Mouse only", "Gamepad only", "Both (PC + Console)", "Touch (mobile)", "All of the above"
>
> (Run `/setup-engine` to save this permanently so you won't be asked again.)

Store the answer for the rest of this session. Do **not** ask again per section
or per screen.

### 2i: Present Context Summary

Before any design work, present a brief summary to the user:

> **Designing: [Screen/Flow Name]**
> - Mode: [UX Spec / HUD Design / Pattern Library / CLI / API]
> - Journey phase(s) / Workflow step(s): [from concept doc or journey map, or "unknown — no journey map"]
> - CDD requirements feeding this spec: [count and names, or "none found"]
> - Related screens/flows already specced: [list, or "none yet"]
> - Known patterns available: [count, or "no pattern library yet"]
> - Accessibility tier: [from requirements doc, or "not yet defined"]
> - Input methods: [from technical-preferences.md, or "asked above"]

Then ask: "Anything else I should read before we start, or shall we proceed?"

---

## 2b. Retrofit Mode Detection

Before creating a skeleton, check if the target output file already exists.

Use the exact output path resolved in Phase 1, which already includes its
directory and `.md` extension. Read that path directly to distinguish an existing
spec, confirmed absence and an inaccessible file. Do not prepend another directory
or append another extension; unresolved or inaccessible targets remain Incomplete.

**If the file exists — retrofit mode:**
- Read the file in full
- For each expected section, check whether the body has real content (more than a `[To be designed]` placeholder) or is empty/placeholder
- Present a section status summary to the user:

> "Found existing UX spec at [the exact output path resolved in Phase 1]. Here's the retained content:
>
> | Section | Status |
> |---------|--------|
> | Overview & Context | [Complete / Empty / Placeholder] |
> | Purpose & User Need | ... |
> | User Context & Journey Integration | ... |
> | Screen Layout & Information Architecture | ... |
> | Interaction Model | ... |
> | Feedback & State Communication | ... |
> | Accessibility | ... |
> | Edge Cases & Error States | ... |
> | Open Questions | ... |
>
> I'll fill the named incomplete sections or revise explicitly selected
> substantive sections; other existing content and examples will be preserved."

- Skip Section 3 (skeleton creation) — the file already exists
- In Phase 4, work on named Empty/Placeholder sections or substantive sections
  explicitly selected in the authorized retrofit/synchronization scope
- Use `Edit` to fill placeholders in-place rather than creating a new skeleton

**If the file does not exist — fresh authoring mode:**
Proceed to Phase 3 (Create File Skeleton) as normal.

---

## 3. Create File Skeleton

After mode detection, read only the matching skeleton in [UX document skeletons](references/templates.md): screen/flow spec, HUD design, or interaction-pattern library. Create a skeleton for a new file only with exact path/effect authority. Existing
scope persists. The referenced skeleton's automatic session-state wording is
subject to the separate authorized effect below.

## 4. Section-by-Section Authoring

Walk through each section in order. For **each section**, follow this cycle:

```
Context  ->  Questions  ->  Options  ->  Decision  ->  Draft  ->  Approval  ->  Write
```

1. **Context**: State what this section needs to contain and surface any relevant
   constraints from context gathered in Phase 2.
2. **Questions**: Ask what is needed to draft this section. Use `AskUserQuestion`
   for constrained choices, conversational text for open-ended exploration.
3. **Options**: Where design choices exist, present 2-4 approaches with pros/cons.
   Explain reasoning in conversation, then use `AskUserQuestion` to capture the decision.
4. **Decision**: User picks an approach or provides custom direction.
5. **Draft**: Write the section content in conversation for review. Flag provisional
   assumptions explicitly.
6. **Approval**: Reuse the approved document/retrofit/batch scope; ask "Does
   this capture it?" for unresolved layout choices, uncovered writes or explicit
   section-by-section preferences, without repeating settled authority.
7. **Write**: Use `Edit` to replace the `[To be designed]` placeholder with approved
   content. Confirm the write.

After each section, record progress in conversation. Update
`production/session-state/active.md` only if its path/effect is authorized.

---

### Mode-Specific Section Guidance

Before authoring a section, read the matching mode and section in [UX section guidance](references/section-guidance.md). Load only the current mode. Its product/game content, accessibility and specialist-delegation rules apply.
Section approval/order means resolved content choices; continuing user scope
controls covered writes. Preserve Game wireframes/HUD examples and existing bodies.

## 5. Cross-Reference Check

Before marking the spec as ready for review, run these checks:

**1. CDD requirement coverage**: Does every CDD UI Requirement that references
this screen have a corresponding element in this spec? Present any gaps.

**2. Pattern library alignment**: Are all interaction patterns used in this spec
referenced by name? If a new pattern was invented during this spec session, flag
it for addition to the pattern library:
> "This spec uses [pattern name], which isn't in the pattern library yet.
> Want to add it now, or flag it as a gap?"

**3. Navigation consistency**: Do the entry/exit points in this spec match the
navigation map in any related specs? Flag mismatches.

**4. Accessibility coverage**: Does the spec address the accessibility tier
committed to in `design/accessibility-requirements.md`? If not, flag open questions.

**5. Empty states**: Does every data-dependent element have an empty state defined?
Flag any that don't.

Present the check results:
> **Cross-Reference Check: [Screen Name]**
> - CDD requirements: [N of M covered / all covered]
> - New patterns to add to library: [list or "none"]
> - Navigation mismatches: [list or "none"]
> - Accessibility gaps: [list or "none"]
> - Missing empty states: [list or "none"]

---

## 6. Handoff

After the scoped authoring changes are written and read back, with actual
incomplete roles/required dependencies stated:

### 6a: Update Session State

Only with separately scoped authority, update `production/session-state/active.md` with:
- Task: [screen-name] UX spec
- Status: Complete (or In Review)
- File: [the exact output path resolved in Phase 1]
- Sections: [actual substantive sections complete / missing required content]
- Next: [suggestion]

### 6b: Suggest Next Step

Before presenting options, state clearly:

> "This spec should be validated with `/ux-review` before it enters the
> implementation pipeline. The Pre-Production gate requires all key screen specs
> to have a review verdict."

Then use `AskUserQuestion`:
- "Run `/ux-review [the exact output path resolved in Phase 1]` now, or do something else first?"
  - Options:
    - "Run `/ux-review` now — validate this spec"
    - "Design another screen first, then review all specs together"
    - "Update the interaction pattern library with new patterns from this spec"
    - "Stop here for this session"

If the user picks "Design another screen first", add a note: "Reminder: run
`/ux-review` on all completed specs before running `/gate-check pre-production`."

### 6c: Cross-Link Related Specs

When other UX specs link to or from this screen, note which ones should reference
this spec. Edit only actual named paths/effects covered by the existing changeset;
otherwise show the proposed links and obtain authority, or just name them.

---

## 7. Recovery & Resume

If the session is interrupted (compaction, crash, new session):

1. If `production/session-state/active.md` exists and belongs to this task, Read
   it for the recorded screen and progress. Otherwise recover the actual screen,
   output path and scoped approvals from the existing conversation and user decisions.
   If the target is still ambiguous, clarify it before dependent work. Recovery does
   not authorize creating or repairing session state.
2. Read the exact output path resolved in Phase 1. Retain substantive sections;
   placeholders and unresolved required content still need work. Content presence
   alone does not establish approval or completion; keep unresolved approvals pending.
3. Resume within the existing scope from the next incomplete section, preserving
   approved content and separate review/status authority.

This is why incremental writing matters: every approved section survives any
disruption.

---

## 8. Specialist Agent Routing

This skill uses `ux-designer` as the primary agent (set in frontmatter). For
specific sub-topics, additional context or coordination may be needed:

| Topic | Coordinate with |
|-------|----------------|
| Visual aesthetics, color, layout feel | `art-director` — UX spec defines zones; art defines how they look |
| Implementation feasibility (engine constraints) | `ui-programmer` — before finalizing component inventory |
| Gameplay data requirements | `game-designer` — when data ownership is unclear |
| Narrative/lore visible in the UI | `narrative-director` — for flavor text, item names, lore panels |
| Accessibility tier decisions | Handled by this session — owned by ux-designer |

When delegating to another agent via the Task tool:
- Provide: screen name, game concept summary, the specific question needing expert input
- The agent returns analysis to this session
- This session presents the agent's output to the user
- The user decides; this session writes to file
- Agents do NOT write to files directly — this session owns all file writes

---

## Collaborative Protocol

This skill follows the collaborative design principle at every step:

1. **Question -> Options -> Decision -> Draft -> Approval** for unresolved choices;
   approved document/batch scope persists for covered sections
2. **AskUserQuestion** at every decision point (Explain -> Capture pattern):
   - Phase 2: "Ready to start, or need more context?"
   - Phase 3: "May I create the skeleton?"
   - Phase 4 (each section): design questions, approach options, draft approval
   - Phase 5: "Run cross-reference check? What's next?"
3. **"May I write to [filepath]?"** for effects outside existing authority
4. **Incremental writing**: Each section is written to file immediately after approval
5. **Session state updates**: Only if its exact path/effect is authorized

**Aesthetic deference**: When layout or visual choices come down to personal taste,
present the options and ask. Do not select a layout because it is "standard" — always
confirm. The user is the creative director.

**Conflict surfacing**: When a CDD requirement and the available screen real estate
conflict, surface the conflict and present resolution options. Never silently drop
a requirement. Never silently expand the layout without flagging it.

**Never** auto-generate the full spec and present it as a fait accompli.
**Never** write outside user-approved scope.
**Never** contradict an existing approved UX spec without flagging the conflict.
**Always** show where decisions come from (CDD requirements, player journey, user choices).

Reread the exact resulting spec and required CDD/journey/pattern/accessibility
closure before handoff. Verify substantive requirement coverage and preserved
Target, not headings/placeholders. Required missing rules block only their
affected sections; continue independent authoring. Verdict: **COMPLETE** means
the scoped drafting/writes closed, not independent /ux-review or implementation
readiness. Report incomplete sections, exact evidence and pending review separately.

---

## Recommended Next Steps

- Run `/ux-review [the exact output path resolved in Phase 1]` to validate this spec before it enters the implementation pipeline
- Run `/ux-design [next-screen]` to continue designing remaining screens or flows
- Run `/gate-check pre-production` once all key screens have approved UX specs
