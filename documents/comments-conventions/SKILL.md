---
name: comments-conventions
description: Write no comment by default, and keep the few that earn their place current. Use when writing or reviewing code comments in TypeScript, JavaScript, Python, or shell files.
license: MIT
compatibility: "Claude Code"
---

# Comments — last resort only

- Write no comment by default. Clear names, small functions and precise types are the documentation. Before writing one, rename the thing or extract a function; that removes the need almost every time. This applies to tests too — a well-named test needs no narration above it.
- Never restate what the next line does, never repeat the function name in a header, never explain the change itself: that belongs in the commit message or the PR description, not in the file.
- A comment earns its place only when the reader cannot recover it from the code at all: a past bug with its date/ticket, a directive (`eslint-disable`, `@ts-expect-error`, `biome-ignore`), or a genuinely non-obvious mechanical fact about a library or platform. One line, not a paragraph.
- Explaining WHY in prose is not a licence to comment. Reserve it for a rejected alternative someone would otherwise "fix" back. If the explanation needs more than a line, it belongs in `docs/pitfalls.md` or a decision record, not next to the code.
- When you change code, update or delete the comment attached to it in the same edit. Leave a project's existing comments alone unless asked — they are often load-bearing; this rule governs only the comments you add.
