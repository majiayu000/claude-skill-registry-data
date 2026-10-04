---
name: post-conference-insights
description: >
  Produce branded conference recap one-pagers (1-2 page PDF) that position Solum Health as an
  industry thought leader. Use this skill whenever the user mentions a conference, summit, event,
  or expo they attended or want insights from. Also trigger on: "conference recap", "post conference
  insights", "event highlights", "conference one-pager", "summit recap", "what happened at [event]",
  "conference takeaways", "event summary", "write up from [event]", "key takeaways from [conference]",
  or anything involving turning conference attendance into a shareable client-facing document.
  Even if the user just names a conference ("HIMSS", "BHASe", "Becker's"), assume they want the
  full insight one-pager workflow unless they say otherwise.
---

# Post-Conference Insights

Turn any healthcare conference into a branded 1-page (max 2-page) PDF one-pager that positions
Solum Health as a thought leader sharing industry intelligence. The output is designed to be sent
directly to clients and prospects as a value-add.

## Core Principle

This is NOT a conference recap. It's a strategic insight document written as if Solum Health's
team attended, took notes, talked to people, and came back with the stuff that actually matters
for practice owners and operators. It should read like a smart colleague sharing field notes
over coffee, not a marketing department producing content.

## The Workflow

Execute these 5 phases in order. Phases 1a and 1b run in parallel.

### Phase 1: Research (parallel agents)

Launch two Task agents simultaneously:

**Agent 1 — Conference Intelligence:**
Research the specific conference. Search the web for:
- Official agenda, session titles, panel topics, speaker names
- Recaps, blog posts, LinkedIn posts, press releases about the event
- Key data points, statistics, and quotes shared at sessions
- Technology, AI, automation, and operations discussions
- Any controversy, surprise announcements, or notable moments

Focus on extracting concrete data points (percentages, dollar amounts, survey results)
rather than vague summaries. The final document needs real numbers.

**Agent 2 — Audience & ICP Analysis:**
Research who attends this specific conference:
- Job titles and roles of typical attendees
- Their top 3 pain points right now
- What kind of conference takeaway they'd actually read vs. dismiss
- What format resonates (bullets, narratives, data, action items)
- What makes them trust a document vs. see it as marketing fluff
- What specific AI/automation topics would be immediately actionable for them

### Phase 2: Content Generation

Write the insights document following these rules:

**Voice & Tone** — Read `references/brand-guide.md` for the full Solum Health brand guide.
The short version: write like a fellow practice owner sharing notes, not a vendor pitching.
Consultative, energetic, practitioner-peer. Use contractions. Be direct. Have opinions.

**Structure for the one-pager:**
1. White branded header strip with Solum Health logo + "INDUSTRY INSIGHTS" tag
2. Navy banner with document title and event details
3. 4 stat cards with the most impactful numbers from the conference
4. 4-6 tight insight sections (each: terracotta left-bar header + 1-2 paragraphs)
5. Page 2: "What Your Team Can Do Monday Morning" with role-based action cards
6. Closing contact card with JP Montoya's info

**Content Rules:**
- Lead every section with a specific, sourced number when possible
- Include "so what" context for every stat (translate to dollar terms for a mid-size practice)
- Add 2-3 "you were there" moments (specific panel reactions, hallway conversations, quotes)
- Include honest uncertainty where appropriate ("we're not 100% sure this holds everywhere")
- NO product promotions. NO sponsor mentions. Pure insights only.
- Role-based action items for: billing team, clinical directors, front desk/intake, owners

### Phase 3: Humanization

Run a QA agent with the anti-AI detection checklist. Read `references/anti-ai-checklist.md`
for the complete list. The critical rules:

- **Zero dashes** as punctuation (em dashes, en dashes). Compound-word hyphens are fine.
- **Zero AI buzzwords** from the banned list (leverage, streamline, robust, comprehensive, etc.)
- **Zero forbidden starters** (However, Moreover, Furthermore, Additionally at sentence start)
- Vary sentence length aggressively. Mix 5-word fragments with 25-word sentences.
- Use contractions everywhere natural. Start sentences with "And" or "But."
- Add colloquial phrases ("here's the thing", "look, we get it", "real talk:")
- Target: AI detection score under 20%. Iterate until met.

### Phase 4: PDF Generation

Generate the branded PDF using the template script. Read `scripts/generate_pdf.py` for
the complete generator. Key specifications:

- **Strict 2-page maximum.** Auto page break disabled, all content manually placed.
- **Logo on every page:** white branded strip at top with large Solum Health logo + "INDUSTRY INSIGHTS" in terracotta
- **Colors:** Navy #0E1C36, Terracotta #BD5237, Teal #267688
- **Fonts:** Georgia Bold for headers, Arial for body. Size 9.5-11pt.
- **Layout:** stat cards with colored top bars, section headers with terracotta left bar, teal bullet points, 2-column role cards on page 2
- **Contact:** JP Montoya, jp@getsolum.com, 628 276 2659, getsolum.com
- **Footer every page:** Solum logo left, "Solum Health Industry Insights" label, contact right

The script at `scripts/generate_pdf.py` is the working template. Copy it, modify the content
sections for the new conference, and run it. The structure and styling should stay the same.

### Phase 5: Verification

Before presenting to the user:
1. Verify the PDF is exactly 2 pages (read binary, count `/Type /Page` entries)
2. Verify the logo path exists (`~/solum_logo.png`)
3. Open the PDF for user review
4. Report: page count, file size, and what's on each page

## File Dependencies

- **Logo:** `~/solum_logo.png` (must exist; if not, fetch from getsolum.com and convert AVIF to PNG)
- **Python:** fpdf2 (`pip install fpdf2` if not available)
- **Fonts:** Georgia.ttf and Arial.ttf from `/System/Library/Fonts/Supplemental/` (macOS)

## Output

Default output path: `~/[ConferenceName]_[Year]_OnePager_Solum_Health.pdf`

Always end by opening the PDF and asking if the user wants adjustments.
