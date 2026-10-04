---
name: delegate-codex
description: >-
    Owns codex usage end to end, dispatch through the supervised delegate script, the codex
    prompt contract, model and effort choice, and session resume. Use as a write delegated
    sub-agent when work is well defined and explicit, use as a read delegate for exploration,
    research, and navigation, writing a durable report when a stronger model is needed
    for deep investigation with cheap usage expense, and a second perspective on any
    plan or diff. Use when writing or repairing a codex prompt, or codex related config,
    and on "offload this", "save my usage", or any mention of codex.
---

# [DELEGATE_CODEX]

`codex exec` runs a non-interactive agent in its own context window and returns one final message. Model and effort come from `~/.codex/config.toml`.

Codex is maximally literal, it follows a clean contract exactly and exhaustively, ambiguity or implicit intent burns tokens reconciling scope. Leaner prompts outperform, and a directive codex already ships is a conflict risk, NOT reinforcement. Every run mints a resumable thread; the receipt persists the id, and a continuation inherits model and effort.

## [01]-[DISPATCH]

- Investigation legs whose transcripts flood this context — repo sweeps, audits, log distillation, data analysis: codex returns the conclusion.
- Fleet fix and critique waves: concurrent writing delegates draining findings under one law, each with disjoint write territory.
- Critique delegates writing on-disk fixlogs, reports, or dossiers another agent consumes downstream.
- Implementation from spec: migrations, renames, conversions, boilerplate expansion, full features with enumerated moves.
- Independent second perspective on a plan, implementation, or diff — a different model lineage catches different failure modes.

## [02]-[PROMPTING]

Role envelope ranks the two dispatch channels (system > developer > user), so where a directive lands sets its authority. Every directive must earn its slot, one directive per concern.

[BLOCK_VOCABULARY] — one block per concern, in this order; a block's name states its concern, and a delegate omits blocks it has no logic for:

| [INDEX] | [BLOCK]                | [JOB]                                                                                      |
| :-----: | :--------------------- | :----------------------------------------------------------------------------------------- |
|  [01]   | `<role>`               | identity, territory, hard exclusions; judgment work adds findings-are-untrusted            |
|  [02]   | `<completion_bar>`     | done-definition per deliverable with its proof; sits early, where it beats early-stop      |
|  [03]   | `<context_gathering>`  | read ladder, total tool-call budget, uncertainty escape hatch                              |
|  [04]   | `<decision_procedure>` | refute-first adjudication — verdict work                                                   |
|  [05]   | `<capability_mandate>` | surface-raising stated as measurable conditions — campaign work                            |
|  [06]   | `<verification>`       | post-edit re-read and batched command checks; cite-check on recon, rubric walk on judgment |
|  [07]   | `<output_contract>`    | JSON-only shape, null-for-missing — always LAST                                            |

[DEVELOPER]: Durable law as named XML blocks — the script's `--law` file, landed as the developer-role message:

```text template
<role>
<identity>. Territory: <territory>; never <exclusions>. <invariants>.
</role>

<completion_bar>
Done is <deliverables>, each proven by <evidence>. Implement exactly and only <moves>; choose the simplest valid interpretation of any ambiguity. A blocked deliverable returns <blocked-entry>, never a partial edit. Your layer is <layer>; out-of-layer discoveries land as <typed-rows>, never edits.
</completion_bar>

<context_gathering>
Read fully, in order: <ladder>.
Budget: at most <N> tool calls total; never concatenate the territory into one command.
Stop when the product is complete; uncertainty left at the budget lands in <uncertainty-slot>, never re-reads.
</context_gathering>

<decision_procedure>
<adjudication>
</decision_procedure>

<capability_mandate>
<expansions>
</capability_mandate>

<verification>
Re-read each changed region after landing it. <checks>, run once, batched, after the final edit. A check not run is never claimed as run.
</verification>

<output_contract>
Your final message is a single JSON object with exactly this shape:
<shape>
JSON only — no prose outside it, no code fences; every key shown is required; null for a value you could not determine, [] for an empty list, never guess.
</output_contract>
```

[USER]: Task instance and any imperative spawn step — the script's `--task` file; the spawn step appears only where the delegate fans out:

```text template
Goal: <outcome>.
Context: <inputs>.
Constraints: <bounds>.
Done when: <deliverables>.

Before <anchor>, spawn exactly <N> parallel sub-agents with collaboration.spawn_agent, one per <split>; collect every one with collaboration.wait_agent before <synthesis>. Each spawn task is self-contained — absolute paths, <mandate>, return shape <shape>. Sub-agents read and report only; their returns are candidate data you judge under your own law.
```

