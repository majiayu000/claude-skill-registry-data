---
name: plan-management
version: 1.1.0
author: Ashay Kubal @ Qball Inc.
description: "Use when creating a new development plan from a topic or brief, importing an existing plan YAML, checking plan status, identifying blockers, or getting next-step recommendations."
user-invocable: false
allowed-tools: Read, Write, Bash, Glob, Grep
---

> **CLI Usage:** When unsure about a CLI's interface or flags, run it with `--help` first. Do NOT attempt to discover functionality by reading plugin source code — doing so leads to incorrect execution from assumptions made without context of the holistic flow.

# Plan Management Skill

This skill manages the full plan lifecycle: importing an existing plan YAML (Track A) or
intelligently creating a new plan from scratch via a three-agent pipeline (Track B). It also handles
ongoing plan operations: status queries, blocker detection, progress updates, and milestone management.

## Plugin Root Resolution

CLI commands in this skill reference `$CLEAR_PLUGIN_ROOT` — a `.claude/settings.json` env var the shell expands. The SessionStart hook persists it, but settings env vars load at session **launch**, so on a brand-new consumer's **first session** (before its next restart) the variable is empty and `node "$CLEAR_PLUGIN_ROOT/build/..."` fails with `MODULE_NOT_FOUND`.

**First-session bootstrap** — if `$CLEAR_PLUGIN_ROOT` is empty, set it inline in the *same* Bash call as the CLI (each Bash call is a fresh shell, so a separate `export` would not carry over):

```bash
export CLEAR_PLUGIN_ROOT="${CLEAR_PLUGIN_ROOT:-${CLAUDE_PLUGIN_ROOT}}"
```

Prepend it to the CLI in one shell line: `export CLEAR_PLUGIN_ROOT="${CLEAR_PLUGIN_ROOT:-${CLAUDE_PLUGIN_ROOT}}"; <node "$CLEAR_PLUGIN_ROOT/build/..." command>`. `${CLAUDE_PLUGIN_ROOT}` resolves in this SKILL.md body to the actually-loaded plugin path; once the consumer restarts, `$CLEAR_PLUGIN_ROOT` is populated and the assignment is a harmless no-op. Reference files are left unchanged.

## When to Use

| Trigger Pattern | Track | Action |
|-----------------|-------|--------|
| User provides a path to a `.yaml` file with `phases[]`/`workpackages[]`, or a directory containing `plan_v*.md` | A | Import via plan-import.sh |
| User provides a topic, brief, package.json description, or says "create a plan for..." | B | Three-agent creation pipeline |
| User says "what should I work on next?" or "recommend next steps" | — | Read `.clear/plans/` + analyze |
| User says "check for blockers" or "what's blocking progress" | — | Invoke plan-blockers.sh |
| User says "update plan progress" or "recalculate progress" | — | Invoke plan-progress.sh |
| User asks to read or view the current plan | — | Read `.clear/plans/master-plan.yaml` |

## DO NOT Use For

- Questions about plan history or reading raw plan documents without any action intent — just read the file directly.
- Workpackage lifecycle operations (starting, completing, updating a workpackage) — use the `workpackage-management` skill instead.

## Dependencies

- Scripts: `scripts/plan/plan-import.sh`, `scripts/plan/plan-progress.sh`, `scripts/plan/plan-blockers.sh`
- Sub-agents (Track B only, located in plugin root `agents/`):
  - `plan-management-requirements-analyst`
  - `plan-management-architect`
  - `plan-management-detail-engineer`

---

## Mandatory Execution Checklist (BINDING)

**Every item below is mandatory. No deviations. No substitutions. No skipping.**

This skill uses a multi-stage pipeline with two tracks. You are the orchestrator. Follow every item in order.

**User Interaction Protocol (BINDING):** Sub-agents run in their own context window and cannot present options to the user directly. When you read a sub-agent's output and encounter questions, options, or decisions directed at the user, you MUST present these to the user via the `AskUserQuestion` tool — never as plain text output. Relay the user's response back to the next sub-agent stage as context.

