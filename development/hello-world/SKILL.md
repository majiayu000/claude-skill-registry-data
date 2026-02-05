---
name: hello-world
description: A simple example skill that demonstrates the basic structure of a Claude Skill, including scripts, references, and best practices. Use this as a learning template when creating new skills.
---

# Hello World Skill

This is a simple example skill that demonstrates the fundamental structure and components of a Claude Skill.

## Overview

The Hello World skill provides a minimal working example of:
- YAML frontmatter configuration
- Markdown-based instructions
- Bundled Python scripts
- Reference documentation
- Clear usage patterns

## Usage

This skill can be triggered with queries like:
- "Run the hello world skill"
- "Show me a greeting"
- "Test the example skill"

### Basic Greeting

To generate a simple greeting, use the bundled script:

```python
python scripts/greet.py
```

### Custom Greetings

The script supports custom names:

```python
python scripts/greet.py --name "Alice"
```

## Bundled Resources

### Scripts

**`scripts/greet.py`** - A simple Python script that generates customizable greetings.

Features:
- Default greeting message
- Custom name support via command-line argument
- Clean, documented code

Usage examples:
```bash
# Basic greeting
python scripts/greet.py

# Custom name
python scripts/greet.py --name "Bob"

# Help
python scripts/greet.py --help
```

### References

**`references/greeting_guidelines.md`** - Best practices for creating effective greetings.

This reference is loaded only when needed, demonstrating progressive disclosure:
- Keeps main SKILL.md lean
- Provides detailed information on demand
- Reduces context window usage

## Best Practices Demonstrated

This skill showcases several Claude Skill best practices:

1. **Concise frontmatter** - Only required fields (name, description)
2. **Clear structure** - Well-organized sections with purpose
3. **Executable resources** - Scripts for deterministic tasks
4. **Progressive disclosure** - References loaded as needed
5. **Practical examples** - Real usage patterns shown

## When to Use This Pattern

Use this skill structure as a template when creating skills that:
- Have deterministic, repeatable operations
- Benefit from executable scripts
- Need reference documentation
- Should minimize context usage

## Extending This Skill

To build upon this example:

1. Replace `greet.py` with your own scripts
2. Update `greeting_guidelines.md` with domain-specific knowledge
3. Modify frontmatter description to match your use case
4. Add assets if needed for output generation

Remember: Only include information Claude doesn't already know. Keep it concise!
