---
name: seo-migration-check
description: >
  Validate SEO preservation during site migrations. Checks redirect chains (301 vs 302,
  hop count), canonical consistency, title/meta preservation, HTTP status codes, content
  similarity, and schema preservation. Accepts single URL pair or CSV file of URL pairs.
  Use when user says "migration check", "site migration", "redirect audit", "URL mapping",
  "domain change", "relaunch", "site move".
allowed-tools:
  - Read
  - Bash
  - Glob
  - WebFetch
---

# Site Migration SEO Validator

Validates redirect chains, canonical tags, metadata, and content preservation during site migrations.

## Inputs

Either:
- `old` and `new`: Two URLs for a single-page check (e.g., `https://old.com/page` `https://new.com/page`)
- `file`: Path to CSV/text file with URL pairs, one per line: `old_url,new_url`

If file provided: Read it and process each line. Skip blank lines and lines starting with `#`.
For large files (>50 URL pairs), process first 50 and note truncation.

## Execution

For each URL pair, run checks a-f:

**Check a: Redirect Chain Validation**

Fetch old URL with WebFetch and follow redirects (track each hop):
1. Record redirect type: 301 (permanent), 302 (temporary), 307, 308
2. Count redirect hops
3. Record final destination URL

Evaluate:
- Final destination matches expected `new` URL: PASS — mismatch: FAIL
- Redirect type is 301: PASS — 302/307: WARN (temporary redirects pass less link equity)
- Hop count 1: PASS — hop count 2: WARN — hop count >2: FAIL (redirect chain too long)
- Direct 200 on old URL (no redirect): FAIL (old page still live, not redirected)

**Check b: Canonical Consistency**

Fetch new URL, extract `<link rel="canonical" href="...">` from `<head>`.
- Canonical matches new URL exactly: PASS
- Canonical missing: WARN (Google will infer, but explicit is better)
- Canonical points to old URL: FAIL (critical — tells Google old is authoritative)
- Canonical points to third URL: WARN

**Check c: Title and Meta Preservation**

Compare title and meta description between old URL (before redirect) and new URL.
Note: old URL may already redirect, so if old URL is not directly fetchable, skip comparison and note.

If comparable:
- Title: Extract both. Compare word overlap.
  - >70% word overlap: PASS
  - 40-70% overlap: WARN (may be intentional change)
  - <40% overlap: WARN with note ("significant title change — verify this was intentional")
- Meta description: Extract both.
  - Present on both: PASS
  - Missing on new URL: WARN
  - Both missing: NOTE

**Check d: HTTP Status**

Verify new URL returns 200 OK:
- 200: PASS
- 301/302 (new URL also redirects): WARN with destination
- 404: FAIL
- 500/5xx: FAIL

**Check e: Content Similarity**

If both old and new pages are fetchable, compare word counts:
- New page word count >= 80% of old: PASS
- New page word count 50-80% of old: WARN (possible content reduction)
- New page word count < 50% of old: FAIL (significant content loss)
If old URL not directly fetchable (already redirects): skip and note.

**Check f: Schema Preservation**

Extract `@type` values from JSON-LD blocks on both pages.
- Same schema types present: PASS
- Schema types reduced: WARN (lost structured data)
- Key schema missing on new (e.g., Product, Article, LocalBusiness): WARN
- No schema on either: NOTE (not a regression)

**Overall Per-URL Result**

FAIL: any check is FAIL
WARN: no FAILs but any check is WARN
PASS: all checks PASS or NOTE

## Output Format

```
## Migration Validation: [old URL] → [new URL]
(or: ## Migration Validation: [N] URL pairs from [filename])

### Summary

| Status | Count |
|--------|-------|
| PASS | N |
| WARN | N |
| FAIL | N |
| Total | N |

### Per-URL Results

| Old URL | New URL | Redirect | Canonical | Title | Meta | Status Code | Schema | Overall |
|---|---|---|---|---|---|---|---|---|
| /old | /new | 301✓ | PASS | PASS | WARN | 200 | PASS | WARN |

### Failed Items Detail

For each FAIL result, expanded information:

**[old URL] → [new URL]**
- Redirect: [issue description]
- Canonical: [issue description]
- [etc.]
- Recommended fix: [specific action]

### Recommendations

[Prioritized list of actions based on failures and warnings]

## Data Sources

- Live URL fetching via WebFetch
- Redirect chain analysis (following HTTP headers)
```
