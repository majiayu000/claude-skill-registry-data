---
name: prompt-guidelines-commands
description: >-
  Command creation guidelines for encapsulating workflows into simple command invocations.
  Provides command syntax, error handling patterns, security validation, and complex command handling.
  Includes examples for environment variables, git operations, and command chaining.
  Scope: command creation, command structure, error handling, security.
  Excludes: skill creation, agent creation (handled by component-specific skills).
  Triggers: command, create command, add command, new command.
---

# PROMPT GUIDELINES FOR COMMANDS

## CONTEXT

### Core Function
- **Goal**: Encapsulate workflows → Simple `/command` invocation
- **Scope**: Reusable templates, multi-step processes, ecosystem integration

### Dependencies
- Bash (shell), YAML (frontmatter), Markdown

### Threat Model
- Input → Sanitize(shell_escapes) → Validate(Safe) → Execute
- Command injection via arguments → Strip dangerous chars
- Destructive_Op → Require User_Confirm

### Validation Layers (Apply in Order)
1. Input: Type check, schema validate, sanitize
2. Context: Verify permissions, check dependencies
3. Execution: Confirm intent, check for destructiveness
4. Output: Verify format, redact secrets

*See Security & Validation section below for detailed implementation*

## SYNTAX & STRUCTURE

### Basic Command Template
```markdown
---
description: >-
  [One-line purpose]
  Scope: [areas covered]
  agent: [Optional: @agent/name]
---

## USER INPUT

**Default**: [Default behavior when no arguments provided]

**Input**: $ARGUMENTS

1. Step_1: Action
2. Step_2: Verify(Result)
3. Step_3: Error_Handle → Fallback
```

### User Input Section (MANDATORY)
All commands MUST include a User Input section:
- **Default**: Document behavior when no arguments provided
- **Input**: MUST contain `$ARGUMENTS` placeholder for command parser substitution
- Do NOT reference $ARGUMENTS inline in execution steps
- **To refer to user-provided data**: Use natural language phrases like "the user input" or "provided context" in execution steps
- **Example**: "Incorporate provided context if available" (correct)

## INLINE COMMAND EXECUTION
- **Syntax**: `!`command`` for shell output in command context
- **Usage**: Embed context from git, environment, file operations
- **Preference**: Use inline execution where feasible (save tokens, direct calls)
- **When to use**:
  - Static data retrieval (dates, branches, file existence)
  - Environment variable checks
  - Git status/info
  - Simple conditionals returning strings
  - Non-destructive commands

### Error Handling (MANDATORY)
- **Handle inline**: All error handling within command itself
- **Simple**: `command 2>/dev/null || fallback` (preferred, no `command -v` needed)
- **Conditional**: `command -v tool && tool command` (only when pre-check needed)
- **Operators**: `||` for fallbacks, `&&` for chains
- **Defaults**: `${VAR:-default}` for missing variables
- **Suppress**: `2>/dev/null` to hide errors
- **PROHIBITED**: `2>&1` redirect causes parser errors (use `2>/dev/null`)
- **Safe alternative for capturing both streams**: Wrap in `sh -c` and use `2>&1` inside: `!`sh -c 'command 2>&1'`

### Examples
- Environment: `IS_WORK=!`echo ${IS_WORK:-0}`
- Date/time: `TODAY=!`date +%Y-%m-%d`
- Git status: `STATUS=!`git status --porcelain || echo "clean"`
- Branch name: `BRANCH=!`command -v git && git rev-parse --abbrev-ref HEAD || echo "not-in-git"`
- File checks: `EXIST=!`test -f .env && echo "exists" || echo "not found"`
- Command results: `PRS=!`gh pr list --state merged --json title | jq '.[] | .title' 2>/dev/null || echo "none"`

## COMPLEX COMMANDS

### Complex Command Wrapper
- **Issue**: Commands with pipes (`|`), subshells `()`, complex conditionals, multiple redirections (`2>/dev/null`) may fail during interpolation
- **Solution**: Wrap complex commands in `sh -c '...'` to ensure proper shell parsing
- **⚠️ SECURITY WARNING**: NEVER include user input inside `sh -c '...'` unless fully sanitised. `sh -c` re-enables shell parsing and command injection risks
- **When to use**:
  - Pipes: `command1 | command2`
  - Subshells: `(command1 && command2) || command3`
  - Multiple redirections: `command 2>&1 | command`
  - Complex conditionals with nested operations

### Complex Command Examples
```markdown
# Simple command (no sh -c needed)
BRANCH=!`git rev-parse --abbrev-ref HEAD`

