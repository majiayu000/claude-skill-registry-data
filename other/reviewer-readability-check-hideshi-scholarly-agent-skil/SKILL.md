---
name: reviewer-readability-check
version: 1.2.0
description: When a chapter draft is completed/revised or before manuscript build, verify with check_reviewer_readability.py that the prose is at reviewer-readable vocabulary level (internal codes, timestamps, version numbers removed from prose) and that section numbering is consistent (branch suffixes, gaps, duplicates, dangling references), and classify findings as must-fix / needs-review / acceptable with a recorded rationale
---

# Reviewer-Readability Check Skill

## Purpose
Manuscript prose (`docs/<paper-id>/chapters/`) is the reviewer-facing academic layer. Internal symbols (`PROP-*`, `SCAF-FAIL`, `RQ-*`, `PH-*`, sentence-subject `NC-xx`, research-program `種①` / `seed 4`) and careless exposure of JST timestamps or protocol version numbers impede comprehension. Section-number anomalies left over from drafting — branch suffixes (`3.2b`), gaps, duplicates, and dangling `§` cross-references — are editing traces that must not survive into the final build. This skill maps `scripts/check_reviewer_readability.py` output to known patterns, classifies each finding as must-fix / needs-review / acceptable, and presents a rationale-backed summary to the author. The goal is to remove dependence on manual read-throughs for readability assurance.

## When to Use
- When a chapter draft is completed or revised (mandated by `rules/en/reviewer-readability-rule.md`)
- When `assemble_manuscript.py` aborts the build on FAIL
- When the pre-submission gate reports WARN/FAIL for `reviewer-readability`

## Principles
- **FAIL always blocks**: never classify FAIL as acceptable. Rewrite with prose-gloss (Japanese/plain description + parenthesized ID) and re-run
- **WARN requires intent check**: subject-matter mentions (protocol versions, author-approved timestamps) may be acceptable, but only with author approval and logging
- **Preserve the three-layer policy**: tables, blockquotes, and code fences are reference layers (exempt). Appendices and the verification inventory keep full internal codes

## Procedure

```text
[Step 1: Run script] ➔ [Step 2: Match known patterns] ➔ [Step 3: Present triage summary] ➔ [Step 4: Author approval ➔ Log]
```

### Step 1: Run the script

```bash
# Single chapter (on chapter completion)
python3 scripts/check_reviewer_readability.py docs/<paper-id>/chapters/<file>.md
# All chapters (pre-build / pre-submission)
python3 scripts/check_reviewer_readability.py docs/<paper-id>/chapters
```

If PASS with zero findings, report and stop. Otherwise proceed to Step 2.

### Step 2: Match findings to known patterns

| Output pattern | Class | Criteria |
| :--- | :--- | :--- |
| `FAIL/code` (bare `PROP-*` etc.) | must-fix | Rewrite as description + parenthesized ID, e.g. "adopted the AI proposal (`PROP-ADOPT`)" |
| `FAIL/nc` (`NC-xx` outside parentheses / as subject) | must-fix | Rewrite as "a case of X (NC-xx)"; never make the ID the subject |
| `WARN/jst` (timestamp in prose) | needs-review | Consolidate into the audit index table by default; acceptable only for author-approved subject mentions |
| `WARN/version` (`v2.x` in prose) | needs-review | Acceptable where the protocol spec itself is the topic; otherwise use "after the protocol revision" etc. |
| `WARN/jargon` (`grounding`, `ingestion`, `stub`, ...) | needs-review | Parenthesized glosses of defined terms are acceptable; otherwise translate |
| `WARN/program-id` (`種①`, `seed 4`, etc.) | needs-review | Research-program internal numbers. Replace with reader-facing language by default; parenthesized gloss is acceptable |
| `WARN/density` (3+ codes in one line) | needs-review | Split the paragraph or translate to plain description |
| `FAIL/secnum-branch` (branch suffix like `3.2b`) | must-fix | Insertion trace from drafting. Renumber to a plain sequence and update all in-text references |
| `FAIL/secnum-dup` (duplicate section number) | must-fix | Renumber the headings |
| `WARN/secnum-gap` (missing section number) | needs-review | Acceptable if intentional (e.g. planned split); otherwise renumber |
| `WARN/secnum-dangling` (`§` ref with no target) | needs-review | References to external works' sections (three-level numbers like `§2.1.1`) are out of scope; fix if it is an internal reference error |

For deliberate exceptions, add `<!-- readability:ignore -->` to the line and record the rationale in the log (do not abuse).

### Step 3: Present the triage summary

```markdown
## Readability triage (<paper-id>, YYYY-MM-DD)

- Scan: FAIL=n / WARN=n
- Classification: must-fix n / needs-review n / acceptable n

| Target | Finding | Class | Rationale | Action |
| :--- | :--- | :--- | :--- | :--- |
| ch4 §4.1.2 | WARN/jst 15:32 JST | acceptable | Author approved keeping the timestamp | none |
| ch5 §5.1.3 | FAIL/nc NC-09 subject | must-fix | prose-gloss policy | rewrite as "the dependency claim (NC-09) ..." |
```

### Step 4: Author approval and logging

1. Present the summary and obtain approval, especially for "acceptable" classifications
2. After approval, append the decision to `docs/<paper-id>/design/logs/reviewer-readability-log.md` (same table format)
3. After fixing must-fix items, re-run the script and append the result to the same log

## Related
- Detection script: `scripts/check_reviewer_readability.py`
- Enforcement: `assemble_manuscript.py` (aborts build on FAIL; `--force` bypasses), pre-submission gate `check_pre_submission.py` check #5
- General WARN/FAIL triage: `pre-submission-triage` skill
- Full code definitions: the paper's Appendix A.3 (glossary) and verification inventory §4.2

## Outputs
- Readability triage summary (chat)
- `docs/<paper-id>/design/logs/reviewer-readability-log.md` (audit trail of decisions)
