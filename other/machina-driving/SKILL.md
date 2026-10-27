---
name: machina-driving
description: >-
  Drive a Machina state machine to a deterministic outcome on behalf of an AI
  agent. USE WHEN: a task is governed by a state machine (a machine definition
  JSON with states, transitions, guards, actions, tools, checks, scenarios);
  executing a workflow that must be deterministic and auditable; running a
  skill whose SKILL.md declares a `machina:` machine; firing events, checking
  status, satisfying evidence checks, verifying run integrity with `check`, or
  producing a terminal report for a machine-driven run; escalating a STUCK run
  to a human conductor. DO NOT USE FOR: authoring or scoring machine definitions
  (use machina-authoring); modifying the Machina simulator app or its engine
  (use machina-simulator); implementing or modifying the driver/runtime tooling
  such as `scripts/machine-driver.py` (engine development) unless you are a
  maintainer of this skill upgrading the driver itself; general diagramming or
  XState/SCXML authoring.
metadata:
  version: 0.5.2
---

# Machina Driving

Execute a task under a Machina state machine: the driver (`scripts/machine-driver.py`)
is the sole mutator of run state; you perform the real work, choose events, and
satisfy evidence checks. The outcome is a deterministic, auditable report.

## Run History Convention

All machina run history must be stored in:
  `<session-workspace>/machina-runs/<run-id>/`

This convention ensures:
- Consistent traceability across sessions
- Easy discovery of run artifacts
- Standardized audit trail

The `--run-dir` parameter should point to `machina-runs/` under the session workspace.
The driver defaults to `machina-runs/` (resolving via `COPILOT_DOJO` or `~/.copilot-dojo` env vars for the session workspace root; falls back to `<cwd>/machina-runs/`).

## Quick start

From the skill directory (or any workspace with this skill installed):

```python
python3 scripts/machine-driver.py init --machine <machine.json> --scenario <id> --input k=v
python3 scripts/machine-driver.py status --run <run_id>
python3 scripts/machine-driver.py fire <EVENT> --run <run_id> --note "what you did"
python3 scripts/machine-driver.py check --run <run_id>
python3 scripts/machine-driver.py report --run <run_id>
```

Every command prints exactly one strict-JSON object. A blocked `fire` is a first-class outcome, not an error.

## Workflow

1. **Discover** the governing machine — read the relevant skill's `SKILL.md`
   frontmatter (`machina: { machine, scenario }`), or use the machine file the
   human conductor names.
2. **Init** the run with all required scenario inputs.
3. **Open the simulator canvas** — immediately after `init`, attempt
   `open_canvas` per [Simulator canvas integration](#simulator-canvas-integration)
   so the human conductor watches the run live. If the `open_canvas` tool does
   not exist in this runtime, say so in one line and continue — never retry.
4. **Work the current state** — the state's `description` tells you what the
   state demands. Do real work before firing events.
5. **Check status** — `status` shows enabled vs blocked events and why.
6. **Fire** events with a `--note`; iterate on `blocked` outcomes by fixing the
   underlying condition (guard or evidence), never by forcing the machine.
7. **Verify integrity** — `check` re-runs the full ledger + artifact-hash
   verification and returns `{ok:true}` only when the run is intact.
8. **Report** at terminal — ground your final summary to the report facts.

## Simulator canvas integration

When the `machina-simulator` Copilot extension is installed, the driving skill
auto-opens its interactive canvas so the human conductor can visually observe
the state machine being driven in real time.

### Open on init

After a successful `init`, open the simulator canvas:

```
open_canvas(canvasId: "machine-simulator", input: {
  runRef: "<run-id>",
  sessionWorkspace: "<session-folder>"
})
```

- `runRef`: the run ID returned by `init` (the directory name under `machina-runs/`).
- `sessionWorkspace`: the agent's current session folder (from the system prompt,
  e.g. `~/.copilot/session-state/<uuid>`). This scopes run-history discovery to
  the current session so the canvas shows only this session's runs.

The canvas enters **replay mode**, loading `machine.json` + `ledger.jsonl` from
the persisted run and displaying the state graph, compliance score, and ledger
trace.

### Refresh on fire

After each successful `fire`, **re-open** the canvas with the same `runRef` +
`sessionWorkspace` to refresh the replay with the updated ledger. The canvas
open handler is idempotent — it re-reads the ledger and broadcasts a `load`
SSE event to the browser, so the conductor sees the latest state without
manual intervention.

### STUCK / escalation