# Complex command with pipe and redirection (sh -c required)
RESULT=!`sh -c 'git diff --staged | grep -Ei "password|secret|key|token|api_key" 2>/dev/null || echo "safe"'`

# Complex command with subshell (sh -c required)
DEFAULT=!`sh -c 'git symbolic-ref --short refs/remotes/origin/HEAD 2>/dev/null | sed "s|^origin/||" || { git rev-parse --verify main >/dev/null 2>/dev/null && echo main; } || echo master'`

# Multiple pipes and operators (sh -c required)
DATA=!`sh -c 'cat file.json | jq -r ".items[].value" 2>/dev/null | head -5 || echo "none"'`
```

## SECURITY & VALIDATION (MANDATORY)
- **Prohibition**: Hardcoded credentials == FORBIDDEN
- **Input Sanitization**: $ARGUMENTS → Strip dangerous chars → Validate schema
  - **Strip characters**: `; | & $ ( ) < >` backticks, newlines
  - **Validate against whitelist**: POSIX character class `[:alnum:]`, `[:punct:]` (safe subset)
  - **Use safe quoting**: `printf '%q'` or `${VAR@Q}` for shell-safe escaping
  - **Example**: `SAFE_INPUT=$(printf '%q' "$ARGUMENTS")`
- **Destructive Ops**: `rm`, `sudo`, `git push -f`, `chmod` → Require `User_Confirm`
- **Validation Pipeline**:
  1. Parse $ARGUMENTS
  2. Sanitize (remove shell escapes)
  3. Validate schema/type
  4. Confirm if destructive
  5. Execute safely
- **Error Handling**: Never expose secrets in error messages

## CRITICAL VARIABLE USAGE RULES

### $ARGUMENTS Variable
- **Purpose**: Capture user input when command is invoked
- **MUST Appear ONLY**: In the User Input section (`**Input**: $ARGUMENTS`)
- **Forbidden Patterns**:
  - NEVER use $ARGUMENTS in ANY phase (Phase 1, 2, 3, or 4)
  - NEVER assign intermediate values to $ARGUMENTS
  - NEVER reference $ARGUMENTS in execution steps
  - NEVER use $ARGUMENTS for conditions or validation

### Referencing User Input
- **To refer to user-provided data**: Use natural language phrases like "the user input" or "provided context" in execution steps
- **Example**: "Incorporate provided context if available" (correct)
- Example: "Incorporate provided context if available" (correct)
- Example: "Use the date from user input" (correct)
- Example: `IF $ARGUMENTS.ambiguous != FALSE` (WRONG - uses $ARGUMENTS)

### Bash Variable Usage (TODAY, PRS, etc.)
- These ARE NOT $ARGUMENTS
- These capture command outputs for later processing
- Example: `TODAY=date +%Y-%m-%d`, `PRS=gh pr list ...` (correct - these are command outputs)

### Violation Check
- User Input section: MUST contain `**Input**: $ARGUMENTS`
- All phases: MUST NOT contain $ARGUMENTS anywhere
- Execution steps: MUST reference user input naturally, not via $ARGUMENTS

## COMMAND TEMPLATE

```markdown
---
description: >-
  [One-line purpose]
  Scope: [areas covered]
---

