---
name: web-interface-guidelines
description: Review web UI code against Vercel's Web Interface Guidelines. Use for an explicit interface review or before shipping a surface.
disable-model-invocation: true
---

# Web Interface Guidelines

Review the named files, or the surface the user points at, against every rule in [guidelines.md](guidelines.md). The rules are the vendored copy of `vercel-labs/web-interface-guidelines/command.md`.

Report findings as `path:line` with the violated rule and a one-line fix. Group by the section headings in the rules file. Skip rules that name a framework the project does not use. Say which sections were not checked.
