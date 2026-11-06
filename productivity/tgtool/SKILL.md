---
name: tgtool
description: Use when the user wants the agent to choose, combine, and actively use the best available local skills for a task.
metadata:
  author: codex
  version: "2.22.0"
---

# TGTool

Use this skill as the top-level router for local Codex skills.

Its job is to pick the **smallest useful skill set**, avoid redundant loading, and move directly into execution.

## Core idea

Route in layers:

1. Reuse current context first
2. Read lightweight capability index first (lazy)
3. Confirm what the current environment can already do
4. Choose one primary workflow skill
5. Add only the minimum supporting capabilities
6. Execute instead of lingering in skill-selection mode

The goal is not to use more skills. The goal is to use fewer, better.

## Context loading mode

Default mode is `lazy`.

- `lazy` (default)
  - do not load all skill bodies at start
  - read `skills/tgtool/skills-index.json` first
  - shortlist likely skills from index fields (`skill_id`, `summary`, `tags`, `triggers`)
  - open only shortlisted `SKILL.md` files when needed
- `full` (fallback)
  - allowed only when explicitly requested by user or when index is missing/corrupted and user approved fallback

Override switch:

- `TGTOOL_CONTEXT_MODE=lazy|full`
- if unset, treat as `lazy`

## Mode selection

When the user explicitly invokes `tgtool`, ask for mode immediately unless the user already specified one in the same turn.

Use:

`Choose a tgtool mode: review (1/re), standard (2/st), or autopilot (3/auto).`

### Modes

- `review`
  - Recommend routing and plan first.
  - Do not execute until the user confirms.
  - In user-facing updates, explicitly state the current workflow stage and one short reason for the choice.
- `standard`
  - Execute normally.
  - Ask when a meaningful branch, uncertainty, or risk appears.
  - In user-facing updates, explicitly state the current workflow stage and one short reason for the choice.
- `autopilot`
  - Execute end-to-end with minimal interruption.
  - Stop only for destructive actions, critical ambiguity, or required permission escalation.

Accept these mode aliases:

- `review`: `1`, `re`, `review`
- `standard`: `2`, `st`, `standard`
- `autopilot`: `3`, `auto`, `autopilot`

## Session persistence

After the user explicitly invokes `tgtool` once, keep `tgtool` active across subsequent turns by default.

Rules:

- Treat the first explicit mention of `tgtool` as the start of a persistent routed session.
- Once activated, mode selection is mandatory before further routed work unless the mode was already provided in the same turn.
- After that, continue applying `tgtool` even if the user does not explicitly mention it again.
- End the persistent routed session only when the user explicitly says `tgend`.
- If the user says `tgend`, stop applying `tgtool` by default from the next turn onward unless they explicitly invoke it again.
- The first activation still requires an explicit `tgtool` invocation.

## Session visibility

Keep tgtool visible without repeating the same boilerplate every turn.

Rules:
- announce tgtool activation and the selected mode when the session starts
- if the mode changes, announce the new mode once
- during longer work, prefer short status markers such as `仍在 tgtool/autopilot` instead of repeating the full termination sentence
- remind the user about `tgend` only at session start, after a long gap, when the user seems uncertain whether tgtool is still active, or near task closeout
- do not append the exact same termination sentence to every response by default

## Global rules

1. Use Chinese by default unless the user explicitly requests another language.
2. Reuse established facts from the current conversation before re-reading files, logs, or skills.
3. Prefer concise summaries, deltas, and direct conclusions over repeated background.
4. Keep active context compact. For very long inputs, summarize or segment before deeper routing.
5. Do not load extra skills unless they materially improve the result.
6. Do not stack overlapping workflow skills unless the task genuinely spans phases.
7. Respect the selected mode throughout the task.
8. Do not stop after recommending skills; execute with them unless the mode says not to.
9. Watch memory risk continuously. If the likely path may cause unsafe memory growth, stop and ask to switch to a safer plan.
10. Watch storage risk continuously. If the likely path may cause unsafe disk or artifact growth, stop and ask to switch to a safer plan.

