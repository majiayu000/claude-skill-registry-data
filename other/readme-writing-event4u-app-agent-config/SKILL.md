---
model_tier: medium
name: readme-writing
description: "Use when creating, rewriting, or significantly improving a README based on the actual repository structure, commands, and intended audience."
domain: process
scope:
  write: []
  verification_reason: "execution.handler is internal, so this skill spawns no subprocess — writes happen through the agent's declared allowed_tools. No command can prove a scope the skill never executes."
execution:
  type: assisted
  handler: internal
  allowed_tools: []
workspaces:
  - agent-config-maintainer
packs:
  - meta
---

# readme-writing

## When to use

- Creating a new README for an **application, CLI tool, internal tool, template, or framework**
- Rewriting an outdated or weak README
- Improving after major repo changes (new tooling, restructure)
- Adapting README for a different audience

Do NOT use when:

- Writing a README for a **reusable package or library** → use `readme-writing-package` instead
- Fixing minor typos or updating a single section
- Writing reference docs that belong in separate files
- Only adding a badge or version bump

## Goal

Write a README that is accurate, evidence-based, scannable, and useful for
the intended audience. Reflects the real repository — not assumptions.

## Core principles

- **Analyze first, write second** — inspect the repo before writing a single line
- **Evidence-based only** — every command, setup step, and feature must exist in the repo
- **Strong quickstart over exhaustive noise** — a reader should get started in 30 seconds
- **Right scope** — high-level overview in README, deep content in dedicated docs
- **Match the repo type** — a package README differs from an app, CLI tool, or framework
- **Re-analyze every time** — never trust cached knowledge of the repo; the README that drifted yesterday is the README the model wrote from memory
- **Preserve existing visual identity** — banner, badges, profile/role grids, official logo lockups stay byte-identical unless the user explicitly asks to change them

## Procedure

### 0. Re-analysis gate — MANDATORY before any writing

Before drafting a single line, run a fresh repository inspection in **this**
session. Do not rely on prior knowledge, prior turns, or the existing README
prose. Produce an explicit evidence ledger:

```
ledger:
  package:      <name + version from manifest>
  description:  <verbatim from manifest>
  cli_entry:    <bin / entry from manifest, if any>
  commands:     <list of real commands from Taskfile / Makefile / package.json scripts>
  install:      <verified install path(s) from scripts/install.* or docs>
  doc_targets:  <list of /docs files actually linked from the new draft>
  counts:       <skills / rules / commands / personas / advisors — if surfaced as badges>
  visual_keep:  <line range of existing README header, banner, badge block to preserve>
```

If any cell is unknown, run `ls`, `grep`, `find`, or read the file before
writing — never invent. If the user asks to "use the existing banner",
locate the exact source lines and reproduce them byte-for-byte, including
the surrounding HTML.

### 1. Identify README type and audience

Determine repository type:

| Type | Audience | Priority |
|---|---|---|
| **Library/Package** | Developers consuming it | Install → Usage → API |
| **Application** | Team / contributors | Setup → Dev workflow → Architecture |
| **CLI tool** | End users | Install → Commands → Examples |
| **Template/Starter** | Bootstrappers | What you get → Quickstart → Customize |
| **Internal tool** | Team members | Purpose → Setup → Common tasks |
| **Agent/Framework** | AI tools + maintainers | What it is → Install → Architecture → Extend |

### 2. Inspect the repository

Read these files to extract truth:

- `README.md` (existing, if any)
- `package.json`, `composer.json` — name, description, scripts, dependencies
- `Dockerfile`, `docker-compose.yml` — runtime setup
- `Taskfile.yml`, `Makefile` — available commands
- CI workflows — what gets tested, how
- `docs/`, `agents/` — existing documentation
- Config files — what tools are used

Extract: project purpose, install path, main commands, requirements,
key workflows, testing/linting commands, contribution flow.

### 3. Choose sections

Only include sections that provide value. Candidates:

1. **Title + one-line summary** — always
2. **Why / what problem it solves** — if not obvious from name
3. **Key features or capabilities** — if more than a trivial tool
4. **Requirements** — only if non-obvious
5. **Installation / setup** — always
6. **Usage / quickstart** — always (most important section)
7. **Configuration / customization** — if applicable
8. **Development workflow** — if repo accepts contributions
9. **Testing / quality** — if tooling exists
10. **Project structure** — if non-trivial
11. **Contributing** — if open or team project
12. **License** — if applicable

Do NOT include sections "because READMEs usually have them."
Skip empty or near-empty sections entirely.

### 4. Write evidence-based content

Rules:

- Only document commands that actually exist in the repo
- Only describe setup steps supported by scripts/configs
- Only claim features confirmed by code or docs
- If something is unclear: inspect more or ask — never invent

Formatting:

- Tables for structured comparisons (tools, options, features)
- Code blocks for every command (copy-pasteable)
- Short paragraphs — max 3 sentences before a break
- Directory trees for project structure (use `tree` format)
- Badges only if they link to live CI/release status

