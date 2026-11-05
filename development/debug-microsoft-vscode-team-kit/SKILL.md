---
name: debug
description: "Debug runtime-dependent bugs by generating competing hypotheses, adding temporary structured-log probes, collecting local evidence, and applying only an evidence-backed fix. Use for intermittent or timing-sensitive bugs, races, frontend/backend interaction failures, runtime-state issues, repeated speculative-fix failures, or explicit requests to instrument and collect evidence. Not for breakpoints, stepping, or variable inspection."
compatibility: "Requires a structured question tool, Node.js with native .mts type stripping, persistent SQL tooling, retained background processes, resumable human turns, and IPv4 connectivity from each instrumented process to the collector."
---

# Debug

Run an evidence-driven debugging session with temporary structured probes. Use `dap-cli` instead for breakpoints, stepping, stacks, or variable inspection.

## Scope

Use for runtime-state, intermittent, timing-sensitive, race, cross-process, or repeatedly misdiagnosed bugs. Do not use for syntax/type errors, an obvious deterministic unit-test failure, ordinary code review, or permanent application logging.

## Invariants

1. Collect runtime evidence before changing production logic.
2. Carry at least two active hypotheses with distinct failure modes and disproof conditions into instrumentation.
3. Missing evidence never proves a hypothesis. Negative inference requires a valid reproduction, demonstrated execution opportunity, complete collection, and the planned observation window.
4. Probe only bounded values needed to distinguish hypotheses. Never collect secrets, credentials, full environment maps, full bodies, or unnecessary personal/user-generated data.
5. Probe failure must not alter application control flow.
6. Every inserted block requires an exact session marker and one physical-ownership `debug_probes` row before reproduction.
7. One orchestrator owns SQL writes, source edits, stage transitions, user gates, and cleanup. Advisors are read-only.
8. Remote ingestion requires explicit approval and a trusted development network. Administration always remains loopback-only.
9. Do not remove probes before human verification. A session is incomplete until owned probes/configuration are removed and collector shutdown is acknowledged.
10. Never store sensitive event payloads in SQL, and never leave probe code or debug-only configuration behind.

## Security Stance

This skill runs on the developer's own machine, against their own code and data, at their request. Calibrate caution to that: the risks worth spending effort on are leaving instrumentation behind, capturing data that outlives the session, and extending trust beyond the local host.

What genuinely matters:

1. **Probe code must not survive the session.** Debug code that reaches a commit, a build artifact, or a colleague's checkout is the most likely real harm. Marker ownership and Stage 7 cleanup exist for this.
2. **Probe payloads must stay bounded.** Events persist to disk in the collector and summaries persist in the ledger, so a probe that captures secrets, credentials, tokens, or personal data creates a durable copy that outlives the investigation. Invariant 4 governs this.
3. **Leaving loopback is a real trust boundary.** Remote ingestion is unauthenticated-in-transit HTTP on a shared network, so it requires approval and a trusted network. Administration stays loopback-only.
4. **Instrumentation must not change program behavior.** Probe failure stays outside control flow.

What does not warrant ceremony: the collector's ingest token is an ephemeral per-session value that only prevents other local processes from posting junk into this collector. It grants no access to the developer's accounts, repository, or machine, and it dies with the collector. Treat it as a nuisance-prevention value rather than a credential. Avoid printing it gratuitously and keep it out of anything durable, but do not build elaborate handling around it. The admin token is held to a higher bar only because it can read collected events and stop the collector.

Apply the same proportionality elsewhere: prefer the simplest delivery and cleanup that satisfies the four points above.

## Runtime Contract

Resolve the directory containing this file and the plugin root as `../..`. Invoke scripts by absolute path.

| Resource | Purpose |
|---|---|
| `skills/debug/schema.sql` | Canonical SQLite schema and enforcement triggers |
| `scripts/log-server.mts` | Start the retained collector |
| `scripts/debug-server-status.mts --config <path>` | Authenticated health and unverified PID diagnostics |
| `scripts/read-session-events.mts --config <path>` | Read one bounded event page |
| `scripts/stop-log-server.mts --config <path>` | Authenticated graceful shutdown |

Collector options are `--port <0-65535>`, `--session-directory <new-path>`, `--allow-remote`, and `--advertise-host <hostname-or-IPv4>`. Never reuse a session directory before authenticated status and shutdown.

## Investigation Ledger

Use the host's persistent session SQL database. Never create a ledger file inside the application repository. If only file-backed SQLite is available, place it in host session state or the OS temporary directory, record its absolute path in the active plan/session context, and reuse it on every turn. If neither persistent SQL nor resumable session state is available, report the incompatibility and stop.