## Strict Read-Only Mode

If the user explicitly says any equivalent of `readonly`, `只读`, `不要修改`, `不要动环境`, `绝对谨慎`, or otherwise makes a strong no-write request, enable strict read-only mode immediately.

Rules while strict read-only mode is active:
- treat the mode as stronger than review/standard/autopilot
- allow only read-only inspection, reasoning, and reporting
- do not edit files, restart services, rebuild containers, register/deregister services, delete data, push commits, or change any local/remote/shared environment state
- do not perform verification steps that create side effects; prefer passive evidence from existing state
- before any substantive action, run an internal precheck: will this write files, change service/container/remote state, or create hard-to-revert side effects?
- if the precheck says yes, stop and ask instead of inferring approval from prior momentum
- state briefly that the task is being handled in strict read-only mode when doing substantive diagnosis

Strict read-only mode stays active until the user explicitly relaxes it.


## Proactive Boundaries

Default posture: aggressively proactive for coding and debugging tasks.

The router should move forward end-to-end whenever the path is technically obvious and low-risk. It should stop only when continued execution would create irreversible damage, introduce product-level ambiguity, affect shared environments without approval, or require elevated privileges.

When in doubt between asking and progressing, prefer progressing if the action is local, reversible, and does not cross a shared-environment or business-semantics boundary.

### Safe to do proactively

The agent should proceed without asking for confirmation when the action is local, reversible, and part of the shortest path to completion.

Examples:
- read code, logs, configs, and git state
- search the repository and trace call paths
- make small or medium local code changes
- run syntax checks, focused tests, and local verification
- add minimal repros or minimal tests needed to validate a fix
- retry with a safer equivalent local approach after a routine failure
- narrow down faults through read-only inspection and evidence gathering
- choose the smallest technically sound fix when the path is clear

### Do proactively, but announce briefly first

The agent should still proceed, but must tell the user what it is about to do in one short sentence before acting.

Examples:
- multi-file code changes
- rebuilding or restarting local development containers
- longer-running local verification
- behavior-affecting bug fixes where the technical path is still clear
- selecting one implementation approach among several close technical options when one is clearly the least risky

Preferred pattern:
- "I’m taking the smallest-impact path: first X, then I’ll verify Y."

### Shared-environment boundary

When the next action touches a remote machine, shared container, shared config, shared data set, or other non-local environment, classify it before acting:
- `只读可做`
- `需确认后可做`
- `禁止默认执行`

When the classification affects the next step, state it in one short line instead of using a long warning template.

### Must stop and ask

The agent must pause for confirmation when any of these are true:
- destructive actions
- irreversible or high-blast-radius actions
- shared or remote environment changes
- product or policy ambiguity
- required privilege escalation
- actions that add new infrastructure, dependencies, or platforms
- actions that change long-term architecture beyond the current task
- actions that may affect external users or live data semantics

Examples:
- deleting data, resetting state, wiping directories
- `git reset --hard`, forced revert, or overwriting unrelated work
- modifying remote/shared machines, containers, or configs without explicit approval
- making a choice between valid business behaviors rather than technical fixes
- introducing a new service, framework, or deployment dependency

### Debugging-specific boundaries

For debugging, default to read-only diagnosis first.

The agent should:
- inspect logs, config, status, and request flow first
- build the smallest useful repro when needed
- separate debugging outputs into:
  - 已验证
  - 推断
  - 未验证
- present conclusions in this order:
  - symptom
  - direct evidence
  - likely root cause
  - remaining uncertainty
- do not present inference as if it had already been verified

The agent must not:
- assign blame without evidence
- modify shared environments during diagnosis unless explicitly approved
- restart services, clear jobs, or change configs on remote systems without approval

For remote debugging, keep a compact evidence ledger as the work proceeds.

Record only the minimum useful facts:
- host or environment
- command or inspection method
- key output or observation
- conclusion tied to that evidence

