---
name: "Web Content Summarizer"
description: "Fetch and summarize web content for any research task - documentation, design inspiration, competitor analysis, tutorials, API docs. Use when you need to understand web pages, extract key information, research patterns, or gather context for development work."
---

# Web Content Summarizer

## What This Skill Does

Fetches web content and generates focused summaries using Claude. Adapted from [Anthropic's web summarization cookbook](https://github.com/anthropics/anthropic-cookbook).

**Use Cases**:
1. **Documentation Research** - Summarize framework docs, API references, tutorials
2. **Design Inspiration** - Analyze competitor sites, design patterns, UI examples
3. **Technical Research** - Extract key info from blog posts, Stack Overflow, GitHub
4. **Content Gathering** - Pull relevant info for site content, copy, features

---

## Quick Start

### Summarize Any Page
```
WebFetch("https://example.com/page", "Summarize the main points and key takeaways")
```

### Search Then Summarize
```
WebSearch("Astro 5.0 new features 2025")
// Then WebFetch the most relevant result
```

---

## Research Patterns

### Pattern 1: Documentation Lookup

**When**: Learning a framework feature, checking API syntax, understanding a library

```markdown
1. WebSearch for "[framework] [feature] documentation"
2. WebFetch the official docs page
3. Ask: "Extract the key syntax, examples, and gotchas"
```

**Example**:
```
WebFetch("https://docs.astro.build/en/guides/content-collections/",
         "Summarize how to set up and use content collections in Astro 5.x")
```

### Pattern 2: Design Research

**When**: Looking for UI patterns, design inspiration, competitor analysis

```markdown
1. WebSearch for "[type of site] design examples" or visit competitor
2. WebFetch the page
3. Ask: "Describe the layout, color scheme, typography, and notable UI patterns"
```

**Example**:
```
WebFetch("https://competitor-site.com",
         "Analyze the design: layout structure, colors, fonts, navigation, calls-to-action")
```

### Pattern 3: Technical Problem Solving

**When**: Debugging, finding solutions, understanding error messages

```markdown
1. WebSearch for "[error message]" or "[problem] [framework] solution"
2. WebFetch Stack Overflow or blog posts
3. Ask: "What's the solution and why does it work?"
```

**Example**:
```
WebSearch("Tailwind CSS 4.0 @theme not working")
// WebFetch the most relevant result
```

### Pattern 4: Content Research

**When**: Gathering information for site content, blog posts, product descriptions

```markdown
1. WebSearch for "[topic] guide" or "[topic] overview"
2. WebFetch multiple authoritative sources
3. Ask: "Extract key facts, statistics, and talking points"
```

---

## Tool Reference

### WebFetch
Fetches a URL and processes content with a prompt.

```
WebFetch(url, prompt)
```

**Parameters**:
- `url`: Full URL to fetch (required)
- `prompt`: What to extract/summarize (required)

**Prompt Tips**:
- Be specific: "Extract the installation steps" vs "Summarize"
- Request format: "List as bullet points" or "Format as a table"
- Focus: "Focus on [specific aspect]" or "Ignore [irrelevant parts]"

**Examples**:
```
// Documentation
WebFetch("https://tailwindcss.com/docs/installation",
         "List the installation steps for Tailwind CSS with Astro")

// Design analysis
WebFetch("https://dribbble.com/shots/example",
         "Describe the color palette, typography, and layout approach")

// Technical article
WebFetch("https://blog.example.com/post",
         "Summarize the main argument and code examples")
```

### WebSearch
Searches the web and returns results.

```
WebSearch(query)
```

**Query Tips**:
- Add year for current info: "React 19 features 2025"
- Add "docs" or "tutorial" for learning: "Astro SSR tutorial"
- Add "vs" for comparisons: "Tailwind vs CSS modules"
- Quote exact phrases: `"exact error message"`

**Examples**:
```
WebSearch("Astro 5.0 content collections tutorial")
WebSearch("Tailwind CSS 4.0 breaking changes")
WebSearch("outdoor store website design inspiration")
```

---

## Output Formats

### Quick Summary
```
WebFetch(url, "Summarize in 3-5 bullet points")
```

### Detailed Breakdown
```
WebFetch(url, "Break down into sections: Overview, Key Points, Examples, Gotchas")
```

### Comparison Table
```
WebFetch(url, "Extract features and format as a comparison table")
```

### Action Items
```
WebFetch(url, "What are the actionable steps or recommendations?")
```

### Code Extraction
```
WebFetch(url, "Extract all code examples with brief explanations")
```

---

## WVWO-Specific Research

When researching for WVWO specifically, maintain the project voice:

### Design Research
- Look for: Rural, authentic, handmade aesthetics
- Avoid: SaaS, startup, corporate patterns
- Ask: "Does this feel like Kim's shop or a tech company?"

### Content Research
- Write summaries in conversational tone
- Avoid marketing speak
- Focus on practical, helpful information

### Technical Research
- Prioritize: Astro, Tailwind CSS, vanilla JS solutions
- Avoid: React, Vue, complex frameworks
- Keep it simple and maintainable

---

## Common Research Tasks

### Task: Learn a New Astro Feature
```
1. WebSearch("Astro [feature] guide 2025")
2. WebFetch official docs
3. WebFetch a tutorial for examples
4. Summarize: Syntax, use cases, gotchas
```

### Task: Find Design Inspiration
```
1. WebSearch("[type] website design inspiration")
2. WebFetch 2-3 examples
3. Summarize: What works, what to adapt for WVWO
```

### Task: Debug an Issue
```
1. WebSearch("[exact error message]")
2. WebFetch Stack Overflow or GitHub issue
3. Extract: Root cause, solution, verification steps
```

### Task: Research a Library
```
1. WebFetch the library's homepage/README
2. WebFetch the documentation
3. Summarize: What it does, how to install, basic usage, alternatives
```

---

## Troubleshooting

### Issue: Page Won't Load
**Cause**: Site blocks automated access
**Solution**: Try WebSearch instead, or manually copy relevant content

### Issue: Content Seems Outdated
**Cause**: Cached or old page
**Solution**: Add current year to search, verify publish date on source

### Issue: Too Much Content
**Cause**: Page is very long
**Solution**: Use more specific prompt: "Focus only on [section]"

### Issue: Paywall or Login Required
**Cause**: Restricted content
**Solution**: Search for alternative sources, or use publicly available portions

---

## Integration with Project Workflow

This skill integrates with other WVWO tools:

1. **Research** → Use this skill to gather context
2. **Implement** → Apply findings to Astro components
3. **Learn** → Store successful patterns with AgentDB
4. **Verify** → Check work against aesthetics guidelines

---

**Skill Version**: 1.1.0
**Based On**: Anthropic's Web Summarization Cookbook
**Scope**: Project-wide research and content gathering
