---
name: sosl-with-clauses
description: "Use when adding result-scoping or result-shaping WITH clauses to a SOSL FIND query — WITH DivisionFilter, WITH DATA CATEGORY, WITH SNIPPET, WITH NETWORK, WITH PricebookId, WITH METADATA, WITH HIGHLIGHT, and WITH SPELL_CORRECTION — including their fixed clause order, supported objects, field-type limits, and API-version floors. Triggers: SOSL snippet, highlight search terms, filter by data category, community/network scoping, spell correction, pricebook filter, division filter. NOT for base FIND/IN/RETURNING mechanics, SOSL-vs-SOQL choice, or injection-safe dynamic search (use data/sosl-search-patterns); NOT for SOSL result-count limits (use data/sosl-search-result-limits)."
category: data
salesforce-version: "Spring '25+"
well-architected-pillars:
  - Performance
  - Security
triggers:
  - "add a snippet excerpt to my SOSL knowledge search results"
  - "highlight the matching search terms in a SOSL query"
  - "filter a SOSL knowledge article search by data category"
  - "scope a SOSL search to one Experience Cloud site"
  - "turn off spell correction in a SOSL FIND query"
tags:
  - sosl-with-clauses
  - sosl
  - with-snippet
  - with-highlight
  - with-data-category
  - with-network
  - spell-correction
inputs:
  - "The SOSL FIND query (static or dynamic Search.query) you want to scope or shape"
  - "The target objects/entities and which channel or surface consumes the results"
  - "The API version the query runs under"
outputs:
  - "A correctly ordered SOSL FIND query with the required WITH clauses"
  - "Review findings on clause order, supported objects, field-type limits, and API-version floors"
dependencies: []
version: 1.0.0
author: Pranav Nagrecha
updated: 2026-07-08
---

# SOSL WITH Clauses

This skill activates when a practitioner is composing or reviewing a SOSL `FIND` query and needs one of the optional `WITH` clauses that either **scope** which records match (`DivisionFilter`, `DATA CATEGORY`, `NETWORK`, `PricebookId`) or **shape** how matches come back (`SNIPPET`, `HIGHLIGHT`, `METADATA`, `SPELL_CORRECTION`). The clauses are standard, released SOSL syntax documented in the SOQL and SOSL Reference — the docs do not stamp them with a GA/Beta/Pilot label, so treat them as core syntax and do not assert a maturity level the docs don't state.

---

## Before Starting

Gather this context before working on a SOSL WITH clause:

- **Know your target objects.** Every WITH clause is gated to specific entities. `SNIPPET`, `HIGHLIGHT`, and `DATA CATEGORY` do nothing on objects they don't support, and there is no error — the clause is just ignored. Confirm the object list (see the clause table) before promising the feature will work.
- **Know your API version.** `DATA CATEGORY` needs 18.0+, `SNIPPET` needs 32.0+, `HIGHLIGHT` needs 39.0+ (40.0+ for custom fields/objects), and `SPELL_CORRECTION` needs 40.0+. A query running below the floor silently loses the clause. Check the `apiVersion` of the class, LWC, or REST call that issues the search.
- **The most common wrong assumption:** that WITH clauses can appear in any order, like SOQL `WHERE`/`ORDER BY`. They can't — SOSL enforces a **single fixed order** and rejects the query otherwise. See Core Concepts.
- **Wildcards suppress shaping.** If the `FIND` term contains `*` or `?`, `SNIPPET` excerpts and `HIGHLIGHT` markup are not generated. Decide up front whether the search needs wildcards or presentation, because you often can't have both.

---

## Core Concepts

### Scoping clauses vs shaping clauses

The eight WITH clauses fall into two jobs:

- **Result-scoping** — narrows *which* records are returned before they reach you: `WITH DivisionFilter` (Division field), `WITH DATA CATEGORY` (Knowledge/Question categories), `WITH NETWORK` (Experience Cloud site), `WITH PricebookId` (a single price book for `Product2`).
- **Result-shaping** — changes *how* the matches are represented: `WITH SNIPPET` (contextual excerpt text), `WITH HIGHLIGHT` (`<mark>`-delimited matched terms), `WITH METADATA` (label metadata in the response), and `WITH SPELL_CORRECTION` (whether a mis-typed term is auto-corrected before matching — it straddles both jobs).

### The clause order is fixed

After the required `FIND ... RETURNING ...`, WITH clauses must appear in exactly this order, then `LIMIT`, then `UPDATE`:

```
FIND {term} [IN SearchGroup] RETURNING FieldSpec
  WITH DivisionFilter
  WITH DATA CATEGORY DataCategorySpec
  WITH SNIPPET (target_length=n)
  WITH NETWORK NetworkIdSpec
  WITH PricebookId
  WITH METADATA
  WITH HIGHLIGHT
  WITH SPELL_CORRECTION = true|false
  LIMIT n
  UPDATE TRACKING, VIEWSTAT
```

You include only the clauses you need, but the ones you include must stay in this relative sequence. `OFFSET` and per-object `WHERE` live **inside** the `RETURNING` field spec, not among the WITH clauses.

### Each clause is object- and version-gated

| WITH clause | Job | Applies to | API floor | Key limit |
|---|---|---|---|---|
| `DivisionFilter` | scope | Orgs using the Divisions feature | — | Accepts a division name or ID; pre-filters all results by the Division field |
| `DATA CATEGORY` | scope | `KnowledgeArticleVersion` / `__kav` types, `Question` | 18.0 | Requires `RETURNING` + a `WHERE PublishStatus=...`; operators `AT` / `ABOVE` / `BELOW` / `ABOVE_OR_BELOW`; multiple specs combine with `AND` only |
| `SNIPPET (target_length=n)` | shape | `Case`, `CaseComment`, `FeedItem`, `FeedComment`, `Idea`, `IdeaComment`, `KnowledgeArticleVersion` | 32.0 | `n` = 50–1,000 (default 300); no snippet with wildcards; only when ≤20 results per page |
| `NETWORK NetworkIdSpec` | scope | Experience Cloud `User` and feeds (`FeedItem`/`FeedComment`) | — | `WITH NETWORK = 'id'` or `IN ('id1','id2')`; `'000...0'` for internal; can't mix scoped and unscoped in one query |
| `PricebookId` | scope | `Product2` only | — | Filters product results to one price book |
| `METADATA` | shape | Search response envelope | — | No metadata (e.g. labels) returned unless the clause is present |
| `HIGHLIGHT` | shape | auto number, email, text, text area, long text area fields | 39.0 (40.0 for custom) | Max 25 records highlighted per entity per query; `<mark>` delimiters; no highlight with wildcards |
| `SPELL_CORRECTION = true\|false` | shape | Searches that support spell correction | 40.0 | Defaults to `true`; only affects supported searches |

---

## Common Patterns

### Knowledge search UI (DATA CATEGORY + SNIPPET + HIGHLIGHT)

**When to use:** a support console or Experience Cloud help center that searches published Knowledge articles, shows a short contextual excerpt, and bolds the matched terms.

**How it works:** `RETURNING KnowledgeArticleVersion (Id, Title, ... WHERE PublishStatus='online' AND Language='en_US')`, then `WITH DATA CATEGORY` to constrain to a category branch, then `WITH SNIPPET (target_length=n)` for the excerpt, then `WITH HIGHLIGHT` for the `<mark>` markup. Keep them in that order.

**Why not the alternative:** building excerpts and highlight markup in Apex after a plain SOSL means re-implementing the search engine's tokenizer and relevance — the platform already computes the best-matching passage.

### Experience Cloud site-scoped search (NETWORK)

**When to use:** a community/site search that must return only users and feed posts belonging to one Experience Cloud site, not the whole org.

**How it works:** `WITH NETWORK = 'siteNetworkId'` (or `IN (...)` for several sites). It scopes `User` and feed results; for other objects the filter is ignored and results span all sites plus internal data.

**Why not the alternative:** filtering feed results in Apex after an unscoped SOSL leaks cross-site content into memory and risks showing one site's posts in another. Let SOSL scope at the source — and never mix a scoped and an unscoped search in the same statement.

### Product search within a price book (PricebookId)

**When to use:** a product-lookup that should only surface products present on a specific price book.

**How it works:** `FIND {term} RETURNING Product2 (Id, Name) WITH PricebookId`. It restricts the `Product2` matches to that price book.

---

## Decision Guidance

| Situation | Recommended clause | Reason |
|---|---|---|
| Show an excerpt of the matched text | `WITH SNIPPET (target_length=n)` | Platform-computed contextual passage; 50–1,000 chars |
| Bold/emphasize the matched terms | `WITH HIGHLIGHT` | Returns `<mark>`-wrapped terms on supported field types |
| Restrict Knowledge/Question by category tree | `WITH DATA CATEGORY ... AT/ABOVE/BELOW` | The only category filter for search; needs `WHERE PublishStatus` |
| Limit results to one Experience Cloud site | `WITH NETWORK` | Scopes `User` and feed results to that site |
| Limit product hits to one price book | `WITH PricebookId` | `Product2`-only price-book scope |
| User keeps mistyping the term | leave `SPELL_CORRECTION` default (`true`) | Auto-correction is on unless you disable it |
| You need exact-match, no auto-correct | `WITH SPELL_CORRECTION = false` | Turns off correction for supported searches |
| Term contains `*`/`?` wildcard | do **not** rely on `SNIPPET`/`HIGHLIGHT` | Neither is generated for wildcard terms |

