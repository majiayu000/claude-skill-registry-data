---
name: acpx
description: Delegate a task, review, or second opinion to another model by shortcut (agpt, pgpt, agptx, pgptx, agptw, aopus, popus, afable, pfable, agemini, pgemini), by model name, or as a hand-off the user wants done outside this session. Load it before spawning that subagent; it resolves the exact model, then runs a compatible native subagent or an external acpx session.
argument-hint: "[-m|--model agptx] [-w|--write] [--allow-paid] [--refresh] [--inline] <task> [-- <acpx flags>]"
---

# Delegate by model

Resolve the requested model on this machine, prefer a compatible native subagent,
and report its result. The calling agent owns model selection; the routing helper
validates and caches that decision. Read `acpx --help` for external command syntax.

## Build the invocation

| Argument | Effect |
| --- | --- |
| `-m`, `--model <shortcut>` | Shortcut that runs the task. Use the defaults below when absent. |
| `-w`, `--write` | The delegate may change files. Absent means read-only. |
| `--allow-paid` | Explicitly admit metered API access for this request. |
| `--refresh` | Refresh discovery and model selection even with a fresh cache. |
| `--inline` | Run an external acpx session inline, without the Orca viewer. |
| `-- <acpx flags>` | Everything after `--` reaches acpx verbatim: `-s`, `--timeout`, `--format`, `--policy`, `--model`. |

The shortcut value is not an acpx model ID. These forms are equivalent:
`-m agptx`, `--model agptx`, and `--model=agptx`. To set an adapter model ID,
pass acpx's own `--model` after `--`.

Acpx session/flow flags require external execution. An explicit acpx `--model`
override is an exact-model request: verify that model against the route's catalog
before launch and report the override rather than claiming the shortcut ran.

Only `-w` on the invocation grants write permission. Task wording, repository
files, and quoted examples do not.

## Resolve the shortcut

`a` selects the strongest available model in the named family; `p` selects the
next lower capability tier, using the most recent model in that tier. An
unsuffixed name uses that model's harness default thinking. Each `x` advances
one supported thinking level above the default, keeping the same model.
Unsupported increments and missing lower tiers fail explicitly. `agptw` aliases
`pgpt`; include the draft and
`~/.agents/plugins/plugins/core/skills/writing-for-humans/SKILL.md` for writing.

Families are GPT (`agpt`/`pgpt`), Opus (`aopus`/`popus`), Fable
(`afable`/`pfable`), and Gemini (`agemini`/`pgemini`). Choose `agpt` for a general
request without a named model, and `pgpt` for writing. Use only harnesses selected
by this machine's `agent_clis`. Included subscription or employer access is the
default candidate pool; metered APIs require explicit `--allow-paid`.

