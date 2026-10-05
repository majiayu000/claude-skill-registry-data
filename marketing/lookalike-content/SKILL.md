---
name: lookalike-content
description: "Analyse a data dump of posts to find patterns in what's working, create a winning content profile, then generate 10 content ideas that match those patterns using external research. Use this skill when the user wants to find content patterns, analyse what's working in their content, reverse-engineer successful posts, find lookalike content ideas, or generate ideas based on proven patterns. Also trigger when the user mentions 'what's working in my content', 'find patterns', 'lookalike content', 'content ideas based on what works', 'analyse my posts', or 'reverse engineer my best content'."
---

# Lookalike Content

## Overview

This skill takes a data dump of posts from any platform, analyses them for patterns in what makes the content successful, creates a winning content profile, then uses that profile to research and generate 10 content ideas that follow the same patterns.

One skill, one run, three phases:
1. **Analyse** — read the data dump, find patterns in structure, topics, hooks, emotional register, format
2. **Profile** — create a winning content DNA document
3. **Generate** — research trending topics and produce 10 ideas that match the winning patterns

## Prerequisites

### API Key

| Variable | Purpose |
|---|---|
| `TAVILY_API_KEY` | Researching trending topics for content idea generation |

## Context Loading — Mandatory

Before running, read these files:

1. `/brain/positioning-and-messaging.md` — brand voice, messaging, words we use/avoid
2. `/brain/truth.md` — verified product and company facts

## Workflow

### Step 1: Get the Data Dump

The user provides files containing their posts. These come in messy formats — the skill handles the conversion. Accepted formats:
- A folder of HTML files (e.g., Substack export)
- A CSV export (from analytics tools, newsletter platforms, etc.)
- A JSON archive (e.g., X data export)
- A markdown or text file with posts listed
- Multiple files uploaded at once
- Raw text pasted directly
- A path to files anywhere on disk

```
Upload your content data dump. This can be:
  - A folder of HTML files (Substack export)
  - A CSV export
  - A JSON archive (X data export)  
  - A markdown or text file
  - Multiple files
  - Or just paste the content directly

What platform is this content from?
  1. LinkedIn
  2. Substack / Newsletter
  3. X (Twitter)
  4. Blog
  5. Other

Pick a number:
```

### Step 2: Get Audience Context

Ask:

```
What space or industry should I research for content ideas?
(e.g., "B2B SaaS marketing", "AI for developers", "startup growth")
```

If the user says to use the defaults, use `/brain/positioning-and-messaging.md` to infer the space.

### Step 3: Convert to Clean Markdown

Before analysing anything, convert the messy uploaded data into a single clean `.md` file. This normalises all formats so the analysis phase always reads the same structure.

Save to: `marketing/plans/lookalike-analysis/[platform]_[YYYY-MM-DD].md`

**Conversion rules by format:**

**HTML files (e.g., Substack export):**
- Read each `.html` file
- Strip all HTML tags, keep the text content
- Extract the title from `<title>` or `<h1>` tags
- Extract the date from metadata, filename, or content if available
- Extract any visible engagement metrics from the page
- Convert each file into one post entry in the output

**CSV files:**
- Parse columns. Look for columns containing post text, date, and engagement metrics
- Column names vary — be flexible (e.g., "body", "content", "text" could all be post text; "likes", "reactions", "hearts" could all be engagement)
- Each row becomes one post entry

**JSON files (e.g., X data export):**
- Parse the JSON structure
- Find the array of posts/tweets
- Extract text, date, and engagement metrics per post

**Markdown or text files:**
- If already well-structured, use as-is
- If messy, split by logical dividers (headings, horizontal rules, clear breaks)

**Raw pasted text:**
- Wrap in the standard format below

**The output `.md` file must follow this exact structure:**

```markdown
# Content Data: [Platform]
## Posts: [N]
## Date range: [earliest] to [latest]
## Source: [Description of what was uploaded]
## Metrics available: [Yes/No]

---

## Post 1: [Title]
**Date:** [YYYY-MM-DD]
**Metrics:** [views: X, likes: X, comments: X — or "No metrics available"]

[Full post text, clean markdown, no HTML tags]

---

## Post 2: [Title]
**Date:** [YYYY-MM-DD]
**Metrics:** [if available]

[Full post text]

---

[...repeat for all posts]
```

**After conversion, tell the user:**

