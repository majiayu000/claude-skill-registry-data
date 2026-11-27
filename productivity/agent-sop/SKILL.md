---
name: sop
description: A human-gated, capability-slotted collaboration workflow. Use when a task needs proportionate research, planning, implementation, independent review, verification, signoff documents, or safe deployment.
compatibility: Roster-agnostic — collaborating agents are discovered at task start via scripts/discover-roster.py, never hardcoded. A pane-based control plane (e.g. Herdr) is recommended for multi-agent work. Designed for shared hosts where agents and production services coexist.
---

# SOP — Agent Collaboration Workflow

**First principle — Agent-first.** Every skill we build or publish, this one included, is operated by agents, not hand-configured by humans. Anyone using a skill has at least one agent, so the skill must guide that agent to do its own onboarding: detect the environment, ask the human only for decisions (never for mechanical setup), and write any required configuration, roster, or paths itself. A skill step that requires a human to edit files by hand is a design bug. Humans own decisions, approvals, and signoffs — agents own everything else.

Use this skill as the local operating procedure. For high-risk work, it provides the full auditable sequence:

research → plan → human approval → implementation → independent review → verification → signoff packet → human signoff → deploy

Lower-risk work uses the lighter workflow in §1.1. The skill is deliberately conservative. It is not permission to change production services, expose ports, restart shared units, or modify private data without an explicit user decision.

## 0. Capability slots and roster discovery

- **Human**: owns scope, accepts trade-offs, signs documents, and approves destructive or operational actions.
- **orchestrator**: classifies the task, assigns slots, enforces gates, and synthesizes artifacts and reports.
- **sole-writer**: is the only agent allowed to edit the declared repository, worktree, or production configuration during a phase.
- **reviewer**: uses an independent read-only session to test requirements and evidence; it never approves its own writing.
- **scout**: performs bounded read-only exploration, research, or monitoring and returns evidence.
- **monitor**: tracks long-running background work (≥2 min) via artifact-file checks, pane status, and logs; identifies stalls and reports progress to the human. Usually carried by the orchestrator; see §5.1.

Assign agents to capability slots at task start; do not encode agent names into the slot definitions. Record at least:

`orchestrator=<agent> sole-writer=<agent|none> reviewer=<agent|none> scout=<agent|none> monitor=<agent|none> writer=<agent|none> repo=<path>`

The roster is **discovered, not declared** — this skill never names specific agents or models. At task start the orchestrator (the agent the human is currently addressing) runs `python3 <skill>/scripts/discover-roster.py --probe --out <task-dir>/roster.json`, assigns slots to the healthy agents **by condition, never by name** (sole-writer = highest-capability agent with write access; reviewer = highest-capability agent from a different vendor, degrading per the ladder in `references/roster-protocol.md`; scouts = cheapest fast-tier), then presents a 3–6 line roster proposal for the human to veto or approve before slotted work begins. Silence is not approval. Full rules, tie-breaks, and the roster.json schema: `references/roster-protocol.md`.

A pane-based multiplexer, when present (e.g. Herdr; commands as of herdr 0.9 — run `herdr --help` if your version differs), is the control plane, not a capability slot. Name panes `<task-slug>:<slot>:<writer|ro>`, keep the pane label synchronized with the recorded writer, use explicit pane IDs and `--no-focus` for background work, wait for agent state with `herdr agent wait <pane_id> --until <idle|working|blocked|done> [--timeout MS]` or for matching output with `herdr pane wait-output <pane_id> --match <text>` instead of polling, and close panes after their results are captured.

Authorization is set at launch, not per command. A sub-agent dispatched into a background pane cannot stall on interactive approval prompts — no human is watching that pane. So the orchestrator must launch each background agent in a mode that auto-approves every in-scope routine action (reads, local tests, edits within the assigned repo, binding scoped localhost test ports) instead of prompting per command. Otherwise the agent blocks and the pipeline hangs. Per-tool launch recipes are not listed here — they live in each agent's `background_recipe` field in roster.json, maintained in the discovery script's probe list. An agent whose `background_recipe` is `null` must not be dispatched to a background pane until a working unattended launch mode is established and added to the script. This does NOT weaken gates: a per-command approval popup is the wrong instrument for a gate — it is too weak (the writer just clicks yes and publishes) and too noisy (it also blocks trivial reads). Gates (publish, deploy, restart production, data writes, visibility changes) are enforced by the task instruction plus the orchestrator splitting the work at each gate (see §5), not by the agent's own approval prompts. Grant broad in-scope autonomy; withhold the gated action itself.

