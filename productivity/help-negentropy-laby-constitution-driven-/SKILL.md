---
name: help
description: "Analyzes what is done and the users query and offers advice on what to do next. Use if user says what should I do next or what do I do now or I'm stuck or I don't know what to do"
argument-hint: "[optional: what you just finished, e.g. 'finished design-review' or 'stuck on ADRs']"
user-invocable: true
allowed-tools: Read, Glob, Grep
context: |
  !echo "=== Live Project State ===" && echo "Stage: $(cat production/stage.txt 2>/dev/null | tr -d '[:space:]' || echo 'not set')" && echo "Latest sprint: $(ls -t production/sprints/*.md 2>/dev/null | head -1 || echo 'none')" && echo "Session state: $(head -5 production/session-state/active.md 2>/dev/null || echo 'none')"
model: haiku
---
Read and apply `docs/COLLABORATIVE-DESIGN-PRINCIPLE.md`,
`standards/evidence-lifecycle.md` and `standards/notes-adr-sync.md` for scoped
authority, exact evidence and decision ownership. Existing named authority
continues; analysis is read-only and report-only excludes input/index/state writes.


## User Guide

- When to use: Analyzes what is done and the users query and offers advice on what to do next. Use if user says what should I do next or what do I do now or I'm stuck or I don't know what to do
- Inputs: Command arguments: `/help [optional: what you just finished, e.g. 'finished design-review' or 'stuck on ADRs']`; project artifacts referenced below; user decisions and approvals before writes.
- Outputs: Primary artifacts, reports, or conversation guidance described below; write files only after user approval.
- Memory-bank writes: None — read-only; reads `memory_bank/t0_core/basic_law_index.md` when present.
- Next steps: Follow the workflow hand-off or next-step guidance below; recommendations do not auto-run and require explicit user command/approval.

# Studio Help — What Do I Do Next?

This skill is read-only — it reports findings but writes no files.

This skill figures out exactly where you are in the project development pipeline and
tells you what comes next. Works for both game and product projects. It is
**lightweight** — not a full audit. For a full gap analysis, use
`/project-stage-detect`.

---

## Step 0: Determine Task and Skill Purpose

Apply the purpose rule to skills, independent agent/role definitions, native
configuration containing instruction bodies and their exclusive references/overlays.
A Target's development-only role stays local-only even without invoking a skill;
TOML, developer_instructions fields and native loading give no exception. Real
product-use agents follow actual product rules. Independent configuration must be
independent of development instructions/role packages and carry no such body;
a native loader of developer roles is not an independent configuration consumer.

Read `standards/skill-purpose.md` and identify the governed project. First distinguish
using its delivered functions from developing it. For product-use requests, orient
from real product instructions/capabilities without requiring CDD development
artifacts. For development, continue catalog routing below; this routing skill is
a local-only Target development template, even if tailored/native. CDD Source
distribution is a separate product role. Mixed/unclear tasks need scoped separation
or clarification; independent work continues.

## Step 1: Read the Catalog

Read `workflow/workflow-catalog.yaml`. This is the authoritative list of all
phases, their steps (in order), whether each step is required or optional, and
artifact locators/structural conditions; owning workflow evidence establishes completion.

---

## Step 1b: Find Skills Not in the Catalog

Use the installed skill entrypoints for the platform actually in use; select that
platform before enumeration. The projected instruction below names its matching
directory. A local maintenance script, import profile or lock is not required.

- Glob `.claude/skills/*/SKILL.md` in the current project.
- Use bounded Read ranges to read only each entry's YAML frontmatter through its
  closing `---`. Extract actual `name:` and `description:` plus any supplied
  invocation metadata. This builds a definition list; inputs and availability
  remain unverified until the selected instructions are read.
- After Steps 2b–6 establish domain, phase and the user's task, shortlist relevant
  definitions before reading their full bodies in Step 6b.
- If both platforms are installed, use the one actually running this skill rather
  than combining their directories. If the platform is unknown, clarify the
  affected selection; do not infer it from a missing file.
