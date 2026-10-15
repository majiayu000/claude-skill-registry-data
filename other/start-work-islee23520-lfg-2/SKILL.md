---
name: start-work
description: "Execute a Prometheus work plan in GrokBuild with `/goal` state, Boulder state, evidence ledger updates, worktree discipline, parallel subagents, and explicit continuation. Use after planning when the user says start work, execute plan, continue plan, resume plan, or asks to run a .omo/plans plan."
---

## GrokBuild Tool Mapping

On Grok Build with lfg installed, use `spawn_subagent` only for Grok host monitoring and read-only discovery. Product implementation goes through the external Codex app-server handoff. This contract is GrokBuild-only (`coding_tool_adapter` = `grok`).

| Intent | GrokBuild tool to use |
| --- | --- |
| Search/read-only worker | `spawn_subagent({ subagent_type: "explore" or "explorer", background: true, description: "...", prompt: "TASK: ..." })` |
| Planning worker | `spawn_subagent({ subagent_type: "plan", background: true, description: "...", prompt: "TASK: ..." })` |
| Product implementation | `lfg --json handoff plan --role coding --engine gpt --focus "..."` → Codex app-server; `codex exec` fallback only when daemon unavailable. |


### Product implementation handoff (GrokBuild)

Grok is the Sisyphus watcher, not the product implementer. For LOW, MEDIUM, or HIGH implementation bodies, create the external Codex work package with `lfg --json handoff plan --role coding --engine gpt --focus "..."`. The handoff creates or attaches the project Codex app-server thread; `codex exec` is fallback only when the daemon is unavailable. Use `spawn_subagent` only for Grok host work by `watcher`, `explorer`, or `git-master`; never spawn `lazycodex-worker-*`, `hephaestus`, or `coding` for the product body.
Before that handoff, consume the `lfg-gjc-intent-gateway` context: clarify high ambiguity and use `refined_focus` to tighten the Codex brief. gjc remains intent-only and fail-open; it never implements product code.
### External Codex implementation lane (GPT only)

**Grok = Sisyphus watcher**; **Codex app-server = sole product implementer**. Default product work is `lfg --json handoff plan --engine gpt` to Codex App.

Product implementation has exactly one worker lane: external Codex app-server handoff through `lfg --json handoff plan --engine gpt`. Grok may use watcher/explorer/git-master for host monitoring and read-only discovery, but must not spawn an in-host implementer for the product body.

1. Run `lfg --json handoff plan --role <role> --engine gpt --focus <focus>` and read `handoff.payloadMarkdown` plus the app-server transport receipt (`fullyTransferable`, `grokIsOrchestrator`).
2. Prefer the created/attached Codex app-server thread. Only when the daemon is unavailable, execute the reported `codex-exec-fallback` launch using `handoff.launch.argv[0]` with `handoff.launch.argv.slice(1)`; `handoff.launch.binary` is identity/readiness metadata. If `launch.stdinSource` is present, pipe that source exactly as described. Use **`timeout: 0`** and kill the process group on cancellation.
3. **Do not** hand off sisyphus/prometheus; **do not** spawn Grok hephaestus/coding/lazycodex-worker for the product body.
4. Read RESULT into Boulder/ledger.

In-host `spawn_subagent` remains only for Grok host monitoring/read-only roles.



## ABSOLUTE RULE: YOU ARE AN ORCHESTRATOR — NEVER THE IMPLEMENTER

**YOU DO NOT WRITE CODE. YOU DO NOT EDIT PRODUCT FILES. YOU DO NOT RUN QA YOURSELF. EVERY unit of implementation, test, QA, and review work MUST be delegated to a worker. NO EXCEPTIONS.** Your hands touch only plan selection, `.omo/` state (Boulder, ledger, plan checkboxes), decomposition, dispatch, verdicts, and evidence records. About to edit a product file or run an implementation command yourself? **STOP. DISPATCH THE SELECTED WORKER LANE INSTEAD.** Orchestrate at **MAXIMUM PARALLELISM**: every independent unit runs concurrently; only named dependencies serialize.