Initialize once by executing `schema.sql` exactly. If the SQL tool cannot execute a file, read the file once and submit it as one batch. Every SQL invocation or connection must enable `PRAGMA foreign_keys = ON`. Require `debug_meta.schema_version = '1'`; do not add compatibility paths for unreleased schemas.

The tables have these responsibilities:

| Table | Responsibility |
|---|---|
| `debug_sessions` | Investigation identity and overall state |
| `debug_rounds` | Enforced round transitions and outcomes |
| `debug_hypotheses` | Round-scoped theories and classifications |
| `debug_probes` | One row per physical marker block for cleanup |
| `debug_probe_rounds` | Round-specific use of a physical probe |
| `debug_evidence`, `debug_snapshots` | Collector-qualified events and immutable ranges |
| `debug_decisions`, `debug_validations` | Decisions, gates, tests, and verification |
| `debug_cleanup` | Cleanup actions and outcomes |

Every query must include the current investigation `session_id`. Allocate numeric IDs monotonically within that investigation. Store only bounded derived summaries.

### Resume before creating

At the start of every turn, including the first, query:

```sql
SELECT session_id, status, collector_config_path
FROM debug_sessions
WHERE status NOT IN ('resolved', 'aborted', 'failed')
ORDER BY updated_at DESC;
```

- If one row belongs to the current workspace/problem, adopt it. Do not generate a new ID. If it has a collector config, run authenticated status before continuing.
- If multiple rows could match, ask via the question tool which investigation to resume, with one choice per candidate `session_id` plus `Start a new investigation`.
- Otherwise create one `debug_sessions` row with status `describing`.

Retain the ledger as investigation history unless host session retention removes it. It is not an application artifact and must never appear in the application diff.

### State model

| Round state | Entry requirement | Next |
|---|---|---|
| `planning` | New round; hypotheses recorded | `authorized` or abort |
| `authorized` | Breadth/risk gate passed | `awaiting_reproduction` |
| `awaiting_reproduction` | Probes and ownership recorded | `analyzing`, repeat, or abort |
| `analyzing` | Reproduction response and event read recorded | repeat same round or `closed` |
| `closed` | Complete snapshot or abort | fix, next round, direction, or cleanup |

The schema enforces legal transitions, hypothesis breadth, evidence-bearing closure, and closed-round immutability. Use exact validation values `kind = 'reproduction'`, `result = 'reproduced'` for a successful reproduction.

## Interaction Policy

Every human gate is one structured question-tool call carrying a single focused question, followed by a full stop. Use choices when the answer set is known; otherwise accept a free-form response rather than guessing exhaustive choices. If the tool requires choices, include the best-known choices and an explicit free-form option. Never continue past a gate before the answer arrives, and do not ask merely to restate supplied information. If no structured question tool is available, report the incompatibility and stop.

Human input is required only for:

- material ambiguity;
- remote exposure or high-risk instrumentation;
- reproduction;
- final verification;
- direction after two inconclusive rounds;
- abort and ambiguous cleanup.

Low-risk same-host probes are authorized by the debugging request once recorded. Plan approval authorizes instrumentation only; it never satisfies reproduction or verification.

In plan mode, keep Stages 1–2 free of source edits, collector startup, and probes. If SQL writes are permitted, initialize and record normally. If writes are blocked, put the framing, hypotheses, probe plan, topology, and risk in the plan artifact; after approval, backfill the session, planning round, hypotheses, and decision as the first Stage 3 action before authorization or instrumentation.

## Independent Advice

Use read-only advisors only when they improve breadth or interpretation:

- disjoint subsystem exploration for broad bugs;
- 2–3 independent hypothesis proposals for complex ambiguity;
- one contrarian probe-plan review when fewer than three plausible candidates survive, timing is sensitive, subsystems cross boundaries, or this is a retry;
- hypothesis-specific analysis against the same immutable snapshot;
- one fix critique for non-trivial or high-blast-radius changes.

Advisors never edit, write SQL, operate the collector, ask user questions, declare root cause, or clean up. Agreement is not evidence.

## Stage 1: Describe

Capture symptom, expected/actual behavior, reproduction, affected subsystem, and timing characteristics. If concrete, record the framing and assumptions without confirmation. Ask via the question tool only when a missing detail materially changes scope, privacy, risk, or reproduction; offer choices only when the plausible answer set is known.

Set the session to `hypothesizing`, then inspect relevant code. Parallelize only genuinely disjoint read-only exploration.

