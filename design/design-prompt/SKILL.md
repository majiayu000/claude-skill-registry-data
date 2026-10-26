---
name: design-prompt
description: Generate a PROFESSIONAL Claude Design brief (token contract + anti-vibe-coding constraints) as a clean copy-paste .md. Use when the user says "design prompt", "prompt for Claude Design", "design brief", or is about to start the UI/UX pass. Design intent only — no code.
argument-hint: [project name]
allowed-tools: Read, Write, Glob, Grep, AskUserQuestion, WebSearch, Bash(python3 *)
---

## Task

Produce `design/<project>-design-prompt.md` — a single copy-paste block for Claude Design that
produces **professional, not vibe-coded** screens. The difference between a cheap prompt and this
one is: a pasted **token contract**, **specific reference/cultural anchors**, **mandatory states**,
and an explicit **DO-NOT list**. Why this works: `docs/research/04-design-and-prompting.md`.

### 1. Read the bar and the contract first

Read `docs/design/quality-bar.md`, `docs/templates/claude-design-prompt.md`,
`docs/conventions/design-system.md`, and `tailwind.config.js`. The filled brief MUST embed the
real token contract and the DO-NOT list — never a generic "make it clean and modern".

### 2. Source the product context

Use the PRD in `docs/product/prds/` and `docs/product/vision.md` if present. Otherwise ask the user
(AskUserQuestion) for the brief inputs that genuinely change the design: product + core gesture +
emotional register; the screens to design; the primary user + the moment; tone words; 2–3 named
reference apps and (optionally) a cultural anchor. Keep it to one round of questions.

### 3. Rebrand away from the defaults (critical)

The skeleton ships **placeholder indigo (`#6366F1`) + Inter** — the two most recognizable AI tells.
The brief must instruct a distinctive palette + typeface for THIS app. If the `ui-ux-pro-max` skill
is installed, use it to pick a product-appropriate palette / style / font pairing:

```bash
python3 .claude/skills/ui-ux-pro-max/scripts/search.py "<product> <industry> <tone>" --design-system
```

If it isn't installed, propose a distinctive palette + font yourself (justify the choice in one
line) — just never default indigo/purple + Inter. For fast-moving platform UX (Dynamic Island,
predictive back, new HIG/Material patterns), do a quick `WebSearch` so the brief is current.

### 4. Fill the template

Fill every section of `docs/templates/claude-design-prompt.md` with this project's specifics:
realistic sample data (never lorem), named + cultural reference anchors, the **token contract as
design values** (palette roles, type scale, spacing, radii, depth, motion), the required states for
**every** screen, accessibility, and the **DO-NOT** list. Keep the multi-pass + 3-directions +
self-critique process section intact.

### 5. No-code rule (hard)

Design intent only. If you catch yourself writing component names, props, class names, or code,
stop — that belongs to the build pass. The token contract is expressed as **design values** (hex
roles, sizes, durations), not code.

### 6. Output hygiene

Clean Markdown, one copy-paste block, no repo-internal jargon. End with: paste into Claude Design,
attach the 3–5 reference images, and export the result as a ZIP back to Cowork. The build pass
(Claude Code) will read the same token contract + `docs/design/quality-bar.md` when implementing.