## Codex Harness Tool Compatibility

Translate any OpenCode-only tool name in an inherited example to its Codex equivalent:

| OpenCode example | Codex tool to use |
| --- | --- |
| final-review `task(...)` | `lfg --json handoff plan --role review --engine gpt --focus "..."`, then launch `handoff.launch.argv` exactly |
| worker `task(...)` | `multi_agent_v1.spawn_agent({"message":"TASK: act as <role>. ...","fork_context":false})` |
| `background_output(task_id="...")` | `multi_agent_v1.wait_agent(...)` for mailbox signals |
| `team_*(...)` | `multi_agent_v1.spawn_agent` + `multi_agent_v1.send_input` + `multi_agent_v1.wait_agent` + `multi_agent_v1.close_agent` |

When translating `load_skills=[...]`, name the skills inside the spawned agent's `message`. If a code block below conflicts with this section, this section wins.

Codex exposes ONE of two subagent tool surfaces per session; check your own tool list and route accordingly. If `multi_agent_v1.*` tools exist, use the table above as written. If instead a flat `spawn_agent` with a required `task_name` exists (`multi_agent_v2`), rewrite every `multi_agent_v1.*` example: `multi_agent_v1.spawn_agent({...,"fork_context":false})` becomes `spawn_agent({"task_name":"<lowercase_digits_underscores>","message":...,"agent_type":...,"fork_turns":"none"})` (`"all"` only when full parent history is truly required); `send_input` becomes `send_message`; do not call `close_agent`/`resume_agent` (finished agents end on their own; `followup_task` re-tasks one, `interrupt_agent` stops one); `wait_agent` takes only `timeout_ms` and returns on any child mailbox activity. `agent_type` works the same on both surfaces. If a code block below conflicts with this section, this section wins.

## Codex Subagent Reliability

Every `multi_agent_v1.spawn_agent` message is a self-contained executable assignment: `TASK: <imperative assignment>`, then `DELIVERABLE`, `SCOPE`, and `VERIFY`, with role instructions inside `message`. Use `fork_context: false` unless full history is truly required; paste only the context the child needs.

Plan and reviewer agents may run for a long time: spawn them in the background, keep doing independent root work, and poll with short `multi_agent_v1.wait_agent` cycles — never a single long blocking wait. A timeout only means no new mailbox update arrived; treat a running child as alive. Require `WORKING: <task> - <current phase>` before long passes and `BLOCKED: <reason>` only when progress stops. Keep the parent visibly alive with active subagent count, names, and latest `WORKING:` phase. Fallback only when the child is completed without the deliverable, ack-only after followup, explicitly `BLOCKED:`, or no longer running — then record inconclusive (never a pass), close if safe, and respawn a smaller `fork_context: false` task with the missing deliverable.

# start-work

## Grok execution boundary

Planning is a separate Codex lane: before approval, run `lfg --json plan ulw-plan --focus <objective>` so Codex loads skill `ulw-plan`, writes the decision-complete `.omo/` plan, and returns `the Codex App thread (optional receipt only if --result-path is set)` for Grok to present.

After approval, never execute implementation inside Grok. Build the implementation plan with `lfg --json plan start-work --plan <path> --focus <objective>` or use `lfg --json handoff plan --role coding --engine gpt --focus <objective>`. Prefer the Codex app-server transport. Use codex-exec fallback only when the daemon is unavailable; only then execute `handoff.launch.argv`. External Codex must invoke Codex `$start-work` and write `the Codex App thread (optional receipt only if --result-path is set)`. Grok only selects, monitors, and reads that receipt before changing Boulder state or reporting completion. The alias `lfg --json start-work launch` has the same planning contract.

## Grok execution boundary

Planning is a separate Codex lane: before approval, run `lfg --json plan ulw-plan --focus <objective>` so Codex loads skill `ulw-plan`, writes the decision-complete `.omo/` plan, and returns `the Codex App thread (optional receipt only if --result-path is set)` for Grok to present.