Exactly one agent may write a given worktree or production configuration at a time. Reviewers are read-only by default.

## 1. Intake and safety gate

Before research or editing:

1. Restate the request in one sentence.
2. Identify the target repository, service, database, and sensitive data involved.
3. Read applicable `AGENTS.md`, project README, and the host's operational map when services are involved.
4. Run and record `git status --short --branch` for every repository that may change. The host may contain intentional dirty operational work; do not assume a clean baseline.
5. Record a baseline of changed paths and relevant service/database hashes when the task is safety-sensitive.
6. Classify the task as read-only, tiny reversible, medium, or data/service/destructive, then select the workflow weight in §1.1.

Stop and ask the human before proceeding when requirements are ambiguous, a production database may change, a public route/port may change, a secret must be handled, or a service restart is needed and was not explicitly approved.

### 1.1 Workflow weight

| Task tier | Qualifying boundary | Required workflow |
| --- | --- | --- |
| Read-only / tiny reversible | No data, service, public route/API, security boundary, credential, or destructive effect; rollback is immediate and scope is small | Execute directly, verify proportionately, then provide an after-action report. No advance plan, approval gate, or independent review is required unless ambiguity triggers the safety stop above. |
| Medium | Reversible multi-file or behavior change with meaningful integration risk, but no production data/service/destructive action | Written plan → explicit human approval → assigned sole-writer implementation → independent review → verification → final report. Use a signoff packet only when a distinct human decision needs durable evidence. |
| Data / service / destructive | Any production data write or migration, service/config/deploy/restart, public exposure change, irreversible action, or high-impact security/privacy change | Use the full workflow: research as needed → plan → explicit per-action approval → sole-writer implementation → independent review → verification → Markdown signoff packet → human signoff → deployment under §7.1. |

When uncertain, choose the heavier tier. A task cannot be downgraded merely because its code diff is small.

## 2. Research mode

Use research mode when facts, architecture, or external libraries are not yet understood.

Parallelize only independent read-only tasks. Typical roles:

- `scout`: map local files, entry points, data flow, and current conventions.
- `researcher`: gather official documentation and source evidence.
- `risk-reviewer`: look for security, privacy, concurrency, rollback, and operational hazards.

Every research result must contain:

- a short conclusion;
- evidence paths or URLs;
- assumptions and unknowns;
- implications for our current workflow;
- no code edits.

Do not treat an agent's guess or a user's correction as fact until it is checked against code, data, or authoritative documentation.

## 3. Plan mode

Create a plan before medium or large changes. The plan must be a Markdown artifact, normally under:

`<workflows-dir>/plans/YYYY-MM-DD-<slug>.md`

(Pick one stable `<workflows-dir>` per machine or project — e.g. `./workflows/` in the project, or a shared data directory — and keep using it. Agents create it if missing; the human is never asked to.)

A plan contains:

- objective and out-of-scope items;
- current-state evidence;
- chosen design and rejected alternatives;
- files, services, databases, and APIs affected;
- small independently verifiable phases;
- tests before implementation tasks;
- build, runtime, functional, security, and rollback checks;
- data migration and concurrency rules;
- signoff criteria;
- explicit human decisions still required.

Do not write `TBD` into a plan. Resolve uncertainty through research or ask the human before the plan is final.

## 4. Human approval gate

Present the plan and wait for explicit approval before implementation. Approval must identify the plan or task; silence is not approval.

For a production/service task, approval must separately cover:

- data writes or migrations;
- service restarts;
- nginx, firewall, port, certificate, or tunnel changes;
- handling of private credentials;
- deployment or rollback.

## 5. Implementation mode

Implementation follows the approved phases. Before editing, place `writer=<agent> repo=<path>` in the task record and, when a pane-based control plane is in use, mirror it in the pane label.

