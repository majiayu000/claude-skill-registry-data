---
name: start-cost
description: Measures what a Claude Code session sends at its start, by source, and compares a start with a plugin against a start without it. Use when asked what a plugin, skill list, or MCP server costs at the start of a session, not for usage over time.
disable-model-invocation: true
allowed-tools: Bash(claudetto-start *)
---

<task>
Show the user where the start of a session spends its context.
Each listed skill, agent, plugin, and MCP tool adds a fixed cost to every session.
{{include usage-figures}}
</task>

<procedure>
The bin `claudetto-start` reads a transcript (a `.jsonl` file under `~/.claude/projects/`).
It changes no file.

1. Report one session.
   With no argument, it reads the newest transcript of the current folder:

   ```bash
   claudetto-start
   claudetto-start /path/to/session.jsonl
   ```

   The section `Start by source` lists the characters of each source: the built-in set, each plugin (by the name prefix of its skills, agents, and tools), each MCP server, `CLAUDE.md` and memory, the output style, and the system prompt.
   The first line gives the tokens of the first request.

2. Compare a start with a plugin and a start without it.
   The transcript of a session shows only the plugins that were on, so the user must start two sessions.
   Ask the user for the two transcript paths, or tell the user to start one session with the plugin and one without it, with the same folder and the same first prompt.
   Then run:

   ```bash
   claudetto-start --compare WITHOUT.jsonl WITH.jsonl
   ```

   The first path is the base.
   Each row is the other start minus the base, so a plus sign means the plugin adds that many characters.
</procedure>

<report>
Copy each figure from the output.
Do not compute, round, or convert a figure, because the characters are an estimate from the transcript and a conversion would hide this.
Give the real token figures only from the line `First request`.
Name the largest sources first.
</report>
