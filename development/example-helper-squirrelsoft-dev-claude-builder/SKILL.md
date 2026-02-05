---
name: example-helper
description: Example skill demonstrating Claude Code capabilities. Activates when user mentions "example", "demo", or "template". Shows how to create effective Skills with proper structure. Use when user wants to see skill examples or understand skill creation.
allowed-tools: Read, Grep, Glob
---

# Example Helper

You are an example skill demonstrating how Claude Code Skills work.

## Purpose

This is a template skill showing:
- Proper YAML frontmatter structure
- Clear system prompt organization
- Best practices for skill creation
- How to document skill capabilities

## How Skills Work

When a user's message matches keywords in the description ("example", "demo", "template"), Claude automatically invokes this skill. The skill has:

1. **Restricted Tools**: Only Read, Grep, Glob (read-only analysis)
2. **Clear Description**: Explains when to activate
3. **Structured Prompt**: Organized methodology

## Example Workflow

### Step 1: Understand Request
- Read the user's question
- Identify what they need help with
- Determine appropriate response

### Step 2: Provide Information
- Give clear, helpful information
- Use examples when relevant
- Reference documentation

### Step 3: Suggest Next Steps
- Point to additional resources
- Recommend related skills or commands
- Encourage exploration

## Customization Guide

To adapt this skill for your use case:

1. **Update name**: Change to descriptive name (lowercase-with-hyphens)
2. **Update description**: Include YOUR trigger keywords
3. **Set appropriate tools**: Choose tools needed for your task
4. **Write specific prompt**: Detail YOUR skill's methodology
5. **Test activation**: Try phrases that should trigger it

## Example Response

When activated, this skill would respond like:

"I'm the example-helper skill! I was automatically invoked because you mentioned 'example'. This demonstrates how Skills activate based on keywords in their description.

Skills can:
- Access specific tools (I only have Read, Grep, Glob)
- Activate automatically based on context
- Provide specialized expertise
- Be shared across projects

Would you like to see how to create your own skill?"

## Remember

- Skills are proactive (Claude decides when to use them)
- Clear descriptions enable better activation
- Tool restrictions improve safety
- Well-structured prompts improve quality

This is a template - customize it for your specific needs!
