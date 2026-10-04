---
name: write-docs
description: >
  Create or update structured docs under docs/ with frontmatter, numbering,
  lifecycle status, and index regeneration — guides, references,
  troubleshooting, design docs and ADRs. Use for "write a doc", "document
  this", "create a guide", "write an ADR", "update the docs". For the
  system-design thinking itself (architecture, trade-offs, failure modes)
  use /ship:arch-design first — it hands back here to record the decision.
---

# Documentation Standard

All structured docs live under `docs/`. Each subdirectory is a category (e.g., `docs/design/`, `docs/guides/`, `docs/troubleshooting/`). Follow this standard when creating new docs or modifying existing ones.

For design docs and ADRs, the thinking is a separate job: `/ship:arch-design`
walks the design lenses (numbers, failure modes, trade-offs, red-team) and
hands the decision back here. This skill governs how the result is recorded —
design category conventions below, Boundaries required. If a design doc is
requested and no analysis exists yet, run `/ship:arch-design` first.

## Red Flag

**Never:**
- Lead with analysis instead of the decision
- Include implementation details that belong in code
- Mix languages within one document
- Silently delete history — mark superseded sections, don't erase them
- Create a doc without adding it to the docs index
- Mark a doc as `current` without verifying claims against code
- Skip the Boundaries section in design docs — it's the core anti-drift mechanism
- Ship a design doc with zero numbers and zero rejected alternatives —
  that's a description, not a design
- Use a duplicate number within a category

## Frontmatter (Required)

Every managed doc MUST start with YAML frontmatter:

```yaml
---
title: "Human-readable title"
description: "One sentence, under 120 chars — enough for an AI to decide whether to read the doc."
category: "design"
number: "002"
status: current | partially-outdated | superseded | draft | not-implemented
services: [scripts, hooks]  # only when specific dirs/components are affected
superseded_by: "034"        # only when status is superseded
related: ["design/001", "guides/003"]  # category-qualified when cross-category
last_modified: "2026-04-13"
---
```

### Required Fields

- **title**: Match the `# heading` below the frontmatter. Use quotes if it contains special chars.
- **description**: One concise sentence for the docs index — write it for an AI that needs to decide "should I read this doc?" without opening it. Max 120 chars.
- **category**: Matches the subdirectory name (e.g., `"design"`, `"guides"`, `"troubleshooting"`). Must be one of the subdirectories under `docs/`.
- **number**: Unique within its category. Zero-padded 3 digits (e.g., `"002"`, `"029"`). Used for file naming (`029-topic.md`) and cross-referencing.
- **status**: One of the 5 allowed values. See Status Lifecycle below.
- **last_modified**: ISO date (`YYYY-MM-DD`) when the doc was last updated. Must be updated on every edit.

### Conditional Fields

- **services**: Array of affected directories or components.
- **superseded_by**: Required when status is `superseded`. Points to the replacement doc as `category/number`.
- **related**: Include when related docs exist. Array of `category/number` references for navigation.

### Docs Index

After creating or updating a doc, regenerate the index:

```bash
# SKILL_DIR = this skill's base directory (announced as "Base directory
# for this skill" when the skill loaded) — your cwd is the user's repo,
# so a bare relative path will not find the plugin's scripts.
bash "$SKILL_DIR/../../scripts/generate-docs-index.sh"
```

