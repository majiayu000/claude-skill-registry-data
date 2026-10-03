---
argument-hint: [instructions]
description: Interview user in-depth to create a detailed spec
allowed-tools: AskUserQuestion, Write, Agent
---

Follow the user instructions and interview me in detail using the AskUserQuestionTool about literally anything: technical implementation, UI & UX, concerns, tradeoffs, etc. but make sure the questions are not obvious. be very in-depth and continue interviewing me continually until it's complete. then, write the spec to a file.

**Save location:** `~/.claude/skills/interview/<project>/<relevant-name>.md`

- `<project>` = the basename of the current working directory (e.g. `trip-planner` for `/Users/johnathanmo/.superset/projects/trip-planner`). Create the directory with the Write tool if it doesn't exist — Write creates parent directories automatically.
- `<relevant-name>` = a short kebab-case slug describing the spec topic, ending in `-spec.md` (e.g. `friends-tab-redesign-spec.md`).
- Always resolve and write the absolute path. Do not save the spec into the working directory or anywhere else.

<instructions>$ARGUMENTS</instructions>
