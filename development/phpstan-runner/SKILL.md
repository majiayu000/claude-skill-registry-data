---
name: phpstan-runner
description: |
  Run PHPStan static analysis and fix errors using intelligent agent delegation. Use when user requests to:
  - Run static analysis
  - Fix PHPStan errors
  - Check code quality
  - Analyze type errors
  Delegates to runner agent (haiku) for execution and fixer agent (sonnet) for fixes.
  Automatically cycles between run and fix until analysis passes or human intervention needed.
allowed-tools: Task
---

# PHPStan Runner Skill

This skill provides intelligent PHPStan static analysis and fixing through specialized agent delegation.

## Agent Delegation Strategy

This skill delegates to specialized agents via the Task tool:

1. **php-qa-ci_phpstan-runner agent (haiku model)** - Runs analysis and parses results
2. **php-qa-ci_phpstan-fixer agent (sonnet model)** - Analyzes and fixes errors
3. **Escalation** - Uses opus model or asks human for stubborn issues

## Workflow

### When User Says: "Run PHPStan"

1. Launch runner agent:
   ```
   Use Task tool:
     description: "Run PHPStan analysis"
     subagent_type: "php-qa-ci_phpstan-runner"
     prompt: "Run PHPStan static analysis and provide summary"
   ```

2. Receive runner output with log location

3. If errors detected:
   - Launch fixer agent:
     ```
     Use Task tool:
       description: "Fix PHPStan errors"
       subagent_type: "php-qa-ci_phpstan-fixer"
       prompt: "Fix errors in log: {log_path}"
     ```

4. After fixes applied, re-run via runner agent

5. Repeat cycle until:
   - Analysis passes → Success
   - Same errors persist 2+ times → Escalate to opus or human
   - User intervention needed → Ask user

### When User Says: "Fix the PHPStan errors"

1. Check if recent log exists in var/qa/phpstan_logs/

2. If log found:
   - Launch fixer agent directly with log path

3. If no log:
   - Launch runner agent first to generate log
   - Then launch fixer agent

### Escalation Triggers

Launch opus model or ask human when:
- Fixer agent reports "cannot fix" for same error 2+ times
- Architecture questions arise (design patterns, type hierarchies)
- User explicitly requests explanation of errors

## Runner Agent Reference

The phpstan-runner agent (haiku model) handles:
- PHPStan execution with proper configuration
- Log parsing for error patterns
- Concise summary generation

See `.claude/agents/php-qa-ci_phpstan-runner.md` for agent implementation details.

## Fixer Agent Reference

The phpstan-fixer agent (sonnet model) handles:
- Log file discovery and parsing
- Error grouping by pattern
- Fix implementation for common PHPStan issues
- Verification that fixes resolve issues

See `.claude/agents/php-qa-ci_phpstan-fixer.md` for agent implementation details.
