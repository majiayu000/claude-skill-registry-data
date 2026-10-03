---
name: supervisor
description: Use when a user asks to run technical-plan, SDD, coding, implementation, or review work through a visible Supervisor workflow with a coder thread, optional reviewer thread, configurable human approval gates, global role memory, and request state stored under ~/.supervisor.
---

# Supervisor

## Overview

Run technical-plan, SDD, and implementation requests through a visible Supervisor workflow. The supervisor identifies the target project, asks the human to confirm the runtime configuration, creates or reuses a visible coder thread and, by default, a visible reviewer thread, then gates each active unit through coder completion, optional reviewer acceptance, and the configured human approval policy.

By default, do not write runtime state into the target code repository. Store request state and global role memory under `~/.supervisor`.

## Required Resources

Before starting a supervised request, read:

- `references/thread-prompts.md` for coder/reviewer message templates.
- `references/review-standards.md` before asking reviewer threads to review or before interpreting reviewer results. Skip this when `review_required=false`.

Read `references/failure-recovery.md` only when a notification, memory compliance, reviewer loop, thread tool, or human scope-change problem occurs.

Use scripts for deterministic work:

- `scripts/init_request.py`: derive `project_key`, render the default config, and create `~/.supervisor/projects/<project-key>/<request-id>/` after human confirmation.
- `scripts/update_status.py`: create and update `supervisor-state.json`.
- `scripts/render_prompt.py`: render coder/reviewer/rework/human prompts from templates.
- `scripts/extract_memory_items.py`: draft coder/reviewer memory bullets from human feedback.
- `scripts/merge_feedback.py`: merge memory bullets into global role memory.

## Supervisor Workspace

Use `~/.supervisor` as the default runtime workspace. Allow the user to override this path during startup.

Default layout:

```text
~/.supervisor/
├── config.json
├── registry.json
├── memory/
│   ├── coder-memory.md
│   └── reviewer-memory.md
└── projects/
    └── <project-key>/
        ├── project.json
        └── <request-id>/
            ├── config.json
            ├── supervisor-state.json
            ├── document-index.json
            ├── requirement.md
            ├── sdd.md
            ├── technical-docs.md
            └── summary.md
```

Rules:

- Create each new request folder under `~/.supervisor/projects/<project-key>/<request-id>/`.
- Keep role memory global across all projects in `~/.supervisor/memory/`.
- Store cross-request defaults in `~/.supervisor/config.json`; each request may override them in its own `config.json`.
- If `~/.supervisor` is missing or required global memory files are missing, ask the user how to initialize memory before showing the startup config confirmation. `coder-memory.md` is always required. `reviewer-memory.md` is required only when `review_required=true`. The user must choose one method: paste memory content in chat, import existing memory files, or create empty templates.
- Record only request-local summaries and global role memory.
- Do not write to the target project repository unless the user explicitly asks.
- If `~/.supervisor` is not writable in the current environment, ask the user for another workspace path or use `/tmp` only as a temporary fallback and report the path clearly.

## Distribution And Use

Use `$supervisor` to start this workflow in Codex after the skill is installed.

For other AI tools:

- Use the same `SKILL.md`, references, and scripts when the tool supports skill folders.
- For tools that do not support this skill format directly, adapt `SKILL.md` into that tool's rule/instruction format and keep the scripts accessible.
- Always point every tool to the same runtime workspace, `~/.supervisor` by default, so request state and global memory stay shared across Codex, Cursor, Claude Code, and other agents.
- Do not rely on the skill installation directory for generated documents. Generated request files belong in the configured supervisor workspace.
- Use the same `projects/<project-key>/<request-id>/` layout across tools so concurrent projects stay isolated.

## Project Identity

Resolve `project_path` and `project_key` before creating coder and optional reviewer threads.

Project path priority:

1. Use an explicit `project_path` provided by the user.
2. Use the current workspace root when it is clearly the target code repository.
3. Infer from a provided requirement, SDD, or technical document path by walking upward to the nearest project marker such as `.git`, `package.json`, `Podfile`, `build.gradle`, `settings.gradle`, `*.xcodeproj`, `*.xcworkspace`, or `pubspec.yaml`.
4. If more than one candidate exists, show the candidates and ask the user to choose.
5. If no reliable candidate exists, ask the user for `project_path`.

Project key rules:

- Use an explicit `project_key` when the user provides one.
- Otherwise derive it from the basename of `project_path`, normalized to lowercase letters, digits, and hyphens.
- If the normalized key conflicts with a different path already present in `~/.supervisor/registry.json`, ask the user to confirm a unique key.
- Use `project_key` as the folder name under `~/.supervisor/projects/`.

## Thread Project Placement

Resolve where visible coder and optional reviewer threads should be created before creating them. Do not use the supervisor thread's current working directory or the skill installation directory unless it is explicitly the configured thread project.

Thread project policy:

- `same_as_project`: default. Create coder and optional reviewer threads in the Codex project that matches `project_path` when possible.
- `custom`: create coder and optional reviewer threads in the user-specified `thread_project_path` or `thread_project_id`.
- `projectless`: create visible threads without binding them to a Codex project, useful for document-only requests or when no matching Codex project exists.

Rules:

- Keep `thread_project_policy`, `thread_project_path`, and `thread_project_id` in the saved request `config.json`, but do not show them in the default startup confirmation view.
- If the user wants custom thread placement, ask for it separately before confirmation; if thread placement may differ from the target project, warn separately instead of adding hidden fields to the default confirmation view.
- If `thread_project_policy=same_as_project`, set `thread_project_path` to `project_path` in `config.json`.
- If `thread_project_policy=custom`, require either `thread_project_path` or `thread_project_id` before creating threads.
- If `thread_project_policy=projectless`, leave `thread_project_path` and `thread_project_id` empty.
- If `thread_project_path` differs from `project_path`, warn that coder/reviewer default workspace may differ from the target codebase and pass the real `project_path` in the role prompts.
- Use `list_projects` to find the Codex project matching `thread_project_id` or `thread_project_path`; if no matching project exists, ask whether to switch to `projectless`, choose another project, or continue in the current supervisor thread.

Example request config written to disk after confirmation:

```json
{
  "supervisor_workspace": "~/.supervisor",
  "project_path": "/path/to/project",
  "project_key": "project-key",
  "request_title": "feature request",
  "mode": "new",
  "request_id": "20260703-project-key-feature-request",
  "project_dir": "~/.supervisor/projects/project-key",
  "request_dir": "~/.supervisor/projects/project-key/20260703-project-key-feature-request",
  "memory_scope": "global",
  "agent_language": "same_as_supervisor",
  "memory_status": {
    "coder_memory_exists": false,
    "reviewer_memory_exists": false,
    "import_prompt_required": true,
    "coder_memory_text_provided": false,
    "reviewer_memory_text_provided": false
  },
  "human_gate_policy": "per_step",
  "review_required": true,
  "review_max_passes": 2,
  "agent_completion_mode": "notify",
  "poll_interval_seconds": 30,
  "thread_project_policy": "same_as_project",
  "thread_project_path": "/path/to/project",
  "thread_project_id": "",
  "supervisor_scope": "per_project",
  "documents": []
}
```

For human confirmation, use the concise startup view generated by `scripts/init_request.py --dry-run --show-options --confirmation-only`. Keep `config.json` as valid JSON; do not insert parenthesized hints into the JSON file itself.

When asking the human to confirm startup config, show the concise confirmation view, not raw JSON. The default startup confirmation view must contain exactly these fields and no others:

- `supervisor_workspace`
- `project_path`
- `project_key`
- `project_dir`
- `request_title`
- `human_gate_policy`
- `review_required`
- `review_max_passes`
- `agent_completion_mode`

Only `human_gate_policy` and `agent_completion_mode` should show parenthesized allowed values.

Prefer:

```bash
python3 scripts/init_request.py ... --dry-run --show-options --confirmation-only
```

Example confirmation view:

```text
supervisor_workspace: "~/.supervisor"
project_path: "/path/to/project"
project_key: "project-key"
project_dir: "~/.supervisor/projects/project-key"
request_title: "feature request"
human_gate_policy: "per_step" (Allowed: per_step, final_only, on_failure_only, none)
review_required: true
review_max_passes: 2
agent_completion_mode: "notify" (Allowed: notify, poll)
```

Do not create coder or reviewer threads until the user confirms the concise startup view or says to use the defaults.

## Configuration Reference

When showing the default startup confirmation view, show exactly the 9 fields listed above and add parenthesized allowed values only for `human_gate_policy` and `agent_completion_mode`. Use this table when the user asks what can be configured or wants to override hidden/default fields. CLI users can also run `python3 scripts/init_request.py --help` to see supported flags and enum values.