- The assigned `sole-writer` is the only writer for the phase.
- The assigned `orchestrator` may coordinate and collect results but must not make a second overlapping edit.
- Use an isolated worktree for parallel implementation; otherwise execute phases serially in the main worktree.
- Keep changes minimal and reversible.
- Never put secrets, tokens, private URLs, or raw personal data into Git, plans, screenshots, or chat.
- Preserve immutable source data. Where a project declares deterministic scripts as the owners of imports and database writes, LLMs only propose relationships or decisions, always with provenance — they never write those stores directly.
- Before service changes, inspect active connections and logs, make a backup when appropriate, test configuration, then restart only after approval.

Gated steps are never self-served. If a plan step is conditioned on a human approval or a reviewer PASS (deploys, publishes, restarts, data writes), the sole-writer must stop before it and hand control back to the orchestrator — even if its task instruction said to "execute all phases". The orchestrator, when dispatching work, must split instructions at every gate: assign only the phases up to the next gate, run the gate itself, then dispatch the rest. A writer performing a gated step on its own initiative is a violation regardless of outcome.

Test claims require evidence. A phase report saying "tests passed" is treated as unverified unless it includes the actual commands and captured output (or a committed evidence file). Reviewers and orchestrators must re-run or spot-check security-relevant tests rather than trust the writer's summary.

Each phase returns:

`STATUS: PASS | NEEDS_CHANGES | BLOCKED`

`FILES: <changed paths>`

`TESTS: <commands and results>`

`RISKS: <remaining risks or none>`

`NEXT: <next phase or human decision>`

## 5.1 Monitor mode

Background agent tasks that run longer than 2 minutes must be actively monitored. **The orchestrator must not sit idle waiting.** This is the mechanism that prevents "the task finished long ago while the coordinator was still blocked on a wait".

### What to monitor

- Agents running in background panes (sole-writer / scout / reviewer)
- Long-running work: batch generation, large downloads, slow test suites, multi-round generation

### Monitoring methods (in priority order)

1. **Artifact-file check (preferred)**: tasks usually write files (output mp4/png/json/md). Check the output directory periodically (every 60–120 seconds):
   ```bash
   ls -lat <output-dir>/ | head        # new or updated files
   find <output-dir> -mmin -2 -type f  # files changed in the last 2 minutes
   ```
   Growing files = the task is progressing. Stalled files = possibly stuck; investigate.
2. **Pane status query**:
   ```bash
   herdr agent get <pane_id>   # status transitions idle→working→done
   ```
   `done` = finished, `blocked` = needs input, `working` = in progress.
3. **Log tail**: progress markers in the agent's output (e.g. `Shot 0X done`):
   ```bash
   herdr pane read <pane_id> --source recent-unwrapped --lines 20
   ```
4. **Process check**: confirm the agent process's CPU / run time (`ps aux | grep <agent>`).

### Cadence

- Short tasks (<2 minutes): a single `herdr agent wait <pane_id> --until idle --until done` is enough.
- Long tasks (>2 minutes): **check artifact files every 60–120 seconds** instead of idling on a wait.
- Record every check as: `<time> <artifact count/size change> <status>`, and report it to the human.

### Stall detection

- **Output stalled**: no change in the output directory for 3+ minutes while the agent status is `working` → possibly stuck; inspect the logs.
- **Blocked**: the agent needs input/approval → handle it immediately or report it.
- **Repeated failure**: the same error appears 2+ times → stop retrying and report to the orchestrator to change approach.

### Monitor slot

The monitor is usually carried by the orchestrator; for large workloads a separate monitor may be assigned. Monitoring is not passive observation — the monitor is responsible for identifying stalls, reporting promptly, and recommending adjustments when needed.

## 6. Independent review mode

Review must be performed in a new, independent, read-only session. The reviewer receives the approved plan, baseline, changed paths, and test evidence; it must not rely on the implementer's summary. Budget context and cost by task tier. If any working session exceeds 60% context, first persist its evidence, current status, assumptions, and next action in the task artifact, then continue in a fresh session rather than carrying an oversized chat history.

Review in this order:

1. requirement and plan coverage;
2. correctness and edge cases;
3. integration and ownership boundaries;
4. security and privacy;
5. concurrency, locking, rollback, and operability;
6. simplicity and cleanup;
7. tests and documentation.

Use two complementary reviews when appropriate:

- **implementation review**: requirement-to-evidence traceability; identify missing or overbuilt work;
- **code review**: architecture, patterns, errors, security, tests, and maintainability.

A reviewer may recommend changes, but does not silently edit the writer's worktree. The writer applies fixes, then the reviewer re-checks. A review is not complete until blocking findings are resolved or explicitly accepted by the human.

Every review returns this reusable contract:

`VERDICT: PASS | NEEDS_CHANGES | BLOCKED`

`BLOCKING: <required fixes with paths/lines, or none>`

`SUGGESTED: <non-blocking improvements, or none>`

`EVIDENCE: <files, lines, commands, logs, or URLs checked>`

## 7. Verification mode

Choose the smallest evidence that proves the risk is controlled, then run it:

- static/syntax/lint/type checks;
- unit or focused tests;
- API or browser smoke tests;
- service health and logs;
- database row counts, schema checks, lock checks, and before/after hashes;
- rollback or dry-run checks for operational changes.

Record commands, timestamps, and outcomes in the task artifact. A passing test suite does not prove that a production service was safely restarted.

## 7.1 Deployment mode

Deployment is a separate operational phase, not an automatic consequence of passing tests. Perform it in this order:

1. create and verify an appropriate backup, and record the restore path;
2. run the relevant configuration or preflight test;
3. obtain the separate action approvals required by §4;
4. deploy and restart only the approved components;
5. run a service/API/UI health check;
6. inspect startup and application logs for errors;
7. report the actual result, timestamp, changed components, and remaining risks.

If any step fails, stop further rollout, preserve the failure evidence, and use the documented rollback path. After rollback, repeat the health and log checks and report the failure and rollback honestly.

## 8. Signoff packet mode

When the human needs to approve research, a design, a deployment, or a decision, create a signoff packet rather than burying it in chat.

Store packets under:

`<workflows-dir>/signoff/`

Version 1 packets are Markdown (`.md`) only. HTML packets and previews remain disabled until a rendering UI exists with both a sandboxed iframe and an isolated origin. The packet must include:

- title and status (`pending`, `approved`, `changes_requested`, or `rejected`);
- date and task/plan reference;
- executive summary;
- evidence and source links;
- decision options and recommendation;
- implementation impact;
- risks, rollback, and open decisions;
- reviewer and verification results;
- a clear list of decisions requested from the human.

Packets go to a private decision inbox owned by the human; the inbox and its records stay private. Any public export must use an explicit whitelist and may include only deliberately publishable content; signoff packets and signoff records are never public exports. Store signoff data separately from production databases. Version 1 renders Markdown only; defer dedicated inbox UI work until 3–5 real packets have accumulated and justified the interface.

Agents may initialize status only as `pending`. Only the human may authorize a transition to `approved`, `changes_requested`, or `rejected`; if an agent mechanically records that transition, it must quote the human's signoff statement verbatim in the packet's signoff record. Agents must never invent, paraphrase, or infer a human decision. Do not treat a document as approved merely because it exists or was viewed.

## 9. Final report

At completion, report:

- what changed and what did not;
- files and commits;
- tests and operational checks;
- signoff status;
- residual risks and rollback path;
- follow-up work.

If a task is blocked, report the exact blocker and the smallest decision or credential needed. Never hide a blocked external dependency behind a fake success.

## Default workflow prompts

Research:

> Use `sop` research mode. Do a read-only scout, official-source research, and risk review. Return evidence paths/URLs, assumptions, and implications. Do not edit files.

Plan:

> Use `sop` plan mode. Convert the verified research into small phases with tests before implementation, rollback, security checks, and explicit human approval points. Write the plan artifact and wait for approval.

Implement:

> Use `sop` implementation mode. Implement only the approved phase as the sole writer. Run the phase checks and return the required STATUS/FILES/TESTS/RISKS/NEXT contract.

Review:

> Use `sop` independent review mode in a new read-only session. Read the plan, baseline, changed files, and evidence. Review requirements, correctness, security, concurrency, rollback, simplicity, tests, and docs. Do not edit; return VERDICT/BLOCKING/SUGGESTED/EVIDENCE with paths and line references.

Signoff:

> Use `sop` signoff mode. Turn the verified research or implementation result into a concise `.md` packet with evidence, risks, decisions requested, and status `pending`. Do not claim approval or write a human decision.