Prefer updating one compact running record over scattering unsupported conclusions across many replies.

For long sessions, emit a compact evidence summary only when the topic shifts or the work is about to be summarized.

Use at most four lines:
- host or environment
- key evidence
- current conclusion
- remaining unverified point

### Coding-specific boundaries

For coding tasks, default to the smallest closed loop:
- identify the fault
- patch the minimal relevant code
- verify locally
- report outcome

The agent should proactively add:
- boundary handling
- compatibility fixes
- focused logging
- focused tests

The agent should not proactively add:
- broad refactors
- framework migrations
- architectural rewrites
- unrelated cleanup

### Decision order

1. Determine whether a smallest safe path is obvious.
2. If yes, proceed without asking.
3. If the change is substantial but still safe, announce briefly and continue.
4. Verify before claiming success.
5. Stop only when a hard boundary above is triggered.

## Working snapshot

Before routing, compress the current task into a tiny working snapshot and keep reusing it.

Include only:

- objective
- current repo or workspace
- selected mode
- selected primary workflow skill, if already chosen
- selected support layers, if already chosen
- confirmed constraints
- unknowns blocking the next step

Reuse this snapshot before re-reading files, skills, or prior context. Update it only when the facts change.

## Decision flow

Apply this flow in order.

### Step 0: Resolution gate for missing skills/tools

When tgtool needs to use any skill/tool (whether user-specified or internally selected), resolve that target first.

For skills, resolve in this strict order:

1. active and enabled in current session
2. present locally but currently not enabled
3. not present locally

If a skill is present locally but not enabled:

- use repo utility `tools/skill_temp_toggle.py on <skill_id>` to temporarily enable it
- continue execution immediately after a successful toggle
- do not trigger fallback routing for this case
- record the skill id in the active task recap
- at task closeout, run `tools/skill_temp_toggle.py reset` to roll back only skills that were previously disabled

Temporary-toggle guardrails:

- never disable skills that were already enabled before this task
- if toggle/reset fails due permissions or environment limits, report the exact error and ask user to approve the next safe step
- treat temporary toggles as task-scoped state, not permanent policy changes

If the target skill/tool cannot be resolved immediately:

- stop automatic fallback
- report the miss clearly (what tgtool attempted to use and what was not found)
- propose the exact next fallback steps in order (for example: local path search, then `find-skills`, then `tool_search`)
- ask for explicit user approval before executing those fallback steps

Approval rule:

- in `standard` and `review`: always wait for explicit user approval before fallback execution
- in `autopilot`: missing skill/tool still requires explicit user approval before fallback execution

Do not silently switch to a different skill/tool when the intended one was not found.
Do not treat "present locally but not enabled" as "not found".

### Step 1: Check whether routing is even needed

Do not over-route.

- If the task is already clearly covered by one obvious skill, use that skill.
- If the user explicitly names a skill, use it.
- If the current session context is already enough and no extra capability is needed, keep routing minimal.

### Step 2: Evidence gate

Use the lowest evidence level that is safe.

- `L0`
  - the current conversation and snapshot are sufficient
  - do not read extra skill files or environment files
- `L1`
  - read `skills/tgtool/skills-index.json`
  - read only the target skill file that you already expect to use
- `L2`
  - inspect environment, additional skills, memory, or external sources because there is real uncertainty

Default to `L0` or `L1`. Escalate to `L2` only when it materially improves correctness.

Index-first rule:

- in `lazy` mode, never bulk-read all `SKILL.md` files for capability scanning
- when uncertainty remains after index read, expand only top `1-3` candidate skill files
- keep non-selected skill bodies unopened

### Step 3: Fast-path precheck

Before any capability scan, check whether the task can be routed immediately with current context.

Use the fast path when one or more of these are true:

- the user explicitly names a skill
- the current session context already established the relevant capability set
- the request is a small question, clarification, explanation, or other non-development task that does not depend on web research, installation, MCP discovery, or cross-repo exploration
- the request is an extremely small local implementation task with one obvious fix, no meaningful ambiguity, and no meaningful behavior risk
- the correct workflow path is already obvious from the current context

Development-task override:

- If the user is asking for code changes, behavior changes, refactors, or implementation work, do not treat it as a fast-path execution task by default.
- For development work, prefer the `superpowers` workflow family by default.
- Default development routing is: analyze first, then write a plan, then implement.
- Use fast-path direct execution for development work only when the change is truly tiny, unambiguous, and low-risk.

If the fast path is sufficient, skip `$tool-advisor` and proceed directly to workflow selection.

### Step 4: Use `$tool-advisor` first by default

Default preference:

- treat this as the capability-confirmation path when uncertainty is real
- do not treat it as a ritual
- skip it when the path is already obvious

Priority rule:

- if `fast-path` and `$tool-advisor` default preference conflict, prefer `fast-path`
- if environment uncertainty could change the routing decision, prefer `$tool-advisor`
- if the current session already covers the key uncertainty, do not call `$tool-advisor` just for formality

Use `$tool-advisor` unless the user explicitly forbids it or the path is already obvious.

Use it to answer:

- What skills are already available?
- What tools, MCP servers, and local capabilities are already usable?
- Is the request already covered without installing or discovering anything else?

Do not use `$tool-advisor` as an excuse to reload everything. Use it to reduce uncertainty.

Lazy interaction rule:

- `tool-advisor` confirms capability surface
- index narrows likely skills
- only shortlisted skill bodies are opened for final route selection

### Step 5: Choose one primary workflow skill

Choose exactly one unless the task clearly moves across phases.

Prefer installed `superpowers` workflow skills when they are a better fit than `$stream-coding`.

Development-task default:

- For implementation work, prefer the `superpowers` workflow family over direct execution.
- If the user explicitly asks for multiple Codex agents, a virtual team, or parallel agent execution, evaluate the `multi-codex-orchestration` skill before ordinary single-session development routing.
- When tgtool routes a task into `superpowers`, let `superpowers` choose and control its own internal development process.
- Do not hard-code a fixed internal sequence such as `brainstorming -> writing-plans -> executing-plans` inside tgtool.
- Keep tgtool responsible for global rules, mode behavior, visibility, boundaries, and support-skill selection while `superpowers` owns the development workflow once selected.
- Use `$stream-coding` directly only when no `superpowers` workflow skill fits better, or when the change is extremely small, unambiguous, and low-risk.
- Do not route code-changing work straight into `$stream-coding` unless one of those narrow exceptions is true.

- Use `using-superpowers`
  - When the task should enter the `superpowers` workflow family and its internal workflow should be delegated to `superpowers` instead of being prescribed by tgtool
- Use `brainstorming`, `writing-plans`, or `executing-plans` directly only when the user explicitly asks for one of them, or when another active instruction already makes that specific entry point mandatory.
- Use `$stream-coding`
  - For direct implementation once analysis and planning are already sufficient, or when the change is truly tiny and obvious

