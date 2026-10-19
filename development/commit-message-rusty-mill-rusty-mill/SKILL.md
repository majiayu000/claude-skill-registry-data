---
name: commit-message
description: Produce a concise, well-structured git commit message from a diff or change description.
tags: [git, writing, engineering]
source: rusty_mill:crates/apps/nexus/crates/nexus-skills/builtins/commit-message.skill.md (converted; template fields became <placeholders>)
---
Write a git commit message in **<style>** style for the supplied
diff or change description.

### Subject line
- Max 72 characters, imperative mood, no trailing period.
- For `conventional`: `<type>(<scope>): <summary>`. Types: `feat`,
  `fix`, `refactor`, `docs`, `test`, `chore`, `perf`, `build`.
- For `plain`: just `<verb> <what changed>` — no prefixes.

### Body (optional — only when the diff genuinely needs it)
- Wrap at 72 columns.
- Explain **why** the change was made. The diff shows what changed;
  the body's job is motivation, not summary.
- If the change has non-obvious consequences (migrations, breaking
  API shifts, perf trade-offs), call them out.
- Omit the body entirely when the subject fully captures the change.

### Footer (optional)
`Fixes #123`, `Closes #456`, or `BREAKING CHANGE: …` as appropriate.
Don't invent issue numbers you weren't given.