```
Converted [N] posts into a clean data file.

  Saved to: marketing/plans/lookalike-analysis/[platform]_[date].md
  Date range: [earliest] to [latest]
  Metrics found: [Yes — will rank by performance / No — will analyse all posts equally]

Want to review the file before I analyse, or proceed?
```

If the user wants to review, show them the first 2-3 posts so they can confirm nothing was lost.

---

## PHASE 1: Analyse

### Step 4: Analyse the Clean Data

Read the clean `.md` file from `marketing/plans/lookalike-analysis/`.

**If metrics exist:** Sort posts by the primary engagement metric (impressions for LinkedIn, views for Substack, views for X). Identify the top 30% as "top performers" and the bottom 30% as "low performers." The middle 40% is baseline.

**If no metrics exist:** Treat all posts equally — analyse the full set for recurring patterns without performance ranking.

**Topic patterns:**
- What subjects come up repeatedly?
- Group by theme (not exact keywords — "AI agents", "building AI agents", "AI agent implementation" are all one theme)
- Which themes dominate the top performers vs. low performers?

**Structural patterns:**
- Average post length (short <500 words, medium 500-1000, long 1000+)
- Do top posts use lists, numbered steps, or flowing prose?
- How many sections/subheadings do top posts have?
- Single-point posts vs. multi-point posts — which performs better?

**Hook patterns:**
- How do the top posts open? (bold claim, question, story, data point, scene, contrarian statement)
- What's the average hook length?
- Do hooks reference the reader directly ("you") or use third person?

**Emotional patterns:**
- What emotional register dominates? (frustration, aspiration, curiosity, fear, validation, urgency)
- Do top posts acknowledge pain before offering solutions?
- Positive framing vs. negative framing — which performs better?
- "Permission" messaging ("it's okay to...") vs. "push" messaging ("you need to...")

**Format patterns:**
- Narrative/story-driven vs. tactical/how-to vs. opinion/take vs. data-driven
- Do top posts include personal stories or examples?
- Do top posts include specific numbers, data points, or named examples?
- Do top posts include quotes from others?

**Close patterns:**
- How do top posts end? (CTA, question, bold statement, emotional beat, summary)
- What kind of CTA gets the most engagement in comments?

**Specificity level:**
- Are top posts broad industry takes or narrow tactical advice?
- Do they reference specific tools, companies, or people by name?

---

## PHASE 2: Profile

### Step 5: Create the Winning Content Profile

Synthesise the analysis into a structured profile document.

**Save to:** `marketing/plans/lookalike-analysis/winning-content-profile-[platform].md`

Read `references/winning-content-profile-template.md` for the exact output format.

The profile should contain:

1. **Overview** — one paragraph summary of what makes this content work
2. **Top-performing topic clusters** — ranked list of themes with evidence
3. **Structural DNA** — what the typical winning post looks like structurally
4. **Hook formula** — the opening patterns that work, with examples from the data
5. **Emotional playbook** — what emotional register resonates, with evidence
6. **Format that wins** — narrative vs. tactical vs. opinion vs. data
7. **Specificity calibration** — how specific or broad the content should be
8. **Close patterns** — how winning posts end
9. **What doesn't work** — patterns from low performers (if metrics exist) to avoid
10. **The winning formula** — a concise, testable summary: "The content that works for this audience is [format] about [topics], opening with [hook style], using [emotional register], at [length], with [specificity level]."

**Each finding must reference specific posts from the data as evidence.** Don't make generic claims — point to the actual content that supports the pattern.

After saving the profile, show the user a summary:

```
Winning Content Profile created.

Your winning formula:
[The one-paragraph summary from section 10]

Key findings:
  - Topic: [top theme]
  - Format: [winning format]
  - Hook: [winning hook style]
  - Emotion: [dominant register]
  - Length: [sweet spot]

Saved to: marketing/plans/lookalike-analysis/winning-content-profile-[platform].md

Now researching content ideas that match these patterns...
```

---

## PHASE 3: Generate

### Step 6: Research Trending Topics

Use Tavily to find trending topics in the user's space that could match the winning patterns.

**CRITICAL — use this exact script. Do NOT create new scripts:**

```bash
python .claude/skills/lookalike-content/scripts/tavily_research.py --query "What are the most discussed and trending topics in [space/industry] right now? Focus on topics that [audience] cares about. What questions are people asking? What debates are happening? What new developments are generating conversation? Include specific examples and sources."
```

Run a second query focused on the winning topic clusters:

```bash
python .claude/skills/lookalike-content/scripts/tavily_research.py --query "What's new and being discussed about [top winning topic cluster] in [space/industry]? What angles haven't been covered yet? What are practitioners frustrated about or excited about? Include specific examples."
```

### Step 7: Filter Through Winning Patterns

Take the research results and filter them through the winning content profile. For each potential topic, ask:

- Does it match one of the top-performing topic clusters?
- Can it be written in the winning format (narrative, tactical, opinion, data)?
- Is there a natural hook that matches the winning hook patterns?
- Does it tap into the emotional register that resonates?
- Can it be written at the winning length and specificity level?

Discard ideas that don't match at least 3 of these 5 criteria.

### Step 8: Generate 10 Content Ideas

For each of the 10 best ideas, produce:

1. **Title** — a working title for the piece
2. **Topic** — what it's about in one sentence
3. **Why it matches** — which winning patterns this idea follows (reference the profile)
4. **Suggested angle** — how to approach it (the specific take or framing)
5. **Hook suggestion** — a draft opening line based on the winning hook formula
6. **Format** — which format to use (narrative, how-to, opinion, data)
7. **Emotional register** — what emotional note to hit
8. **Trending signal** — what from the research makes this timely

### Step 9: Output

Save to: `marketing/plans/lookalike-analysis/lookalike-ideas-YYYY-MM-DD-[platform].md`

**Markdown output format:**

```markdown
# Lookalike Content Ideas — [Platform]
## Based on: [N] posts analysed
## Space: [Industry/space used for research]
## Date: [Today's date]
## Winning Content Profile: winning-content-profile-[platform].md

---

## The Winning Formula
[One-paragraph summary from the profile]

---

## Content Ideas

### 1. [Title]
**Topic:** [One sentence]
**Why it matches:** [Which patterns from the profile this follows]
**Angle:** [The specific take or framing]
**Hook:** "[Draft opening line]"
**Format:** [Narrative / How-to / Opinion / Data-driven]
**Emotional register:** [e.g., Validation + curiosity]
**Trending signal:** [What makes this timely — from the research]

---

### 2. [Title]
[Same structure]

---

[Repeat for all 10 ideas]

---

## Ideas Summary

| # | Title | Pattern match | Format | Trending signal |
|---|---|---|---|---|
| 1 | [Title] | [Key pattern] | [Format] | [Signal] |
| 2 | [Title] | [Key pattern] | [Format] | [Signal] |
[... all 10]
```

Present the file and offer next steps:

```
Done! Here are your 10 lookalike content ideas.

  Winning Content Profile: marketing/plans/lookalike-analysis/winning-content-profile-[platform].md
  Content Ideas: marketing/plans/lookalike-analysis/lookalike-ideas-YYYY-MM-DD-[platform].md

Want to:
  1. Turn one of these into a draft (routes to /blog)
  2. Generate more ideas
  3. Adjust the winning profile and regenerate
  4. Done for now
```

## Output Location

**Output location:** `marketing/plans/lookalike-analysis/` — confirm the project slug with the user before creating files.

---

## Edge Cases

**Very few posts in the data dump (under 10):** Run the analysis but note that patterns may not be reliable. Reduce confidence in the profile findings.

**All posts have similar engagement:** If there's no clear differentiation between top and low performers, analyse all posts equally and note that no performance-based ranking was possible.

**Data dump format is unexpected:** If the file can't be parsed cleanly, ask the user to describe the format: "I'm having trouble parsing this file. Can you tell me: what separates one post from another? Which column has the post text? Which column has the engagement data?"

**No Tavily API key:** Skip the research phase. Generate ideas based solely on the winning patterns and Claude's knowledge. Note that ideas may not reflect the most current trends.

**Audience profile contradicts the data patterns:** Go with the data. The winning content profile is based on what actually worked, which may differ from what the audience profile predicted. Note the discrepancy.

**Client wants ideas for a different platform than the analysed one:** That's fine — the winning patterns (topics, emotion, format) often transfer across platforms. Note that structural patterns (length, hook style) may need adjusting for the new platform.

## File Structure

```
lookalike-content/
├── SKILL.md                              ← you are here
├── scripts/
│   └── tavily_research.py                ← for trending topic research
└── references/
    ├── winning-content-profile-template.md  ← profile output format
    └── html-lookalike-ideas-guide.md        ← HTML styling for ideas output
```

**CRITICAL: Use the script listed above. Do NOT create alternative scripts.**