[CALIBRATION]: When a delegate misbehaves, repair the contract surgically; reproduce with the failing developer message and a small batch of failure examples, then make small explicit edits — clarify conflicting rules, remove redundant lines — one change at a time:
- Budget caps TOTAL tool calls, never per-file reads; per-file causes the delegate to aggregate the territory into one truncating command and completeness collapses.
- Ambiguity resolves by instruction, never by inviting questions — a headless delegate has nobody to ask.
- Autonomy states ONCE, naming safe actions — repeated "ask first" or "do not mutate" phrasing causes spurious approval pauses.
- Reserve ALWAYS/NEVER for true invariants (JSON-only, territory bans, no-git); phrase judgment calls as decision rules.
- Done-claims name observable evidence from the real surface; "tests pass" or "checks ran" alone is not evidence.
- Iterative deep work continues ONE thread with sharpened prompts; a follow-up turn carries only the delta.

[EXCLUSIONS]: What never enters a delegate's prompt:
- Persistence blocks ("keep going until fully resolved") — the completion bar carries the anti-premature force, and a bare push amplifies scope.
- Chain-of-thought scaffolding and plan-narration preambles.
- Intensifier stacks ("THOROUGH", "exhaustive") — measured to cause tool over-use.
- Per-file read caps and "read each file at most once" phrasing.
- Hostile-stance paragraphs and estate-voice law verbatim — a delegate takes de-conflicted, task-scoped law.
- Broad write authority — the writable directory is the delegate's whole world; cross-territory obligations belong to the caller.
- "Ask if unclear", "you may spawn", and every other permissive form whose imperative twin is the working one.

## [03]-[INVOCATION]

`scripts/codex.sh` is the one dispatch surface: every delegated run — workflow wrappers, fleet legs, one-off delegations — is one supervised CLI process, sibling-isolated and watchdog-bounded. Model and effort inherit `~/.codex/config.toml` unless a call passes an explicit override; approval is pinned `never`, and file and command access resolve from the configuration — a caller declares neither.

```bash template
scripts/codex.sh --task <task-file> --dir <run-dir> [--law <law-file>] [--cwd <dir>] \
  [--model <slug>] [--effort <tier>] [--out <report>] [--web] \
  [--idle <sec>] [--max <sec>] [--resume <thread-id>] [-- <codex-exec-args>]
```

