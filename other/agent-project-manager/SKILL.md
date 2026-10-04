---
name: apm
description: Give an AI agent persistent project memory, a clean workspace and an optional multi-agent delegation path. Load only what the current task needs, keep durable user intent and decisions, and resume long projects with minimal tokens. Activate only for an explicit $apm command; maintaining this skill never activates it.
license: Apache-2.0
metadata:
  author: "jaywavfeng"
  version: "1.1.0"
---

# Agent Project Manager

> Agents can be swapped. The project must not lose its memory.

Understand the project, read only the memory this task needs, do the work, update the minimum necessary state, and stop. Delegation is available but is never the default.

## Start or resume

Only an explicit `$apm` request activates this skill. Maintaining it, pasting examples and finding existing runtime files never activate it. Finish simple tasks directly without initializing state.

For durable work, initialize once and keep stable goals and acceptance in `PLAN.md`. The default mode is `standalone`: one agent completes the task and no Worker is created. Use `set-project --mode leader` only when separate work is genuinely useful, then read [delegation policy](references/delegation-policy.md) before assigning anything.

`init` creates exactly three files — `STATE.json`, `memory.jsonl` and `PROJECT_STATUS.md`. `PLAN.md`, `workers/`, `review/` and `inbox/owner/` appear only when the command that needs them first runs. Do not pre-create empty scaffolding: the manager must cost less than the work it saves.

Existing `$apm continue worker-N` or `reviewer-N` resumes that role; `$apm continue lead` reads the current leader context. The repository, not chat history, carries the handoff.

Invoke the helper in a terminal with a verified Python 3.9+ interpreter and this skill's absolute script path:

```powershell
& "<absolute path to python.exe>" "<absolute skill directory>\scripts\statectl.py" context --project-root "<project directory>" --role lead
```

Replace placeholders. Never launch a bare `.py`, `code`, `Invoke-Item` or a file-opening tool for a state operation. Do not open it in VS Code to execute it. Use subcommand `--help` for unfamiliar arguments; `context` returns reusable executable/script arguments.

## Project memory

Durable compressed memory lives in `.agent-project-manager/memory.jsonl`. Record conclusions, never raw chat. Categories: `human-intent`, `decision`, `constraint`, `lesson`, `rejected`, `direction`, `open-question`.

Record the user's long-term requirements as `human-intent` — a deployment preference, a dependency they refuse, a feature explicitly out of scope, a rejected design direction, an output-language preference. Record `rejected` whenever a direction was considered and dropped, so a later agent does not silently retry it.

Use `memory-add --kind ... --text ...` to append and `memory-show` to read. Never dump the whole file into context: read only the kinds relevant to the current task. Run `memory-consolidate` when memory has grown noticeably; it compresses and deduplicates old entries and archives them, keeping the active file small. `human-intent` and `constraint` entries are never archived, whatever the retention window: they are the requirements an agent must not silently drop.

## Where files live

Two audiences, two places. Human-readable Markdown lives in the **project root** as `README.md` (English) and `README.zh-CN.md` (Chinese). Project memory lives in `.agent-project-manager/` and is single-language — it is machine-facing, so translating it wastes tokens and creates drift.

`PROJECT_STATUS.md` inside the runtime is the one human-facing page that belongs with the state: it is regenerated from `STATE.json` and `memory.jsonl`, so it never goes stale. It is bilingual by default. Keep it short and free of internal agent mechanics.

## Context compiler

Before starting a task, do not read the entire project memory. Run `context --role <role> --task "<current task>"` to get the minimum necessary context: project state, the current task, relevant user intent, relevant decisions, relevant file paths.

Without `--task` the command returns the standard role packet. Prefer the task-filtered form; a new agent should reach a correct working state with as few tokens as possible.

## Execute and accept

**standalone (default).** Read only the context this task needs, do the work, verify it against actual acceptance criteria, update state and memory, finish. Do not create roles for simple work.

**leader.** Read [delegation and roles](references/delegation-and-roles.md) for planning and direction changes, and [state ownership](references/runtime-state.md) before state changes. Select one [OpenAI](profiles/openai-codex.md) or [generic](profiles/generic.md) profile when routing. Persist bounded objectives, allowed_scope and acceptance before delegating. Keep final user-facing writing, core conclusions, architecture decisions and acceptance for yourself. Continue authorized work after verification without repeatedly seeking permission.

**worker.** Read `context --role worker-N`, the current task/status, relevant directives and dependencies. Respect write scopes and exclusions; validate actual results. Record meaningful transitions with `set-worker-status`. Relay and controlled assignments use `--assignment-revision`; only the current executor writes results. Leader-owned work uses `--actor lead`. Never validate or gate reasoning in an Owner-created conversation.

A stopped/blocked assignment can be resumed, cancelled or taken over through `control-worker`; record the reason and confirmed writer/process quiescence. Silence, timeout and blocked status are not stopping evidence. Takeover preserves scope and partial results, increments revision and fences old updates. Reassign stopped work without pretending it completed.

**reviewer.** Inspect the assigned scope and evidence. Record both review completion and `--verdict approved|changes-requested` with its revision. The leader can `cancel-review`, fix the issue, and request a fresh review; the review requirement is retained. A finished review is not necessarily approval.

Complete only against actual criteria and current evidence. Completed projects stay frozen for read-only questions; actionable changes use `reopen-project`. No role bypasses host permissions or expands external-action authority.

## Communicate only when useful

Read [host dispatch](references/host-dispatch.md) when binding or messaging. Prefer existing independent conversations. With existing Owner authority, automatically create an independent conversation only if the host supports explicit model and reasoning selection. Missing effective metadata means unverified routing, not automatic refusal; contradictory metadata requires correction. If creation is unavailable, provide one manual setup instruction. Do not use automatic subagents: requested routing is not proof of correct token billing.

Use `prepare-message`, the host send tool, then `record-message`. A leader dispatches ready assignments; workers and reviewers report result transitions. Preserve per-role receipts, ignore stale events, and reconcile uncertain sends once without blind retries. Host messages wake roles to read canonical state; delivery is not acceptance. Passive waits end on one unchanged timeout; no polling daemon.

## Keep the working set small

Ordinary continuation uses one role context, not repeated protocol or history reads. Context pages identify omitted active roles/events; inspect relevant pages before acceptance. Write facts once at assignment, control, blocker, direction or completion transitions. There is no handoff file to keep current: everything a cold start needs is read from `STATE.json`, `memory.jsonl` and `PLAN.md` when it exists.

`PROJECT_STATUS.md` is the human-facing page: concise, bilingual by default, refreshed from state rather than a log. It must not expose internal agent mechanics. `OWNER_STATUS.md` is the older optional variant.

Use [workspace housekeeping](references/workspace-housekeeping.md) when declaring output directories or tidying. Run it at milestone completion, before project completion, or when `housekeeping_due` is true during substantive continuation (7 days). Never mutate on a status-only request. Register task/run directories in batches; keep evidence and deliverables. Archive resolved feedback and released intermediate artifacts; only explicitly released reproducible temporary artifacts enter 7-day quarantine. Unknown files remain untouched. Normal searches exclude history/storage/generated outputs unless the task needs them.

Target **coordination tokens / actual-task tokens <= 10%**. Substantive leader work counts as task work. Without purpose-attributed telemetry, report only measured context/action proxies; use [benchmark rules](benchmarks/README.md) when measuring. No daily ledger, background cleanup or routine whole-project audit.

Prefer the simplest mechanism reliable for actual failures. Read-only commands never repair state; use explicit `recover` after a reported interrupted update. Advance the task once the necessary checks pass.
