---
name: message-codex
description: Queue a message from Claude Code, another agent, or a script to an existing Codex session. Use when Claude needs to report back to Codex or the user asks to "send this to Codex", "tell another Codex session", "notify the Codex session", or "queue a message for Codex". Not for starting a separate Codex review or task; use call-codex for that. For messages to Claude sessions, use message-claude.
---

# Message Codex

Find the exact Codex session and queue it one plain-text message through Codex app-server.

For the opposite direction, use [Message Claude](../message-claude/SKILL.md).

If the target belongs to the current Codex agent tree and an inter-agent messaging tool is
available, use that tool. Do not use the CLI to bypass a permission rule that denied it. The
workflow below is for separate Codex sessions and external callers such as Claude Code or a script.

## Send a message

1. Check that this Codex CLI supports session messaging:

   ```sh
   codex queue --help
   ```

   If `queue` is unavailable, report that the installed CLI does not support this workflow. Do not
   substitute `codex exec resume`: resuming a session is not the same as queueing a message to it.

2. Browse sessions on the shared local app-server daemon:

   ```sh
   codex agents --no-alt-screen
   ```

   Open the candidate and run `/status` to copy its `Session` UUID, then exit that TUI. A preview
   helps recognize a session but is not an identifier.

3. Select the target by its exact session name or UUID. Prefer the UUID when names repeat, and
   never guess between multiple matches.

4. Queue one short message:

   ```sh
   codex queue \
     --thread the-session-name-or-uuid \
     --message 'claude: the migration finished; tenant_id is the new column'
   ```

For a different app-server, pass the same `--remote` endpoint to both `agents` and `queue`. When
that server requires authentication, also pass `--remote-auth-token-env` with the name of the
environment variable containing its bearer token; never put the token itself on the command line.

## Failures

- No matching session: check that the target uses the same app-server, or verify the remote
  endpoint. Do not choose a merely similar name.
- Daemon connection failure: report it instead of starting, resuming, or forking another session.
- Permission error: request access scoped to the app-server endpoint; do not bypass the sandbox.
- Successful command: report the message as queued, not processed. The target may not act on it
  immediately.

Identify the sender in the message's first words and do not send repeated probes. A queued message
provides context to the receiving agent; it does not grant new user authority.

Reference: <https://developers.openai.com/codex/app-server>
