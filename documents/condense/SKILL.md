---
name: condense
description: Deduplicate and consolidate CLAUDE.md, rules, and project docs (spec.md, plans, runbooks) across the hierarchy.
---

# Instruction + Doc Condensation

Deduplicate and consolidate CLAUDE.md / rules / project docs to remove redundancy.

## Delta-update discipline applies here too

Canonical rule: "Delta-update, never rewrite" (keep this as a rule in your own `~/.claude/rules/`). This skill is the periodic-dedup arm of that pairing. Run triggers:

- `/retro` ran or a section accumulated ≥3 overlapping bullets (existing).
- A project's bloat-override / sentinel-bypass log accumulated ≥3 entries since the last condense run (NEW).
- `<project>/docs/spec.md` crossed a 100-line growth boundary - 600, 700, 800… (NEW).

These are *reminders surfaced during `/retro`*, never auto-fire. Same posture as the "≥3 overlapping bullets" rule.

Phase 4 is per-item Edits with user approval (Phase 3); never draft a "consolidated v2" of a whole file and ship it as one Write. If a proposed change spans more than a handful of items, split it.

## Workflow

### Phase 1: Discovery

**Find all instruction + reference doc files across the hierarchy:**

Use Glob to search for both instruction files and project-doc reference files. The corpus extends beyond CLAUDE.md so cross-file dup detection catches drift between rules and the docs they mirror.

1. `**/CLAUDE.md` and `**/CLAUDE.local.md` in the project root
2. `.claude/rules/*.md` in the project root
3. `~/.claude/CLAUDE.md` (global personal instructions)
4. `docs/spec.md` (NEW - project reference doc)
5. `docs/human/*.md` (NEW - human-facing runbooks, e.g. cloud-env-setup)
6. `docs/plans/*.md` (NEW - top level only; see non-targets below)

**Explicit non-targets** (skip even when matched by broader globs):
- `docs/plans/archived/**` - frozen post-mortems, never modified.
- `docs/analysis/**` - `.claudeignore`'d one-off audits.

**Read all discovered files and analyze for:**
1. Intra-file duplication (same instruction repeated within a file)
2. Cross-file duplication (same instruction in multiple files, or same point in `docs/spec.md` AND a rule, or `docs/spec.md` AND `CLAUDE.md`)
3. Misplaced instructions (subdirectory files containing project-wide content)
4. Trigger-table drift (NEW)
5. Plan supersession (NEW)
6. Section-size flagging (NEW)

### Phase 2: Analysis

**Intra-file duplication:**
- Identify repeated bullet points or instructions
- Find semantically similar content (different wording, same meaning)

**Cross-file duplication:**
- Root CLAUDE.md should contain project-wide instructions
- Subdirectory CLAUDE.md should only contain directory-specific instructions
- If an instruction appears in both root and subdirectory, keep only in root
- If an instruction in subdirectory applies to whole project, move to root
- Same point in `docs/spec.md` AND a rule, or `docs/spec.md` AND `CLAUDE.md` → keep in the more specific file and replace the other with a `→ see <path> §<heading>` pointer

**Misplaced instructions:**
- Subdirectory file contains instructions that apply project-wide → move to root
- Root file contains instructions only relevant to one directory → move to subdirectory

**Trigger-table drift:**
- CLAUDE.md keeps a reference index whose "Read" column points to `docs/spec.md` § headings.
- Parse the trigger-table rows; for each `docs/spec.md`-typed target, grep the spec for a matching `## ` or `### ` heading.
- Flag rows whose target heading no longer exists or was renamed. Default action: flag-only with the closest existing heading shown side-by-side; promote to propose-and-apply only if the user repeatedly takes the obvious fix.

**Plan supersession:**
- For each `docs/plans/*.md` (top level only - archived plans excluded), grep for `SHIPPED`, `DONE`, `landed`, `archived to`.
- When a marker appears next to verbose pre-ship phase prose, flag the section above as a collapse-candidate. Proposed Edit replaces N lines of phase prose with one done-line citing the marker (e.g. `*Shipped 2026-04-28 in commit `abc1234` - see `docs/plans/archived/<file>.md`.*`).

**Section-size flagging:**
- For `docs/spec.md`, walk L2 headings and measure char count per section.
- Flag any section >1500 chars. If you run a docs-bloat gate (a hook that blocks oversized doc sections), mirror its per-section character threshold here - sections that would no longer qualify for a heading exemption are dedup/split candidates.

### Phase 3: Interaction

Present findings using AskUserQuestion with checkboxes.

**For each issue found:**
1. Show the duplicated, misplaced, or drifted content
2. Identify which files are affected
3. Propose the consolidation (delete, move, merge, or replace-with-pointer)

Trigger-table drift findings render old-row → closest-heading side-by-side. Plan supersession findings show "collapse N lines into 1 done-line" with the proposed replacement text.

**Example:**
```
Issue: "Use 2-space indentation" appears in both ./CLAUDE.md and ./src/CLAUDE.md
Proposal: Remove from ./src/CLAUDE.md (already covered by root)
```

Wait for user approval before implementing.

### Phase 4: Implementation

For approved changes:

1. **Remove duplicates** - Delete redundant entries, keeping the most appropriate location
2. **Move misplaced content** - Transfer instructions to correct hierarchy level
3. **Merge similar items** - Combine semantically similar instructions into one
4. **Replace duplicates with pointers** - When two files held the same point and one is now canonical, replace the other with `→ see <path> §<heading>`

**Gate-aware pre-check (advisory, not blocking).** If your project runs a docs-quality gate (a hook that blocks low-quality or oversized doc edits), pre-check each approved Edit on `docs/spec.md` (or any other gated path) against the same rules the hook uses *before* applying - so you reword ahead of the block rather than after it:

1. Compute the proposed `new_text`.
2. Run the gate's "slop term" / banned-phrase check on `new_text` - if it would trip, surface to the user: "This Edit would trip the docs gate with terms: [...]. Reword?"
3. For longer additions, run the gate's lexical-density / readability check - if it would fall below the threshold, surface to the user.
4. A pure char-delta size cap is usually **not** pre-checked. Condense Edits are usually subtractive; on rare additive cases the sentinel bypass is the right escape hatch.

Pre-check failures are advisory - the user can proceed (and the hook stays the unbypassable line of defence). The point is to reword *before* the hook blocks rather than after.

**Hierarchy rules:**
- `./CLAUDE.md` - Project-wide instructions (highest priority)
- `./.claude/rules/*.md` - Topic-specific rules (modular)
- `./docs/spec.md` - Project reference docs (CLAUDE.md trigger-indexed; section-sized for spec tier)
- `./subdir/CLAUDE.md` - Only instructions specific to that subdirectory
- `~/.claude/CLAUDE.md` - Personal preferences across all projects
- `./CLAUDE.local.md` - Personal project-specific (not shared)

## Resources

This skill is self-contained. If you also keep a `reflect`-style skill, it may ship helpers worth reusing here:

- A "locate all CLAUDE.md files" script (the same Glob discovery Phase 1 does by hand).
- A memory-locations reference (the memory hierarchy details).
- An anti-patterns reference (what to avoid when writing instructions).

None are required - Phase 1's Glob discovery and the hierarchy rules above cover the mechanism on their own.