When the run enters `STUCK` or `ESCALATED`, the canvas is already showing the
stuck state and blocked events. No extra canvas action is needed — the
grounded report to the human conductor is the escalation channel.

### Graceful fallback (three tiers)

1. **`open_canvas` unavailable** (e.g. VS Code / Agent-Host SDK runtimes
   without canvas tools): **auto-start the standalone simulator** instead of
   giving up — run `node "<extension>/scripts/start-standalone.mjs"` where
   `<extension>` is the installed machina-simulator folder
   (`~/.copilot/extensions/machina-simulator`; the workspace copy's
   `scripts/start-standalone.mjs` works too). The launcher is idempotent: if
   a simulator already listens on `127.0.0.1:7750` it exits 0 with
   "already running" — treat both outcomes as success. Then emit **one line**
   for the human conductor:
   `machina-simulator ready at http://127.0.0.1:7750/ — open it to watch this run (runRef <run-id>)`
   and continue driving; the conductor browses Runs/Live tabs manually.
2. **Start failed** (no shell, no node, script missing): emit **one line** —
   `simulator unavailable (open_canvas absent, standalone start failed); continuing without it` —
   then continue the run.
3. **Never retry, never treat as an error.** The simulator is a convenience,
   not a requirement.

## Tamper prevention

The driver makes accidental or silent tampering fail closed. Four mechanisms
(v0.3.0):

1. **Ledger hash chain** — `ledger.jsonl` records chain via `prev_hash`/`hash`;
   any insert, remove, or reorder is detected on every command.
2. **Artifact-hash binding** — `init` pins the run's machine definition
   (`machine_sha256`) and every referenced tool/checker script (`tool_hashes`)
   in the init record; `status` / `fire` / `check` / `report` recompute them and
   fail closed on mismatch. A mid-run edit to `machine.json` or a checker script
   is a ledger integrity violation.
3. **Repo-worktree run-dir refusal** — `init` refuses to create a run dir
   inside a git worktree (only overridable via `MACHINA_ALLOW_REPO_RUNS=1`), so
   run state cannot silently land in something you might commit.
