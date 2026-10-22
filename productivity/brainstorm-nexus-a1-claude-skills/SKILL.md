---
name: brainstorm
category: planning
model: claude-opus-5-5
userInvocable: true
description: Explore implementation strategies for business requirements. Interactive brainstorming that presents multiple approaches, trade-offs, and creates high-level implementation picture before committing to detailed specs.
argument-hint: "[--light] [feature-description] | promote <slug> [ticket-id]"
allowed-tools: "Read, Write, Glob, Grep, Bash(source:*), Bash(echo:*), Bash(pwd:*), Bash(touch:*), Bash(flock:*), Bash(mv:*), Bash(rm:*), Bash(git:*), Bash(mkdir:*), Bash(jq:*), Bash(yq:*), Task, AskUserQuestion"
---

# Brainstorm Implementation

Transform brief business requirements into clear implementation strategy through interactive exploration.

## Purpose

This skill sits in the **early thinking phase** - after you get business requirements but before you commit to detailed technical specs. It helps you:

1. Explore different ways to implement something
2. Understand trade-offs between approaches
3. Get a clear picture of what implementation looks like
4. Outline tickets/work items needed

**Use this when:** You have a business request and want to think through implementation options.

**Don't use this when:** You already know the approach and need detailed specs (use `/create-requirements` instead).

## Context

Current directory: !`pwd`

Git status: !`git status --short 2>/dev/null || echo "Not a git repository"`

Arguments: $ARGUMENTS

---

## Configuration

Read `.claude/configuration.yml` for project-specific paths. If the file doesn't exist or a key is missing, use defaults:

| Config Key | Default | Purpose |
|-----------|---------|---------|
| `storage.artifacts.brainstorms` | `location: local, subdir: brainstorm` | Brainstorm sessions |
| `storage.artifacts.work` | `location: local, subdir: work` | Session registry (`.active-sessions`) only |

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
BRAINSTORM_DIR=$(resolve_artifact brainstorms brainstorm)
BRAINSTORM_WORKFLOW_ENABLED=$(resolve_brainstorm_workflow_enabled)

# The cross-skill session registry (.active-sessions) is shared with /implement,
# /create-requirements and friends, so it stays under the work artifact. Only
# brainstorm *content* lives in $BRAINSTORM_DIR.
WORK_DIR=$(resolve_artifact work work)

# Back-compat: brainstorm sessions used to be written into $WORK_DIR/{slug}.
# Sessions created before that fix still live there, so lookups fall back.
# Writes go to $BRAINSTORM_ROOT (below) — which is $BRAINSTORM_DIR for a new
# session and the legacy directory for a resumed pre-migration one.
LEGACY_BRAINSTORM_DIR="$WORK_DIR"
[ "$LEGACY_BRAINSTORM_DIR" = "$BRAINSTORM_DIR" ] && LEGACY_BRAINSTORM_DIR=""

