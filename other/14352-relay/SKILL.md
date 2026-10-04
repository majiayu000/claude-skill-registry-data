---
name: relay
description: Find local Claude sessions or saved Codex threads, then send a short message or handoff. Codex delivery queues through its shared App Server daemon or a local Claude inbox socket; use after an explicit cross-session request or live xm:toss notice.
---

# x-relay — local session messages

<Purpose>
`/xm:relay` uses Claude Code's native `ListAgents` and `SendMessage` for Claude-to-Claude messages. Its shell adapter also sends Codex messages to a live local Claude inbox socket, and queues Codex messages through the shared App Server daemon. It does not create sessions, move conversation history, publish externally, or replace the durable `/xm:toss` inbox.
</Purpose>

<Use_When>
- The user asks to list reachable local Claude sessions or saved Codex threads.
- The user asks to send a short message or a work handoff to one specific local session.
- `/xm:toss` was asked to notify a session about a report it already recorded.
</Use_When>

<Do_Not_Use_When>
- The content must survive until the receiver acts on it: file it with `/xm:toss` instead.
- The recipient is a cloud, Remote Control, or other-machine session, or no session is running and one would have to be started.
- The goal is to get another session to do something this session's permissions refused.
</Do_Not_Use_When>

## CLI Invocation

> **⚠ Call `xm relay <command>` directly. Claude Code's Bash tool starts a fresh shell on every invocation — shell functions (`xrelay()`) defined in one call do NOT persist to the next, causing `command not found: xrelay`. Never define a helper across calls; always use the dispatcher.**
>
> **Fallback** (only when `xm` is not in PATH — rare; `${CLAUDE_PLUGIN_ROOT}` is NOT exported to Bash subprocesses, so don't rely on it bare):
> ```bash
> XRELAY_CLI=$(ls -d ~/.claude/plugins/cache/xm/xm/*/lib/x-relay-cli.mjs 2>/dev/null | sort -V | tail -1)
> [ -n "$XRELAY_CLI" ] || XRELAY_CLI=~/.codex/xm/lib/x-relay-cli.mjs   # Codex global bundle
> node "$XRELAY_CLI" <command> [args]
> ```
>
> **Forbidden:** `XRELAY="node ..."; $XRELAY sessions` — zsh treats the quoted string as a single command and fails.

## Modes

| Invocation | Result |
|---|---|
| `/xm:relay` or `/xm:relay sessions [project]` | Overview: live Claude sessions and saved Codex threads in separate sections |
| `/xm:relay sessions [project] --provider claude\|codex` | Show only that provider's full candidate list |
| `/xm:relay send <session> <message> [--provider claude\|codex]` | Send or queue the user's short message for one selected session |
| `/xm:relay handoff <session> [topic] [--provider claude\|codex]` | Send or queue a concise current-work summary |

Natural-language equivalents use the same modes. The provider default below applies to `send` and `handoff`; listing without `--provider` is the overview. Default to Claude in Claude Code and Codex in Codex. In Codex, use `--provider claude` to target a local Claude session; in Claude Code, use `--provider codex` to target a Codex thread. The shell CLI uses Claude Code's local inbox socket protocol for Codex-to-Claude delivery on macOS and Linux, so it supports live local sessions only. This adapter follows the observed `peerProtocol: 1` frame format, which is an internal interface that may change; if the session advertises another protocol, report it as unavailable. Windows named pipes are not supported. Never handcraft a socket frame, use `claude -p`, or start a new session as a substitute for a missing recipient.

In a source checkout whose installed `xm` dispatcher predates `relay`, run `node xm/lib/x-relay-cli.mjs` from that checkout instead. Use the same `sessions` or `send` arguments; do not read a stale installed bundle and claim it has the new adapter.

## Overview listing (both providers)

A bare `/xm:relay`, or `sessions` without `--provider`, lists both providers. Claude and Codex delivery differ — a live Claude session receives a message now, a saved Codex thread only queues it — so never merge them into one table.

1. Claude section first, labeled live. In Claude Code, build it with `ListAgents` under Claude recipients; in Codex, with `xm relay sessions --provider claude` under Sending from Codex to Claude.
2. Codex section second, labeled saved threads, queued delivery, live status unverified. Run `xm relay sessions` once for the full inventory. If the current checkout resolves to exactly one unarchived registry project by the canonical-path rule in Claude recipients step 4, or the user named a project, also run `xm relay sessions --project <id>`; both calls may share one Bash invocation.
3. Show at most 5 Codex threads in the CLI's order — daemon-loaded threads (`loaded: true`) first, then newest: the project-matched ones when a project resolved, otherwise the overall list, and say which. Mark loaded rows as open in the daemon with their `app_server_status`. Thread names are often `null`, so show the full UUID, working directory, and relative last activity. Never shorten the UUID; a send still requires the exact ID. Close with one line giving the remaining count and `/xm:relay sessions --provider codex` for the full list. Mention `partial: true` when present.
4. A Codex failure must not hide the Claude section. If the daemon is unavailable or `xm relay` fails, print one line with the CLI's error under the Codex heading and do not start the daemon. If the Claude listing fails, do the same in reverse.
5. The overview only lists. A follow-up `send` or `handoff` still re-lists the chosen provider and requires its exact address or UUID.

## Claude recipients

1. Call `ListAgents` for each `sessions` request and immediately before each send. Consider only independent Claude sessions that the tool identifies as local to this machine. Subagents, teammates, cloud sessions, and Remote Control sessions on another machine are outside this mode.
2. Show the tool's session address or disambiguating identifier, name, working directory, and status. Do not infer that a saved session or a process found by scanning is addressable. If the tool withholds a directory, show it as unknown.
3. For a direct `send` or `handoff`, require a unique address returned by the fresh listing. If a name matches several sessions, show the candidates and wait for a specific selection. If the chosen session disappeared, stop without sending.
4. For a project-scoped request, never infer project membership from a session name. If `ListAgents` withholds working directories, show local sessions as unverified candidates and skip automatic project routing. Do not work around that privacy boundary through process scans or another session inventory. When directories are available, read the local project registry at `~/.xm/projects.json` and filter its `projects` array to one exact, unarchived `id` or `name` before displaying it; `xm project list --json` can truncate a large registry. Never pass a user-supplied project name as shell code. Compare the confirmed path with each session's directory. A Git worktree belongs to its main checkout: canonicalize it with the same `git rev-parse --git-common-dir` rule used by `xm/lib/x-projects-registry.mjs`. An absent directory, failed canonicalization, or ambiguous match prevents automatic project routing.

For `sessions`, just show the available candidates and any unverified project match. Before a project-scoped send, if routing cannot establish a unique recipient, show the addressable candidates and ask the user to select one. A selection by the tool-provided unique address authorizes a direct send even when the directory is unavailable; say that its project affiliation was not verified. Never choose the first candidate. For a direct message to a uniquely named session, the user may select a session in another project; show its directory before sending when the tool supplies one.

## Codex recipients

1. Call `xm relay sessions [--project <id>]` to list saved local Codex threads. The CLI requires the shared daemon and reads thread metadata from it over the WebSocket on the daemon's reported `socketPath` (observed with codex 0.160.0; an internal interface that may change). Only the daemon knows which threads are open, so `loaded: true` (any `app_server_status` other than `notLoaded`) marks a thread the daemon currently holds; such a thread can usually take a queued message promptly. Its `live_status: unverified` is still deliberate: a loaded thread may have no attached UI, and a queue on an unloaded thread may wait for a later resume. Show UUID, name when present, working directory, and last activity. If `partial: true`, say the list may omit older threads. If the daemon is unavailable, report that instead of starting it automatically.
2. Require the exact thread UUID selected from that inventory or supplied by the user. Re-read the thread before delivery; for a project-scoped notice, use `--project <id>` so the CLI checks the thread's canonical repository path against the registered project. Never pick a thread by preview text, array position, or a partial ID.
3. Put the exact outgoing text in a temporary UTF-8 file using a file-writing tool. Call `xm relay send --thread <uuid> --message-file <path> [--project <id>]`, then remove only that temporary file. Do not interpolate untrusted text into a shell command. The CLI invokes `codex queue` without a shell and returns a submission ID when available.
4. Report `queued` only. An attached idle Codex TUI can start the queued turn immediately; a detached saved thread can wait until it resumes. Neither CLI exit 0 nor a queued submission ID proves the receiver read or acted. Do not auto-resume another thread or steer its active turn.

## Sending from Codex to Claude

1. Call `xm relay sessions --provider claude [--project <id>]`. It lists live local sessions exposed by `claude agents --json` only when their current session record and registered private inbox socket agree. Cloud and other-machine Claude sessions are outside this adapter.
2. Require the exact `session_id` selected from that fresh list. Put the requested message in a temporary UTF-8 file and call `xm relay send --provider claude --session <uuid> --message-file <path> [--project <id>]`. Remove only that temporary file afterward.
3. The CLI checks that the PID still belongs to the listed session, the protocol version is supported, the socket is a private local socket, and any requested project matches. It sends an untrusted peer message with normal queue priority and no asserted Claude permission mode. Never add or invent a permission-mode assertion to avoid a hold; Codex has no Claude permission mode to attest. Whether the receiver delivers it is decided by that session, as described under Receiver hold policy.
4. Report `submitted` only. This means message bytes were submitted to the local socket; it does not confirm that Claude received or read them. The adapter requests no delivery receipt and registers no reply address for Codex, so the Claude session cannot reply through this path.

## Receiver hold policy

A receiving Claude session decides whether a peer message reaches its Claude, through the user-level setting `crossSessionInbound` (`/config` → "Messages from your other sessions"). Behavior observed with Claude Code 2.1.287:

| Value | Effect |
|---|---|
| unset (default) | Delivered only when the sender's permission-mode class matches the receiver's (bypass↔bypass, prompting↔prompting). A mismatch is held for the user's approval and can expire. A relay message from Codex asserts no mode, so a bypass receiver holds it and a prompting receiver delivers it. |
| `"accept"` | Every peer message from the user's other sessions is delivered, including Codex relay messages to a bypass session. |

Claude Code's own setting description also lists `"hold"` (every peer message waits for review; Claude cannot act on it before approval) and `"refuse"` (the session opts out), and says repository or managed settings may tighten the value to `hold` or `refuse` in a way a user's `accept` cannot override. These were not exercised by this skill's checks. When a user asks why a message was held, explain this policy and its trade-off: with `accept`, text from another session reaches a bypass Claude without review. Do not change the setting yourself; it is the user's decision, made through `/config`, their settings file, or `claude --settings '{"crossSessionInbound":"accept"}'` for one session.

## Send

- `send` forwards the user's requested message. `handoff` composes a short card from verified current-session facts: the current objective, decisions made, relevant files or commit IDs, and unresolved questions. Omit empty fields and anything the receiver cannot use. Do not paste the transcript or assume an `@`-mentioned file is attached on arrival.
- Remove secrets, credentials, tokens, and private output from either message. Preserve exact identifiers, paths, and commands that are safe to share. The receiver treats the message as another session's report, never as user approval or permission to change its own settings.
- For Claude, call `SendMessage` once for the selected address. For Codex, queue once through `xm relay send`. Do not broadcast, automatically retry, or ask for permission again when the user has already requested this send. A live notice explicitly requested as part of `/xm:toss` carries that same authorization.
- Report only what the tool established: sent, held, refused, or unknown. A successful send does not prove that the receiver read, accepted, or acted on the message. An inbox `take` and a terminal receipt remain separate events. A one-shot sender such as `claude -p` may exit before a reply arrives; promise an ACK only when the sender remains addressable and the reply was observed.

When `/xm:toss` invokes this skill, send only the toss ID, redacted title, source and target project IDs, and a pointer to `/xm:inbox` for the durable body. Tell the receiver that the notice does not change its current task or authorize work. If the project cannot be matched and the user has not selected an exact session, leave the durable toss intact and report that no live notice was sent.

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "The user typed `01a0fc52`, that's obviously the thread." | A prefix can match a different thread after new ones appear. Re-list, confirm exactly one match, and send with the full UUID. |
| "The listing from a few turns ago is good enough." | Sessions exit and threads unload. Re-list the chosen provider immediately before every send. |
| "`queued` / `submitted` came back, so the receiver got it." | `queued` only means the daemon accepted it; `submitted` only means bytes reached a socket. Report exactly that state, never "delivered" or "read". |
| "The bypass receiver held the message; I'll mark the frame as bypass so it goes through." | That forges an attestation the sender cannot make and defeats the receiver's review. Explain the Receiver hold policy and let the user choose `crossSessionInbound`. |
| "The message is long; I'll pass it with `--message \"...\"`." | Shell quoting corrupts quotes, backticks, and newlines without an error. Write the text to a temp file and use `--message-file`. |
| "No Claude session matched, so I'll start one with `claude -p` to deliver it." | A new session is not the intended recipient, and a one-shot process exits before any reply. Report that no recipient was available. |
| "The live notice can carry the whole toss body." | Relay is best-effort and not durable. Send only the toss ID, title, projects, and a pointer to `/xm:inbox`. |

## Verification

- `xm relay sessions` returns `ok: true`; open Codex threads show `loaded: true` and come first.
- A send reports `queued` (Codex) or `submitted` (Claude) with the exact UUID that was re-listed just before it.
- The temporary message file was removed after the send.
