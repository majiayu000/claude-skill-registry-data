---
name: commitmsg
description: Generate a concise commit message by analyzing git diff changes
---

# Commit Message Generator

This skill analyzes the changes in your git repository and generates a concise, single-line commit message that follows conventional commit standards.

## How to use this skill

When you want to create a commit message for your changes:

1. Run the `commitmsg.sh` script in this directory
2. The script will analyze the git diff of staged changes
3. It will output a single line commit message you can use

## Example usage

```bash
# Stage your changes first
git add .

# Generate commit message
./commitmsg.sh

# Use the output as your commit message
git commit -m "feat: add user authentication system"
```

## What the script does

The `commitmsg.sh` script:
- Checks if you're in a git repository
- Gets the diff of staged changes (or working directory if nothing staged)
- Analyzes the changed files and their content
- Generates a concise commit message following conventional commit format
- Outputs a single line suitable for `git commit -m`

## Conventional commit format

The generated messages follow the pattern:
- `feat:` for new features
- `fix:` for bug fixes
- `docs:` for documentation
- `style:` for formatting changes
- `refactor:` for code restructuring
- `test:` for test additions
- `chore:` for maintenance tasks

Each message includes a brief description of what changed.