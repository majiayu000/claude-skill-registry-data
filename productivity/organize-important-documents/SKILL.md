---
name: organize-important-documents
description: Design, review, and incrementally build a personal or family filing system for important documents and official records. Use when a user wants to organize or audit life-admin records, consolidate material from folders, scans, email, or cloud drives, choose a durable storage home and backup model, or set up a recurring maintenance routine. Also use when the user asks how to organize taxes, identity, immigration, health, insurance, housing, employment, education, legal, finance, travel, estate, or family records for themselves or someone else.
disable-model-invocation: true
---

# Organize Important Documents

Build a durable records system that is easy to search, private, backed up, and simple to maintain. Treat this as records management, separate from general digital decluttering. Prefer one source of truth and small, reversible changes.

## Workflow

### 1. Choose a mode

Start by identifying the user's current need:

- `design`: no coherent system exists.
- `audit`: an existing system needs review.
- `migrate`: records are scattered and need consolidation.
- `maintain`: an established system needs upkeep rules.

When several modes fit, audit first, then move into migration or maintenance.

### 2. Discover scope before location

Ask short questions in batches of no more than five. Begin with what the system should cover, who needs access, which categories are sensitive, and which originals must remain physical. Ask about locations only after the scope is clear. Then establish what sources the user can make available now.

Use [references/interview-checklist.md](references/interview-checklist.md) for question batches. Ask only questions that block a decision; inspect user-provided material when a low-risk read can answer instead. After each batch, summarize what is known, what remains open, and whether the next step is another question batch or inspection.

### 3. Inspect existing material

When the user provides a folder tree, inspect names and paths before proposing changes. Prefer a low-risk inventory read to asking questions about category counts, file types, root depth, duplicate names, or generated files. Open document contents only when necessary and appropriate.

For local folders, use the bundled reports:

- `scripts/inventory_tree.py` for folder depth, counts, and sizes.
- `scripts/extension_summary.py` for file-type mix.
- `scripts/duplicate_name_report.py` for repeated basenames.

Look for useful domain groupings, overloaded roots, official records mixed with working material, inconsistent dates, generated artifacts, and duplicate names that could complicate a move.

### 4. Set the storage boundary

Agree on the primary source of truth, backup, sharing model, and any categories that need separate storage. If the user has not chosen a home, consult [references/storage-and-backup-options.md](references/storage-and-backup-options.md). Proceed incrementally when some choices remain open; mark those decisions as unresolved in the plan.

### 5. Design the filing system

Keep the root narrow and organized by life domain, then by case, provider, or year. Include an inbox for unsorted records and an archive for closed or historical cases. Use ISO dates (`YYYY-MM-DD`) in filenames. Prefer final PDFs, scans, and signed copies; keep drafts, exports, scripts, and scratch work outside the records system unless they belong to a clearly labeled active case.

Use [references/category-patterns.md](references/category-patterns.md) for sample layouts, naming examples, and common exclusions. Make the result understandable to another person who may need to find a record.

### 6. Return a concrete package

After discovery and inspection, provide:

1. **Current state:** what exists, where it lives, and the main risks.
2. **Proposed folder layout:** the root tree and important subfolders.
3. **Naming convention:** rules with concrete filename examples.
4. **Migration plan:** map current sources to target folders.
5. **Maintenance plan:** separate manual tasks from LLM-assisted tasks.
6. **Backup and privacy notes:** source of truth, backup, sharing, and sensitive-category handling.
7. **V1 next steps:** the smallest useful checklist.

### 7. Make upkeep sustainable

Keep the routine light enough to follow. Use [references/maintenance-cadence.md](references/maintenance-cadence.md) when setting a default cadence. Distinguish manual tasks, recurring LLM assistance, and actions that happen only when explicitly requested.

LLM assistance can propose filenames and likely destinations, draft a migration plan, summarize missing paperwork in a case, or review naming and category drift. Keep consequential actions under the user's control.

## Safety and consent

- Confirm the plan before moving or renaming files on a real filesystem.
- Treat health, legal, immigration, identity, and finance records as sensitive by default.
- Check privacy and family-sharing constraints before recommending a cloud service or shared location.
- Keep categories with stricter access in separate locations when needed.
