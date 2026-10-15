---
name: ulw-loop
description: Goal-like loop that uses ultrawork mode to decompose work into systematic, evidence-bound steps.
metadata:
  short-description: Goal-like ultrawork loop for systematic decomposition
---

## Grok CEO goal boundary

Grok CEO: never execute goal body in-host; launch the Codex skill. Host `/goal` is display/state only.

## GrokBuild Tool Mapping

On Grok Build with lfg installed, use `spawn_subagent` only for Grok host monitoring and read-only discovery. Product implementation goes through the external Codex app-server handoff. This contract is GrokBuild-only (`coding_tool_adapter` = `grok`).

| Intent | GrokBuild tool to use |
| --- | --- |
| Search/read-only worker | `spawn_subagent({ subagent_type: "explore", background: true, description: "...", prompt: "TASK: ..." })` (host built-in; use `"explorer"` only for OMO persona) |
| Planning worker | `spawn_subagent({ subagent_type: "plan", background: true, description: "...", prompt: "TASK: ..." })` |
| Product implementation | `lfg --json handoff plan --role coding --engine gpt --focus "..."` → Codex app-server; `codex exec` fallback only when daemon unavailable. |


# ulw-loop

Use this skill when the user asks for `ulw-loop`, `ulw`, durable goal execution, evidence-led work, manual QA, or checkpointed long-running delivery.

This skill is intentionally compact. The full workflow lives in `references/full-workflow.md`. Read only the sections needed for the current phase, then execute them exactly.

### Product implementation handoff (GrokBuild)

Grok is the Sisyphus watcher, not the product implementer. For LOW, MEDIUM, or HIGH implementation bodies, create the external Codex work package with `lfg --json handoff plan --role coding --engine gpt --focus "..."`. The handoff creates or attaches the project Codex app-server thread; `codex exec` is fallback only when the daemon is unavailable. Use `spawn_subagent` only for Grok host work by `watcher`, `explorer`, or `git-master`; never spawn `lazycodex-worker-*`, `hephaestus`, or `coding` for the product body.


### External Codex implementation lane (GPT only)

**Grok = Sisyphus watcher**; **Codex app-server = sole product implementer**. Default product work is `lfg --json handoff plan --engine gpt` to Codex App.

Product implementation has exactly one worker lane: external Codex app-server handoff through `lfg --json handoff plan --engine gpt`. Grok may use watcher/explorer/git-master for host monitoring and read-only discovery, but must not spawn an in-host implementer for the product body.

1. Run `lfg --json handoff plan --role <role> --engine gpt --focus <focus>` and read `handoff.payloadMarkdown` plus the app-server transport receipt (`fullyTransferable`, `grokIsOrchestrator`).
2. Prefer the created/attached Codex app-server thread. Only when the daemon is unavailable, execute the reported `codex-exec-fallback` launch using `handoff.launch.argv[0]` with `handoff.launch.argv.slice(1)`; `handoff.launch.binary` is identity/readiness metadata. Use **`timeout: 0`** and kill the process group on cancellation.
3. **Do not** hand off sisyphus/prometheus; **do not** spawn Grok hephaestus/coding/lazycodex-worker for the product body.
4. Read RESULT into Boulder/ledger.

In-host `spawn_subagent` remains only for Grok host monitoring/read-only roles.


## Required First Steps

1. Open `references/full-workflow.md`.
2. Read through **Bootstrap** (including its tier triage), **GrokBuild `/goal` state**, **Execution Loop**, and the **Manual-QA channels** table before running any ULW command or recording evidence.
3. If the task has code edits, tests, QA, or commit work, follow the full workflow's delegation and evidence rules. Tests alone never prove done.

## Non-Negotiables

- Use the ulw-loop CLI state under `.omo/ulw-loop`; do not hand-edit goal state.
- After any compaction or context loss, re-read brief + goals + ledger FIRST plus `omo ulw-loop status --json`, then resume; never re-plan from scratch.
- If `omo ulw-loop create-goals` says the existing aggregate is already complete, start unrelated new work with a fresh `--session-id <new-id>` instead of steering or forcing the completed default state. Use `--force` only to intentionally overwrite completed evidence.
- Every success criterion needs observable evidence from a real surface: a channel (terminal/TUI via the xterm.js web terminal, HTTP, browser, computer-use) or, for CLI- or data-shaped criteria, an auxiliary surface (CLI stdout, DB diff, parsed config dump).
- Record evidence through the CLI only after cleanup receipts are available.
- Send every product edit, test, fix, and product QA body through `lfg --json handoff plan --engine gpt`; Grok keeps only watcher/explorer/git-master host work.
- Every `multi_agent_v1.spawn_agent` message starts with `TASK:`, then names `DELIVERABLE`, `SCOPE`, and `VERIFY`; put role and specialty instructions inside `message`; use `fork_context: false` unless full history is truly required.
- Plan and reviewer agents may run for a long time; spawn them in the background, keep doing independent root work, and poll with short `multi_agent_v1.wait_agent` cycles. Never use a single long blocking wait for them.
- For work likely to exceed one wait cycle, require the child to send `WORKING: <task> - <current phase>` before long reading, testing, or review passes, and `BLOCKED: <reason>` only when it cannot progress.
- Track spawned agent names locally. Use `multi_agent_v1.wait_agent` for mailbox signals, not proof of completion. A timeout only means no new mailbox update arrived. Treat a running child as alive.
- While children run, surface the active subagent count, agent names, and latest `WORKING:` phase.
- Fallback only when the child is completed without the deliverable, ack-only after followup, explicitly `BLOCKED:`, or no longer running. Then record inconclusive and respawn a smaller `fork_context: false` task with the missing deliverable.
- Use `git-master` for git-tracked edits: inspect recent and touched-path commit history, then commit each verified work unit atomically in the repository's observed language, scope, and message style with only that unit's files staged.

## Codex Tool Mapping

The full workflow may mention OpenCode-style orchestration examples. In Codex, translate them to native tools:

| Workflow intent | Codex tool |
| --- | --- |
| Plan agent | `multi_agent_v1.spawn_agent({"message":"TASK: act as a planning agent. ...","fork_context":false})` |
| Search/read-only worker | `multi_agent_v1.spawn_agent({"message":"TASK: act as an explorer. ...","fork_context":false})` |
| Product implementation | `lfg --json handoff plan --role coding --engine gpt --focus "..."` → Codex app-server; `codex exec` fallback only when daemon unavailable. |
| Final verification reviewer | `multi_agent_v1.spawn_agent({"message":"TASK: act as a rigorous reviewer. ...","fork_context":false})` |
| Wait for background result | `multi_agent_v1.wait_agent(...)` |
| Clean up finished worker | `multi_agent_v1.close_agent(...)` |

Flat `spawn_agent` requiring `task_name` instead (`multi_agent_v2`)? Rewrite rows: add `"task_name"`, `"fork_context":false` → `"fork_turns":"none"`, `wait_agent` takes only `timeout_ms`, no `close_agent` — finished agents end on their own.

When translating `load_skills=[...]`, include the requested skill names in the spawned agent's `message`.
