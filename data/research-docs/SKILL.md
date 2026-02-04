---
name: research-docs
description: Research and persist coding documentation using Perplexity AI. Use when user asks about documentation, APIs, frameworks, libraries, best practices, coding patterns, or needs to research technical topics. Always checks existing research first.
allowed-tools: Read, Write, Bash, Grep, Glob
---

# Documentation Research Skill

Research coding documentation efficiently using Perplexity AI and persist findings in a structured, AI-optimized format.

## Core Principles

1. **Check Existing Research First** - Always read `research/CLAUDE.md` (memory index) to see if topic was researched before
2. **Structured Persistence** - Save all research to `research/<topic>.md` with consistent formatting
3. **AI-Optimized Output** - Use clear sections, code examples, and structured data
4. **Documentation Focus** - Prioritize official docs, GitHub repos, and authoritative sources
5. **Memory-Based Index** - `research/CLAUDE.md` is a Claude Code memory file that auto-loads to provide research context

## research/CLAUDE.md Format

The `research/CLAUDE.md` file is a **Claude Code memory file** that follows these best practices:

**Memory Best Practices** (from Claude Code documentation):
- ✓ **Be specific**: "Use 2-space indentation" not "Format code properly"
- ✓ **Use structure**: Format as bullet points under descriptive headings
- ✓ **Stay scannable**: Clear sections, consistent formatting
- ✓ **Review periodically**: Update as research evolves

**Index Entry Format:**
```markdown
### <Topic Name> (`<topic>.md`)

**Researched:** YYYY-MM-DD
**Status:** Active | Deprecated | Updated
**When to Use:** Specific concrete scenarios (be detailed)
**Summary:**
- Specific actionable point 1
- Specific actionable point 2
- Specific actionable point 3
```

This format ensures:
- Claude can quickly scan for relevant research
- Entries are specific and actionable
- Research context loads automatically in every session
- Index serves as a memory aid across sessions

## Workflow

### Step 1: Check Existing Research

**ALWAYS start by checking if we've researched this topic before:**

```bash
# Read the research index
cat research/CLAUDE.md
```

Look for the topic in the research index. If found, read the existing research file:

```bash
cat research/<topic>.md
```

If the research exists and is recent (< 3 months old), use it. Otherwise, proceed to Step 2.

### Step 2: Identify Research Topic

Determine the specific topic to research. Create a clean topic name:

- Use lowercase with hyphens
- Be specific but concise
- Examples: `python-asyncio`, `react-hooks`, `typescript-generics`, `docker-best-practices`

### Step 3: Execute Perplexity Search

Use the optimized research script with appropriate parameters:

```bash
# Basic documentation research
.claude/skills/research-docs/scripts/perplexity-research.sh "python asyncio best practices"

# Target specific domains
.claude/skills/research-docs/scripts/perplexity-research.sh -d "docs.python.org,realpython.com" "python async await"

# Recent documentation only
.claude/skills/research-docs/scripts/perplexity-research.sh -r month "react 19 new features"

# More comprehensive results
.claude/skills/research-docs/scripts/perplexity-research.sh -n 20 "rust ownership patterns"
```

**Script Options:**
- `-n, --max-results NUM`: Number of results (1-20, default: 15)
- `-r, --recency FILTER`: day, week, month, year (default: year)
- `-d, --domains LIST`: Comma-separated domain list
- `-f, --format FORMAT`: structured (default), json, plain

### Step 4: Create Structured Documentation

Save the research output to `research/<topic>.md` using this format:

```markdown
# <Topic Name>

**Research Date:** YYYY-MM-DD
**Status:** Active | Deprecated | Updated
**Related Topics:** topic1, topic2, topic3

## Overview

Brief 2-3 sentence overview of the topic.

## Key Concepts

- **Concept 1**: Explanation
- **Concept 2**: Explanation
- **Concept 3**: Explanation

## Official Documentation

- [Primary Docs](<url>) - Description
- [API Reference](<url>) - Description

## Best Practices

### Do's

- ✓ Practice 1 with brief explanation
- ✓ Practice 2 with brief explanation

### Don'ts

- ✗ Anti-pattern 1 with brief explanation
- ✗ Anti-pattern 2 with brief explanation

## Common Patterns

### Pattern 1: <Name>

**Use Case:** When to use this pattern

**Example:**
```language
// Code example
```

**Explanation:** Why this works

### Pattern 2: <Name>

**Use Case:** When to use this pattern

**Example:**
```language
// Code example
```

**Explanation:** Why this works

## Common Pitfalls

### Pitfall 1: <Name>

**Problem:** Description of the issue

**Solution:**
```language
// Correct approach
```

### Pitfall 2: <Name>

**Problem:** Description of the issue

**Solution:**
```language
// Correct approach
```

## Integration Examples

### Basic Setup

```language
// Installation or basic setup
```

### Advanced Usage

```language
// More complex example
```

## Version Information

- **Current Stable:** Version number
- **Minimum Required:** Version number
- **Deprecated Features:** List any deprecated features

## Related Resources

- [Resource 1](<url>) - Description
- [Resource 2](<url>) - Description

## Research Sources

<Paste the Perplexity research output here>

---

**Last Updated:** YYYY-MM-DD
**Next Review:** YYYY-MM-DD (3 months from research date)
```

### Step 5: Update research/CLAUDE.md Index

**ALWAYS update research/CLAUDE.md** with an entry for the research.

