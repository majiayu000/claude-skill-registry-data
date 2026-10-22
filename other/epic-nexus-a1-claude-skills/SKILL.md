---
name: epic
category: planning
model: claude-opus-5-5
userInvocable: true
description: Decompose large initiatives into dependency-mapped, wave-sequenced tickets with per-ticket requirements. Use when a feature is too large for a single /create-requirements run — typically 5+ tickets with complex interdependencies.
argument-hint: <epic-description>
allowed-tools: "Read, Write, Grep, Glob, Bash, Task, Workflow, AskUserQuestion"
---

# Epic Command

Break down large initiatives (epics) into sequential, implementable tickets with proper dependencies.

## Context

Current directory: !`pwd`

Git status: !`git status --short 2>/dev/null || echo "Not a git repository"`

Arguments: $ARGUMENTS

## Configuration

Read `.claude/configuration.yml` for project-specific paths. If the file doesn't exist or a key is missing, use defaults:

| Config Key | Default | Purpose |
|-----------|---------|---------|
| `storage.artifacts.work` | `location: local, subdir: work` | Work state and context |

```bash
# Source resolve-config: marketplace installs get ${CLAUDE_PLUGIN_ROOT} substituted
# inline before bash runs; legacy local copies fall back to ~/.claude. If neither
# path resolves, fail loudly rather than letting resolve_artifact be undefined.
if [ -f "${CLAUDE_PLUGIN_ROOT}/shared/resolve-config.sh" ]; then
  source "${CLAUDE_PLUGIN_ROOT}/shared/resolve-config.sh"
elif [ -f "$HOME/.claude/shared/resolve-config.sh" ]; then
  source "$HOME/.claude/shared/resolve-config.sh"
else
  echo "ERROR: resolve-config.sh not found — reinstall the nexus plugin: /plugin install nexus@claude-skills" >&2
  exit 1
fi
WORK_DIR=$(resolve_artifact work work)
echo "WORK_DIR=$WORK_DIR"
EPIC_WORKFLOW_ENABLED=$(resolve_epic_workflow_enabled)
echo "EPIC_WORKFLOW_ENABLED=$EPIC_WORKFLOW_ENABLED"
```

Use the printed `EPIC_WORKFLOW_ENABLED` value to decide whether Phase 1.5 attempts the
orchestrated path.

Use `$WORK_DIR` instead of a hardcoded `.claude/work` — but only inside this block. Each later block is its own Bash tool call and does not inherit the variable, so those substitute the value printed above instead.

Never hardcode `.claude/work/`: the configured work directory can be anywhere.

---

## Your Task

Transform a large initiative into a structured set of implementable tickets with dependencies.

---

## Phase 1: Parse Epic Description

**From $ARGUMENTS:**

If empty or insufficient:
```
Error: Epic description required.

Usage:
  /epic "Implement user authentication system"
  /epic "Add payment processing with Stripe"
  /epic "Migrate to microservices architecture"
```

Extract:
- **Epic ticket** (e.g., `EPIC-42`, `PROJ-100`) — ask via AskUserQuestion if not provided. Must match `[A-Z]+-[0-9]+`. Store as `{epic-ticket}`.
- **Epic slug** — a short, kebab-case descriptor (2–5 words) derived from the epic description. Lowercase, ASCII, `[a-z0-9-]+`. Confirm with the user before proceeding.
- **Epic identifier** `{epic-id}` = `{epic-ticket}-{slug}` (per the Work Directory Naming Convention in `CLAUDE.md`). This is the full composite identifier used throughout the rest of this skill for paths, manifest entries, and resume handles.
- Epic description (what needs to be built).

**Per-ticket naming:** each generated ticket has `{ticket-id}` = `{ticket-number}-{ticket-slug}` where `{ticket-number}` is the Jira/issue identifier the user will assign (or a placeholder like `{epic-ticket}-001` until real ticket IDs are created) and `{ticket-slug}` is a kebab-case descriptor derived from the ticket's title. The composed `{ticket-id}` is the value used in paths and references throughout this skill.

---

## Phase 1.5: Path Selection

Two paths through Phases 2-5.5. The orchestrated one makes the analysis blind, turns the
too-small gate and the wave assignment into computations over typed data, and runs the
per-ticket spec work as a **pipeline** — ticket A is verified while ticket B is still being
written. The classic one is everything from Phase 2 down and remains fully supported.

