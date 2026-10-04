---
name: design
version: 1.4.0
description: >
  Plan implementation before coding: investigate the repo, write spec and plan,
  and validate with a peer. Use for "plan", "design approach", "scope", or any
  coding task needing a plan. Not system-design thinking
  (/ship:arch-design) or full /ship:auto.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Agent
  - AskUserQuestion
  - mcp__codex__codex
  - mcp__codex__codex-reply
---

# Ship: Design

You ARE the planner. You read code, investigate, write spec and plan.
Read the load-bearing code yourself — a plan written from someone
else's summary loses the context that makes it executable. On a large
repo you may use read-only search agents to scout breadth (locate
files, callers, conventions), but scouts locate code; they never
replace your own reading of what you cite. A peer agent investigates
independently and produces its own spec for adversarial comparison.

## Runtime Resolution

_Path note: `../shared/*.md` references resolve against this skill's base
directory (announced as "Base directory for this skill" when the skill
loaded), not your working directory._

See `../shared/runtime-resolution.md` for the host/peer concept and
dispatch commands. In /ship:design, the peer plays two roles:
**investigator** (Phase 2) and **drill agent** (Phase 6).

## Scope Mode

The prompt may specify `Scope mode: full` (default) or
`Scope mode: refactor`. It controls how much adversarial validation runs:

| Phase | `full` | `refactor` |
|-------|--------|-----------|
| 1 Init | ✅ | ✅ |
| 2 Investigate (host + peer) | ✅ | ✅ |
| 3 Write spec | ✅ | ✅ (behavior-contract template) |
| 4 Diff & verify | ✅ | ✅ |
| 5 Write plan | ✅ | ✅ |
| 6 Execution drill | ✅ | ⏭ **skipped** |

**Why refactor mode skips Phase 6:** for behavior-preserving changes
(refactor, simplify, rename, extract, dedupe), the plan steps are
usually small, mechanical code movements. The drill's "is every step
implementable" check earns little here while adding a full peer
round-trip. Peer investigation and diff stay on because they catch the
real refactor failure mode — "moved complexity instead of removing it."

If no scope mode is specified (e.g. standalone /ship:design invocation),
default to `full`.

## Process Flow

```
Phase 1  Init            resolve task_id, create .ship/tasks/<id>/plan/
Phase 2  Investigate     dispatch peer (parallel) ─┐
                         you read the code         │
                         ↓                         │
Phase 3  Write spec      write host spec.md  ←─── peer writes peer-spec.md
                         vague? ask user → re-investigate
                         ↓
Phase 4  Diff & verify   compare specs → resolve each divergence
                         disagree? → debate peer (max 2 rounds)
                         still open? → escalate to user
                         critical gap? → re-investigate (max 1 loop)
                         ↓
Phase 5  Write plan      write plan.md with executable tasks
                         self-review against spec
                         ↓
Phase 6  Execution drill dispatch peer (fresh session) to validate plan
                         BLOCKED step?  → escalate
                         UNCLEAR step?  → revise plan (max 1 loop)
                         all CLEAR      → ready for execution
```

## Roles

| Phase | Who | Why |
|-------|-----|-----|
| Investigation (read code, trace paths) | **Host + peer (parallel)** | Independent investigation catches different blind spots |
| Write spec (host version) | **You** | Investigation context must not be lost |
| Write spec (peer version) | **Peer agent** | Independence requires separation |
| Diff & verify divergences | **You** | You have the context + code access to judge |
| Write plan.md | **You** | Spec context must flow into plan |
| Execution Drill | **Peer agent** (fresh session) | Fresh eyes test implementability |


## Quality Gates

