---
name: lead
description: Make this Claude Code session the project's lead session, where code-kit's loop runs and the plan's stories are dispatched from, when several sessions work one project. Says which session leads now and what moving the lead does, then gives the person the command that moves it. Use when the person says this session should lead, asks which session leads, or runs /code-kit:lead.
---

# Lead from this session

Several Claude Code sessions can work one project at once. One is the lead session: code-kit's loop runs there, and the plan's stories are dispatched from it. The others are working sessions: they stay quiet (no loop prompts, no other session's decisions), and each records its ad hoc task, with the paths it leases, before it changes code.

The CLI is `node "${CLAUDE_PLUGIN_ROOT}/bin/code-kit.mjs"`, run from the project root.

1. See who leads now:

   ```bash
   node "${CLAUDE_PLUGIN_ROOT}/bin/code-kit.mjs" who
   node "${CLAUDE_PLUGIN_ROOT}/bin/code-kit.mjs" sessions
   ```

2. If this session already leads, say so and stop.
3. Otherwise, tell the person what moving the lead does: this session starts running the loop and dispatching the plan's stories, and the session that led becomes a working session, which stops prompting its lead. Choosing the lead is theirs, so give them the command to run themselves (the hooks refuse it from an agent), or point them to **Lead from here** in the code-kit band:

   ```text
   ! node "${CLAUDE_PLUGIN_ROOT}/bin/code-kit.mjs" sessions lead
   ```

4. Once they have, run `who` again and confirm this session leads.

A working session doesn't need this to work: it records its task (`code-kit task "<what>" --touches "<globs>"`), works in a worktree of its own, and `code-kit task done` when it's finished.