# BRAINSTORM_ROOT is the directory this run reads and writes. It defaults to the
# new artifact (correct for every new session) and is REBOUND to the legacy
# directory when Phase 0 or promote resolves a pre-migration session. Every
# per-session path below uses $BRAINSTORM_ROOT/{slug}/... — writing some files
# via $BRAINSTORM_DIR while state.json lives in the legacy directory would split
# one session across two locations.
BRAINSTORM_ROOT="$BRAINSTORM_DIR"
echo "BRAINSTORM_DIR=$BRAINSTORM_DIR"
echo "BRAINSTORM_WORKFLOW_ENABLED=$BRAINSTORM_WORKFLOW_ENABLED"
echo "WORK_DIR=$WORK_DIR"
```

Shell variables do not survive this Bash call; later steps use the printed values.
Brainstorm content lives under the printed `BRAINSTORM_DIR` (`$BRAINSTORM_ROOT` in later
fences, re-derived there), never a hardcoded `.claude/brainstorm`. The work directory is used
only for the `.active-sessions` registry and the legacy read fallback.

**Reading an existing session** (resume, promote, active-session listing): look
under `$BRAINSTORM_DIR` first, then `$LEGACY_BRAINSTORM_DIR/{slug}/state.json`
when it is set and the state has `"type": "brainstorm"`. A session found only in
the legacy location is read and updated in place; do not move it silently.

---

## Promote Subcommand

If `$ARGUMENTS` begins with `promote`, handle the promote flow instead of normal brainstorm.

**Syntax:** `/brainstorm promote {slug} [{ticket-id}]`

**Behavior:**

1. Parse `$ARGUMENTS`: extract `{slug}` (word after "promote") and optional `{ticket-id}` (next word).
2. Locate the session. Check `$BRAINSTORM_DIR/{slug}/state.json` first; if
   absent and `$LEGACY_BRAINSTORM_DIR` is set, check
   `$LEGACY_BRAINSTORM_DIR/{slug}/state.json` and require
   `"type": "brainstorm"` there (the legacy directory also holds non-brainstorm
   work sessions, so the type check is what disambiguates). Bind
   `BRAINSTORM_ROOT` to whichever matched and use it for every read and write in
   steps 3-6 — a legacy session is promoted in place, not moved.

   If neither location has it, output error and stop:
   ```
   Error: Brainstorm session not found: {slug}
   Available sessions:
   {list from both manifests, or $BRAINSTORM_DIR/ and $LEGACY_BRAINSTORM_DIR/ dirs}
   ```
3. Read `state.json`. Warn if `"status"` is already `"promoted"`:
   ```
   Warning: This brainstorm is already promoted to {promoted_to}.
   Re-promote? [y/n]
   ```
   Use AskUserQuestion. On **n**: stop.

4. If `{ticket-id}` was not provided, ask:
   ```
   AskUserQuestion: Enter the ticket number for this work (e.g., PROJ-123), or leave blank to be asked by /create-requirements:
   ```
   If blank, leave `{ticket-id}` unset — do **not** substitute `{slug}` (a brainstorm
   slug like `user-data-export` never matches create-requirements' required
   `[A-Z]+-[0-9]+` ticket format, so passing it through would only produce a
   validation failure downstream). `/create-requirements` Stage 1.1 will prompt
   for the ticket itself when none was pre-filled.

   **Check `{ticket-id}`, whether it was given or typed here.** The whole value
   must be exactly `[A-Za-z]+-[0-9]+` and be at most 32 characters — the shape
   `/create-requirements --ticket` accepts — and is stored uppercase (`proj-7` →
   `PROJ-7`). If it does not match, say so and ask again; a blank answer leaves it
   unset. Step 7 prints it after `--ticket`, where a value of another shape stops
   `/create-requirements` with an error instead of asking for the ticket.

5. **Update brainstorm state** (`$BRAINSTORM_ROOT/{slug}/state.json`):
   ```json
   {
     "status": "promoted",
     "promoted_to": "{ticket-id or null if not yet known}",
     "updated_at": "{ISO_TIMESTAMP}"
   }
   ```
   Merge these fields into the existing JSON (preserve all other fields).
   `/create-requirements` Stage 1.3b overwrites `promoted_to` with the final
   identifier once one is assigned, so a `null` here is only transient.

6. **Update manifest** (`$BRAINSTORM_ROOT/manifest.json`) — match on
   `.slug == {slug}` for a new-style manifest or `.identifier == {slug}` for a
   legacy work manifest, then set `status` to `"promoted"` and add
   `promoted_to`.

7. Announce the promotion and the command that continues it, then stop — do not
   run the brainstorm phases:
   ```
   Brainstorm '{slug}' promoted → {ticket-id}

   Run: /create-requirements --from-brainstorm {slug} --ticket {ticket-id}
   ```
   **Omit the whole `--ticket {ticket-id}` part if no ticket was provided** — never
   substitute `{slug}` in its place, and never print `--ticket` without a value.
   `/create-requirements` takes the ticket from `--ticket` and asks for one when
   there is none; it no longer picks a ticket-shaped word out of free text.
   Stage 1.3b loads the brainstorm context.

---

## Lightweight Mode

If `$ARGUMENTS` begins with `--light`, strip the flag and enable lightweight mode:

- Output to user: "Lightweight mode enabled: business-analyst runs on Sonnet; other agents are unchanged."
- **Explore agent**: unchanged
- **business-analyst**: spawn with model **sonnet** (ALWAYS Opus in standard mode — the only meaningful downgrade here)
- **Plan agent**: unchanged
- **architect**: unchanged
- All orchestration flow and output formats remain identical

This reduces cost for exploratory brainstorming where deep reasoning is less critical than in requirements or implementation.

The list above is the classic path. The orchestrated path (Phase 3.1) sets no model override, so `--light` does not change it: every agent runs on its pinned model. Say that instead of the message above when the orchestrated path runs.

---

## Workflow

### Phase 0: Check for Existing Session

Before starting, check whether an active brainstorm session already exists for this topic.

```bash
# Re-derived here: shell state does not survive between Bash tool calls.
if [ -f "${CLAUDE_PLUGIN_ROOT}/shared/resolve-config.sh" ]; then
  source "${CLAUDE_PLUGIN_ROOT}/shared/resolve-config.sh"
