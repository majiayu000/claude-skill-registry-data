---
name: template-skill
description: A template for creating new skills. Use this as a starting point when creating your own skill. Replace all template content with your skill's specific information.
license: Apache 2.0
metadata:
  version: "1.0.0"
  author: "your-username"
  tags: ["template", "example"]
---

# Template Skill

This is a template for creating new skills. Copy this entire directory and modify it to create your own skill.

## Purpose

Explain the purpose of your skill. What problem does it solve? What capability does it add to Claude?

Example:
> This skill helps Claude [specific capability], making it easier to [specific benefit]. It's designed for use when [specific scenarios].

## When to Use This Skill

Be very explicit about when Claude should activate this skill. List specific trigger conditions:

- When the user asks to [specific task 1]
- When working with [specific technology, format, or domain]
- When [specific condition] is met
- For [specific use case]

**Do NOT use this skill when:**
- [Specific exclusion 1]
- [Specific exclusion 2]

## Prerequisites

List any prerequisites or requirements:

- Required knowledge: [e.g., Python programming, API design]
- Required tools: [e.g., specific CLI tools, libraries]
- Environment setup: [e.g., environment variables, configuration]

## Instructions

Provide clear, step-by-step instructions for Claude to follow. Be specific and actionable.

### Step 1: [First Major Step]

Detailed instructions for the first step:

1. Substep 1
2. Substep 2
3. Substep 3

**Example:**
```
[Code example or demonstration]
```

**Important considerations:**
- Point 1
- Point 2

### Step 2: [Second Major Step]

Detailed instructions for the second step.

### Step 3: [Third Major Step]

Continue with additional steps as needed.

## Examples

Provide concrete examples that demonstrate the skill in action.

### Example 1: [Scenario Name]

**User Request:**
> "..."

**Claude Response:**
1. [First action]
2. [Second action]
3. [Result]

**Output:**
```
[Example output]
```

### Example 2: [Another Scenario]

Provide multiple examples covering different use cases.

## Best Practices

List best practices Claude should follow when using this skill:

1. **Practice 1**: Explanation
2. **Practice 2**: Explanation
3. **Practice 3**: Explanation

## Common Pitfalls

Warn about common mistakes or issues:

- **Pitfall 1**: How to avoid it
- **Pitfall 2**: How to avoid it

## Constraints and Limitations

Document any constraints or limitations:

- This skill does not support [limitation 1]
- Maximum/minimum requirements: [constraint]
- Known issues: [issue description]

## Supporting Files

If your skill includes supporting files, document them here:

### scripts/

- `script_name.py`: Description of what this script does
- `requirements.txt`: Python dependencies

Usage:
```bash
python scripts/script_name.py [arguments]
```

### templates/

- `template_name.ext`: Description of this template
- Usage instructions

### reference/

- `reference_doc.md`: Additional reference material
- Links to external documentation

## Validation Checklist

Use this checklist to ensure your skill is complete:

- [ ] Skill name matches directory name (lowercase, hyphens only)
- [ ] YAML frontmatter is complete and valid
- [ ] Description clearly states what the skill does AND when to use it
- [ ] Instructions are clear and actionable
- [ ] Examples are provided and tested
- [ ] Supporting files are documented
- [ ] LICENSE.txt is included
- [ ] No hardcoded credentials or sensitive data
- [ ] Security best practices followed

## References

- Link to relevant documentation
- Link to API references
- Link to tutorials or guides
- Credit to original sources (if applicable)

---

## Customization Guide

When creating your skill from this template:

1. **Update frontmatter:**
   - Change `name` to match your skill's directory name
   - Write a comprehensive `description` (1-3 sentences)
   - Set appropriate `license`
   - Update `metadata` fields

2. **Replace all template content:**
   - Remove this "Customization Guide" section
   - Replace all bracketed placeholders [like this]
   - Provide real examples and instructions

3. **Structure your content:**
   - Keep sections that are relevant
   - Remove sections that don't apply
   - Add custom sections as needed

4. **Test thoroughly:**
   - Verify YAML frontmatter is valid
   - Test all examples
   - Ensure instructions are clear

5. **Document everything:**
   - Explain all supporting files
   - Document dependencies
   - Provide usage examples