# COMMAND_NAME

## EXECUTION PROTOCOL

### Phase 1: Clarification [MANDATORY]
- **Rule**: Multiple logic chains supported. Each on new line.
- **Logic**:
  - Check overall context ambiguity
  - Validate arguments provided
  - Validate command dependencies
  - Validate permissions

IF arguments ambiguous THEN
  - List required arguments
  - Wait(User_Input)
END

IF dependencies missing THEN
  - List required tools/commands
  - Wait(User_Input)
END

IF all validations pass
  - Proceed to Phase 2
END

### Phase 2: Planning [MANDATORY]
- **Rule**: Multiple logic chains supported. Each on new line.
- **Logic**:
  - Analyze command requirements
  - Identify execution steps
  - Map dependencies
  - Assess impacts

IF impact > Low THEN
  - Propose plan (Steps + Bash Commands + Impacts)
  - Wait(User_Confirm)
ELSE
  - Execute plan directly
END

### Phase 3: Execution [MANDATORY]
- **Rule**: Multiple logic chains supported. Each on new line.
- **Logic**:
  - For each step
    - Execute bash command
    - Validate result

    IF result fails THEN
      - Identify failure point
      - Apply error handling
      - Retry with fallback
    END

### Phase 4: Validation [MANDATORY]
- **Rule**: Multiple logic chains supported. Each on new line.
- **Logic**:
  - Run final checklist
  - Verify command executed successfully
  - Verify output matches expected format
  - Verify no side effects

IF checklist fails THEN
  - Identify failed checks
  - Apply corrections
  - Re-run checklist
END

IF checklist passes
  - Complete command execution
END

## USER INPUT [MANDATORY]

**Default**: [Default behaviour. Remove if not set]
**Input**: $ARGUMENTS

## EXECUTION STEPS [MANDATORY]

### Execution Pattern
Execute bash commands step by step

IF step fails THEN
  - Identify failure point
  - Apply error handling
  - Retry with fallback
  - Abort if cannot recover
END

### Conditional Execution

IF environment variable set THEN
  - Use variable value
  - Apply environment-specific logic
ELSE
  - Use default value
  - Apply default logic
END

### Multi-Step Execution

Execute step 1
  - Validate result
  - IF result invalid THEN
    - Apply fix
    - Re-validate
  - END

Execute step 2
  - Validate result
  - IF result invalid THEN
    - Apply fix
    - Re-validate
  - END

Continue until all steps complete

### Error Handling

IF command fails THEN
  - Check exit code
  - Display meaningful error
  - Suggest resolution
  - Exit with error code
END

## THREAT MODEL [OPTIONAL]

### Input Validation
Input → Sanitize() → Validate(Safe) → Execute

IF input contains shell metacharacters THEN
  - Sanitize input
  - Validate schema
  - Reject if validation fails
END

IF path traversal detected THEN
  - Reject absolute paths
  - Validate against whitelist
  - Error if path invalid
END

### Destructive Operations

IF destructive operation requested THEN
  - Require User_Confirm
  - Display operation details
  - Display impact assessment
  - Wait(User_Confirm)
END

IF operation is rm OR sudo OR chmod 777 THEN
  - Require User_Confirm
  - Display warning message
  - Wait(User_Confirm)
END

## DEPENDENCIES [OPTIONAL]

### External Tools
- tool1: [version/purpose]
- tool2: [version/purpose]

### Skills
- skill(skill-id): [purpose]

### Dependency Validation

IF tool required THEN
  - Check tool availability
  - Validate tool version
  - Error if tool not installed
END

IF skill required THEN
  - Load skill(skill-id)
  - Verify skill availability
  - Error if skill not found
END

IF dependency missing THEN
  - Error(Dependency not available)
  - List missing dependency
  - Abort command execution
END

## GLOSSARY [RECOMMENDED when abbreviations exist]

**TERM1**: [Definition]
**TERM2**: [Definition]
```
