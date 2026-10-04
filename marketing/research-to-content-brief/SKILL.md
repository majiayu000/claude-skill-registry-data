---
name: research-to-content-brief
description: "Transform research notes (audience, competitor signals, trend snippets) into a structured content brief. Use when turning scattered research files into an actionable creation plan. Triggers: 'research to content brief', 'бриф из исследований', 'составь контент-бриф из заметок'."
version: 1.0.0
---

# Research to Content Brief

This skill reads a folder of raw research notes (audience observations, competitor signals, trend snippets) and synthesizes them into a structured content brief. Unlike dialogue-based brief generators, it extracts insights directly from your files — no interview needed.

**Input:**
- Folder path containing `.md` and/or `.txt` research files, OR direct paste of research notes with type labels
- Optional: target content format hint (blog post, landing page, social, email)

**Output:**
- `content-brief.md` — structured markdown brief with six sections: Audience, Core Message, Content Angles, Competitive Differentiation, Trend Hooks, Recommended Formats

---

## Language Detection

Detect the user's language from their message:
- If Russian (or contains Cyrillic): respond in Russian
- If English (or other Latin-script language): respond in English
- If ambiguous: respond in the language of the trigger phrase used

---

## Instructions

### Step 1: Read and Categorize Research Files

1. Read all `.md` and `.txt` files from the provided folder path (or accept pasted content)
   - If no files found and no content pasted: stop immediately. Report: "No research files found. Provide a folder path with .md or .txt files, or paste research notes directly."
   - If files exist but contain no readable text (images, binary, placeholder text): Report: "Files found but contain no extractable research content. Ensure files are .md or .txt with actual text."

2. Categorize each file into one of four types:
   - **Audience notes** — pain points, goals, jobs-to-be-done, user profiles, quotes
   - **Competitor signals** — what competitors do/say, feature lists, positioning language
   - **Trend snippets** — industry trends, emerging topics, market shifts, date-stamped observations
   - **Other** — anything that doesn't fit the above (include in extraction as context)

3. If files lack explicit category labels, auto-categorize by keyword heuristics:
   - Competitor names, brand names, "they offer", "pricing", "compared to" → competitor signals
   - "pain", "problem", "frustrated", "goal", "wants to", "needs to", "job" → audience notes
   - "trend", "growing", "2025", "2026", "new", "emerging", "market shift" → trend snippets
   - Note classification rationale in the output source coverage section

**Edge Case — Sparse files (< 5 lines each or bare bullet lists):**
   - Continue processing; prepend warning at top of output: "⚠️ Source files are sparse — brief may need manual enrichment before use."

**Edge Case — Only one file type present:**
   - Continue processing; mark all missing-type sections as "NEEDS MANUAL INPUT — no source data."

### Step 2: Extract Key Data Points per Category

1. **From audience notes** — extract:
   - Who they are (role, context, expertise level)
   - Core pain points (what frustrates them)
   - Jobs to be done (what they're trying to accomplish)

2. **From competitor signals** — extract:
   - What competitors are saying or doing
   - Gaps or angles competitors are missing
   - Differentiation opportunities

3. **From trend snippets** — extract:
   - Emerging topics with relevance to the audience
   - Hooks or angles tied to current market shifts

4. **From "other" files** — extract any signal that informs content strategy: context, constraints, goals

### Step 3: Synthesize the Core Message

1. Based on audience pain points + differentiation opportunities, formulate a Core Message:
   - 1–2 sentences stating the central claim the content should make
   - Should be specific (not generic brand messaging)

### Step 4: Generate Content Angles

1. Derive at least 2 distinct content angles from the research:
   - Each angle = a hook + rationale (why it will resonate with the audience based on extracted data)
   - Angles should be concrete, not generic (e.g., "How PMs are solving X without Y" not "Tips for PMs")

2. If content format hint was provided, tune angles:
   - Blog post → narrative hooks, problem-solution structure
   - Landing page → value propositions, objection handling
   - Social → punchy angles, pattern interrupts, CTAs
   - Email → subject line hooks, personal framing

### Step 5: Compile and Output Content Brief

1. Build the `content-brief.md` document using the Output Format template below
2. Flag any section with no source data as "NEEDS MANUAL INPUT — no source data"
3. Include source coverage summary at the bottom (which files contributed to which sections)
4. If sparse-files warning was triggered in Step 1, include it at the top of the document

---

## Output Format

Save output as `content-brief.md` with this structure:

```markdown
# Content Brief: [topic derived from research]

**Generated:** YYYY-MM-DD
**Source files:** [list of files used]
**Target format:** [if provided, otherwise "unspecified"]

---

## Audience
- **Who they are:** [role, context, expertise level]
- **Pain points:** [extracted from audience notes]
- **Jobs to be done:** [what they're trying to accomplish]

## Core Message
[1–2 sentences: the central claim this content should make]

## Content Angles
1. [Angle 1: hook + rationale based on research]
2. [Angle 2: hook + rationale based on research]
3. [Angle 3: hook + rationale — optional]

## Competitive Differentiation
- **What competitors say/do:** [extracted]
- **Gap they're missing:** [extracted angle]
- **Differentiation point:** [synthesized]

## Trend Hooks
- [Trend 1 with relevance note and source file]
- [Trend 2 with relevance note and source file]

## Recommended Formats
- [Format 1: rationale based on audience + angles]
- [Format 2: rationale]

---
**Source coverage:**
- Audience notes: [N files — list filenames]
- Competitor signals: [N files — list filenames]
- Trend snippets: [N files — list filenames]
⚠️ Sections marked [NEEDS MANUAL INPUT] had no source data.
```

**Field rules:**
- Content Angles must be derived from extracted research (not generic advice)
- Sections with no source data must be marked "NEEDS MANUAL INPUT" — never silently omitted
- Source coverage must list filenames, not just counts

---

## Negative Cases

- If folder path not provided and no content pasted: Stop. Report "No research files found. Provide a folder path with .md or .txt files, or paste research notes directly."
- If all files are unreadable (binary, images, empty): Report "Files found but contain no extractable research content. Ensure files are .md or .txt with actual text."