### 5. Optimize for the first screen

A reader scanning the README should answer within 10 seconds:

1. What is this?
2. Why does it exist?
3. How do I install/start it?

The first screen (before scrolling) must contain the title, summary,
and either install command or quickstart. Everything else comes after.

### 6. Size and structure

Keep the README scannable. If it grows past ~150 lines, add a Table of
Contents; past ~300 lines, split deep content out to `/docs/` or
`references/`. Use `<details>` only for secondary, bulky content (never
for install, first example, or requirements).

→ See `docs/guidelines/docs/readme-size-and-splitting.md` for thresholds,
splitting strategies (reference-split, deep-link tables, collapsibles),
multi-audience handling, and anti-patterns.

### 7. Validate links and detect orphans — MANDATORY

For every internal link in the new draft:

1. Resolve the path. If it points to a file, `test -f` the path. If a
   directory, `test -d`. Strip `#anchor` and `?query` before the check.
2. For every anchor link (`file.md#section`), grep the target file for
   the heading slug. Missing anchor = broken link.
3. Build the **link-delta** between the old README and the new one:
   - **kept**: linked in both
   - **added**: only linked by the new README
   - **dropped**: only linked by the old README

For every `dropped` target, search the rest of the repository
(`grep -r "<path>"` over `AGENTS.md`, `docs/`, `dist/agent-src*/`,
`.augment/`, `packages/`). If no other file references it, mark
**orphan-candidate**. Surface the list to the user — do not delete
silently.

### 8. Validate

After writing, verify:

- [ ] Every documented command exists in the repo (`Taskfile.yml`, `Makefile`, `package.json scripts`, etc.)
- [ ] Setup steps are reproducible (no missing prerequisites)
- [ ] No features or capabilities are invented
- [ ] **First screen contract** — within the first ~40 lines: project name, one-sentence pitch, install command (or pointer), and the primary CTA
- [ ] Banner, badges, and any explicit "preserve" block from Step 0 are byte-identical to source
- [ ] No dead sections (heading with 1-2 trivial sentences)
- [ ] Scope is right — deep content moved to dedicated docs, not crammed in
- [ ] Size below the "overloaded" threshold, or splitting is in place (see size guideline)
- [ ] ToC present if README > 150 lines or > 6 top-level sections
- [ ] Matches existing tonality if repo has established voice
- [ ] Every internal link resolved per Step 7 — zero broken file or anchor links
- [ ] Orphan-candidate list produced even if empty

## Output format

1. Full README draft
2. Short note: detected repo type + audience
3. **Link delta** — `kept` / `added` / `dropped` with orphan-candidates flagged
4. Evidence ledger (Step 0) so the user can audit assumptions
5. Any uncertainties or assumptions that need confirmation

## Gotcha

- The model tends to write generic boilerplate instead of repo-specific documentation
- The model tends to include commands or setup steps that don't actually exist in the repo
- The model tends to over-document and bury the quickstart under walls of text
- Existing README structure can be misleading — don't preserve weak structure blindly
- READMEs for packages consumed by others need install/usage focus, not internal dev workflow
- The model forgets to validate commands against `Taskfile.yml` / `Makefile` / `package.json scripts`

## Frugality Standards

Apply the [Frugality Charter](../../contexts/contracts/frugality-charter.md)
to every README you author.

**Examples in this artifact:**
- Per the charter's default-terse rule, the README opens with one
  sentence stating what the project is.
- Per the cite-don't-restate principle, "Installation" links to the
  canonical install script, not its full contents.
- Per the cheap-question check, "Quick start vs. full guide" is
  offered only when the two paths produce different artifacts.

**Pre-save self-check:**
1. Does the opening paragraph carry marketing adjectives ("modern",
   "comprehensive", "powerful")?
2. Are setup steps narrated instead of bulleted commands?
3. Are screenshots / GIFs present without explicit user request? A
   **data-bearing** screenshot (dashboard, admin panel, form/list with real
   content) without an explicit request is a stronger flag — route it through
   [`screenshot-hygiene`](../screenshot-hygiene/SKILL.md): anonymize sensitive
   data and human-gate the embed before it ships. Illustrative / no-data visuals
   (diagrams, placeholder-only UI) are the reconciled exception.
4. Is content duplicated from `AGENTS.md` rather than linked?

## Do NOT

- Do NOT invent features, setup steps, or commands not found in the repo
- Do NOT copy generic README templates without adapting to the actual project
- Do NOT overload with deep reference material — link to docs instead
- Do NOT write for "everyone" — choose a real audience
- Do NOT skip repository inspection before writing
- Do NOT preserve weak structure from an existing README just because it exists
- Do NOT add marketing language ("blazing fast", "revolutionary", "next-gen")

→ Final prose pass for audience-facing output: [`humanizer`](../humanizer/SKILL.md) — remove AI-writing tells before delivery.
