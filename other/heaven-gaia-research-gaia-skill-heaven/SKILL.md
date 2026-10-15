---
name: heaven
description: Explicit read-only Skill Heaven console report (model-mediated).
disable-model-invocation: true
---
# Skill Heaven console (preview)
Default output must be the concise bundled summary (at most eight lines). Never add raw JSON, lengthy capability notes, fallback recipes or diagnostic prose. Only an explicit `heaven inspect [status|lens|session|scope|flow|trust]` request adds `--details` and the chosen `--surface` to the same report invocation. Never run `--details` as the default. Printed commands are never executed. The host owns dismissal and tool-trace presentation; do not install a persistent statusline.
This command is model-mediated: you run a bundled read-only Node report and return its stdout, not a native pane or HUD.

Resolve `../../scripts/heaven.mjs` relative to THIS SKILL.md's directory, not the workspace. Run it using argv `node`, the resolved script path, `--host`, `codex`. If the person supplies `--session-root`, pass only the exact Core `sessionRoot` returned in THIS conversation's summon result. Never infer a root from temp directory timestamps, another session, environment-wide searches or a broad transcript scan. Without that root run the unbound report: it says unknown, not zero. Print the output as-is; never execute printed handoff or scope commands.

## Explicit Lens
Only when the person explicitly requests `heaven lens <need>`, call THIS conversation's existing Core skill-summon MCP tool once with `{query: <need>, surface: "any", preview: true}`. No independent MCP server, no materialization call, no follow-up body read. Run the report bound to the `sessionRoot` in that exact result, if present. Hand back the printed `/summon` suggestion for the person to type. Never submit it. If Core is unavailable, say so without bootstrapping another server.