**Attempt the orchestrated path when both hold:**
- the `EPIC_WORKFLOW_ENABLED` value printed by the Configuration block is `true` (the default), and
- the `Workflow` tool is available in this session.

**If so, read `references/workflow-decompose.md` and follow it.** It replaces Phases 2, 2.5,
2.6, 3, 4, 5 and 5.5, and changes what Phase 6 receives. Pass the raw epic description,
`{epic-id}`, `{epic-ticket}`, where the description came from, and a timestamp as `args` — the
script cannot read files or shell out, so anything it needs must arrive that way.

**Fall back to the classic path below — silently, it is not an error — when:**
- the config disables it, or
- the `Workflow` tool is not available, or
- the orchestrated run fails, does not complete, or returns `status: "incomplete"`.

**On a mid-run failure, discard the partial result and run the classic path from Phase 2 in
full.** Do not merge partial orchestrated output into a classic run, and do not present a
partial run as complete. Name the path actually taken in Phase 7.

**One exception, and it matters:** `status: "too-small"` is a **completed run with a negative
answer**, not a failure. Print the "Epic too small" template from `references/error-handling.md`
verbatim and stop. Re-running the classic path after a too-small verdict would spend a second
analysis to reach the same conclusion — and might reach a different one, which turns a gate
into a coin flip.

> Detection is attempt-and-observe: nothing in the tool's contract describes how absence
> manifests, so do not write logic that depends on a specific error shape. If the orchestrated
> path does not produce a result, take the fallback.

**What never moves, on either path:** the epic-ticket and slug questions in Phase 1, every file
write, the epic structure in Phase 6, the manifest upsert in Phase 6.5, and the summary in
Phase 7. The script has no filesystem, cannot ask the user anything, and reaches no mutation.

---

## Phases 2-5.5 — the classic path

Everything from here to Phase 5.5 is the classic path. On the orchestrated path it is replaced
wholesale by `references/workflow-decompose.md`; skip to **Consuming the orchestrated result**
below, then continue at Phase 6.

---

## Phase 2: Analyze Initiative

Read `references/agent-prompts.md` for the `business-analyst` and `architect` prompt templates. Fill in `{description}` and, for architect, `{from business-analyst}`.

**Run both agents in parallel.**

---

## Phase 2.5: Too-Small Gate

**Goal**: Refuse to continue as an epic when `business-analyst`'s findings show
this is really single-ticket work — before any specialist agent is spawned.

Read the trailer directly from the `business-analyst` agent's returned text —
do not shell out or interpolate the agent's output into a Bash command. The
analyst's output is derived from user-supplied `{description}` and possibly
web/repo content; treating it as a string to paste into a command line is a
command-injection surface. Take **only the last two lines** of the output as
the trailer, matching exactly:

```
TICKET_COUNT: <int>
INDEPENDENT: yes|no
```

**If those two lines are missing, malformed, or don't appear as the final
two lines:** treat this the same as `TICKET_COUNT: 1` — fail closed, do not
default to proceeding.

**If `TICKET_COUNT` < 2, or `INDEPENDENT` is `no` (including the fail-closed
case above):** STOP. Read `references/error-handling.md` and print the
"Epic too small" template verbatim. Do not proceed to Phase 2.6 or Phase 3 —
no specialist agent is spawned for an initiative that fails this gate. The
template's "Recommendation: Use /create-requirements instead" line is the
redirect for every too-small verdict, including runs that arrived through
`/meeting`'s "route to epic", so this skill does not need to know where a run
came from.

**Otherwise:** proceed to Phase 2.6 (conditional specialist deep dive).

---

## Phase 2.6: Conditional Specialist Deep Dive

**Goal**: Based on Phase 2 findings, run specialist agents to gather deeper context for areas that will significantly impact the epic breakdown.

This phase is conditional: run only the specialists whose signals appear in the Phase 2 findings, and none at all when the initiative touches no database, external API, cloud infrastructure, or security-sensitive area.

### 2.6.1 Determine Required Specialists

Review the combined output from `business-analyst` and `architect` in Phase 2. Check for signals that warrant specialist agents:

| Signal in Phase 2 Findings | Agent | Purpose |
|----------------------------|-------|---------|
| New tables, schema modifications, migrations, entity changes | `data-modeler` | Analyze schema impacts, migration complexity, relationship constraints |
| Third-party API integrations, webhooks, external service calls | `integration-analyst` | Map API contracts, auth requirements, error handling patterns |
| New AWS/cloud resources, infrastructure changes, IaC modifications | `aws-architect` | Assess infrastructure needs, IAM requirements, cost implications |
| Authentication, authorization, PII handling, payments, compliance | `security-requirements` | Identify security constraints, compliance needs, audit requirements |

**If no signals are detected**: Skip to Phase 3 immediately.

**If one or more signals are detected**: Proceed to 2.6.2.

### 2.6.2 Run Applicable Specialist Agents in Parallel

**Execute all applicable agents in a single message with multiple Task tool calls.** Only run the agents whose Phase 2 signals matched.

Read `references/agent-prompts.md` (Phase 2.6.2: Conditional Specialist Agents section) for the full prompt templates for `data-modeler`, `integration-analyst`, `aws-architect`, and `security-requirements`. Fill in `{description}`, `{from business-analyst}`, and `{from architect}` in each applicable prompt.

### 2.6.3 Incorporate Specialist Findings

Feed specialist agent outputs into the subsequent phases:
- **Phase 3 (Decompose)**: Use specialist findings to ensure tickets properly account for DB migrations, API integration steps, infrastructure provisioning, and security hardening.
- **Phase 4 (Dependencies)**: Use specialist findings to identify cross-cutting dependency chains (e.g., infrastructure must be provisioned before services that depend on it).
- **Phase 5 (Technical Requirements)**: Include relevant specialist context in each ticket's technical details and implementation notes.

---

## Phase 3: Decompose into Tickets

Based on analysis from Phase 2 and specialist findings from Phase 2.6 (if any), break the epic into tickets:

**Ticket sizing rules:**
- Each ticket: 1-3 days of work max
- One focused change per ticket
- Should be independently testable
- Should have clear acceptance criteria

**Ticket structure:**
```
{ticket-id}: {Title}             # e.g., PROJ-101-db-schema
  Description: {What this ticket accomplishes}
  Components: {Files/areas affected}
  Dependencies: {Which other tickets must complete first}
  Estimate: Small | Medium | Large
  Type: Database | Backend | Frontend | Infrastructure | Integration
```

---

## Phase 4: Create Dependency Graph

Analyze ticket dependencies:

```
Dependency Analysis (use each ticket's `{ticket-id}`; example uses
`PROJ-1NN` placeholders):

PROJ-101-db-schema: Database schema
  Blocks: PROJ-102-entity-layer, PROJ-104-...
  Blocked by: None

PROJ-102-entity-layer: Entity layer
  Blocks: PROJ-105-..., PROJ-106-...
  Blocked by: PROJ-101-db-schema

PROJ-103-external-api-client: External API client
  Blocks: PROJ-105-...
  Blocked by: None
  (Can run in parallel with PROJ-101, PROJ-102)

...

Implementation Waves (use full {ticket-id} — same identifiers used in Blocks/Blocked-by above):
  Wave 1 (parallel): PROJ-101-db-schema, PROJ-103-external-api-client
  Wave 2: PROJ-102-entity-layer
  Wave 3: PROJ-104-..., PROJ-105-...
  Wave 4: PROJ-106-...
```

Identify opportunities for parallel work.

---

## Phase 5: Generate Per-Ticket Spec

For each ticket, create a **lightweight spec.md** — Spec-Driven Development at the ticket level. The epic-level `EPIC_PLAN.md` plays the role of shared `plan.md`; each ticket emits only its product-facing spec. The full triad (plan + tasks) materializes when `/implement` picks up the ticket and derives them from the spec + EPIC_PLAN.md context.

**Layer boundary — strict at ticket level too:** spec.md contains NO file paths, class names, or library choices. HOW lives in the parent `EPIC_PLAN.md` and per-ticket `plan.md` (derived later by `/implement`).

