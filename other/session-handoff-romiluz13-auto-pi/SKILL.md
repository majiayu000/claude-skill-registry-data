---
name: session-handoff
description: Hand off work to another Pi session — write a handoff doc, save key decisions to memory, and notify the target session via intercom. Use when a session is getting long, when you need to continue work in a fresh context, or when transferring work between projects/sessions. Composes handoff.ts (doc writer) + memory (persistence) + pi-intercom (transport).
user-invocable: true
---

# Session Handoff

Transfer work from one Pi session to another without losing context. This is the cross-session version of compact-safe — instead of compressing the current session, you're moving the work to a new session.

## When to use

- Session is getting long (approaching compaction) and you want a fresh context
- You need to continue work in a different project or branch
- You're transferring work to a specialist session (e.g., handing a plan to a builder)
- The user says "handoff", "continue in a new session", "pass this to X"

## Procedure

1. **Write the handoff doc.** The `handoff` extension (`extensions/handoff.ts`) writes a deterministic `HANDOFF.md` from recent turns + the last compaction summary. No LLM call — it's a snapshot. If the extension is available, it fires automatically. If not, write a markdown file to `docs/handoff/<YYYY-MM-DD>-session-handoff.md` with:
   - **Active constraints** — what must not change, what rules are in effect
   - **Current state** — what's done, what's in progress, what's blocked
   - **Key decisions** — what was decided and why
   - **Errors (verbatim)** — any error messages, stack traces, or failures
   - **Next steps** — what the receiving session should do first

2. **Save key decisions to memory.** Use the `memory` tool to save:
   - Architecture decisions (to `project` or `memory` target)
   - Failures and corrections (to `failure` target with category)
   - User preferences discovered during the session (to `user` target)

   Capture memory payload BEFORE validation — compaction can fire between return and parse. If memory is full, save to the handoff doc instead.

3. **Discover the target session.** Run `intercom({ action: "list" })` to see active sessions. Filter by:
   - Same cwd (sessions in the same project)
   - Session name (if the user named it with `/name`)
   - Status (look for "idle" or "active" sessions that can receive work)

4. **Notify the target session.** Run `intercom({ action: "send", to: "<session-id-or-name>", message: "..." })` with:
   - The handoff doc path
   - A 3-line summary of what to do next
   - Any blocking constraints ("don't touch X", "Y is in progress")

5. **Confirm to the user.** Tell them:
   - Where the handoff doc was written
   - Which session was notified
   - What the receiving session should do first

## Rules

- The handoff doc is the source of truth. Memory is the backup. Intercom is the notification.
- KEEP constraints and errors verbatim — do not summarize them. The receiving session needs the exact error text.
- SUMMARIZE resolved decisions — don't replay the whole discussion.
- DROP prose and diary — keep only load-bearing context.
- If the target session doesn't exist or is unreachable, write the doc anyway and tell the user to start a new session pointing at the doc.
- Do NOT use this for in-session compression — that's `compact-safe`. This is for cross-session transfer.

## Discovery without manual IDs

`intercom({ action: "list" })` returns all active sessions with their IDs, names, cwd, and status. You don't need to know the session ID in advance — list first, then send. The `session-status.ts` extension also writes `~/.pi/agent/session-status.jsonl` which any session can read for a quick overview.

Convention: when starting a new session in a project, run `intercom list` to discover other sessions in the same project. If any exist, send them your session ID + role so they know you're there.
