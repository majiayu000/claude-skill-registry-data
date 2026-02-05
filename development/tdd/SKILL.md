---
name: tdd
description: Enforce Test-Driven Development when writing or modifying code. Use when implementing features, fixing bugs, or when the user asks to write code. Activates automatically for code changes unless user says "quick fix" or "no tdd".
---

# TDD Skill

Enforce Red-Green-Refactor discipline for all code changes.

## When This Skill Activates

- User asks to implement a feature
- User asks to fix a bug
- User asks to write or modify code
- `/start-dev` delegates Phase 3 to this skill

## When This Skill Does NOT Activate

- User says "quick fix" or "no tdd"
- Pure refactoring with no behavior change (user specifies)
- Documentation-only changes

## Review Modes

Mode determines when user reviews your work. Default is **interactive**.

### Changing Modes

User can say:
- `use interactive` - review each cycle (default)
- `use batch-ac` - review after each acceptance criterion
- `use batch-story` - review after all acceptance criteria
- `use autonomous strict` - agent reviews, flags any code smell
- `use autonomous normal` - agent reviews, flags significant issues
- `use autonomous relaxed` - agent reviews, flags blockers only

### Mode Behavior

| Mode | Review Point | Best For |
|------|--------------|----------|
| **Interactive** | After each Red-Green cycle | Learning, complex logic, unfamiliar code |
| **Batch AC** | After completing an acceptance criterion | Moderate oversight, well-understood domain |
| **Batch Story** | After all acceptance criteria complete | Maximum flow, trusted patterns |
| **Autonomous** | Agent reviews continuously | Speed with quality gates |

### Mode Persistence

- Remember the current mode throughout the conversation
- If uncertain about mode, default to **interactive**
- Acknowledge mode on each cycle: "Running in [mode] mode..."
- When mode changes, confirm: "Switched to [mode] mode"

## The Red-Green-Refactor Workflow

For each piece of functionality:

### RED: Write a Failing Test

1. Identify the smallest next piece of functionality
2. Write just enough test code to fail
3. **Interactive/Batch**: Show the test, explain what it tests
4. **Autonomous**: Proceed without showing
5. Run the test:
   ```bash
   ./gradlew test
   ```
6. **Confirm RED**: Test MUST fail
   - If it passes: STOP - this is suspicious, discuss with user

### GREEN: Make it Pass

1. Choose a technique:
   | Technique | When | How |
   |-----------|------|-----|
   | **Fake It** | Unsure of implementation | Return constant, replace with variables later |
   | **Obvious Implementation** | Know exactly what to type | Write real implementation directly |
   | **Triangulation** | Design unclear | Add test cases to reveal pattern |

2. Write minimum code to pass - no more
3. **Interactive/Batch**: Show the implementation
4. **Autonomous**: Proceed without showing
5. Run the test:
   ```bash
   ./gradlew test
   ```
6. **Confirm GREEN**: Test MUST pass before proceeding

### REFACTOR: Clean Up

1. Look for duplication (primary target)
2. Apply clean code principles
3. **Interactive mode**: Ask "Any refactoring before we commit?"
4. **Batch mode**: Note refactoring opportunities, continue
5. **Autonomous mode**: Invoke Review skill, act on findings based on threshold
6. If refactoring: Run tests again to ensure still GREEN

### COMMIT

**Interactive mode**: Wait for user confirmation before committing

**Batch mode**: Commit automatically, user reviews at batch point

**Autonomous mode**: Commit if Review skill found no blockers

```bash
git add -A && git commit -m "<descriptive message> #<issue-number>

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

## Autonomous Mode Details

When in autonomous mode, invoke the Review skill after GREEN phase.

### Threshold Behavior

| Threshold | Interrupt For | Continue If |
|-----------|---------------|-------------|
| **Strict** | Any finding (blocker, warning, suggestion) | No findings at all |
| **Normal** | Blockers and warnings | Only suggestions |
| **Relaxed** | Blockers only | Warnings and suggestions OK |

### On Interrupt

When Review skill finds issues above threshold:
1. Show the findings to user
2. Ask how to proceed:
   - Fix now
   - Ignore and continue
   - Switch to interactive mode

## Batch Review Points

### Batch AC Mode

After completing an acceptance criterion:
1. Show summary of all changes made
2. Show cumulative Review skill findings (if any)
3. Ask user to review
4. Address feedback before next criterion

### Batch Story Mode

After completing all acceptance criteria:
1. Show full summary of implementation
2. Run comprehensive Review skill scan
3. Present findings by category
4. Address feedback before marking story complete

## Integration with /start-dev

When invoked from `/start-dev`:
- Story context is already established
- Acceptance criteria are defined
- Work through criteria one by one
- Use review mode specified (or default to interactive)

## Key Principles

From `docs/context/testing.md`:

### Kent Beck's Two Rules
1. Write new code only if an automated test has failed
2. Eliminate duplication

### The Three Laws (Uncle Bob)
1. No production code unless it makes a failing test pass
2. No more test code than sufficient to fail
3. No more production code than sufficient to pass

### Remember
- **No code without a failing test first** - non-negotiable
- **Tests must actually run** - "this would fail" doesn't count
- **Small steps** - each test covers one small piece
- **When uncertain, ask** - never proceed without clarity