Scenario-specific route:

  - Use `multi-codex-orchestration`
  - When the user explicitly wants multiple Codex agents or a virtual team, the task can be decomposed into 2+ relatively independent subproblems, sequential single-agent execution would be materially worse, and role-based ownership would improve throughput or confidence
  - Do not use it for tiny fixes, tightly coupled single-threaded work, pure read-only diagnosis without real parallel value, or tasks that would create conflicting write scopes across agents
  - If the user explicitly asks for a `ruflo` backend or asks to initialize the orchestration runtime, first use `skills/multi-codex-orchestration/scripts/bootstrap_ruflo_backend.py` to automatically chain `ruflo init --codex`, `ruflo init --minimal --force`, and `ruflo swarm init --v3-mode` as needed
  - After `ruflo` bootstrap succeeds, prefer the current session's `claude_flow` orchestration tool family for actual execution: initialize a swarm, spawn agents, create tasks, assign tasks, and monitor status there instead of stopping at CLI bootstrap
  - Use `skills/multi-codex-orchestration/scripts/probe_ruflo_execution.py` only as a shell-side sanity check that the local `ruflo` CLI path can create a swarm, spawn an agent, create a task, and assign it; do not mistake that probe for the main in-session execution path
  - In token-sensitive orchestration, default to a single active `operator`; keep `critic` dormant and wake it only on failure, stage transition, or explicit review/feedback demand
  - In explicit tmux mode, default to `2 pane` only (`operator + critic`) unless the user explicitly asks for more panes
  - If the user asks for explicit/visible execution, use `skills/multi-codex-orchestration/scripts/launch_explicit_tmux.py` and treat “explicit” as auto-trying to pop a foreground tmux terminal, not requiring manual attach first
  - Do not re-send the same large context block to multiple Codex workers by default; compress it first and send only role-specific deltas
  - If orchestration is unavailable or rejected, fall back in this order: `subagent-driven-development`, `dispatching-parallel-agents`, then ordinary `using-superpowers` routing
  - Reject orchestration when write ownership cannot be made disjoint enough for safe parallel execution

Workflow boundary rule:

- Once a task is routed into the `superpowers` workflow family, do not prescribe its internal fallback or forward transitions from tgtool; let `superpowers` manage that flow.
- Use `$stream-coding` as a separate default execution workflow only when no `superpowers` workflow skill clearly fits, not as the default internal fallback once `superpowers` has been chosen.

### Step 6: Add supporting capabilities only when they matter

These are optional support layers, not defaults.

#### `claude-mem`

Use when:

- the user asks what was done before
- the task continues a long-running effort
- prior experiments, decisions, or historical context would materially help
- repeated context reconstruction would waste tokens

Do not use for short, self-contained tasks where current-session context is already sufficient.

When deciding whether to write or update memory, prefer high-value knowledge only.

Treat information as high-value when one or more of these are true:

- it is likely to recur across future sessions
- it captures an environment constraint, workflow constraint, or tested operational fact
- it is not obvious from reading the code alone
- it has been verified by testing, execution, or direct inspection
- preserving it will materially reduce future context rebuilding, repeated debugging, or repeated explanation

Do not write low-value memory for:

- one-off noise
- unverified guesses
- transient intermediate steps
- facts that are trivial to recover from the repo

When new verified information supersedes older memory, prefer updating the existing understanding instead of storing a conflicting duplicate.

#### `planning-with-files`

Use when:

- the task is complex, multi-step, or likely to require more than 5 tool calls
- the work will span multiple phases, discoveries, or verification loops
- persistent file-backed planning would reduce context loss or help recovery after interruptions
- the task benefits from maintaining `task_plan.md`, `findings.md`, and `progress.md` in the project root

Do not use when:

- the task is short, obvious, and easily held in normal session context
- the overhead of planning files would exceed the value of the task itself

Use it as a support layer, not a replacement workflow:

- let `superpowers` own the development flow when `superpowers` is selected
- add `planning-with-files` only when disk-backed plan, findings, and progress tracking would materially improve execution or recovery
- do not make `planning-with-files` the default primary workflow for ordinary coding tasks

#### `jstorcli-yatc-jetice-ops`

Use when:

- the task involves `jstorcli` workflows with `yatc`, `jetice`, or `jetlake`
- VM lifecycle, image preparation, deployment checks, or command lookup is part of execution
- avoiding hardcoded local paths is important for correctness and portability

Do not use when:

- the task is unrelated to `jstorcli` or those environments
- generic workflow skills already fully cover the need without environment-specific operational guidance

Use it as a domain support layer:

- keep one primary workflow skill selected by tgtool
- add `jstorcli-yatc-jetice-ops` only when those operations are actually in scope
- remove it from the active skill set once the environment-specific step is completed


#### `exa`

Use when:

- the user needs latest information
- the task needs live web research or external documentation
- recent product, library, or service state matters

