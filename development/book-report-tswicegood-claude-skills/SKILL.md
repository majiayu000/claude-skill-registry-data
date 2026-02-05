---
name: book-report
description: Comprehensive research and analysis of books with actionable insights, hidden gems, and personalized recommendations. Use when the user requests book research, book reports, book analysis, or says "Research Book" followed by a book title. Adapts to project context (professional, personal, academic, hobby).
---

# Book Report

Generate comprehensive, actionable book reports with strategic insights, immediate action items, overlooked insights, and personalized recommendations.

## Trigger Phrases

Activate this skill when the user says:
- "Research Book: {Book Title}"
- "Create a book report for {Book Title}"
- "Analyze {Book Title}"
- Similar requests for book analysis or research

**Conciseness Modes:**
- Default: Concise, edited reports (50% reduction from initial draft)
- Verbose mode: When user requests "detailed," "comprehensive," "full," or "wordy" version

## Context Adaptation

This skill adapts to the project context (professional/business, personal development, academic, hobby). Infer context from:
- Project name and description
- Conversation history
- Project Knowledge documents
- Topics being discussed

**For detailed adaptation guidance**, read `references/context_adaptation.md` for tailoring tone, action items, and recommendations to specific contexts.

## Workflow

### Step 1: Confirm Book

When the user requests a book report:

1. Perform a web search for the book
2. Present findings with:
   - Full title
   - Author name
   - Publication date (original and latest edition if applicable)
3. Ask user to confirm this is the correct book
4. Wait for confirmation before proceeding to Step 2

**Example response format:**
```
I found the following book:
- **Title:** [Full Title]
- **Author:** [Author Name]
- **Publication Date:** [Date]

Is this the correct book you'd like me to research?
```

### Step 2: Adaptive Research Protocol

Once confirmed, execute the following structured research process:

**PHASE 1: RECONNAISSANCE (Max 5 searches)**
- Search for: [book title + author], [book title + reviews], [book title + summary]
- Assess information density:
  * HIGH: 3+ detailed sources found (professional reviews, author interviews, critical analysis)
  * MEDIUM: 2-3 basic sources (publisher description, brief reviews, goodreads)
  * LOW: 0-1 sources or only announcement/pre-release info

**DECISION CHECKPOINT:**
- IF information density = HIGH → Research Mode OFF (sufficient data in 10-15 total searches)
- IF information density = MEDIUM → Research Mode PARTIAL (up to 20 searches, focus on depth)
- IF information density = LOW → Research Mode OFF (stop at 15 searches, note limited availability)

Explicitly state your decision and reasoning before proceeding to Phase 2.

**PHASE 2: DEEP RESEARCH**
- Execute based on decision from checkpoint
- Gather information from: book reviews (professional and reader), academic analyses, expert commentary, author interviews, summary resources, related discussions
- Stop early if searches return redundant information

Create an initial draft with the full report using the structure below.

### Step 3: Editorial Pass for Conciseness

**Default behavior (concise mode):**
After completing the initial draft, perform a rigorous editing pass to reduce content by approximately 50% while preserving all critical insights:

1. **Identify core insights:** Mark the essential points that must remain
2. **Eliminate redundancy:** Remove repetitive explanations and examples
3. **Tighten language:** Replace wordy phrases with concise alternatives
4. **Consolidate sections:** Merge overlapping points
5. **Focus on actionability:** Keep what's implementable, remove philosophical padding

**Quality standards for editing:**
- Every remaining sentence must serve a clear purpose
- No loss of critical insights or actionable recommendations
- Maintain the full 8-section structure
- Preserve context-specific adaptations
- Keep all strategic insights from "Hidden Gems"

**Verbose mode exception:**
Skip this step entirely if the user's request includes words like "detailed," "comprehensive," "full," "thorough," or "wordy." Proceed directly with the unedited comprehensive report.