elif [ -f "$HOME/.claude/shared/resolve-config.sh" ]; then
  source "$HOME/.claude/shared/resolve-config.sh"
else
  echo "ERROR: resolve-config.sh not found — reinstall the nexus plugin: /plugin install nexus@claude-skills" >&2
  exit 1
fi
BRAINSTORM_DIR=$(resolve_artifact brainstorms brainstorm)
LEGACY_BRAINSTORM_DIR="<WORK_DIR printed above>"
# Brainstorms manifest: slug-keyed, no `type` field (every item is a brainstorm).
# "promoted" is terminal — the work continues under the requirements session.
if [[ -f "${BRAINSTORM_DIR}/manifest.json" ]]; then
  jq -r '.items[] | select(.status != "completed" and .status != "promoted") | "\(.slug)\t\(.title)\t\(.current_phase)\t\(.updated_at)"' "${BRAINSTORM_DIR}/manifest.json"
fi

# Legacy sessions are still indexed in the work manifest, where they DO carry
# `type` and are keyed by `identifier`.
if [[ -n "$LEGACY_BRAINSTORM_DIR" && -f "${LEGACY_BRAINSTORM_DIR}/manifest.json" ]]; then
  jq -r '.items[] | select(.type == "brainstorm" and .status != "completed" and .status != "promoted") | "\(.identifier)\t\(.title)\t\(.current_phase)\t\(.updated_at)"' "${LEGACY_BRAINSTORM_DIR}/manifest.json"
fi
```

**If active sessions exist AND an argument was provided:**
Check whether any session identifier or title fuzzy-matches `$ARGUMENTS`. If a match is found, present it:

```
Found active brainstorm: {title} ({slug})
Status: {current_phase} — last updated {updated_at}

Resume this session? [y] Yes  [n] No, start fresh  [s] Show status
```

Use AskUserQuestion. On **yes**: rebind `BRAINSTORM_ROOT` to the directory the
session was listed from — `$BRAINSTORM_DIR` for a new-style entry,
`$LEGACY_BRAINSTORM_DIR` for one surfaced by the legacy query above — then load
state from `$BRAINSTORM_ROOT/{slug}/state.json` and resume from the last
incomplete phase. A legacy session is resumed and updated in place. On **show
status**: display phase completion table, then ask again. On **no**: continue to
Phase 1.

**If no argument and active sessions exist:** Skip this check — Phase 1 will ask for the feature description and can detect duplicates at that point.

**If no active sessions:** Proceed directly to Phase 1.

---

### Phase 1: Capture Requirements

#### 1.1 Get Feature Description

**From $ARGUMENTS:**
- If provided → Use as feature description
- If empty → Use AskUserQuestion:

```
What feature or change do you want to brainstorm?

Provide a brief description (1-3 sentences):
- What problem are you solving?
- What does the business want?
- Any key constraints?

Examples:
- "Users need to export their data to Excel"
- "Integrate SSO with Azure AD for authentication"
- "Add webhook notifications when orders complete"
```

Store as `{feature_description}`.

#### 1.2 Gather Business Context

Use AskUserQuestion to understand context:

```
Questions:
1. What's the business driver?
   - New customer requirement
   - Compliance/regulatory need
   - Performance or user-experience improvement
   - Technical debt reduction

2. What's the urgency?
   - Critical (blocking customers)
   - High (planned for next sprint)
   - Medium (on roadmap)
   - Low (nice to have)

3. Any known constraints?
   - Must use specific technology
   - Budget limitations
   - Timeline restrictions
   - Integration requirements
```

#### 1.3 Create Work Directory and State File

```bash
# Re-derived here: shell state does not survive between Bash tool calls.
if [ -f "${CLAUDE_PLUGIN_ROOT}/shared/resolve-config.sh" ]; then
  source "${CLAUDE_PLUGIN_ROOT}/shared/resolve-config.sh"
elif [ -f "$HOME/.claude/shared/resolve-config.sh" ]; then
  source "$HOME/.claude/shared/resolve-config.sh"
else
  echo "ERROR: resolve-config.sh not found — reinstall the nexus plugin: /plugin install nexus@claude-skills" >&2
  exit 1
