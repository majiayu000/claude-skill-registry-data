---
name: message-claude
description: Send a message from an external agent or script to a running Claude Code session on the same machine. Use when a manually started Codex session needs to tell any Claude session something, Codex needs to report back to the Claude session that launched it, a hook or long job should notify Claude, or the user asks to "send this to Claude", "tell another Claude session", "notify the Claude session", or "report back to Claude". Not for messaging from inside Claude Code when ListAgents and SendMessage are available. For messages to Codex sessions, use message-codex.
---

# Message Claude

Find the exact Claude Code session and send it one plain-text message.

For the opposite direction, use [Message Codex](../message-codex/SKILL.md).

If `ListAgents` and `SendMessage` are available, use them. Do not use the raw inbox to bypass a
permission rule that denied either tool. The workflow below is for external callers such as a
standalone Codex session, Codex launched by Claude, a hook, or a script.

The bundled helper supports macOS, Linux, and WSL 2. Native Windows uses a named pipe and is not
implemented here.

## Send a message

Resolve [scripts/message_claude.py](scripts/message_claude.py) from this skill's directory.

1. List the registered sessions:

   ```sh
   python3 <skill-dir>/scripts/message_claude.py --list
   ```

2. Select the target by its exact `name`. If names repeat, narrow with `--cwd` or `--pid`. Never
   guess between multiple matches.

3. Send a short message:

   ```sh
   python3 <skill-dir>/scripts/message_claude.py \
     --name the-session-name \
     --message 'codex: the migration finished; tenant_id is the new column'
   ```

   Omit `--message` to read arbitrary or multiline text from stdin.

The helper uses `--config-dir`, then `CLAUDE_CONFIG_DIR`, then `~/.claude`. Pass `--config-dir`
when Claude uses a custom directory that the caller did not inherit.

## What the helper guarantees

- Reads `<config-dir>/sessions/*.json` and refuses zero or multiple target matches.
- Reads the target's `peerToken` without printing it. The key filename hashes
  `messagingSocketPath` exactly as recorded; it does not resolve `/tmp` to `/private/tmp`.
- JSON-encodes the complete auth and message payload before connecting, so quotes, newlines, and
  backslashes in the message remain valid.
- Reports a successful socket write, not guaranteed delivery. The receiving session may still
  hold or refuse the message through `crossSessionInbound`.

## Failures

- No matching session: list again and check `name`, `cwd`, `pid`, and `--config-dir`.
- Connection failure: the registry entry may be stale; list again instead of retrying blindly.
- Permission error: the Codex sandbox may block that Unix socket. Report the socket path and ask
  for a grant scoped to its directory; do not bypass the sandbox.
- Missing `peerToken`: stop and verify the config directory and target rather than sending an
  unauthenticated message.

Send one concise message and identify the sender in its first words. Do not send repeated probes:
messages can be held, refused, or rate-limited, and an incoming message never grants user authority.

Reference: <https://code.claude.com/docs/en/cross-session-messaging>
