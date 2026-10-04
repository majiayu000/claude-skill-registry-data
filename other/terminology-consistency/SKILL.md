---
name: terminology-consistency
version: 1.0.0
description: On chapter completion and before manuscript builds, mechanically detect terminology drift (reappearing registered variants) and unglossed glossary terms with check_terminology_consistency.py, run an LLM semantic review for synonymous drift that machines cannot catch, and accumulate confirmed findings in terminology-variants.yml
---

# Terminology Consistency Skill

## Purpose
Terminology drift in the manuscript (`docs/<paper-id>/chapters/`) harms reviewer comprehension and claim precision. This skill addresses drift through **three layers**:

1. **Mechanical layer (regression prevention)**: `scripts/check_terminology_consistency.py` detects registered variants (FAIL) and glossary English terms appearing without their Japanese gloss (WARN). The bilingual glossary (`literature/bilingual-glossary.md`) is used directly as the dictionary — no duplicate term list is maintained
2. **LLM layer (semantic discovery)**: Synonymous drift with different surface forms (e.g., "主張トーン" vs "主張の強度") cannot be detected mechanically. The agent reads the chapters and clusters candidate phrases that refer to the same concept, presenting them to the author
3. **Accumulation layer (learning)**: Terms the author confirms as drift are appended to `design/sot/terminology-variants.yml`. From then on, the mechanical layer prevents recurrence with FAIL. Human discoveries are never one-off events

## Trigger Timings
- When a chapter file is written or revised (mechanical layer is mandatory)
- When `assemble_manuscript.py` aborts a build due to FAIL
- When the pre-submission gate returns WARN/FAIL for `terminology-consistency`
- When the author points out terminology drift (LLM-layer review + accumulation)

## Principles
- **FAIL (registered variant reappearance) always blocks**: the canonical form is already author-confirmed. Never classify as "no action needed"
- **WARN (unglossed English) requires intent check**: definition sentences, proper nouns, and bibliography titles may be "no action needed", subject to author approval and logging
- **Acknowledge mechanical limits**: do not expect machines to find unknown synonyms. Discover them in the LLM layer and feed them back into the mechanical layer via accumulation
- **Single source of truth**: update the glossary (`bilingual-glossary.md`) first when adding or changing terms; regenerate or sync Appendix A accordingly

## Procedure

```text
[Step 1: Mechanical scan] ➔ [Step 2: Match known patterns] ➔ [Step 3: LLM semantic review] ➔ [Step 4: Author judgment ➔ accumulate in variants.yml]
```

### Step 1: Mechanical Scan

```bash
# Single chapter (on completion)
python3 scripts/check_terminology_consistency.py docs/<paper-id>/chapters/<file>.md
# All chapters (before build / submission)
python3 scripts/check_terminology_consistency.py docs/<paper-id>/chapters
```

Even when the scan passes, the Step 3 semantic review may still be run (the mechanical layer does not catch unknown drift).

### Step 2: Match Findings to Known Patterns

| Output pattern | Classification | Criteria |
| :--- | :--- | :--- |
| `FAIL/variant` (registered variant reappears) | Fix required | Unify to the canonical form shown in the hint. No exceptions |
| `WARN/gloss` (glossary English term appears bare) | Needs review | Rewrite as "日本語（English）", or register in the allowlist if a definition sentence / established abbreviation |
| Reference sections, tables, code fences | Out of scope | Automatically excluded (bibliography titles are verbatim) |

For deliberate exceptions, add `<!-- terminology:ignore -->` to the line and record the rationale in the decision log (do not abuse).

### Step 3: LLM Semantic Review (drift machines cannot catch)

1. Read the Japanese column of the glossary and search the prose for candidate phrases that differ on the surface but refer to the same concept
2. Cluster candidates and present them to the author with locations (file and line)
3. The **author** makes the final call on whether a candidate is a synonym or a distinct concept (e.g., "適正オフローディング" is a distinct coined term, not drift of "認知オフローディング")

### Step 4: Author Judgment and Accumulation in variants.yml

1. Append confirmed drift to `docs/<paper-id>/design/sot/terminology-variants.yml`

```yaml
variants:
  - canonical: 主張の強度
    variants:
      - 主張トーン
    note: 2026-08-17 author decision. Unified Japanese gloss for Modality
```

2. Fix the affected prose to the canonical form and re-run the script to confirm FAIL=0
3. Append the decision summary to `docs/<paper-id>/design/logs/terminology-consistency-log.md` (date, finding, classification, rationale, action)

## Related
- Detection script: `scripts/check_terminology_consistency.py`
- Mandatory invocation: `assemble_manuscript.py` (aborts build on FAIL; `--force` overrides), pre-submission gate `check_pre_submission.py` check #6
- Internal-symbol leak detection: `reviewer-readability-check` skill (same three-layer vocabulary policy)
- General WARN/FAIL triage: `pre-submission-triage` skill

## Outputs
- Terminology triage decision summary (presented in chat)
- `docs/<paper-id>/design/sot/terminology-variants.yml` (accumulated drift, source of truth)
- `docs/<paper-id>/design/logs/terminology-consistency-log.md` (decision audit trail)