fi
BRAINSTORM_DIR=$(resolve_artifact brainstorms brainstorm)
BRAINSTORM_ROOT="$BRAINSTORM_DIR"
mkdir -p $BRAINSTORM_ROOT/{slug}/context
```

Where `{slug}` is kebab-case version of feature (e.g., "user-data-export").

Initialize state file `$BRAINSTORM_ROOT/{slug}/state.json`:

```json
{
  "schema_version": 1,
  "identifier": "{slug}",
  "type": "brainstorm",
  "title": "{feature_description_summary}",
  "status": "in_progress",
  "created_at": "{ISO_TIMESTAMP}",
  "updated_at": "{ISO_TIMESTAMP}",
  "selected_approach": null,
  "phases": {
    "exploration": {"status": "pending"},
    "approaches": {"status": "pending"},
    "refinement": {"status": "pending"},
    "quality_guard": {"status": "pending"},
    "work_breakdown": {"status": "pending"}
  },
  "outputs": {
    "exploration": "context/exploration.md",
    "business_context": "context/business-context.md",
    "approaches": "context/approaches.md",
    "architecture_validation": "context/architecture-validation.md",
    "implementation_picture": "implementation-picture.md",
    "work_breakdown": "work-breakdown.md",
    "summary": "brainstorm-summary.md"
  },
  "updates": []
}
```

Register active session for the optional `auto-context.sh` PostToolUse hook (no-op when neither `CLAUDE_SESSION_ID` nor `CLAUDE_CODE_SESSION_ID` is set):

```bash
# Re-derived here: shell state does not survive between Bash tool calls.
if [ -f "${CLAUDE_PLUGIN_ROOT}/shared/resolve-config.sh" ]; then
  source "${CLAUDE_PLUGIN_ROOT}/shared/resolve-config.sh"
elif [ -f "$HOME/.claude/shared/resolve-config.sh" ]; then
  source "$HOME/.claude/shared/resolve-config.sh"
else
  echo "ERROR: resolve-config.sh not found — reinstall the nexus plugin: /plugin install nexus@claude-skills" >&2
  exit 1
fi
BRAINSTORM_DIR=$(resolve_artifact brainstorms brainstorm)
BRAINSTORM_ROOT="$BRAINSTORM_DIR"
# A wrong or missing substitution must fail here, not write next to `/`.
[ -n "<WORK_DIR printed above>" ] && [ -d "<WORK_DIR printed above>" ] || exit 1
SID="${CLAUDE_SESSION_ID:-${CLAUDE_CODE_SESSION_ID:-}}"
if [ -n "$SID" ] && command -v jq >/dev/null 2>&1; then
  mkdir -p "$BRAINSTORM_ROOT" "<WORK_DIR printed above>"
  touch "<WORK_DIR printed above>/.active-sessions.lock"
  (
    flock -x -w 2 200 || exit 0
    [ -s "<WORK_DIR printed above>/.active-sessions" ] || echo '{}' > "<WORK_DIR printed above>/.active-sessions"
    jq --arg s "$SID" --arg w "{slug}" \
       '. + {($s): $w}' "<WORK_DIR printed above>/.active-sessions" \
       > "<WORK_DIR printed above>/.active-sessions.tmp.$$" \
       && mv "<WORK_DIR printed above>/.active-sessions.tmp.$$" "<WORK_DIR printed above>/.active-sessions" \
       || rm -f "<WORK_DIR printed above>/.active-sessions.tmp.$$"
  ) 200>"<WORK_DIR printed above>/.active-sessions.lock"
