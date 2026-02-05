---
name: Git Version Control
description: Provides Git version control operations for managing code repositories. Allows agents to check repository status, view commit history, and perform basic Git operations.
---

## Context Keywords

- git
- version control
- repository
- commit
- source control
- vcs

## Tools

- `example-git-skill_git_status` - Get the current Git status (HTTP endpoint)
- `example-git-skill_git_log` - View commit history (HTTP endpoint)
- `check_git_status` - Check Git status (direct tool call)

## Instructions

Use this skill when you need to:

1. Check the current state of a Git repository
2. View recent commit history
3. Understand what files have been modified, added, or deleted
4. Get information about the current branch

**Prerequisites:**
- The working directory must be within a Git repository
- Git must be installed on the system

**Best Practices:**
- Always check the status before making changes
- Use descriptive commit messages
- Review changes before committing

## Examples

### Example 1: Check Repository Status

```python
# Using the tool decorator
status = check_git_status()
print(f"Current status: {status}")
```

### Example 2: View Recent Commits

```python
# Using the HTTP endpoint
response = await git_log(limit=10)
if response["status"] == "success":
    print(f"Recent commits:\n{response['output']}")
```

### Example 3: Combined Workflow

When asked "What changes are in the repository?":
1. First, call `check_git_status()` to see modified files
2. Then, call `git_log(limit=5)` to see recent commits
3. Provide a summary of both results to the user

### Example 4: Error Handling

Always check the response status and handle errors gracefully:

```python
result = await git_status()
if result["status"] == "error":
    print(f"Git operation failed: {result['message']}")
else:
    print(f"Status: {result['output']}")
```