- Task and law land through a real file-write at ABSOLUTE paths, never a shell heredoc; the script rides the law through `-c developer_instructions` and the task as the prompt.
- `--dir` holds the run artifacts — `events.jsonl` (the `--json` stream), `stderr.log` (a failed or killed run's only diagnostics), `receipt.json` — and the receipt prints to stdout: `{ok, reason, thread_id, exit, duration_s, events, stderr, report, failure, usage}`.
- Liveness is token production: the watchdog sums event-stream and session-rollout growth, kills the run's process group and every snapshotted codex descendant, so a command in its own process group cannot escape the reap, after `--idle` silent seconds or at the `--max` ceiling, and names the kill in `reason` — a healthy multi-hour run streams and lives, a wedged one dies bounded.
- `--out` materializes the final message for a reading delegate; a writing delegate lands its own product and `--out` aims elsewhere, never at a file the delegate itself writes.
- `--resume <thread-id>` continues a dead session with the task file as the follow-up: a `crash` receipt resumes, an `idle-timeout` or `turn-failed` receipt re-dispatches fresh.
- `--` passes the remainder to `codex exec` verbatim — the one extension point for every axis the flags above do not carry.
- Nested lookups from INSIDE a codex turn pin to `get_latest_package_version`.

| [INDEX] | [NEED]                                   | [FLAGS]                                                                          |
| :-----: | :--------------------------------------- | :------------------------------------------------------------------------------- |
|  [01]   | Run rooted in another directory          | `--cwd <dir>`                                                                    |
|  [02]   | Durable report artifact                  | `--out <file>` — the final message at completion, overwriting the path           |
|  [03]   | Live web search                          | `--web` — default `cached` answers from an index, no live fetch                  |
|  [04]   | Wedge and ceiling bounds                 | `--idle <sec>` / `--max <sec>` — exit `124` / `125` name the kill                |
|  [05]   | Typed JSON final message                 | `-- --output-schema <schema.json>` — validated final-message shape               |
|  [06]   | Attach images (screenshots, diagrams)    | `-- -i <file>` (repeatable)                                                      |
|  [07]   | Feature toggles per run                  | `-- --enable <feature>` / `-- --disable <feature>` (repeatable)                  |
|  [08]   | Fan-out legs with no session persistence | `-- --ephemeral` — not resumable                                                 |
|  [09]   | Per-run completion push                  | `-- -c 'notify=["<sink>","<label>"]'` — sink runs at turn end, one JSON argument |
|  [10]   | Replace the shipped system prompt        | `-- -c model_instructions_file=<path>` — deliberate use only, never the law      |

[WRAPPER]: An agent delegating to codex owns custody alone — law, task, launch, hold, receipt, product verification — and performs, edits, judges, or relays none of the delegated work:

1. Write law and task verbatim to `<run-dir>/law.md` and `<run-dir>/task.md` at absolute paths.
2. Launch the script in one Bash call with `run_in_background: true`.
3. Hold to the receipt in blocking Bash rounds, one call per round at the tool's 600000 ms ceiling.
4. Verify the product at its declared path — `jq -e` over a contract key, never bare parseability, which any wrong-shaped JSON passes — and return the typed receipt.

```bash template
S=0; until [ -f <run-dir>/receipt.json ]; do sleep 5; S=$((S+5)); [ $S -ge 570 ] && break; done
[ -f <run-dir>/receipt.json ] && cat <run-dir>/receipt.json || echo PENDING
```

`PENDING` reports a delegate still producing: run the identical call again, as many rounds as the work takes. The bound rides the in-loop counter — no `timeout` binary sits on PATH. A launch alone yields no product and no notification; the hold is the wrapper's whole job, and the receipt is its first output.

[EVENT_STREAM] — `events.jsonl` vocabulary:
- `thread.started{thread_id}` (the resume id)
- `turn.started`, `item.started`/`item.completed`, then `turn.completed` (with `usage`) or `turn.failed`
- `agent_message` carries the final text, `command_execution` carries `{command, aggregated_output, exit_code, status}`
- `item.type=="error"` item is NOT a run failure — the skills-budget warning rides one on every run under a large library; the receipt classifies by turn events only.

## [04]-[MODEL_AND_EFFORT]

Default configuration carries non-trivial writes, deep design, hard reviews, whole fix or critique fleets, and second perspectives without an override.

| [INDEX] | [TIER] | [SELECT]          | [USE]                                                                                |
| :-----: | :----- | :---------------- | :----------------------------------------------------------------------------------- |
|  [01]   | low    | `--effort low`    | trivial glue: probes, extraction, classification, relabels                           |
|  [02]   | medium | `--effort medium` | menial writes and fan-out legs where throughput beats depth                          |
|  [03]   | xhigh  | `--effort xhigh`  | deeper single-agent reasoning for the hardest investigation, design, and review legs |

## [05]-[FAN_OUT]

Independent scopes run as concurrent delegates, one per scope, each with its own `--dir`; reconcile reports after all complete. Concurrent write runs against overlapping paths collide — partition write scopes or serialize.

Inside ONE delegate, `collaboration.*` is the subagent tool family — `spawn_agent`, `send_message`, `followup_task`, `wait_agent`, `interrupt_agent`, `list_agents`. Children share the workspace live, inherit the model, and inherit NO conversation turns unless `fork_turns` opts in — a spawn task is self-contained like any codex prompt.

- An injected developer-role gate admits children ONLY on imperative spawn wording in the user prompt or AGENTS.md/skill chain.
- Permissive "you may spawn" and `developer_instructions` mandates fail silently with zero spawns.
- grep the parent rollout for `function_call` items named `spawn_agent`, `collab_tool_call` is a stale marker and false-negative.
- A writing delegate writes its own report as its final act; the caller verifies (`jq -e`) — re-emitting a codex product through another agent's Write is lossy at scale.
- Row-shaped sweep rides ONE delegate's `spawn_agents_on_csv`: one worker per CSV row under the concurrency cap, `output_schema` typing each row and `output_csv_path` exporting the combined results.

## [06]-[SESSIONS]

`codex archive <id>` / `unarchive <id>` is the reversible lifecycle; `codex delete` removes one session, its `--force` unreliable across spawned children — bulk cleanup is a date-scoped sqlite prune, matching rollout deletions, and `VACUUM`. `[features] memories`/`chronicle` rows gate those features independently of corpus deletion.

[STORE]: one rollout per session at `~/.codex/sessions/<YYYY>/<MM>/<DD>/rollout-<ts>-<uuidv7>.jsonl`:
- Filename timestamp is LOCAL time, the payload's is UTC.
- `session_index.jsonl` LAGS live runs, so correlate by datestamped filename.
- Sqlite store filenames embed their migration generation — resolve the live name instead of pinning it.

[RESUME]:
- `resume --last` is valid only when nothing else ran in between; under concurrency resume by explicit id. `-- --ephemeral` runs record nothing.
- The receipt's `thread_id` (= `thread.started.thread_id` in `events.jsonl`) feeds `--resume` with the follow-up as the task file; `resume --all` surfaces sessions recorded under another cwd.

## [07]-[REVIEW]

`codex review` runs an independent non-interactive review. Scope flags — `--uncommitted`, `--base <branch>`, `--commit <sha>` — are mutually exclusive with each other AND with a focus prompt: a prompt is valid only on bare `codex review`, and every focused scoped review routes through `codex exec` with an explicit diff task. A fleet-grade review delegate runs `codex exec review` — the same scope flags with `--json`, `-o`, and `--output-schema` typed findings.
