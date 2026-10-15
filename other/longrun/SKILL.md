---
provider-specific: true
name: longrun
description: >
  Orchestrates long-running Devin CLI sessions in --sandbox --permission-mode
  autonomous. Bundles workspace selection (git worktree), session continuity
  (seshat/thoth HANDOFF chain), work selection, economy-gated execution,
  quality gates, output classification, promotion, and operator observation
  into one pipeline. Use when devin must run for hours in a sandbox with
  outputs that promote to real work outside. Triggers: "longrun", "long run",
  "sandbox long run", "autonomous long run", "extended sandbox session",
  "multi-session autonomous", "long sandbox run".
version: 0.1.0
execution-mode: side_effecting
meta-skill: orchestrate
meta-skill-mode: invocation-time
meta-skill-topology: ladder
argument-hint: "[--workspace <path>] [--mission <statement>] [--duration <hours>] [--type code|research|ops|govern]"
category: fleet-ops
status: candidate
---

# Longrun

Orchestrates a multi-session, sandboxed, autonomous Devin CLI run whose
outputs promote to real work outside the sandbox. The workspace is a git
worktree; outputs are commits; promotion is merge or ingest.

## When to Use

- Devin needs to run for hours in `--sandbox --permission-mode autonomous`
- Outputs must survive session death and be usable outside the sandbox
- Operator wants a structured pipeline, not ad-hoc autonomous mode
- Multi-session continuity is required (sessions >4h are reaped)

## When NOT to Use

- Single short task — use `/surge` or `/build` directly
- Operator-present interactive pair — use `/pair-mode`
- Unattended research with cost ceilings — use `/autoresearch-mode` directly
- Cross-machine dispatch — use `/swarm` (SSH-based)

## Pre-flight (mandatory before any work)

### 0. Emit SKILL_INVOKE
```
Type: SKILL_INVOKE
To: all
Message: [skill=longrun] [mode=side_effecting] [args_hash=<sha256>] [session=<session_id>]
```

### 0.5. Kill-switch check (I6 — mandatory before any work)
Check the kill switch before proceeding. If engaged,
abort immediately and post a STATUS to the bus:

```bash
python3 -c "
from pathlib import Path
from hummbl_governance import kill_switch
ks_dir = Path('$HOME/.agents/governance/state')
state_file = ks_dir / 'kill_switch_state.json'
if state_file.exists():
    ks = kill_switch.KillSwitch.load_from_file(ks_dir, require_hmac=False)
    if ks.engaged:
        print(f'HALT: kill switch engaged: {ks.mode.name}')
        exit(2)
    print(f'kill-switch: {ks.mode.name}')
else:
    print('kill-switch: no state file (gate skipped)')
"
```

If exit code is 2, post `STATUS: host=<machine> HALT: longrun aborted — kill switch engaged`
to the bus and stop. Do not proceed to Phase 1.

**Repeat this check at the start of each session** (multi-session runs:
each new session must re-check the kill switch before resuming).

### 1. Verify sandbox envelope
Confirm the session is running under `--sandbox`. If not, warn the operator
and ask whether to proceed unsandboxed (not recommended for long runs).

### 2. Select workspace
The workspace determines whether outputs escape the sandbox. Default: create
a git worktree of a fleet repo.

| Type | Workspace | Promotion path |
|------|-----------|----------------|
| code | git worktree of target repo | `commit` → `ship` or `auto-ship` (merge branch) |
| research | git worktree of `hummbl-research` or `autoresearch-reports` | `research-ingest` → CLP + evidence docs |
| ops | git worktree of `~/.agents` | `commit` → `ship` (ops changes) |
| govern | git worktree of `~/.agents` | `evidence-pack` → audit artifacts |

Use `/worktree` to create the worktree. The worktree branch is the staging
area; merge is the promotion.

### 3. Declare mission bounds
Use `/mission-declare` with operator ACK. Set:
- `expected_duration_minutes`: max 480 (8h ceiling per session)
- `cost_budget_usd`: per operator
- `risk`: P2 default, P1 for production-touching work
- `reversible`: true (worktree branches are reversible by default)

### 4. Self-discovery
Run `/self-discovery` to confirm the runtime envelope (model, permissions,
profile, tools, MCP servers) matches expectations.

## Pipeline (8 phases)

### Phase 1: Open — `/seshat`
Read full system state before acting. Seshat reads bus (last 10 + last
HANDOFF), memory (fleet + runtime), git state, health, guardrails. Produces
a 5-line state declaration. Dispatches to the right execution mode.

### Phase 2: Select — `/goal-selection` or `/find-work`
- `/goal-selection` — deterministic next-goal from live bus/repo/PR/CI/memory
- `/find-work` — scan for highest-value next task
- `/inbox-zero` — if the run is a "clear the queue" session

Produce one concrete goal with acceptance criteria and bus receipt.

### Phase 3: Execute — `/jarvis` (outer loop) + sub-skills

**I6 kill-switch check (mandatory before execution):** Re-run the
kill-switch check from step 0.5 before engaging the execution loop.
If engaged, abort and post STATUS to the bus. Do not start execution.

Engage Jarvis economy-gated autonomy as the outer loop:
- Credits gate autonomy level (Level 0 bounded → Level 3 full)
- Earn credits by completing tasks correctly; lose credits for failures
- Heartbeat protocol: check events, work queue, pursue goal, post SITREP

Within the outer loop, use:
- `/swarm-subagent` for parallel lanes (profile="subagent_general", free tier)
- `/cross-runtime-bridge` to delegate heavy work to opencode
- `/crab-loop` for bounded iteration within the run
- `/loop` for watch/retry/converge sub-tasks

**Subagent policy:** ALL `run_subagent` dispatches use `profile="subagent_general"`.
Persona goes in the task prompt, not the profile. No exceptions without
operator approval.