This produces `docs/DOCS_INDEX.md` — a compact table (Category, #, Status, Name, Description, Last Modified, Path) that agents can read on demand to see what docs exist without opening each one. Superseded docs are excluded from the index.

## Status Lifecycle

```
draft → current → partially-outdated → superseded
                ↘ not-implemented (if design was never built)
```

| Status | Meaning |
|--------|---------|
| `draft` | Proposed but not yet approved or implemented |
| `current` | Content matches production code |
| `partially-outdated` | Core content still applies but some details have drifted from code |
| `superseded` | Replaced by another doc — must set `superseded_by` |
| `not-implemented` | Approved but never built |

When changing status, also update `last_modified` to today's date.

## Numbering & File Naming

- Next available number: check `ls docs/<category>/ | sort` and pick the next zero-padded 3-digit number (e.g., `003`, `010`).
- No duplicate numbers within a category. Each top-level doc or directory within a category gets a unique number.
- Sub-documents inside a directory (e.g., `design/014-credentials-vault/plan-1-vault-service.md`) share the parent number.

```
docs/<category>/{number}-{kebab-case-topic}.md
```

Example: `docs/design/029-prototype-v3-web-migration.md`

## Document Structure

```markdown
---
(frontmatter)
---

# {Number} — {Title}

## Status

{Status explanation with context — why it has this status, what changed}

## Summary

{2-3 sentences: what problem this solves and the key content}

## (Body sections — flexible per topic and category)

## References

- Related docs, external links, prior art
```

### Writing Rules

- Lead with the decision or answer, not the analysis. Readers want to know "what" before "why."
- Use concrete file paths, struct names, and API endpoints — not abstractions.
- If the doc is in Chinese, keep it in Chinese. If in English, keep it in English. Don't mix.
- Mark superseded sections inline with strikethrough or a note, don't silently delete history.
- When content changes, update the existing doc rather than creating a new one — unless the change is a complete replacement (then supersede).

## Category Conventions

### design (architectural decisions)
- **Boundaries section required** — the core anti-drift mechanism
- **Recommended body shape** (adapt, don't pad — a small ADR needs only
  Context, Decision, Trade-offs, Revisit triggers):
  Context → Goals / Non-goals → Requirements & numbers → Design
  (components, data model, contracts) → Failure modes → Rollout &
  operations → Security → Alternatives considered → Assumptions →
  Revisit triggers
- **Trade-offs section recommended** — what alternatives were considered, what was given up, and why this choice won
- **Assumptions section recommended** — state what must be true for this design to hold (e.g., "assumes < 10k users", "assumes single-region"). When assumptions change, the doc is stale.

### guide (how-to guides)
- Step-by-step structure with numbered steps
- Include prerequisites and expected outcomes
- Code examples should be copy-pasteable

### troubleshooting (debug playbooks)
- Symptom → Diagnosis → Fix structure
- Include exact error messages for searchability
- Link to related design docs for context

### reference (API docs, schemas, config reference)
- Organized by entity or endpoint
- Include examples for every parameter
- Version-sensitive — note which versions apply

Other categories: any subdirectory under `docs/` becomes a category; adapt the body to fit, universal rules still apply.

## Cross-References

- Reference docs in the same category by number: "see 023-agent-broker-architecture"
- Reference docs in other categories with category prefix: "see `guides/003-getting-started`"
- When renaming/renumbering, update ALL references. Use: `grep -r "old-name" docs/`

## Verification

Before marking a doc as `current`, verify key claims against code:
- Do referenced file paths exist?
- Do referenced struct/function names exist?
- Do referenced API endpoints exist?
- Does the described architecture match the actual service boundaries?

Update `last_modified` when you complete verification.

## Execution Handoff

After writing or updating a doc, regenerate the index and output the
report card — read the format from `../shared/report-card.md` (resolved
against this skill's base directory, not the working directory):

```
## [Write Docs] Report Card

| Field | Value |
|-------|-------|
| Status | <DONE / BLOCKED> |
| Summary | <category/number: doc title — created / updated / superseded> |

### Metrics
| Metric | Value |
|--------|-------|
| Docs created | <N> |
| Docs updated | <N> |
| Index regenerated | yes / no |

### Artifacts
| File | Purpose |
|------|---------|
| docs/<category>/<number>-<topic>.md | The doc |
| docs/DOCS_INDEX.md | Regenerated index |

### Next Steps
1. **Review the doc** — read it and verify claims against code
2. **Deepen the design thinking** — /ship:arch-design if the analysis needs more depth
3. **Plan implementation** — /ship:design to turn the decision into executable stories
4. **Ship it** — /ship:handoff to create a PR with the doc changes
```