---

## Recommended Workflow

1. **Classify the need** — is it scoping (which records) or shaping (how they look)? Pick the specific clause(s) from the table; a Knowledge search often needs three.
2. **Verify object + field-type support** — confirm each chosen clause actually applies to the objects and (for `HIGHLIGHT`) the field types in your `RETURNING` list; drop clauses the objects don't support.
3. **Check the API-version floor** — confirm the issuing class/LWC/REST call runs at or above each clause's minimum (18.0 / 32.0 / 39.0 / 40.0); bump the `apiVersion` if needed.
4. **Assemble in the fixed order** — write the clauses in canonical sequence (DivisionFilter → DATA CATEGORY → SNIPPET → NETWORK → PricebookId → METADATA → HIGHLIGHT → SPELL_CORRECTION), with `RETURNING`-internal `WHERE`/`OFFSET` in place and `LIMIT` after the WITH block.
5. **Validate wildcard and required-clause rules** — if the term has `*`/`?`, don't expect snippet/highlight output; if using `DATA CATEGORY`, ensure `RETURNING` + `WHERE PublishStatus` are present. Run `scripts/check_sosl_with_clauses.py` against the query.
6. **Test on real data** — snippets only appear at ≤20 results per page and highlighting caps at 25 records per entity; run the query and confirm the shaping actually renders before wiring the UI.

---

## Review Checklist

Run through these before marking a SOSL WITH-clause query complete:

- [ ] WITH clauses appear in the fixed canonical order; `LIMIT`/`UPDATE` follow them
- [ ] Every clause's target objects support it (no `SNIPPET`/`HIGHLIGHT`/`DATA CATEGORY` on unsupported entities)
- [ ] The issuing context's API version meets each clause's floor (18.0 / 32.0 / 39.0 / 40.0)
- [ ] `SNIPPET` `target_length` is within 50–1,000; a bad value silently falls back to 300
- [ ] `HIGHLIGHT` fields are auto number / email / text / text area / long text area only
- [ ] `DATA CATEGORY` query includes `RETURNING` and `WHERE PublishStatus=...`; multiple specs joined with `AND` only
- [ ] `NETWORK` query does not mix scoped and unscoped searches; non-user/feed objects aren't assumed to be filtered
- [ ] Wildcard terms don't rely on `SNIPPET`/`HIGHLIGHT` output

---

## Salesforce-Specific Gotchas

Non-obvious platform behaviors that cause real production problems:

1. **Clause order is enforced** — SOSL rejects WITH clauses that appear out of the fixed sequence, even though each clause is individually valid. This surprises anyone used to reordering SOQL clauses freely.
2. **Snippets and highlights vanish with wildcards** — add a `*` to the `FIND` term and the excerpt/`<mark>` markup silently disappears; the query still runs and returns rows, just without shaping.
3. **`NETWORK` only scopes users and feeds** — for any other object, the site filter is ignored and results span all sites plus internal data, which can leak cross-site content if you assumed it filtered everything.

---

## Output Artifacts

| Artifact | Description |
|---|---|
| Ordered SOSL `FIND` query | A `FIND ... RETURNING ...` statement with WITH clauses in canonical order |
| `scripts/check_sosl_with_clauses.py` output | Lint findings on clause order, `SNIPPET` range, `SPELL_CORRECTION` value, and wildcard/required-clause rules |
| `templates/sosl-with-clauses-template.md` | A fill-in worksheet + ordered clause skeleton to assemble the query |

---

## Related Skills

- `data/sosl-search-patterns` — base SOSL mechanics: SOSL-vs-SOQL choice, `FIND`/`IN`/`RETURNING`, search groups, and injection-safe `Search.query`. Start there for the query itself; use *this* skill for the WITH clauses layered on top.
- `data/sosl-search-result-limits` — how many rows SOSL returns per object and overall; pair with `LIMIT` when your WITH-clause query returns too much.
- `data/knowledge-article-import` — populating the `KnowledgeArticleVersion` and data-category structures that `WITH DATA CATEGORY` filters against.