| Field | Allowed values | Default | Notes |
| --- | --- | --- | --- |
| `supervisor_workspace` | Any writable path | `~/.supervisor` | Runtime workspace outside target repos. |
| `project_path` | Absolute local project path | Inferred or ask user | Target codebase or source project. Do not hardcode a personal path in the skill. |
| `project_key` | Lowercase letters, digits, hyphens | Basename of `project_path` | Folder key under `projects/`. |
| `request_title` | Short text | Ask user or infer | Human-readable request name. |
| `mode` | `new`, `adopt` | `new` | Use `adopt` for half-finished work. |
| `request_id` | Unique folder-safe id | Generated | Request folder name under the project. |
| `memory_scope` | `global` | `global` | Role memory is shared across projects. |
| `agent_language` | `same_as_supervisor` or explicit language name | `same_as_supervisor` | Coder/reviewer visible threads use the same language as the supervisor/user unless configured otherwise. |
| `human_gate_policy` | `per_step`, `final_only`, `on_failure_only`, `none` | `per_step` | Controls when humans approve progress. |
| `review_required` | Boolean | `true` | Whether to create a reviewer thread and run reviewer gates. When `false`, skip reviewer memory, review prompts, review statuses, and `review_max_passes`. |
| `review_max_passes` | Integer `>= 1` | `2` | Human intervenes after this many failed review passes. Ignored when `review_required=false`. |
| `agent_completion_mode` | `notify`, `poll` | `notify` | Active notification or supervisor polling. When `review_required=false`, this applies only to the coder thread. |
| `poll_interval_seconds` | Integer `>= 5` | `30` | Applies only when `agent_completion_mode=poll`. |
| `thread_project_policy` | `same_as_project`, `custom`, `projectless` | `same_as_project` | Controls where visible coder and optional reviewer threads are created. |
| `thread_project_path` | Absolute local path or empty | `project_path` | Required for `custom` unless `thread_project_id` is set. |
| `thread_project_id` | Codex project id or empty | Empty | Optional alternative to `thread_project_path` for `custom`. |
| `supervisor_scope` | `global`, `per_project`, `per_request` | `per_project` | Controls intended supervisor-thread reuse. |
| `documents` | Array of local paths or URLs | `[]` | Requirement, SDD, technical docs, or references. |

## Memory Bootstrap

Before showing startup config confirmation or writing a new request config, check `~/.supervisor`, `~/.supervisor/memory/coder-memory.md`, and, when `review_required=true`, `~/.supervisor/memory/reviewer-memory.md`.

If `~/.supervisor` does not exist or any required memory file is missing:

1. Tell the user which memory files are missing.
2. Ask whether to paste memory content directly in chat, import existing memory files, or create empty templates.
3. Do not show startup config confirmation until the user has chosen one memory bootstrap method.
4. If the user pastes content, create the missing `coder-memory.md` and/or `reviewer-memory.md` from that chat content. Use `scripts/init_request.py --coder-memory-text` and/or `--reviewer-memory-text` for short content, or write the pasted content to a temporary text file and pass `--coder-memory-text-file` and/or `--reviewer-memory-text-file` for multiline content.
5. If the user provides import paths, pass them to `scripts/init_request.py` with `--coder-memory-source` and/or `--reviewer-memory-source`.
6. If the user chooses empty templates, pass `--create-empty-memory-templates` and create empty global memory files with only headings.
7. If the user does not choose a method, stop before startup config confirmation.
8. Never overwrite an existing global memory file unless the user explicitly asks.
9. Do not write the full pasted memory content into `config.json`; store only status such as `created_from_chat`, `imported`, `created_empty_template`, or `exists`.

## Document Discovery

User requirement, SDD, and technical documents usually live outside this skill and may live outside the code repository.

Document handling rules:

- If the user provides document paths or URLs, read those documents after config confirmation and record their original locations in `document-index.json`.
- If the user provides no documents but the request requires SDD or technical-plan context, ask for the requirement/SDD/technical document paths or URLs.
- If the project path is confirmed, you may search for likely local documents with `rg --files` using names such as `sdd`, `prd`, `requirement`, `需求`, `技术方案`, and `开发步骤`; show likely candidates and ask for confirmation before treating them as source documents.
- For web documents, browse/read only the links the user provides or explicitly approves.
- Store request-local extracts, copies, or summaries in the request folder only when useful for recovery. Preserve the original paths/URLs in `document-index.json`.

## Supervisor Rules

