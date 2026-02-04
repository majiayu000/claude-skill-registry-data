---
name: finwiz-documentation
description: "Standards for creating, organizing, and maintaining technical documentation in FinWiz using the Diátaxis framework. Use when writing docs, organizing content, or establishing documentation workflows."
allowed-tools: ["Read", "Edit", "Bash"]
---

# FinWiz Documentation Standards

Comprehensive standards for creating, organizing, and maintaining technical documentation in the FinWiz project using the Diátaxis framework.

## Documentation Architecture

### Diátaxis Framework (Required)

Organize all documentation using four categories:

| Type | Purpose | Location | When to Use |
|------|---------|----------|-------------|
| **Tutorials** | Learning by doing | `docs/tutorials/` | Step-by-step learning |
| **How-to Guides** | Solving problems | `docs/how-to/` | Specific problem solving |
| **Reference** | Information lookup | `docs/reference/` | API docs, CLI commands |
| **Explanation** | Understanding concepts | `docs/explanations/` | Architecture, principles |

### Content Decision Tree

Ask yourself:
1. **Is it step-by-step learning?** → Tutorial
2. **Is it solving a specific problem?** → How-to Guide  
3. **Is it reference information?** → Reference
4. **Otherwise** → Explanation

### Directory Structure

```
docs/
├── index.md                    # Main entry point
├── tutorials/
│   ├── getting_started.md
│   └── first_analysis.md
├── how-to/
│   ├── setup_environment.md
│   └── configure_crews.md
├── reference/
│   ├── api/
│   ├── cli_commands.md
│   └── schemas/
└── explanations/
    ├── architecture.md
    └── flow_patterns.md
```

## File Organization Standards

### Naming Conventions

- **Files**: `snake_case.md` (consistent with Python codebase)
- **Directories**: `kebab-case/` (URL-friendly paths)
- **One concept per file**: Each major topic gets its own file
- **Descriptive names**: `portfolio_analysis_guide.md` not `guide.md`

### Content Structure Requirements

**Every documentation file must include:**

1. **Clear H1 title** (only one per file)
2. **Purpose statement** in first paragraph
3. **Logical H2/H3 hierarchy**
4. **Code examples** with proper syntax highlighting
5. **Cross-references** using relative links

### Document Template

```markdown
# Document Title

Brief description of what this document covers and who should read it.

## Prerequisites

- Required knowledge
- System requirements
- Dependencies

## Main Content

### Section 1

Content with examples...

### Section 2

More content...

## Next Steps

- Links to related documentation
- Suggested follow-up actions

## References

- External links
- Related internal docs
```

## Writing Style Standards

### Voice and Tone

- **Active voice**: "Configure the API key" not "The API key should be configured"
- **Present tense**: "The application connects" not "The application will connect"
- **Direct address**: "You can configure" not "One can configure"
- **Professional but approachable**: Friendly without being casual

### Language Guidelines

- **Use simple, common words**: use, help, show vs utilize, facilitate, demonstrate
- **Keep sentences concise**: Aim for 15-20 words
- **Be specific**: "Set timeout to 30 seconds" not "Set appropriate timeout"
- **Consistent terminology**: Use same terms throughout (API key, not access key)

### Code Examples

- **Always specify language** for syntax highlighting
- **Include comments** for clarity
- **Show expected output** when helpful
- **Use consistent prompt symbols**: `$` for user commands

```python
# ✅ GOOD: Clear example with comments
def analyze_stock(ticker: str) -> StockAnalysis:
    """Analyze stock with proper error handling."""
    if not ticker:
        raise ValueError("Ticker cannot be empty")
    
    return StockAnalysis(ticker=ticker)
```

## Content Templates

### Tutorial Template

```markdown
# Tutorial Title

Brief description of what the user will learn and accomplish.

## Prerequisites

- Requirement 1
- Requirement 2

## What You'll Learn

By the end of this tutorial, you'll be able to:

- [ ] Learning objective 1
- [ ] Learning objective 2

## Step 1: [Action Verb] [Object]

Explanation of what we're doing and why.

```bash
# Code example with explanation
command --option value
```

Expected output:
```
Output example
```

## Step 2: [Next Action]

Continue with clear, sequential steps...

## Next Steps

- Link to related tutorials
- Link to how-to guides for advanced topics
```

### How-to Guide Template

```markdown
# How to [Accomplish Specific Task]

Brief description of the problem this guide solves.

## Prerequisites

- Requirement 1
- Requirement 2

## Method 1: [Approach Name] (Recommended)

### When to Use

Describe scenarios where this method is best.

### Steps

1. **Action 1**: Detailed instruction
   ```bash
   command example
   ```

2. **Action 2**: Next instruction

### Verification

How to confirm the task was completed successfully.

## Troubleshooting

Common problems and solutions.
```

### Reference Template

```markdown
# [Component/API/Tool] Reference

Comprehensive reference for [component name].

## Quick Reference

| Item | Description | Example |
|------|-------------|---------|
| Item 1 | Description | `example` |

## Parameters/Options

| Parameter | Type | Required | Description | Default |
|-----------|------|----------|-------------|---------|
| param1 | string | Yes | Description | - |

## Examples

### Basic Example

```python
# Code example with explanation
example_code()
```
```

## Quality Assurance

### Content Quality Checklist

- [ ] **Technical accuracy**: All code examples work
- [ ] **Current information**: No outdated references
- [ ] **Complete coverage**: All necessary information included
- [ ] **Clear objectives**: User knows what they'll accomplish
- [ ] **Logical flow**: Information in sensible order
- [ ] **Actionable content**: User can follow instructions

### Validation Tools

```bash
# Markdown linting
make docs-lint

# Link validation  
make docs-validate

# Build validation
make docs-build
```

## Integration with Codebase

### Inline Documentation

Follow Python docstring standards:

```python
def analyze_portfolio(holdings: list[Holding]) -> PortfolioAnalysis:
    """
    Analyze portfolio holdings and generate recommendations.
    
    Args:
        holdings: List of portfolio holdings to analyze
        
    Returns:
        PortfolioAnalysis with recommendations and risk assessment
        
    Raises:
        ValidationError: If holdings data is invalid
        APIError: If external data sources are unavailable
    """
```

### Schema Documentation

All Pydantic models must include field descriptions:

```python
class StockAnalysis(BaseModel):
    ticker: str = Field(..., description="Stock ticker symbol (e.g., AAPL)")
    recommendation: str = Field(..., description="BUY, HOLD, or SELL")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence level 0-1")
```

## Anti-Patterns to Avoid

❌ **Monolithic files** - Split large documents into focused files
❌ **Generic titles** - Use specific, descriptive headings  
❌ **Untested code** - All examples must be verified
❌ **Broken links** - Validate all cross-references
❌ **Inconsistent terminology** - Use standard FinWiz terms
❌ **Missing context** - Always explain prerequisites
❌ **Outdated examples** - Keep code examples current

## Documentation Workflow

### Creating New Documentation

1. **Determine type** using Diátaxis framework
2. **Choose appropriate template**
3. **Write content** following style guidelines
4. **Add code examples** with proper syntax highlighting
5. **Validate links** and references
6. **Test all code examples**
7. **Review for clarity** and completeness

### Updating Existing Documentation

1. **Check for accuracy** against current codebase
2. **Update examples** to match current APIs
3. **Fix broken links** and references
4. **Improve clarity** based on user feedback
5. **Validate changes** don't break other docs

Remember: **Good documentation is code**. It should be maintained with the same rigor as the codebase itself.