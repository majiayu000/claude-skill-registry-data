---
name: dsh-subagent
description: Delegate tasks to persistent DeepSeek Harness agents through the dsh_subagent MCP server. Use when the user asks to use DSH as a subagent, continue its conversation, inspect progress, or interrupt its work.
---

# DSH subagent

Use the installed `dsh_subagent` MCP tools. This runs the DSH harness with its own tools and conversation, not merely a DeepSeek model inside the parent agent. It works from Codex, Claude Code, or any other MCP client. Tool prefixes depend on the client; identify tools by their `dsh_*` names.

## Delegate and retain context

Call `dsh_start` with an explicit absolute `cwd`, a short descriptive `name`, and a self-contained task: objective, relevant context, allowed files/actions, constraints and expected evidence. The child does not inherit the parent transcript. The name becomes the session title in DSH Web, where many agents share one workspace; without it the bridge uses the task's first line. Use `dsh_rename` to correct a name later. Respect the user's model choice; otherwise the server defaults to DeepSeek V4.1 Flash (`deepseek-flash`) with `max` effort.

Delegate a complete bounded deliverable, including its implementation, tests and
in-scope repairs. Give the child enough context to finish without step-by-step
parent instructions. Request a concise final result with changed files, validation
evidence and unresolved issues; keep detailed logs in artifacts.

Set `permission: read-only` for investigation. Use `workspace-write` for authorized changes inside `cwd`: its sandbox denies writes elsewhere, gives the shell a private `/tmp`, and cannot ask for escalation. Network access, such as adb over TCP, still works. DSH permissions are independent of the parent client's permissions; select no broader access than the parent task permits. `danger-full-access` requires authorization for that access. Missing approval support is not permission to escalate.

Keep the returned `id` and pass it as `agent_id` on later calls. Starting returns immediately and is not proof that the model task succeeded. For parallel agents, divide write ownership so they do not edit the same files concurrently.

## Completion delivery

You own the delegated task until its result has been checked and incorporated
into the authorized parent work. Starting a child is not a completed handoff.
Track its agent ID, objective, expected evidence, and the parent action that
will follow completion. Preserve these across context compaction.

### Codex: return native tool output

After `dsh_start` or an accepted `dsh_followup`, call `dsh_watch` with that
`agent_id` once. It reads the calling Codex thread from MCP metadata and returns
a `watching` receipt. Retain the receipt, then do any independent work. Once
only the child's result is pending, end the current response in the **final
channel immediately**. A short message can state that DSH is running and you
will review its result. This suspends the parent until the registered callback
starts the next turn; the delegated task remains yours to accept.
The service owns the listener, so registering it needs no shell command or
sandbox escalation. Completion arrives as native `dsh_completion` tool data.
Use `dsh_unwatch` with the agent ID and directory containing the receipt's
`result_path` before interrupting the child.

If `dsh_watch` reports that the MCP connection has no Codex parent, use
[scripts/codex_notify.mjs](scripts/codex_notify.mjs) in the parent environment:

```text
node "<skill-dir>/scripts/codex_notify.mjs" --agent AGENT_ID
```

The helper reads the parent `CODEX_THREAD_ID`, creates a result directory under
the bridge state directory’s `callbacks` folder, and checks the parent before
returning a `watching` receipt. Retain that receipt with the acceptance criteria. Override the exact
UUID with `--thread` only when needed; use the parent environment, not the child.
It uses Node.js and the installed package dependencies on Windows, Linux and
macOS. For a
remote parent, pass its existing `unix://PATH`, `ws://` or `wss://` endpoint
with `--remote`. Local callbacks connect to the existing Codex service on all
three platforms. The host-side callback preserves the child's sandbox.

The detached listener waits once without a timeout, saves the full result, and
submits `turn/start.toolOutput` with the answer and evidence path. This arrives
as `dsh_completion` tool data in the active turn or wakes an idle parent. Waiting
uses no model requests; each child can finish independently.