| Gate | Condition | Fail action |
|------|-----------|-------------|
| Investigation → Spec | All claims trace to file:line you read | Re-investigate |
| Spec → Diff | spec.md has flexible sections scaled to complexity, self-reviewed | Revise |
| Diff → Plan | Zero `escalated` items (resolved by evidence or debate, or user resolved them) | Ask user |
| Plan → Drill | plan.md has TDD tasks, checkbox steps, complete code, no placeholders | Revise |
| Drill → Ready | Zero BLOCKED steps, zero UNCLEAR steps | Revise plan (max 1 loop) |

No artifact passes to the next phase without meeting its gate.

## Progress Tracking

Track your progress with the harness's task/todo list. After Phase 1
(init), create items that reflect the actual work ahead. Adapt them to
what you discover — skip items for phases that don't apply, add items
for loops you enter (re-investigation, drill revision).

**Principle**: one item per major phase the user would care about.
Update the in-progress label to reflect what's happening within a phase.

**Example** (full run with peer available):

```
[in_progress] Investigate codebase (host + peer)
[pending]     Write spec
[pending]     Diff host vs peer specs
[pending]     Write implementation plan
[pending]     Execution drill
```

**Adaptations** (not exhaustive — use judgment):
- Peer unavailable → drop "Diff" item, rename "Investigate" to reflect self-produced peer spec
- Upstream spec already exists → drop "Write spec", start with "Validate existing spec"
- Re-investigation needed → re-mark "Investigate" as in progress
- Drill revision needed → keep "Execution drill" as in progress

## Red Flag

**Never:**
- Cite files you haven't opened
- Let the peer see your spec before producing its own
- Resolve divergences by reasoning instead of code evidence (max 2 debate rounds, both cite file:line)
- Trust prior conversation over disk artifacts
- Mark plan ready when drill has BLOCKED or UNCLEAR items
- Skip the drill because "the plan looks solid"
- Write a spec claim from a sub-agent's summary — read-only search
  agents may scout breadth on a large repo (where things live, callers,
  naming conventions), but every claim that enters the spec must trace
  to file:line YOU read
- Claim "function X is not called" without tracing all callers
- Propose a fix without searching for existing defenses
- Propose to create a file without checking if it already exists
- Change a value without grepping tests that assert the old value
- Write plan.md with vague steps or placeholders (TBD, TODO, "similar to Task N")

---

## Phase 1: Init

- Resolve task_id, create `.ship/tasks/<task_id>/plan/` directory.
- If resuming, read existing artifacts and determine current state.
- Collect branch name and HEAD SHA.

### Task ID

1. If invoked by /ship:auto, the task_id is provided.
2. If invoked standalone, generate a concise deterministic task slug:
   ```bash
   TASK_ID=$(printf '%s' "<description>" \
     | tr '[:upper:]' '[:lower:]' \
     | sed 's/[^a-z0-9]/-/g' \
     | sed 's/--*/-/g' \
     | sed 's/^-//;s/-$//' \
     | cut -c1-60)
   ```

Artifacts go to `.ship/tasks/<task_id>/plan/`. The Write tool creates
directories automatically — no mkdir needed.

### Existing spec.md detection

Check if `spec.md` already exists with content:
```bash
[ -s .ship/tasks/<task_id>/plan/spec.md ] && echo 'SPEC_EXISTS' || echo 'NO_SPEC'
```

If `SPEC_EXISTS`:
- Read `spec.md`. This was written by an upstream skill (e.g. refactor).
- Check if spec records a HEAD SHA. If it does and it differs from
  current HEAD, treat spec as stale — proceed as `NO_SPEC`.
- **Do not overwrite it.** Use it as your investigation input.
- Your job narrows: investigate to validate the spec's claims, then
  produce only `plan.md`. You may append an `## Investigation` section
  to the existing spec if it lacks one, but preserve all existing sections.
- Peer investigation and diff still run — the peer validates the
  upstream spec independently. Execution drill runs per Scope Mode
  (always in `full`, skipped in `refactor`).

If `NO_SPEC`: proceed to Phase 2.

## Phase 2: Investigate (Parallel)

