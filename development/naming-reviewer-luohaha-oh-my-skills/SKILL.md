---
name: naming-reviewer
description: "Expert code naming review and refactoring. Reviews variables, functions, and classes to improve readability and maintainability using master-level naming principles. Use when: (1) User asks to review naming/variable names in code, (2) User wants to improve code readability, (3) User requests naming suggestions or refactoring, (4) User mentions code quality or maintainability concerns related to naming, (5) User asks to apply best practices to naming"
---

# Naming Reviewer

Expert-level code naming review that analyzes variables, functions, and classes, then applies master programming principles to improve readability and maintainability.

## Workflow

### 1. Identify Target Code

Ask the user to specify what code to review:
- Specific files or directories
- Code snippets pasted directly
- Recent changes (git diff)
- Entire modules or packages

### 2. Load Naming Principles

Before reviewing, load the comprehensive naming guidelines:
- Read `references/naming-principles.md` for master-level naming principles
- Read `references/antipatterns.md` for common mistakes to detect

These references contain detailed examples and language-specific conventions.

### 3. Analyze Code

Systematically review all identifiers in the specified code:

**Variables:**
- Are names descriptive and reveal intent?
- Do they follow language conventions (camelCase, snake_case)?
- Are collections properly pluralized?
- Are booleans named with appropriate prefixes (is, has, can)?
- Are magic numbers replaced with named constants?

**Functions/Methods:**
- Do names clearly describe the action?
- Are verbs specific rather than generic (avoid process, handle, manage)?
- Do queries use appropriate prefixes (get, find, is)?
- Are parameters clearly named?

**Classes:**
- Do names use descriptive nouns?
- Are they specific rather than generic (avoid Manager, Handler)?
- Do they follow language conventions (PascalCase)?

**General:**
- Is vocabulary consistent across similar concepts?
- Are names appropriately sized for their scope?
- Are abbreviations avoided or justified?
- Is redundant context removed?

### 4. Detect Antipatterns

Cross-reference findings with `references/antipatterns.md` to identify:
- Generic verbs (process, handle, manage)
- Type encodings (strName, intCount)
- Abbreviation soup (usr, msg, btn)
- Negative booleans (notActive, disabled)
- Magic numbers and strings
- Inconsistent vocabulary
- Overly long or cryptic names

### 5. Consider Project-Specific Rules

**Check for project conventions:**
- Read any existing style guides in the project
- Observe patterns in existing code
- Ask user about specific naming preferences
- Respect established patterns unless they're clearly problematic

**Common project-specific considerations:**
- Domain-specific terminology (e.g., medical, financial, scientific terms)
- Established abbreviations (e.g., "API", "URL", "ID")
- Team conventions for certain patterns
- Framework-specific naming requirements

### 6. Generate Refactored Code

**Directly produce refactored code with:**
- All naming improvements applied
- Comments explaining significant renames
- Consistent style throughout
- Preserved functionality

**Format:**
```language
# Original code snippet for reference
[original code]

# Refactored code with improved naming
[refactored code]

# Summary of changes:
- oldName → newName: [reason]
- ...
```

### 7. Explain Improvements

For each significant rename, provide:
- **What changed:** Old name → New name
- **Why:** Reference specific principle or antipattern
- **Impact:** How it improves readability/maintainability

**Example:**
```
process() → parseJsonAndValidate()
  Why: Generic verb "process" doesn't reveal intent. New name describes specific actions.
  Principle: Use specific verbs over generic ones (naming-principles.md, section 4)
```

## Handling Edge Cases

### Mixed Languages
If code mixes languages (e.g., JavaScript and Python), apply appropriate conventions to each:
- Python: snake_case for functions/variables
- JavaScript: camelCase for functions/variables
- Both: PascalCase for classes

### Legacy Code
When reviewing established codebases:
- Prioritize consistency with existing patterns over "perfect" naming
- Suggest gradual refactoring for major issues
- Note if project-wide changes are needed (mention in summary)

### Domain-Specific Terms
Respect specialized terminology:
- Medical: ICD, CPT, EMR (standard abbreviations)
- Finance: APR, EBITDA, P&L
- Scientific: pH, ATP, DNA
- Ask user to confirm unfamiliar domain terms

### Ambiguous Cases
When multiple valid approaches exist:
- Present options with trade-offs
- Recommend the clearer, more common approach
- Defer to user preference if both are reasonable

## Output Format

**Structure your response as:**

1. **Executive Summary:**
   - Total issues found
   - Severity breakdown (critical/moderate/minor)
   - Overall code quality assessment

2. **Refactored Code:**
   - Complete refactored version of the code
   - Inline comments for major changes
   - Preserved functionality

3. **Detailed Changes:**
   - Organized by file/section
   - Each change with rationale
   - References to principles/antipatterns

4. **Recommendations:**
   - Patterns to adopt going forward
   - Project-wide issues that need attention
   - Suggested coding standards (if none exist)

## Quality Standards

**Every rename should:**
- Make the code more self-documenting
- Reduce need for explanatory comments
- Follow established language conventions
- Maintain or improve consistency
- Be justified by principle or antipattern

**Avoid:**
- Renaming for the sake of renaming
- Breaking established project patterns without strong reason
- Over-engineering simple, clear names
- Imposing personal preferences over established conventions

## Resources

- **naming-principles.md**: Comprehensive guide to master-level naming practices
- **antipatterns.md**: Common naming mistakes and how to fix them

Load these before beginning any review to ensure comprehensive, consistent analysis.
