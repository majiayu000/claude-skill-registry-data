---
name: self-improving-agent
description: Continuous improvement through error tracking, lesson learning, and feedback integration
activation_keywords: [error, fix, mistake, fail, wrong, correct, learn, improve, retry]
---

# Self-Improving Agent

This skill enables continuous improvement by tracking errors, lessons learned, and user corrections. Uses persistent database storage.

## When to Use

Use this skill proactively in these scenarios:

1. **Command or operation fails unexpectedly** - A tool execution fails, command returns error
2. **User corrects you** - User says "no, that's wrong", "not what I meant", or provides corrections
3. **Repeated failures** - Same type of error occurs multiple times
4. **Unknown uncertainty** - Not sure if approach is correct, want to verify before proceeding

## How It Works

### Using the Tool

Use `builtin_learning` tool with the following operations:

#### 1. Record a Learning (add)
Record what you learned from an error or correction:

```
operation: "add"
error_type: "shell_command_permission_denied"
context: "Tried to run 'apt-get install' without sudo"
root_cause: "User not in sudoers file"
fix: "Use 'sudo' prefix or check if user has permission"
lesson: "Always check if elevated permissions are needed before system commands"
```

**Parameters:**
- `operation`: "add" or "create"
- `error_type`: Short identifier (e.g., "shell_permission", "wrong_editor")
- `context`: What were you trying to do?
- `root_cause`: Why did it fail?
- `fix`: What did you do differently?
- `lesson`: What did you learn? (general principle)
- `user_id`: User ID (optional, omit for global learning)

#### 2. List Learnings (list)
Get all learnings for a user (or global if no user_id):

```
operation: "list"
user_id: "123"
```

#### 3. Get Specific Learning (get)
Retrieve a specific learning by error_type:

```
operation: "get"
error_type: "shell_command_permission_denied"
```

## Key Principles

- **Don't repeat mistakes** - Apply learnings to avoid same class of errors
- **Be specific** - Log concrete details, not vague notes
- **Extract patterns** - Look for recurring themes
- **Acknowledge uncertainty** - It's okay to ask for verification when unsure
- **Learn from users** - Their corrections are valuable feedback

## After Each Error/Correction

When you learn something, record it:

```
Error/Lesson: [Brief description]
Root Cause: [Why it happened]
Fix Applied: [What you did differently]
Learnings: [General principle for future]
```

This skill should be used proactively - don't wait to be told to improve. The platform gets smarter over time!