---
name: audit-best-practice-domain
description: Use when you need to assess the quality of all skills in a grimoire domain or sub-domain — before a release, after a bulk contribution, or when adopting a domain for the first time.
source: Wikipedia Featured Article review criteria, npm package quality scoring, Apache project governance
tags: [skill-quality, domain-health, bulk-review, maintainer, repo-health]
---

# Audit Best Practice Domain

Batch-review all SKILL.md files in a grimoire domain or sub-domain and produce a
structured quality report showing PASS / NEEDS-REVISION / REJECT per skill.

## Why This Is Best Practice

**Adopted by:** Batch quality audits are standard in OSS projects with quality bars —
Linux kernel subsystem maintainers review all patches in a tree before release, npm
registry uses automated batch checks across all packages, and the Python Package Index
runs consistency checks across the full package set.
**Impact:** Individual ad-hoc review of large corpora is inconsistent — Bacchelli &
Bird (ICSE 2013) found reviewer agreement drops sharply without structured criteria.
Batch audits with a consistent rubric catch systemic issues invisible in individual
review: outdated patterns reviewers normalize over time, structural inconsistencies
across the corpus, and quality drift between releases. Both npm's automated package
quality scoring and Wikipedia's Featured Article batch review demonstrate that
per-item pass/fail metrics enable quality tracking over time in ways ad-hoc review
cannot reproduce.
**Why best:** A file-by-file manual review is unrepeatable and doesn't produce a
comparable baseline across releases. A batch audit with a consistent rubric produces
actionable counts that track over time.

Sources: Wikipedia Featured Article review criteria, npm package registry audit tooling,
Bacchelli & Bird (ICSE 2013)

## Steps

### 1. Identify the audit target

User provides a domain or sub-domain path:
- Full domain: `health/`
- Sub-domain: `engineering/testing/`
- All skills: `.` (repo root)

If no path provided, ask: "Which domain or sub-domain should I audit?"

### 2. Find all SKILL.md files

```bash
find <target-path> -name "SKILL.md" | sort
```

If zero files found: report "Domain has no skills yet" and stop.

### 3. Apply `review-best-practice-skill` to each file

**Error handling:** If a domain referenced in the audit target does not exist in the installed skills index, stop and output: 'Domain not found: [domain-name]. Run /discover-best-practices to see installed domains.' If a skill file is missing or malformed (can't be parsed), mark it as UNREADABLE in the report and continue with remaining skills — do not abort the entire audit.

For each SKILL.md, run the full `review-best-practice-skill` evaluation:
- Check frontmatter (name, description, source, tags)
- Check required sections (`## Why This Is Best Practice`, `## Steps`)
- Evaluate "Why This Is Best Practice" sub-fields
- Check 5 quality criteria
- Check domain safety footer
- Check size (50–300 lines)

### 4. Handle REJECT immediately

If any skill produces a REJECT verdict:
- Flag it prominently in the report
- List all REJECT reasons with required fixes
- Continue auditing remaining skills (don't abort the whole audit)

### 5. Produce summary report

```
## Domain Audit: <path>

### Summary
- Total skills: N
- PASS: N
- NEEDS-REVISION: N  
- REJECT: N

### Results

| Skill | Path | Verdict | Top Issue |
|-------|------|---------|-----------|
| propose-commit | engineering/development/skills/propose-commit | PASS | — |
| skill-name | path/to/skill | NEEDS-REVISION | Impact: no number cited |
| skill-name | path/to/skill | REJECT | Adopted by: no specific names |

### Required fixes (REJECT / NEEDS-REVISION only)

**skill-name** (REJECT)
1. "Adopted by" names no specific companies — add named institutions
2. "Impact" missing — add measurable outcome with citation

**skill-name** (NEEDS-REVISION)
1. "Impact" says "significantly improves" — cite the study or number
```

### 6. Recommend action

After the report:
- If all PASS: "Domain is release-ready."
- If any REJECT: "Domain blocked — N skill(s) must be fixed or removed before release."
- If NEEDS-REVISION only: "Domain releasable with known debt — N skill(s) need improvement."

**Recommendation criteria:** Only include a recommendation if:
- A skill has a REJECT or NEEDS-REVISION finding (not just WARNING)
- OR a skill is missing required frontmatter fields (name, description, source, tags)
- OR a skill's description doesn't start with 'Use when'

Do not recommend action for WARNING-only findings — warnings are informational. Recommendations must be actionable: 'Add `source:` field to [skill-name]' not 'Improve skill quality.'

## Rules

- Never modify skill files during an audit — read-only
- Apply the same `review-best-practice-skill` criteria to every file — no exceptions for "almost passing"
- If a domain has 0 skills, report that; don't invent findings
- A REJECT in one skill does not block reporting other skills — complete the full sweep
- Report counts at the top so maintainers can assess at a glance without reading every row

## Common Mistakes

**Stopping at first REJECT**: audit the whole domain, then report. Stopping early
leaves the maintainer with an incomplete picture.

**Inconsistent standards**: apply identical criteria to every skill. Don't soften
"Adopted by" requirements for skills in domains where data is harder to find.

**Audit without action**: a report is only useful if it drives fixes. End every
NEEDS-REVISION or REJECT finding with the specific fix required.