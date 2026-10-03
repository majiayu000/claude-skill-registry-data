---
name: coding-standards
description: Load and enforce the layered coding-standards/ chain (global → file-role partial → framework override) before editing. Trigger before editing/creating CSS, HTML, JS/TS, or framework files in a project with coding-standards/, or on mention of standards, conventions, compliance.
---

# Coding Standards — Load the Chain, Then Edit

The user maintains a portable, layered standards system (`coding-standards/` in the project root). The contract is absolute: **never edit a file without loading its standard chain first**, and never invent a rule where the standards are silent — flag the gap instead.

**This skill deliberately contains zero rule content.** The actual rules — `[CX]` response contract (ai-standards), data-attribute-driven state (css RULE 23), no inline styles (css RULE 08), token variables, selector signatures, and all the rest — live only in the standards files. Duplicating them here would create a second source of truth that drifts the moment a standard is edited. The skill's whole job is making sure the right files get loaded and obeyed; when standards update, this skill is current by construction.

## Self-improvement (do this first and last)
1. **At start:** read `learnings.md` in this skill's folder if it exists. Apply relevant lessons.
2. **At end of every use:** append one dated bullet — a chain-loading shortcut that worked, a standards gap flagged, a violation class that keeps appearing. Merge instead of duplicating; delete disproven bullets.

## The three layers (read top → down, per file being edited)
1. **Universal global rules** — `coding-standards/{discipline}-standards.md` (css, html, js / ts / js-and-ts, plus git, versioning, seo, performance, accessibility, qa, ai).
2. **File-role partials** — `coding-standards/{discipline}-standards/{file-role}.md` (e.g. `css-standards/component-files.md`). Identify the file's role via the File-to-Role Mapping in `coding-standards/index.md` — don't guess the role.
3. **Framework overrides** — `frameworks/{framework}.md` + `frameworks/{framework}/{file-role}.md`. Framework files may extend or explicitly override universal rules; an override always says so.

Then apply project-specific context (CLAUDE.md / handover: prefixes, token files, file placement) on top.

## Loading discipline (correct AND cheap)
- **Load per file-role, lazily.** Editing one component stylesheet needs: index (once per session) → css global → component-files partial → framework css layer if any. Not the whole folder.
- **Once per session per chain.** Track which chains are already loaded; re-read only if the task moves to a new discipline or file role.
- **Exactly one script standard per project** — the project's CLAUDE.md/handover declares JS-only, TS-only, or combined. Never read more than one.
- Cross-cutting standards (accessibility, performance, seo, qa) load at their checkpoint (new page → seo + accessibility; pre-release → qa + performance), not on every edit.
- If the project has no `coding-standards/` folder, this skill doesn't apply — say so rather than importing rules from another project.

## Enforcement discipline
- **Standards are law, not suggestions.** Where a standard and habit/training conflict, the standard wins — including when it feels non-idiomatic.
- **Gaps get flagged, never filled silently.** If a needed rule doesn't exist, say "the standards don't cover X; I'll do Y — flag for the standards repo" and proceed. Recurring gaps are candidates for the user to add as new partials.
- **Session protocol compliance:** if the project's CLAUDE.md defines a behavioral contract (response markers, standards declaration, no-filler rules), it is part of the standards — follow it exactly.
- Before finishing any edit: self-check the diff against the loaded chain (prefixes, tokens vs hardcoded values, structure rules), not against generic best practice.

## Reviewing / retrofitting
When asked to check compliance of existing files: load the chain for each file's role, report violations grouped by rule (rule → offending `file:line` list), ranked by severity per the standard's own wording (law vs recommendation). Don't fix unprompted — the audit is the deliverable unless asked to apply. Gate behavior across session modes: see `mode-kernel`.

## Keeping the system healthy (owner's privilege)
The standards system is itself a repo the user maintains and ports across projects. Improvements discovered in use (ambiguous wording, missing file-role, framework gap) should be surfaced as concrete proposed edits to the standards files — the user decides; never edit standards files as a side effect of feature work.
