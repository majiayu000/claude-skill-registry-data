---
name: review-best-practice-skill
description: Use when evaluating whether a SKILL.md meets STANDARD.md criteria — for PR review of official grimoire-core contributions, self-review before submitting, auditing existing skills, or reviewing skills in a user package that has voluntarily adopted the standard.
source: Linux kernel patch review process, CPython PEP review guidelines, Apache Software Foundation governance
tags: [skill-review, quality-gate, checklist, reviewer, maintainer, defect-prevention, consistency]
---

# Review Best Practice Skill

Evaluate a proposed SKILL.md against grimoire standards and produce a structured
PASS / NEEDS-REVISION / REJECT verdict with specific findings per criterion.

## Why This Is Best Practice

**Adopted by:** Deterministic review checklists are standard in high-quality OSS
projects — Linux kernel patch review, CPython PEPs, React RFC process, and most
projects with a quality bar use structured, criteria-based review over subjective
human judgement.
**Impact:** Structured checklist-based review (Fagan Inspection method, IBM 1976)
achieves 60–90% defect detection — highest of any quality technique per Capers Jones
(Software Quality Engineering, 2011). Consistent criteria reduce reviewer disagreement
from 40–60% (ad-hoc review) to <10% (checklist-based) per Bacchelli & Bird, ICSE 2013.
Agent execution reduces review turnaround from days to seconds.
**Why best:** A checklist applied by humans drifts over time and varies by reviewer.
A skill applied by an AI agent produces identical criteria evaluation every time,
making the standard self-enforcing rather than aspirational.

Sources: Linux kernel patch review process, CPython PEP review guidelines,
Bacchelli & Bird (ICSE 2013), Capers Jones (Software Quality Engineering, 2011)

## Steps

### 1. Read the proposed skill

> **Package scope.** This review applies the full STANDARD.md checklist, which is required for the official **grimoire-core** package. For skills in a user package, this review is optional — use it only if the package has chosen to follow STANDARD.md.

Read the SKILL.md at the path provided (or inferred from context).
Extract: full frontmatter, all `##` section headers, full body content.

### 2. Check frontmatter — FAIL any missing field → REJECT

| Field | Check |
|-------|-------|
| `name` | Passes naming standard: verb-first, specific subject, 2–4 words, no rejected verbs, abbreviation policy applied |
| `description` | Starts with "Use when", describes triggering conditions NOT content, ≤500 chars |
| `source` | Present and names specific institution, standard body, or top-tier companies |
| `tags` | 3–8 tags covering all 4 axes: problem keyword, tool/method, role/context, outcome |

### 3. Check required sections — missing either → REJECT

- `## Why This Is Best Practice` exists
- `## Steps` or `## Core Pattern` exists

### 4. Grill "Why This Is Best Practice" — each sub-field

**Adopted by** — ask these challenge questions:
- Does it name specific companies or institutions? ("many companies" = FAIL)
- Does it claim majority top-tier adoption, not just notable examples?
- Would a domain expert agree this is the majority position?

**Impact** — ask these challenge questions:
- Is the outcome measurable? (%, time saved, defect reduction, risk reduction)
- Is specific evidence cited? (study, company data, systematic review)
- Is "significantly better" or similar vague language present? (FAIL if no number)

**Why best** — ask these challenge questions:
- Is at least one alternative mentioned and explicitly compared?
- Is the argument "this wins because X" rather than just "this is good"?

**Sources** — ask these challenge questions:
- Is the source verifiable? (not just "industry standard" — name the standard)
- Is the source credible? (institution, peer-reviewed research, major engineering blog)

### 5. Check quality criteria

- **Actionable**: steps are concrete, commandable, immediately executable — not theory
- **Scoped**: one concept only — ask "could this cleanly be two skills?"
- **Industry-proven**: cross-check "Adopted by" claim against criterion 3 bar (majority, not minority)
- **Specific**: names tools, cites numbers, shows commands — no abstract rules without examples
- **Complete**: covers failure modes, edge cases, "if X fails do Y" — not just happy path

### 6. Check domain safety (where applicable)

