---
name: implementation-guidance-generator
description: Generates structured implementation guidance documents for technical issues, bug fixes, and feature development. Use when creating actionable implementation plans with file references, code locations, and step-by-step approaches following Obsidian markdown formatting standards.
---

# Implementation Guidance Generator

## Overview

This skill enables the creation of comprehensive implementation guidance documents that follow specific formatting standards for technical tasks. It transforms issue descriptions into actionable implementation plans with proper file references, code locations, and structured approaches.

## Quick Start

To generate implementation guidance:

1. **Request Linear URL** - Ask the user for the Linear issue URL (e.g., `https://linear.app/workspace/issue/PROJ-123`)
2. **Retrieve issue from Linear** - Use Linear MCP tools to fetch complete issue details including title, description, labels, status, and comments
3. **Identify affected files** - Analyze the issue description and codebase to determine which files need modification
4. **Generate structured guidance** - Create implementation guidance following the specified format
5. **Apply formatting standards** - Ensure proper Obsidian markdown formatting and GitHub links

## Implementation Guidance Generation Process

### Step 1: Request and Retrieve Linear Issue

**Ask the user for the Linear URL:**

- Request the full Linear issue URL (format: `https://linear.app/[workspace]/issue/[ISSUE-ID]`)
- Extract the issue identifier from the URL (e.g., PROJ-123)

**Use Linear MCP to retrieve issue details:**

- Use the `mcp__linear_get-issue` tool with the issue ID to fetch:
  - **Issue identifier** - The unique Linear issue ID (e.g., PROJ-123)
  - **Title** - Issue title/summary
  - **Description** - Full issue description with technical details
  - **Labels** - Any labels or tags applied to the issue
  - **Status** - Current issue status
  - **Priority** - Issue priority level
  - **Comments** - Any relevant comments or discussion
  - **Project** - The project/team the issue belongs to

**Extract key technical details:**

- **Technical problem description** - Core issue that needs to be resolved
- **Expected behavior** - What the system should do after implementation
- **Current behavior** - What the system is doing incorrectly
- **Environment/context** - Any relevant technical constraints or dependencies from description and comments

### Step 2: Identify Implementation Approach

Determine the most likely solution approach:

* **Primary implementation approach** - Start with the most likely solution or entry point
* **File identification** - Locate specific files that need modification
* **Code analysis** - Identify the exact functions, classes, or methods involved
* **Dependency mapping** - Understand how changes might affect other parts of the system

### Step 3: Generate Implementation Guidance

Create guidance following this exact structure, incorporating the Linear issue details:

```markdown
# [Linear Issue ID]: [Issue Title]

**Linear Issue:** [PROJ-123](https://linear.app/workspace/issue/PROJ-123)
**Status:** [Issue Status] | **Priority:** [Issue Priority]

## Issue Description

[Full description from Linear, including any relevant context from comments]

## Implementation guidance

* The culprit for this is most likely `FunctionName.methodName` ([GitHub](https://github.com/[repo/path/file.ext]#L123)), which has the query:

```typescript
[Code example showing the problematic code]
```

* Alternative approach: modify `OtherService.method` ([GitHub](https://github.com/repo/path/other.ts#L42))
* [Additional context and implementation notes]
```

### Step 4: Apply Formatting Standards

Ensure all generated guidance follows these requirements:

**Content Structure:**
1. **Primary implementation approach** - Most likely solution or entry point
2. **Specific code locations** - GitHub links with exact file paths and line numbers
3. **Code examples** - Relevant code snippets with proper syntax highlighting
4. **Multiple approaches** - Alternative solutions when applicable
5. **Context and constraints** - Technical constraints or considerations

**Style Guidelines:**
- Use bullet points for clear, actionable steps
- Include GitHub links in format: `([GitHub](https://github.com/[repo/path/file.ext]#L123))`
- Reference functions/classes with backticks: `FunctionName.methodName`
- Use proper TypeScript syntax highlighting for code examples
- Be specific about file locations and line numbers
- Include explanatory context for recommended approaches

## File Structure Standards

### Document Naming Convention

When creating implementation guidance documents, follow this naming pattern:
```
yyyy-mm-dd [Linear Issue ID] [short description].md
```

**Examples:**
- `2025-10-24 PROJ-123 Fix authentication bug.md`
- `2025-10-24 FEAT-456 Add user registration feature.md`

**Guidelines:**
- Use ISO date format yyyy-mm-dd
- Include the Linear issue ID (e.g., PROJ-123)
- Keep descriptions concise (use the Linear issue title or a shortened version)
- Use sentence case for descriptions and filenames
- Include file extension `.md`
- Use spaces for multi-word descriptions

### Content Organization

Structure implementation guidance documents with:
- Clear hierarchy using standard markdown headings
- Code blocks with appropriate language highlighting
- Checklists for actionable items
- Internal links using `[[filename]]` format for related documents

## Resources

### scripts/
Contains executable code for generating implementation guidance documents:

- `generate_guidance.py` - Python script that parses issue content and generates structured implementation guidance following formatting standards

### references/
Contains documentation and reference material:

- `formatting_guidelines.md` - Complete formatting standards and style guidelines for implementation guidance documents

These resources provide both automated generation capabilities and detailed reference material for creating high-quality implementation guidance.
