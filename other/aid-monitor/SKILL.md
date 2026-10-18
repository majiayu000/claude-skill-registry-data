---
name: aid-monitor
description: >
  Watch production, classify what you find, and route it to whoever should act. Use this
  skill after a deployment, on a schedule, or whenever something looks wrong in the field.
  It reads telemetry, detects anomalies, performs root-cause analysis on the ones that are
  bugs, and then routes: bugs to `/aid-fix`, change requests to `/aid-triage`. Scoped to one
  work at a time.
allowed-tools: Read Glob Grep Bash Shell Terminal Write
---

# Observe, Classify, Act

State machine: OBSERVE → CLASSIFY → ROUTE → DONE.

Monitor production. Detect what's wrong. Route it to where it gets fixed.

## Agents Involved

- **Default executor:** `aid-orchestrator` (routes findings; never implements directly).
- **Telemetry interpretation:** `aid-researcher` (reads logs/metrics, classifies anomalies).
- **Routing targets:**
  - BUG → `/aid-fix` (creates + implements the fix work).
  - Change Request → `/aid-triage` (routes to the right entry).
  - Infrastructure → escalated to ops (outside AID scope).

## Argument-Hint

```
/aid-monitor work-NNN
/aid-monitor "<free-form description of what to observe>"
```

**Two invocation modes** (invocation-context detection; see `## ⚠️ Pre-flight Checks`
Step 0):

- **`work-NNN` present** -- the existing pipeline path below runs unchanged
  (`OBSERVE -> CLASSIFY -> ROUTE -> DONE`, post-deployment). Required: work ID. If only
  one work exists, auto-select it.

  Optional flags (this mode only):
  - `--since "YYYY-MM-DD"` — observation window start (default: last deploy or last monitor run)
  - `--package package-NNN` — scope to a specific deployment package

- **No `work-NNN`, a free-form description instead** -- the Lite-path direct-entry
  shortcut: binds `{name}=aid-monitor`, `{verb}=monitor`, `{artifact}=""` (bare verb),
  `{description}=<the given text>`, then delegates to the shared shortcut engine
  (`.aid/runtime/templates/shortcut-engine.md`, `INTAKE -> ... -> APPROVAL-HALT`),
  scaffolding a flattened Lite work and running the grading gates. **Never executes** --
  it halts for approval; this shortcut entry does not replace the pipeline role below,
  it adds a second, independent entry point to the same skill directory.

## Workspace

```
.aid/works/{work}/
  packages/                    ← deployment history
  features/                    ← SPECs (expected behavior)
  deliveries/delivery-NNN/tasks/task-NNN/  ← full path: task files (acceptance criteria)
  tasks/task-NNN/                          ← lite path: task files (acceptance criteria; no delivery-NNN/ nesting)
  known-issues.md              ← known problems
```

<!-- NOTE: The Monitor area STATE is deferred until the area matures. When authored, MONITOR-STATE.md follows the area-STATE pattern documented at .aid/runtime/templates/work-state-template.yml (per-work) and .aid/knowledge/schemas.md §1A. -->

## ⚠️ Pre-flight Checks

### Step 0: Invocation-context mode detection

- **`work-NNN` argument present** → proceed with Steps 1–6 below (the existing
  pipeline path; untouched).
- **No `work-NNN` argument, but a free-form description was given instead** → the
  shortcut-scaffold path (see `## Argument-Hint` above): bind `{name}=aid-monitor`,
  `{verb}=monitor`, `{artifact}=""`, `{description}=<the given text>`, then delegate
  directly to `.aid/runtime/templates/shortcut-engine.md § State: INTAKE` — Steps 1–6
  below do not run for this path (that pre-flight belongs to the post-deployment
  pipeline role, not the shortcut entry).
- **Neither `work-NNN` nor a description** → print the `## Argument-Hint` usage block
  and exit.

1. Verify `.aid/` workspace exists.
2. Resolve work directory.
3. Read or create the in-memory monitor context (observation log, finding statuses):
   ```
   Last Run: {never}
   Window: {start} → {end}
   Findings: 0
   Active Findings: {none}
   Resolved Findings: {none}
   ```
4. Read `PLAN.md` — understand deliveries and what was shipped.
5. Read `packages/` — what's deployed and when.
6. Read `known-issues.md` — filter out already-known problems.

## State Detection

