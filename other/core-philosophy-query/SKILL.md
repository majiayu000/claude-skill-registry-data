---
name: core-philosophy-query
description: "Query Drupal core philosophy lenses using evidence-backed positions, tradeoffs, and debate patterns rather than contributor personas."
---

# core-philosophy-query

Answer questions about Drupal core philosophies through public evidence-backed lenses, not named-contributor simulation.

## Mandatory Disclosure

Every response must close with:

> Based on public issue queue records and cross-author analysis. Not authored by or endorsed by any named contributor.

## Inputs

Use this skill when the user asks:
- what philosophy is driving a decision
- what objections are likely on a topic
- how Drupal core tends to think about a subsystem or tradeoff
- which lens applies to a proposal, patch, or technical question

## Required Data Sources

- `config/philosophy-lenses.json`
- `analysis/lenses/author-lens-map.json`
- `config/topic-taxonomy.json`
- `analysis/grounding/manifest.json`
- `analysis/grounding/*.json` as needed through `scripts/build-grounding-bundle.py`

## Required Process

1. Classify the query against the public lenses using:
   - lens `trigger_terms`
   - canonical topic keywords
   - any explicit subsystem language in the user request
2. Use `scripts/build-grounding-bundle.py --topic <topic_id>` or `--file <artifact>` when the query needs grounding evidence.
3. Select the top 1-3 matching lenses.
4. For each selected lens:
   - summarize the likely concern, priority, or tradeoff in neutral prose
   - cite supporting contributors only in the evidence section
   - cite issue CIDs where available
5. If the evidence is weak, split, or keyword-only, say so explicitly.

## Hard Rules

- Do not write in first person as a contributor.
- Do not use signature-phrase imitation.
- Do not answer with “what X would say”.
- Prefer phrasing like:
  - “The strongest lens here is …”
  - “The main objection this lens raises is …”
  - “This is supported by comments from …”

## Output Structure

Use this structure:

### Detected Lenses
- lens name + short reason

### Likely Concerns
- grouped by lens

### Evidence
- named contributors + issue/CID citations

### Uncertainty
- what is weak, missing, or contested
