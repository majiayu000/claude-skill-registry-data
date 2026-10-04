---
name: git-commit
description: Commit current changes with conventional commits format, respecting logical units of work. Use when making local commits to the repository with properly formatted conventional commit messages.
allowed-tools:
  - Bash(git add:*)
  - Bash(git commit:*)
models:
  claude: haiku      # low-complexity; fast git operations need minimal reasoning
  copilot: gpt-5.4-mini  # mini equivalent for low-complexity Copilot tasks
  codex: gpt-5.4-mini
---

# Git Commit with Conventional Format

Commit current changes using conventional commits format.

## Logical Units of Work

**IMPORTANT**: Always split commits into logical units of work. Each commit should represent a cohesive, atomic change that can stand alone.

### Examples of Logical Units:
- **Related implementation**: Interface + implementation + model + tests for a single feature
- **Database changes**: Migration + related model changes + tests
- **Refactoring**: Changes to a specific component/service and its tests
- **Configuration**: Config changes + documentation updates
- **Bug fix**: Fix + tests that verify the fix
- **Domain model**: Model changes + repository/service updates + tests

### When to Split Commits:
- **Different types of changes** (feat vs refactor vs fix) → Separate commits
- **Unrelated features** → Separate commits
- **Different layers/concerns** → Assess if they're truly independent, ask user if unclear (skipped when `--mansplain` is passed)
- **Documentation vs implementation** → Usually separate, unless tightly coupled

### When to Combine in One Commit:
- Implementation + its direct tests
- Interface + implementation when inseparable
- Model + configuration needed for that model
- Tightly coupled changes that don't make sense separately

**If uncertain whether changes form a logical unit, ask the user for clarification before committing.** _(Skipped when `--mansplain` is passed — use best judgment.)_

## Workflow Steps

1. Check git status to identify all modified, added, and deleted files
2. Review the changes using git diff to understand what was modified
3. **Analyze and group changes into logical units** — Identify related changes that should be committed together
4. **Ask user if grouping is unclear** — When uncertain about logical boundaries, confirm with user. **Skip this step when `--mansplain` is passed** — use best judgment and proceed without asking.
5. For each logical unit:
   a. Stage all relevant changes using git add
   b. Create a conventional commit message following the format: `<type>[optional scope]: <description>` (per `.agents/rules/git/git-policy.instructions.md` — the source of truth for allowed types and subject rules). **No commit may be created unless its message conforms — if a conforming message cannot be determined, STOP and ask the user; never commit with a non-conforming message.** _(When `--mansplain` is passed: make your best determination and proceed without asking.)_
   c. Fallback types — use ONLY when the git-policy rule is not loaded in context (e.g. a runner that doesn't auto-load `.agents/rules/`). These mirror the rule and must never override it; if the rule is present, it wins. Keep this list in sync with `git-policy.instructions.md`:
      - `feat` (new feature)
      - `fix` (bug fix)
      - `chore` (maintenance, dependency updates, tooling)
      - `docs` (documentation)
      - `refactor` (code restructuring without behaviour change)
      - `test` (tests)
      - `ci` (CI/CD)
      - `perf` (performance)
      - `build` (build system)
   d. Add `BREAKING CHANGE:` footer or `!` after type/scope for breaking changes
   e. Execute git commit with the conventional commit message
6. Repeat for each logical unit until all changes are committed

## Arguments

- Optional: pre-defined commit message (if not provided, will analyze changes and generate appropriate conventional commit message)
- `--mansplain` — suppress all interactive questions; the agent uses its best judgment on grouping and commit messages without asking. Never stops to confirm with the user.

## Usage Examples

```
/git-commit
/git-commit feat: add user authentication system
/git-commit fix(auth): handle expired sessions properly
/git-commit --mansplain
/git-commit --mansplain feat: add user authentication system
```