## Stage 2: Hypothesize and Authorize

Create the round in `planning`. Consider 3–5 plausible theories without filler; carry at least two distinct active failure modes.

For each hypothesis record:

```text
H1 — <theory>
Failure mode: <causal class>
Confidence: low | medium | high
Static support: <specific code evidence>
Expected signal: <observation if true>
Would disprove: <observation>
Probe plan: <location and bounded values>
```

Record statically excluded candidates as inactive with a specific citation; exclusions never waive the two-active floor.

Plan shared discriminating probes where possible. For each physical marker use a stable `probe_id`; for each round use a new round-qualified event label such as `R2-H1H3-P1-before-save`. Record expected volume and observer effect in `debug_probe_rounds`. A carried probe keeps its single physical `debug_probes` row, but its owned block is updated to emit the new round-qualified label and receives a new `debug_probe_rounds` row. Never duplicate physical ownership rows.

Authorize after the schema breadth trigger passes. Probe coverage is checked in Stage 3 after the authorized round's `debug_probe_rounds` rows exist.

A plan is low-risk same-host only when all probes use loopback, tier 1 or tier 2 configuration delivery, bounded permitted values, no dependency/new file/persistent configuration/behavior change, failure outside control flow, and no sensitive or materially timing-changing boundary. Record automatic authorization. Otherwise obtain explicit approval by asking via the question tool with these choices:

```text
Approve the probe plan
Adjust the probe plan
Abort and clean up
```

For remote mode state in the question the intended target and that ingestion is unencrypted trusted-network HTTP.

## Stage 3: Start and Instrument

Start same-host collection:

```sh
node <plugin>/scripts/log-server.mts
```

For approved non-local probes:

```sh
node <plugin>/scripts/log-server.mts --allow-remote \
  --advertise-host <target-reachable-host>
```

Require `RESULT: DEBUG_SERVER_READY`, then verify `RESULT: DEBUG_SERVER_RUNNING` using the status script. Select an unambiguous topology-matching ingest URL automatically; only when multiple plausible non-loopback candidates remain, ask via the question tool with one choice per candidate URL. `0.0.0.0` is never an ingest URL.

The config contains separate ingest/admin tokens. Give probes only the selected ingest URL, collector session ID, and ingest token; never give a probe the admin token, and do not print either token when avoidable.

Choose the lowest tier the target supports:

| Tier | Delivery | Use when |
|---|---|---|
| 1 | Environment variables set by the launch command | The target reads `process.env` and you launch it |
| 2 | Literals inside the owned marker block | The target cannot read the environment (sandboxed renderer, worker, browser page) |
| 3 | Runtime injection of configuration into an already-running process | The target already loaded the owned probe block through hot reload or an equivalent mechanism and cannot be relaunched |

Record the chosen tier per probe in `debug_decisions` before reproduction; Stage 7 reads those rows to determine its obligations. Never write a token value into a ledger row.

### Tier 1: environment

Read the token into the child environment as part of the launch command. On POSIX:

```sh
DEBUG_URL=<ingest-url> DEBUG_SESSION_ID=<collector-id> \
DEBUG_INGEST_TOKEN="$(node -e \
  'const fs=require("node:fs");const c=JSON.parse(fs.readFileSync(process.argv[1],"utf8"));process.stdout.write(c.ingestToken)' \
  <config-path>)" <application-command>
```

On Windows, set the variables in the debug launch script by reading the JSON through Node or PowerShell.

### Tier 2: inline literals

Write the ingest URL, collector session ID, and token as literals inside the owned marker block. Permitted when:

- the ingest URL is loopback;
- the values appear only inside that block, so ordinary cleanup removes them;
- the file is not published, deployed, or committed automatically by a watcher or hook.

Never stage or commit a block containing the token. Because the values live inside the marker block, Stage 7's existing marker search already covers them; no separate token hunt is required.

### Tier 3: runtime injection

Injecting into a process this investigation did not launch requires the Stage 2 approval gate, because the target's state is not fully known. Inject configuration only, never probe logic: the probe body stays in source inside its marker block so ordinary ownership and cleanup still apply, which means the target must already be running that block. Record the injection channel, the target process identity, and the exact injected identifier in `debug_decisions`, and clear it in Stage 7 with a `debug_cleanup` action.

Record active collector identity in `debug_sessions`. Before reproduction:

1. Insert one `debug_probes` row per physical marker and one `debug_probe_rounds` row per current-round use.
2. For carried probes, update only the contents inside the same owned marker block.
3. Use paired markers:

   ```text
   [debug:<collector-session-id>:probe:<probe-id>:start]
   [debug:<collector-session-id>:probe:<probe-id>:end]
   ```