- Treat the current thread as the supervisor unless the user explicitly asks for a new supervisor thread.
- For each new request, create one visible coder thread. When `review_required=true` (default), also create one visible reviewer thread. If `review_required=false`, do not create a reviewer thread. Reuse the same role thread(s) across all technical-plan, SDD, and coding units for that request unless the user asks for new threads.
- Use Codex thread tools for visible histories. If thread tools are not already available, search for `create_thread`, `send_message_to_thread`, `read_thread`, `list_threads`, `list_projects`, and `set_thread_title`.
- Create coder and optional reviewer threads in the same Codex project as the requested codebase when possible. Use `list_projects` before `create_thread` when the tool requires a project id.
- Follow the configured thread project placement. `thread_project_policy` overrides assumptions from the supervisor thread's current directory.
- Name threads so the role, project key, and request are obvious, for example `Coder - project-key - feature request` and `Reviewer - project-key - feature request`.
- Maintain `supervisor-state.json` inside the confirmed request directory.
- Preserve the user's language across visible role threads. If the supervisor/user is communicating in Chinese, coder and reviewer prompts must instruct those threads to write progress updates, summaries, findings, risks, suggestions, questions, and memory compliance in Chinese. Keep protocol labels such as `CODER_DONE`, `REVIEW_PASSED`, and `BLOCKER` exactly in English.
- Keep reviewer context independent: pass requirements, changed-file/diff summary, verification output, and any necessary design or SDD notes. Do not pass coder's full rationale unless it is needed to review architecture.
- Paste global role memory directly into the coder/reviewer prompts. Do not send only a file path and assume the thread will read it. When `review_required=false`, paste only coder memory.
- Require coder and reviewer outputs to include `Memory compliance`, listing which memory bullets were followed or why a bullet was not applicable. When `review_required=false`, require this only from coder.
- If an agent omits memory compliance, send it back for correction before advancing.
- Follow the configured `agent_completion_mode`: `notify` or `poll`.
- Default `agent_completion_mode` is `notify`. Include the supervisor thread id and active notification instructions in coder/reviewer prompts when the mode is `notify`. When `review_required=false`, include notification instructions only in coder prompts.
- In `notify` mode, the supervisor must not run a timed `read_thread` polling loop. Wait for an active notification in the supervisor thread, then read the role thread once to collect full details if needed.
- `notify` mode requires a known `supervisor_thread_id` and usable thread-send tooling. If the supervisor thread id is unavailable, do not silently fall back to polling. Ask the human to choose one of: provide/confirm the supervisor thread id, switch `agent_completion_mode` to `poll`, or continue with explicit manual status checks.
- If `agent_completion_mode` is `poll`, do not ask coder/reviewer threads to send separate completion notifications. Read the role thread at the configured `poll_interval_seconds` until the required terminal status appears.
- `poll_interval_seconds` must be at least 5 seconds; default is 30 seconds and applies only when `agent_completion_mode=poll`.
- Follow the configured `human_gate_policy`: `per_step`, `final_only`, `on_failure_only`, or `none`.
- Follow the configured `review_required`: when `false`, skip reviewer dispatch, reviewer result interpretation, reviewer pass counting, and reviewer memory. A `CODER_DONE` result becomes the unit's agent acceptance signal before the configured human gate.
- Use the configured `review_max_passes` for each active unit. Memory-compliance correction prompts do not count as substantive reviewer passes unless they request a new review.
- Treat `REVIEW_FAILED` as valid only when reviewer reports at least one `BLOCKER` or `REQUIRED` finding.

## Workflow

