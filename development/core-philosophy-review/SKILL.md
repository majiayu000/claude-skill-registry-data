---
name: core-philosophy-review
description: "Review a patch, proposal, or technical question through Drupal core philosophy lenses with evidence-backed findings."
---

# core-philosophy-review

Review work through Drupal core philosophy lenses rather than named reviewer personas.

## Mandatory Disclosure

Every response must close with:

> Based on public issue queue records and cross-author analysis. Not authored by or endorsed by any named contributor.

## Inputs

Use this skill when the user asks:
- review this patch through core philosophies
- what objections would core lenses raise
- how this change fares against Drupal core priorities

## Required Data Sources

- `config/philosophy-lenses.json`
- `analysis/lenses/author-lens-map.json`
- `analysis/grounding/manifest.json`
- `analysis/grounding/*.json` as needed through `scripts/review-with-philosophy.py`
- `scripts/review-with-philosophy.py`

## Required Process

1. Detect the relevant subsystems, tradeoffs, and canonical topics from the artifact.
2. Run `python3 scripts/review-with-philosophy.py --file <artifact> --grounding-mode on` when a file or diff is available.
3. Select the 1-3 strongest relevant public lenses.
4. For each lens:
   - identify likely objections, constraints, and approval conditions
   - cite named evidence sources only in the supporting evidence section
5. Synthesize:
   - agreement between lenses
   - unresolved tension
   - missing evidence
6. If selected lenses sit on a configured `tension_axis`, surface the corresponding counter-lens even if it was not in the initial top 3.
7. If the disagreement is about product direction, release timing, governance, or site-builder value, include the `project-stewardship` review lens.
8. Save the full output, unmodified, to `~/Codex/drupal-core-reviews/YYYY-MM-DD-{slug}.md` with the required frontmatter from `AGENTS.md`.

## Hard Rules

- No contributor roleplay.
- No first-person reviewer simulation.
- Findings must be grouped by lens, not by person.
- Named contributors may appear only as provenance/evidence.
- Prefer configured lens oppositions over ad hoc named-person conflict.
- Use the project-stewardship review only at the level of project-wide tradeoffs, not as a replacement for subsystem expertise.

## Output Structure

### Selected Lenses

### Findings By Lens
- lens name
- likely objection
- likely approval condition
- evidence

### Cross-Lens Tension

### Blind Spots

### Arbiter Lens
- project-strategy / State-of-Drupal citations when `project-stewardship` is selected
- issue-backed arbiter support

### Recommendation