- A missing installed entry or unreadable/invalid frontmatter leaves that lookup
  Incomplete or unverified. Do not invent its description, copy general Source
  skills into the project, or fetch Source merely for ordinary orientation.

Keep this skill's Read/Glob/Grep limits; no command facility is added. Installed
file observations do not prove current Source reproduction, supported execution
or completed workflow. An import/update still requires the actual designated
Source, covered project-write authority and independent review of exact update
paths and the required local-input allowlist. Review Git submission candidates
separately; neither required reads nor update-write authority grants Git eligibility.

Compare against the `command:` values in the catalog. Any skill whose actual
name is absent is an **uncataloged skill** outside the phase-gated workflow.
Report its selected platform and installed path; a definition alone does not
qualify runtime invocation.

Collect these for the output in Step 8 — show them as a footer block:

```
### Other definitions (not in workflow; state selected platform)
- `/skill-name` — [description from SKILL.md frontmatter]
- `/skill-name` — [description]
```

Only show this block if at least one uncataloged skill exists. Limit to the 10
most relevant after the domain/phase/task filtering in Step 6b. Label unread
definitions as instructions/execution unverified; recommend only selected skills
whose full instructions and required inputs have been checked.

---

## Step 2: Check for Constitution

Before determining phase, check if the project has a constitution:

1. Read substantive laws/acceptance when `memory_bank/t0_core/basic_law_index.md`
   exists; a copied template/path does not prove ratification.
2. Missing optional Memory Bank uses actual root instructions, accepted decisions
   and established artifacts. Recommend `/constitute` for requested initialization
   or unresolved governance, without blocking valid independent legacy work solely
   on optional absence.
3. Read applicable current-state and established active context when present;
   compare declarations with exact relied-on evidence.

## Step 2b: Detect Project Domain

Read concept bodies and `standards/technical-preferences.md` domain/capability
evidence, including populated legacy Product aliases. Classify the current scope
as Game, Product or Unknown from consistent actual sources. Conflicting concepts
or mixed scope need a concrete Game or Product selection before dependent advice
and catalog filtering; do not auto-select Both or qualify completion from this
choice. Missing concepts never default Game; actual configured legacy Product
remains Product. Independent neutral guidance continues.

For product projects, also check `design/ux/surface-profile.md` if present. It
records which API, CLI, SDK, UI, admin, operator, docs-driven, or headless
surfaces exist and which UX artifacts are accepted as N/A.

The domain affects which catalog steps are shown as required. Steps with an
`applies_to` field in `workflow-catalog.yaml` are filtered:
- `applies_to: [game]` → only shown for game projects
- `applies_to: [product]` → only shown for product projects
- No `applies_to` field → shown for both

## Step 3: Determine Current Phase

Check in this order:

1. **Read `production/stage.txt`** — if it exists and has content, this is the
   declared phase name, not a verified transition. Map it to a catalog phase key:
   **[游戏专用] Game phases:**
   - "Concept" → `concept`
   - "Systems Design" → `systems-design`
   - "Technical Setup" → `technical-setup`
   - "Pre-Production" → `pre-production`
   - "Production" → `production`
   - "Polish" → `polish`
   - "Release" → `release`

   **[通用产品] Product phases:**
   - "Concept" → `concept`
   - "Specification" → `systems-design`
   - "Architecture" → `technical-setup`
   - "Pre-Implementation" → `pre-production`
   - "Implementation" → `production`
   - "Verification" → `polish`
   - "Release" → `release`

2. **Advisory candidate phase** uses observed work below when needed; indicators
   locate workflow, not qualified preceding phases:
   - Actual ongoing implementation evidence → candidate `production`; file
      counts indicate scale only
   - `production/epics/**/*.md` story files exist (excluding `EPIC.md`) → `pre-production`
   - `docs/architecture/adr-*.md` exists → `technical-setup`
   - `design/cdd/module-index.md` exists → `systems-design`
   - `design/cdd/game-concept.md` or `design/cdd/product-concept.md` exists → `concept`
   - `memory_bank/t0_core/basic_law_index.md` exists → `concept` (constitution established, no domain artifacts yet)
   - Nothing → `concept` (fresh project — suggest `/constitute`)

