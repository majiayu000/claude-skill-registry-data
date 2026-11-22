---
name: system-browser-open-discipline
version: "1.0.0"
user-invocable: true
description: "Hard discipline for human-view opens of .md/.html: open via the OS default handler so files land in the system default browser — not IDE Simple Browser or in-editor Markdown preview. Use when presenting generated HTML/Markdown for human acceptance, or when the user asks to open/view those files in a browser. Triggers — 「用浏览器打开」「系统浏览器打开」「打开 markdown」「打开 html」「浏览器查看 md」 / open in browser, system browser open, view markdown in browser. Referenced by goal-driven-queue and goal-driven-workflow via frontmatter dependencies. Do NOT use for Agent self-read/analysis, for editing files in the editor, or as an installer for browser extensions."
---

# System Browser Open Discipline

> Shared discipline for **human-view** opens of Markdown and HTML. Hosts that open generated views for acceptance declare this skill in `dependencies` and abort if missing. Humans may also invoke it directly.

## Iron Law

**WHEN OPENING `.md` / `.html` FOR A HUMAN TO VIEW, USE THE SYSTEM DEFAULT BROWSER.**

- Resolve the path, then open it with the **OS default application** for that file so it lands in the system default browser.
- Do **not** use IDE Simple Browser, an integrated browser pane, or in-editor Markdown preview as the human-view channel.
- Same rule for `.htm` / `.markdown` when those extensions appear.

## When to apply

| Situation | Action |
|-----------|--------|
| User asks to open/view a `.md` or `.html` in the browser | Open via OS default → system browser |
| Host interactive handback (e.g. `verification.html`, review/evidence HTML) | Same open channel |
| Explicit "open this view" while a human is present | Same open channel |
| Scheduled / unattended handback with no view request | Print paths only — do not auto-open |

## Boundaries (stay on the other path)

| Situation | Channel |
|-----------|---------|
| Agent needs file text to analyze, search, or diff | Normal read tools — no browser open for the read alone |
| User asks to **edit** the file | Editor — not a human-view browser open |
| Non-`.md`/`.html` artifact | Out of scope for this skill |

## How to open (intent only)

Describe the outcome: **open this absolute path with the OS default handler so the system default browser shows it.** Use whichever native capability the running agent has for that intent. Prefer a direct argument vector over a shell string when spawning an opener. If the environment cannot perform an OS open, print the absolute path, record that browser open was skipped, and do not claim the page was shown.

Hosts that already ship a tested opener for their own views (path-contained, injectable in tests) keep that opener; this skill constrains the **channel** (system browser), not the host's internal function name.

## Integration guide

- Hosts: one-line pointer at human-view open sites — load this skill; do not paste the Iron Law.
- Prefer declaring frontmatter `dependencies` when the host regularly opens views for humans.
- Optional environment tips (Markdown browser extensions, OS file associations): see [reference.md](reference.md). Those tips are **not** gates.
