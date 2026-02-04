---
name: my-skill-name
description: Brief description of what this Skill does and when to use it
---

# Skill Name

Provide a detailed explanation of what this skill does and when Claude should invoke it.

## Purpose

Explain the main purpose and use cases for this skill. Be specific about:
- What problem this skill solves
- When it should be automatically invoked
- What the expected outcomes are

## When to Invoke

List the specific scenarios or user requests that should trigger this skill:
- "When the user asks to [specific action]..."
- "When you need to [specific task]..."
- "After [certain event or condition]..."

## Prerequisites

List any requirements needed before this skill can run:
- Required files or directories
- Dependencies or tools that must be installed
- Environment variables that must be set
- Permissions needed
- Other skills that should run first

## Instructions

Provide clear, step-by-step instructions for Claude to follow:

### Step 1: Initial Setup
- Describe what to check or verify first
- List any validation steps
- Mention what to do if prerequisites aren't met

### Step 2: Main Actions
- Be specific about what operations to perform
- Include exact commands or tool calls when possible
- Explain the purpose of each action

### Step 3: Validation
- How to verify the actions were successful
- What to check for errors or issues
- How to confirm the expected state

### Step 4: Finalization
- Any cleanup or final steps needed
- What to report back to the user
- How to mark the task as complete

## Tool Usage

Specify which tools should be used and how:

```markdown
- Use `Read` tool to examine: [files to read]
- Use `Edit` tool to modify: [what to modify]
- Use `Bash` tool to run: [commands to run]
- Use `Write` tool to create: [what to create]
```

## Expected Output

Describe what the skill should produce:
- Files created or modified (with paths)
- Terminal output or logs
- Status messages to show the user
- Success criteria to validate

## Error Handling

Explain how to handle common errors:

### Common Error 1: [Error Type]
- **Symptom**: What the error looks like
- **Cause**: Why it happens
- **Solution**: How to resolve it

### Common Error 2: [Error Type]
- **Symptom**: Description
- **Cause**: Explanation
- **Solution**: Steps to fix

### When to Ask for Help
- List scenarios where Claude should ask the user for input
- Explain what information to request
- Describe any blocking issues that require user intervention

## Examples

See `examples.md` for detailed usage examples, or include simple examples here:

### Example 1: Basic Usage

```
User: [Example request that would trigger this skill]

Expected Behavior:
1. Skill is invoked automatically
2. [Action 1 happens]
3. [Action 2 happens]
4. User sees: [output]
```

### Example 2: Edge Case

```
User: [More complex or unusual request]

Expected Behavior:
1. Skill detects [special condition]
2. [Handles it appropriately]
3. [Produces correct result]
```

## Variables and Customization

If this skill uses variables or can be customized:

- `${VARIABLE_NAME}`: Description of what this represents
- `${ANOTHER_VAR}`: How to use or override this
- Configuration options available

## Integration with Other Skills

- `other-skill-name`: When to use together, in what order
- `another-skill`: How they complement each other
- Dependencies or conflicts to be aware of

## Testing

How to verify this skill works correctly:

1. **Test Case 1**: [Scenario to test]
   - Input: [What to provide]
   - Expected: [What should happen]

2. **Test Case 2**: [Another scenario]
   - Input: [Test input]
   - Expected: [Expected outcome]

## Notes and Best Practices

- Important considerations when using this skill
- Performance tips or optimization suggestions
- Security or safety warnings
- Common pitfalls to avoid
- Best practices for success

## Reference Documentation

See `reference.md` for detailed technical documentation, or list key references here:

- Link to relevant documentation
- API references
- Related tools or libraries
- External resources

## Metadata

- **Author**: Your Name or Organization
- **Version**: 1.0.0
- **Last Updated**: YYYY-MM-DD
- **Category**: [Development / Testing / Documentation / Deployment / Other]
- **Complexity**: [Simple / Moderate / Complex]
- **Estimated Time**: [How long this typically takes]