After approval, never execute implementation inside Grok. Build the implementation plan with `lfg --json plan start-work --plan <path> --focus <objective>` or use `lfg --json handoff plan --role coding --engine gpt --focus <objective>`. Prefer the Codex app-server transport. Use the reported codex-exec fallback only when the daemon is unavailable; only then execute `handoff.launch.argv`. External Codex must invoke Codex `$start-work` and write `the Codex App thread (optional receipt only if --result-path is set)`. Grok only selects, monitors, and reads that receipt before changing Boulder state or reporting completion. The alias `lfg --json start-work launch` has the same planning contract.

## Grok execution boundary

Never execute this workflow inside Grok. Build the dry-run launch with `lfg --json plan start-work --plan <path> --focus <objective>`, then launch the returned Codex argv. External Codex must invoke Codex `$start-work` and write `the Codex App thread (optional receipt only if --result-path is set)`. Grok only selects, monitors, and reads that receipt before changing Boulder state or reporting completion. The alias `lfg --json start-work launch` has the same planning contract.

Execute a Prometheus work plan until every top-level checkbox is complete. Use GrokBuild's `/goal` command as the host goal-state surface for the aggregate objective. The upstream Codex `Stop` / `SubagentStop` continuation hook (`components/start-work-continuation`) is not a GrokBuild runtime contract, so do not depend on automatic hook reinjection; preserve state in `.omo/boulder.json` and continue explicitly from that durable state.

## Usage

```text
/start-work [plan-name] [--worktree <absolute-path>]
```

- `plan-name` (optional): a full or partial file stem under `.omo/plans/`.
- `--worktree` (required for PR/branch work; otherwise optional): the task-owned git worktree path.

## Phase 1: Select the plan

0. Inspect GrokBuild `/goal` state. If no active goal exists, create one with `/goal <aggregate objective>` once the objective is known. If a different active goal exists, stop and surface the conflict instead of overwriting it.
1. Read `.omo/boulder.json` if it exists.
2. List Prometheus plan files under `.omo/plans/`.
3. If `plan-name` was provided, select the matching plan.
4. If exactly one active or paused Boulder work exists for this session, resume it.
5. If no active work exists and exactly one plan exists, select it.
6. If no active work exists and there is no selectable plan, enter **No-plan bootstrap**.
7. If multiple plans remain possible, ask one focused selection question.

### No-plan bootstrap

When the user explicitly said `start work` / `/start-work` and no selectable plan exists, treat that phrase as approval: bootstrap `ulw-plan` to create the approved plan before execution and implementation, instead of stalling or asking for generic approval again. A brief or notes file without waves, checkboxes, and acceptance criteria is NOT decision-complete — enter this bootstrap too.

1. Invoke the `ulw-plan` skill from the current request and require its dynamic adversarial workflow: collect, verify, design, adversarial plan-review, synthesize.
2. The generated Prometheus plan must be saved under `.omo/plans/<slug>.md` before implementation or Boulder state writes that point at plan work.
3. Use maximum safe parallelism in the generated plan: independent files/tasks fan out; same-file writes, shared state, and named dependencies serialize.
4. Preserve safety boundaries. Ask one focused question only when the objective is missing, destructive, or has a safety/product ambiguity that repository exploration cannot resolve.
5. After the plan exists, continue directly to Phase 2.

## Phase 2: Create or update Boulder state

Write `.omo/boulder.json` before implementation starts. Prefix session ids with `grok:` for GrokBuild-owned work; if resuming an older `codex:<session_id>` entry, preserve it as historical state but attach the current `grok:<session_id>` before continuing.

```json
{
  "schema_version": 2,
  "active_work_id": "<work-id>",
  "works": {
    "<work-id>": {
      "work_id": "<work-id>",
      "active_plan": ".omo/plans/<plan-name>.md",
      "plan_name": "<plan-name>",
      "session_ids": ["grok:<session_id>"],
      "status": "active",
      "worktree_path": null
    }
  }
}
```

For PR/branch work, `--worktree` is mandatory before implementation starts. Verify the path with `git worktree list --porcelain` or create it with `git worktree add <path> <branch-or-HEAD>`, then store the absolute path as `worktree_path`. All edits, commands, tests, and evidence capture must run inside that worktree.

