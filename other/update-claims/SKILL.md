---
name: update-claims
description: Find outdated stats and assertions in an extracted article. For each, check freshness and propose a replacement with a current source.
allowed-tools: Read, Write, WebFetch, WebSearch
---

# Update Claims Skill

Articles age via stale data more than via stale prose. This skill walks every numerical claim and checks whether it still holds. Then it proposes replacements with current sources.

## Input

`/update-claims <slug>`

Reads:
- `content-pipeline/updates/1-extracted/{slug}.md` (with the "Numerical claims" section)
- `content-pipeline/updates/0-guidance/{slug}.md` (if exists — for which claims to focus on)

## Process

1. **Read the extracted file's "Numerical claims" section.**
2. **For each claim:**
   - Identify the source currently cited (from the extract, if any)
   - Search for a more recent, authoritative source on the same statistic (use WebSearch + WebFetch)
   - Compare current value with the article's value
   - Decide: **still valid** / **needs replacement** / **wrong** / **unverifiable**
3. **For each "needs replacement":**
   - Find the new value
   - Find the current source URL
   - Suggest the rewrite (the original sentence + the proposed new sentence)
4. **For each "wrong":**
   - Note the actual value
   - Recommend either replacement or removal of the claim
5. **For each "unverifiable":**
   - Note that no current source could be found
   - Recommend either flagging for human review or removing
6. **Write the audit** to `content-pipeline/updates/2-update-claims/{slug}.md`:

```markdown
# Claims audit: {slug}

## Summary
- Total claims reviewed: {n}
- Still valid: {n}
- Needs replacement: {n}
- Wrong: {n}
- Unverifiable: {n}

## Replacement queue (apply these in /update-draft)

### Claim 1
- **Original sentence:** "..."
- **Original source:** [link or "no source"]
- **Status:** needs replacement
- **New value:** ...
- **New source:** [Title](url)
- **Proposed rewrite:** "..."

### Claim 2
...

## Wrong claims (to remove or correct)

### Claim N
- **Original sentence:** "..."
- **Why it's wrong:** ...
- **Suggested action:** remove / replace with: "..."

## Unverifiable claims (flag for human)

### Claim M
- **Original sentence:** "..."
- **What we tried:** ...
- **Suggested action:** ...
```

## Output

`content-pipeline/updates/2-update-claims/{slug}.md`

A queue of specific edits the `update-draft` skill will apply.

## Quality checklist

- [ ] Every numerical claim from the extract has a status
- [ ] No fabricated "new sources" — every replacement has a real, verifiable URL
- [ ] Suggested rewrites match the original sentence's voice and length
- [ ] Wrong claims include a clear reason

## What to NOT update

- Round-figure claims with no time-decay risk ("there are 12 months in a year")
- Brand-specific claims about the brand's own products (the brand knows its own product better than an audit)
- Hypotheticals or examples ("if a page gets 1,000 visits a day...")

## When most claims are fine

If the audit finds 0–1 stale claims, that's the result. Don't manufacture replacements. The update-draft skill simply applies fewer edits.
