---
description: Comprehensive code refactoring operations for improving code quality and maintainability
---

# Code Refactoring Skill

You are executing a **code refactoring operation** to improve code quality, maintainability, and architecture without changing external behavior.

## Operation Routing

Parse `$ARGUMENTS` to identify the requested operation and parameters:

**Available Operations**:
- `analyze` → Analyze code quality and identify refactoring opportunities
- `extract` → Extract methods, classes, modules, or components
- `patterns` → Introduce design patterns (Factory, Strategy, Observer, etc.)
- `types` → Improve type safety (TypeScript)
- `duplicate` → Eliminate code duplication
- `modernize` → Update legacy code patterns

**Base Directory**: `/home/danie/projects/plugins/architect/open-plugins/plugins/10x-fullstack-engineer/commands/refactor`

## Request Processing

**Received**: `$ARGUMENTS`

**Parse format**:
```
<operation> <parameters>
```

Example arguments:
- `analyze scope:"user authentication module" metrics:"complexity,duplication" depth:"detailed"`
- `extract scope:"UserProfile.tsx" type:"method" target:"validateEmail" reason:"reduce complexity"`
- `patterns scope:"services/" pattern:"dependency-injection" reason:"improve testability"`
- `types scope:"api-client/" strategy:"eliminate-any" strict:"true"`
- `duplicate scope:"src/validators" threshold:"80" strategy:"extract-function"`
- `modernize scope:"legacy-api/" targets:"callbacks-to-async,classes-to-hooks"`

## Pre-Refactoring Safety Checklist

**CRITICAL**: Before ANY refactoring, verify:

1. **Test Coverage**:
   - Existing test coverage is adequate (>70% for code being refactored)
   - All tests currently passing
   - Tests are meaningful and test behavior, not implementation

2. **Version Control**:
   - All changes committed to version control
   - Working on a feature branch (not main/master)
   - Clean working directory (no uncommitted changes)

3. **Backup**:
   - Current state committed with clear message
   - Can easily revert if needed
   - Branch created specifically for this refactoring

4. **Scope Definition**:
   - Clearly defined boundaries of what to refactor
   - No mixing of refactoring with new features
   - Reasonable size for one refactoring session

5. **Risk Assessment**:
   - Understand dependencies and impact
   - Identify potential breaking changes
   - Have rollback plan ready

## Operation Execution

Based on the first word in `$ARGUMENTS`, execute the corresponding operation:

### If operation is "analyze":
Read and execute: `.claude/commands/refactor/analyze.md`

**Purpose**: Analyze code quality, identify code smells, calculate metrics, prioritize refactoring opportunities.

### If operation is "extract":
Read and execute: `.claude/commands/refactor/extract.md`

**Purpose**: Extract methods, classes, modules, components, utilities, or interfaces to improve code organization.

### If operation is "patterns":
Read and execute: `.claude/commands/refactor/patterns.md`

**Purpose**: Introduce design patterns (Factory, Strategy, Observer, Dependency Injection, Repository, etc.) to solve recurring design problems.

### If operation is "types":
Read and execute: `.claude/commands/refactor/types.md`

**Purpose**: Improve type safety by adding types, strengthening types, migrating to TypeScript, eliminating 'any', or adding generics.

### If operation is "duplicate":
Read and execute: `.claude/commands/refactor/duplicate.md`

**Purpose**: Detect and eliminate code duplication through extraction, parameterization, or templating.

### If operation is "modernize":
Read and execute: `.claude/commands/refactor/modernize.md`

**Purpose**: Update legacy code patterns (callbacks→async/await, var→const/let, prototypes→classes, CommonJS→ESM, jQuery→vanilla, classes→hooks).

### If operation is unknown or missing:
Provide operation list and usage examples.

## Error Handling