Determine the current entry state from context:
- No prior run context → **OBSERVE** state (pull telemetry; see `references/state-observe.md`)
- Active findings present → **CLASSIFY** state (classify and analyze; see `references/state-classify.md`)
- All findings classified → **ROUTE** state (propose and act; see `references/state-route.md`)
- All findings resolved → **DONE**

Print the state-entry line and "you are here" map:

**OBSERVE:**
```
[State: OBSERVE] — Pulling telemetry signals and correlating against baselines.
aid-monitor  ▸ you are here
  [● OBSERVE ] → [ CLASSIFY ] → [ ROUTE ] → [ DONE ]
```

**CLASSIFY:**
```
[State: CLASSIFY] — Classifying each anomaly as BUG, CHANGE REQUEST, INFRASTRUCTURE, or NO ACTION.
aid-monitor  ▸ you are here
  [✓ OBSERVE ] → [● CLASSIFY ] → [ ROUTE ] → [ DONE ]
```

**ROUTE:**
```
[State: ROUTE] — Proposing and executing routing actions per finding classification.
aid-monitor  ▸ you are here
  [✓ OBSERVE ] → [✓ CLASSIFY ] → [● ROUTE ] → [ DONE ]
```

**DONE:**
```
[State: DONE] — All findings routed; monitor cycle complete.
aid-monitor  ▸ you are here
  [✓ OBSERVE ] → [✓ CLASSIFY ] → [✓ ROUTE ] → [● DONE ]
```

## Severity Thresholds

| Signal | Threshold | Classification |
|--------|-----------|----------------|
| New error type | Any | Finding |
| Error rate increase | >200% baseline | Finding |
| Performance degradation | >50% latency | Finding |
| Persistent test failure | Any new | Finding |
| Support ticket cluster | 3+ same issue | Finding |
| Below all thresholds | — | Clean report, no findings |

## Inputs

**From the project (what to observe):**
Any combination of: error tracking (Sentry, AppInsights, CloudWatch), CI/CD results,
APM/performance metrics, test trends, user feedback, support tickets, log files.

**From AID artifacts (what's expected):**
- Feature specifications (`.aid/works/{work}/REQUIREMENTS.md § 11`) — expected behavior
- Per-task `DETAIL.md` — acceptance criteria; full path: `.aid/works/{work}/deliveries/delivery-NNN/tasks/task-NNN/DETAIL.md`; lite path: `.aid/works/{work}/tasks/task-NNN/DETAIL.md`
- Package files — what was deployed and when
- `known-issues.md` — exclude known problems

**From KB (context):**
Read `.aid/knowledge/INDEX.md`, pull relevant docs (typically architecture, module-map,
infrastructure, test-landscape) for baseline context and root cause analysis.

## Dispatch Protocol (L1+L2+L3 subagent visibility)

Every subagent dispatch in this skill MUST follow this protocol so the user
sees mid-wait progress instead of going silent for 10–25+ minutes. The full
protocol lives in two reference docs; this section is a checklist citing them.

**Before each dispatch:**

1. **Look up ETA** in `.aid/runtime/templates/rough-time-hints.md` for the
   subagent's operation class. Capture LOW–HIGH band.
2. **Read heartbeat config** via
   `bash .aid/runtime/scripts/config/read-setting.sh --path traceability.heartbeat_interval --default 1`
   (resolves from `.aid/settings.yml`; default 1; `0` = disabled).
3. **Pre-create heartbeat file** (always — unconditional):
   - Pre-create `.aid/.heartbeat/<agent-name>-<unix-ts>.txt`
   - Include `HEARTBEAT_FILE=<path>` + `HEARTBEAT_INTERVAL=Nm` in dispatch prompt with explicit instruction to update during long phases
   - SKIP only if `traceability.heartbeat_interval: 0` (user-explicit opt-out in `.aid/settings.yml`)
4. **Arm 3 L2 timers** (always — even for short ETAs use minimums 60s/120s/180s; never gate on ETA):
   - `sleep <min(LOW/2, 270) in s> && echo "... <agent> still running (Xm elapsed of ~LOW–HIGH)"`
   - `sleep <min(LOW, 540) in s> && echo "... <agent> at estimated time (LOWm elapsed)"`
   - `sleep <min(1.5×LOW, 810) in s> && echo "⚠️ <agent> EXCEEDED estimate (1.5×LOWm elapsed); consider checking on it or cancelling"`
   - **Keep-warm re-arm:** when the last timer fires and the sub-agent is still running, arm one more `sleep 270 && echo "... <agent> still running (Xm elapsed)"`, and again on each fire, until the completion notification arrives. Every fire is a request that re-reads the cached context and refreshes its 5-minute prompt-cache TTL; a silent gap over 5 minutes re-writes the whole context at full price.

**During dispatch:**

- **On L2 timer fire:** surface the timer output. If heartbeat file exists,
  also read it and append `[from heartbeat] state: <state> · progress: <progress>
  · activity: <activity>` to the narration.

**On completion / failure:**

- **Success:** emit `✓ <agent> done in <actual>` with measured time. When the dispatch is
  for a real `task-NNN`, append a `dispatch_log` entry to that task's own state (full
  path: its `STATE.yml`; flat path: `tasks_lifecycle.task-NNN.dispatch_log`) with
  fields `date`/`agent`/`eta_band`/`actual`/`outcome` -- the work-level Calibration
  Log / Dispatches views are derived at read time from these entries
  (`work-state-template.yml`); there is no work-level section to write. When the
  dispatch is NOT task-scoped, there is no persisted
  target at all -- the console narration above is the sole record. Mandatory
  wherever a target exists (never optional, never "if tracked"). Delete heartbeat file.
