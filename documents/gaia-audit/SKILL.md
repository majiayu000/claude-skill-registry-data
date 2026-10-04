---
name: gaia-audit
description: >
  Focused single-target audit of one Gaia skill, named skill, or real-skill catalog item.
  Use this skill when: auditing a specific skill by ID or name, a skill looks overpromoted,
  evidence feels thin or dead, a contributor's skill seems outdated or superseded, the rank
  doesn't match the source quality, evidence is mapped to the wrong Evidence Type, a skill at 3★+ is
  missing a working GitHub link, someone asks "does this skill deserve its stars?", or you
  want the smallest possible correction with validation — not a bulk sweep.
  This is NOT for bulk curation passes (use /gaia-curate for that) or meta-level registry
  sweeps (use /gaia-meta-audit). It is specifically for "fix this one skill, get it right."
version: 1.0.0
---

# gaia-audit

Perform a focused, single-target audit of one Gaia skill or catalog item and apply the smallest correct source-level fix. The goal is accuracy over coverage: one skill, done properly.

## Why single-target?

Bulk passes introduce unintended side effects and make diffs hard to review. A single-target audit lets you go deep — verifying the actual source material, not just the metadata — and produces a minimal, reviewable change. If you find adjacent issues while auditing, note them but do not fix them in this pass.

## Workflow

### 1. Locate the target

Determine which registry layer owns the skill:
- Generic (starless) canonical skill: `registry/nodes/<id>.json` (or via `registry/gaia.json`)
- Named skill implementation: `registry/named/<contributor>/<skill>.md`
- Real-skill catalog item: `registry/real-skills.json`

Run `rg <skill-id>` across the repo to find every occurrence — frontmatter references, named files, catalog entries, and timeline events — before touching anything.

### 2. Ask the diagnostic questions

Work through these in order. Stop when you find a violation — that's the correction to make.

- Does the skill exist at all in the registry?
- Is it generic (no stars) or named (2★–6★)? Generic skills have no level; only named implementations carry stars.
- Does it map to the claimed Gaia capability? (Check `CONTEXT.md` for canonical vocabulary.)
- Does the evidence actually support the claimed rank (stars)? Re-read each source URL — homepage and directory listings are weak; `SKILL.md` blobs, papers, benchmarks, and release notes are strong.
- Is it outdated, superseded, or a duplicate of something already in the registry?
- For named skills at 3★+: is there a working `blob/branch/subpath` GitHub link? A dead or missing link is grounds for demotion.
- For fusion/upgrade opportunities: note if related basic skills could cleanly consolidate, but do not act on it in this pass unless the target is explicitly the consolidation candidate.
- Does the skill have structural, documentation, or packaging issues? **Classify against the Four-Tier Audit Taxonomy (GOVERNANCE.md §4.2 / RFC #1809):**
  - **Tier 1 (Malicious / Imposter Squatter)**: Bad-faith aggregation, hijacking other maintainers' repos/stars, or falsified attribution → Expungement from registry.
  - **Tier 2 (Packaging / Install Shape Gap)**: Authentic concept and author, but missing standard packaging or broken links → For ≤2★, tag `installable: false` per CONTRIBUTING.md §12. For 3★+, demote to 2★ (or 1★ per Star Bar) and request repackaging. **Never purge or label as an imposter.**
  - **Tier 3 (Early-Stage / Under-Evidenced Stub)**: Authentic author, thin docs or preliminary evidence → Keep at baseline 1★ (Awakened), request doc enrichment, or tag `needs-info`. **Never purge.**
  - **Tier 4 (Product-Coupled / Non-Generalized)**: Real tool documentation needing generalization (#1766, #1801) → Enforce maker attribution via `check_product_attribution.py` and route to generalization.
- **Mandatory Contributor Check**: If the author is a known contributor, co-founder, or team member, deletion is strictly prohibited without direct maintainer outreach and documented review.

Skip the `rarity` field entirely — it is deprecated and carries no review signal (see `CONTEXT.md` § Rarity).

### 3. Present findings before acting

Write out what you found and the proposed correction before making any edit. This gives the user a chance to redirect. If no correction is warranted, say so explicitly with the reason — "no action" is a valid and useful audit outcome.

### 4. Apply the correction via CLI

All mutations go through the CLI, not direct file edits — this preserves timeline logging and schema integrity.

```bash
# Adjust rank (named skills only — use contributor/skill format, not bare generic IDs)
gaia dev calibrate <contributor/skill_id> <N>★

# Change generic type (basic / fusion)
gaia dev reclassify <generic_id> <type>

# Update named status (awakened / named / etc.)
gaia dev update-named <contributor/skill_id> --status <status>

# Add or replace evidence
gaia dev evidence <skill_id> "<url>" --type <arxiv|repo|github-stars|...> --trust <value>

# Log a demotion event in the timeline
gaia dev timeline <skill_id> --action demote --notes "<reason>"
```

For dead evidence links: remove or replace the offending entry, then log a timeline event. Do not patch a `demerits` field — that field is being removed from the schema.

### 5. Regenerate and verify

```bash
gaia dev build       # sync all derivative files after registry edits
gaia dev validate
gaia dev validate --intake
gaia dev test all
git diff --check
```

## Demotion enforcement rules

These are hard rules — they apply regardless of how prominent or well-known the skill is:

- **3★+ without a working `links.github` blob URL** → hard-demote to 1★ (Awakened) — a missing verified blob link is a hard reset, not a soft step-down (META.md §2.4); apply via `gaia dev update-named --status awakened`, then re-earn rank with a valid link
- **Unique-branch skill demoted below 4★** → it loses its Unique-branch rank status; if its structure no longer warrants `fusion`, reclassify the generic to `basic` (`gaia dev reclassify` accepts only `basic` / `fusion`)
- **Dead evidence links** → remove/replace the entry and add a `demote` timeline event
- **Placeholder or non-verifiable evidence only** → demote to Awakened (1★) via `gaia dev update-named --status awakened`
- **Suite components**: the suite itself does not need `links.github`, but each component must have a specific `blob/branch/subpath` URL

## Output

Conclude with a concise report covering:
- Which skill was audited and what layer it lives in
- Evidence reviewed (URLs checked and their quality)
- Correction applied, or the explicit reason no change was warranted
- CLI commands run
- Validation results