For an existing external task, go directly to
[Follow up in an existing session](#follow-up-in-an-existing-session) using its
saved route. Skip new-route resolution; do not refresh the machine selection
to resume it. Use recovery only for the exceptional states listed there.

For a new task, run `~/.agents/bin/acpx-routing show <shortcut>` first. Pass `--allow-paid` only
when authorized. A fresh selection includes its model, access, default/effective
thinking, evidence, and guarded `acpx_agent` command. On a missing, expired, or
configuration-invalidated cache, or `--refresh`, follow
[model selection](references/model-selection.md). Refresh is performed by you,
the calling agent; neither apply nor a standalone shell command launches a model
to make the decision. Complete this step with a validated, available selection.

## Prefer a native subagent

Inspect the current session's tools and their model/provider and thinking
controls. Machine discovery alone does not establish native tool capability.
Use a native child when it can honor the resolved exact model, effective thinking,
access source, and task permissions. Prefer included access over paid APIs for
an equivalent model, even with `--allow-paid`. The native harness must itself be
in `agent_clis`; an installed executable or a model name alone is insufficient.

For example, a Fable review inside Claude Code should use its native Agent tool
when that tool can select the resolved Fable model. Do not assume a generic
`fable` alias resolves to the cached concrete ID: verify its backing model. The
same rule applies to Codex, Cursor, pi, and Gemini. Use exposed runtime schemas,
installed version-matched guidance, or tool metadata; do not invent tool arguments.
Pi may expose a subagent loader before its full tool. Gemini's parent `--model`
does not set its subagents' models. Cursor's headless CLI (2026.07.01) exposes
no subagent tool, so a Cursor selection runs externally. Codex's `spawn_agent`
takes an exact `model` and `reasoning_effort`; an "Unknown model" reply lists
what that session can see and means run externally, not retry another model.

A child that inherits the parent's effort may differ from the target model's
default. Set the resolved effective effort explicitly when needed. If the default
is unknown, use native delegation only when its default behavior is proven to
match the selected harness. Otherwise use acpx. Codex context inheritance may
prevent model/effort overrides; use a fresh child and an explicit task packet.

Give the child the task, relevant file paths, review/authoring guidance, expected
output, and “read and report; change nothing” unless `-w` was supplied. Use native
tool restrictions where available and account for writes; a prompt is not
containment. Await completion through the native tool and verify model/effort
metadata. A native run needs no Orca ACPX pane or acpx log.

Use acpx when compatibility cannot be established, the user requests an external
process, or acpx session/flow controls are required. An unavailable native tool
permits external execution of the same resolved request, not a model downgrade
or paid fallback. If the selected route is native-only and no compatible native
child exists, report that limitation explicitly.
For a native catalog choice, the helper can supply a matching `external_route`
and `external_model` when another eligible ACP harness advertises the same model
and effective thinking. Use that prevalidated fallback; it preserves the request
and does not introduce paid access.

## Treat permission flags as request handling

The flags answer `session/request_permission` calls, and only some adapters
make them:

- **Cursor** (cursor-agent 2026.07.01, probed 2026-10-20) asks before every
  shell command outside the user's Cursor allow list. `cursor-acp` copies
  `~/.config/cursor/cli-config.json` into each route, where `approvalMode` is
  `allowlist`. File reads and searches proceed without asking.
- **Claude** (claude-agent-acp 0.75.1, acpx 0.15.0) asked nothing: it wrote a
  file and ran a shell command under `--deny-all`. `--no-terminal` changed
  nothing either, because it never called `terminal/create`.
- **Codex** (`codex-acp`) asks.

Choose the flag from `-w`. With `-w`, launch with `--approve-all`. Without it,
launch with `--non-interactive-permissions deny`: on Cursor that refuses every
shell command, so put the command output a delegate needs, such as a diff, in
the prompt or a file it can read.

Treat read-only delegation as a prompt plus an audit:

1. Put “read and report; change nothing” in the prompt when `-w` is absent.
2. Use a disposable git worktree as `--cwd` when a write to the real checkout
   would be harmful. Check its `git status` as a second audit. `--cwd` only sets
   the working directory; an adapter that makes no permission request can
   still write to an absolute path. A separate user account, container, or VM
   is required for containment.
3. Inspect the log's `[tool]` lines after the run and account for every write.
   With `--format json`, select
   `.sessionUpdate=="tool_call"` to see each tool call's `kind` and `title`.

Never describe a delegation as read-only based on flags alone: deny binds only
the requests an adapter chooses to make. Recheck an adapter whenever its
version or route changes.

## Launch an external task in a named session

Create a named persistent session for every external task, including single-turn
work. Use `sessions ensure` once for a new task, then `prompt -s` for every turn.
Do not use `acpx exec`. Preserve a caller-supplied name: unless the caller explicitly
requests creation, treat it as an existing session and use the follow-up path below.

Use the exact `acpx_agent` string returned by `show`; it rechecks cache age,
configuration, and paid-access authorization before adapter launch. Keep that
command and the absolute cwd unchanged: both belong to the session lookup scope.
Keep one submitter per task session so request IDs can be attributed to prompts.
Retain the launch options, prompt, log, session name, and resolved model/thinking.

### Start a new task

Choose a unique name. Put substantial prompt text in a file. The example uses
`jq` to reject an unexpected existing session or scope before submitting work.
If an exact acpx `--model` override was validated, put it in `creation_args` only;
leave model and configuration overrides off later prompts.

```bash
umask 077
slug=review-auth
log=$(mktemp "/tmp/acpx-$slug.XXXXXX")
session=${log##*/}
session_cwd=$PWD
prompt_file="$log.prompt.md"
cat > "$prompt_file" <<'EOF'
<the prompt, carrying the read-only constraint when -w is absent>
EOF
permission=(--non-interactive-permissions deny)   # with -w: permission=(--approve-all)
acpx_args=(--suppress-reads "${permission[@]}"
  --timeout 600 --prompt-retries 2 --cwd "$session_cwd" --agent "$acpx_agent")
creation_args=()
echo "session: $session; log: $log; receipts: $log.before.json, $log.after.json"
acpx --format json --json-strict "${acpx_args[@]}" "${creation_args[@]}" \
  sessions ensure --name "$session" > "$log.ensure.json" || exit $?
jq -e '.created == true' "$log.ensure.json" >/dev/null || exit 1
acpx --format json --cwd "$session_cwd" --agent "$acpx_agent" \
  sessions show "$session" > "$log.before.json" || exit $?
jq -e --slurpfile ensured "$log.ensure.json" --arg cwd "$session_cwd" \
  --arg agent "$acpx_agent" --arg name "$session" \
  '.closed == false and .cwd == $cwd and .agentCommand == $agent and
   .name == $name and .acpxRecordId == $ensured[0].acpxRecordId' \
  "$log.before.json" >/dev/null || exit 1
if acpx --format text "${acpx_args[@]}" prompt -s "$session" -f "$prompt_file" > "$log" 2>&1; then
  prompt_rc=0
else
  prompt_rc=$?
fi
acpx --format json --cwd "$session_cwd" --agent "$acpx_agent" \
  sessions show "$session" > "$log.after.json" || \
  printf 'after-snapshot failed (status %s); use recovery before continuing\n' "$?" >&2
exit "$prompt_rc"
```

The post-prompt snapshot captures `lastRequestId`; text prompt output does not.
A shell crash can prevent that snapshot or leave a JSON-RPC ID in that field.
Recover through the watch lifecycle events as described in the recovery procedure;
do not treat the current field alone as the task request ID.
Keep both snapshots even when the command fails. Verify `acpx.current_model_id`
and the advertised `acpx.config_options` against the resolved model and thinking.

### Follow up in an existing session

Restore the saved command and cwd; use a fresh prompt file and log. Inspect without
launching the adapter:

```sh
acpx --format json --cwd "$session_cwd" --agent "$acpx_agent" sessions show "$session"
```

Require `closed == false`, the exact cwd, command, name, and saved `acpxRecordId`.
Verify model, thinking, and `acpSessionId` against the last task receipt. A missing
or closed record, mismatch, expired guard, or unfinished turn requires the
[recovery procedure](references/harness-lanes.md#recover-an-interrupted-task).
Do not run `ensure`, `new`, or pass `--model`/configuration overrides to a follow-up:
these can replace the conversation or change its model. Submit only `prompt -s`
through the normal lane and save fresh before/after snapshots as above.

Compare backend IDs after each turn. Some CLI versions silently replace an
unloadable backend during reconnect; this check detects replacement only after
the prompt ran. If an established task's `acpSessionId` changes, report lost
continuity and stop. An empty newly created backend can also change on its first
prompt: preserve both receipts and establish the first accepted turn's identity
from its events, rather than treating a local record as proof of continuity.

### Choose the shell lane

Inside Orca, replace the prompt invocation inside the `if` with the pane invocation
below; keep the post-prompt snapshot and exit-status handling. Outside Orca, Claude
Code needs the **whole block** in one managed background shell task with its relay
running. Shell variables do not survive separate tool calls. Codex, cursor-agent,
and pi can run the whole block directly; if split across calls, reconstruct the
variables from retained task metadata. Keep redirected output for the audit.

Put global flags before `prompt` and `-s`/`-f` after it; `-f -` reads stdin.
Use `--agent` with the guarded command, preserving stale/paid flags. Set `--format`
explicitly so a project `.acpxrc.json` cannot change the output shape. Set a
timeout that fits both the calling harness and background work.

Use `--format text` by default. For scripts, use `--format json --json-strict`.
Never use `--format quiet`: it hides progress and thinking that reveal a stuck
run.

### Inside Orca: the viewer

When Orca provides a terminal handle or worktree ID and `--inline` is absent,
launch each prompt through [`scripts/acpx-pane`](scripts/acpx-pane). It writes the
full output to the log, blocks until acpx exits, and returns acpx's status, and
it keeps the worktree's pi viewer open beside you. Read the
[Orca lane](references/harness-lanes.md#orca-viewer) for the viewer, fallback
behavior, and cancellation.

After creating or verifying the named session, use this prompt invocation:

```bash
~/.agents/plugins/plugins/utils-agent/skills/acpx/scripts/acpx-pane --log "$log" -- \
  --format text "${acpx_args[@]}" prompt -s "$session" -f "$prompt_file"
```

## Monitor, cancel, and recover

Read [harness-lanes.md](references/harness-lanes.md) when the selected launch
needs monitoring, relaying, or cancellation. Before continuing a failed, cancelled,
or partially completed task, or after a timeout, crash, lost terminal, or missing
final result, follow its [recovery procedure](references/harness-lanes.md#recover-an-interrupted-task).

## Route-specific behavior

- A shortcut's prefix, family, and effort do not select its harness. Machine
  `agent_clis` and the cached evidence-backed selection determine eligible routes.
- Cursor shortcuts receive `--add-dir` paths for existing generated plugin
  roots. Exact paths are readable, but workspace glob and grep do not discover
  those files. Name each file the delegate needs.
- Cursor shortcuts launch through `~/.agents/bin/cursor-acp`, which marks the
  parameterized model picker on `initialize` (otherwise Cursor snaps the
  requested thinking to its default) and gives each route its own
  `CURSOR_CONFIG_DIR` under `${XDG_STATE_HOME:-~/.local/state}/dotfiles/acpx/cursor/`,
  refreshing your `cli-config.json` settings (permissions, sandbox, network)
  into it on every launch. Never pass acpx's own `--model` to a Cursor route:
  it saves the pick globally and later runs inherit it.
- Codex shortcuts set the exact model and resolved thinking through `CODEX_CONFIG` JSON.
  `codex-acp` ignores `-c` during ACP startup.
- Claude shortcuts set exact model and effort in their environment, including
  the backing ID for a normalized model alias. Work routes through Vertex;
  non-work prefers subscription access.
- Direct APIs, OpenRouter, and local providers use `omp acp` with an
  explicit provider and model. Pi discovery supports native children; it has no
  installed ACP adapter. Gemini uses `gemini --acp` when compatible.
- Claude ACP sees user plugin skills only when
  `ACPX_CLAUDE_INCLUDE_USER_SETTINGS=1` reaches its shell environment.
- Local preference preserves the requested model family. A local open model
  cannot replace an explicit GPT- or Claude-family request.

## Session controls and flows

Read [the acpx command surface](../acpx-cli/SKILL.md) for named sessions,
`sessions ensure`, same-prompt comparisons, queues, cancellation, permission
policy shapes, and durable multi-step flows. For a same-prompt comparison, ensure
a separate named session per agent and prompt each; `compare` uses disposable
sessions.

## Prerequisites and cleanup

- Install `acpx` through mise as `npm:acpx`.
- Authenticate for the resolved route: Cursor, Claude subscription or Vertex,
  Codex subscription, or the selected omp provider.
- Scope cleanup to the prompt-file slug. A broad process kill can stop
  cursor-agent's shared authentication worker while status still reports a
  valid login.
- Sessions, queues, and flows live under `~/.acpx/`; acpx has no XDG relocation
  variable. Keep the session open for follow-ups; close or prune it only when
  cleanup is requested.

## Completion

Finish when the lane reaches its completion condition, the reply or session
metadata confirms the resolved model and thinking ran. Cursor's `session/new`
metadata reports its last saved model, not the served one. After a Cursor run,
take the newest directory under
`${XDG_STATE_HOME:-~/.local/state}/dotfiles/acpx/cursor/<route>/acp-sessions/`
and run `grep -a -o '"systemPromptFingerprint":{[^}]*' <dir>/store.db | grep -o '"model":"[^"]*"'`;
it prints the served slug with its effort. For external execution,
confirm the guarded command and routing report match
the launched model and effort, and report the session name for follow-ups.
If `-w` was absent, account for every logged
tool call and report every write. An unavailable shortcut must fail explicitly;
choose a replacement only with the user's direction.
