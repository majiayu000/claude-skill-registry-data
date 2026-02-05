---
name: "API Documentation"
description: "Document APIs comprehensively with signatures, parameters, return values, errors, and working code examples for developer reference"
category: "documentation"
required_tools: ["Read", "Write", "Grep", "Glob"]
---

# API Documentation

## Purpose
Create comprehensive API documentation that enables developers to quickly understand and correctly use APIs, including parameters, return values, errors, and practical examples.

## When to Use
- Documenting public APIs
- Creating developer references
- Writing SDK documentation
- Updating API changes

## Key Capabilities
1. **Signature Documentation** - Clear parameter and return type descriptions
2. **Example Creation** - Practical, working code examples
3. **Error Documentation** - All possible errors and when they occur

## Approach
1. Document function signature with types
2. Describe each parameter clearly
3. Describe return value and possible states
4. List all exceptions/errors that can be raised
5. Provide working example code
6. Note version added or deprecated

## Example
**Context**: Documenting a task creation function
````markdown
### add_task(title, agent, priority, description)

Creates a new task in the queue.

**Parameters**:
- `title` (string) - Short descriptive title for the task
- `agent` (string) - Agent name to assign (must exist in agents.json)
- `priority` (string) - One of: "critical", "high", "normal", "low"
- `description` (string) - Detailed task description

**Returns**:
- `string` - Unique task ID for the created task

**Raises**:
- `ValueError` - If agent name is invalid or priority is unknown
- `FileNotFoundError` - If queue file cannot be accessed

**Example**:
```python
task_id = queue.add_task(
    title="Fix login bug",
    agent="implementer",
    priority="high",
    description="Users cannot log in with valid credentials"
)
print(f"Created task: {task_id}")
```

**Since**: v1.0.0
````

## Best Practices
- ✅ Include type information for all parameters
- ✅ Provide complete, working examples
- ✅ Document all possible errors
- ❌ Avoid: Incomplete or outdated examples