1. Identify `project_path`, `project_key`, request title, optional document paths/URLs, and likely SDD/technical-plan needs.
2. If `~/.supervisor` is missing or memory files are missing, ask the user to choose a memory bootstrap method before showing startup config confirmation.
3. Render the default startup config with `scripts/init_request.py --dry-run --show-options --confirmation-only` or equivalent reasoning, show exactly the 9 startup fields, include parenthesized allowed values only for `human_gate_policy` and `agent_completion_mode`, and wait for confirmation.
4. After confirmation, create the request directory under `~/.supervisor/projects/<project-key>/<request-id>/`, create missing global memory files according to the already chosen memory bootstrap method, write `project.json`, and write the request `config.json`.
5. Read required resources and confirmed source documents. Create `document-index.json` when documents are used.
6. Create or update `supervisor-state.json` with `scripts/update_status.py`.
7. Create or reuse the coder thread and, when `review_required=true`, the reviewer thread for this request. Include relevant global role memory in each role prompt.
8. Render prompts with `scripts/render_prompt.py` when enough context is available; otherwise use `references/thread-prompts.md` directly.
9. Select exactly one active unit of work: technical solution drafting, SDD decomposition, the next SDD development step, or the whole request when no split exists.
10. Send the active unit to the coder thread. Use the configured completion mode: in `notify` mode, tell the coder to notify the supervisor thread when it emits `CODER_DONE` or `BLOCKED`; in `poll` mode, tell the coder to keep the terminal status in its own thread and read it every `poll_interval_seconds`.
11. If `review_required=true`, send the active unit, coder result, diff context, verification output, reviewer memory, and review standards to the reviewer thread. Use the configured completion mode: in `notify` mode, tell the reviewer to notify the supervisor thread when it emits `REVIEW_PASSED` or `REVIEW_FAILED`; in `poll` mode, tell the reviewer to keep the terminal status in its own thread and read it every `poll_interval_seconds`.
12. If `review_required=false`, do not create or message a reviewer thread. After `CODER_DONE`, apply the configured human gate directly; if no human gate applies for this unit, mark it `DONE` and advance.
13. If reviewer rejects and the pass budget remains, send only `BLOCKER` and `REQUIRED` findings back to coder, then re-review.
14. If reviewer rejects after `review_max_passes`, stop at `REVIEW_LIMIT_REACHED` and ask the human whether to apply remaining findings, override, or revise scope.
15. Apply the configured human gate before advancing.
16. After the whole request is complete and the configured human approval point is satisfied, draft candidate global role memory updates and ask the human to approve them before merging. Do not update `coder-memory.md` or `reviewer-memory.md` until the human confirms the proposed memory changes.
17. Write `summary.md` in the request directory and send the supervisor's final summary, including coder and, when present, reviewer thread ids or links.

## SDD Ownership

Support both SDD sources:

- If the user provides an existing SDD, manage that SDD: identify the current active unit, run coder and optional reviewer gates, and preserve the user's step structure unless changes are approved.
- If no SDD exists and the request needs one, create an initial active unit for technical solution and SDD decomposition before implementation.
- If another skill or human-generated document is responsible for SDD creation, treat its output as source input and manage execution only.

## Adopting Existing Work

If a project or request is already halfway done, start in `mode=adopt` instead of restarting from scratch.

Adoption rules:

- Read the current requirement, SDD, technical docs, local diffs, existing implementation, and any available notes.
- Ask the user which units are already completed, which unit is active, and which parts still need review if this cannot be inferred safely.
- Create a new request folder under `~/.supervisor/projects/<project-key>/<request-id>/` and record `mode=adopt` in `config.json`.
- Mark completed units as `DONE` or `HUMAN_APPROVED` in `supervisor-state.json` only when there is clear evidence or human confirmation.
- Continue from the current active unit. Do not rewrite history or re-run completed work unless the human asks.

## State File

Use `scripts/update_status.py` to make recovery explicit:

```bash
python3 scripts/update_status.py \
  --file ~/.supervisor/projects/<project-key>/<request-id>/supervisor-state.json init \
  --title "Request title" \
  --project-path "/path/to/project" \
  --project-key "<project-key>" \
  --request-dir "~/.supervisor/projects/<project-key>/<request-id>" \
  --supervisor-thread-id "<id>"
```

Update each active unit before dispatching, after coder completion, after reviewer completion when review is required, and after human approval when the gate policy requires it.

## SDD Step Gate

For technical-plan, SDD, and coding work, the supervisor must maintain a visible unit status list in the supervisor thread:

- `PENDING`: not started.
- `CODING`: coder is drafting, decomposing, implementing, or verifying this unit.
- `CODER_DONE`: coder says the unit is ready for review.
- `REVIEWING`: reviewer is checking this unit. Used only when `review_required=true`.
- `REVIEW_FAILED`: reviewer requires changes. Used only when `review_required=true`.
- `REVIEW_LIMIT_REACHED`: reviewer used the configured pass budget and still requires changes; wait for human direction. Used only when `review_required=true`.
- `REVIEW_PASSED`: reviewer accepts the unit. Used only when `review_required=true`.
- `HUMAN_REVIEW`: waiting for human approval.
- `HUMAN_APPROVED`: human approved this unit.
- `DONE`: unit is closed and the supervisor may start the next unit.

With `human_gate_policy=per_step`, never work on unit N+1 while unit N is before `HUMAN_APPROVED`, unless the user explicitly authorizes parallel work.