- **Failure:** emit `✗ <agent> FAILED after <elapsed> (reason: <one-line>)`.
  Decide whether to re-dispatch, fall back, or surface to user. Delete
  heartbeat file.

**References:**

- `.aid/runtime/templates/long-wait-protocol.md` — full L2 spec
- `.aid/runtime/templates/subagent-heartbeat-protocol.md` — full L3 spec
- `.aid/runtime/templates/rough-time-hints.md` — current measured ETAs
- `aid-*` agent definitions, `## Heartbeat protocol` section — subagent-side contract

The existing `▶ <agent> starting (~<ETA>)` and `✓ <agent> done` bracket-pair
lines elsewhere in this skill body remain in place; this protocol just makes
them more informative by adding mid-wait check-ins + structured progress.

## Dispatch

| State | Detail | Worker | Advance |
|-------|--------|--------|---------|
| OBSERVE | `references/state-observe.md` | `aid-researcher` | → CLASSIFY |
| CLASSIFY | `references/state-classify.md` | `aid-researcher` | → ROUTE |
| ROUTE | `references/state-route.md` | `aid-orchestrator` | → DONE |
| DONE | _(inline — see Re-run below)_ | `inline` | → halt |

On state entry, print `[State: NAME]` + the "you are here" map from State Detection above.
When a state completes, route by its `**Advance:**` type (per [`state-machine-chaining.md`](../../aid/templates/state-machine-chaining.md)):
- **CHAIN** → begin the next state's reference doc within the same invocation; no exit.
- **PAUSE-FOR-USER-ACTION** / **PAUSE-FOR-USER-DECISION** → print the pause reason + resume command and exit.
- **HALT** → print the closing summary and exit.

## Re-run

When prior findings exist (from conversation context or referenced findings list):

```
[State: RE-RUN] — Prior findings on record; confirming whether to run fresh or review a finding.
aid-monitor  ▸ you are here
  [✓ OBSERVE ] → [✓ CLASSIFY ] → [✓ ROUTE ] → [✓ DONE ] → [● RE-RUN ]
```

1. Show active findings and their current status.
2. Show observation history (last runs).
3. Ask: **[1] New observation** (fresh run) or **[2] Review finding-N** (check if resolved)?
4. If [1] → re-enter the OBSERVE state with a new window (previous run end → now); router exits and user re-invokes `/aid-monitor`.
5. If [2] → Re-check evidence for that specific finding, update status.

## Quality Checklist

- [ ] All configured data sources checked
- [ ] Observation window clearly defined
- [ ] Each finding has concrete evidence (not speculation)
- [ ] Classification references feature SPECs
- [ ] Bug vs CR distinction explicit and justified
- [ ] For bugs: root cause identified (one sentence, specific)
- [ ] For bugs: patch scope defined (minimal — fix, don't refactor)
- [ ] For bugs: test requirements defined
- [ ] Severity with expected response time
- [ ] Routing decision clear for each finding
- [ ] Known issues filtered out (no duplicate findings)
- [ ] Correlations with deployments noted
- [ ] Monitor run summary printed with all findings and statuses
- [ ] KB docs consulted via INDEX.md (not hardcoded)