---

## Step 4: Read Session Context

Read `production/session-state/active.md` if it exists. Extract:
- What was most recently worked on
- Any in-progress tasks or open questions
- Current epic/feature/task from STATUS block (if present)

This tells you what the user just finished or is stuck on — use it to personalize
the output.

---

## Step 5: Check Step Completion for the Current Phase

Before checking completion, filter the current phase's steps by the detected
domain:
- If domain is `game`, skip steps whose `applies_to` exists and does not include `game`
- If domain is `product`, skip steps whose `applies_to` exists and does not include `product`
- If domain is `unknown`, label `applies_to`-limited steps as applicability pending.
  Hold dependent single-domain routing/completion claims until a concrete Game or
  Product scope resolves; independent neutral guidance continues.

For each remaining step in the current phase:

### Artifact-based checks

If the step has `artifact.glob`:
- Use Glob to check if files matching the pattern exist
- If `min_count` is specified, verify at least that many files match
- If `artifact.pattern` is specified, use Grep to verify the pattern exists in the matched file
- **Observed** = locator/count/pattern condition met; read bodies/required closure.
- **Complete** = exact current required checks, decisions/reviews and completion
  authority verified under the owning workflow. Otherwise report pending/unverified;
  file/keyword/count presence is insufficient.
- **Incomplete** = required artifact/evidence missing or unsatisfied.

If the step has `artifact.note` (no glob):
- Mark as **MANUAL** — cannot auto-detect, will ask user

If the step has no `artifact` field:
- Mark as **UNKNOWN** — completion not trackable (e.g. repeatable implementation work)

### Special case: product `required_when`

When a product step has `required_when`, evaluate applicability before marking
it incomplete:
- Existing required artifacts are observed; read bodies/required evidence before
  qualifying Complete under their actual owner.
- If `design/ux/surface-profile.md` explicitly marks the artifact N/A with a
  reason, mark the step **N/A** and show the rationale.
- If the artifact is missing and there is no surface profile, mark the step
  **Incomplete** and recommend creating `design/ux/surface-profile.md` from
  `templates/surface-profile.md`.
- Never silently skip `design/ux/interaction-patterns.md` for API, CLI,
  SDK/library, UI, admin, operator, or docs-driven consumer surfaces.

### Special case: production phase — read `sprint-status.yaml`

When the current phase is `production`, check for `production/sprint-status.yaml`
before doing any glob-based story checks. If it exists, read it directly:

- Stories with `status: in-progress` → surface as "currently active"
- Stories with `status: ready-for-dev` → surface as "next up"
- Stories with `status: done` → recorded done; verify exact owning closure
  evidence before counting qualified complete
- Stories with `status: blocked` → surface as blocker with the `blocker` field

This gives precise per-story status without markdown scanning. Skip the glob
artifact check for `implement`/`story-done` locators; YAML is a status projection,
not independent closure or execution proof.

### Special case: `repeatable: true` (non-production)

For repeatable steps outside production (e.g. "System CDDs"), the artifact
check tells you whether *any* work has been done, not whether it's finished.
Label these differently — show what's been detected, then note it may be ongoing.

---

## Step 6: Find Position and Identify Next Steps

From the completion data, determine:

1. **Last confirmed complete step** — the furthest completed required step
2. **Current blocker** — the first incomplete *required* step (this is what the
   user must do next)
3. **Optional opportunities** — incomplete *optional* steps that can be done
   before or alongside the blocker
4. **Upcoming required steps** — required steps after the current blocker
   (show as "coming up" so user can plan ahead)

If the user provided an argument (e.g. "just finished design-review"), use that
to locate relevant evidence and acknowledge declared completion, not advance
qualified progress from ambiguous evidence. Identify the affected recheck.

---

## Step 6b: Read the Selected Instructions

Use the actual domain, current phase, catalog `applies_to` and step order, and the
user's task to filter the frontmatter list. Description matches identify
candidates; they do not establish applicability. Prioritize one primary next
step and a few relevant optional or uncataloged definitions. When domain is
Unknown, keep neutral guidance and mark domain-limited candidates pending.

