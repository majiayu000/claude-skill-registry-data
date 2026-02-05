---
# IMPORTANT: Skill name must contain only lowercase letters, numbers, and hyphens
# Must start and end with a letter or number (not a hyphen)
# Valid: my-skill, pdf-helper, cli-helper, docker2k8s
# Invalid: My-Skill, my_skill, my-skill-, -my-skill
# Test locally: ./scripts/validate-skill-name.sh
name: your-skill-name
description: This skill should be used when the user asks about [X], needs to [Y], or mentions [Z]. Use when queries involve [key terms, file types, specific actions]. Be specific about trigger words and scenarios.
---

# Your Skill Name

**Note:** This template follows Anthropic's skill-creator best practices. Use imperative/infinitive form (verb-first instructions) throughout.

## Purpose

[2-3 sentences] Explain what this skill does and why it's useful. Be specific about the problems it solves.

Example: "This skill provides tools and workflows for rotating, cropping, and editing PDF documents. It simplifies PDF manipulation tasks that would otherwise require re-writing the same code repeatedly."

## When to Use This Skill

This skill should be used when:

- The user asks about [specific topic]
- The user needs to [specific action]
- Working with [specific files/formats]
- Queries mention [key terms]

Example:

- The user asks to rotate, edit, or manipulate PDF files
- The user needs to perform batch operations on PDFs
- Working with PDF documents that require structural changes
- Queries mention "PDF", "rotate", "crop", "merge", or "split"

## Prerequisites

List any requirements or setup needed:

- Required tools (e.g., Python 3.6+, jq, etc.)
- Required files or configuration
- Environment setup
- Permissions needed

Example: "Requires Python 3.8+ with PyPDF2 library installed. Install with: `pip install PyPDF2`"

## Bundled Resources

This skill follows the progressive disclosure principle with three resource types:

### Scripts (`scripts/`)

Executable code for tasks requiring deterministic reliability or frequently rewritten.

**When to include:** When the same code is repeatedly rewritten or deterministic behavior is needed.

**Included scripts:**

- `scripts/example_script.py` - [Description of what it does]

**Usage:**

```bash
python scripts/example_script.py --option value
```

### References (`references/`)

Documentation loaded into context as needed to inform Claude's process.

**When to include:** For detailed documentation, schemas, API specs, policies, or domain knowledge.

**Included references:**

- `references/example_reference.md` - [Description of what it contains]

**Note:** Keep SKILL.md lean; move detailed information to reference files. For large files (>10k words), include grep search patterns in this section.

### Assets (`assets/`)

Files used in output, not loaded into context (templates, images, boilerplate).

**When to include:** When the skill needs files for the final output.

**Included assets:**

- `assets/example_asset.txt` - [Description of what it's used for]

**Usage:** Copy, modify, or reference these assets in the output produced.

## How to Use This Skill

Provide clear, actionable instructions using imperative form. Reference bundled resources where appropriate.

### Basic Workflow

**Task 1: [Common Task]**

1. Run the script: `python scripts/example_script.py --input file.pdf`
2. Verify the output in the specified directory
3. Handle any errors using the troubleshooting guide below

**Task 2: [Another Task]**

1. Read the reference documentation: `references/example_reference.md`
2. Apply the workflow to the user's specific case
3. Use assets from `assets/` as needed

### Advanced Workflow

**Task 3: [Complex Task]**

1. Combine multiple scripts for batch processing
2. Reference advanced patterns in `references/advanced.md`
3. Customize asset templates for specific use cases

## Key Information

Important details about the skill:

- **Tool/Library:** Name and version
- **File locations:** Where files are stored
- **Output format:** What format output is provided
- **Limitations:** What the skill cannot do

Example:

- **Tool/Library:** PyPDF2 v3.0+
- **Input:** PDF files from any location
- **Output:** Modified PDF files in the same directory or specified output path
- **Limitations:** Cannot edit PDF content (text/images), only structural operations

## Troubleshooting

Common errors and solutions using imperative form:

**Error: [Error Message]**

- **Cause:** [Why this occurs]
- **Solution:** [How to fix]
  1. Check [specific condition]
  2. Run [specific command]
  3. Verify [expected outcome]

**Error: [Another Error]**

- **Cause:** [Why this occurs]
- **Solution:** [How to fix]

## Best Practices

- Use [specific approach] for [specific scenario]
- Avoid [anti-pattern] because [reason]
- Prefer [better approach] over [alternative]
- Test [what to test] before [what depends on it]

## Additional Notes

Important considerations:

- Edge cases or special scenarios
- Performance considerations
- Security implications
- Related tools or resources
- When to use alternative approaches

## Examples

**Note:** Remove this section or provide real examples. Avoid hypothetical placeholders.

Reference actual files in the skill directory:

- See `examples/sample-input.txt` for input format
- See `examples/expected-output.txt` for expected results
- See `assets/template.html` for the output template structure