After editing (or if skipping in verbose mode), create an artifact (.md file) with the final report. Also provide a one-paragraph "bottom line up front" summary in the main response.

## Report Structure

### 1. Bottom Line Up Front Summary (1 paragraph)

Synthesize the book's most transformative insight and core value proposition. Answer: Why should someone read this book?

Include this paragraph both at the beginning of the artifact AND in the main response.

### 2. Book Overview (2-3 sentences)
- Core thesis and main themes
- Target audience and historical context
- Why this book matters

### 3. Comprehensive Summary
Break down into 4-5 key concepts or sections:
- Main idea for each concept
- Supporting evidence and arguments
- Relevant examples or case studies the author uses
- How concepts interconnect

### 4. Immediate Action Items (5-7 specific actions)
List concrete, implementable steps for the next 30 days:
- **Action:** Clear, specific step
- **Why it's impactful:** Evidence or reasoning
- **How to implement:** Practical guidance
- **Priority order:** From easiest to most challenging

Adapt actions to project context (business implementations vs. personal habits vs. research applications vs. hobby skills).

### 5. Strategic Applications (3-4 broader concepts)
Longer-term strategies and mindset shifts:
- Key principle or strategy
- How it applies to relevant domain (business/personal/academic/hobby)
- Potential obstacles and solutions
- How to measure progress or success

### 6. Hidden Gems: Overlooked Insights (minimum 5 takeaways)
Critical thinking required - identify insights that most readers miss:
- Ideas mentioned but not emphasized in typical reviews
- Subtle concepts often overlooked on first reading
- Counter-intuitive insights challenging conventional wisdom
- Connections between different parts of the book
- Small details with significant implications
- Nuances in the author's arguments

**Think deeply:** What would a casual reader miss? What do reviews underemphasize?

### 7. Critical Analysis
Balanced evaluation:
- **Strongest arguments:** What does the book do exceptionally well?
- **Weaknesses or gaps:** Are there limitations, biases, or criticisms from experts?
- **Comparative context:** How does this compare to similar works?
- **Applicability:** When is this book most/least useful?

### 8. Personalized Recommendations

Based on the user's inferred profile and project context:
- **2-3 complementary books:** Titles that extend or complement this book's ideas
- **Why these books:** How each recommendation connects
- **Most valuable insights:** Which parts of this book are most relevant to this specific user/context

Tailor recommendations to context:
- **Business:** Industry-relevant, practical business books
- **Personal:** Growth-oriented, habit/mindset books
- **Academic:** Scholarly works, research methodologies
- **Hobby:** Skill-building, practitioner guides

## Quality Standards

- **Adaptive research:** Follow the phased research protocol with density assessment and appropriate search limits
- **Original synthesis:** Avoid merely aggregating summaries - provide unique insights
- **Actionability:** Make every recommendation concrete and implementable
- **Context awareness:** Seamlessly adapt tone and focus to project context
- **Citation quality:** Focus on authoritative sources (author interviews, scholarly analyses, reputable publications)
- **Depth over breadth:** Better to deeply analyze 4-5 key concepts than superficially cover 10
- **Conciseness by default:** Edit ruthlessly to reduce length by ~50% without losing substance (unless verbose mode requested)

## Response Format

After completing research:

1. **Main response:** Brief confirmation + one-paragraph BLUF summary + link to artifact
2. **Artifact:** Full markdown report with all 8 sections

**Example main response:**
```
I've completed comprehensive research on [Book Title] by [Author] and edited it for conciseness while preserving all critical insights.

[One-paragraph BLUF summary]

[View your complete book report](computer://...)
```

## Common Pitfalls to Avoid

- Don't just summarize the book - provide analysis and synthesis
- Don't ignore the user's context - adapt recommendations
- Don't list obvious insights - dig for hidden gems
- Don't copy book summaries verbatim - paraphrase and cite
- Don't skip the confirmation step - verify the correct book first
- Don't skip the editing pass unless verbose mode is requested - wordiness obscures insights

