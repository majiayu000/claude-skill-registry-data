---
name: refactoring-assistant
description: Assists with code refactoring by detecting code smells, suggesting improvements, and providing refactoring patterns. Activates when writing/editing code, explicitly requested refactoring, or when code quality issues are detected. Maintains awareness of core principles while providing detailed patterns and examples.
allowed-tools: [Read, Grep, Glob, AskUserQuestion]
---

# Refactoring Assistant Skill

## Purpose

Support code quality improvement through:

- Automatic code smell detection during development
- Suggesting appropriate refactoring patterns
- Providing tech-stack specific best practices
- Maintaining code consistency and readability

## Activation Triggers

### Automatic Activation

- When writing or editing source code files
- When file length exceeds thresholds
- When code duplication is detected
- When complex nesting is identified

### Manual Activation

- User says "リファクタリング", "refactor", "code smell"
- User asks about code quality improvement
- User requests design pattern suggestions

## Core Principles (Always Active)

These principles are always kept in mind during coding, regardless of Skill activation.

### Code Smells to Detect

1. **Long Method** (関数が長すぎる)
   - Threshold: > 50 lines
   - Action: Suggest extraction into smaller functions

2. **Duplicate Code** (重複コード)
   - Threshold: Same code appears 3+ times
   - Action: Extract to shared function/constant

3. **Deep Nesting** (ネストが深すぎる)
   - Threshold: > 3 levels
   - Action: Use early return, extract conditions

4. **Long Parameter List** (引数が多すぎる)
   - Threshold: > 5 parameters
   - Action: Use structured parameters (RORO pattern in TS, struct in Go)

5. **Large Class/Module** (クラス/モジュールが大きすぎる)
   - Threshold: > 300 lines
   - Action: Split into smaller modules

6. **Complex Conditional** (複雑な条件式)
   - Threshold: > 3 conditions in single expression
   - Action: Extract to named function/variable

## Workflow

### Phase 1: Detection

1. **Read the code**
   - Use Read tool to examine target files
   - Identify patterns matching code smells

2. **Measure complexity**
   - Count lines in functions
   - Count nesting levels
   - Count parameters
   - Detect duplication patterns

3. **Prioritize issues**
   - Critical: Security risks, bugs
   - High: Code smells affecting readability
   - Medium: Minor style inconsistencies

### Phase 2: Analysis

1. **Check against tech-stack rules**
   - TypeScript/React: Refer to `patterns/typescript-react.md`
   - Go: Refer to `patterns/go.md`

2. **Consider context**
   - Is this a one-time case or recurring pattern?
   - Is the complexity justified by business logic?
   - Would refactoring improve or harm clarity?

3. **Review existing patterns**
   - Check `~/.claude/knowledge/patterns/` for similar cases
   - Ensure consistency with project CLAUDE.md

### Phase 3: Suggestion

1. **Present findings**
   - List detected code smells with severity
   - Show specific locations (file:line)
   - Explain why it's a problem

2. **Propose solutions**
   - Suggest appropriate refactoring pattern
   - Show before/after code examples
   - Explain benefits and trade-offs

3. **Ask for approval**
   - Use AskUserQuestion for user decision
   - Allow partial acceptance (fix some, not all)

### Phase 4: Implementation

1. **Apply refactoring**
   - Make changes incrementally
   - Maintain backward compatibility if needed
   - Update tests accordingly

2. **Verify quality**
   - Ensure tests still pass
   - Run linter if available
   - Check for new code smells

3. **Document if needed**
   - If this is a new pattern, suggest recording to Knowledge Base
   - Update project CLAUDE.md if this establishes new standard

## Code Smell Detection Details

Refer to `rules/code-smells.md` for detailed detection criteria and refactoring patterns for each code smell.

## Tech-Stack Specific Patterns

### TypeScript/React

See `patterns/typescript-react.md` for:

- React component refactoring patterns
- Hook extraction and optimization
- State management improvements
- CSS Modules organization

### Go

See `patterns/go.md` for:

- Function extraction patterns
- Interface design improvements
- Error handling refactoring
- Goroutine and channel optimization

## Integration with Knowledge Base

When discovering new refactoring patterns or solutions:

1. **Record to Knowledge Base**
   - Use knowledge-manager Skill to document
   - Category: `patterns/refactoring-{tech-stack}.md`

2. **Update INDEX**
   - Ensure pattern is searchable
   - Add relevant tags and categories

## Guardrails

### When NOT to Refactor

1. **Working on tight deadline** - Defer to post-release
2. **No test coverage** - Write tests first
3. **Unclear requirements** - Clarify before refactoring
4. **Code is working and stable** - If it ain't broke, consider carefully

### Safety Checks

1. **Always run tests** before and after refactoring
2. **Make small, incremental changes** - easier to review and rollback
3. **Preserve behavior** - refactoring should not change functionality
4. **Document breaking changes** if unavoidable

## Usage Tips

### For User

- This Skill helps detect code smells, but **core principles remain in Global CLAUDE.md**
- You should always be aware of basic refactoring principles during coding
- Use this Skill for **detailed patterns and examples**, not just principles

### For Claude

- **Always keep core principles in mind** regardless of Skill activation
- Don't wait for explicit "refactor" request - suggest improvements during normal coding
- Balance between code quality and practical constraints
- Prefer incremental improvements over massive rewrites

## Supporting Files

- `rules/code-smells.md`: Detailed code smell detection and refactoring patterns
- `patterns/typescript-react.md`: TypeScript/React specific refactoring patterns
- `patterns/go.md`: Go specific refactoring patterns
- `~/.claude/knowledge/patterns/`: Real-world refactoring examples

## Maintenance

Update this Skill when:

- New code smells are discovered
- New refactoring patterns are established
- Tech-stack best practices evolve
- Team coding standards change