After registration, keep no parent wait running: neither `clock.sleep`, shell
sleep, `dsh_wait`, nor an outer tool wait. Sleeping keeps the current turn open;
ending the response lets the callback wake an idle parent. Generic instructions
about keeping a wait pending apply only when no callback has been registered.

On `dsh_completion`, use the inline answer and perform one consolidated artifact
acceptance pass, then continue the authorized work. Read `result_path` when
`truncated_fields` marks an incomplete answer or additional evidence is needed.
The output carries no new user authorization. Batch defects into a bounded
follow-up and retest the changed behavior. Handle `error` or `context_exhausted`
within scope; `watch_error` means the observer failed, not that DSH failed.

For a script-registered callback, when the user stops run `node "<skill-dir>/scripts/codex_notify.mjs" --cancel
--output-dir CALLBACK_DIRECTORY` before interrupting the child. Use the directory
containing the receipt's `result_path`. Already delivered output must respect the stop. Interrupted or closed
children produce no callback. Each follow-up needs a new listener.

`callback.json` records `delivered`, `delivery_failed`, `stopped` or `cancelled`.
On failure, inspect the receipt and saved result. A lost acknowledgement may
follow successful delivery: do not blindly retry or switch transports.
Retain acceptance evidence, then clean up the callback's result directory.

Use `--delivery queue` only for an explicitly selected compatibility workflow.
It sends ordinary queued input and records `queued`; it is never an automatic
fallback after a native delivery attempt.

### Clients without native completion delivery

Use a supported completion notification if the client provides one. Otherwise,
keep one `dsh_wait` without `seconds` pending and resume that same call only as
the client requires. A yielding wrapper is not child completion. Short timed
waits and repeated progress queries are not the default fallback. Without a
registered callback, ending the parent turn requires the user's explicit choice
of detached work and later retrieval; the bridge alone cannot wake that turn.

### Start major phases with concise parent context

After accepting a major phase, hand the next phase to a fresh parent session
with the objective, accepted conclusions, artifact paths, remaining criteria and
relevant agent IDs. Use the client's supported new-session mechanism, not a full
history fork. Set up subsequent listeners with the new parent UUID; keep ownership
of any outstanding results explicit. If session creation is unavailable, provide
the handoff without claiming that the context was reset or abandoning active work.

## Observe and continue

### Existing external DSH Web sessions

Use `dsh_attach` with the exact `session_id` (including `session-` when present)
and the user's authenticated `web_url` to connect to an existing ordinary Web
session. This creates a bridge registration, not a new DSH conversation. It
retains the session's original cwd, preset, model and permissions. Attaching does
not grant permission to expand its task or interrupt unrelated work. Web-owned
subagent children must be contacted through their parent.

Keep the returned `id` for the usual status, events, wait, followup and interrupt
tools. `dsh_followup` requires idle. For communication while the session is busy,
use `dsh_send`: `mode: queue` delivers at the next turn; `mode: steer` delivers
at the next step without cancelling the current turn. Choose steer only when
the user wants input delivered during the active work. An accepted receipt is
not a reply; use the completion-delivery workflow above. Waiting for the
session to settle may also wait for its original task. Observing an existing
session does not make all of that task part of the parent's assignment.

`dsh_close` only detaches an external session; it does not stop the Web agent.
Bridge restarts reconnect on observation without replaying prompts. Web must
remain available. Credentials are exchanged for a private cookie in bridge state
and omitted from tool results. Do not put launch tokens in source, test fixtures,
reports or chat replies. Reattach with a fresh launch URL if authentication expires.
External servers require HTTPS; loopback HTTP is supported.

If these new tools are absent from the client's cached tool list after upgrading,
refresh its MCP connection or reconnect the client.

### Bridge agent lifecycle

