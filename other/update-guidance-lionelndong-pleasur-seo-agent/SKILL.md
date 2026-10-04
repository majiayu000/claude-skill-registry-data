---
name: update-guidance
description: Set update priorities for an article before running detailed audits. Reviews extracted content and proposes which update audits to focus on (claims-stale, product-features-missing, topic-gaps).
allowed-tools: Read, Write
---

# Update Guidance Skill

Not every article needs every audit. This skill reads the extracted article and decides which audits to prioritize before running them. Saves time on update-pipeline runs and avoids generating noise from low-value audits.

## Input

`/update-guidance <slug>`

Reads:
- `content-pipeline/updates/1-extracted/{slug}.md` (extracted article)
- `content-pipeline/0-context/{slug}.md` (if user provided context for the update)
- `brand-config.md` (current product list — used to spot what's missing)

## Process

1. **Read the extracted article.** Note publish date, last updated, claims count, products mentioned.
2. **Assess each potential audit:**

   **Claims audit** — high priority if:
   - Last updated > 18 months ago AND article has 3+ numerical claims
   - Article cites studies older than 3 years
   - Article makes specific traffic/percentage claims (these decay fast)

   **Product mentions audit** — high priority if:
   - Brand has products NOT mentioned in the article
   - Article was published before some products were launched
   - Brand product list in `brand-config.md` is significantly different from "Mentioned products" in the extract

   **Topic gaps audit** — high priority if:
   - Article is older than 12 months (SERP has likely shifted)
   - Article H2 count seems thin for the topic complexity
   - User context mentions wanting to compete with newer ranking pages

3. **Score each audit** as `high`, `medium`, `low`, or `skip`.
4. **Write the guidance file** to `content-pipeline/updates/0-guidance/{slug}.md` with the verdict line at the top so the orchestrator can parse it programmatically:

```markdown
# Update guidance: {slug}

## Verdict: PROCEED

(or `## Verdict: SKIP_ARTICLE` if all three audits scored skip — the orchestrator reads this single line to decide whether to dispatch update-draft or write a no-update-needed marker. Always present, always one of the two values.)

## Article context
- URL: {url}
- Last updated: {date}
- Word count: {n}
- Numerical claims: {n}
- Products mentioned: {list}

## Audit priorities

### Claims audit: {high/medium/low/skip}
**Reason:** {why}
**Focus areas:** {which specific claims to scrutinize first}

### Product mentions audit: {high/medium/low/skip}
**Reason:** {why}
**Specific products to consider adding:** {list from brand-config not in article}

### Topic gaps audit: {high/medium/low/skip}
**Reason:** {why}
**Worth re-pulling SERP:** {yes/no}

## Update angle (informed by user --context)

{1-2 sentences on the overall direction for the update — refresh stats? Add product walkthroughs? Compete with new SERP? Major restructure?}

## Recommended skip-list

Audits scored "skip" can be omitted from `/update-pipeline`. Skipping these saves time and reduces noise:
- {audit name} — {why skipping}
```

5. **Tell the user** the priority list and ask whether to proceed with `/update-pipeline` or run individual audits.

## Output

`content-pipeline/updates/0-guidance/{slug}.md`

The audit-priority plan. `/update-pipeline` reads this to decide which audits to run.

## Quality checklist

- [ ] Each of three audits has a priority + reason
- [ ] At least one audit is `high` priority (otherwise the article probably doesn't need an update)
- [ ] User-provided context is reflected in the angle
- [ ] Specific products / claims / sections are named, not generic recommendations

## When the article doesn't need an update

If all three audits score `skip` or `low`:
- State this clearly in the file
- Suggest the user reconsider whether the update is worth doing
- Don't fabricate priorities to justify a run
