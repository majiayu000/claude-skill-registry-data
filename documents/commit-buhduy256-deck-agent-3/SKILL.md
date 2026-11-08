---
name: commit
description: Generate and create git commits with clear, conventional commit messages. Use when the user wants to commit changes, save work, or asks for a commit message.
allowed-tools: Bash(git:*), Read, Grep, Edit
user-invocable: true
---

# Git Commit Skill

## Overview

Create well-structured git commits with conventional commit messages that clearly describe the changes.

## Instructions

When committing changes, follow these steps:

1. **Check the current state** - Run these commands in parallel:
   - `git status` to see staged and unstaged changes
   - `git diff --cached` to see what's staged
   - `git diff` to see unstaged changes
   - `git log --oneline -5` to see recent commit style

2. **Stage changes if needed** - If there are unstaged changes the user wants to commit, stage them with `git add`

3. **Analyze the changes** - Review what's being committed:
   - What files are affected?
   - What's the nature of the change (fix, feature, refactor, docs, etc.)?
   - What's the primary purpose?

4. **Update CHANGELOG.md** - Add a description of the changes under the `## [Unreleased]` section:
   - Read the top of `CHANGELOG.md` to see the current format
   - If there's no `## [Unreleased]` section, create one at the top (after the header)
   - Add entries under the appropriate category header:
     - `### Added` - New features or capabilities
     - `### Changed` - Changes to existing functionality
     - `### Fixed` - Bug fixes
     - `### Removed` - Removed features or code
     - `### Security` - Security-related changes
   - Each entry should be a bullet point with a clear description
   - Use sub-bullets for additional context when helpful
   - Example format:
     ```markdown
     ## [Unreleased]
     ### Added
     - New phone agent limitation directives
       - Agent now clarifies it cannot make calls including 911
       - Redirects persistent requests to main clinic
     ```
   - Stage the CHANGELOG.md changes with `git add CHANGELOG.md`

5. **Generate a commit message** following this format:
   ```
   <type>: <short description>

   <optional body explaining what and why>
   ```
   Never add a `Co-Authored-By` trailer or any attribution to Claude or any other AI agent or model (AGENTS.md "GitHub conventions").
   Types:
   - `feat`: New feature
   - `fix`: Bug fix
   - `refactor`: Code restructuring without behavior change
   - `docs`: Documentation changes
   - `style`: Formatting, whitespace
   - `test`: Adding or updating tests
   - `chore`: Maintenance tasks, dependencies
6. **Create the commit** using a HEREDOC for proper formatting:
   ```bash
   git commit -m "$(cat <<'EOF'
   type: short description
   Optional longer description.
   EOF
   )"
   ```

7. **Verify success** - Run `git status` to confirm the commit was created

## Guidelines

- Keep the first line under 72 characters
- Use imperative mood ("add feature" not "added feature")
- Focus on WHY the change was made, not just WHAT changed
- Don't include file lists in the message - git tracks that
- Match the style of recent commits in the repo when possible

## Safety

- Never use `--force` or destructive commands
- Never skip hooks with `--no-verify` unless explicitly asked
- Never amend commits that have been pushed
- If there are no changes to commit, inform the user