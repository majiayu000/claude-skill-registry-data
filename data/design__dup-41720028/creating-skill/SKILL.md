---
name: creating-skill
description: Guide for creating effective Claude Skills. Covers structure, naming, progressive disclosure, workflows, and best practices. Use when the user wants to create a new Skill, improve existing Skills, or learn Skill authoring patterns.
---

# Creating Skills

A comprehensive guide to authoring effective Claude Skills.

## Quick Start

To create a basic Skill:

1. Create a directory with your skill name (lowercase, hyphens only)
2. Create a `SKILL.md` file with YAML frontmatter:

```yaml
---
name: your-skill-name
description: What this Skill does and when to use it
---
```

3. Add instructions and examples in the markdown body
4. Test the Skill with Claude

That's it! For a minimal Skill, this is all you need.

## Core Principle 1: Concise is Key

**Default assumption**: Claude is already very smart. Only add context Claude doesn't have. 

### Example: Concise vs Verbose

**✓ Good: Concise** (50 tokens):

````markdown
## Extract PDF text

Use pdfplumber for text extraction:

```python
import pdfplumber
with pdfplumber.open("file.pdf") as pdf:
    text = pdf.pages[0].extract_text()
```
````

**✗ Bad: Too verbose** (150 tokens):

```markdown
## Extract PDF text

PDF (Portable Document Format) files are a common file format that contains
text, images, and other content. To extract text from a PDF, you'll need to
use a library. There are many libraries available for PDF processing, but we
recommend pdfplumber because it's easy to use and handles most cases well.
First, you'll need to install it using pip. Then you can use the code below...
```

The concise version assumes Claude knows what PDFs are and how libraries work.

## Core Principle 2: Set Appropriate Degrees of Freedom

Match specificity to task fragility. Think of Claude as a robot exploring a path:
- **Narrow bridge with cliffs**: Only one safe way forward → Use specific guardrails (low freedom)
- **Open field with no hazards**: Many paths lead to success → Give general direction (high freedom)

### High Freedom (Text Instructions)

Use when multiple approaches are valid:

```markdown
## Code review process

1. Analyze the code structure and organization
2. Check for potential bugs or edge cases
3. Suggest improvements for readability and maintainability
4. Verify adherence to project conventions
```

### Medium Freedom (Pseudocode/Parameters)

Use when a preferred pattern exists:

````markdown
## Generate report

Use this template and customize as needed:

```python
def generate_report(data, format="markdown", include_charts=True):
    # Process data
    # Generate output in specified format
```
````

### Low Freedom (Exact Scripts)

Use when operations are fragile:

````markdown
## Database migration

Run exactly this script:

```bash
python scripts/migrate.py --verify --backup
```

Do not modify the command or add additional flags.
````

## Skill Structure Requirements

Every Skill requires YAML frontmatter with two fields:

### name Field

**Requirements:**
- Maximum 64 characters
- Only lowercase letters, numbers, hyphens
- Cannot contain: XML tags, "anthropic", "claude"

**Good examples (gerund form):**
- `processing-pdfs`, `analyzing-spreadsheets`, `managing-databases`

**Avoid:**
- Vague: `helper`, `utils`, `tools`
- Generic: `documents`, `data`, `files`

### description Field

**Requirements:**
- Must be non-empty
- Maximum 1024 characters
- Write in third person (not "I" or "you")
- Include both WHAT it does and WHEN to use it

**✓ Good example:**
```yaml
description: Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDF files or when the user mentions PDFs, forms, or document extraction.
```

**✗ Bad example:**
```yaml
description: Helps with documents
```

## Progressive Disclosure: Organizing Content

Keep SKILL.md under 500 lines. Split content into reference files when needed.

### Pattern 1: High-Level Guide with References

Common operations in SKILL.md, detailed docs separate:

````markdown
## Quick start

Extract text with pdfplumber:

```python
import pdfplumber
with pdfplumber.open("file.pdf") as pdf:
    text = pdf.pages[0].extract_text()
```

## Advanced features

**Form filling**: See [FORMS.md](FORMS.md) for complete guide
**API reference**: See [REFERENCE.md](REFERENCE.md) for all methods
````

### Pattern 2: Domain-Specific Organization

For Skills covering multiple domains:

```
bigquery-skill/
├── SKILL.md (overview and navigation)
└── reference/
    ├── finance.md (revenue, billing metrics)
    ├── sales.md (opportunities, pipeline)
    └── product.md (API usage, features)
```

This keeps token usage low - Claude loads only the relevant domain.

### Critical Rule: One Level Deep

**✓ Good:** All reference files link directly from SKILL.md
**✗ Bad:** Reference files that link to other reference files