**This is the most important phase. Do not rush it.**

### Step A: Dispatch peer investigation

Kick off the peer investigation **before** you start investigating.
The peer works in parallel while you read code.

Read `independent-investigator.md` for the dispatch pattern and
prompt template. Fill in the task description, task_id, and repo root.
Dispatch the resolved peer runtime and save the returned thread or
session id as `INVESTIGATION_THREAD_ID` when the runtime provides one
— needed for debate in Phase 4.

#### When the peer agent is unavailable

If peer dispatch fails, self-produce the second spec:
1. Run a second-pass review of your spec using only: placeholder scan,
   contradiction scan, coverage scan, ambiguity scan
2. Search for code paths, callers, or consumers you did not trace
3. Write `peer-spec.md` with any changed conclusions or additions
4. Add a warning: `WARNING: Second spec was self-generated, not independent`

### Step B: Your investigation

Read `write-spec.md` for investigation methodology and spec authoring.

Investigate the codebase, then write `spec.md`. The reference covers
investigation strategy (bug fixes, new features, all tasks), vagueness
checks, spec structure, and self-review.

If investigation reveals hidden dependencies or cross-cutting concerns
not apparent from the task description, note them for the spec.

## Phase 3: Write Spec

Covered by `write-spec.md` — follow the spec writing and self-review
guidance there.

## Phase 4: Diff & Verify

Read `peer-spec.md` (written by the peer investigation dispatched in Phase 2).
Compare it against your `spec.md`.

### For each divergence point:

1. **Identify the divergence** — what does your spec say vs the peer spec?
2. **Verify against code** — read the actual code to determine which
   is correct. Do NOT resolve by reasoning about which "sounds better."
3. **If still disagree — debate with the peer agent.** Continue on the
   same peer thread or session when possible using that runtime's
   follow-up mechanism. Present your code evidence and ask the peer to
   present counter-evidence. If the runtime cannot continue the same
   session, dispatch a fresh peer session with the prior evidence quoted
   verbatim. Maximum 2 debate rounds. Both sides must cite file:line
   references.
4. **Assign disposition after debate:**
   - **patched** → Your spec updated based on evidence. Show the diff.
   - **proven-false** → The peer claim is wrong. Cite the code evidence.
   - **conceded** → The peer convinced you with code evidence. Update spec.
   - **escalated** → 2 debate rounds exhausted, still unresolved. Needs user input.

### Record in diff-report.md

Only record divergences and their resolutions. If both specs agree on
something, there's nothing to record — move on.

For each divergence, write what happened: what each side claimed, what
code evidence was cited during debate, and the final disposition
(patched / proven-false / conceded / escalated).

### After diff resolution:

- Update `spec.md` with all `patched` and `conceded` items.
- If any `escalated` items exist:
  - **Standalone mode:** ask user via AskUserQuestion before proceeding.
    Record the user's ruling in diff-report.md with disposition
    `user-resolved` and what they decided. Update spec.md accordingly.
  - **/ship:auto mode:** do NOT ask user. Treat escalated items as BLOCKED
    and return. `/ship:auto` owns the only user-approval gate.
- If diff reveals a critical investigation gap (e.g., the peer found
  important code you missed entirely), go back to Phase 2 for
  targeted re-investigation. Maximum 1 re-investigation loop.

## Phase 5: Write Plan

Read `write-plan.md` for plan structure, task granularity, no-placeholder
rules, and self-review.

Translate the validated spec.md into an executable plan.md. The reference
covers the plan template, bite-sized steps, code completeness guidance,
and the self-review checklist.

## Phase 6: Execution Drill

**Skip this phase when `Scope mode: refactor`.** Record in the report
card that the drill was skipped due to refactor scope, then finish.

For `full` scope (default), run the drill as below.

The final gate. Give the plan to the peer agent and ask it to validate
every step is implementable.

