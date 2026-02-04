---
name: Technical Blog Post Generator
description: Transform markdown notes into engaging technical blog posts for both programmers and non-technical readers
when_to_use: when you need to create a technical blog post from markdown notes or research material
version: 1.0.0
languages: markdown
---

# Technical Blog Post Generator

## Overview

Transform raw technical notes, research, or project documentation into engaging blog posts that educate both technical and non-technical audiences. The goal is to make complex technical concepts accessible without losing depth.

**Core principle:** Every technical blog post should teach something valuable, tell a story, and be enjoyable to read regardless of the reader's technical background.

## When to Use

Use this skill when:
- Converting project notes or documentation into blog posts
- Writing about technical experiments, case studies, or lessons learned
- Creating educational content about programming concepts
- Sharing technical solutions to real-world problems
- Publishing retrospectives on technical projects

## Required Blog Post Format

**CRITICAL: This is the ONLY acceptable output format. Do NOT deviate from this structure.**

**LANGUAGE: All blog posts MUST be written in ENGLISH (US). Title, excerpt, content, code comments - everything in English.**

Every generated blog post MUST follow this exact structure:

```markdown
---
title: "Your Post Title"
date: "YYYY-MM-DD"
slug: "your-post-slug"
excerpt: "A brief summary of your post (appears in listings)"
thumbnail: "/images/default-thumbnail.png"
categories: ["Category1", "Category2"]
---

# Your Post Title

Introduction paragraph goes here.

## Section Heading

Content goes here with **bold** or *italic* formatting.

### Code Example

\`\`\`javascript
// This is a code block with syntax highlighting
function helloWorld() {
  console.log("Hello, world!");
}
\`\`\`
```

### Mandatory Format Requirements

**YOU MUST adhere to these rules without exception:**

1. **Frontmatter Block** (lines 1-7):
   - MUST start with `---` on line 1
   - MUST end with `---` on line 7
   - MUST contain exactly these 6 fields in this order: title, date, slug, excerpt, thumbnail, categories
   - All field values MUST use double quotes for strings
   - Categories MUST be an array with square brackets: `["Cat1", "Cat2"]`
   - Date MUST be in format: `"YYYY-MM-DD"` (e.g., "2025-10-27")
   - NO extra fields, NO missing fields, NO reordering