## Human Feedback Memory

When the configured human approval point is satisfied and the request produced meaningful feedback:

- Extract at most 10 coder-memory items for technical-solution preferences, SDD decomposition style, implementation preferences, architecture guidance, naming/style preferences, testing expectations, and recurring mistakes.
- If a reviewer participated, extract at most 10 reviewer-memory items for review blind spots, project-specific quality gates that should generalize, risk patterns, and standards the reviewer should enforce next time.
- Do not store one-off feature facts in role memory.
- Show the proposed coder/reviewer memory bullets to the human and ask for confirmation before writing memory files.
- If the human edits, rejects, or says to skip memory updates, follow that decision. If the human is silent, leave memory unchanged and record that memory update is pending or skipped.
- Merge rather than duplicate. If a new item is the same as, more specific than, or substantially similar to an existing item, update the existing bullet.
- Prefer `scripts/extract_memory_items.py` to draft candidate bullets and `scripts/merge_feedback.py` for line-level fuzzy merging. Inspect the result and clean up wording if needed.

Example:

```bash
python3 scripts/merge_feedback.py \
  --file ~/.supervisor/memory/coder-memory.md \
  --item "Prefer small, well-scoped changes over broad refactors unless the request requires them."
```

## Status Protocol

Use clear status labels when communicating between threads:

- `CODER_DONE`: active unit ready for review.
- `REVIEW_FAILED`: reviewer found required changes.
- `REVIEW_PASSED`: reviewer accepts the current unit.
- `REVIEW_LIMIT_REACHED`: maximum reviewer passes reached; supervisor needs human direction.
- `MEMORY_COMPLIANCE_MISSING`: an agent omitted required memory compliance output.
- `HUMAN_CHANGES_REQUESTED`: human requested more work.
- `HUMAN_APPROVED`: human accepted the current unit.
- `SUPERVISOR_DONE`: memory and request summary are complete.

## Common Mistakes

- Writing runtime state into the target business repository by default.
- Creating request folders directly under `~/.supervisor`; request folders should live under `~/.supervisor/projects/<project-key>/`.
- Creating a new supervisor thread per request when the configured scope says to reuse one.
- Creating new coder/reviewer threads for every unit. Reuse the role thread(s) for a request so each role keeps its visible history.
- Creating a reviewer thread when `review_required=false`.
- Creating coder/reviewer threads in the supervisor's current directory or the skill installation project instead of the configured thread project.
- Ignoring `thread_project_policy=custom` or `thread_project_policy=projectless`.
- Showing raw JSON only during startup confirmation. Use the concise confirmation view; keep the saved config as clean JSON.
- Showing fields other than `supervisor_workspace`, `project_path`, `project_key`, `project_dir`, `request_title`, `human_gate_policy`, `review_required`, `review_max_passes`, and `agent_completion_mode` in the default startup confirmation view.
- Adding parenthesized option hints to fields other than `human_gate_policy` and `agent_completion_mode`.
- Showing startup config confirmation before the user chooses how to initialize missing global memory.
- Starting the next technical-plan, SDD, or coding unit before the configured human gate allows it.
- Polling coder/reviewer threads without `agent_completion_mode=poll`. Default to active notifications unless the user configures polling.
- Treating `agent_completion_mode=notify` as permission to poll every 30 seconds. In notify mode, no timed polling loop is allowed.
- Rendering notify prompts with `supervisor_thread_id=<unavailable>` and then reading role threads on a timer. Either supply the supervisor thread id, switch to poll with human confirmation, or use explicit manual checks.
- Hard-coding a polling interval. Use `poll_interval_seconds` from `config.json`.
- Sending English coder/reviewer prompts when the supervisor/user is communicating in Chinese.
- Sending a unit through more reviewer passes than `review_max_passes` without human direction.
- Requiring reviewer memory or reviewer notification when `review_required=false`.
- Passing only memory file paths. Paste the relevant memory bullets into the thread prompt and require memory compliance output.
- Assuming bundled seed memory exists inside the skill. Global role memory lives under `~/.supervisor/memory/`; missing memory is pasted, imported, or initialized as an empty template.
- Letting reviewer rely on coder's persuasive explanation instead of reviewing the diff and requirements.
- Updating memory before the configured human approval point or before the human confirms the proposed memory bullets.
- Storing feature-specific facts in coder/reviewer memory.
- Treating reviewer suggestions as failures. Only required architecture, function, security, correctness, robustness, or test issues should block.
