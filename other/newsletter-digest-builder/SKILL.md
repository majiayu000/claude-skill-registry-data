---
name: newsletter-digest-builder
description: "Build a structured weekly digest from a folder of saved articles and newsletters. Prioritizes by role (PM, marketer, or custom). Triggers: 'build newsletter digest', 'newsletter digest', 'summarize my saved articles', 'I have too many newsletters to read', 'собери дайджест из рассылок', 'дайджест из статей', 'сделай еженедельный дайджест', 'у меня накопилось много статей'."
version: 1.0.0
---

# Newsletter Digest Builder

This skill takes a folder of saved articles and newsletters (.txt or .md files) and returns a structured weekly digest: articles scored by relevance to your role, grouped by topic, with a "Read This Week" shortlist at the top.

**Input:**
- A folder path (or list of files) containing .txt/.md articles — one article per file
- Your role or current focus area (stated in 1–2 sentences in your message)

**Output:**
- Markdown digest with a "Read This Week" shortlist (5–7 items), full list grouped by topic, and a "Can Skip This Week" section

---

## Language Detection

Detect the user's language from their message:
- If Russian (or contains Cyrillic): respond in Russian
- If English (or other Latin-script language): respond in English
- If ambiguous: respond in the language of the trigger phrase used

---

## Instructions

### Step 1: Validate Input

1. Check that files have been provided (folder path, uploaded files, or pasted list)
   - If no files provided: stop and return — "Please provide a folder path or upload your saved article files (.txt or .md). I need at least 1 article to build a digest."
   - Accepted formats: .txt files, .md files, pasted markdown list

2. Check that the user's role or focus area is stated in their message
   - If missing: ask once before proceeding — "What's your current role or focus area? (e.g., 'PM focused on AI product launches' or 'Marketer working on B2B demand generation')"
   - Do not guess or assign a generic role — prioritization depends on it

3. Validate files: skip empty or unreadable files; note count at end of output
   - If all files are empty or unreadable: stop with — "No readable article files found. Check that files contain article text."

### Step 2: Extract Articles

1. For each file, extract:
   - **Title**: first H1 heading, first bold line, or filename (as fallback)
   - **Source domain**: from URLs in the file if present (e.g., `hbr.org`, `lenny.substack.com`)
   - **Body text**: first 200–300 words for topic detection and relevance scoring

2. Build a working list: `[title, source, body_excerpt]` per article

3. Skip binary, code, or non-article files silently; note count at end if any skipped

**Edge Cases:**
- Files contain only a URL with no body text: extract domain and URL path as title; flag in output "digest based on URL metadata only"
- Very large folder (50+ files): process all; cap shortlist at 7; note total count
- Files in mixed languages (EN + RU): process both; group by topic regardless of language; respond in user's message language

### Step 3: Detect Topics

1. Analyze all article titles and body excerpts to identify 3–6 topic clusters
   - Use title keywords and source domain signals:
     - `hbr.org`, `mckinsey.com` → Leadership/Strategy
     - `lenny.substack.com`, `svpg.com` → Product Management
     - `nngroup.com`, `smashingmagazine.com` → UX/Design
     - `techcrunch.com`, `theverge.com`, `wired.com` → Tech/Industry News
     - `towardsdatascience.com`, `arxiv.org` → AI/Data
     - Marketing/growth newsletters → Growth/Marketing
   - For unknown sources: use title keywords to assign topic
   - Articles that don't fit any cluster: assign to "General"

2. Aim for 3–6 distinct groups; if folder is small (< 6 files), use 2–3 groups

**Edge Cases:**
- All articles from a single domain: group by subtopic using title keywords; note "All items from one source — grouped by subtopic"
- Only 1–2 articles total: skip topic grouping; output flat list with labels; note "Too few files for grouping"

### Step 4: Score Relevance by Role

1. For each article, score relevance to the user's stated role and focus area:
   - **[Must Read]**: Directly relevant — topic matches stated role/focus, or title addresses a specific problem the user likely faces
   - **[Useful]**: Broadly relevant — adjacent topic, useful background, or industry context
   - **[Optional]**: Low relevance — interesting but tangential to stated role and focus

2. Apply scoring across all articles before ranking

3. Role-specific scoring signals (examples):
   - **PM / Product Manager**: prioritize product strategy, user research, metrics, AI product, B2B SaaS topics
   - **Marketer / Marketing**: prioritize growth, SEO, content strategy, demand gen, social, copywriting topics
   - **Custom role**: score based on keywords in the stated description

4. Within each topic group, sort: Must Read → Useful → Optional

### Step 5: Build "Read This Week" Shortlist

**Exception — 1–2 articles total:** Skip the "Read This Week" shortlist heading entirely. Output a flat list of all articles with relevance labels only. Add note: "Too few files for grouping — showing all items." Go directly to Step 6 with flat-list format (omit shortlist and topic group sections).

1. Select top 5–7 articles overall:
   - Prefer [Must Read] items from the widest topic variety (max 2 per topic in shortlist)
   - If fewer than 5 [Must Read] items: include top [Useful] items

2. For each shortlisted item, add a 1-sentence relevance note explaining why it's recommended for this role

3. Cap at 7 items regardless of folder size

### Step 6: Format and Output

1. Build the output markdown (see Output Format section below)
2. Include all articles from input in the full grouped list — no items silently dropped
3. Add footer with count of skipped files (if any)

---

## Negative Cases

- **No files provided**: Stop — "Please provide a folder path or upload your saved article files (.txt or .md)."
- **All files empty**: Stop — "No readable content found. Files appear empty or contain no article text."
- **Role not provided**: Ask once — do not produce output without it (prioritization is meaningless without role context)
- **Non-article files only (code, spreadsheets, binary)**: Stop — "No readable article files found. Expected .txt or .md files with article content."

---

## Output Format

```
## Weekly Digest — [YYYY-MM-DD]
**Role:** [user-stated role and focus]
**Articles processed:** X | **Skipped:** Y (omit if 0)

---

### Read This Week (Top 5–7)
1. **[Title]** — [Topic] · [1-sentence relevance note for this role]
2. **[Title]** — [Topic] · [1-sentence relevance note for this role]
...

---

### Full List by Topic

#### [Topic 1 name]
- [Must Read] **[Title]** — [source domain or filename]
- [Useful] **[Title]** — [source domain or filename]
- [Optional] **[Title]** — [source domain or filename]

#### [Topic 2 name]
...

---

### Can Skip This Week
- [Optional] **[Title]** — [brief reason: low relevance to stated focus]
...
```

**Field rules:**
- Relevance labels: always one of [Must Read] / [Useful] / [Optional]
- "Read This Week" items always include a 1-sentence relevance note
- "Can Skip This Week": only [Optional] items; include brief reason if non-obvious
- If all items are [Must Read]: omit "Can Skip This Week" section
- Filename used as title fallback when no title detected in file