Read `execution-drill.md` for the dispatch pattern, role, and
prompt template. Use a **new** peer session, not the investigation
thread. Save the returned thread or session id as `DRILL_THREAD_ID`
when the runtime provides one — needed for revision reruns.

#### When the peer agent is unavailable

If peer dispatch fails, dispatch a fresh fallback Agent to perform the
drill instead. The Agent gets the same prompt from `execution-drill.md`
— it reads spec.md and plan.md with no prior context, providing the
best available independent review. Add a warning:
`WARNING: Drill was fallback-Agent-performed, not peer-agent`

### After the drill:

- **All CLEAR** → Plan is ready for execution.
- **UNCLEAR items** → Revise plan.md to make each step unambiguous.
  Then re-run ONLY the unclear steps:
  - If the peer runtime supports continuation, continue on
    `DRILL_THREAD_ID` with: "Tasks N, M were revised. Re-read plan.md
    and re-evaluate ONLY those tasks using the same criteria. Report
    CLEAR/UNCLEAR/BLOCKED."
  - Otherwise re-dispatch the peer agent with the same
    `execution-drill.md` prompt scoped to the revised tasks only.
  - If peer dispatch is unavailable, use the same fallback-Agent pattern.
  Maximum 1 revision loop.
- **BLOCKED items** → If resolvable by investigation, investigate and
  fix. If not, escalate to user or mark plan as `blocked`.

---

## Artifacts

```text
.ship/tasks/<task_id>/
  plan/
    spec.md          — final merged spec (flexible sections, brainstorming style)
    peer-spec.md     — peer agent's independent spec
    plan.md          — how to build it (TDD tasks, writing-plans style)
    diff-report.md   — host spec vs peer spec divergences and resolutions
```

## Error Handling

| Error | Action |
|-------|--------|
| Peer agent unavailable | Self-produce second spec + fallback drill with warning |
| Peer output unparseable | Retry once with format reminder, then fall back to fallback drill |
| Timeout | Abort, preserve artifacts, summarize honestly |
| Re-investigation needed | Maximum 1 loop back to Phase 2 |
| Drill revision needed | Maximum 1 revision loop |

## Completion

### Only stop for
- Task too vague to plan → ask user via AskUserQuestion
- Execution drill blockers that require user input → `blocked`
- Timeout → preserve artifacts, summarize honestly

### Never stop for
- Peer unavailable (self-produce second spec with warning)
- Peer output parse failure (retry once, then fallback Agent)

### Execution Handoff

Verify `spec.md` and `plan.md` are non-empty on disk, then output the report card
(read `../shared/report-card.md` for the standard format):

```
## [Design] Report Card

| Field | Value |
|-------|-------|
| Status | DONE |
| Summary | <task title> — <N> stories planned |

### Metrics
| Metric | Value |
|--------|-------|
| Scope mode | <full | refactor> |
| Files traced | <N> |
| Divergences resolved | <N> (<M> by evidence, <K> by debate) |
| Drill steps CLEAR | <N>/<total>  (or `skipped — refactor scope`) |
| Stories | <N> |

### Artifacts
| File | Purpose |
|------|---------|
| .ship/tasks/<task_id>/plan/spec.md | Merged spec |
| .ship/tasks/<task_id>/plan/peer-spec.md | Peer spec |
| .ship/tasks/<task_id>/plan/plan.md | Executable plan |
| .ship/tasks/<task_id>/plan/diff-report.md | Divergence resolutions |

### Next Steps
1. **Full workflow (recommended)** — /ship:auto to implement, review, QA, refactor, and ship
2. **Implement only** — /ship:dev to execute this plan
3. **Review the plan** — read the artifacts and give feedback
```


### Blocked (both modes)

```
[Design] BLOCKED
REASON: <what failed and why>
ATTEMPTED: <what was tried>
UNRESOLVED: <escalated items from diff or drill>
RECOMMENDATION: <what the user should do next>
```
