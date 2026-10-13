---
name: status
disable-model-invocation: true
description: Check every link between Claude Code and the Apeiron editor, and say how to fix what is broken
allowed-tools: Bash(ngine mcp status:*), Bash(ngine doctor:*), Bash(ngine mcp list:*)
---

Diagnose the Apeiron connection. Run `ngine doctor` and `ngine mcp status`, then `ngine mcp list`
if an editor is expected to be running. Report, in order: which checks FAILED or WARNED, the
`fix:` line printed for each, and which checks did not run (a skipped check is not a pass — say so).
Do not change anything: this command only reads. If everything passes, say so in one line and
suggest calling `ngine.guide` for orientation.
