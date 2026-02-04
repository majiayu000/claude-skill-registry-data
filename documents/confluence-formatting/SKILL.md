---
name: Confluence Formatting
description: This skill should be used when the user asks to "generate Confluence documentation", "create wiki markup", "format for Confluence", "convert to Confluence format", or when generating documentation that needs to be pasted into Atlassian Confluence. Provides expertise in Confluence wiki markup syntax, macros, and styling conventions.
---

# Confluence Wiki Markup Expertise

This skill provides knowledge for generating documentation in Atlassian Confluence wiki markup format.

## Core Syntax

### Headings

Use heading markers for document structure:

```
h1. Main Title
h2. Section Header
h3. Subsection
h4. Minor Section
h5. Detail Level
h6. Smallest Heading
```

### Text Formatting

Apply inline formatting:

- **Bold**: `*bold text*`
- **Italic**: `_italic text_`
- **Strikethrough**: `-strikethrough-`
- **Underline**: `+underline+`
- **Monospace**: `{{monospace}}`
- **Superscript**: `^superscript^`
- **Subscript**: `~subscript~`

### Lists

Create ordered and unordered lists:

```
* Bullet item
** Nested bullet
*** Deep nested

# Numbered item
## Nested number
### Deep nested
```

Mixed lists:

```
# First ordered
#* Bullet under ordered
#* Another bullet
# Second ordered
```

### Links

Format links appropriately:

- **External**: `[Link Text|https://example.com]`
- **Internal page**: `[Page Name]`
- **Anchor**: `[Link Text|#anchor-name]`
- **Email**: `[mailto:email@example.com]`

### Tables

Structure tabular data:

```
||Header 1||Header 2||Header 3||
|Cell 1|Cell 2|Cell 3|
|Cell 4|Cell 5|Cell 6|
```

## Essential Macros

### Code Block

Display code with syntax highlighting:

```
{code:language=python|title=Example Code|collapse=false}
def hello_world():
    print("Hello, World!")
{code}
```

Supported languages: python, java, javascript, typescript, bash, sql, xml, json, yaml, csharp, go, rust

### Info Panel

Highlight informational content:

```
{info:title=Note}
Important information for the reader.
{info}
```

### Warning Panel

Alert readers to cautions:

```
{warning:title=Caution}
Be careful when performing this action.
{warning}
```

### Note Panel

Add supplementary notes:

```
{note:title=Remember}
Keep this in mind while proceeding.
{note}
```

### Tip Panel

Provide helpful suggestions:

```
{tip:title=Pro Tip}
This approach saves time.
{tip}
```

### Expand/Collapse

Create collapsible sections:

```
{expand:title=Click to expand}
Hidden content that appears when expanded.
{expand}
```

### Table of Contents

Generate automatic TOC:

```
{toc:printable=true|style=disc|maxLevel=3|indent=20px}
```

### No Format

Preserve whitespace and prevent wiki rendering:

```
{noformat}
Preformatted text
    with preserved spacing
        and no wiki parsing
{noformat}
```

### Panel

Create bordered content panels:

```
{panel:title=Panel Title|borderStyle=solid|borderColor=#ccc|bgColor=#f5f5f5}
Panel content here.
{panel}
```

## Document Structure Patterns

### API Reference Pattern

Structure API documentation consistently:

```
h1. API Reference

{toc:maxLevel=2}

h2. Overview

Brief description of the API.

h2. Authentication

{code:language=bash}
curl -H "Authorization: Bearer TOKEN" https://api.example.com
{code}

h2. Endpoints

h3. GET /resource

{info}
Retrieves a list of resources.
{info}

*Parameters:*
||Name||Type||Required||Description||
|limit|integer|No|Maximum results to return|
|offset|integer|No|Starting position|

*Response:*
{code:language=json}
{
  "data": [],
  "total": 0
}
{code}
```

### Architecture Document Pattern

Structure system architecture docs:

```
h1. System Architecture

{toc}

h2. Overview

Brief system description.

h2. Components

h3. Component Name

*Purpose:* What this component does.

*Dependencies:*
* Dependency 1
* Dependency 2

*Interfaces:*
||Interface||Protocol||Description||
|API|REST|External access|
|Events|Kafka|Async messaging|

h2. Data Flow

{info}
Describe how data moves through the system.
{info}

h2. Deployment

{code:language=yaml|title=Deployment Configuration}
service:
  replicas: 3
  memory: 2Gi
{code}
```

### Getting Started Pattern

Structure onboarding documentation:

```
h1. Getting Started

{tip}
This guide takes approximately 15 minutes to complete.
{tip}

h2. Prerequisites

* Prerequisite 1
* Prerequisite 2

h2. Installation

{code:language=bash}
npm install package-name
{code}

h2. Quick Start

h3. Step 1: Configure

{code:language=json|title=config.json}
{
  "setting": "value"
}
{code}

h3. Step 2: Initialize

{code:language=javascript}
const client = new Client(config);
{code}

h3. Step 3: Verify

{info}
Run the verification command to confirm setup.
{info}

h2. Next Steps

* [Advanced Configuration]
* [API Reference]
* [Troubleshooting]
```

## Best Practices

### Readability

- Use headings to create clear hierarchy
- Keep paragraphs short (3-5 sentences)
- Use lists for sequential steps or related items
- Add whitespace between sections

### Code Presentation

- Always specify language for syntax highlighting
- Add titles to code blocks for context
- Use collapse for long code examples
- Include comments in code samples

### Visual Hierarchy

- Use panels to highlight important content
- Apply info/warning/tip macros appropriately
- Create tables for structured data
- Use expand macros for optional detail

### Navigation

- Include table of contents for long documents
- Use anchor links for cross-references
- Create consistent heading structure
- Link to related pages

## Output File Convention

Generate Confluence wiki files with `.wiki` extension:

- `api-reference.wiki`
- `architecture.wiki`
- `getting-started.wiki`

Files should be plain text containing wiki markup, ready for copy-paste into Confluence page editor (switch to wiki markup mode).
