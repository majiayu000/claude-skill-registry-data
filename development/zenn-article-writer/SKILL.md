---
name: zenn-article-writer
description: Write technical articles for Zenn in Oikon's distinctive writing style. This skill should be used when creating articles about AI tools, development workflows, tool integrations, updates/new features, or technical reports. The skill provides detailed writing guidelines, article structure patterns, and reference materials based on Oikon's existing articles.
---

# Zenn Article Writer

## Overview

Write technical articles for Zenn that match Oikon's writing style and structure. This skill provides comprehensive guidelines for creating engaging technical content with a casual yet professional tone, clear structure, and practical examples.

## When to Use This Skill

Use this skill when:

- Writing articles about AI tools (Claude Code, Codex, CodeRabbit, etc.)
- Explaining development workflows and practical implementations
- Describing tool integrations and ecosystem setups
- Reporting on updates, new features, or version releases
- Creating technical reports with hands-on experience
- Needing to match Oikon's established writing style and tone

## Article Writing Process

Follow this workflow to create well-structured articles:

### 1. Define Article Type and Scope

Identify which pattern best fits the article:

- **Workflow explanation**: Step-by-step processes with tools and services
- **Update/feature explanation**: Version releases and new functionality
- **Tool integration**: Connecting multiple tools and services
- **Tool review**: Introduction and evaluation of new tools

### 2. Gather Required Information

Collect necessary materials before writing:

- Personal experience and background context
- Tool/service names and links
- Screenshots, diagrams, or workflow visualizations
- Code examples, commands, and configuration files
- Reference links to official documentation
- Related tweets, slides, or external content

### 3. Create Article Structure

Outline the article based on the selected pattern (see `references/article-structure.md`):

- Start with personal introduction and motivation
- Present overall workflow or concept with visual aids
- Break down into clear, numbered steps
- Include concrete examples and commands
- Provide tips, warnings, and personal insights
- Conclude with summary and key takeaways

### 4. Write with Oikon's Style

Apply the distinctive writing characteristics (see `references/writing-style.md`):

- Use casual but professional tone
- Share personal experiences and trial-and-error processes
- Include humble acknowledgments of limited experience
- Provide multiple options with personal comparisons
- Add screenshots and visual aids generously
- Present concrete commands and code examples
- Emphasize practical usability

### 5. Add Metadata and Closing

Complete the article with proper metadata and closing sections:

- Set appropriate frontmatter (title, emoji, topics, publish date)
- Write concise summary revisiting key points
- Include X (Twitter) follow invitation
- List all referenced links in bibliography

## Writing Guidelines

### Article Structure Patterns

Reference `references/article-structure.md` for detailed structure patterns:

- **Workflow explanation pattern**: Overall workflow → Step details → Summary
- **Update explanation pattern**: Overview → Feature details → Overall impression
- **Tool integration pattern**: Overall flow → Prerequisites → Setup steps → Usage
- **Tool review pattern**: Overview → Features → Usage examples → Comparison → Summary

### Writing Style Characteristics

Reference `references/writing-style.md` for detailed style guidelines:

- **Casual and approachable tone**: Technical content with conversational language
- **Experience-based introduction**: Start with personal background and context
- **Humble stance**: Acknowledge limited experience and respect readers
- **Clear structure**: Use `##` and `###` headings for scannable content
- **Visual aids**: Include screenshots, diagrams, and workflow visualizations
- **Concrete examples**: Provide actual commands, code, and configuration
- **Personal insights**: Share comparisons, opinions, and lessons learned

### Zenn-Specific Formatting

Use Zenn's markdown features effectively:

- Frontmatter with title, emoji, type, topics, published, published_at
- `:::message` blocks for important notes and warnings
- Image sizing: `![alt text](/images/folder/file.png =400x)`
- External link embedding (tweets, slides, etc.)
- Code blocks with language specification

## Templates and References

### Article Template

Use `assets/zenn-template.md` as the starting point for new articles. Copy this template and customize:

- Update frontmatter with appropriate metadata
- Fill in personal introduction and background
- Structure content based on selected pattern
- Add actual content, examples, and visuals
- Complete summary and closing sections

### Style Reference

Consult `references/writing-style.md` for:

- Detailed tone and voice guidelines
- Structural conventions and best practices
- Do's and Don'ts for writing
- Image and link handling
- Section-specific writing approaches

### Structure Reference

Consult `references/article-structure.md` for:

- Complete article pattern templates
- Section-by-section writing guidance
- Example phrases and structures
- Article writing checklist

### Example Articles

Review `references/example-articles.md` for:

- Real excerpts from Oikon's published articles
- Pattern-specific examples
- Introduction and conclusion variations
- Concrete demonstration of style guidelines

## Key Principles

Remember these core principles when writing:

1. **Share real experiences**: Base content on actual trials and implementations
2. **Provide actionable guidance**: Include concrete steps readers can follow
3. **Balance casual and professional**: Maintain approachability without sacrificing quality
4. **Use visuals generously**: Support explanations with screenshots and diagrams
5. **Show comparisons**: Present multiple approaches with personal assessments
6. **Acknowledge limitations**: Be honest about experience level and constraints
7. **Enable reproducibility**: Include all necessary commands, configs, and links
8. **Respect the reader**: Assume expertise while providing helpful context

## Resources

### references/writing-style.md
Comprehensive documentation of Oikon's writing style, including tone, structure, explanatory approaches, and detailed Do's and Don'ts. Load this when needing guidance on voice, formatting conventions, or stylistic decisions.

### references/article-structure.md
Complete article structure patterns for different article types, with section-by-section templates and writing guidance. Reference this when planning article organization or needing structure-specific examples.

### references/example-articles.md
Real excerpts from Oikon's published articles demonstrating each pattern type. Consult this when needing concrete examples of introductions, explanations, or closing sections.

### assets/zenn-template.md
Blank article template with proper frontmatter and structural skeleton. Copy this file as the starting point for new articles and fill in with actual content following the style guidelines.