2. **Title (line 9)**:
   - MUST be H1 (single #)
   - MUST match the title in frontmatter exactly
   - MUST be followed by a blank line

3. **Content Structure**:
   - Introduction paragraph(s) come immediately after title
   - Major sections use H2 (##)
   - Subsections use H3 (###)
   - NEVER skip heading levels (no H2 → H4)

4. **Code Blocks**:
   - MUST specify language after opening triple backticks
   - Example: \`\`\`javascript NOT \`\`\`
   - Supported languages: javascript, typescript, python, bash, json, etc.

5. **Spacing**:
   - Blank line after frontmatter closing `---`
   - Blank line before and after headings
   - Blank line before and after code blocks
   - Blank line between paragraphs

**Example of CORRECT format:**

```markdown
---
title: "Building AI Agents with Claude SDK"
date: "2025-10-27"
slug: "building-ai-agents-claude-sdk"
excerpt: "Learn how to build production-ready AI agents using Claude Agent SDK and monitor them with New Relic"
thumbnail: "/images/default-thumbnail.png"
categories: ["AI", "TypeScript", "Observability"]
---

# Building AI Agents with Claude SDK

AI agents are transforming how we build applications. But how do you create one that's reliable and observable in production?

In this post, I'll walk you through building a real AI agent using Anthropic's Claude Agent SDK.

## The Challenge

Building an AI agent is straightforward. Making it production-ready is not.

### Observability Matters

Without monitoring, you're flying blind. Here's why:

- Token costs can spiral out of control
- Performance issues go unnoticed
- Errors happen silently

\`\`\`typescript
// Configure the agent with monitoring
const agent = new Agent({
  model: "claude-sonnet-4",
  observability: true
});
\`\`\`

## Lessons Learned

After building this agent, here's what I discovered:

1. Always instrument your agents from day one
2. Monitor token usage in real-time
3. Set up alerts for cost thresholds
```

## Content Structure Checklist

When creating a blog post, ensure you include:

### 1. Compelling Introduction (First 2-3 paragraphs)
- **Hook**: Start with an interesting question, surprising fact, or relatable problem
- **Context**: What is this post about? Why does it matter?
- **Promise**: What will the reader learn or gain from reading?

**Example:**
```markdown
Ever wondered how AI agents know when they're making mistakes? In production,
an AI agent without monitoring is like flying blind - you don't know if it's
working until something breaks spectacularly.

In this post, I'll show you how I built a real-world AI agent using Claude
Agent SDK and integrated it with New Relic for full observability. You'll
learn what worked, what didn't, and why monitoring AI systems is harder than
you might think.
```

### 2. Clear Section Structure
- Use H2 (##) for major sections
- Use H3 (###) for subsections
- Keep sections focused on a single idea
- Use descriptive headings that work as a table of contents

**Recommended sections:**
- Introduction
- The Problem / Context
- The Solution / Approach
- Technical Implementation (if applicable)
- Results / Outcomes
- Lessons Learned
- Conclusion

### 3. Code Examples (for technical posts)
- Always include syntax highlighting (specify language)
- Add comments explaining non-obvious parts
- Show real, working code (not pseudo-code)
- Explain what the code does before showing it

**Example:**
```markdown
The agent uses OpenTelemetry to send traces to New Relic:

\`\`\`typescript
// Configure OpenTelemetry with New Relic exporter
const provider = new NodeTracerProvider({
  resource: new Resource({
    [SemanticResourceAttributes.SERVICE_NAME]: 'markdown-analyzer',
  }),
});

// Send traces to New Relic via OTLP
provider.addSpanProcessor(
  new BatchSpanProcessor(
    new OTLPTraceExporter({
      url: 'https://otlp.nr-data.net:4318/v1/traces',
      headers: { 'api-key': process.env.NEW_RELIC_LICENSE_KEY },
    })
  )
);
\`\`\`
```

### 4. Visual Aids
- Use bullet points for lists
- Use numbered lists for steps or sequences
- Add quotes for important insights
- Consider tables for comparisons

### 5. Accessibility for Non-Technical Readers
- Define technical jargon on first use
- Use analogies to explain complex concepts
- Provide context for why technical details matter
- Include "What this means" explanations after technical sections

**Example:**
```markdown
The agent uses **OpenTelemetry** - think of it as a flight recorder for software,
capturing every action the AI agent takes. This lets us answer questions like
"How long did it take?" and "Did it work correctly?"
```

### 6. Real-World Context
- Explain the "why" not just the "what"
- Share actual problems you faced and how you solved them
- Include lessons learned, including failures
- Make it relatable with real use cases

### 7. Strong Conclusion
- Summarize key takeaways (2-4 bullet points)
- Suggest next steps or further reading
- Optional: Call to action (try it yourself, share feedback, etc.)

## Writing Style Guidelines

### Tone
- **Conversational but professional**: Write like you're explaining to a colleague over coffee
- **Honest**: Share what didn't work, not just successes
- **Enthusiastic but not hyperbolic**: Show genuine interest without overselling

### Language
- Use active voice: "I built" not "was built"
- Use "you" to engage readers directly
- Avoid unnecessary jargon; explain terms when needed
- Use short sentences for clarity, longer ones for rhythm

### Technical Depth
- **Layer your explanations**: Start high-level, then go deeper
- **Provide context first**: Explain why before how
- **Show don't just tell**: Use examples and code snippets
- **Respect all readers**: Technical readers want depth, non-technical want understanding

## Content Generation Process

Follow these steps when generating a blog post:

### Step 1: Analyze the Input
- Read the provided markdown notes thoroughly
- Identify the core story or lesson
- Note key technical concepts
- Identify the target audience

### Step 2: Extract Key Information
From the notes, identify:
- **Main topic**: What is this really about?
- **Problem**: What challenge was addressed?
- **Solution**: How was it solved?
- **Learning**: What did this teach?
- **Technical details**: What specifics matter?

### Step 3: Structure the Narrative
Create a logical flow:
1. Hook readers with the interesting part
2. Provide necessary context
3. Explain the journey (problem → solution)
4. Share technical implementation details
5. Reflect on outcomes and lessons
6. Wrap up with actionable takeaways

### Step 4: Write for Multiple Audiences
For each section, consider:
- **Technical readers**: Provide accurate details, code examples, architectural decisions
- **Non-technical readers**: Explain why it matters, use analogies, provide context
- **Skimmers**: Use clear headings, bullet points, and highlighted key points

### Step 5: Generate Frontmatter
- **title**: Clear, engaging, descriptive (50-60 chars ideal)
- **date**: Use the current date in YYYY-MM-DD format
- **slug**: URL-friendly version of title (lowercase, hyphens)
- **excerpt**: Compelling 1-2 sentence summary (140-160 chars)
- **thumbnail**: Use "/images/default-thumbnail.png" or suggest specific image
- **categories**: 2-4 relevant categories (e.g., "AI", "Observability", "TypeScript")

### Step 6: Polish and Refine
- Check that all code blocks have language specified
- Ensure technical terms are explained
- Verify the narrative flows logically
- Confirm the conclusion summarizes key points

## Example Transformations

### From Project Notes to Blog Post

**Input (notes):**
```
Built an AI agent with Claude SDK. Added New Relic monitoring.
First tried Traceloop but didn't work. Then used OpenTelemetry.
Agent analyzes markdown files.
```

**Output (blog post intro):**
```markdown
# Monitoring AI Agents: A Practical Guide to Claude SDK and New Relic

Building an AI agent is exciting. Deploying it to production without monitoring
is terrifying. How do you know if it's working? How much is it costing? Where
are the bottlenecks?

I recently built a markdown analysis agent using Anthropic's Claude Agent SDK
and quickly realized that observability wasn't optional - it was critical.
But integrating monitoring turned out to be more challenging than expected.

In this post, I'll show you how I solved the observability problem, including
a false start with Traceloop and the eventual solution using OpenTelemetry.
You'll learn practical patterns for monitoring AI agents and avoid the mistakes
I made along the way.
```

## Common Mistakes to Avoid

### Content Mistakes
- **Too much assumed knowledge**: Always explain context
- **Jumping to code too quickly**: Set up the problem first
- **No "why"**: Technical details without purpose are boring
- **Missing the human element**: Share struggles and insights
- **No conclusion**: Always summarize and suggest next steps

### Format Mistakes
- **Missing frontmatter fields**: All fields are required
- **Wrong date format**: Must be YYYY-MM-DD
- **No language in code blocks**: Always specify (javascript, typescript, python, etc.)
- **Inconsistent heading levels**: Don't skip from H2 to H4
- **Wall of text**: Break up long paragraphs with lists, code, or subheadings

### Style Mistakes
- **Passive voice overuse**: "The agent was built" → "I built the agent"
- **Jargon without explanation**: Define or avoid
- **Too formal or academic**: This is a blog, not a research paper
- **Hyperbolic claims**: "Revolutionary" "Best ever" "Game-changing" - be honest instead

## Output Requirements

**CRITICAL: Read the "Required Blog Post Format" section and follow it EXACTLY.**

**LANGUAGE REQUIREMENT: Write EVERYTHING in ENGLISH (US). No exceptions.**

When generating a blog post, you MUST:

1. **Start with complete frontmatter** including all required fields (title, date, slug, excerpt, thumbnail, categories)
2. **Use the EXACT format** specified in the "Required Blog Post Format" section - NO deviations
3. **Frontmatter format**:
   - Lines 1-7 only
   - Start and end with `---`
   - All string values in double quotes
   - Categories as array: `["Cat1", "Cat2"]`
   - Date format: `"YYYY-MM-DD"`
4. **Title on line 9** must be H1 (#) and match frontmatter title exactly
5. **Include at least 3-5 major sections** (H2 headings)
6. **Add code examples** with proper syntax highlighting (for technical posts)
7. **Specify language for ALL code blocks** (```javascript NOT ```)
8. **Write 800-2000 words** depending on topic complexity
9. **End with a strong conclusion** that summarizes key takeaways
10. **Make it accessible** to both technical and non-technical readers
11. **Tell a story** not just present information

**FORMAT VALIDATION CHECKLIST - Verify before outputting:**
- [ ] EVERYTHING is written in ENGLISH (US)
- [ ] Frontmatter starts with `---` on line 1
- [ ] Frontmatter ends with `---` on line 7
- [ ] All 6 required fields present: title, date, slug, excerpt, thumbnail, categories
- [ ] All strings use double quotes
- [ ] Date is "YYYY-MM-DD" format
- [ ] Categories is an array with brackets
- [ ] Blank line after frontmatter (line 8)
- [ ] Title is H1 on line 9 and matches frontmatter
- [ ] All code blocks specify language
- [ ] Proper spacing throughout (blank lines before/after headings and code blocks)

## Customization Based on Content Type

### Technical Tutorial
- Focus on step-by-step implementation
- Include complete, working code examples
- Add troubleshooting section
- Provide prerequisites upfront

### Case Study / Project Retrospective
- Start with the problem context
- Explain the approach and alternatives considered
- Share implementation details with code
- Reflect on lessons learned and outcomes

### Concept Explanation
- Build from simple to complex
- Use analogies and real-world examples
- Include practical applications
- Provide further reading resources

### Opinion / Best Practices
- State your position clearly upfront
- Back claims with evidence or experience
- Acknowledge alternative viewpoints
- Provide actionable recommendations

## Quality Checklist

Before considering a blog post complete, verify:

- [ ] Entire post is written in ENGLISH (US) - no Polish, no other languages
- [ ] Frontmatter is complete and correctly formatted
- [ ] Title is clear and engaging
- [ ] Excerpt accurately summarizes the post
- [ ] Introduction hooks the reader and sets expectations
- [ ] Sections are logically organized with clear headings
- [ ] Code examples have language specified and are explained
- [ ] Technical terms are defined on first use
- [ ] Content is accessible to both technical and non-technical readers
- [ ] Real-world context and "why" are provided
- [ ] Lessons learned or insights are shared
- [ ] Conclusion summarizes key takeaways
- [ ] Post is 800+ words (unless intentionally shorter)
- [ ] No formatting errors or markdown issues

## Final Notes

**Remember**: The best technical blog posts teach something valuable while being
enjoyable to read. Focus on clarity, honesty, and providing real value to your readers.

When in doubt, ask yourself: "Would I want to read this?" and "Did I learn something
I can actually use?"

---

## FINAL OUTPUT FORMAT REMINDER

**Before you output ANYTHING, re-read this:**

**WRITE IN ENGLISH (US) - Every word, every sentence, every code comment must be in English.**

Your output MUST be a complete markdown file that starts EXACTLY like this:

```
---
title: "Your Actual Title Here"
date: "2025-10-27"
slug: "your-actual-slug-here"
excerpt: "Your actual excerpt here"
thumbnail: "/images/default-thumbnail.png"
categories: ["Category1", "Category2"]
---

# Your Actual Title Here

Your introduction starts here...
```

**NON-NEGOTIABLE RULES:**

1. First line MUST be `---` (three dashes)
2. Line 7 MUST be `---` (three dashes)
3. Lines 2-6 MUST contain exactly: title, date, slug, excerpt, thumbnail, categories (in that order)
4. ALL string values MUST use double quotes: `"like this"`
5. Categories MUST be an array: `["Cat1", "Cat2"]`
6. Date MUST be `"YYYY-MM-DD"` format (e.g., "2025-10-27")
7. Line 8 MUST be blank
8. Line 9 MUST be `# Title` (H1 matching frontmatter title)
9. ALL code blocks MUST specify language: ```javascript NOT ```

**DO NOT:**
- Add extra frontmatter fields
- Use single quotes
- Forget the blank line after frontmatter
- Start with explanations or preamble
- Output anything before the frontmatter
- Write in any language other than English (US)

**START YOUR OUTPUT WITH THE FRONTMATTER. NOTHING ELSE.**
**WRITE EVERYTHING IN ENGLISH.**
