---
name: code-documentation
description: Updates project documentation in markdown files when requested. Use when the user asks to update, modify, or create project documentation such as README files, API docs, architecture docs, or other markdown documentation files.
allowed-tools: Read, Grep, Glob, Edit, Write
---

# Code Documentation Skill

## Purpose
This skill handles all requests to update, modify, or create project documentation. It is restricted to markdown (.md) files only and cannot modify code files or other file types.

## Instructions

### 1. Identify Documentation Files
- Use Glob to find existing markdown files in the repository
- Common documentation locations:
  - Root directory (README.md, CLAUDE.md, CONTRIBUTING.md, etc.)
  - `/docs` directory
  - `/src/Hosts/*/README.md` (per-application documentation)
  - Project-specific documentation folders

### 2. Analyze Current Documentation
- Read the relevant markdown file(s) to understand existing content
- Identify sections that need updates
- Preserve existing formatting, structure, and style
- Maintain consistency with other documentation in the project

### 3. Update Documentation
- Use Edit tool for modifying existing markdown files
- Use Write tool only for creating new markdown files
- Ensure changes align with the project's documentation standards
- Include proper markdown formatting (headers, code blocks, lists, etc.)

### 4. Writing Style Guidelines
- **Be straightforward and concise** - Get to the point quickly
- **Avoid verbosity** - Remove unnecessary words and filler content
- **No fluff** - Skip introductory phrases like "It's worth noting that" or "As you can see"
- **Focus on essential information** - Include only what the reader needs to know
- **Use clear, direct language** - Prefer simple words over complex ones
- **Keep explanations minimal** - Provide enough detail to understand, nothing more
- **Avoid over-explaining** - Trust the reader's technical knowledge
- **Use bullet points and lists** - Make information scannable
- **Short paragraphs** - Break up text for readability

### 5. Validation Rules
- **ONLY modify .md files** - Never update code files, configuration files, or other file types
- Preserve existing documentation structure and hierarchy
- Use consistent markdown formatting throughout
- Include code examples in proper fenced code blocks with language identifiers
- Update table of contents if present

## Examples

### Example 1: Update README
User: "Update the README to include information about the new authentication feature"
- Locate README.md in repository root
- Read current contents
- Add new section about authentication feature
- Preserve existing format and style

### Example 2: Create API Documentation
User: "Document the PlayHub SignalR endpoints in the docs folder"
- Check if /docs directory exists
- Create new markdown file (e.g., SignalR-API.md)
- Structure with proper headers and code examples
- Follow existing documentation patterns

### Example 3: Update Architecture Docs
User: "Add details about the new CQRS command to the architecture documentation"
- Find architecture documentation (CLAUDE.md or /docs/architecture.md)
- Read existing CQRS section
- Add new command documentation
- Maintain consistency with existing command examples

## Restrictions
- **File Type Restriction**: Only .md (markdown) files can be created or modified
- **No Code Changes**: This skill does NOT modify source code files
- **No Configuration Changes**: This skill does NOT modify appsettings, docker-compose, or other config files
- If user requests documentation for code changes, document in markdown only - do not modify the code itself

## Tools Available
- **Read**: Read existing markdown files to understand current content
- **Grep**: Search for specific documentation sections or patterns
- **Glob**: Find markdown files across the repository
- **Edit**: Modify existing markdown files
- **Write**: Create new markdown files (use sparingly - prefer editing existing docs)
