---
name: conventional-commit
description: Create commit messages following the Conventional Commits specification
allowed-tools: Bash, Read, Edit, AskUserQuestion
---

# Conventional Commit Skill

This skill helps create commit messages following the [Conventional Commits](https://www.conventionalcommits.org/) specification.

## Instructions

You are a commit message assistant. Your task is to analyze the current changes, split them into logical commits if needed, and create well-formatted commit messages.

### Steps to Follow

1. **Analyze Changes**: Run `git status` and `git diff --staged` (or `git diff` if nothing is staged) to understand what has been changed.

2. **Evaluate whether to split**: Group changes by their logical purpose. If changes span multiple types (e.g., tests + docs + chore), split into separate commits. Apply these rules:
   - **Split when**: Changes have different commit types (test vs docs vs feat), touch unrelated scopes, or serve independent purposes
   - **Keep together when**: Changes are tightly coupled and one doesn't make sense without the other (e.g., a feature + its test in the same module)
   - **Ordering**: Commit in dependency order — foundational changes first (e.g., tests before docs that reference them)

3. **Determine the Commit Type** for each commit:
   - `feat`: A new feature
   - `fix`: A bug fix
   - `docs`: Documentation only changes
   - `style`: Changes that do not affect the meaning of the code (white-space, formatting, etc.)
   - `refactor`: A code change that neither fixes a bug nor adds a feature
   - `perf`: A code change that improves performance
   - `test`: Adding missing tests or correcting existing tests
   - `build`: Changes that affect the build system or external dependencies
   - `ci`: Changes to CI configuration files and scripts
   - `chore`: Other changes that don't modify src or test files
   - `revert`: Reverts a previous commit

4. **Identify the Scope** (optional): Determine if there's a specific component, module, or area affected.

5. **Write the Description**: Create a concise description in imperative mood (e.g., "add feature" not "added feature").

6. **Add Body** (if needed): For complex changes, add a body explaining the motivation and contrast with previous behavior.

7. **Add Footer** (if needed): Include any breaking changes or issue references.

### Commit Message Format

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

### Splitting Example

Given these unstaged changes:
- `src/api/types.rs` — added deserialization tests
- `tests/fixtures/*.json` — new test fixture files
- `docs/api-type-guide.md` — new documentation
- `CLAUDE.md` — added rules about API types
- `.claude/skills/verify/SKILL.md` — added test step

Split into:
1. `test(api): add deserialization tests for API types` — types.rs + fixtures/
2. `docs(api): add API type definition guide` — docs/api-type-guide.md + CLAUDE.md
3. `chore(verify): add cargo test step to verify skill` — verify/SKILL.md

### Important Rules

- Keep the first line (header) under 72 characters
- Use lowercase for type and scope
- Do not end the description with a period
- Use imperative mood in the description
- Separate header from body with a blank line
- Wrap body at 72 characters
- Do NOT include auto-generated footers (e.g., "Generated with Claude Code", "Co-Authored-By")

### Interactive Workflow

After analyzing the changes, present the user with:

1. A summary of what changed
2. The proposed commit(s) — if splitting, show each commit with its files
3. Ask for confirmation or modifications before executing

If the user provides additional context or wants changes, adjust accordingly.

### Execution

For each commit:
1. Stage only the relevant files with `git add <specific files>`
2. Commit with the message using a HEREDOC:
   ```bash
   git commit -m "$(cat <<'EOF'
   <commit message here>
   EOF
   )"
   ```
3. Proceed to the next commit

$ARGUMENTS
