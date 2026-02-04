---
name: github-formatter
description: Formats and styles content for professional GitHub presentation. Use when the user asks to style files for GitHub, format documentation, improve markdown presentation, or prepare repository for publishing. Applies clean, consistent GitHub-flavored markdown.
allowed-tools: Read, Write, Edit, Glob, Task
---

# GitHub Formatter Skill

This skill formats and styles content for professional, polished presentation on GitHub.

## When to Use

Use this skill when the user:
- Asks to format files for GitHub
- Wants to style documentation professionally
- Requests README improvements
- Needs consistent markdown formatting
- Wants to prepare repository for publishing or sharing
- Asks to make content "look good on GitHub"

## What This Skill Does

1. **Identifies Files** to format:
   - Specific files user mentions
   - All markdown files in repository
   - README files specifically
   - Documentation needing polish

2. **Invokes the github-stylist Subagent** to apply:
   - Consistent GitHub-flavored markdown (GFM)
   - Strategic emoji usage (purposeful, not excessive)
   - Proper heading hierarchy (H1 → H2 → H3)
   - Formatted code blocks with language specification
   - Navigation links between related files
   - Table of contents for long documents
   - Visual breaks and spacing
   - Professional tables and lists
   - Callouts and blockquotes for important info

3. **For README Files** specifically:
   - Compelling introduction
   - Clear repository structure
   - Visual hierarchy with sections
   - Badges if appropriate
   - Quick start guide
   - Usage instructions
   - Contributing and contact sections
   - License information

4. **Ensures Consistency** across all files:
   - Same emoji usage patterns
   - Uniform heading styles
   - Matching code block formatting
   - Consistent link styles
   - Professional appearance throughout

## Styling Principles

- **Clean and Professional**: Not cluttered or over-styled
- **Strategic Emoji**: 🎯 📚 💡 ✅ (one per major section max)
- **Scannable**: Easy to skim with clear hierarchy
- **Consistent**: Same patterns throughout repository
- **Mobile-Friendly**: Renders well on all devices
- **Linked**: Easy navigation between files

## What Gets Formatted

- Heading hierarchy and structure
- Code block syntax highlighting
- Table formatting and alignment
- List consistency (bullets vs. numbers)
- Emoji placement (strategic only)
- Link styles (relative for internal)
- Blockquotes for callouts
- Horizontal rules for visual breaks

## Example Usage

User: "Make all the markdown files look professional for GitHub"

This skill will apply consistent, professional styling across all repository files.