Claude may only partially read deeply nested files, missing critical information.

## Common Patterns

### Template Pattern

Provide templates matching your strictness needs:

**For strict requirements:**

````markdown
## Report structure

ALWAYS use this exact template:

```markdown
# [Analysis Title]

## Executive summary
[One-paragraph overview]

## Key findings
- Finding 1 with supporting data
- Finding 2 with supporting data
```
````

**For flexible guidance:**

````markdown
## Report structure

Here's a sensible default format, but use your best judgment:

```markdown
# [Analysis Title]

## Executive summary
[Overview]

## Key findings
[Adapt sections based on what you discover]
```
````

### Examples Pattern

For Skills where quality depends on seeing examples:

````markdown
## Commit message format

Generate commit messages following these examples:

**Example 1:**
Input: Added user authentication with JWT tokens
Output:

```
feat(auth): implement JWT-based authentication

Add login endpoint and token validation middleware
```

**Example 2:**
Input: Fixed bug where dates displayed incorrectly
Output:

```
fix(reports): correct date formatting in timezone conversion

Use UTC timestamps consistently across report generation
```
````

### Conditional Workflow Pattern

Guide Claude through decision points:

```markdown
## Document modification workflow

1. Determine the modification type:

   **Creating new content?** → Follow "Creation workflow" below
   **Editing existing content?** → Follow "Editing workflow" below

2. Creation workflow:
   - Use docx-js library
   - Build document from scratch

3. Editing workflow:
   - Unpack existing document
   - Modify XML directly
   - Validate after each change
```

## Key Anti-Patterns to Avoid

### 1. Windows-Style Paths

**✓ Good:** `python scripts/helper.py`, `[link](reference/guide.md)`
**✗ Bad:** `python scripts\helper.py`, `[link](reference\guide.md)`

Unix-style paths (`/`) work everywhere. Windows-style (`\`) only work on Windows.

### 2. Too Many Options

**✗ Bad:** "You can use pypdf, or pdfplumber, or PyMuPDF, or pdf2image, or..."

**✓ Good:** "Use pdfplumber for text extraction. For scanned PDFs requiring OCR, use pdf2image with pytesseract instead."

Provide one default that handles 80% of cases. Mention alternatives only when they solve different problems.

### 3. Time-Sensitive Information

**✗ Bad:** "If you're doing this before August 2025, use the old API."

**✓ Good:** Use "Old patterns" section with `<details>` tags:

```markdown
## Current method

Use the v2 API endpoint: `api.example.com/v2/messages`

## Old patterns

<details>
<summary>Legacy v1 API (deprecated 2025-08)</summary>

The v1 API used: `api.example.com/v1/messages`

This endpoint is no longer supported.

</details>
```

### 4. Inconsistent Terminology

**✗ Bad:** Mix "API endpoint", "URL", "API route", "path", "API address"

**✓ Good:** Choose one term and use it throughout (e.g., always "API endpoint")

### 5. Assuming Tools Are Installed

**✗ Bad:** "Use the pdf library to process the file."

**✓ Good:** "Install required package: `pip install pdfplumber`"

Always show installation commands explicitly.

## Complete Example

Here's a well-structured minimal Skill:

````markdown
---
name: processing-pdfs
description: Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDF files or when the user mentions PDFs, forms, or document extraction.
---

# PDF Processing

## Quick Start

Extract text with pdfplumber:

```python
import pdfplumber
with pdfplumber.open("file.pdf") as pdf:
    text = pdf.pages[0].extract_text()
```

## Extract Tables

```python
with pdfplumber.open("file.pdf") as pdf:
    table = pdf.pages[0].extract_table()
```

## Advanced Features

**Form filling**: See [FORMS.md](FORMS.md) for complete guide
**API reference**: See [REFERENCE.md](REFERENCE.md) for all methods
````

## Deep Dive: Reference Documentation

For detailed information on specific topics, see these reference files:

**[Core Principles](reference/core-principles.md)** - Detailed exploration of conciseness and degrees of freedom with more examples

**[Skill Structure](reference/structure.md)** - Complete YAML requirements, naming conventions, description writing checklist

**[Document Organization](reference/organization.md)** - All progressive disclosure patterns, file splitting strategies, refactoring tips

**[Workflows & Feedback Loops](reference/workflows.md)** - Multi-step processes, checklists, validation loops, complex workflows

**[Common Patterns](reference/patterns.md)** - All patterns: templates, examples, conditionals, configuration, error handling

**[Anti-Patterns](reference/anti-patterns.md)** - Complete list of what to avoid with detailed explanations

**[Advanced: Executable Code](reference/advanced.md)** - Utility scripts, visual analysis, verifiable outputs, MCP tools, runtime environment