The `research/CLAUDE.md` file is a **memory file** that Claude Code automatically loads. It serves as an index of all researched topics.

**Format Guidelines** (following Claude Code memory best practices):
- ✓ **Be specific**: Include concrete details, not vague descriptions
- ✓ **Use structure**: Format as bullet points under descriptive headings
- ✓ **Stay scannable**: Use clear sections and consistent formatting
- ✓ **Update regularly**: Keep status and dates current

Add a new entry under the "Research Index" heading:

```markdown
### <Topic Name> (`<topic>.md`)

**Researched:** YYYY-MM-DD
**Status:** Active
**When to Use:** Specific scenarios where this applies (be concrete)
**Summary:**
- Key point 1 with specific detail
- Key point 2 with specific detail
- Key point 3 with specific detail
```

**Example entry:**
```markdown
### Python Asyncio (`python-asyncio.md`)

**Researched:** 2025-11-18
**Status:** Active
**When to Use:** Building concurrent I/O-bound applications, async web servers, or async database operations
**Summary:**
- Use `asyncio.create_task()` for fire-and-forget, `asyncio.gather()` for concurrent execution with results
- Always use `async with` for async context managers to ensure proper cleanup
- Avoid blocking calls in async functions - use `asyncio.to_thread()` for CPU-bound work
```

### Step 6: Create TODO List

Use the TodoWrite tool to track research progress:

```json
[
  {"content": "Check existing research in research/CLAUDE.md", "status": "completed", "activeForm": "Checking existing research"},
  {"content": "Execute Perplexity search for <topic>", "status": "completed", "activeForm": "Executing Perplexity search"},
  {"content": "Structure documentation in research/<topic>.md", "status": "in_progress", "activeForm": "Structuring documentation"},
  {"content": "Update research/CLAUDE.md research index", "status": "pending", "activeForm": "Updating research/CLAUDE.md research index"}
]
```

## Documentation Categories

### Framework Documentation
- React, Vue, Angular, Svelte
- Next.js, Nuxt, SvelteKit
- Express, FastAPI, Django

### Language Documentation
- Python, JavaScript/TypeScript, Rust, Go
- Java, Kotlin, Swift
- Ruby, PHP, C#

### Tool Documentation
- Docker, Kubernetes
- Git, GitHub Actions
- Webpack, Vite, esbuild

### API Documentation
- REST API design
- GraphQL
- WebSockets

### Best Practices
- Code patterns
- Architecture patterns
- Security practices
- Performance optimization

## Output Quality Standards

### Must Include
- ✓ Clear, scannable structure
- ✓ Code examples for key concepts
- ✓ Links to official documentation
- ✓ Best practices and anti-patterns
- ✓ Version information
- ✓ Common pitfalls and solutions

### Avoid
- ✗ Large blocks of unformatted text
- ✗ Outdated information without version context
- ✗ Examples without explanation
- ✗ Missing links to sources
- ✗ Vague or generic advice

## Example Queries That Trigger This Skill

- "Research Python asyncio documentation"
- "Find best practices for React hooks"
- "Look up TypeScript generics documentation"
- "What are the latest Docker best practices?"
- "Research how to implement WebSockets in Node.js"
- "Find documentation on Rust error handling"
- "Look up GraphQL schema design patterns"

## Maintenance

### Updating Existing Research

When updating research:

1. Read the existing file
2. Add a note at the top: `**Updated:** YYYY-MM-DD - Reason for update`
3. Update the "Last Updated" date
4. Update the "Next Review" date
5. Update the research/CLAUDE.md entry with new date

### Deprecation

If documentation becomes outdated:

1. Update status to "Deprecated"
2. Add deprecation notice with replacement topic
3. Update research/CLAUDE.md status

## Troubleshooting

### Perplexity API Errors

**Error: API key invalid**
- Check `PERPLEXITY_API_KEY` environment variable
- Ensure you have a new API key that supports Search API

**Error: Rate limit exceeded**
- Wait before making additional requests
- Consider reducing result count with `-n` flag

### Research Quality Issues

**Too many irrelevant results**
- Use domain filtering: `-d "official-docs.com,github.com"`
- Make query more specific
- Adjust recency filter: `-r month`

**Missing official documentation**
- Explicitly include official domain in search query
- Use `-d` flag to target specific authoritative sources

## Best Practices

1. **Always check existing research first** - Avoid duplicate work
2. **Use specific queries** - "Python 3.12 asyncio patterns" vs "Python async"
3. **Target authoritative sources** - Use domain filtering for official docs
4. **Structure consistently** - Follow the documentation template
5. **Include examples** - Code examples make documentation actionable
6. **Update research/CLAUDE.md** - Keep the research index current
7. **Set review dates** - Mark when research should be refreshed
8. **Track with TODOs** - Use TodoWrite to show progress

## Script Reference

The `perplexity-research.sh` script is located at:
```
.claude/skills/research-docs/scripts/perplexity-research.sh
```

**Key Features:**
- Pre-configured for documentation domains
- AI-optimized structured output
- Flexible filtering options
- Error handling and validation
- Multiple output formats

**Default Documentation Domains:**
- stackoverflow.com
- github.com
- docs.python.org
- developer.mozilla.org
- nodejs.org
- reactjs.org
- vuejs.org
- angular.io
- rust-lang.org
- go.dev
- kotlinlang.org
- dev.to
- medium.com

Override with `-d` flag for specific research needs.