## Phase 3: Execute the next checkbox

1. Read the full selected plan.
2. Find the first unchecked column-0 checkbox in `## TODOs` or `## Final Verification Wave`.
3. Ignore nested checkboxes under acceptance criteria, evidence, and definition-of-done sections.
4. Classify the checkbox tier and record it in its ledger entry. Default is LIGHT — a narrow change inside existing layers. Take HEAVY only on a fact you can point to: a new module / abstraction / domain model; auth, security, or session; an external integration; a DB schema or migration; concurrency or transaction boundaries; a cross-domain refactor; or the plan or user signals care. When unsure, take HEAVY; upgrade and redo skipped gates the moment a HEAVY fact surfaces; never downgrade.
5. Decompose that checkbox into atomic sub-tasks. Collect every other unchecked checkbox in the same plan wave whose dependencies are met — their lanes execute concurrently.
6. **DELEGATE EVERYTHING. YOU NEVER IMPLEMENT.** Dispatch ALL independent sub-tasks across those checkboxes in parallel through each task's already selected worker lane; serialize only named dependencies. Verification and checkbox marking stay per-checkbox.

Each sub-task message must include:

1. Goal and exact files or directories in scope.
2. When the task touches existing behavior: a baseline characterization test, written first, that pins current observable behavior and passes on the unchanged code (exact inputs, exact observable, exact assertion). Then the failing-first proof for the new behavior before production changes — a unit test where a seam exists, otherwise the sub-task's Manual-QA scenario captured failing. A test that mirrors its implementation (mock-call assertions, pinned constants) is not evidence.
3. Implementation constraints from the plan and project rules.
4. Automated verification commands to run.
5. One Manual-QA channel, named with the exact tool and exact invocation (the literal `curl`, `send-keys`, `browser:control-in-app-browser` action, `page.click`, payload, selectors, and the binary observable that decides PASS/FAIL), not "verify it works". A LIGHT checkbox needs one real-surface proof of its deliverable, and auxiliary surfaces (CLI stdout, DB state diff, parsed config dump) are first-class when the surface is CLI- or data-shaped:
   - HTTP call: `curl -i` against the live endpoint.
   - Terminal / TUI: drive a real pty; `tmux send-keys` is fine for a boot/behavior smoke, but color/layout/CJK evidence goes through the xterm.js web terminal below, NEVER `tmux capture-pane`.
   - Browser use: in Codex, use `browser:control-in-app-browser` first when available and the scenario does not need an authenticated or persistent user browser profile; otherwise drive the real page with Chrome, or agent-browser (https://github.com/vercel-labs/agent-browser) when Chrome is unavailable.
   - Computer use: OS-level GUI automation against the running desktop app when the surface is not a page.
   - TUI visual evidence: when a TUI claim needs visual QA or PR proof, run `node script/qa/web-terminal-visual-qa.mjs --command "<cmd>" --input "{Enter}" --evidence-dir <dir>` (real pty rendered through xterm.js in Chrome) and attach `terminal.png` plus `metadata.json`.
6. The adversarial classes that apply to this sub-task (from the 9 ultraqa classes) and how each is probed.
7. Required artifact path and cleanup receipt.

The 9 ultraqa classes are trigger-mapped: new input parsing → malformed input; untrusted external text → prompt injection; resumable or long-running flows → cancel/resume; generated or cached artifacts → stale state; uncommitted user files in scope → dirty worktree; long external commands → hung or long commands; new or timing-sensitive tests → flaky tests; log-based success claims → misleading success output; mid-operation interrupts → repeated interruptions. A class applies when its trigger fact holds. Probe each applicable class; record the rest as not-applicable with a one-line reason.

## Phase 4: Verify and record evidence

For each checkbox, complete all five gates before marking it done:

1. Plan reread: confirm the checkbox and acceptance criteria.
2. Automated verification: run tests, typecheck, lint, build, or the plan-specific equivalent.
3. Manual-QA channel: capture a real artifact, not a dry-run claim.
4. Adversarial QA: exercise every class the Phase 3 trigger map marks applicable and capture the observable result for each.
5. Cleanup: register every QA resource teardown as its own todo when spawned (QA scripts, tmux assets, browser sessions, PIDs, ports, containers, temp dirs), execute each, and capture the receipt. No QA asset is left running.

Append evidence to `.omo/start-work/ledger.jsonl`, one JSON object per line. Include at least `event`, `plan`, `task`, `session_id`, `commands`, `artifact`, `adversarial_classes`, and `cleanup` fields. `adversarial_classes` lists each probed class with its observable result and each ruled-out class with a one-line reason.

### Sisyphus-style completion contract

A worker done claim is never final: each implementation sub-task returns a `DoneClaim`, a different context runs `AdversarialVerify` probing or reproducing the claim, failures loop back to the executor, and only a confirmed verifier verdict becomes `FullyDone`.

```json
{
  "DoneClaim": {
    "task": "<task id/title>",
    "changed_files": ["path"],
    "tests": ["exact command + result"],
    "manual_qa": ["artifact path"],
    "cleanup": ["receipt"],
    "risks": ["known risk or none"]
  },
  "AdversarialVerify": {
    "verdict": "confirmed | false-positive | needs-fix | needs-human-review",
    "evidence": ["file path, command, log, artifact, or explicit not inspected"],
    "repro": "exact command or manual steps when available",
    "confidence": 0.0
  }
}
```

Rules:
- `confirmed` is the only pass verdict. `false-positive`, `needs-fix`, and `needs-human-review` all block checkbox completion.
- The verifier must be independent from the executor: create a separate external Codex review handoff, or use root only when root did not implement or materially rewrite that task.
- A worker done claim must be independently verified before it becomes checkbox completion.
- On any non-confirmed verdict, append the feedback to the ledger, reset the checkbox work to in-progress, and re-dispatch the executor with the exact failure.
- The verifier must probe the applicable adversarial keys, including `stale_state`, `dirty_worktree`, and `misleading_success_output`, before allowing `FullyDone`.

## Phase 5: Mark progress

Only after verification passes:

1. Edit the plan checkbox from `- [ ]` to `- [x]`.
2. Re-read the plan and confirm the remaining count decreased.
3. Append a `task-completed` ledger entry.
4. Continue with the next checkbox. Do not ask whether to continue.

## Completion

When all top-level checkboxes in `## TODOs` and `## Final Verification Wave` are complete:

1. Run the plan's final verification commands.
2. For PR/branch work, finish the lifecycle from the task-owned worktree: sync `.omo/` state back to the main repo, create or update the PR, wait for review/verification gates, merge by default unless explicitly opted out, and remove the worktree only after successful merge or explicit handoff.
3. Remove or mark the Boulder work as completed.
4. Print an `ORCHESTRATION COMPLETE` block with the plan path, verification commands, artifacts, and cleanup receipts.

## Hard rules

- No production change before a failing-first proof exists (unit test at a seam, otherwise the failing Manual-QA scenario), and no change to existing behavior before a baseline characterization test pins the current behavior and passes on the unchanged code.
- No `--dry-run` as completion evidence.
- No tests-only completion claim. A Manual-QA artifact is required.
- **NO DIRECT IMPLEMENTATION BY THE ORCHESTRATOR.** Root NEVER edits product files, writes tests, or runs QA itself — a delegated worker does.
- No completion claim while an applicable ultraqa adversarial class was never probed. Each applicable class needs a captured observable result; each skipped class needs a one-line not-applicable reason in the ledger.
- No PR/branch implementation, review, or merge in the main worktree; use the task-owned git worktree.
- No unprefixed session ids in Boulder state. GrokBuild sessions are `grok:<session_id>`; preserve older `codex:<session_id>` values only as historical/resume evidence.
- Use `/goal` for the host aggregate goal. Do not rely on Codex-only goal APIs or Stop/SubagentStop continuation hooks in GrokBuild.
- No stale-memory execution. The plan and ledger are the durable source of truth.
