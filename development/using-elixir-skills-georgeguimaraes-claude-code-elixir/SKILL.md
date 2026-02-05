---
name: using-elixir-skills
description: Use when writing Elixir, Phoenix, or OTP code - routes to the correct thinking skill before any code is written
---

<EXTREMELY-IMPORTANT>
If the task involves Elixir, Phoenix, or OTP code, you MUST invoke the relevant skill BEFORE doing ANYTHING else—including exploring the codebase.

THIS IS NOT OPTIONAL. Skills tell you HOW to explore and WHAT to look for. You cannot rationalize your way out of this.
</EXTREMELY-IMPORTANT>

## The Rule

```
Elixir/Phoenix/OTP task → Invoke skill FIRST → Then explore/research → Then write code
```

**Skills come before exploration.** The skills tell you what patterns to look for, what questions to ask, and what anti-patterns to avoid. Exploring without the skill means you don't know what you're looking for.

## Skill Triggers

| Trigger Phrases | Skill to Invoke |
|-----------------|-----------------|
| code, implement, write, design, architecture, structure, pattern | `elixir-thinking` |
| LiveView, Plug, PubSub, mount, channel, socket, component | `phoenix-thinking` |
| context, schema, Ecto, changeset, preload, Repo, migration | `ecto-thinking` |
| GenServer, supervisor, Task, ETS, bottleneck, Broadway, Oban | `otp-thinking` |

## Red Flags

These thoughts mean STOP—invoke the skill:

| Thought | Reality |
|---------|---------|
| "Let me explore the codebase first" | Skills tell you WHAT to look for. Invoke first. |
| "Let me understand the code first" | Skills guide understanding. Invoke first. |
| "But first, let me..." | No. Skills come first. Always. |
| "I'll add a process to organize this" | Processes are for runtime, not organization. |
| "GenServer is the Elixir way" | GenServer is a bottleneck by design. |
| "I'll query in mount" | mount is called twice. |
| "Task.async is simpler" | Use Task.Supervisor in production. |
| "I know Elixir well enough" | These skills contain paradigm shifts. Invoke them. |