**Use the Task tool with `context-builder` agent** to gather context for each ticket area (used to populate the ticket's `context/` directory, not to put HOW into the spec).

For each ticket, generate:

```markdown
# {ticket-id}: {Title}             <!-- e.g., PROJ-101-db-schema -->

> **Layer: SPEC** — WHAT & WHY for this ticket. Part of epic `{epic-id}`.

## Summary
{One paragraph: what this ticket delivers and why it matters in the context of the epic.}

## User Stories
- **US-{ticket-number}.1**: As a {role}, I want {capability}, so that {outcome}.
- **US-{ticket-number}.2**: ...

## Acceptance Criteria
Stable IDs scoped to the ticket: `AC-{ticket-number}.{n}` (so two tickets in the same epic don't collide).

- **AC-{ticket-number}.1**
  - Given {precondition}
  - When {action}
  - Then {observable outcome}
- **AC-{ticket-number}.2**
  - Given ...
  - When ...
  - Then ...

## Security & Compliance Criteria
(If `security-requirements` ran in Phase 2.6, include AC-SEC-{ticket-number}.{n} entries here. Otherwise omit.)

## Scope
**In scope:**
- {specific behavior delivered by this ticket}

**Out of scope:**
- {explicit exclusions — typically deferred to other epic tickets, link by {ticket-id}}

## Dependencies
- Blocked by: {ticket-id} (must complete first)
- Blocks: {ticket-id} (others waiting on this)

## Estimate
{Small: <1 day | Medium: 1-2 days | Large: 2-3 days}

## Epic Context
- Epic: `{epic-id}` — {epic title}
- Wave: {N}
- Shared technical context: see `../EPIC_PLAN.md`
```

Save each to: `$WORK_DIR/{epic-id}/{ticket-id}/spec.md`

**Note:** No `plan.md` or `tasks.md` is generated here. `/implement` bootstraps both from this spec + parent `EPIC_PLAN.md` when the ticket is picked up.

---

## Phase 5.5: Quality Guard Review

**Goal**: Validate the ticket breakdown before saving the epic structure.

Use Task tool with `subagent_type: "quality-guard"`:

```
Prompt: Challenge this epic breakdown for '{epic_description}'.

Epic plan context (from Phase 2-4):
- Business analyst findings: {business_analyst_output}
- Architect validation: {architect_output}
- Tickets generated: {ticket_list_summary}

Review:
1. Is every ticket independently testable and deliverable? Flag any that are too broad or too vague.
2. Are the dependencies complete and correct? Are there hidden dependencies not captured?
3. Are the wave assignments valid — can Wave 1 tickets actually start in parallel?
4. Are there missing tickets (e.g., infrastructure setup, migration rollback, documentation)?
5. Is the scope appropriate — are any tickets doing too much (should be split) or too little (should be merged)?
6. Does the epic cover the full feature, or are there gaps between tickets?
7. **Spec-layer hygiene** — does each ticket's `spec.md` contain HOW-leakage (file paths, class names, library choices)? Those belong in `EPIC_PLAN.md` or in the per-ticket `plan.md` derived later by `/implement`, never in the ticket spec.
8. **AC scoping** — do AC IDs use the `AC-{ticket-number}.{n}` format so they don't collide across tickets in the same epic?
9. **AC coverage** — does every user story have at least one Given/When/Then AC? AC must be observable/testable.

Return: APPROVED / CONDITIONAL (list specific issues) / REJECTED (fundamental restructuring needed).
```

**Process the verdict:**

- **APPROVED**: Proceed to Phase 6.
- **CONDITIONAL**: Adjust the ticket breakdown based on findings before saving.
- **REJECTED**: Return to Phase 3 to re-decompose the epic.

---

## Consuming the orchestrated result

Only on the orchestrated path. You hold a validated object from
`references/workflow-decompose.md`. **Do not re-summarise it.** The decomposition, the wave
verdict and the drops already happened, mechanically, where they could not be renegotiated.
Render it; do not re-judge it.

`status` decides what happens next before anything else is read:

| `status` | What you do |
|---|---|
| `complete` | Continue below, then Phase 6 |
| `too-small` | Print the "Epic too small" template verbatim and stop. Do **not** run the classic path |
| `incomplete` | Discard the whole result and run the classic path from Phase 2 in full |

On `complete`, the mapping into Phase 6's files is direct:

- **`tickets[].specText`** is the spec, already rendered. Write it verbatim to
  `$WORK_DIR/{epic-id}/{tickets[].specPath}`. Do not re-generate it and do not edit it into
  shape — the AC ids in it are scoped to the ticket number by construction, and rewriting them
  is how the collision Phase 5.5 asks about gets reintroduced.
- **`tickets[]`** and **`waves[]`** populate `state.json` per `references/state-schema.md`.
  The mapping is exact, so do not re-derive any of it: state's `slug` is the ticket's **`id`**
  (the full `{ticket-number}-{ticket-slug}`, not the bare `slug` field beside it), `spec_file`
  is `specPath`, `title`/`type`/`estimate` map straight across, `blocked_by` is `blockedBy`,
  `blocks` is `blocks` (computed from `blockedBy`, never asserted separately — that is what
  keeps the two halves of the relation from drifting), and each wave's `tickets` list is
  `waves[].tickets`.
- **`tickets[].context`** is the codebase inventory the classic Phase 5 gathers with
  `context-builder`. Write it to `$WORK_DIR/{epic-id}/{tickets[].id}/context/context.json`. One
  agent per ticket was spent producing it; a run that writes the spec and drops this has paid
  for it and thrown it away.
- **`initiative`** and the surviving findings populate `EPIC_PLAN.md` per
  `references/epic-plan-template.md`.

Rules that are not stylistic, because each one is a way the plan can claim more than it checked:

- **A wave with `parallel: false` is reported as broken, at the top of the plan**, with its
  `violations` and the quote each one cites. That is the finding the wave check exists to
  produce; burying it in an appendix undoes the check.
- **A wave's `arithmetic` entries are reported beside its `violations`.** They come from the
  declared graph, not from an agent: `wave-too-early` means the decomposition scheduled a
  ticket before something it says blocks it, and a `cycle` entry (which carries `ticket: null`)
  means no wave assignment can be valid at all. `waveFindings` holds the same set for the whole
  epic, including the `wave-late` notes — a ticket that could start earlier than it was placed.
- **A wave with `parallel: true` and `verified: false` is labelled `[UNCHECKED]`, never
  "parallel".** Either the panel was short or a lens that answered skipped this wave — 
  `noVerdictFrom` names which. Nobody contradicted the wave, and nobody confirmed it either;
  those are different claims. `checkedBy` is per wave, so report it per wave.
- **`waves[].lensVerdicts` is the record of what each lens actually said about that wave.**
  Show it beside the verdict when a wave is contested or unverified; it is the difference
  between "three lenses agreed" and "one answered and two were quiet".
- **When any `panelIntegrity.*.complete` is false, say so at the top**, with the
  received/dispatched counts and the missing names. A missing specialist means that area is
  **uncovered**, not clean; a missing architect means the decomposition is **not
  architecture-validated**, and it must not be described as if it were.
- **Every `unresolved` entry is listed, with its ticket and its reason.** A ticket dropped at
  the cap got no spec at all; a ticket at the revision cap has a spec that still fails its own
  checks. Neither is a finished ticket and neither may be presented as one.
- **`droppedViolations`, `droppedDependencies`, each ticket's `droppedFindings`, and each
  ticket's non-blocking `findings` go in their own section**, with reasons. A finding that
  vanishes silently is indistinguishable from one never found — which is why the script returns
  what it dropped rather than only logging it.
- **`gaps` are listed as open questions for the user**, not silently turned into extra tickets.
  Adding a ticket nobody asked for is a decision, and decisions are the user's.
- **Every `danglingEdges` entry is listed beside the ticket it belongs to.** Those edges are
  real — the decomposition declared them — but the ticket they name got no spec, so it has no
  directory and `/implement {epic-id}/{that-id}` resolves to nothing. Do not delete the edge to
  tidy the graph; say which ids in `state.json` have no ticket behind them.
- **A wave's `unsupportedDoubts` are reported beside it even when it is `parallel: true`.** A
  lens answered "these cannot start together" and could not show why. It does not move the
  verdict — an uncited doubt is not evidence — and it does not disappear either.
- **`strayLensVerdicts` go in the dropped section** with the rest. A lens answered for a wave
  the epic does not have, or answered one twice; the first answer per lens per wave stands and
  the remainder is reported rather than binned.
- **Name the path in Phase 7** — `orchestrated` or `classic (fallback: {reason})` — and, on the
  orchestrated path, print `caps.ticketsProposed` beside `caps.ticketsSpecced` so a capped run
  is visible without reading `unresolved`.

The `Agents Used` block in Phase 7 comes from `specialistsRun` and `specialistsSkipped`, so a
specialist that was skipped and one that died are shown differently.

---

## Phase 6: Create Epic Structure

Create directory structure:

```bash
# A wrong or missing substitution must fail here, not write next to `/`.
[ -n "<WORK_DIR printed above>" ] && [ -d "<WORK_DIR printed above>" ] || exit 1
mkdir -p <WORK_DIR printed above>/{epic-id}
```

For each ticket:
```bash
# A wrong or missing substitution must fail here, not write next to `/`.
[ -n "<WORK_DIR printed above>" ] && [ -d "<WORK_DIR printed above>" ] || exit 1
mkdir -p <WORK_DIR printed above>/{epic-id}/{ticket-id}
```

Save files:
1. `$WORK_DIR/{epic-id}/EPIC_PLAN.md` - Shared technical plan (epic-level HOW context for all tickets)
2. `$WORK_DIR/{epic-id}/state.json` - Epic tracking
3. `$WORK_DIR/{epic-id}/{ticket-id}/spec.md` - Each ticket's product spec (WHAT/WHY only)
4. `$WORK_DIR/{epic-id}/{ticket-id}/context/context.json` - The ticket's codebase context inventory (orchestrated path: `tickets[].context`; classic path: the `context-builder` output from Phase 5)

Register active session for the optional `auto-context.sh` PostToolUse hook (no-op when neither `CLAUDE_SESSION_ID` nor `CLAUDE_CODE_SESSION_ID` is set):

```bash
# A wrong or missing substitution must fail here, not write next to `/`.
[ -n "<WORK_DIR printed above>" ] && [ -d "<WORK_DIR printed above>" ] || exit 1
SID="${CLAUDE_SESSION_ID:-${CLAUDE_CODE_SESSION_ID:-}}"
if [ -n "$SID" ] && command -v jq >/dev/null 2>&1; then
  mkdir -p "<WORK_DIR printed above>"
  touch "<WORK_DIR printed above>/.active-sessions.lock"
  (
    flock -x -w 2 200 || exit 0
    [ -s "<WORK_DIR printed above>/.active-sessions" ] || echo '{}' > "<WORK_DIR printed above>/.active-sessions"
    jq --arg s "$SID" --arg w "{epic-id}" \
       '. + {($s): $w}' "<WORK_DIR printed above>/.active-sessions" \
       > "<WORK_DIR printed above>/.active-sessions.tmp.$$" \
       && mv "<WORK_DIR printed above>/.active-sessions.tmp.$$" "<WORK_DIR printed above>/.active-sessions" \
       || rm -f "<WORK_DIR printed above>/.active-sessions.tmp.$$"
  ) 200>"<WORK_DIR printed above>/.active-sessions.lock"
fi
```

---

## Epic Plan Template

Read `references/epic-plan-template.md` for the full `EPIC_PLAN.md` markdown template (overview, business context, tickets, implementation waves, progress tracking).

---

## Epic State Schema

Read `references/state-schema.md` for the complete `state.json` schema (schema_version, tickets, waves, progress).

---

## Phase 6.5: Update Work Manifest

After saving all epic files, upsert into `${WORK_DIR}/manifest.json` (see `${CLAUDE_PLUGIN_ROOT}/shared/manifest-schema.md` for the envelope/upsert contract).

Read or initialize manifest, then upsert item using `identifier` (the full `{epic-id}`) as unique key:

```json
{
  "identifier": "{epic-id}",
  "title": "{Epic Title}",
  "type": "epic",
  "status": "in_progress",
  "created_at": "{ISO_TIMESTAMP}",
  "updated_at": "{ISO_TIMESTAMP}",
  "current_phase": "planning",
  "progress": "0/{total_tickets} tickets",
  "branch": null,
  "tags": [],
  "path": "{epic-id}/"
}
```

Update `last_updated` and `total_items` in the envelope.

---

## Phase 7: Present Epic Plan

Show the user a clear summary:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Epic Created: {epic-id}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{Epic Title}

{Brief description}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Breakdown: {N} tickets
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Wave 1 (Start first):
  ✓ {ticket-id}: {Title} [{Type}, {Estimate}]
  ✓ {ticket-id}: {Title} [{Type}, {Estimate}] (parallel)

Wave 2 (After Wave 1):
  → {ticket-id}: {Title} [{Type}, {Estimate}]
  → {ticket-id}: {Title} [{Type}, {Estimate}]

Wave 3 (After Wave 2):
  → {ticket-id}: {Title} [{Type}, {Estimate}]

...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Agents Used
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  ✓ business-analyst (initiative analysis)
  ✓ architect (technical feasibility)
  {✓ data-modeler - if used}
  {✓ integration-analyst - if used}      [PARALLEL]
  {✓ aws-architect - if used}
  {✓ security-requirements - if used}
  ✓ context-builder (ticket context)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Files Created
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

$WORK_DIR/{epic-id}/
├── EPIC_PLAN.md                # Shared HOW context for all tickets
├── state.json
├── {ticket-id}/                # e.g., PROJ-101-db-schema/
│   ├── spec.md                 # Product spec (WHAT/WHY) — plan.md + tasks.md derived by /implement
│   └── context/context.json    # Codebase context inventory
├── {ticket-id}/                # e.g., PROJ-102-entity-layer/
│   ├── spec.md
│   └── context/context.json
└── ...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Next Steps
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Review the epic plan:
   cat $WORK_DIR/{epic-id}/EPIC_PLAN.md

2. Start implementing first ticket:
   /implement {epic-id}/{ticket-id}   # e.g., /implement PROJ-100-user-auth-system/PROJ-101-db-schema

3. Track progress:
   /resume-work {epic-id}

4. View ticket details:
   cat $WORK_DIR/{epic-id}/{ticket-id}/spec.md
```

```bash
# A wrong or missing substitution must fail here, not write next to `/`.
[ -n "<WORK_DIR printed above>" ] && [ -d "<WORK_DIR printed above>" ] || exit 1
# Clear auto-context sentinel on completion
SID="${CLAUDE_SESSION_ID:-${CLAUDE_CODE_SESSION_ID:-}}"
if [ -n "$SID" ] \
   && [ -f "<WORK_DIR printed above>/.active-sessions" ] \
   && command -v jq >/dev/null 2>&1; then
  (
    flock -x -w 2 200 || exit 0
    jq --arg s "$SID" 'del(.[$s])' "<WORK_DIR printed above>/.active-sessions" \
       > "<WORK_DIR printed above>/.active-sessions.tmp.$$" \
       && mv "<WORK_DIR printed above>/.active-sessions.tmp.$$" "<WORK_DIR printed above>/.active-sessions" \
       || rm -f "<WORK_DIR printed above>/.active-sessions.tmp.$$"
  ) 200>"<WORK_DIR printed above>/.active-sessions.lock"
fi
```

---

## Error Handling

Read `references/error-handling.md` for error-scenario message templates (no description provided, epic too small, epic already exists).

---

## Important Notes

- **Epic identifiers** follow `{epic-ticket}-{slug}` (e.g., "PROJ-100-user-auth-system") — see Work Directory Naming Convention in `CLAUDE.md`
- **Ticket identifiers** follow `{ticket-number}-{slug}` (e.g., "PROJ-101-db-schema") or use placeholders like `{epic-ticket}-001` until real ticket IDs are assigned
- Each ticket should be **independently testable**
- Tickets are **sized appropriately** (1-3 days max)
- **Dependencies are explicit** - clear what blocks what
- **Parallel opportunities** are identified
- Epic state is **trackable** across sessions via `/resume-work`

## Integration with Existing Workflow

After epic creation:
- Each ticket can be implemented with `/implement {epic-id}/{ticket-id}` (e.g., `/implement PROJ-100-user-auth-system/PROJ-101-db-schema`) — the nested path is required: tickets live at `$WORK_DIR/{epic-id}/{ticket-id}/`, not `$WORK_DIR/{ticket-id}/`, and have no per-ticket `state.json` of their own (see `/implement` §0.2's epic-ticket carve-out)
- Progress tracked in `state.json`
- `/resume-work {epic-id}` shows epic status and suggests next ticket (e.g., `/resume-work PROJ-100-user-auth-system`)
- After all tickets complete, epic status becomes "completed"
