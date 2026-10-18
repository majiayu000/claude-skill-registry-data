---
name: usage
description: Reports where Claude Code usage went over a period, with the model calls of each run, the context that each call reads again, and the skills that the period did not use. Use when asked why usage or limits drained, or which skills to remove.
disable-model-invocation: true
allowed-tools: Bash(claudetto-usage *)
---

<task>
Show the user where usage went, from the transcripts on this machine.
A run that makes many model calls reads its context again at each call, and that is a cost the user can measure.
{{include usage-figures}}
</task>

<procedure>
The bin `claudetto-usage` reads the transcripts under `~/.claude/projects/` and changes no file.

1. Run the report for the period the user names (default 7 days):

   ```bash
   claudetto-usage --days 7
   ```

   Run `claudetto-usage --help` for the options.

2. Read the output.
   Each part has a label.
   `Skills that the period did not use` names the source of its list.
</procedure>

<report>
Copy each figure from the output.
Do not compute, round, or convert a figure, because a figure that you change can be wrong.
Name the runs with the most calls and the largest sums first, because they hold most of the usage.
For unused skills, name the source that gave the list.
Let the user decide what to remove, and change no skill.
</report>