Do not use for purely local code or repository work when the answer is already in the workspace.

#### `find-skills`

Use when:

- the user's request implies a capability gap in the currently installed skills
- the user explicitly wants to discover whether a skill exists
- a reusable skill likely exists and would materially improve the result

Use `find-skills` only when at least one of these harder conditions is true:

- there is no installed domain skill that directly matches the requested capability
- the available skills cover workflow only, but not the missing capability itself
- the requested capability looks reusable and general rather than one-off or project-specific
- installing or discovering a skill is likely to improve quality more than handling the task ad hoc

Do not use when the current installed skills already clearly cover the task.

If the intended skill was not found (user-specified or internally selected by tgtool):

- do not call `find-skills` immediately
- first report the miss and ask for explicit approval of the fallback plan
- call `find-skills` only after approval

Prefer direct handling instead of `find-skills` when one or more of these are true:

- the task is one-off, narrow, or tightly tied to the current project
- the missing capability is small enough that existing tools or reasoning can cover it cleanly
- installing a new skill would cost more time or context than solving the problem directly
- the request is primarily execution, not capability extension

### Step 7: Execute with the minimum skill set

After routing, open only the selected skill files and follow them.

Do not browse every skill body.
Do not reload the same skill unless something changed or verification is required.

If tgtool auto-enabled any local skill for this task:

- keep it enabled only for the active task scope
- disable it automatically at closeout
- include one short line in the completion recap listing which skills were temporarily enabled and then disabled

## Long-context policy

When inputs are large, old, or repetitive:

- prefer incremental updates over restating background
- summarize before routing
- inspect only the needed files or sections
- avoid rereading large unchanged logs or documents
- prefer “what changed?” over “repeat everything”

Use this fixed compression flow:

1. Decide whether full reading is actually required.
2. If not, extract only:
   - objective
   - constraints
   - current state
   - deltas or failures
3. Route using that compressed view first.
4. Open original long content only for the specific sections needed by the selected skill.
5. Preserve the compressed summary as the working context instead of repeatedly rebuilding it.

If a task is long-running:

- use `claude-mem` only if the added recall value is real
- otherwise stay with current-session incremental context

## Context bloat guard and restart handoff

Continuously estimate whether the current session context is becoming bloated.

Primary trigger uses context-window percentage when available:

- above `70%`: issue an early warning and recommend preparing handoff
- above `85%`: start Phase A preview handoff suggestion
- above `92%`: recommend immediate Phase B final handoff and session switch

Explicit invocation hook:

- when the user explicitly invokes `$tgtool` in a turn, run `skills/tgtool/scripts/context_guard.js` once before deeper routing
- use this call shape:
  - `node skills/tgtool/scripts/context_guard.js --input-text "<current turn text>"`
- use the script output `estimated_context_pct` as the percentage source for the `70/85/92` threshold logic in this section

When a threshold is reached:

1. Tell the user context is now high-risk for token waste.
2. Ask one direct question: whether to start restart handoff now.
3. Do not continue deep execution until the user answers.

If user agrees to restart handoff, run in two phases:

- Phase A (preview only)
  - generate a compact preview handoff first
  - show it and ask for confirmation to finalize
- Phase B (final handoff pack)
  - after confirmation, produce final `summary + compact evidence`
  - write the handoff pack to:
    - `docs/session-handoffs/YYYY-MM-DD-<topic>.md`
  - keep the pack short and executable for the next session

Handoff pack must include:

- objective
- completed work
- key decisions
- open risks or blockers
- next first action
- compact evidence (only critical logs, errors, or file refs)

Session switch boundary:

- tgtool cannot programmatically force the client UI to create a new session
- after final handoff pack is written, instruct user to open a new session
- in the new session, first step is to read the handoff file and continue from it

## Memory writeback policy

At natural completion points, briefly evaluate whether memory should be written or updated.

Use this rule:

1. Ask whether the result has durable reuse value.
2. If no, do not store it.
3. If yes, prefer concise, validated conclusions over process noise.
4. If the new result corrects or supersedes prior memory, update that understanding rather than duplicating it.
5. Only write memory that would plausibly help a future session make better decisions faster.

### Memory update rules

When deciding between updating prior memory and writing a new memory:

- Update existing memory when the new result is about the same workflow, environment fact, operational constraint, or previously recorded conclusion.
- Write a new memory only when the result introduces a genuinely new reusable fact that is not simply a correction or refinement of an older one.
- If old and new memories conflict, prefer the newer result only when it is more directly verified by execution, testing, or direct inspection.
- If confidence is still mixed or the evidence is weak, do not overwrite high-confidence memory with speculation.
- Prefer one clean updated understanding over multiple partially conflicting notes.

Priority of trust:

1. direct execution or test results
2. direct inspection of current code, config, or runtime state
3. previously stored memory
4. inference or guesswork

If the new result does not beat the old one on that scale, do not treat it as an authoritative update.

## Routing explanation policy

When reporting routing decisions, be concise but auditable.

Required:

- the selected skill or skill set
- the main reason it was selected

Optional when helpful:

- mention the most plausible skipped alternative and why it was skipped

Examples:

- current context was already sufficient
- a more specific installed skill already covered the task
- the task was implementation-heavy, not research-heavy
- no real cross-session value justified `claude-mem`
- no actual capability gap justified `find-skills`

Do not enumerate every rejected skill. Mention only the most plausible skipped candidate when it improves trust in the routing choice.

## Output behavior

Required:

- before substantial work, obtain the mode if needed
- then say which skills are being used and why in one concise line

Also required in `review` and `standard`:

- the current workflow stage
- one short reason for why this stage or routing choice is being used now

When the persistent `tgtool` session is active, keep session state visible without fixed boilerplate.

Preferred behavior:
- mention tgtool activation and mode at session start
- mention a new mode only when the mode actually changes
- use brief status reminders only when useful during long work
- if the active mode materially changes execution strategy, say so once at the decision point
- repeat `如需结束本轮 tgtool 调用，请回复 tgend。` only when the user may need the reminder, near closeout, or after a long gap

Examples:

- `Using fast-path routing with $stream-coding because the task is a small local code change and the path is already obvious.`
- `Using $tool-advisor to confirm available capabilities, $stream-coding as the workflow skill, and $bucketmanager-s3control-e2e for local S3Control validation.`
- `Using $tool-advisor first, then brainstorming because the request is still in the design phase.`
- `Using $tool-advisor first, then $stream-coding, and adding find-skills because the current installed skills do not clearly cover the requested capability.`

## Completion recap

At the end of a routed task, prefer a very short recap when it adds value.

Use this shape:

- what skill path was used
- whether the routing worked well or exposed a gap
- whether memory should be updated
- whether a missing capability suggests using `find-skills` next time

Keep it compact. Use it only when it helps future execution or user understanding.

## Layered skill map (current repository)

Use this capability map as an index-first router. Keep routing progressive and minimal.

### L0: Workflow entrance and orchestration

- `tgtool`: top-level router and mode/state manager
- `using-superpowers`: delegate internal development workflow to superpowers
- `tool-advisor`: capability confirmation when uncertainty is real
- `find-skills`: capability-gap discovery/install path after explicit fallback approval

### L1: Core engineering workflow skills

- `brainstorming`
- `writing-plans`
- `executing-plans`
- `subagent-driven-development`
- `dispatching-parallel-agents`
- `systematic-debugging`
- `test-driven-development`
- `verification-before-completion`
- `requesting-code-review`
- `receiving-code-review`
- `finishing-a-development-branch`
- `using-git-worktrees`
- `planning-with-files`
- `stream-coding`

### L2: Memory, platform, and domain skills

Memory and docs:
- `claude-mem-codex`
- `openai-docs`
- `writing-skills`