fi
```

---

### Phase 2: Exploration

**Goal:** Understand what exists and what's needed.

#### 2.1 Explore Codebase

Use Task tool with `subagent_type: "Explore"`. Read `references/agent-prompts.md` (Phase 2.1 section) for the prompt template.

Save output to `$BRAINSTORM_ROOT/{slug}/context/exploration.md`. Update state: `phases.exploration = completed`.

#### 2.2 Understand Business Requirements

Use Task tool with `subagent_type: "business-analyst"`. Read `references/agent-prompts.md` (Phase 2.2 section) for the prompt template.

Save output to `$BRAINSTORM_ROOT/{slug}/context/business-context.md`. Update state: `phases.exploration = completed` (covers both exploration agents).

**Before launching parallel agents, define non-overlapping scopes.** Each agent should own one domain of knowledge with no shared territory. Split by system/component boundary, not by feature keyword. Example:
- Agent 1 (Explore): "How does {system A} work — services, commands, flags, data flow"
- Agent 2 (business-analyst): "Business requirements — problem, personas, success metrics, edge cases"

Do NOT include supporting context from one agent's domain in the other's prompt.

**Run both agents in parallel.**

---

### Phase 3: Generate Approaches

**Goal:** Present 2-3 different ways to implement this feature.

#### 3.0 Path selection

Two paths through **3.1 and 3.1b only**. 3.2 and 3.3 are unchanged on both.

**Attempt the orchestrated path when both hold:**
- `<BRAINSTORM_WORKFLOW_ENABLED printed above>` is `true` (the default), and
- the `Workflow` tool is available in this session.

**If so, read `references/workflow-judge-panel.md` and follow it.** It replaces 3.1 and 3.1b
and changes what 3.2 and 4.5 receive. Pass the captured feature, the Phase 2 exploration and
business context, the repo name, optionally a shorter `angles` list, and a timestamp as
`args` — the script cannot read files or shell out.

**Choose how wide to cast before calling.** All four angles run by default; pass a shorter
`angles` list for a small feature. The script generates what it is given and cannot judge
whether four proposals are warranted — that is a read on the size of the thing, which the lead
has and the script does not.

**What it does NOT replace. All of it stays in the lead:**

1. **The user's choice at 3.3.** The script scores and recommends; it never decides. Present
   the synthesis as one option *alongside* the originals, not instead of them.
2. **Every write** — `approaches.md`, `architecture-validation.md`, the state update, the
   manifest.
3. **Phase 0 resume, Phase 1 capture, the Phase 4 refine loop, and 4.5**, which now judges the
   synthesis rather than a single-pass proposal.

**Take the classic path — silently, it is not an error — when:**
- the config disables it, or
- the `Workflow` tool is not available, or
- the orchestrated run fails, does not complete, or returns `ok: false`.

**On any of those, run 3.1 and 3.1b below in full.** Name the path taken when presenting at
3.2 either way.

**Read the failure before discarding it.** An `ok: false` result is not empty, and 3.1z is
skipped on this branch, so this is the only place its fields are ever seen:

- **`stage`** says what died. `generate` means no angle produced a usable approach; `judge`
  means approaches were generated but the panel produced no usable score row — a judge
  scoring by approach *name* instead of by id lands here while looking perfectly healthy.
  Two very different situations, and the second is a defect worth reporting.
- **`unknownAngles` / `anglesArgIgnored`** mean the angles argument was wrong: a name that
  does not exist, or a value that was not an array. That is a bug in *this skill's* call,
  not in the feature, and it is the likeliest reason a `generate` stage came back empty.
- **`judgeIntegrity.rejected`** on a `judge` failure names every judge whose rows were
  discarded and why — `off-scale`, `malformed`, `unknown-approach-id`, or
  `contradictory-duplicate`. Three rejections
  out of three is a panel that did not follow the scoring contract at all, which is worth
  reporting as a defect rather than absorbing silently into the classic path.

Say in one line what failed and why before running the classic path. Falling back silently
after a `judge`-stage failure hides a script defect behind a working result.

---

#### 3.1 Brainstorm Implementation Options

Use Task tool with `subagent_type: "Plan"`. Read `references/agent-prompts.md` (Phase 3.1 section) for the prompt template, including the architectural-distinction and trade-off rules.

Save output to `$BRAINSTORM_ROOT/{slug}/context/approaches.md`. Update state: `phases.approaches = in_progress`.

#### 3.1b Validate Architecture Context

**Run in PARALLEL with 3.1** — the architect works from exploration context, not from Plan's approaches.

Use Task tool with `subagent_type: "architect"`:

```
Prompt: Analyze the project's architectural constraints and patterns relevant to this feature.

Feature: {feature_description}
Codebase patterns: {from exploration.md}

Assess:
1. Architecture style in use (layered, hexagonal, modular, MVC) and its constraints
2. Established patterns that any implementation MUST follow
3. Integration points and their architectural boundaries
4. Known technical debt or fragile areas to avoid
5. Scalability constraints relevant to this feature