| Domain | Required |
|--------|---------|
| health / medicine | Evidence tier tags `[RCT]`/`[SR]`/`[Consensus]`/`[Practical]` present; healthcare provider footer |
| law | Jurisdiction stated; "not legal advice" disclaimer footer |
| finance / investing | Risk disclosure where relevant; "not financial advice" footer |
| psychology / mental health | No diagnosis/prescription; mental health professional footer |

**Domain safety list:** Valid domains are defined in CLAUDE.md's domain table. If the skill's domain field does not match one of the listed domains, flag it: 'Unknown domain: [domain]. Valid domains: engineering, business, science, health, writing, design, marketing, finance, law, film, music, art, sports, psychology, language, education, cooking, travel, home, parenting, automotive, pets, fashion, environment, photography, productivity, meta.'

### 7. Check size

- Under 50 lines: too shallow — flag for expansion
- Over 300 lines: likely two skills — flag for splitting

### 8. Staleness check

- Does the content reference tools, APIs, or practices that are outdated or superseded?
- Does the "Adopted by" claim reflect current (not historical) practice?
- Search the internet to verify — don't rely on training-data recall alone, since it may predate recent changes. Confirm whether the cited institution/source still holds this position and whether the referenced tool/API is still current before flagging or clearing this criterion. If no internet-access tool is available in this environment, say so explicitly and proceed on best available knowledge — flag the claim as unverified rather than silently skipping the check or asserting it was confirmed. After searching, state what was found (or that nothing conclusive turned up) before proceeding — don't just announce the check and discard the result.

### 9. Output structured verdict

```
## Skill Review: <skill-name>

### Overall Verdict: PASS | NEEDS-REVISION | REJECT

### Findings

| Criterion | Result | Finding |
|-----------|--------|---------|
| name | ✅ / ❌ / ⚠️ | — or specific issue |
| description | ✅ / ❌ / ⚠️ | — or specific issue |
| source | ✅ / ❌ / ⚠️ | — or specific issue |
| tags | ✅ / ❌ / ⚠️ | — or specific issue |
| Why Best Practice — present | ✅ / ❌ | — |
| Why Best Practice — Adopted by | ✅ / ❌ / ⚠️ | — or specific issue |
| Why Best Practice — Impact | ✅ / ❌ / ⚠️ | — or specific issue |
| Why Best Practice — Why best | ✅ / ❌ / ⚠️ | — or specific issue |
| Why Best Practice — Sources | ✅ / ❌ / ⚠️ | — or specific issue |
| Actionable | ✅ / ❌ / ⚠️ | — or specific issue |
| Scoped | ✅ / ❌ / ⚠️ | — or specific issue |
| Industry-proven | ✅ / ❌ / ⚠️ | — or specific issue |
| Specific | ✅ / ❌ / ⚠️ | — or specific issue |
| Complete | ✅ / ❌ / ⚠️ | — or specific issue |
| Domain safety | ✅ / ❌ / N/A | — or specific issue |
| Size | ✅ / ⚠️ | <N> lines |
| Staleness | ✅ / ⚠️ | — or specific issue |

### Required fixes before merge (REJECT / NEEDS-REVISION only)
1. <specific fix with example>
2. <specific fix with example>
```

## Rules

- REJECT if any frontmatter field is missing or empty
- REJECT if `## Why This Is Best Practice` section is absent
- REJECT if "Adopted by" names no specific companies or institutions
- REJECT if "Impact" has no quantified outcome
- NEEDS-REVISION for vague claims that can be strengthened with specifics
- PASS only when all criteria are ✅ — no unchecked items
- When flagging a FAIL or REVISION, always state exactly what fix is needed

**REJECT vs NEEDS-REVISION criteria:**
- **REJECT** — use when: the skill's core premise is wrong (bad source, disproven claim), the skill is a duplicate of an existing skill, or the skill violates STANDARD.md in a way that requires a complete rewrite (not iteration)
- **NEEDS-REVISION** — use when: the skill's premise is sound but execution has fixable issues (missing fields, weak examples, unclear steps, threshold not defined)
- **PASS** — use when: all STANDARD.md criteria are met or only trivial formatting issues remain

Do not REJECT a skill that merely needs improvement — that wastes the author's work. REJECT is for fundamental problems.