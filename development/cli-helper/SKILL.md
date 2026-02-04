---
name: cli-helper
description: Use this skill when the user asks about CLI tool options, parameters, or flags. Activate when queries mention command-line tools, --help output, CLI documentation, or organizing tool parameters into levels. Helps parse and structure CLI help documentation into Basic, Medium, and Advanced complexity levels.
---

# CLI Helper Skill

Organize and parse command-line tool help documentation into three structured levels of complexity (Basic, Medium, Advanced).

## Purpose

This skill provides systematic guidance for working with command-line interface (CLI) tools by parsing and organizing their help documentation. It helps you understand CLI tool options by categorizing them into three levels based on usage frequency and complexity. This is particularly valuable for proprietary tools, complex utilities with extensive options, or any situation where accurate CLI parameter information is critical.

## When to Use This Skill

Activate this skill when:

- The user asks about CLI tool options, parameters, or flags
- The user needs to parse or organize `--help` output
- Working with complex CLI tools that have many options
- The user requests categorization of CLI options by complexity
- Queries mention specific CLI tools (e.g., "ffmpeg", "kubectl", "grep", "dataproc")
- The user wants to create reference documentation for a CLI tool

## Bundled Resources

This skill follows the progressive disclosure principle with three resource types:

### References (`references/`)

Documentation loaded into context as needed to inform the CLI documentation process.

**Included references:**

- `references/template.md` - Template for creating new CLI tool reference documentation
- `references/example-tool.md` - Example reference for a fictional DataProc CLI tool showing proper structure

**Note:** Reference files demonstrate the three-level organization system and proper categorization techniques.

## How to Use This Skill

### Three-Level Organization System

Organize CLI options into three complexity levels:

**Level 1: Basic**
- Essential options for most common tasks
- Help, version, and basic operations
- Simple flags with clear, single purposes
- Minimal dependencies on other options
- Examples: `--help`, `--version`, `--output FILE`

**Level 2: Medium (Commonly Used)**
- Options used in typical workflows
- Configuration, formatting, and filtering options
- Used regularly but not universally
- May have some option dependencies
- Examples: `--format FORMAT`, `--verbose`, `--config FILE`

**Level 3: Advanced (Complex Cases)**
- Specialized options for complex scenarios
- Performance tuning, debugging, edge cases
- Often require multiple parameters or complex syntax
- MUST include concrete usage examples
- Examples: `--parallel NUM`, `--memory-limit SIZE`, `--custom-function`

### Categorization Criteria

Categorize options based on:

1. **Usage frequency indicators**: Keywords like "common", "basic" in help text
2. **Complexity**: Number of parameters, dependencies on other options
3. **Purpose keywords**: Terms like "debug", "advanced", "experimental" → Level 3
4. **Common sense**: What typical users need first vs. what specialists need

### Basic Workflow: Parse CLI Help Output

**Task 1: Parse a CLI Tool's Help**

1. Execute the tool's help command: `tool-name --help` or `tool-name -h`
2. Analyze the output for option patterns and descriptions
3. Categorize each option into Basic, Medium, or Advanced levels
4. Structure the information using clear headings and descriptions

**Task 2: Create Reference Documentation**

1. Use the template from `references/template.md`
2. Fill in the three-level structure with categorized options
3. Add concrete examples for all Advanced options
4. Save to `references/tool-name.md` for future reference

**Task 3: Organize Existing Reference**

1. Read the tool's existing reference file from `references/`
2. Present the information in the three-level structure
3. Help the user find options appropriate for their task

## Key Information

Important details about this skill:

- **Organization system**: Three levels (Basic, Medium, Advanced)
- **Reference location**: `references/` directory for pre-parsed tools
- **Template**: `references/template.md` provides the structure
- **Line limits**: Keep reference files under 500 lines (max 1000 lines)
- **Examples required**: Advanced options MUST have concrete usage examples

## Categorization Guidelines

### Level 1: Basic - Criteria

Include options that:
- Are used in >80% of common use cases
- Have single, clear purposes without complex interactions
- Are essential for getting started with the tool
- Include help, version, and basic I/O options

### Level 2: Medium - Criteria

Include options that:
- Are used in typical workflows but not universally
- Involve configuration, customization, or formatting
- May have some dependencies but are still straightforward
- Appear in standard tutorials and common examples

### Level 3: Advanced - Criteria

Include options that:
- Are used in specialized or complex scenarios
- Require deep understanding of the tool
- Often combine with other options
- Include performance tuning, debugging, or edge cases
- MUST provide concrete examples showing actual usage

## Best Practices

- Categorize based on usage frequency, not just technical complexity
- Always provide concrete examples for Advanced options (never hypothetical)
- Keep descriptions focused on WHEN to use each option, not just WHAT it does
- Use clear, scannable headings for easy navigation
- Note option interactions and warnings where relevant
- Keep reference files under 500 lines when possible (max 1000 lines)

## Common Workflows

### Workflow 1: Parse New CLI Tool

1. Run `tool-name --help` to get the help output
2. Identify all available options and flags
3. Group related options together
4. Categorize each option into Basic, Medium, or Advanced
5. Write descriptions focusing on when to use each option
6. Add concrete examples for Advanced options
7. Save to `references/tool-name.md`

### Workflow 2: Answer User Query About CLI Tool

1. Check if a reference exists in `references/` for the tool
2. If exists, read the reference and present relevant level(s)
3. If not exists, execute `--help` and parse on-the-fly
4. Organize the response by complexity level
5. Offer to save the structured information for future use

### Workflow 3: Update Existing Reference

1. Read the current reference from `references/`
2. Parse new help output if tool version changed
3. Update categorization if needed
4. Add any new options to appropriate levels
5. Ensure Advanced options have concrete examples

## Troubleshooting

**Issue: Unsure which level an option belongs to**

- Check help text for keywords: "common", "basic" → Level 1; "advanced", "debug" → Level 3
- Consider usage frequency: used in >80% of cases → Level 1; <20% → Level 3
- Look at parameter complexity: simple flag → Level 1; requires multiple params → Level 3
- When in doubt, start with Medium and adjust based on user feedback

**Issue: Option seems to fit multiple levels**

- Prioritize usage frequency over technical complexity
- If truly borderline, choose the lower level (more accessible)
- Note cross-references if an option is relevant to multiple scenarios

**Issue: Reference file exceeds line limits**

- Split into multiple files (e.g., `tool-basic.md`, `tool-advanced.md`)
- Move detailed examples to separate example files
- Use more concise descriptions while maintaining clarity
- Consider if some rarely-used options can be omitted

## Additional Notes

Important considerations:

- **Proprietary tools**: This skill is especially valuable for internal/proprietary CLI tools not widely documented
- **Reference library**: Build a collection of pre-parsed documentation for frequently-used tools
- **Consistent structure**: Always follow the three-level organization for consistency
- **Real examples**: Never use hypothetical examples in Advanced sections; show actual working commands
- **Context awareness**: Consider the user's skill level when presenting information

## Writing Style

- Use imperative/infinitive form (verb-first instructions) throughout
- Focus on practical usage: "Run this command to..." vs. "This command can be run to..."
- Emphasize WHEN to use options, not just WHAT they do
- Keep descriptions concise but informative
- Use active voice for clarity
