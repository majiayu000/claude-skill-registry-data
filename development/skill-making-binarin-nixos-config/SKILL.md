---
name: skill-making
description: Creates and refines Claude agent skills following best practices. Use when creating new skills, improving existing ones, or learning about skill structure and conventions.
---

# Skill Making

This skill helps you create high-quality Claude agent skills that follow established best practices and conventions.

**CRITICAL: All skill files MUST use Unix line endings (LF, \n) only. Never use Windows line endings (CRLF, \r\n).**

## When to Create a Skill

Create a skill when:
- You've refined an approach through repeated use and want consistent application
- Quality requires specific materials (templates, examples, domain knowledge)
- Task involves complex multi-piece setups requiring coordinated requirements
- You want to package expertise for automatic activation

Don't create a skill for:
- One-off exploratory tasks
- Simple tasks better handled by regular prompting
- General preferences (use Custom Instructions instead)
- Accumulated context over time (use Projects instead)

## Skill Discovery Context

**Important**: Skills stored in `~/.claude/skills/` may be symlinked from other locations (e.g., `files/claude-skills` in version-controlled repos). When using tools like `find` to discover skills:
- Use `find -L` to follow symbolic links
- Or search in the actual source directory
- Standard `find` won't follow symlinks by default

## File Structure

```
skill-name/
├── SKILL.md           (required: main instructions)
├── REFERENCE.md       (optional: domain knowledge)
├── EXAMPLES.md        (optional: input/output examples)
└── scripts/           (optional: utility scripts)
    └── validator.py
```

## SKILL.md Format

Every SKILL.md requires YAML frontmatter plus markdown body:

```markdown
---
name: skill-name
description: What this skill does and when to use it (max 1024 chars)
---

# Skill Name

[Instructions for Claude in markdown]
```

### YAML Frontmatter Requirements

**`name`** (required):
- Maximum 64 characters
- Lowercase letters, numbers, hyphens only
- Use gerund form (verb + "-ing"): `processing-pdfs`, `analyzing-spreadsheets`
- Avoid: `helper`, `utils`, reserved words containing "anthropic" or "claude"
- No XML tags

**`description`** (required):
- Maximum 1024 characters
- Write in third person
- Be specific about functionality AND usage triggers
- Include key terms that match user intent
- Good: "Extracts text and tables from PDFs, fills forms, merges documents. Use when working with PDF files."
- Bad: "Helps with documents" (too vague)
- No XML tags

## Content Best Practices

### Conciseness
"The context window is a public good." Only include information Claude doesn't already know. Challenge every element: does it justify its token cost?

### Progressive Disclosure
- Keep SKILL.md under 500 lines
- Move advanced content to separate files (REFERENCE.md, EXAMPLES.md)
- Reference files load only when Claude needs them
- Keep references one level deep from SKILL.md

### File Organization Patterns

**High-level guide with references:**
```markdown
For detailed procedures, see FORMS.md.
For API specifications, see REFERENCE.md.
For examples, see EXAMPLES.md.
```

**Domain-specific organization:**
```
reference/finance.md
reference/sales.md
reference/legal.md
```

**Conditional details:**
```markdown
For advanced error handling, see [advanced-errors.md](advanced-errors.md).
```

### Reference File Guidelines
- Use forward slashes in paths (not backslashes)
- Include table of contents for files over 100 lines
- Keep one level deep from SKILL.md

### Terminology Consistency
Choose one term and use it consistently:
- Don't mix: "field/box/element" or "extract/pull/get"
- Consistent terminology helps Claude understand

### Freedom Levels

Match specificity to task requirements:

**High freedom** (flexible approaches):
- Text-based instructions
- Multiple valid approaches
- Creative or analytical work

**Medium freedom** (preferred patterns):
- Pseudocode
- Structured workflows
- Some flexibility needed

**Low freedom** (precise execution):
- Specific scripts
- Fragile operations
- Consistency critical

## Workflows for Complex Tasks

Structure multi-step operations with explicit checklists:

```markdown
## Review Process

Copy this checklist and mark items as you complete them:

- [ ] Run validator on input
- [ ] Fix any validation errors
- [ ] Generate output
- [ ] Validate output format
- [ ] Confirm all requirements met
```

### Feedback Loop Pattern
```markdown
1. Run validator script
2. Review errors
3. Fix issues
4. Repeat until validation passes
```

## Scripts and Code

### Utility Scripts
Provide pre-made scripts for:
- Reliability (complex operations)
- Efficiency (repeated tasks)
- Consistency (fragile operations)

Clearly distinguish:
- **Execution**: "Run analyze_form.py with input file"
- **Reference**: "See analyze_form.py for the algorithm"

### Error Handling
"Handle error conditions rather than punting to Claude."

```python
try:
    result = process_data(input)
except ValidationError as e:
    # Provide meaningful alternative
    result = handle_validation_error(e)
except Exception as e:
    # Log and provide fallback
    log_error(e)
    result = safe_fallback()
```

### Self-Documenting Code
Justify all configuration values:

```python
# Good: explains the why
MAX_RETRIES = 3  # Balance between reliability and performance

# Bad: unexplained "voodoo constant"
MAX_RETRIES = 3
```

### Verifiable Outputs
For complex operations, create intermediate verifiable files:

```python
# Generate changes first
changes = analyze_input(data)
save_json(changes, "changes.json")

# User can review changes.json before applying
if validate_changes("changes.json"):
    apply_changes(changes)
```

## Templates and Examples

### Output Format Templates
Adjust strictness based on requirements:

**Mandatory** (for APIs):
```markdown
## Output Format (Required)

```json
{
  "field": "value",
  "items": []
}
```
```

**Flexible** (for analysis):
```markdown
## Output Format (Suggested)

Present findings in these sections:
- Summary
- Key insights
- Recommendations
```

### Example Patterns
Include input/output pairs demonstrating:
- Desired style
- Appropriate detail level
- Expected structure

```markdown
## Example

Input:
```
[concrete example input]
```

Output:
```
[expected output showing style and detail]
```
```

## Avoiding Time-Sensitive Information

Don't use date-based conditions:
```markdown
<!-- Bad -->
As of 2024, use method A. Before 2024, use method B.

<!-- Good -->
Use method A (current approach).

<details>
<summary>Legacy patterns</summary>
Method B was used in older versions...
</details>
```

## Anti-Patterns to Avoid

❌ Offering excessive options: "Use pypdf, pdfplumber, PyMuPDF, or..."
✅ Provide default with escape hatch: "Use pypdf. For special cases requiring X, consider Y."

❌ Windows-style paths: `scripts\validator.py`
✅ Unix-style paths: `scripts/validator.py` (works everywhere)

❌ Abstract examples: "For a document like X, do Y"
✅ Concrete examples: Actual input/output pairs

❌ Vague descriptions: "Helps with documents"
✅ Specific descriptions: "Extracts text and tables from PDFs, fills forms"

❌ Inconsistent terminology: field/box/element mixed
✅ Consistent terminology: Use "field" throughout

## Development Workflow

### 1. Design Phase
Use one Claude instance to design and refine the skill:
- Discuss requirements
- Draft SKILL.md structure
- Create examples and scripts
- Iterate on content

### 2. Testing Phase
Test with a separate Claude instance:
- Start fresh chat (no design context)
- Use real tasks that should trigger the skill
- Observe: Does it activate? Does it work correctly?

### 3. Observation Points
Monitor for:
- Unexpected navigation paths
- Missed connections between sections
- Overreliance on specific sections
- Ignored content

### 4. Refinement
Return to design instance:
- Report observations
- Adjust content based on behavior
- Clarify unclear sections
- Add missing connections

### 5. Evaluation
Build test scenarios:
- Establish baseline (no skill)
- Measure with skill
- Document improvements
- Create at least 3 evaluations

## Cross-Model Testing

Test skills across all Claude models:
- **Haiku**: Fast, efficient, good for straightforward tasks
- **Sonnet**: Balanced capability and speed
- **Opus**: Maximum capability for complex tasks

Effectiveness varies by model capability. Ensure skills work acceptably across all three.

## Final Verification Checklist

Before considering a skill complete:

- [ ] Description is specific with key terms and usage triggers
- [ ] No time-sensitive information (no dates, no "current" references)
- [ ] Consistent terminology throughout
- [ ] Concrete examples with input/output pairs
- [ ] File references are one level deep
- [ ] Forward slashes in all paths
- [ ] Scripts handle errors explicitly
- [ ] All required packages listed and available
- [ ] At least 3 test scenarios created
- [ ] Tested across Haiku, Sonnet, and Opus
- [ ] SKILL.md under 500 lines
- [ ] All files use Unix line endings (LF only)

## Skill Locations by Platform

**Claude.ai**: Upload via Settings > Features as zip files

**Claude API**: Upload through Skills API (`/v1/skills`)
- Requires beta headers: `code-execution-2025-08-25`, `skills-2025-10-02`, `files-api-2025-04-14`
- No network access
- No runtime package installation

**Claude Code**: Filesystem-based
- Project or personal directories
- Full network access
- Avoid global package installation

**Agent SDK**: `.claude/skills/` configuration directories

## Activation Mechanism

Skills use progressive disclosure with three tiers:

1. **Metadata always loads**: YAML frontmatter (~100 tokens per skill)
2. **Instructions load when triggered**: Full SKILL.md when description matches user intent
3. **Resources load as needed**: Referenced files only when Claude accesses them

Only relevant content occupies context window at any time.

## Resources

- [Claude Skills Overview](https://support.claude.com/en/articles/12580051-teach-claude-your-way-of-working-using-skills)
- [Creating Skills with Claude](https://support.claude.com/en/articles/12599426-how-to-create-a-skill-with-claude-through-conversation)
- [Skills Technical Overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)
- [Skills Best Practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- [Skills Cookbooks (GitHub)](https://github.com/anthropics/claude-cookbooks/tree/main/skills)
