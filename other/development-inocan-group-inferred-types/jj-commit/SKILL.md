---
name: jj-commit
description: Generate conventional commit messages for jj by analyzing diffs, running tests first, and handling immutable commits
---

# JJ Commit Message Generator

Generate conventional commit messages for Jujutsu (jj) by analyzing diffs.

## Instructions

When the user asks to create a commit message or commit changes:

1. **Run tests first:**
   - Detect test framework from project (package.json, Cargo.toml, pyproject.toml, etc.)
   - Run appropriate test command:
     - npm/yarn: `npm test` or `yarn test`
     - Rust: `cargo test`
     - Python: `pytest` or `python -m pytest`
     - Go: `go test ./...`
   - If tests fail:
     - Show failures to user
     - Ask: "Tests failing. Fix before commit, skip tests, or commit anyway?"
     - Only proceed with commit if user explicitly chooses to skip/ignore
   - If no test command found, proceed without testing

2. **Gather context:**
   - Run `jj diff` to see current changes
   - Run `jj log -r @` to see the current change description
   - If working with specific revisions, use `jj diff -r <revision>`

3. **Analyze changes:**
   - Identify the type: feat, fix, refactor, docs, test, chore, style, perf
   - Determine scope if clear from file paths
   - Summarize the "why" (intent) not just "what" changed

4. **Generate message:**
   Format: `<type>(<scope>): <subject>`

   - Subject: imperative mood, lowercase, no period, < 72 chars
   - Body (optional): explain why, not what
   - Favor precision over verbosity

   Examples:
   - `feat(ui): add dark mode toggle`
   - `fix(auth): prevent token refresh loop`
   - `refactor(api): simplify error handling`

5. **Handle immutable commits:**
   If you get error: `Commit ... is immutable`:
   - Explain that the commit is immutable
   - Suggest running the command with `--ignore-immutable` flag
   - Ask user if they want to proceed with the flag

6. **Execute commit:**
   - Use `jj describe -m "message"` for current change
   - Or `jj describe -r <revision> -m "message"` for specific revision
   - If immutable and user approves, add `--ignore-immutable`

## Tool access
allowed-tools:
  - Bash
  - Read
  - Grep

## Notes
- Keep messages concise and clear
- Focus on intent, not implementation details
- Follow conventional commit format strictly
