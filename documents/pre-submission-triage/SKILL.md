---
name: pre-submission-triage
version: 1.2.0
description: When running the pre-submission gate (check_pre_submission.py) or when WARN/FAIL output needs interpretation before submission, classify each finding against known patterns into "must-fix / needs-review / acceptable" and present and record a rationale-backed judgment summary
---

# Pre-Submission Triage Skill

## Purpose
The pre-submission gate `scripts/check_pre_submission.py` mechanically emits PASS/WARN/FAIL, but cannot judge which WARNs are acceptable and which must not be ignored. This skill cross-references gate output against known patterns, classifies each finding as "must-fix / needs-review / acceptable", presents a judgment summary to the author, and records approved judgments with rationale in a log. The goal is to prevent ad-hoc, person-dependent WARN handling and overlooked judgments.

## Trigger Conditions
- When `check_pre_submission.py` is run before submission or manuscript build
- When the author asks how to handle WARN/FAIL output from the gate
- When reviewing results of chapter-completion or periodic quality checks

## Principles
- **FAIL always blocks**: never classify a FAIL as "acceptable"; fix and re-run the gate
- **"Acceptable" WARNs require rationale**: a WARN that matches no known pattern below falls to "needs-review"
- **Record only after author approval**: present the classification and obtain approval before logging. The agent must never silently dismiss a WARN on its own

## Workflow

```text
[Step 1: Run gate] -> [Step 2: Match known patterns] -> [Step 3: Present judgment summary] -> [Step 4: Author approval -> Log]
```

### Step 1: Run the Gate

```bash
python3 scripts/check_pre_submission.py <paper-id> --repo-root <paper-repo-root>
```

If every check is PASS with no WARN, report "gate passed" and stop. Otherwise proceed to Step 2.

### Step 2: Match Findings Against Known Patterns

#### literature-grounding

| Output pattern | Classification | Criterion |
| :--- | :--- | :--- |
| `no matching literature/papers/*.md artifact` (FAIL) | must-fix | No artifact for the citation; create `papers/*.md` |
| `status=manual-stub` | acceptable | Legitimate grounding form for books/theses where PDF auto-fetch is impossible (fact-grounding-rule §2-B-3). **Condition**: the `papers/*.md` records page-anchored excerpts (page-verified excerpts); without excerpts, treat as needs-review |
| `status=abstract-only` | needs-review | Visually confirm whether the manuscript claim depends only on abstract-level content; if dependence is strong, upgrade to full-text or manual-stub with page excerpts |
| `status=full-text but no PDF at _downloads/` | must-fix | The Markdown note is a transcription, not the original. Place the PDF at `_downloads/{slug}.pdf` and re-audit. If there is no redistribution right, drop to `manual-stub` |
| `bot-challenge … human handoff required` (download script) | must-fix (human task) | Automated fetch blocked by reCAPTCHA/Cloudflare. Wait until the user saves the PDF to `_downloads/{slug}.pdf` via browser. Do not retry the same URL or hunt unofficial mirrors (pdf-paper-ingestion Step 1b) |

#### fact-grounding

| Output pattern | Classification | Criterion |
| :--- | :--- | :--- |
| Paragraphs containing only headings, section numbers, version numbers, or publication years | acceptable | Numeric-pattern false positive |
| Count mentions in qualitative text (e.g., "four mechanisms") | acceptable | Design constants, not quantitative claims |
| Quantitative claims (statistics, ratios, multipliers) with no Harvard citation, footnote, `docs/data/` reference, or table reference | must-fix | Add an evidence anchor |

#### output-boundary

| Output pattern | Classification | Criterion |
| :--- | :--- | :--- |
| Internal workflow terms (TDD, test cases, internal file paths) leaking into chapters | must-fix | Never ship internal process vocabulary in the public manuscript; do not treat as WARN |

#### citation-format

| Output pattern | Classification | Criterion |
| :--- | :--- | :--- |
| In-text citation not registered in the matrix | must-fix | Register in `literature-matrix.md` and ground via `papers/*.md` |
| Undefined footnotes / orphan references | must-fix | Restore 1-to-1 consistency between text and references |

### Step 3: Present the Judgment Summary

Present in chat using this format:

```markdown
## Triage Result (<paper-id>, YYYY-MM-DD)

- Gate totals: PASS=n / WARN=n / FAIL=n
- Classification: must-fix n / needs-review n / acceptable n

| Check | Target | Classification | Rationale | Action |
| :--- | :--- | :--- | :--- | :--- |
| literature-grounding | Wood et al. (1976) | acceptable | manual-stub + page-verified excerpts at p.90/98 | none |
| fact-grounding | ch3 §3.2 heading | acceptable | section-number false positive | none |
| fact-grounding | ch5 paragraph X | must-fix | quantitative claim without anchor | add citation footnote |
```

### Step 4: Author Approval and Logging

1. Present the summary and obtain the author's approval for the classifications (especially "acceptable" and "needs-review")
2. After approval, append the judgments to `docs/<paper-id>/design/logs/pre-submission-triage-log.md`:

```markdown
## YYYY-MM-DD — pre-submission triage (<paper-id>)

- Gate: PASS=n WARN=n FAIL=n / Classification: must-fix n, needs-review n, acceptable n

| Check | Target | Classification | Rationale | Action |
| :--- | :--- | :--- | :--- | :--- |
```

3. After completing must-fix items, re-run the gate and append the result to the same log

## Outputs
- Triage judgment summary (presented in chat)
- `docs/<paper-id>/design/logs/pre-submission-triage-log.md` (audit trail of judgments)
