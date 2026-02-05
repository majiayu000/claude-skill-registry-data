---
name: gathering-skills-examples
description: Real-time collection and analysis of Claude Skills examples from multiple sources including GitHub repositories, blog posts, documentation, and community discussions. Use this skill when the user requests to gather examples, use cases, best practices, or implementation patterns for Claude Skills. Generates comprehensive markdown reports summarizing collected examples.
---

# Gathering Skills Examples

## Overview

Collect and analyze real-world examples of Claude Skills from various online sources to provide up-to-date insights into how developers are using and implementing skills. Generate comprehensive markdown reports summarizing findings.

## When to Use This Skill

Use this skill when users request:
- "Find examples of Claude Skills being used in practice"
- "What are people building with Claude Skills?"
- "Show me real-world Claude Skills implementations"
- "Collect the latest Claude Skills tutorials and guides"
- "What are best practices for building Claude Skills?"

## Collection Workflow

### 1. Determine Collection Scope

Identify which information sources to search:
- **GitHub repositories**: Source code, implementation examples, open-source skills
- **Articles and blog posts**: Tutorials, guides, announcements, best practices
- **Community discussions**: Forums, Discord, Reddit, GitHub issues/discussions

### 2. Execute Collection Process

Use the bundled resources to efficiently gather examples:

**Search Patterns**: Reference `references/search_patterns.md` for effective search queries and keywords to use across different platforms.

**Information Sources**: Reference `references/sources.md` for a curated list of URLs and platforms where Claude Skills examples are commonly shared.

**Web Search**: Use WebSearch tool with queries from search patterns to find:
- Recent blog posts and articles
- Tutorial content
- Documentation updates
- Community discussions

**GitHub Search**: When GitHub examples are needed, search for:
- Repositories with "claude skills" or "claude-code"
- SKILL.md files in public repositories
- Example implementations and templates

### 3. Generate Report

Use `assets/report_template.md` as the base structure and populate with collected findings:
- Categorize examples by type (workflows, tools, integrations)
- Include source links and descriptions
- Highlight notable patterns and best practices
- Add timestamps for freshness context

## Bundled Resources

### references/search_patterns.md
Contains effective search queries and keywords for finding Claude Skills examples across different platforms. Load this file when determining what search queries to execute.

### references/sources.md
Curated list of URLs and platforms where Claude Skills examples are commonly shared (documentation sites, community forums, key GitHub organizations). Reference this when identifying where to search.

### assets/report_template.md
Markdown template for structuring the final report. Use this template as the base and populate with collected findings to ensure consistent, well-organized output.