Provide:
- A list of architectural constraints any approach must satisfy
- Patterns that must be followed (with file path examples)
- Risk areas to avoid
- A feasibility checklist for evaluating approaches
```

Save output to `$BRAINSTORM_ROOT/{slug}/context/architecture-validation.md`.

When both 3.1 (Plan agent) and 3.1b (architect) have returned, annotate each approach from 3.1 with architect constraints from 3.1b. Flag any approach that violates identified constraints. Add feasibility rating: Recommended / Feasible / Risky / Not Recommended.

#### 3.1z Consume the orchestrated result (orchestrated path only)

Skip this step entirely on the classic path.

1. **Write the files yourself.** `context/approaches.md` from `approaches` and `synthesis`,
   `context/architecture-validation.md` from `constraints`. The script wrote nothing.
2. **Show the scores at 3.2, not just the ranking.** `criteria` and `scores` come back in
   full — every judge's row, the per-criterion means and the total — so the user can disagree
   with a number rather than with a verdict. A ranking with the arithmetic hidden is the prose
   judgment this path replaced.
3. **Present the synthesis as one option beside the originals.** It is built from the winner
   and grafted from the runners-up, each graft naming its source id. It is not automatically
   the right answer, and 3.3 still asks.
4. **Say when a tie was broken.** `tieBroken` true means two approaches scored identically and
   declaration order decided it. That is a tie-break, not a judgement, and the user may prefer
   the other one.
5. **Say when a panel was short.** `generatorIntegrity` incomplete means an angle is missing
   from the comparison entirely; `judgeIntegrity` incomplete means the totals rest on fewer
   judges than were dispatched. `fullyScored: false` means exactly that — fewer judges than
   dispatched — and after any rejection EVERY approach carries it while the panels stay
   identical, so it is not the relative-evidence signal it looks like. For "was this approach
   judged on less evidence than its rivals", read `rankingComparable` and `judgePanels`.
6. **`constraintsRan: false` is not "no constraints".** It means nobody checked. Say which one
   happened — an empty list reads as the comfortable claim.
7. **`graftsDropped > 0`** means the synthesis cited approach ids that do not exist. Worth a
   line, because it casts doubt on its other attributions.
8. **`judgeIntegrity.rejected` is the one to say out loud.** Each entry names a judge whose
   rows were discarded **in full** — every approach, not just the one it fumbled — and why.
   A judge is rejected when it scored off the 1-5 scale, returned a non-number, scored an
   approach nobody generated, or gave one approach two different scores. Discarding it everywhere is what keeps the remaining totals
   means over one panel rather than a mix; keeping its good rows was tried four times and each
   version decided a winner the panel had not chosen.
9. **Do not call the result undistorted.** A smaller panel is a *commensurable* comparison,
   not an unbiased one: judges are not interchangeable, and a harsh judge's absence lifts every
   approach it would have marked down. Say who is missing, why, and that a full panel might
   have ranked differently. `rowTriage.duplicate` is minor by comparison — it counts identical
   repeats only, so nothing was lost.
10. **`rankingComparable: false` means the totals are means over different panels** — judged
    by *which* judges, not how many, so two approaches with two judges each and none in common
    counts as uneven. `judgePanels` names the panel behind each. Rejection cannot cause this
    (it removes a judge from every approach at once); a judge that simply omitted an approach
    can. Show the ranking and say who scored what.
11. **`total` follows the rows, `means` are rounded for display.** Their visible sum can sit
    a cent below the total (four means of 3.333 print as 3.33 and sum to 13.32 against a total
    of 13.33). That is display rounding, not an error; do not "correct" either number when
    presenting them.
12. **`unknownAngles` and `anglesArgIgnored` are caller bugs.** An angle name that does not
    exist, or an `angles` value that was not an array, was requested and silently did not
    take effect. Report it as a defect in the invocation, not as a finding about the feature.

---

#### 3.2 Present Approaches to User

Display the approaches using the format in `references/display-templates.md` (Phase 3.2 section).

#### 3.3 Get User Feedback

Use AskUserQuestion:

```
Which approach interests you most?

1. {Approach 1 name}
2. {Approach 2 name}
3. {Approach 3 name}
4. Combination of approaches
```

At most 4 options. With more than three candidates (the orchestrated path returns up to four
approaches plus the synthesis), offer the synthesis and the highest-ranked originals. The
tool's free-text **Other** covers "none of these" and specific feedback.

Update state with selected approach: `"selected_approach": "{approach_name}", "phases.approaches": "completed"`.

---

### Phase 4: Refine & Iterate

**Goal:** Refine the chosen approach based on feedback.

#### 4.1 Deep Dive on Selected Approach

Based on user selection, use Task tool with `subagent_type: "Plan"`. Read `references/agent-prompts.md` (Phase 4.1 section) for the refinement prompt covering component breakdown, data flow, database changes, API design, security, and testing strategy.

Save to `$BRAINSTORM_ROOT/{slug}/implementation-picture.md`. Update state: `phases.refinement = completed`.

#### 4.2 Validate Architecture

Use Task tool with `subagent_type: "architect"`. Read `references/agent-prompts.md` (Phase 4.2 section) for the architecture-validation prompt.

**Run architect AFTER Plan refinement completes** — architect needs the refined implementation picture from 4.1 to validate effectively.

#### 4.3 Present Refined Approach

Show the detailed implementation picture using the format in `references/display-templates.md` (Phase 4.3 section).

#### 4.4 Ask if More Refinement Needed

Use AskUserQuestion:

```
Is this implementation picture clear?