- [ ] **Stage 0 — Input Assessment**: Input parsed (path, topic, or bare invocation)
- [ ] **Stage 0 — Input Assessment**: Input classified as Track A (existing plan YAML) or Track B (create from scratch)
- [ ] **Stage 1A — Track A Import**: (if Track A) plan-import.sh invoked via Bash
- [ ] **Stage 1A — Track A Import**: (if Track A) Results reported to user
- [ ] **Stage 1B — Track B Pre-Flight**: (if Track B) Output directory created at `$PROJECT_DIR/logs/plan-creation/{slug}/`
- [ ] **Stage 2B — Requirements**: (if Track B) Requirements Analyst sub-agent spawned, output read from `01-requirements.md`
- [ ] **Stage 3B — Architecture**: (if Track B) Architect sub-agent spawned with requirements path, output read from `02-architect.md`
- [ ] **Stage 4B — Detail**: (if Track B) Detail Engineer sub-agent spawned with architect output path, output read from `03-detail-engineer.md`
- [ ] **Stage 5B — Synthesis**: (if Track B) All 3 outputs synthesized into final plan YAML structure
- [ ] **Stage 5B — Approval**: (if Track B) Plan presented to user via AskUserQuestion
- [ ] **Stage 5B — Write**: (if Track B) Approved YAML piped through `plan-write-cli.js` (NOT direct Write on `.clear/`)
- [ ] **Stage 5B — Workpackages**: (if Track B) User prompted for WP YAML creation; if yes, pipe JSON to `create-cli.js --from-stdin` per WP

---

## Command Reference

Plan CLIs at `$CLEAR_PLUGIN_ROOT/build/infrastructure/plan/cli/`. Scripts at `$CLEAR_PLUGIN_ROOT/scripts/plan/`.

| Action | Command |
|--------|---------|
| Create new plan scaffold | `create-cli --cwd=. --name="..."` |
| Import existing plan YAML | `import-cli --plan-path=<path> [--force] [--skip-workpackages]` |
| Write plan YAML to disk | `echo "<yaml>" \| plan-write-cli --cwd=. [--backup]` |
| Add new phase to existing plan | `phase-cli --cwd=. --name="..." [--after=<phase-id>]` |
| Set active phase (manual override) | `update-cli --active-phase=<phase-id>` |
| Mark milestone complete (manual override) | `update-cli --milestone=<id> --status=complete --session-number=<n>` |
| Rollup progress from WPs | `update-cli --rollup --cwd=.` |
| Add changelog entry | `update-cli --changelog --changelog-type=<type> --session-number=<n>` |
| Recommend next workpackage | `next-cli --clear-dir=./.clear` |
| Check blockers | `blockers-cli --clear-dir=./.clear [--phase=<phase-id>]` |
| Check progress | `progress-cli --clear-dir=./.clear` |
| Create WP from plan | `echo '<json>' \| wp/create-cli --from-stdin --phase=<id>` |

---

## Usage

```
/plan-management [path-to-plan-yaml | topic | brief]
/plan-management                            # bare invocation: status + next steps
/plan-management plans/my-plan.yaml         # Track A: import existing plan YAML
/plan-management "build a REST API"         # Track B: create plan from topic
```

---

## Pipeline Notation

```fsharp
// plan-management dispatch
InputAssessment(args)
|> (if ExistingPlan then TrackA_Import else TrackB_Create)

// Track A
TrackA_Import(plan_path)
|> ReportResults()

// Track B
TrackB_PreFlight(topic)
|> RequirementsAnalyst(topic, codebase)
|> Architect(requirements)
|> DetailEngineer(architecture)
|> Synthesize(all_outputs)
|> ApprovalGate(plan)
|> WritePlan(approved_plan)
|> OfferWorkpackageCreation(plan)
```

---

## Stage 0: Input Assessment

Parse the invocation argument:

| Input Form | Classification |
|------------|---------------|
| Path ending in `.yaml` or `.yml` that exists on disk | Track A |
| Path to a directory containing `plan_v*.md` | Track A |
| YAML content with top-level `phases:` or `workpackages:` keys | Track A |
| Free-form text, topic, project name, or no argument | Track B |
| Bare invocation with no args | Existing plan operations (see Stage 6) |

If classification is ambiguous, ask the user: "Is this a path to an existing plan YAML, or should I create a new plan from this description?"

---

## Stage 1A: Track A — Existing Plan Import

MUST be executed when input is classified as Track A. `plan-import.sh` reads JSON from stdin (not positional args):

```bash
echo '{
  "cwd": ".",
  "plan_path": "<plan_path>",
  "force": "false",
  "session_id": "'"$CLAUDE_SESSION_ID"'",
  "session_number": "'"$CLEAR_SESSION_NUMBER"'"
}' | bash "${CLEAR_PLUGIN_ROOT}/scripts/plan/plan-import.sh"
```

- Capture stdout and stderr.
- On success: parse the JSON envelope; report imported phases, workpackage count, and output location to the user.
- On failure: display the full error output verbatim. Do not attempt manual transformation.

