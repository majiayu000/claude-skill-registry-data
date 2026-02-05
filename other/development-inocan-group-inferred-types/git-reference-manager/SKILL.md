---
name: git-reference-manager
description: "Safely introduce external Git repositories as reference materials. Responsible for managing the `_reference` directory, ensuring external code is read-only and does not pollute the project's version control."
---

# Git Reference Manager

This skill provides guidance on how to formally introduce external repositories into a project for reading and learning. This is crucial for understanding third-party library architectures or finding best practices.

## Core Rules

> **Isolation Principle**: Reference code must be strictly isolated within the `_reference/` directory. It is strictly forbidden to commit it to the main project's Git history.

## Standard Workflow

When you need to reference an external repository (e.g., `anthropics/skills` or `pandas`), you **must** strictly follow these three steps in order:

### 1. Prepare Sandbox

First, ensure the dedicated directory for storing reference materials exists.

- **Check**: Does the `_reference` directory exist in the project root?
- **Action**: If not, create it.

  ```bash
  mkdir -p _reference
  ```

### 2. Secure Boundary

Before pulling any code, you must ensure that Git ignores this directory.

- **Check**: Does the `.gitignore` file contain `_reference/`?
- **Action**: If not, append it to the end of the file.

  ```bash
  # Check
  grep "_reference/" .gitignore
  # Append (if missing)
  echo -e "\n# External References\n_reference/" >> .gitignore
  ```

### 3. Fetch References

Clone the target repository into a subdirectory within the sandbox.

- **Naming**: Use the repository name as the subdirectory name.
- **Action**: Use `git clone`.

  ```bash
  git clone <REPO_URL> _reference/<REPO_NAME>
  ```

- **Note**: Deep history is not required; it is recommended to use `--depth 1` to save time and space.

  ```bash
  git clone --depth 1 https://github.com/anthropics/skills.git _reference/anthropics_skills
  ```

## Best Practices

- **Read-Only Mode**: Treat all files under `_reference/` as **read-only**. Do not modify them unless it is for testing certain changes (but be aware that changes will be lost).
- **Search via grep**: Use `grep` or `ripgrep` to search for code patterns within the reference directory.
- **Discard Anytime**: Since these files are ignored by git and can be re-cloned, you can delete them at any time to free up space after finishing your task.

## Example

**User Request**: "I want to see how React's source code handles Hooks."

**Agent Execution**:

1. `mkdir -p _reference`
2. `grep "_reference" .gitignore || echo "_reference/" >> .gitignore`
3. `git clone --depth 1 https://github.com/facebook/react.git _reference/react`
4. Start reading `_reference/react/packages/react-reconciler/...`
