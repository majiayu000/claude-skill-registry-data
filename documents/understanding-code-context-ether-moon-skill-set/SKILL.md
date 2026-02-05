---
name: understanding-code-context
description: Use when understanding external libraries, frameworks, or dependencies - provides workflows for finding and reading official documentation via Context7 instead of web search or source code reading
---

# Understanding Code Context

## Overview

**Core principle**: Use official documentation (Context7) to understand external libraries and frameworks instead of web search or reading source code.

This skill provides structured workflows for finding authoritative, version-specific documentation for external dependencies.

## When to Use

Use this skill when:
- Understanding how an external library/framework works
- Learning library concepts, patterns, and APIs
- Finding official documentation for dependencies
- Understanding library configuration and usage patterns

Don't use for:
- Exploring project code (use other tools)
- Finding implementations in your codebase
- Simple file content reading

## Context7 Tool Usage

**Primary tool**: Context7 provides authoritative, version-specific documentation for external libraries.

### Commands

```bash
# Step 1: Find library ID
resolve-library-id "library-name"

# Step 2: Get documentation
get-library-docs context7CompatibleLibraryID="/org/project"
```

### Search Strategy

When searching for library documentation, try multiple variations:

1. **Exact package name**: `"importmap-rails"`
2. **Framework + concept**: `"rails import maps"`
3. **Organization/repo**: `"rails/importmap"`
4. **Base name**: `"importmap"`

**Important**: Try 2+ variations before using WebSearch. Context7 has official, version-specific documentation. WebSearch gives you blog posts and outdated StackOverflow.

## Core Workflow

**Understanding External Library:**

```
1. resolve-library-id "library-name"
   - If not found: try variations (framework + concept, org/repo, base name)
   - Try 2+ variations before giving up
2. get-library-docs context7CompatibleLibraryID="/org/project"
3. Read and understand official patterns, APIs, and concepts
4. Apply understanding to project usage
```

**Example:**
```markdown
User: "Help me understand how importmap works and how to add a new library"

You:
1. resolve-library-id "importmap-rails"
   - If not found: try "rails/importmap", "rails import maps", "importmap"
2. get-library-docs context7CompatibleLibraryID="/rails/importmap"
3. Understand: import maps spec, pin vs pin_all_from, CDN vs vendor
4. Explain concepts and how to add a new library based on official docs
```

## Red Flags - STOP Immediately

If you catch yourself doing ANY of these, STOP and start over:

- ❌ "Context7 didn't work" after 1 try (try 2+ search term variations!)
- ❌ "WebSearch is faster" (it's less accurate and often outdated!)
- ❌ "I know how this lib works" (check official docs anyway!)
- ❌ Reading source code before checking Context7 docs
- ❌ Using WebSearch before trying Context7 variations

**All of these mean: STOP. Try Context7 with multiple search variations first.**

## Anti-Patterns

**Common mistakes:**

| Mistake | Fix |
|---------|-----|
| **WebSearch first** | Use Context7 with multiple search term variations |
| **One search term only** | Try 2+ variations (exact name, framework+concept, org/repo, base name) |
| **Reading source code** | Check Context7 official docs first |
| **Assuming library behavior** | Official docs explain intent, best practices, and gotchas |

**Why Context7 over WebSearch:**
- Official, version-specific documentation
- Authoritative patterns and APIs
- Up-to-date information
- Explains intent and best practices

## Quick Reference

**Find library documentation:**
```bash
resolve-library-id "library-name"
get-library-docs context7CompatibleLibraryID="/org/project"
```

**Search term variations to try:**
1. Exact package name: `"package-name"`
2. Framework + concept: `"framework concept"`
3. Organization/repo: `"org/repo"`
4. Base name: `"basename"`