---

## Stage 1B–5B: Track B — Intelligent Plan Creation

### Pre-Flight (Stage 1B)

1. Derive a slug from the topic: lowercase, spaces to hyphens, max 40 characters.
   Example: "build a REST API" → `build-a-rest-api`
2. Create the output directory:
   ```bash
   mkdir -p "$PROJECT_DIR/logs/plan-creation/${slug}"
   ```

### Requirements Analyst (Stage 2B)

Spawn the Requirements Analyst sub-agent.

Spawn via: `Task(subagent_type="plan-management-requirements-analyst", prompt=...)`

Pass as context:
- The user's topic or brief (verbatim)
- The output path: `$PROJECT_DIR/logs/plan-creation/{slug}/01-requirements.md`
- The project root: `$PROJECT_DIR`

After the sub-agent completes, READ `01-requirements.md` in full before proceeding. Do not proceed to Stage 3B if the file is missing or empty.

### Architect (Stage 3B)

Spawn the Architect sub-agent.

Spawn via: `Task(subagent_type="plan-management-architect", prompt=...)`

Pass as context:
- Path to `01-requirements.md`
- The output path: `$PROJECT_DIR/logs/plan-creation/{slug}/02-architect.md`
- The project root: `$PROJECT_DIR`

After the sub-agent completes, READ `02-architect.md` in full before proceeding. Do not proceed to Stage 4B if the file is missing or empty.

### Detail Engineer (Stage 4B)

Spawn the Detail Engineer sub-agent.

Spawn via: `Task(subagent_type="plan-management-detail-engineer", prompt=...)`

Pass as context:
- Path to `02-architect.md`
- Path to `01-requirements.md` (for traceability)
- The output path: `$PROJECT_DIR/logs/plan-creation/{slug}/03-detail-engineer.md`
- The project root: `$PROJECT_DIR`

After the sub-agent completes, READ `03-detail-engineer.md` in full before proceeding.

### Synthesis (Stage 5B)

Synthesize all three sub-agent outputs into a master plan structure. The synthesis produces TWO outputs handled separately:

1. **master-plan.yaml** — phases + milestones + plan-level pointers. Written via `plan-write-cli` to `.clear/plans/master-plan.yaml`.
2. **WP JSON payloads** — one per workpackage. Piped individually to `wp/create-cli --from-stdin` to write `.clear/workpackages/wp-<systemId>.yaml`. WPs are NOT written into master-plan.yaml.

#### master-plan.yaml shape (canonical)

```yaml
version: '1.0'
projectName: "<derived from requirements>"
status: active
activePhase: phase_1                       # Top-level pointer; first phase becomes active on plan creation
activeWorkpackage: ''                      # Empty until first WP starts

phases:
  - id: phase_N                             # Display ID (auto-derived from position)
    name: "<from architect>"
    status: not_started                     # not_started | in_progress | complete
    workpackages: ["<WP display ID>", ...]  # Display IDs of WPs in this phase
    # systemId, position, progress, weights are AUTO-POPULATED by plan-write-cli + CLI ops.
    # Do NOT pre-fill them in synthesis — let the system assign canonical values.

milestones:
  - id: <M-ID>
    name: "<from architect>"
    phase: <phase_N>
    type: major | minor | gate
    requires: ["<WP display ID>", ...]      # Display IDs of WPs that must be complete
    status: not_started
```

**Fields NOT in canonical master-plan.yaml** (do not include them in synthesis output even if a sub-agent suggests them): `created`, `summary`, `description` on phases. Provenance / narrative belongs in sub-agent output files under `logs/plan-creation/{slug}/`, not in the canonical plan.

#### WP JSON payload shape (per workpackage)

Each workpackage from synthesis gets its own JSON payload piped to `wp/create-cli --from-stdin`. Schema matches `wp/create-cli --help`:

```json
{
  "phaseId": "<phase systemId — e.g. ph-12a34b56>",
  "title": "<WP title — IMPORTANT: use 'title' not 'name'. CLEAR WP YAMLs use 'title:'>",
  "afterId": "<optional — WP systemId to insert after for explicit ordering>",
  "type": "feature | spike | bug | refactor | doc",
  "priority": "low | medium | high",
  "description": "<WP description>",
  "acceptance_criteria": ["<criterion 1>", "<criterion 2>"],
  "deliverables_text": ["<artifact description 1>", "<artifact description 2>"],
  "scope_in": ["<in-scope item>"],
  "scope_out": ["<out-of-scope item>"],
  "verification": ["<command or procedure>"],
  "notes": ["<note>"]
}
```

