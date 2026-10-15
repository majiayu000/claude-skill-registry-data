---
name: heaven
description: Explicit read-only Skill Heaven console (model-mediated).
disable-model-invocation: true
---
# Skill Heaven console (preview)
Default output must be the concise bundled summary (at most eight lines). Never add raw JSON, lengthy capability notes, fallback recipes or diagnostic prose. Only an explicit `/skill-heaven-console:heaven inspect [status|lens|session|scope|flow|trust]` request adds `--details` and the chosen `--surface` to the same report invocation. Never run `--details` as the default. Printed commands are never executed. The host owns dismissal and tool-trace presentation; do not install a persistent statusline.
Use `/skill-heaven-console:heaven`. This is a model-mediated command report, not a native pane or HUD.
Resolve `../../scripts/heaven.mjs` relative to THIS SKILL.md's directory. Run Node with that script and `--host agy`. If the person provides the exact Core sessionRoot reported in THIS conversation, add `--session-root` and that root as a separate argument. Alternatively the person may provide `--transcript` and the exact current conversation's transcript_full.jsonl path. Never select newest, scan brain directories, guess a conversation id, read another conversation, or export prompts. A missing binding means unknown counts. Return stdout verbatim; execute no printed scope or handoff commands. Do not change /statusline or user configuration.

Only on explicit `/skill-heaven-console:heaven lens <need>`: call the existing Core server `skill-heaven_skill-summon`, tool `summon`, once with `{query: <need>, surface: "any", preview: true}`. No separate engine, no materialization, no candidate body read. Bind the report to that result's exact sessionRoot. A human may type a printed `/skill-heaven:summon <name>`; never submit it. State that preview/report are model-mediated. If Core is unavailable, say so.