Before recommending an actionable command, Read its complete installed
`SKILL.md` and classify its whole package, not just the current invocation. Names,
overlays or test/release labels give no Git exception. Resolve and Read references for the
applicable branch, inputs, routing and conditions, following their owning paths.
Use Glob for referenced locators as needed; optional references and future
outputs do not become required inputs merely because they are mentioned.
There is no full-body pre-read of every installed skill or every reference tree.

Apply this check to next-up, optional, coming-up, gate and escalation commands
you intend to recommend. An entry whose body is unread may only be identified
as a definition with instructions/execution unverified, never as an executable
next step. Missing required entries/originals leave the affected recommendation
Incomplete; inaccessible or unread inputs remain unverified. Unresolved domain
or scope keeps dependent advice Unknown while independent guidance continues.
File observations and complete instructions still do not qualify runtime
invocation or workflow completion.

---

## Step 7: Check for In-Progress Work

If `active.md` shows an active task or epic:
- Surface it prominently at the top: "It looks like you were working on [X]"
- Suggest continuing it or confirm if it's done

---

## Step 8: Present Output

Keep it **short and direct**. This is a quick orientation, not a report.

```
## Where You Are: [Phase Label]

**In progress:** [from active.md, if any]

### ✓ Done
- [completed step name]
- [completed step name]

### → Next up (REQUIRED)
**[Step name]** — [description]
Command: `[/command]`

### ~ Also available (OPTIONAL)
- **[Step name]** — [description] → `/command`
- **[Step name]** — [description] → `/command`

### Coming up after that
- [Next required step name] (`/command`)
- [Next required step name] (`/command`)

---
Approaching **[next phase]** gate → run `/gate-check` when ready.
```

**Formatting rules:**
- `✓` for confirmed complete
- `→` for the current required next step (only one — the first blocker)
- `~` for optional steps available now
- Show commands inline as backtick code
- If a step has no command (e.g. "Implement Stories"), explain what to do instead of showing a slash command
- For MANUAL steps, ask the user: "I can't tell if [step] is done — has it been completed?"

Verdict: **HELP COMPLETE** — guidance produced. The concise output separates
declared phase, observed work, candidate phase and verified qualification.

---

## Step 9: Gate Warning (if close)

After the current phase's steps, check if the user is likely approaching a gate:
- If all required steps in the current phase are complete (or nearly complete),
  add: "You're close to the **[Current] → [Next]** gate. Run `/gate-check` when ready."
- If multiple required steps remain, skip the gate warning — it's not relevant yet.
- If 3 or more required steps in the current phase are incomplete or missing,
  add: "For a saved roadmap, run `/cdd-status --dry-run`."

---

## Step 10: Escalation Paths

After the recommendations, if the user seems stuck or confused, add:

```
---
Need more detail?
- `/constitute` — establish or refresh governing principles (works for both game and product projects)
- `/constitute-check` — constitutional health audit
- `/project-stage-detect` — full gap analysis with all missing artifacts listed
- `/cdd-status --dry-run` — saved-roadmap preview with blockers and next commands
- `/gate-check` — formal readiness check for your next phase
```

Only show this if the user's input suggested confusion (e.g. "I don't know", "stuck",
"lost", "not sure"). Don't show it for simple "what's next?" queries.

---

## Collaborative Protocol

- **Never auto-run the next skill.** Recommend it, let the user invoke it.
- **Ask about MANUAL steps** rather than assuming complete or incomplete.
- **Match the user's tone** — if they sound stressed ("I'm totally lost"), be
  reassuring and give one action, not a list of six.
- **One primary recommendation** — the user should leave knowing exactly one thing
  to do next. Optional steps and "coming up" are secondary context.

Canonical definitions and recorded adapter state do not prove runtime availability.
Consult actual runtime metadata and `adapters/README.md` before invocation claims;
disclose unsupported/unverified execution without installing/activating anything.
Next commands follow actual catalog order and evidence; unavailable commands are
disclosed rather than invented.