Note: deliverables are passed as `deliverables_text` (array of plain strings). The CLI generates structured `deliverables[]` objects with `id`, `weight`, `status`, `pattern` fields server-side. Do NOT try to pre-construct the structured deliverable shape from synthesis.

### Approval Gate (Stage 5B)

Present the synthesized plan to the user:

```
Plan ready for review:

  Project: <name>
  Phases: <N>
  Workpackages: <N>
  Milestones: <N>

[Display full YAML]

Approve this plan and write to .clear/plans/master-plan.yaml? [Y/n/edit]
```

Wait for user response via AskUserQuestion. On "edit", incorporate the user's changes and re-present. On "n", stop and discard.

### Write Plan (Stage 5B)

On approval, pipe the approved YAML through `plan-write-cli.js` (do NOT use the Write tool directly on `.clear/` paths — the PreToolUse guard will block it):

```bash
echo '<approved YAML>' | node "$CLEAR_PLUGIN_ROOT/build/infrastructure/plan/cli/plan-write-cli.js" --cwd="$PROJECT_DIR"
```

The CLI validates the YAML via `parseMasterPlanContent()`, then delegates to `writeMasterPlan()` which handles directory creation, backup, and serialization.

### Offer Workpackage Creation (Stage 5B)

After writing the plan, ask:

```
Plan written. Create individual workpackage YAML files for each WP? [Y/n]
```

If yes: for each workpackage in the plan, construct a JSON payload (see "WP JSON payload shape" above for full schema) and pipe it to `create-cli.js --from-stdin`. This preserves all rich fields (acceptance_criteria, scope, deliverables) across the skill-CLI boundary.

```bash
echo '{
  "phaseId": "<phase system ID>",
  "title": "<WP title>",
  "type": "feature",
  "priority": "medium",
  "description": "<WP description>",
  "acceptance_criteria": ["<criterion 1>", "<criterion 2>"],
  "deliverables_text": ["<deliverable 1>", "<deliverable 2>"],
  "scope_in": ["<in-scope item>"],
  "scope_out": ["<out-of-scope item>"],
  "verification": ["<verification step>"],
  "notes": ["<note>"]
}' | node "$CLEAR_PLUGIN_ROOT/build/infrastructure/workpackage/cli/create-cli.js" --from-stdin --cwd="$PROJECT_DIR" --phase="<phase-id>"
```

Do NOT write WP YAML files directly — the PreToolUse guard blocks Write/Edit on `.clear/` paths. Do NOT use the Skill tool for WP creation during Stage 5B — use the CLI directly to avoid re-entering the skill system.

---

## Stage 6: Existing Plan Operations (Bare Invocation)

When invoked with no arguments, or when user asks about status, blockers, or next steps:

### Next-Step Recommendations

```bash
node "$CLEAR_PLUGIN_ROOT/build/infrastructure/plan/cli/next-cli.js" --clear-dir=./.clear
```

`next-cli` resolves dependencies, applies phase ordering, and returns a ranked recommendation in the JSON `additionalContext` field. Use this as the canonical surface; do NOT manually traverse `.clear/plans/master-plan.yaml` + `.clear/workpackages/` for ranking unless next-cli is unavailable.

**Fallback (if next-cli fails or is unavailable):**
1. Read `$PROJECT_DIR/.clear/plans/master-plan.yaml`
2. Read `$PROJECT_DIR/.clear/workpackages/` — all WP files
3. Find workpackages where all dependencies have `status: complete`
4. Prioritize: critical path (HIGH), unblocking others (MEDIUM), parallel (LOWER)
5. Present recommendations in ranked list with rationale

### Check for Blockers

```bash
node "$CLEAR_PLUGIN_ROOT/build/infrastructure/plan/cli/blockers-cli.js" --clear-dir=./.clear [--phase=<phase-id>]
```

Present: blocked WP ID, blocker type (dependency / technical / decision), severity, resolution path. Use `--phase=<id>` to scope to a specific phase.

### Update Plan Progress

```bash
node "$CLEAR_PLUGIN_ROOT/build/infrastructure/plan/cli/progress-cli.js" --clear-dir=./.clear
```

Present: overall progress %, phase breakdown, at-risk milestones.

### Add a New Phase Mid-Plan

```bash
node "$CLEAR_PLUGIN_ROOT/build/infrastructure/plan/cli/phase-cli.js" --cwd="$PROJECT_DIR" --name="<phase name>" [--after=<phase-id>]
```

