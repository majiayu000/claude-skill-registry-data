---
name: design-search-ux
description: Use when designing a search feature for a website or application — to structure the input, autocomplete, results list, and zero/no-results states so users find what they need with minimal friction.
source: NNG "Search UX" (Pernice, 2020); Morville & Callender "Search Patterns" (O'Reilly, 2010); Baymard Institute "On-site Search UX" (2021, 70-guideline study across 60 major sites)
tags: [search, search-ux, autocomplete, search-results, information-retrieval, zero-results, filters, ux-patterns]
---

# Design Search UX

Place search in the expected location, expose the input field (not just an icon), support autocomplete for large corpora, and design no-results states that recover users rather than abandoning them.

## Why This Is Best Practice

**Adopted by:** Baymard Institute's "On-site Search UX" (2021) is the most comprehensive empirical study — 70 guidelines tested across 60 major e-commerce sites; NNG's "Search UX" research (Pernice, 2020) covers placement, input design, and results across enterprise and consumer products; Google, Amazon, and Spotify have published case studies on search autocomplete and result quality improvements; Elasticsearch and Algolia both document UX patterns in their implementation guides
**Impact:** Baymard Institute: 68% of major e-commerce sites fail basic on-site search UX — the majority of search UX problems are in placement, autocomplete, and no-results design, not result ranking; NNG: users who successfully use site search convert at 1.8× the rate of non-searchers (Chase 2016); Etsy's search UX redesign (2019) — fixing autocomplete and result highlighting — increased search conversion by 6%; Spotify's search interface redesign (2018) increased search session completion by 34%
**Why best:** Search is the highest-intent interaction on a website — a user who types a query is expressing an explicit need; the design of the search UI determines whether that intent is fulfilled or abandoned; poor search design (hidden input, no autocomplete, empty no-results page) wastes the highest-value user action

Sources: Baymard Institute "On-site Search" (2021); NNG "Search UX Strategies" (Pernice, 2020); Morville & Callender "Search Patterns" (O'Reilly, 2010); Nielsen "10 Usability Heuristics" (1994) — Heuristic 1: Visibility of system status

## Steps

### 1. Place search where users expect it

Search placement is convention-driven — deviating from conventions requires measurable justification:

**Desktop:**
- Top-right or top-center: expected by 91% of users (NNG)
- Always visible on pages where search is a primary mode of navigation (e-commerce, documentation, news)
- Below-the-fold placement: never — search is a primary navigation element, not secondary content

**Mobile:**
- Top bar with search icon (tapping expands to full-width input)
- Bottom bar search tab (if search is a primary navigation destination, not just a utility)
- Full-screen search overlay on activation for complex search (autocomplete + filters)

**Input field vs icon only:**

```
❌ Icon only (desktop):
   [search icon] — requires a click to reveal the input field; hides a primary affordance

✅ Visible input field (desktop):
   [🔍 Search products...              ] — input always visible; no extra click required

✅ Icon with expand (mobile):
   [🔍] — tapping expands to full-width input; acceptable on mobile where space is limited
```

Baymard: icon-only search on desktop increases search abandonment by 22% — the extra click interrupts intent. Expose the input field on desktop.

### 2. Size the input field appropriately

The input field width should accommodate the expected query length:

```
Recommended minimum width:
   27 characters (fits "running shoes for women size 10")
   Narrower fields cause users to shorten their queries to fit the visual box

Recommended default for desktop: 300–400px (≈ 30–40 characters)
Expand on focus if space-constrained — input grows to 400px when user clicks

Placeholder text:
   ✅ Shows what can be searched: "Search products, brands, or categories"
   ❌ Generic: "Search"  (adds no information)
   ❌ Misleading: "What are you looking for?" (conversational UX pattern — only if the UI supports it)
```

### 3. Implement autocomplete for corpora > 200 items

Autocomplete (type-ahead suggestions) reduces search time and corrects spelling:

**When to use autocomplete:**
- Corpora > 200 items: autocomplete helps users discover vocabulary and correct spelling
- Corpora < 50 items: autocomplete is overhead — users can scan results; use instant search instead
- Always for e-commerce product catalogs, documentation with > 50 articles, content libraries

**Autocomplete design rules:**
```
Show: 5–8 suggestions (more creates scroll; fewer may miss the right match)
Highlight: bold the portion of each suggestion that matches the query
Group: if suggestions span types (products, categories, articles), use headers
Trigger: after 2+ characters (1 character is too broad; shows irrelevant suggestions)
Debounce: 150–250ms (prevents API call on every keystroke)

❌ Autocomplete without highlighting: "Running Shoes for Women" — which part matched?
✅ Autocomplete with matching bolded: "**Running** Shoes for Women" — query was "running"
```

**Recent searches:** Show the last 3–5 searches when the input is focused (before typing). Users frequently repeat searches. Label the section "Recent searches" — not the same list as autocomplete suggestions.

### 4. Design the results page

Results must communicate what was found, how many, and allow refinement:

**Result count:**
```
✅ "1,240 results for 'running shoes'"
✅ "Showing 1–20 of 1,240 results"
❌ No count → user doesn't know if the search worked or returned nothing
```

**Query term highlighting:**
Highlight the query term within each result:
```
Search: "machine learning"
Result: "An introduction to **machine learning** algorithms and supervised classification"
```

Highlighting helps users confirm the result is relevant before clicking.

**Sorting and filtering:**
- Show sort options above results (Relevance, Newest, Price, Rating)
- For > 500 items: provide faceted filters (category, price range, rating, date)
- Mobile: filters behind a "Filter" button that opens a bottom sheet — do not show filters inline on mobile (they consume the viewport)
- Show active filters as removable chips/tags above results so users can see and clear them

**Result layout:**
- List view: better for dense data, text-heavy results, comparison
- Grid view: better for visual products, images, media
- Provide a toggle for user preference when both are reasonable

### 5. Design the no-results state

A blank screen on no results is an abandonment trigger. The no-results state must:

1. **Confirm what was searched:** "No results for 'red running shoez'"
2. **Suggest a recovery action:**
   - Typo? Show "Did you mean: red running shoes?"
   - Too specific? Show "Try a broader search"
   - Show related items or popular searches in the same category
3. **Provide an escape hatch:** Link to browse by category, or to a contact/support page

```
Example no-results layout:

We couldn't find anything for "red running shoez"

Did you mean: red running shoes?

Or try:
  • Browse all Running Shoes →
  • View new arrivals →
  • Contact support
```

**What never to show on no-results:**
- Blank white screen
- Only "No results found" with no recovery options
- Random unrelated items ("You might also like…" with zero connection to the query)

### 6. Support typo tolerance and query expansion

Most users cannot spell product or technical terminology correctly. Search must compensate:

- **Fuzzy matching:** tolerate 1–2 character transpositions or omissions (Levenshtein distance ≤ 2 for queries > 5 characters)
- **Stemming:** "running" matches "run", "runs", "runner"
- **Synonyms:** "laptop" matches "notebook", "MacBook"; "sofa" matches "couch", "settee"
- **Phonetic matching:** "Nikon" matches "Nikkon", "Nicon"

If building on Elasticsearch, Algolia, or Typesense: all support these features in configuration — enable them. Do not require exact-match search as the default.

### 7. Scope search to context when appropriate

For large applications with distinct content types, provide scoped search:

```
[🔍 Search...          ] [▼ All] ← scope selector

Scopes: All | Products | Articles | Help | Orders
```

Scoped search reduces noise when users know which type of content they're searching for. Default scope to "All" — do not default to a narrow scope that hides content.

**When scoping is NOT needed:** applications with a single content type (e-commerce with only products; a blog with only articles); adding scope selector adds UI complexity without benefit.

## Rules

- Expose the input field on desktop — icon-only search adds an extra click that reduces search activation
- Show result count — users need to know if the search worked before evaluating results
- Always highlight the query term within results — confirms relevance before clicking
- Never show a blank no-results page — provide typo correction, recovery suggestions, and a browse escape
- Autocomplete after 2+ characters with matching term bolded — no earlier, no later
- Enable typo tolerance in the search engine — do not require exact-match search as default

## Common Mistakes

- **Icon-only search on desktop**: saves 30px of horizontal space; costs 22% search activation — not a good trade
- **No result count**: users submit a search, see results, don't know if there are 5 or 5,000; this changes whether they use filters or refine the query
- **Autocomplete without bolding the match**: user types "mach" and sees "Machine Learning, Machine Design, Machine Tools" — which part matched? Bolding makes it instantly clear
- **"No results" blank page**: user's highest-intent moment ends with a dead end; recovery suggestions and related content reduce abandonment
- **Exact-match only**: most users misspell queries; exact-match search without fuzzy matching returns no results for common misspellings, leaving users to conclude the content doesn't exist

## When NOT to Use

- Applications with fewer than 50 items total — for small corpora, a filtered list or tag-based navigation is faster than a search box; search implies a large corpus, and showing one when items are few creates a mismatch expectation
- Real-time communication tools (chat, messaging) where search is for finding messages by date or sender — search within a conversation thread follows different patterns (chronological, speaker-filtered) than content search