4. Keep instrumentation-only imports inside the owned block.
5. Estimate aggregate event volume; narrow or sample if it could approach capacity or materially affect timing.
6. Verify every active hypothesis is covered:

```sql
SELECT h.hypothesis_id
FROM debug_hypotheses AS h
WHERE h.session_id = '<id>' AND h.round = <round> AND h.active = 1
AND NOT EXISTS (
  SELECT 1
  FROM debug_probe_rounds AS p, json_each(p.hypothesis_ids) AS mapped
  WHERE p.session_id = h.session_id
    AND p.round = h.round
    AND mapped.value = h.hypothesis_id
);
```

This must return no rows.

Canonical event:

```json
{
  "schemaVersion": 1,
  "sessionId": "<collector-session-id>",
  "kind": "probe",
  "label": "R1-H1H2-P1-before-save",
  "timestamp": "<ISO-8601>",
  "location": {"file": "src/save.ts", "function": "save"},
  "hypothesisIds": ["H1", "H2"],
  "data": {"state": "pending", "retryCount": 2}
}
```

Send with `Authorization: Bearer <DEBUG_INGEST_TOKEN>` and JSON content type. Bound every request to approximately 250 ms (`AbortSignal.timeout(250)` for Node fetch; `timeout=0.25` for Python) and keep rejection/failure handling outside application control flow. Do not use synchronous probes in timing-sensitive critical sections.

Frontend probes are permitted through tier 2 or tier 3 against a loopback collector, which handles browser preflights only for event ingestion. Never point a frontend probe at a non-loopback collector, and never leave the ingest token in code that ships, deploys, or is committed.

For non-local targets, require a target-originated `lifecycle` event labeled `debug-connectivity-check`, observe it locally, and record a `preflight` validation before reproduction. Store the event once in `debug_evidence`, but exclude it from hypothesis classification and snapshot `event_count`.

If startup fails after creating a session directory, the script must remove only the directory it created. For an existing configured collector, run status and authenticated shutdown. If unreachable with a live recorded PID, report identity as unverified and require manual inspection; never emit a kill command.

## Stage 4: Reproduce

Set session and round to `awaiting_reproduction`, then ask via the question tool with these choices and stop:

```text
Reproduced
Could not reproduce — adjust
Abort and clean up
```

Include only required launch/restart instructions. Reuse a preflight-launched target unless restart is part of reproduction. Record the response in `debug_validations`.

A `Could not reproduce — adjust` response stays in the same round. If the needed correction is still unclear, ask one focused free-form question through the question tool and stop; do not record another reproduction result until the user attempts reproduction again.

A failed/invalid reproduction, collection failure, observer effect, or reproduction-step correction stays in the same round. Any probe-plan change returns that round to `authorized` before editing instrumentation; reapprove only material or newly high-risk changes. Material means a new subsystem/file/data category, meaningful volume/timing increase, topology/exposure/dependency/configuration/security change.

## Stage 5: Read and Analyze

Read pages of at most 100 events:

```sh
node <plugin>/scripts/read-session-events.mts \
  --config <config-path> --offset <offset> --limit 100
```

Freeze the first response's total and paginate only through that bound. `DEBUG_EVENT_CAPACITY_REACHED`, `DEBUG_EVENT_STORAGE_FAILED`, or non-zero rejected/storage counts make the collector evidence incomplete. Do not classify it. Record an incomplete diagnostic snapshot only if useful; never close an evidence-bearing round with it.

Persist each event once using collector ID plus sequence. Materialize a snapshot with inclusive `min_sequence`/`max_sequence`, event count, completeness, rejected count, and storage-failure count. Cite multi-collector evidence as `<collector-id>:<sequence>`.

Classify each active hypothesis:

| Classification | Meaning |
|---|---|
| `supported` | Predicted signal observed |
| `weakened` | Counter-evidence lowers confidence |
| `falsified` | Complete observation satisfies the disproof condition |
| `inconclusive` | Path ran, but evidence does not discriminate |
| `not_exercised` | No demonstrated execution opportunity |

No pre-fix classification establishes causality. Causal confidence requires successful intervention and human verification.

Check actual volume for each round-qualified label within the snapshot range:

```sql
SELECT p.probe_id, p.estimated_max_events, COUNT(e.sequence) AS actual_events
FROM debug_probe_rounds AS p
LEFT JOIN debug_evidence AS e
  ON e.session_id = p.session_id
  AND e.collector_session_id = '<collector-id>'
  AND e.label = p.event_label
  AND e.sequence BETWEEN <min-sequence> AND <max-sequence>
WHERE p.session_id = '<id>' AND p.round = <round>
GROUP BY p.probe_id, p.estimated_max_events
HAVING COUNT(e.sequence) > p.estimated_max_events;
```

Close as `evidence_sufficient` before fixing, or as `inconclusive` only with a successful reproduction validation and complete snapshot. Collection/capacity/storage failures and `not_exercised` do not consume a round.

Start a new round only when the prior round closed `inconclusive` and the next plan changes theories or discrimination. Preserve prior rows and use `supersedes_round` for revised theories. One retry round may proceed automatically through normal risk classification.

After two closed inconclusive rounds, set the session to `awaiting_direction` and ask via the question tool with these choices:

```text
Broaden to another subsystem
Add the suggested higher-cost probe
Switch to DAP-based debugging
Abort and clean up
```

Collector replacement stays in the same round. Shut down and remove only the verified old collector directory, start a fresh collector, update active collector identity while retaining physical marker ownership, update the carried probe blocks/configuration, then return through reproduction.

## Stage 6: Targeted Fix

Set status `fixing`. Record the proposed smallest fix with supporting snapshot and collector-qualified sequences, then edit production logic. Avoid speculative refactors. Keep probes active and run the smallest existing automated tests covering the change; record results.

## Stage 7: Verify and Clean Up

Set status `awaiting_verification`, then ask via the question tool with these choices and stop:

```text
Resolved
Issue persists
Unable to verify — keep open
Abort and clean up
```

Automated tests, silence, plan approval, and advisor agreement never satisfy verification. If the issue persists, return to analysis/fixing or Stage 2 when theories/probes must change.

After resolution or abort, clean up in this order while continuing independent actions whose ownership remains unambiguous:

1. Set status `cleaning_up`; select every physical `debug_probes` row for this investigation.
2. Verify exactly one ordered start/end pair at each recorded path and marker.
3. On missing, duplicate, reordered, or drifted ownership, emit `CLEANUP_FAILED`, leave that probe `active`, and do not edit its block.
4. Remove each validated block once; set its probe status to `removed`.
5. Remove a file only when `file_created = 1`, every probe for it belongs to this investigation, every block verified and was removed, and the complete file is session-owned.
6. Search all recorded files for every distinct `debug:<marker_session_id>:` prefix, even when an earlier action failed. Any match is `CLEANUP_FAILED`. This also covers inlined tier 2 values, which live inside those blocks.
7. If any tier 3 injection was recorded, clear each injected identifier from the target process, or note that a restart will clear it.
8. Remove debug-only configuration.
9. Stop the active collector with the shutdown script and require `DEBUG_SERVER_STOPPED`.
10. After acknowledged collector shutdown, delete only the resolved directory containing the recorded collector config. A `debug-<id>` name is supporting evidence, not a requirement for explicit `--session-directory` paths.
11. Inspect the final application diff for residue and unrelated changes.

Record every cleanup failure and continue with independent verified actions; never mutate an artifact whose ownership is ambiguous. After all safe actions have been attempted, keep the session incomplete, set it to `failed`, and make one question-tool call that identifies each unresolved absolute path and marker, with the choices `Leave the remaining artifacts untouched` and `Wait for manual resolution`.

Record each action in `debug_cleanup`. Set `resolved` only after successful human verification and complete cleanup; otherwise use `aborted` or `failed`.

## Result Handling

| Result | Action |
|---|---|
| `DEBUG_SERVER_READY`, `DEBUG_SERVER_RUNNING` | Verify identity, then instrument |
| `DEBUG_EVENTS_READ` | Materialize the bounded snapshot |
| `DEBUG_EVENT_CAPACITY_REACHED`, `DEBUG_EVENT_STORAGE_FAILED` | Evidence incomplete; repair/restart and reproduce |
| `DEBUG_SERVER_STOPPED` | Continue artifact cleanup |
| `DEBUG_SERVER_ALREADY_STOPPED`, `DEBUG_SERVER_UNREACHABLE` | Report unverified state/PID; inspect identity manually |
| `DEBUG_STATUS_ERROR`, `DEBUG_SERVER_ERROR` | Do not instrument |
| `DEBUG_READ_ERROR` | Do not analyze |
| `DEBUG_SHUTDOWN_ERROR`, `CLEANUP_FAILED` | Session remains incomplete |

No success-shaped fallback is allowed.