Environment/domain operations:
- `jstorcli-yatc-jetice-ops`
- `bucketmanager-s3control-e2e`
- `multi-codex-orchestration`

AWS domain pack:
- `api-gateway`, `bedrock`, `cloudformation`, `cloudwatch`, `cognito`
- `dynamodb`, `ec2`, `ecs`, `eks`, `eventbridge`
- `iam`, `lambda`, `rds`, `s3`, `secrets-manager`, `sns`, `sqs`, `step-functions`

Specialized systems:
- `fuse`

Layer progression rule:

1. Start at `L0` and select one primary workflow path.
2. Add only the needed `L1` workflow skills for the current phase.
3. Pull `L2` domain/memory skills only when they materially improve correctness.
4. If required skill is locally present but disabled, use temporary toggle flow, then auto-reset at closeout.
5. Do not jump directly into broad `L2` domain routing when `L0/L1` already cover the task.

## Common routing patterns

These are defaults and examples, not mandatory routes.

- Small obvious question or local non-development task:
  - fast path + target workflow skill
- Tiny low-risk code change:
  - fast path or `tool-advisor` + `$stream-coding`
- Default development task:
  - `superpowers` workflow family first, with internal development flow delegated to `using-superpowers` instead of hard-coded here
- Direct `$stream-coding` development exception:
  - only for truly tiny, obvious, low-risk changes, or when no `superpowers` workflow skill fits better
- Planned execution:
  - fast path or `tool-advisor` + `using-superpowers`, unless a specific superpowers entry skill was explicitly requested
- Cross-session recall:
  - fast path or `tool-advisor` + `claude-mem`
- Multi-Codex orchestration:
  - `using-superpowers` + `multi-codex-orchestration` when the user explicitly wants multiple Codex agents and the task can be split into safe parallel roles; explicit `ruflo` backend requests should run `bootstrap_ruflo_backend.py` first and then execute real orchestration through the current session's `claude_flow` swarm/agent/task tools
- Complex multi-step task with persistent working state:
  - `using-superpowers` + `planning-with-files` when disk-backed planning, findings, and progress tracking would materially help
- Environment-aware execution:
  - `tool-advisor`
- Jstorcli / Yatc / Jetice / Jetlake operations:
  - primary workflow skill + `jstorcli-yatc-jetice-ops` as a domain support layer when those environment-specific operations are in scope
- Ambiguous design work:
  - fast path or `tool-advisor` + `using-superpowers`, unless a specific design skill was explicitly requested
- External research:
  - `tool-advisor` or direct trigger + `exa`
- Skill discovery:
  - `tool-advisor` + `find-skills`
- Local bucketmanager S3Control testing:
  - `superpowers` workflow family + `bucketmanager-s3control-e2e`, unless the change is truly tiny or another explicit skill choice overrides it

## Scope

This skill is the router and activator.

It should:

1. minimize routing overhead
2. choose the best fitting skills
3. keep context lean
4. move into execution quickly

It should not become a second planning layer that delays work.

## Index maintenance

Keep the lazy index fresh:

- source of truth for behavior remains each skill's `SKILL.md`
- `skills/tgtool/skills-index.json` is a routing index, not policy authority
- rebuild index after adding/removing/renaming skills or changing frontmatter descriptions
- rebuild command:
  - `node skills/tgtool/scripts/build_skills_index.js`

## Local context guard script (estimation mode)

Use local estimation when runtime percentage is not directly available to the agent.

Script:

- `skills/tgtool/scripts/context_guard.js`

Recommended call at each tgtool execution turn:

```bash
node skills/tgtool/scripts/context_guard.js \
  --input-text "<this turn's new user+assistant text>" \
  --context-limit 200000 \
  --fixed-overhead 2500
```

Recommended reset after final handoff + new session:

```bash
node skills/tgtool/scripts/context_guard.js --reset
```

Interpretation:

- `estimated_context_pct > 70`: warn
- `estimated_context_pct > 85`: preview
- `estimated_context_pct > 92`: critical
