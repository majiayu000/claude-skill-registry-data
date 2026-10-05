---
name: research
description: "Research-note driver. Create, continue, conclude, or archive KB research notes (incident-investigation, math-model, competitive-analysis, exploration). Notes live at <kb>/repos/<project>/research/."
argument-hint: "new <title> | continue [path] | status [--all] | conclude [path] | archive [path]"
---

# Research Skill

Research notes are free-form exploration documents. Unlike `/feature`, there is no implementation checklist and no audit — just KB-backed notes that persist across sessions. This skill is the driver for creating and managing them; the orchestrator writes the file directly (the Librarian is an optional helper, not a mandatory gateway — see `agents/librarian.md` for when it's actually useful).

User-input prompt presentation in this skill follows the banner
convention in `docs/user-input-banner-convention.md`. Each real decision
fork — subtype selection, reopen-concluded-note, overwrite-vs-append
conclusion, conclusion-text input — carries the `AWAITING YOUR INPUT`
banner.

### Caveman activation in this flow

Caveman compression is mandatory in this flow. The wire prefix `[COMPRESSION:terse]` MUST be prepended to every subagent Task description and to every Codex MCP `developer-instructions:` field within this flow. Machine-output payloads (haiku scorer JSON, `render_findings` / `dedupe_findings` IO, parser inputs) are exempt per `skills/caveman/SKILL.md` §7.

## Modes

Parse `$ARGUMENTS`:

| Input | Mode | Action |
|-------|------|--------|
| `new <title>` | **New** | Ask subtype → create note → report path |
| `continue [path]` | **Continue** | Resume an existing note (bare path also works) |
| `status [--all]` | **Status** | List ACTIVE notes (default) or everything with `--all` |
| `conclude [path]` | **Conclude** | Append conclusion block; flip `status: CONCLUDED` |
| `archive [path]` | **Archive** | Flip `status: ARCHIVED`; soft — reverse by editing frontmatter |

---

## Phase 0: KB Discovery

KB discovery algorithm follows `docs/kb-discovery.md` — single source of truth.

### Research-skill extensions

Research skill reads only `kb_path` and `project` from the resolved config. No codex.* reads, no LLM dispatch.

---

## New: Create a research note

### Step 1 — Subtype

Ask the user:

---
## ⏸ AWAITING YOUR INPUT

Pick a research subtype for the new note (default: `exploration` — hit Enter to accept).

1. `incident-investigation` — facts-first analysis of a production incident before a postmortem
2. `math-model` — formulas, derivations, modeling spreadsheets
3. `competitive-analysis` — market / vendor / protocol comparison. For decision-making comparisons with a recommendation at the end, use `/investigate` instead — it runs an adversarial Claude+Codex debate and produces a convergence report.
4. `exploration` — open-ended investigation without a clear destination

**Which subtype?**

Accept the number or the slug. Default if user just hits enter.

### Step 2 — Slug

Compute slug:

```
<YYYY-MM-DD>-<lowercased-title with spaces → hyphens, stripped of punctuation>
```

Truncate the title portion to ~50 chars. If the resulting file already exists, append `-2`, `-3`, … until unique.

### Step 3 — Create the note

Target path: `<kb_path>/repos/<project>/research/<slug>.md`. Create the `research/` directory if missing.

Authoring style: caveman-style per skills/caveman/SKILL.md §8 — see skills/feature/references/kb-authoring-style.md.

Use the template from `references/research-template.md`. Frontmatter:

```yaml
---
title: <the given title>
project: <project>
type: research
subtype: <selected subtype>
status: ACTIVE
created: YYYY-MM-DD
tags: [research, <project>, <subtype>]
---
```

Write a stub Context paragraph if the user supplied any framing along with the title; otherwise leave it blank with a `<!-- context here -->` hint.

Spawn **Librarian** only if you need to update MOC indexes afterward.

### Step 4 — Report

> Research note created at `<path>` (subtype `<subtype>`, status `ACTIVE`).
> Open it and start writing.

---

## Continue mode

1. Run Phase 0.
2. Read the note. Inspect `status`:
   - `ACTIVE` → print the Notes section's tail and ask what to work on.
   - `CONCLUDED` or `ARCHIVED` → report state and ask the banner below.

---
## ⏸ AWAITING YOUR INPUT

The note is `CONCLUDED` (or `ARCHIVED`). Continuing requires flipping `status` back to `ACTIVE`.

- Yes → flip status to `ACTIVE` and resume.
- No → stop, leave state untouched.

**Reopen this note?**

3. Never edit existing sections silently — always append new sub-sections with a date header.

---

## Status mode

1. Run Phase 0.
2. Glob `<kb_path>/repos/*/research/*.md`. Parse frontmatter.
3. Default filter: only `status: ACTIVE`. `--all` lifts the filter.
4. Print:

```
| Note | Project | Subtype | Status | Updated |
|------|---------|---------|--------|---------|
| ... | ... | exploration | ACTIVE | 2026-04-17 |
```

---

## Conclude mode

Argument form: `/research conclude [path] [--queue-spec]`. The optional `--queue-spec` flag triggers an interactive queue-publication prompt (step 4b below).

1. Run Phase 0, read the note.
2. If already `CONCLUDED`: ask the banner below.

---
## ⏸ AWAITING YOUR INPUT

This note already has a `## Conclusion` block. Two options:

- `overwrite` → replace the existing conclusion with the new text.
- `append` → add a fresh dated `## Conclusion (YYYY-MM-DD)` block; the old one stays intact.

**Overwrite or append?**

3. Prompt the user for a brief conclusion / decision / follow-up (multi-line accepted):

---
## ⏸ AWAITING YOUR INPUT

Write the conclusion text. Multi-line is fine. It is appended verbatim under the `## Conclusion (YYYY-MM-DD)` heading; any `- [ ]` lines become entries under a `### Follow-up` subsection.

**What is the conclusion?**

4. Append:

```markdown
## Conclusion (YYYY-MM-DD)

<user text>

### Follow-up
- [ ] <derived follow-up items, if any>
```

4b. **If `--queue-spec` was passed**, prompt the user for successor specs to publish in the note's frontmatter as a machine-readable queue (consumed by `/feature continue` and `/feature status` next session):

---
## ⏸ AWAITING YOUR INPUT

Queue successor specs for next-session pickup. One per line, **pipe-delimited**.
Two forms accepted (id is optional per the schema):

  `<id> | <slug> | <scope>`          (3-field — id present)
  `<slug> | <scope>`                 (2-field — id omitted)

Examples:
  `56 | removed-cli-flag-hard-fail | One-cycle deprecation with explicit error`
  `q3-slice-2 | full-reliability-spec | Distribution rollup gated on 5-10 release window`
  `q3-slice-2-full-reliability | Distribution rollup gated on 5-10 release window`

Empty input = no queued specs.

**What specs should be queued?**

Parse non-empty input lines using **pipe-count branching** (matches the schema in `references/research-template.md` where `id` is OPTIONAL):

- **2 pipes per line** → `(id, slug, scope)` triple (3-field form). Trim whitespace around each split field.
- **1 pipe per line** → `(None, slug, scope)` — id-omitted form; the `id` key is omitted from the emitted YAML mapping.
- **0 pipes or >2 pipes** → invalid line; skip with one-line warning `⚠ malformed --queue-spec line (expected 1 or 2 pipes): <line>` and continue parsing the rest.
- **Empty required field after trim** (`slug` or `scope` empty/whitespace-only) → skip line with warning `⚠ malformed --queue-spec line (empty <slug|scope> field): <line>` and continue. Both `slug` and `scope` MUST be non-empty strings per the schema. The placeholder `<slug|scope>` is replaced with the literal name of the missing field (or `slug+scope` when both are empty).
- **Slug fails validation regex** — validate `slug` against `^[a-z0-9][a-z0-9-]*$` (lowercase ASCII alphanumerics + hyphens; no leading hyphen). Skip line with warning `⚠ malformed --queue-spec line (slug fails validation regex): <line>` and continue. The slug is also used for materialization lookup (per §3.3 lookup contract), so the regex matches the canonical filesystem-safe form.

Effect on **frontmatter** (NOT body):

- Append a `queued_specs:` block to the note's **frontmatter** (insert just before the closing `---` of the frontmatter block; preserve all other fields). Each parsed item is emitted as a YAML mapping with `slug:` and `scope:` (and optional `id:`) — `scope:` value MUST be emitted as a **double-quoted YAML string** with `\` and `"` escaped per YAML 1.1 (covers `:`, `#`, leading sigils `>`/`|`/`*`/`&`/`!`, control chars). `slug:` value MAY be emitted unquoted iff it matches the validation regex `^[a-z0-9][a-z0-9-]*$` above; otherwise the line is skipped with warning per the parsing rules. `id:` value MUST be emitted single-quoted per the §3.1 always-quoted-string rule (already specified; example: `id: "56"`).
- If `queued_specs:` already exists in the frontmatter (re-conclude with `--queue-spec`): **deduplicate on slug** — append new items only when the slug is not already present (skip duplicates silently). This preserves prior queue items and adds new ones; existing items are never modified.
- After writing the updated frontmatter, the orchestrator MUST **re-parse the note's frontmatter as YAML** to confirm round-trip success (YAML round-trip check). If parse fails, abort the conclude step with the YAML error message (do NOT flip status to CONCLUDED) and surface to the user. This catches any lingering corrupt-frontmatter case that the quote-on-emit rule missed.

Example emitted block:

```yaml
queued_specs:
  - id: "56"
    slug: removed-cli-flag-hard-fail
    scope: "One-cycle deprecation with explicit error"
  - slug: q3-slice-2-full-reliability
    scope: "Distribution rollup gated on 5-10 release window"
```

5. Flip frontmatter `status: CONCLUDED`.
6. Report: > Note concluded. (If `--queue-spec` ran with non-empty input: also report `> Queued N successor specs in frontmatter: <slug-list>`.)

---

## Archive mode

1. Run Phase 0, read the note.
2. Flip frontmatter `status: ARCHIVED`. Do not delete. Do not prompt — archive is cheap and reversible.
3. Report: > Note archived. Resurrect any time with `/research continue <path>`.

---

## Rules

- **Research notes live only in KB.** No source repo artefacts.
- **Frontmatter is the state machine.** Status transitions happen only in frontmatter; body sections are append-only.
- **Never delete.** Archive instead.
- **Default subtype is `exploration`.** Other subtypes are more specialised.
