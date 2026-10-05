---
name: kpa-find-spec-duplications
description: Find duplications across OpenSpec specs and recommend consolidations
context: fork
agent: Sonnet
metadata:
  author: kpa
  updated-date: "2026-03-19"
---

Find duplications across OpenSpec specs and recommend consolidations so specs are not larger than they should be.

## Steps

1. List all spec files in `openspec/specs/*/spec.md` and count total lines per file.
2. Group specs into overlap clusters by naming patterns and subject matter (e.g., specs with "word-lookup" in the name, specs about the same UI component, specs about the same data model).
3. Read every spec file. For each spec, note:
   - What capability it describes
   - What requirements and scenarios it contains
   - What other specs it cross-references
4. Compare specs within each cluster and across clusters. Identify duplications (see categories below).
5. Classify each duplication by severity and recommend an action.
6. Report findings (see format below). Do NOT make changes — only report.

## What Counts as a Duplication

### Eliminable specs (HIGH severity)
- A spec that is purely a summary or reference view of content that lives authoritatively in other specs (e.g., a "data sources" spec that just lists tables and services already documented elsewhere)
- A spec so small and narrowly scoped that it belongs as a requirement inside another spec

### Mergeable specs (HIGH severity)
- Two specs that describe different aspects of the same cohesive capability and would be clearer as one (e.g., "greek-typography" and "greek-web-font-loading" both about Greek font rendering)
- A spec whose requirements all relate to a mode or toggle of another spec (e.g., "reader-text-selection" is entirely about copy mode behavior, which is already the subject of "reader-copy-mode")

### Content duplications (MEDIUM severity)
- The same requirement or scenario appears in two or more specs (e.g., migration logic described in both the feature spec and the migration spec)
- The same behavior is specified with different wording in two specs, creating a risk of specs drifting apart
- Permissions or access control rules duplicated across the feature spec and the admin spec

### Acceptable cross-references (LOW severity — do not report)
- Specs that reference each other for context without duplicating content
- A higher-level spec mentioning a capability that has its own detailed spec
- Shared data models mentioned in multiple specs by name without re-specifying their structure

## What Does NOT Count as a Duplication
- Two specs that mention the same database table or API route in different contexts (that's normal)
- A spec referencing another spec's requirement by name without restating it
- Two specs covering different lifecycle stages of the same entity (e.g., import vs. display)

## Recommended Actions

For each finding, recommend one of:
- **Eliminate**: Delete the redundant spec, moving any unique content to the canonical spec first
- **Merge**: Combine two specs into one, choosing the better name
- **Deduplicate**: Remove duplicated content from the non-canonical spec and replace with a cross-reference note like: `**Note:** [topic] is documented in the [other-spec](../other-spec/spec.md) spec.`

## Report Format

For each duplication found, report:

- **Severity**: HIGH / MEDIUM
- **Type**: Eliminable / Mergeable / Content Duplication
- **Specs involved**: Which spec files
- **What's duplicated**: The overlapping requirements, scenarios, or content (be specific)
- **Canonical home**: Which spec should own this content
- **Action**: Eliminate / Merge / Deduplicate
- **Details**: What exactly to move, merge, or replace with a cross-reference

## Strategy Tips

- Start by grouping specs by naming patterns (shared prefixes like `word-lookup-*`, `text-*`, `reader-*`).
- Small specs (under 50 lines) are prime candidates for merging into a parent spec.
- Reference/summary specs that don't define unique requirements are candidates for elimination.
- When two specs both describe the same scenario, the one closer to the feature (not the architecture overview) is usually the canonical home.
- Read cross-reference notes (`**Note:**` paragraphs) — they may indicate prior consolidation work or remaining duplication.
- Use parallel reads to check multiple specs efficiently.
