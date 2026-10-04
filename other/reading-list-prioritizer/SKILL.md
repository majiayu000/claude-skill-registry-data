---
name: reading-list-prioritizer
description: "Prioritize and group your reading list from a local md-file by topic and relevance to your role. Use when you have too many saved articles and need a weekly reading plan. Triggers: 'prioritize my reading list', 'what should I read first', 'расставь приоритеты в списке чтения', 'что мне читать первым'."
version: 1.0.0
---

# Reading List Prioritizer

This skill takes your personal reading list (a local markdown file with article titles and/or URLs) and returns a structured weekly reading plan: items scored by relevance to your role, grouped by topic, with a "Read this week" shortlist at the top.

**Input:**
- A markdown file (.md) with your reading list — one item per line, as `[Title](URL)` links, bare URLs, or plain text titles
- Your role or current focus area (stated in 1–2 sentences in your message)

**Output:**
- Markdown response with a prioritized "Read this week" shortlist + full list grouped by topic, each item labeled [High] / [Med] / [Low]

---

## Language Detection

Detect the user's language from their message:
- If Russian (or contains Cyrillic): respond in Russian
- If English (or other Latin-script language): respond in English
- If ambiguous: respond in the language of the trigger phrase used

---

## Instructions

### Step 1: Validate Input

1. Check that a reading list file has been provided (uploaded or pasted)
   - If no file and no pasted list: stop and return: "Please provide your reading list as a .md file or paste the list directly."
   - Accepted formats: `.md` file, pasted markdown list, plain text list

2. Check that the user's role or focus area is stated in their message
   - If missing: ask for it before proceeding — "What's your current role or focus area? (e.g., 'PM focused on AI product strategy')"
   - Do not guess or assume a generic role — prioritization depends on it

3. Validate file content: must contain at least 3 parseable items
   - If fewer than 3 items: proceed but note "Short list — showing all items with priority labels"
   - If file is empty or contains no recognizable items: stop with message "The reading list appears empty. Please check the file format."

### Step 2: Parse the Reading List

1. Read each line of the list and extract:
   - **Title**: from `[Title](URL)` format, or plain text line, or domain-derived label if only a bare URL
   - **URL/domain**: extract domain from URL if present (e.g., `nngroup.com`, `hbr.org`, `stratechery.com`)
   - **Tags or notes**: if the user appended a tag or comment after the link (e.g., `[Article](url) #ux`), extract them

2. Build a working list of items: `[title, domain, tags]` per item

3. Silently remove exact duplicate URLs; note count at the bottom of output if any found

### Step 3: Detect Topics

1. Analyze all item titles and domains together to identify 2–7 topic clusters
   - Use title keywords and known domain signals:
     - `nngroup.com`, `smashingmagazine.com` → UX/Design
     - `hbr.org`, `mckinsey.com` → Leadership/Strategy
     - `stratechery.com`, `ben-evans.com` → Business/Tech Strategy
     - `towardsdatascience.com`, `arxiv.org` → AI/Data
     - `substack.com`, newsletters → Industry News
   - For unknown domains: use title keywords to assign topic
   - Items that don't fit any cluster: assign to "General"

2. Aim for 2–7 distinct groups; if all items cluster into one topic, add subtopic labels where possible

**Edge Cases:**
- All items from a single domain: group by subtopic using title keywords; note "All items from one source — grouped by subtopic"
- Items in mixed languages (EN + RU titles): process both; group by topic regardless of language
- Items with only bare URLs and no titles (domain cannot be identified or title keywords unavailable): assign to "General"; add note at top of Full List section: "Note: grouping is approximate — limited metadata available for these items"

### Step 4: Score Relevance

1. For each item, score relevance to the user's stated role/focus area:
   - **[High]**: Directly relevant — topic matches role or stated focus area, or title addresses a specific problem the user likely faces
   - **[Med]**: Broadly relevant — adjacent topic, useful background, or industry-relevant but not core to stated focus
   - **[Low]**: Low relevance — interesting but tangential to stated role and focus area

2. Apply scoring across all items before ranking

3. Within each topic group, sort: High → Med → Low

### Step 5: Build "Read This Week" Shortlist

1. Select top 5–7 items overall:
   - Prefer [High] items from the widest topic variety (1–2 per topic max in shortlist)
   - If fewer than 5 [High] items exist, include top [Med] items

2. For each shortlisted item, add a 1-sentence relevance note explaining why it's recommended

3. Cap at 7 items regardless of list size

**Edge Cases:**
- Very long list (50+ items): process all; limit shortlist to 7; add note "Remaining X items are in the full grouped list"

### Step 6: Format and Output

1. Build the output markdown (see Output Format below)
2. Include all items from input in the full grouped list — no items silently dropped
3. Add footer with count of duplicates removed (if any)

---

## Negative Cases

- **Empty file:** Return "The reading list file appears empty or has no recognizable items. Paste your list directly or check the file format."
- **Non-md / unreadable file:** Return "Expected a markdown (.md) file with a list of articles or links. Please convert your list to markdown format."
- **No role/focus provided:** Ask once before proceeding — do not produce output without it (prioritization would be meaningless without context)
- **All items unresolvable (no titles, no domains, no text):** Return "Could not parse any items from the list. Check that each line contains a title or URL."

---

## Output Format

```
## Reading Plan — [YYYY-MM-DD]
**Focus area:** [user-stated role and focus]
**Total items:** X | **Duplicates removed:** Y (or omit if 0)

---

### Read This Week (Top 5–7)
1. [Title](URL) — [Topic] · [1-sentence relevance note]
2. [Title](URL) — [Topic] · [1-sentence relevance note]
...

---

### Full List by Topic

#### [Topic 1 name]
- [High] [Title](URL)
- [Med] [Title](URL)
- [Low] [Title](URL)

#### [Topic 2 name]
- [High] [Title](URL)
...

---

### Skippable This Week
- [Low] [Title](URL) — low relevance to stated focus
...
```

**Field rules:**
- "Read This Week" items: include relevance note (why recommended for this role)
- Priority labels: always present, always one of [High] / [Med] / [Low]
- "Skippable This Week": list only [Low] items; include a brief reason if non-obvious
- If all items are [High] relevance: omit "Skippable This Week" section
- Bare URLs without titles: display as domain name (e.g., `stratechery.com — [article path]`)
