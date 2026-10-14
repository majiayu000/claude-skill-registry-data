---
name: claude-audit
description: Use when auditing a Claude Code setup for token waste.
---

Audit this setup for token waste. Do not fix anything. Report only.

Use your shell and file tools to measure each item. If you cannot invoke slash
commands yourself, ask me to run /context and /usage and paste the output, then
continue.

1. MEMORY
   Find every CLAUDE.md in scope: this project, parent directories, the user
   level one, and anything pulled in with @imports. Report each file's size in
   tokens. Flag any single file over 5k and any total over 10k.

2. TOOLS
   List connected MCP servers and how many tools each exposes. State plainly
   whether tool deferral is ACTIVE or NOT. Then check for a proxy or gateway
   (ANTHROPIC_BASE_URL, ANTHROPIC_AUTH_TOKEN, any gateway variable) and say so
   loudly if you find one, because routing through a proxy silently turns
   deferral off and nothing warns you.

3. MODEL
   Report the current model and effort level and where each is set. Flag any
   mode that changes model automatically during a session, because every
   switch rebuilds the whole cache.

4. HOOKS
   List any PreToolUse hooks that rewrite noisy commands to produce less
   output. If there are none, say so, because unfiltered test and build output
   lands in context verbatim and is re-sent for the rest of the session.

5. SUBAGENTS
   List every agent file in the project and user agent directories. For each,
   report whether it sets an explicit model in frontmatter or inherits the
   main session's model.

6. SCHEDULED WORK
   List every cron, scheduled task and background job with its interval.
   Compare each interval against the prompt cache lifetime. Flag every one
   whose interval is longer, because those miss cache on every single fire.

7. CACHE
   Parse the newest session log under the projects directory. For every
   assistant turn, sum usage.cache_read_input_tokens,
   cache_creation_input_tokens, input_tokens and output_tokens. Report each as
   a percentage of the total. Also report the context size on the first turn
   and on the last turn.

Output one table, sorted by cost, highest first:

   FINDING | SEVERITY | EVIDENCE | WHAT IT IS COSTING ME

Severity is RED, AMBER or GREEN. Evidence is a number or a file path, never an
adjective.

Then one final line: the single highest-leverage change I should make. One
line, nothing else.

Rules: measure, do not estimate. Write UNKNOWN rather than guessing. Change no
file and no setting.
