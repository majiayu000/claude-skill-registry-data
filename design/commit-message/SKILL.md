---
name: commit-message
description: Generates clear commit messages from git diffs. Use when writing commit messages, reviewing staged changes, or when the user asks to create a commit.
allowed-tools: Bash, Read
user-invocable: true
---

# Commit Message Generator

Generate clear, conventional commit messages by analyzing git diffs and staged changes.

## Instructions

When asked to generate or create a commit message:

1. **Analyze Current State**
   - Run `git status` to see what files are staged and unstaged
   - Run `git diff --cached` to review staged changes
   - Run `git log --oneline -10` to understand the project's commit message style

2. **Understand the Changes**
   - Read the diff carefully to understand what changed
   - Identify the type of change (feature, fix, refactor, etc.)
   - Determine the scope/area affected (component, file, feature)
   - Understand the "why" behind the changes, not just the "what"

3. **Generate the Commit Message**

Use this format:
```
<type>(<scope>): <subject>

<body>

Co-Authored-By: ai <caizongding@gmail.com>
```

### Commit Types
- **feat**: New feature or functionality
- **fix**: Bug fix
- **refactor**: Code refactoring (no behavior change)
- **perf**: Performance improvement
- **style**: Styling or formatting changes
- **docs**: Documentation updates
- **test**: Adding or updating tests
- **chore**: Maintenance, dependencies, configuration
- **build**: Build system or dependency changes
- **ci**: CI/CD configuration changes

### Writing Rules
- **Subject line**: Use imperative mood ("add" not "added" or "adds")
- **Length**: Subject ≤ 50 characters, body lines ≤ 72 characters
- **Clarity**: Be specific and descriptive
- **Scope**: Use relevant scope like `todos`, `auth`, `ui`, `api`, etc.
- **Body**: Explain WHY, not WHAT (the diff shows what)

4. **Present the Message**
   - Show the generated commit message clearly
   - Explain your reasoning if the change is complex

5. **Create the Commit Automatically**
   - Use heredoc format for proper multiline message:
   ```bash
   git commit -m "$(cat <<'EOF'
   <type>(<scope>): <subject>

   <body>

   Co-Authored-By: ai <caizongding@gamil.com>
   EOF
   )"
   ```

## Examples

### Example 1: New Feature
**Scenario**: User added a dark mode toggle to settings

```
feat(settings): add dark mode toggle

Implement dark mode toggle with localStorage persistence. The toggle
respects system preferences on first load and provides smooth transitions
between themes using CSS variables.

Co-Authored-By: ai <caizongding@gamil.com>
```

### Example 2: Bug Fix
**Scenario**: Fixed hydration mismatch in todo list

```
fix(hydration): prevent SSR/client mismatch in todo list

Use two-phase hydration pattern to avoid mismatch errors. Now loading
from localStorage in useEffect after component mounts rather than
during initial render.

Co-Authored-By: ai <caizongding@gamil.com>
```

### Example 3: Refactoring
**Scenario**: Extracted logic into custom hook

```
refactor(hooks): extract todo storage logic into useTodoStorage

Move localStorage sync logic into reusable hook for better testability
and separation of concerns. No functional changes to user-facing behavior.

Co-Authored-By: ai <caizongding@gamil.com>
```

### Example 4: Performance Optimization
**Scenario**: Added memoization to expensive calculation

```
perf(todos): memoize completed count calculation

Wrap todo completion calculation in useMemo to prevent unnecessary
recalculation on every render. Improves performance with large todo lists.

Co-Authored-By: ai <caizongding@gamil.com>
```

### Example 5: Style Changes
**Scenario**: Improved responsive layout

```
style(layout): improve mobile responsive design

Adjust grid layout to stack vertically on small screens with better
padding and spacing. Enhance glassmorphism effects for improved contrast.

Co-Authored-By: ai <caizongding@gamil.com>
```

## Best Practices

### Do ✅
- Analyze the full diff before writing the message
- Match the project's existing commit style
- Use specific, actionable language
- Explain the reasoning in the body
- Keep each commit focused on one logical change
- Use conventional commit format consistently

### Don't ❌
- Use vague messages like "fix bug" or "update code"
- Mix multiple unrelated changes in one commit
- Write overly long subject lines
- Forget to add Co-Authored-By attribution
- Skip the body for non-trivial changes
- Use past tense or gerunds

## Special Cases

### Breaking Changes
Add an exclamation mark (!) after the type and include BREAKING CHANGE in body:

```
feat(api)!: change todo response format

BREAKING CHANGE: Todo API now returns different structure.
Before: { id, title, done }
After: { id, text, completed, createdAt }

Update all API consumers to use new format.

Co-Authored-By: ai <caizongding@gamil.com>
```

### Multiple Related Changes
Use bullet points in the body:

```
feat(todos): add filtering and sorting

- Add filter buttons for all/active/completed states
- Implement sort by date or alphabetically
- Persist filter/sort preferences in localStorage

Co-Authored-By: ai <caizongding@gamil.com>
```

### Fixing Issues
Reference issue numbers:

```
fix(auth): resolve login redirect loop

Fixes #123

Detect token expiration properly and redirect to login without
creating an infinite loop.

Co-Authored-By: ai <caizongding@gamil.com>
```

## Verification Checklist

Before committing, verify:
- [ ] Type is correct (feat, fix, refactor, etc.)
- [ ] Scope accurately describes affected area
- [ ] Subject line uses imperative mood
- [ ] Subject line is ≤ 50 characters
- [ ] Body explains WHY, not just WHAT
- [ ] Body lines are ≤ 72 characters
- [ ] Co-Authored-By is included
- [ ] Message follows project conventions
- [ ] Commit is atomic (one logical change)

## Integration with Workflow

This skill works seamlessly with Claude Code's commit workflow:

1. User makes changes and stages them with `git add`
2. User asks "Create a commit" or "Generate commit message"
3. This skill activates automatically
4. Analyzes diff and generates conventional commit message
5. Creates commit with proper attribution

The skill respects the project's existing conventions by analyzing recent commit history.