4. **Report bound to the ledger** — `report.json` carries `ledger_final_hash`
   (the last ledger record's hash), so a report can be traced to the exact
   ledger state it was generated from.

**Honest ceiling:** this is *detect-and-fail-closed*, not cryptographic proof.
The driver verifies hashes it derives from the same run directory, so an
attacker who can rewrite all of it (including the init record) is not stopped —
there is no OS-level read-only and no HMAC by design. The guarantee is that any
edit to the definition copy, a checker script, or the ledger is *detected* and
the run refuses to continue.

## Hard rules

- **INV-1**: never hand-edit a machine's state, context, history, or logs. The
  driver is the only writer; the ledger is tamper-evident.
- **INV-2**: never inline code into machine JSON. Tools are named references to
  scripts the driver executes.
- **Never run runs from inside a repo**: `init` refuses repo-worktree run dirs
  (override with `MACHINA_ALLOW_REPO_RUNS=1`); run state stays session-scoped.
- **Post-init context immutability**: after `init`, only machine actions and
  tool-output mappings mutate context. Your `--note` never touches context.
- **STUCK is not a crash**: a non-final state with zero enabled events is a
  modeling gap. Report it to the human conductor; never improvise a transition
  or fabricate completion.
- **Ground your summary to the report**: render only report facts
  (`result`, `final_state`, `path`, `events`, `evidence`, `context_snapshot`).

## References (load on demand)

| File | Load when |
|---|---|
| [references/driving-protocol.md](references/driving-protocol.md) | Any driving task — the full protocol: command surface, driving loop, evidence, phase states, STUCK/escalation, report grounding, discovery |
| [references/schema-v3.md](references/schema-v3.md) | Reading or writing machine JSON — v3 field reference, tools registry, checks/requires/ensures, inputs, limits, phase states |

## Dependency

This skill **depends on** [`machina-authoring`](../machina-authoring/SKILL.md):
`scripts/machine-driver.py` imports the shared engine (guard/action evaluation,
terminal detection, compliance scoring) from `machina-authoring/scripts/machine-validator.py`.
Distributing this skill to a workspace **implicitly distributes `machina-authoring`**.
The [`machina-simulator`](../../.copilot/extensions/machina-simulator) Copilot
extension is **auto-invoked** when installed — the driving skill opens its
canvas on `init` for live visual observability. When absent, the skill degrades
gracefully (no canvas, run continues normally).

For precision: the driver consumes the engine's **blocking validation**
(`run_compliance(...)["blocking"]`) as the structural gate and executes the machine's declared
tool scripts itself. It does **not** consume the authoring compliance *score* — see
[machina-authoring's Compliance boundary](../machina-authoring/SKILL.md). "Excellent" is a
declaration-quality signal; runtime soundness is established only by actually running the tools.

## Samples

- [samples/docs-authoring.machine.json](samples/docs-authoring.machine.json) — a
  v3 machine with tools, checks, requires, inputs, and a phase state.
- [samples/scripts/check_file.py](samples/scripts/check_file.py) — a read-only
  checker script referenced by the sample machine.

## Trust boundary

The driver executes referenced checker scripts with the user's privileges.
Machines are trusted artifacts (authored by the user or by `machina-authoring`).
No sandboxing in v1.

Corollary of the [compliance boundary](../machina-authoring/SKILL.md): a machine can be declared
"Excellent" yet fail at runtime if its tool scripts are missing, incorrect, or hostile — the
driver is what establishes runtime behavior by executing the declared read-only checkers, which is
exactly why they must exist and stay read-only.

## Hook hardening (defense-in-depth)

Three agent hooks provide lifecycle-based enforcement that augments the driver's internal tamper prevention. These hooks are **advisory-to-mandatory** depending on the event type and fill gaps where the driver's prompt-level instructions are insufficient.

| Hook | Event | Enforcement | Gap filled |
|---|---|---|---|
| `machina-ensures-runner` | `postToolUse` | `modifiedResult` (mandatory data) | `ensures[]` post-conditions declared in schema but not enforced by driver |
| `machina-event-gate` | `postToolUse` | `modifiedResult` (mandatory data) | `status` shows events "enabled" when evidence checks would block them |
| `machina-summary-guard` | `agentStop` | `decision:"block"` (forced turn) | Agent can fabricate summary contradicting `report.json` |

**How they work:**

- **Fire guard**: After a `fire` command, runs `transition.ensures[]` tools and
  appends pass/fail results to the tool output. The agent sees post-condition
  failures as part of the fire result.
- **Status enhancer**: After a `status` command, cross-references
  `enabled_events` against `state.checks[]` and replaces the output with
  accurate categorization (truly enabled vs checks-failed vs checks-pending).
- **Report validator**: Before session ends, compares the last assistant message
  against `report.json` facts. If contradictions are found, forces another turn
  to correct the summary (capped at 8 consecutive blocks).

**Deployment:** These hooks live in `hooks/machina-*/` and are published to
`.github/hooks/` via `publish-hooks.ps1`. They activate automatically when the
agent uses the machina-driving skill.

## Report output contract

Your final user-facing summary is a **grounded report** that renders only facts
from the terminal `report` output. It is not prose — each field must trace to a
`machina.report.v1` field.

| Report field | Required content | Source (`report`) field |
|---|---|---|
| `result` | `SUCCESS` · `ESCALATED` · `ABORTED` · `STUCK` · `IN_PROGRESS` | `result` |
| `final_state` | the final state id | `final_state` |
| `path` | the visited state sequence | `path` |
| `events` | count + comma-separated event names | `events`, `agent_notes[].event` |
| `evidence` | `passed N / failed M` | `evidence.passed`, `evidence.failed` |
| `blocked_events` | only when present | `blocked_events` |
| `context_snapshot` | only when it affects the outcome | `context_snapshot` |

Rules:

- Keep it under ~80 words; one paragraph per report.
- **Never invent claims beyond the report.** If `result` is `STUCK`, say
  `STUCK` — do not claim success.
- On `STUCK` or `ESCALATED`, head the summary as a **grounded escalation**:
  state the blocked events, the evidence failures, and the decision the human
  conductor must make. Never improvise a transition or fabricate completion.
- On `ABORTED`, render the abort reason from the report.
- If the driver emitted a strict-JSON `machina.report.v1` object, that object is
  the report — do not paraphrase it into different fields.

## Resources

- `scripts/` — `machine-driver.py` implements the `init` / `status` / `fire` /
  `abort` / `check` / `report` command surface. Execute it directly; do not load
  into context.
- `references/` — `driving-protocol.md` (the driving loop, evidence, STUCK,
  report grounding, tamper prevention) and `schema-v3.md` (machine JSON v3
  reference). Load on demand per the table above.
- `samples/` — `docs-authoring.machine.json` and its `scripts/` checkers for a
  worked example of a driven run.
