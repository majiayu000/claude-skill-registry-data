---
name: trust-appraise
description: >
  Dry-run Trust Magnitude for proposed named skills or suites before curation. Use when deciding whether a proposed suite deserves A/S treatment, when checking Fusion Score structural inputs, when comparing repo stars vs suite component counts, or when asked to appraise a candidate before adding it to the registry.
version: "1.0.0"
genericSkillRef: registry-inspection
---

# /trust-appraise

Runs a **non-mutating** Trust Magnitude dry run. Works in two modes:

1. **Registry node mode** (`--skill`) — appraise an already-curated skill using its live evidence from `registry/nodes/`. Use this during L4 human review to surface real TM and per-row artifact scores before signing off.
2. **Suite proposal mode** (`--repo`) — appraise a proposed suite from live GitHub signals before curation. This is the pre-curation companion to `/trust-appraise-all`.

## Usage

```bash
# Appraise one or more curated registry nodes (use during L4 human review)
PYTHONPATH=src python3 scripts/trust_appraise.py \
  --skill rico-favor/implement-with-discernment \
  --skill caioribeiroclw-pixel/evidence-attestation

# Appraise a proposed suite (pre-curation)
PYTHONPATH=src python3 scripts/trust_appraise.py \
  --repo gsd-build/get-shit-done \
  --components 5 \
  --evidence-path docs/INVENTORY.md

# Default suite appraisal set
PYTHONPATH=src python3 scripts/trust_appraise.py

# Machine-readable output
PYTHONPATH=src python3 scripts/trust_appraise.py --skill foo/bar --json
```

## What it scores

**Registry node mode (`--skill`):** reads `registry/nodes/` directly and calls the same `computeTrustMagnitude` + `computeRowArtifactScores` used by the live registry. Shows per-row artifact scores so you can see exactly which evidence entries are contributing TM and which are scoring 0.

**Suite proposal mode (`--repo`):** builds a temporary skill object combining live GitHub signals:
- `github-stars-own` scored under logarithmic diminishing-returns adoption (`min(175.0, 35.0 * log10(stars/10.0))` capped at 175 TM; #1705), with `skillCountInRepo` so mothership discount applies.
- `repo-own` from live GitHub contributor and contribution counts.
- `fusion-recipe` from the proposed curated component count — structural only, contributing **0 TM**. It feeds the informational **Fusion Score**, never Trust Magnitude (META.md §2.1e).
- Component repository evidence is bounded to 50.0 TM per suite component to prevent sub-suite cap evasion. Grade S (5★) requires an independent witness row (`benchmark-result`, `verifier-attestation`, or Grade A `peer-review`) and cannot be reached by repository stars alone.

## Important caveat

A high dry-run score is **not** promotion approval. Use this skill to surface evidence quality and TM bias before L4 human review, not to bypass review. In particular: `arxiv` entries with 0 citations score 0 TM regardless of `trustNumber`; `social-signal` entries require verifiable view counts — fabricated numbers directly inflate scores.