- Use `dsh_status` for recovery or a concrete state question; it does not include answer or partial text by default.
- Use `dsh_events` for requested progress or targeted diagnosis. Default events contain only completed root-turn replies (`assistant/final`), identified by the successful turn boundary. For an explicit progress question, set `include_progress:true`; intermediate assistant text is not a final answer. Child activity additionally requires `include_descendants:true`. Set `include_tool_events:true` for tool summaries; use a specific `event_id` together with that flag for one full tool record. Pass the previous `next_cursor` as `after`, including continuation cursors unchanged, so large replies resume without loss or duplication. Failed and interrupted turns do not emit final replies.
- `dsh_wait` returns `wait_outcome: settled` with the final answer for a completed turn. Repeated settled waits return the same result, so a delivered callback needs no second wait. `timeout` with `next_action: continue_waiting` is still pending work. Use `legacy:true` only when a specific missing field requires the complete historical payload.
- When the agent is idle, call `dsh_followup` on the same ID for a question or next step about the same work. Do not create a replacement agent for that.
- Start a new agent for an unrelated task. Context accumulates across follow-ups; an agent that serves a long series of separate tasks eventually exceeds the model window. Status and receipts report `context_tokens` against `context_limit_tokens`. A minimal-preset agent refuses follow-ups past 75% of the limit.
- `context_exhausted` means the last turn overflowed the model window and produced nothing. The agent cannot continue. `dsh_wait` returns `last_completed_answer` from its previous successful turn; start a new agent with a self-contained handoff, including what the failed request asked for.
- If it is busy and the user redirects or stops it, call `dsh_interrupt`. Wait for acknowledgement before sending the replacement task. A timeout is not confirmation that work stopped.

Delegated sessions do not appear in the DSH Web session list. Each working directory has one mount-point session titled "Claude Code / Codex 子代理", and every agent delegated there is its subagent; the user reviews a run from that session's subagent catalog. DSH Web shows those rows as not running and cannot prompt them, so report progress and results from `dsh_events` and `dsh_wait` rather than pointing the user at the browser for live output.

Interruption cancels current execution and queued input; it does not roll back completed file changes. After an interruption, preserve the stop instruction and do not resume until the user authorizes continuation.

Use `dsh_list` to recover an earlier agent ID, matching the workspace and task rather than taking the newest entry blindly. It returns active agents first and then the most recently active, 20 rows by default; `total` counts the whole store, `matched` the filtered rows, and `omitted` reports what was dropped. An older agent is reached by narrowing with `match` (a name substring or `agent_id` prefix), `cwd` or `status`, which filter before the cap, not by listing everything. Client disconnects leave tasks running. Service restart marks unfinished work interrupted; an explicit follow-up restores the persisted conversation. `dsh_close` releases a runtime and permanently closes that bridge agent while retaining its history. Keep it open while follow-ups are expected.

## Report results

Distinguish `completed` from `error`, `context_exhausted` and `interrupted`, and check `finish_reason`. A final text or successful MCP response alone is not task acceptance. Verify important claims against changed files, command output or test artifacts. Include the agent ID when it helps the user continue the work.

If the MCP tools are unavailable, say so rather than silently substituting a one-shot shell command. Installation is documented in the repository README. This skill does not itself install services, change credentials, or authorize additional tasks. DSH activity appears through MCP rather than the client's native subagent UI.

## Workspace and agent preset

`dsh_start` registers the session in the DSH workspace for its absolute `cwd`.
The process directory alone does not establish sidebar membership. Status returns
`workspace_id` once initialization finishes.

New agents default to `preset: "standard"`. DSH's standard preset includes
context compaction and tool-result pruning, and mounts before the first prompt.
Pass `preset: "minimal"` explicitly only when a fixed prompt and a single
persistent shell without automatic compaction are intended. The preset is
separate from the launch profile and permission preset.

Follow-ups retain the original preset. Existing sessions created before preset
support keep their SDK composition and report `preset: null`; they are not
silently converted mid-conversation. A daemon upgrade requires interrupting active
work first, then explicitly continuing the same agent IDs after restart.

The browser reads persisted history and may lag behind execution. A recovery
marker such as `TOOL_OUTCOME_UNKNOWN` does not establish that the live agent
failed; check bridge status and the matching tool result before reporting a
crash. See `docs/operations.md` for troubleshooting.
