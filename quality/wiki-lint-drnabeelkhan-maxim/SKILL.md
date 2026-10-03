---
skill_id: wiki-lint
name: Wiki Lint
description: "Audit wiki health — \"wiki health check\", \"audit the wiki\", \"find contradictions\", weekly pass, before a major content release. Catches contradictions, stale pages, orphans, duplicate concepts and broken links."
version: 1.0.0
category: knowledge-management
type: audit
frameworks:
  - llm-wikid-pattern
triggers:
  - weekly schedule
  - "wiki health check"
  - "audit the wiki"
  - "find contradictions"
  - before any major content release
collaborates_with:
  - wiki-ingest
  - wiki-query
  - wiki-explore
  - memory-palace
  - knowledge-base-curator
ethics_required: false
priority: medium
tags: [knowledge, audit, mempalace, contradictions, staleness]
created: 2026-04-16
updated: 2026-04-16
---

# Wiki Lint

## Purpose

Audit the wiki for structural and quality issues. Catches contradictions, stale content, orphan pages, duplicate concepts, missing sections, and broken `[[wikilinks]]` BEFORE downstream agents act on stale or conflicting data.

Run weekly (default Mondays via scheduled task). Outputs `lint-report.md` for human review — never auto-fixes.

## When To Invoke

- Weekly schedule (default: Mondays at 7am via `/mxm-tasks`)
- User asks for "wiki health check" or "audit the wiki"
- Before any major content release
- After bulk ingest of >50 pages

## Checks Performed

### 1. Contradictions

For every entity or concept appearing in multiple pages, compare claims using:
- `mempalace_kg_query(entity, direction="both")` — find all triples for that entity
- `mempalace_search(entity)` — find all pages mentioning it
- Flag pages making contradictory factual claims

### 2. Stale Content

- Pages where `updated` date > 90 days old AND `confidence: high`
- These are high-confidence claims that may have decayed
- Output: list with last-updated date, suggest re-verification

### 3. Orphan Pages

- Pages with **zero** inbound `[[wikilinks]]` from other pages
- Use `mempalace_find_tunnels` and graph queries
- Suggest either deletion or linking from related pages

### 4. Duplicate Concepts

- Different page names covering the same idea (semantic similarity)
- Use `mempalace_check_duplicate(content, threshold=0.85)`
- Suggest merge with target page

### 5. Missing Mandatory Sections

For every page, verify presence of:
- `## TLDR`
- `## Counter-Arguments`
- `## Related` (with at least 2 wikilinks)
- `## Sources`

Pages missing any: flag for completion.

### 6. Broken Wikilinks

- `[[wikilinks]]` pointing to non-existent pages
- Suggest: create stub page, fix link target, or remove

### 7. Confidence Inconsistency

- Pages with `confidence: high` but `explored: false` — invalid combination
- Suggest: lower confidence to `medium` OR run `/mxm-wiki explore` to verify

### 8. AI-Tell Contamination

- Any page containing phrases from `.brand-foundation/personal/ai-tells.md`
- Suggest: rewrite that paragraph

## Output Format

```
Wiki Lint Report — [YYYY-MM-DD HH:MM]
Total pages audited: [N]
Issues found: [N]

## Contradictions ([N])
- entity: <X>
  - page: [[A]] claims: "<claim 1>"
  - page: [[B]] claims: "<claim 2 — contradicts>"
  - resolution: HUMAN_REVIEW

## Stale Content ([N], confidence:high + updated >90d)
- [[<page>]] (updated YYYY-MM-DD, [N] days old) — re-verify

## Orphan Pages ([N])
- [[<page>]] — 0 inbound links — suggest delete OR link from [[parent-concept]]

## Duplicate Concepts ([N])
- [[<page-A>]] ≈ [[<page-B>]] (similarity 0.92) — suggest merge into [[<page-A>]]

## Missing Sections ([N])
- [[<page>]] — missing: Counter-Arguments, Sources

## Broken Wikilinks ([N])
- [[<page>]] → [[<missing-target>]] — suggest: create stub OR fix typo

## Confidence Inconsistency ([N])
- [[<page>]] — confidence:high + explored:false → set medium OR run /mxm-wiki explore

## AI-Tell Contamination ([N])
- [[<page>]] paragraph 3 contains banned phrase: "delve into the landscape"

---
Confidence: 🟢 HIGH (full corpus scanned, all checks passed) | 🟡 MEDIUM (sample only, time-bounded) | 🔴 LOW (corpus too large to fully audit; partial report)
Next: human review at lint-report.md, then `/mxm-wiki explore` for any flagged unverified pages.
```

**Output is written to** `lint-report.md` in the project root (under `.mxm-knowledge/` if using project-scoped knowledge).

## Critical Rule

**`wiki-lint` NEVER auto-fixes.** All changes require human review. The skill produces findings; the operator decides resolution.

## MemPalace Integration

```
mempalace_kg_query(...)        # contradictions
mempalace_check_duplicate(...) # duplicates
mempalace_find_tunnels(...)    # orphan / linking analysis
mempalace_search(...)          # full-corpus audit pass
mempalace_kg_timeline(...)     # staleness via update history
```

## Handoff

- Contradictions found → escalate to `wiki-explore` (human verification queue)
- Stale high-confidence pages → notify `wiki-ingest` to re-check sources
- Compliance-sensitive contradictions → loop `compliance-officer`
- AI-Tell contamination → notify `brand-guardian` for rewrite

## Maxim Behavioral Layer

- **Confidence tagging**: 🟢 HIGH on full-corpus audit | 🟡 MEDIUM on sampled | 🔴 LOW on partial
- **Frameworks**: LLM Wikid quality control pattern
- **Anti-noise**: thresholds tuned to minimize false positives (similarity 0.85 for duplicates, 90d for staleness)

## Source References

- `FINAL_RELEASE_CHANGES/Brandvoice-wiki-example.md` — wiki-lint pattern
- `documents/reference/AGENTS.md` — wiki trust levels
- `.brand-foundation/personal/ai-tells.md` — AI-tell scanner source

---
_Copyright (c) 2026 iSystematic Inc. Maxim product. BSL 1.1._
