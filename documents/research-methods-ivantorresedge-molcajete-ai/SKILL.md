---
name: research-methods
description: Standards and methods for conducting research, gathering information, and presenting findings with proper source attribution. Use when researching topics, analyzing documentation, or synthesizing information from multiple sources.
---

# Research Methods

Comprehensive standards for conducting research, evaluating sources, and presenting information in clear, well-formatted responses.

## When to Use This Skill

Use this skill when:
- Researching documentation for tools, frameworks, or APIs
- Gathering information from multiple sources
- Synthesizing findings into coherent responses
- Creating reference materials
- Answering questions requiring external information
- Building knowledge bases

## Key Principles

1. **Ask before researching** - Clarify ambiguous queries before starting
2. **Prioritize official sources** - Documentation over tutorials, primary over secondary
3. **Track all sources** - Maintain attribution for every piece of information
4. **Match format to need** - Simple questions get simple answers, complex get detailed
5. **Accuracy over speed** - Cross-reference critical information
6. **User-focused presentation** - Scannable, organized, actionable

## Response Type Selection

### Simple Response

**Use when:**
- Single, specific question
- How-to query with clear scope
- Quick reference lookup
- Command syntax or parameter info
- Definition or concept explanation
- User wants fast answer

**Template:**
```markdown
# [Concise Title]

[Direct answer to the question]

[Code example if applicable]

## Sources
- [URL] - [Description]
```

**Example questions:**
- "How do I amend a git commit?"
- "What is the Stop hook in Claude Code?"
- "How to use WebFetch tool?"

### Detailed Response

**Use when:**
- Broad, exploratory question
- Request mentions "comprehensive", "all", "detailed"
- Time estimate provided ("5 min intro", "quick overview")
- Multiple related concepts
- Comparative analysis
- Building reference material

**Template:**
```markdown
# [Descriptive Title]

[Executive summary - 2-3 sentences providing overview]

## Overview
[Context and background]

## [Topic Section 1]
[Detailed information]

## [Topic Section 2]
[Detailed information]

## Key Takeaways
- [Point 1]
- [Point 2]
- [Point 3]

## Sources
- [URL] - [Description]
```

**Example questions:**
- "Research all available hooks in Claude Code"
- "Give me a comprehensive overview of git workflows"
- "Explain React hooks and when to use them"

## Research Process

### 1. Clarification Phase

Before starting research:
- Identify ambiguities in the query
- Ask specific clarifying questions
- Don't assume user intent
- Use AskUserQuestion tool for multiple clarifications

**Examples of good clarifications:**
- "Are you asking about React library hooks or Claude Code hooks?"
- "Do you want a quick reference or detailed explanation?"
- "Which version are you using?"

### 2. Source Selection

**Priority order:**

**Tier 1: Official Documentation**
- `https://code.claude.com/docs/**` - Claude Code docs
- `https://github.com/**` - Official repositories
- `https://gist.github.com/**` - Official gists
- Tool/framework official documentation sites

**Tier 2: Community Resources**
- Stack Overflow (for specific problems)
- Technical blogs (recent, authoritative)
- Tutorial sites (well-maintained)

**Tier 3: General Web**
- General search results
- Use only when Tier 1-2 insufficient
- Verify information quality carefully

### 3. Information Gathering

**For each source:**
1. Read thoroughly
2. Extract relevant information
3. Note source URL and description
4. Identify key points
5. Check publication date/relevance

**Cross-referencing:**
- Verify critical facts across 2+ sources
- Note version-specific information
- Flag contradictions for investigation
- Prefer recent over outdated

### 4. Synthesis

**Organize information:**
- Group related concepts
- Order from general to specific
- Identify patterns and relationships
- Extract key takeaways

**Quality checks:**
- Is it accurate?
- Is it complete for the query?
- Is it clearly presented?
- Are sources properly attributed?

## Formatting Standards

### Markdown Structure

**Headers:**
- H1 (`#`) - Title only
- H2 (`##`) - Major sections
- H3 (`###`) - Subsections if needed
- Keep hierarchy shallow (max 3 levels)

**Code blocks:**
```language
# Always specify language
# Include comments for clarity
```

**Lists:**
- Use bullets for unordered items
- Use numbers for sequential steps
- Keep items parallel in structure
- One idea per bullet point

**Emphasis:**
- **Bold** for key terms and important points
- *Italic* sparingly for subtle emphasis
- `Code font` for technical terms, commands, file names

### Source Attribution

**Format:**
```markdown
## Sources
- [URL] - [Brief description of what info came from this source]
```

**Best practices:**
- List in order of importance/relevance
- Keep descriptions concise (5-10 words)
- Include official docs first
- Don't duplicate similar sources

**Example:**
```markdown
## Sources
- https://code.claude.com/docs/hooks - Hook events and configuration
- https://github.com/example/repo/docs - Implementation examples
- https://blog.example.com/hooks-guide - Best practices guide
```

## Template Usage

### Simple Response Template

**Structure:**
1. Title (clear, specific)
2. Direct answer (1-3 paragraphs)
3. Code example (if applicable)
4. Sources (2-4 typically)

**Length:** 100-300 words plus code examples

**Tone:** Direct, practical, focused

### Detailed Response Template

**Structure:**
1. Title (descriptive, comprehensive)
2. Executive summary (2-3 sentences)
3. Overview section (context/background)
4. Topic sections (2-5 sections, organized logically)
5. Key takeaways (3-5 bullet points)
6. Sources (5-10 typically)

**Length:** 500-1500 words

**Tone:** Comprehensive, educational, organized

## Quality Standards

### Accuracy
- Cross-reference critical information
- Note version-specific details
- Flag assumptions or uncertainties
- Prefer official sources

### Completeness
- Answer the actual question asked
- Include necessary context
- Provide examples when helpful
- Cover edge cases if relevant

### Clarity
- Use simple, direct language
- Define technical terms
- Organize information logically
- Make content scannable

### Attribution
- Cite every source used
- Track where information came from
- Describe what each source contributed
- Link to original documentation

## Error Handling

### Insufficient Information
```
I found limited information about [topic]. Based on available sources:
[Present what was found]

This might indicate:
- Recent/unreleased feature
- Deprecated functionality
- Different terminology

Would you like me to search with alternative terms?
```

### Contradictory Sources
```
I found conflicting information:
- Source A: [X]
- Source B: [Y]

This appears to be due to [version/context/timing].
The most current information suggests: [recommendation]
```

### No Results
```
I couldn't find reliable sources for [topic].

Could you:
- Verify the terminology?
- Provide more context?
- Specify the tool/version?
```

## Related Files

- `templates.md` - Detailed template examples with full samples
- `search-strategies.md` - Advanced search techniques per domain
- `source-evaluation.md` - Criteria for assessing source quality