1. Yes, I understand the approach
2. Need more detail on specific area (tell me which)
3. Want to explore a different approach
4. Ready to outline work items
```

If user wants more detail, repeat refinement on specific areas.

---

### Phase 4.5: Quality Guard Validation

**Goal**: Independently challenge the implementation picture before committing to the work breakdown.

Use Task tool with `subagent_type: "quality-guard"`. Read `references/agent-prompts.md` (Phase 4.5 section) for the challenge prompt, which lists the context files to read and the 6 review questions. The verdict is APPROVED / CONDITIONAL / REJECTED.

**Process the verdict:**

- **APPROVED**: Update state `phases.quality_guard = completed/approved`. Proceed to Phase 5.
- **CONDITIONAL**: Present concerns to user. Annotate them in the work breakdown as risks. Update state `phases.quality_guard = completed/conditional`. Proceed to Phase 5.
- **REJECTED**: Present the fundamental issue to the user via AskUserQuestion. Options:
  1. Return to Phase 3 to select/refine a different approach
  2. Override and proceed (user accepts the risk)

Save quality-guard output to `$BRAINSTORM_ROOT/{slug}/context/quality-guard.md`. Update state: `phases.quality_guard = completed`.

---

### Phase 5: Work Breakdown

**Goal:** Outline tickets/tasks needed.

#### 5.1 Break Down Into Work Items

Based on the implementation picture, create logical work items:

```markdown
## Work Items

### 1. Database Schema
**Type:** Database
**Description:** Create migrations for new entities
**Files affected:**
- migrations/Version{timestamp}.php
- Entity/{Entity1}.php
- Entity/{Entity2}.php

**Dependencies:** None
**Estimate:** Small (< 1 day)

---

### 2. Service Layer
**Type:** Backend
**Description:** Implement core business logic
**Files affected:**
- Service/{Feature}/{ServiceName}.php
- Tests/Service/{Feature}/{ServiceName}Test.php

**Dependencies:** #1 (Database Schema)
**Estimate:** Medium (1-2 days)

---

### 3. API Endpoints
**Type:** Backend
**Description:** Create REST endpoints
**Files affected:**
- Controller/{Feature}/{HTTPMethod}Controller.php
- Model/{Feature}/{HTTPMethod}Request.php
- Model/{Feature}/{HTTPMethod}Response.php

**Dependencies:** #2 (Service Layer)
**Estimate:** Medium (1-2 days)

---

{Additional work items...}
```

Save to `$BRAINSTORM_ROOT/{slug}/work-breakdown.md`. Update state: `phases.work_breakdown = completed`.

#### 5.2 Create Visual Summary

Generate ASCII diagram showing relationships:

```
Work Item Flow:

[1] Database Schema
     ↓
[2] Service Layer
     ↓
[3] API Endpoints
     ↓
[4] Frontend (if applicable)

Parallel work:
- [5] External API Integration (independent)
- [6] Documentation (can start anytime)

Estimated total: {X} days/weeks
```

#### 5.3 Present Work Breakdown

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Work Breakdown: {feature}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Total Items: {N}
Estimated Effort: {X} days/weeks

{work_items_summary}

{visual_flow_diagram}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Files Created:

$BRAINSTORM_ROOT/{slug}/
├── state.json
├── context/
│   ├── exploration.md
│   ├── business-context.md
│   ├── approaches.md
│   ├── architecture-validation.md
│   └── quality-guard.md
├── implementation-picture.md
├── work-breakdown.md
└── brainstorm-summary.md

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Next Steps:

1. Review the work breakdown
2. Create detailed requirements: /create-requirements --from-brainstorm {slug}
3. Or break into epic: /epic "{feature}"
4. Or start implementing first item directly

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

### Phase 5.5: Update Manifest

After saving all brainstorm outputs, update the brainstorms manifest.

Update the manifest that **owns this session** — `$BRAINSTORM_ROOT`, not
`$BRAINSTORM_DIR`. For a resumed pre-migration session those differ, and writing
to the new artifact would leave the legacy entry permanently un-completed, so it
would keep reappearing as resumable in Phase 0, `/resume-work` and
`/work-status` (see `${CLAUDE_PLUGIN_ROOT}/shared/manifest-schema.md` for the
envelope/upsert contract):

```bash
# Re-derived here: shell state does not survive between Bash tool calls.
if [ -f "${CLAUDE_PLUGIN_ROOT}/shared/resolve-config.sh" ]; then
  source "${CLAUDE_PLUGIN_ROOT}/shared/resolve-config.sh"