- `--name=<name>` — REQUIRED. Human-readable phase name (max 80 chars).
- `--after=<phase-id>` — Optional. Display ID (e.g., `phase_3`) or system ID (e.g., `ph-12a34b56`) of the phase to insert AFTER. If omitted, the new phase appends to the end of the phase list.
- The CLI assigns a new `systemId`, reindexes display IDs for downstream phases, and writes the updated `master-plan.yaml` atomically.

### Milestone Status Update (Manual Override)

Milestones auto-complete when their `requires` WPs all hit `complete` (see Automatic State Advancement below). Use the explicit invocation only as an override — for example, to mark a milestone complete when one of its WPs was deferred but the milestone's intent has otherwise been satisfied.

```bash
# Step 1: Mark milestone complete in .clear/plans/master-plan.yaml
node "$CLEAR_PLUGIN_ROOT/build/infrastructure/plan/cli/update-cli.js" --cwd="$PROJECT_DIR" --milestone=<id> --status=complete --session-id=<session-id> --session-number=<num>
```

```bash
# Step 2: Append changelog entry to .clear/plans/change-log.yaml
node "$CLEAR_PLUGIN_ROOT/build/infrastructure/plan/cli/update-cli.js" --cwd="$PROJECT_DIR" --changelog --changelog-type=milestone_complete --changelog-milestone=<id> --session-number=<num>
```

**Do NOT use Write or Edit on `.clear/` files.** The CLI handles all `.clear/` mutations via `fs.writeFileSync`, which is invisible to the PreToolUse guard.

Parse each CLI's JSON output to confirm `"status": "success"` before proceeding.

---

## Automatic State Advancement (K0 Behavior)

Three state transitions fire automatically without explicit CLI invocation. Understanding these is critical: redundant manual updates may conflict with auto-advance and produce no-op success responses (or in rare cases, audit log churn).

### What auto-fires

| Auto-Transition | Trigger | CLI / Hook |
|-----------------|---------|------------|
| **Milestone auto-completes** | All WPs in `requires:` list hit `status: complete` | `update-cli --rollup` (or any WP `--status=complete`) |
| **activePhase auto-advances** | Current phase's required milestones all complete | Same as above (cascades through rollup) |
| **master-plan.yaml write-back** | Any of the above triggers a state change | All update-cli / lifecycle-cli mutations |

### When to use manual `update-cli --milestone=<id> --status=complete`

- The milestone's WPs do NOT all show `complete` (e.g., one was deferred), but the milestone's intent has been satisfied via alternative work.
- You need to set a milestone to a non-`complete` status (e.g., flag it `blocked`).

### When to use manual `update-cli --active-phase=<phase-id>`

- Auto-advance picked the wrong next phase (e.g., parallel phases where the system chose A but you want B active).
- You need to set activePhase to a non-canonical value during a refactor or migration.

### Risk: manual + auto overlap

If you run `update-cli --active-phase=phase_2` and then complete a WP in phase_2 that closes its final milestone, the auto-advance will fire and likely set activePhase = phase_3 (next phase), overriding your manual override. Treat manual `--active-phase` as transient — assume auto-advance will replay over it.

For audit trail purposes, manual milestone completes via `update-cli --milestone=<id> --status=complete --session-id=<id> --session-number=<n>` ARE recorded distinctly from auto-completes (the changelog `--changelog-type` field disambiguates).

---

## Plan File Locations

| File | Purpose |
|------|---------|
| `$PROJECT_DIR/.clear/plans/master-plan.yaml` | Active plan |
| `$PROJECT_DIR/.clear/plans/change-log.yaml` | Audit trail of plan changes |
| `$PROJECT_DIR/.clear/workpackages/<ID>.yaml` | Per-WP detail files |
| `$PROJECT_DIR/.clear/workpackages/registry.yaml` | WP status index |
| `$PROJECT_DIR/logs/plan-creation/{slug}/01-requirements.md` | Requirements Analyst output |
| `$PROJECT_DIR/logs/plan-creation/{slug}/02-architect.md` | Architect output |
| `$PROJECT_DIR/logs/plan-creation/{slug}/03-detail-engineer.md` | Detail Engineer output |

---

## Automatic Hook Integrations

| Script | Triggered By | What It Does |
|--------|--------------|--------------|
| `scripts/plan/plan-load.sh` | SessionStart hook | Loads active plan and phase context |
| `scripts/plan/plan-progress.sh` | UserPromptSubmit hook | Aggregates progress from workpackages |
| `scripts/plan/plan-blockers.sh` | On demand | Detects and reports blockers |