**Unknown Operation**:
```
Error: Unknown refactoring operation: <operation>

Available operations:
- analyze   - Analyze code quality and identify opportunities
- extract   - Extract methods, classes, modules, components
- patterns  - Introduce design patterns
- types     - Improve type safety (TypeScript)
- duplicate - Eliminate code duplication
- modernize - Update legacy code patterns

Usage: /refactor <operation> <parameters>

Examples:
  /refactor analyze scope:"user-service/" depth:"detailed"
  /refactor extract scope:"UserForm.tsx" type:"component" target:"EmailInput"
  /refactor patterns scope:"services/" pattern:"dependency-injection"
```

**Missing Parameters**:
```
Error: Required parameters missing for <operation>

Expected format: /refactor <operation> scope:"..." [additional-params]

See: /refactor <operation> help
```

**Insufficient Test Coverage**:
```
Warning: Test coverage is below recommended threshold (<70%).

Recommendations:
1. Add tests for code being refactored
2. Reduce refactoring scope to well-tested areas
3. Write tests first, then refactor (Red-Green-Refactor)

Continue anyway? This increases risk of breaking changes.
```

**Uncommitted Changes**:
```
Error: Working directory has uncommitted changes.

Refactoring requires clean version control state for safety.

Action required:
1. Commit current changes: git add . && git commit -m "..."
2. Or stash changes: git stash
3. Create feature branch: git checkout -b refactor/<description>

Then retry refactoring operation.
```

## Integration with 10x-fullstack-engineer Agent

All refactoring operations leverage the **10x-fullstack-engineer** agent for:
- Expert code quality analysis
- Best practice application
- Pattern recognition and recommendation
- Consistency with project standards
- Risk assessment and mitigation
- Test-driven refactoring approach

The agent applies SOLID principles, DRY, YAGNI, and follows the Boy Scout Rule (leave code better than found).

## Refactoring Principles

All operations adhere to:

1. **Preserve Behavior**: External behavior must remain unchanged
2. **Small Steps**: Incremental changes with frequent testing
3. **Test-Driven**: Tests pass before, during, and after refactoring
4. **One Thing at a Time**: Don't mix refactoring with feature development
5. **Frequent Commits**: Commit after each successful refactoring step
6. **Clear Intent**: Each change has clear purpose and benefit
7. **Reversibility**: Easy to revert if something goes wrong
8. **Maintainability First**: Optimize for readability and maintainability

## Usage Examples

**Analyze codebase for refactoring opportunities**:
```bash
/refactor analyze scope:"src/components" metrics:"complexity,duplication,coverage" depth:"detailed"
```

**Extract long method into smaller functions**:
```bash
/refactor extract scope:"UserService.ts" type:"method" target:"validateAndCreateUser" reason:"function is 150 lines, too complex"
```

**Introduce dependency injection pattern**:
```bash
/refactor patterns scope:"services/" pattern:"dependency-injection" reason:"improve testability and flexibility"
```

**Strengthen TypeScript type safety**:
```bash
/refactor types scope:"api/" strategy:"eliminate-any" strict:"true"
```

**Eliminate duplicate validation logic**:
```bash
/refactor duplicate scope:"src/validators" threshold:"75" strategy:"extract-function"
```

**Modernize legacy callback code to async/await**:
```bash
/refactor modernize scope:"legacy-api/" targets:"callbacks-to-async" compatibility:"node14+"
```

## Best Practices

1. **Start Small**: Begin with low-risk, high-value refactorings
2. **Test Continuously**: Run tests after each change
3. **Commit Frequently**: Small commits with clear messages
4. **Pair Review**: Have someone review refactored code
5. **Measure Impact**: Track metrics before and after
6. **Document Why**: Explain reasoning in commits and comments
7. **Avoid Scope Creep**: Stay focused on defined scope
8. **Time Box**: Set time limits for refactoring sessions

## Output

All operations provide detailed reports including:
- Before/after code examples
- Metrics improvement (complexity, coverage, duplication)
- Changes made and reasoning
- Verification steps
- Future refactoring opportunities
- Risk assessment and mitigation

---

**Ready to refactor**: Specify operation and parameters to begin.