elif [ -f "$HOME/.claude/shared/resolve-config.sh" ]; then
  source "$HOME/.claude/shared/resolve-config.sh"
else
  echo "ERROR: resolve-config.sh not found — reinstall the nexus plugin: /plugin install nexus@claude-skills" >&2
  exit 1
fi
BRAINSTORM_DIR=$(resolve_artifact brainstorms brainstorm)
BRAINSTORM_ROOT="$BRAINSTORM_DIR"
MANIFEST="${BRAINSTORM_ROOT}/manifest.json"
# Initialize if missing. artifact_type follows the manifest being written:
# "brainstorms" for $BRAINSTORM_DIR. A legacy <WORK_DIR printed above> manifest already exists
# with artifact_type "work" — never rewrite that envelope.
if [[ ! -f "$MANIFEST" ]]; then
  # Create empty manifest with artifact_type: "brainstorms"
  :  # written with the Write tool, not from this block
fi
```

**Upsert item.** The two manifests use different key shapes, so match on either
and *keep the shape the existing entry already has* — converting a legacy work
entry to the brainstorms schema would orphan it from `/resume-work`'s
identifier-keyed work scan:

- **`$BRAINSTORM_DIR` (normal):** brainstorms schema below, unique key `slug`.
- **`$WORK_DIR` (resumed legacy session):** the entry is already there under
  `identifier` with `type: "brainstorm"`. Update `status`, `current_phase` and
  `updated_at` on that entry in place. Do **not** insert a second, slug-keyed
  entry beside it.

Match with `select(.slug == $id or .identifier == $id)`, the same dual-key form
the Promote flow uses.

Brainstorms schema (for `$BRAINSTORM_DIR`) — *not* the work schema; brainstorms
carry both catalog fields and session fields because a brainstorm is resumable
until it is promoted:

```json
{
  "slug": "{slug}",
  "title": "{feature_description_summary}",
  "status": "in_progress|completed|promoted",
  "created_at": "{ISO_TIMESTAMP}",
  "updated_at": "{ISO_TIMESTAMP}",
  "current_phase": "completed",
  "selected_approach": "{chosen_approach_name}",
  "alternatives_count": {n},
  "promoted_to": null,
  "tags": [],
  "path": "{slug}/"
}
```

Update `last_updated` and `total_items` in the envelope.

---

### Phase 6: Create Summary

Write a comprehensive summary document:

**`$BRAINSTORM_ROOT/{slug}/brainstorm-summary.md`:**

```markdown
# Brainstorm Summary: {feature}

**Date:** {timestamp}
**Status:** Completed

## Business Context

{summary_from_phase_2}

## Approaches Considered

### Approach 1: {name}
{brief_description}
**Outcome:** {Selected | Rejected - why}

### Approach 2: {name}
{brief_description}
**Outcome:** {Selected | Rejected - why}

## Selected Approach: {name}

### Why This Approach?
{rationale}

### Implementation Picture

**Components:**
{list}

**Data Flow:**
{steps}

**Database:**
{changes}

**APIs:**
{endpoints}

### Work Breakdown

{work_items_summary}

**Total Effort:** {estimate}

## Risks & Considerations

- Risk 1: {description}
  - Mitigation: {how to address}

- Risk 2: {description}
  - Mitigation: {how to address}

## Next Steps

1. {action 1}
2. {action 2}
3. {action 3}

## Decision Log

- **{Date}:** Selected {approach_name} because {reason}
- **{Date}:** Decided to {decision} based on {rationale}

## References

- Codebase examples: {file_paths}
- Related features: {links}
- External docs: {urls if any}
```

Update state: `"status": "completed", "updated_at": "{ISO_TIMESTAMP}"`.

Then clear the session registry:

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

Read `references/error-handling.md` for error-scenario message templates (no feature description, feature too vague, all approaches rejected).

---

## Important Notes

- **Non-committal** - Brainstorming doesn't create branches or modify code
- **Lightweight** - Files saved to `$BRAINSTORM_ROOT/` for reference only
- **Flexible** - Can iterate multiple times before moving forward
- **Educational** - Explains trade-offs to help decision-making
- **Transition-ready** - Outputs can feed into next workflow stage

---

## Workflow Integration

```
Business Request
      ↓
/brainstorm ← [You are here]
      ↓
   Decision: What next?
      ↓
      ├─→ /create-requirements (single feature)
      ├─→ /epic (large initiative, multiple tickets)
      ├─→ /create-proposal (formal proposal needed)
      └─→ Direct implementation (simple, well-understood)
```