### Phase 4: Quality gate — `/report-card` (mandatory)
After each work unit, before promotion:
- `/report-card` — self-audit claims against actual tool output (mandatory)
- `/alignment-check` — verify outputs align with stated goals (detect drift)
- `/claim-verify` — for research outputs (extract claims, verify vs sources)
- `/hallucination-check` — for synthesis outputs (cross-ref vs source docs)
- `/hummbl-change-review` — for code changes (defect-first, repository doctrine)
- `/mtsmu-review` — for code/config changes (bug-first, severity-ranked)

No output promotes without passing the quality gate. If the gate fails,
route back to Phase 3 with specific remediation.

### Phase 5: Classify — `/trichotomy-route`
Route each output to the correct tier:
- `_internal/` — fleet-only (most autonomous outputs)
- `_between/` — partner/client-facing
- `_external/` — public

If anything will leave the fleet, `/admission-gate` is mandatory — it
hard-fails on local paths, machine names, Tailscale/SSH identifiers,
secrets, bus paths. Produces machine-readable receipt + human audit summary.

### Phase 6: Promote
By output type:

| Type | Skill | Destination |
|------|-------|-------------|
| code | `/commit` → `/ship` or `/auto-ship` | merge worktree branch to main |
| research | `/research-ingest` | CLP + evidence docs + Open Brain |
| governance | `/evidence-pack` | shareable audit artifacts |
| intelligence | `/intel-ingest` | all ingestion surfaces |
| open-source | `/oss-graduation` | public PyPI |

### Phase 7: Close — `/thoth`
Harvest session artifacts, CRAB-reconcile commits vs bus posts, distill
patterns into MEMORY.md, post structured HANDOFF. The HANDOFF is the next
session's boot context — this is what makes 4× 3h sessions function as
one 12h run.

### Phase 8: Observe (parallel, not blocking)
Operator observation runs alongside the pipeline, not in sequence:
- `/watch-session` — live monitoring across bus, git, filesystem
- `/dashboard-tui` — fleet TUI (agents, bus stream, tasks, governance)
- Post-run: `/session-forensics-batch` + `/cross-session-learnings`

## Multi-session continuity

Sessions >4h are reaped by `devin-reap-stale.sh`. Long runs are multi-session:

```
Session 1: seshat → select → execute → quality-gate → thoth (HANDOFF)
Session 2: seshat (reads HANDOFF) → select → execute → quality-gate → thoth (HANDOFF)
Session 3: seshat (reads HANDOFF) → select → execute → quality-gate → promote → thoth (HANDOFF)
```

Each session starts with seshat reading the previous thoth HANDOFF. The
HANDOFF chain is the cross-session memory. Without it, session 2 starts
cold and repeats or contradicts session 1.

## Known constraints

| Constraint | Mitigation |
|------------|------------|
| Sessions >4h reaped | Multi-session with thoth HANDOFFs |
| Subagent profile policy | All dispatches use `subagent_general` (free) |
| Sandbox network filtering unstable | Use `sandbox.excluded` for specific commands, not domain allowlists |
| Sandbox writes confined to workspace + granted scopes | Workspace IS the escape hatch — use a git worktree |
| `goal-cycle --auto --forever` requires operator present | Use `jarvis` or `autoresearch-mode` for unattended loops |
| `mission-declare` requires operator ACK | Operator must declare; agent cannot self-declare |
| Sandbox requires `bwrap` + `socat` on Linux | Verify installation before starting |

## Output Format

```
Longrun | <mission> | <type> | <duration>h
═══════════════════════════════════════════

Workspace: <worktree path>
Mission ID: <msn-xxxx>
Sessions: <N>

## Phases
| # | Phase | Skill | Status | Output |
|---|-------|-------|--------|--------|
| 1 | Open | seshat | DONE | state declaration |
| 2 | Select | goal-selection | DONE | 1 goal, acceptance criteria |
| 3 | Execute | jarvis + swarm-subagent | DONE | N work units |
| 4 | Quality | report-card | PASS | grade: B+ |
| 5 | Classify | trichotomy-route | DONE | _internal/ |
| 6 | Promote | commit → ship | DONE | PR #NNN |
| 7 | Close | thoth | DONE | HANDOFF posted |
| 8 | Observe | watch-session | ACTIVE | live monitor |

## Artifacts
- Worktree branch: <branch-name>
- Commits: <N>
- Bus posts: <N>
- Ledger entries: <N>
- HANDOFF: <timestamp>

## Next session
<one line from thoth HANDOFF>
```

## Skill Chains

### Mandatory

- **[MANDATORY]** `/mission-declare` with operator ACK before any work begins
- **[MANDATORY]** `/self-discovery` at session start to verify sandbox envelope
- **[MANDATORY]** `/report-card` before any output promotes (quality gate)
- **[MANDATORY]** `/thoth` at session close (HANDOFF for next session)

### Advisory

- After `/longrun` completes → `/session-forensics-batch` (post-hoc audit)
- After `/longrun` completes → `/cross-session-learnings` (compound across runs)
- If output leaves fleet → `/admission-gate` (mandatory before external publish)
- If multi-session → `/seshat` opens each new session reading prior HANDOFF

## Authority

- **T1 (TRUSTED)**: May run with operator ACK on mission declaration
- **T2 (Active/High)**: May run with operator ACK on mission declaration
- **T3 (Medium)**: Operator approval required (mission + workspace + promotion path)
- **T4 (Probationary)**: BLOCKED — cannot invoke (requires autonomous sandbox execution)
- **Operator**: Override any restriction; operator declares the mission

## References

- [references/architecture.md](references/architecture.md) — full pipeline architecture, decision matrix, and startup script template
