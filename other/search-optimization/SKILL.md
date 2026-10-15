---
name: search-optimization
description: Improve a site's own search box - relevance, aliases and synonyms, typo tolerance, partial matching, ranking and empty states - and prove it with a table of real queries and the results they must return. Use when people search a component library, docs or catalogue and don't find what is there.
---

# /search-optimization

Good site search is predictable: the obvious query finds the obvious thing first. Every change here is checked against a query table, so improving one search can't silently break another.

## 1. Build the query table first

Write 30–60 queries real people would type, each with the results that **must** appear in the top 5. Cover:

- **Exact names:** "silk field".
- **What it is, not what it's called:** "animated button", "glass button", "background", "card", "chart".
- **Jargon and short forms:** "cta", "auth", "login", "sign in", "ai", "llm", "nav", "modal", "toast".
- **Plurals and capitals:** "Buttons", "PRICING".
- **One typo:** "backgorund", "pricng".
- **Two-word intents:** "pricing toggle", "dark mode switch".
- **Nonsense:** "zzzz", which must show a helpful empty state, not an error.

Run it as a script against the real search function and print pass/fail per row. This is the test suite.

## 2. Know what each item is indexed by

Search can only find what its metadata says. For every item check that it has:

- a name;
- a category with a human label;
- 4–8 tags that use the words people search with ("glass", "cta", "login"), not internal ones;
- a description that says what it is in plain words.

Missing or inconsistent tags are the most common cause of "search can't find it". Fix the data before the algorithm.

## 3. Synonyms, explicitly

Keep a small, reviewed synonym map from what people type to the vocabulary of your data:

- cta → call to action / ctas
- login, signin → auth / sign in
- chart, graph → analytics / stats
- llm, chat → ai
- menu → navbar / navigation
- modal → dialog / overlay

Expand each query term to *term OR its synonyms*. Score synonym hits slightly below exact hits, so "login" still ranks a component literally named "login" first. Never generate synonyms automatically; every entry is a decision.

## 4. Matching and ranking

- **Tokenise** lowercase on non-alphanumerics, and fold plurals (strip a trailing "s"/"es" when the stem matches).
- **Field weights:** name > tags = category > description. Multi-word queries are AND, with each term matching some field.
- **Partial matching:** prefix matches on any word; substring only for terms of 4 or more characters.
- **Typos:** allow 1 edit for terms of 5 or more characters, scored lowest.
- **Ties** fall back to the curated order, so results don't shuffle between renders.

## 5. The interface

- Results update as you type (debounce ≤ 150ms), and the query lives in the URL (`?q=`) so it can be shared and survives reload. Search-result URLs canonicalise to the unfiltered page.
- **Keyboard:** a shortcut opens search, ↑/↓ move, Enter opens, Escape closes or clears.
- **Empty state:** say what was searched, suggest the nearest categories or a correction, and offer to clear.
- Show the result count, and announce it politely to screen readers.

## Output

The query table before and after, with every row passing, plus the list of metadata fixes and synonym entries added.
