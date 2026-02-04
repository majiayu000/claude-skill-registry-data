---
name: managing-hooks
description: Creates, analyzes, updates, and improves Claude Code hooks including configuration, scripts, and security validation. Use when user asks how hooks work, explaining hook concepts, understanding hook types and event lifecycle, describing hook configuration, creating new hooks, analyzing existing hooks for improvements, validating hook security, debugging hook activation, updating hook configurations, or when user mentions "hook", "PreToolUse", "PostToolUse", "SessionStart", or other hook event types. Handles both command hooks and prompt-based hooks across all 9 event types.
---

# Managing Hooks

Comprehensive management of Claude Code hooks including creation, analysis, updates, and security validation.

## When to Use This Skill

Activate this skill when:
- User requests creation of a new hook
- User asks to analyze or improve existing hooks
- User needs to validate hook security
- User mentions debugging hook activation or behavior
- User asks if current logic should become a hook
- User mentions specific hook types: PreToolUse, PostToolUse, UserPromptSubmit, SessionStart, SessionEnd, Stop, SubagentStop, Notification, PreCompact
- User provides hook configuration or scripts for review
- User asks about hook best practices or patterns

## Core Concepts

**Hooks** are automated shell commands that execute at specific Claude Code lifecycle points, providing deterministic control over behavior.

**Key Characteristics**:
- Execute automatically with environment credentials
- Run in parallel with 60-second default timeout
- Receive JSON input via stdin
- Return control via exit codes and optional JSON output
- Security critical: must validate inputs and prevent injection

**Hook Locations**:
- User hooks: `~/.claude/settings.json`
- Project hooks: `.claude/settings.json`
- Local hooks: `.claude/settings.local.json`

## Workflow 1: Creating New Hooks

### Step 1: Determine Hook Type and Event

First, identify which hook event type is appropriate:

**Tool-Based Events** (require matcher):
- **PreToolUse**: Block or modify tool calls before execution
- **PermissionRequest**: Allow or deny permission dialogs
- **PostToolUse**: Process results after tool completion

**Lifecycle Events** (no matcher needed):
- **SessionStart**: Initialize environment at session start
- **SessionEnd**: Cleanup at session termination

**Agent Events**:
- **Stop**: Decide whether to continue after agent response
- **SubagentStop**: Control continuation after subagent tasks

**Context Events**:
- **UserPromptSubmit**: Validate or inject context before processing prompts
- **Notification**: Respond to permission requests or waiting messages
- **PreCompact**: Prepare for context compaction

Ask user:
- What should trigger the hook? (specific tool, session event, etc.)
- What should the hook do? (validate, transform, log, block, etc.)
- Should it block operations or just observe?

Load hook-types-reference.md now for detailed specifications on each event type.

### Step 2: Design Hook Behavior

Define the hook's logic:

**Input Processing**:
- What data does hook need from stdin JSON?
- Which fields are required: tool_name, tool_input, tool_response, session_id, cwd?

**Decision Logic**:
- What conditions trigger hook actions?
- What validation rules apply?
- What patterns should be detected?

**Output Requirements**:
- Exit code: 0 (success), 2 (block), other (non-blocking error)
- Use official response schema with fields: continue, suppressOutput, systemMessage, hookSpecificOutput
- For complex hooks, consider structured JSON in additionalContext for precise Claude instructions

Load official-response-schema.md for complete schema details and structured JSON guidance.

**Security Considerations**:
- What inputs need validation?
- Are file paths sanitized?
- Are shell commands properly quoted?
- Could this exfiltrate sensitive data?

Load security-checklist.md now for comprehensive security validation requirements.

### Step 3: Create JSON Configuration

Build the hooks configuration structure:

**For Tool-Based Hooks**:
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/script-name.sh",
            "timeout": 60000
          }
        ]
      }
    ]
  }
}
```

**For Lifecycle Hooks**:
```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/session-start.sh"
          }
        ]
      }
    ]
  }
}
```

**Matcher Patterns**:
- Simple string: `"Bash"` or `"Write"`
- Multiple tools: `"Bash|Write|Edit"`
- Regex: `"mcp__memory__.*"` (all memory server tools)
- Wildcard: `"mcp__.*__write.*"` (all write tools across MCP servers)

Load configuration-guide.md for detailed JSON structure guidance and advanced patterns.

### Step 3.5: Prompt-Based Hooks (Optional)

For advanced decision-making, use LLM-based hooks instead of shell commands:

**When to Use Prompt Hooks**:
- Stop/SubagentStop: Let LLM decide if Claude should continue
- UserPromptSubmit: Validate prompts with natural language understanding
- PreToolUse/PermissionRequest: Context-aware permission decisions

**Basic Configuration**:
```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Should Claude continue? Check: all tasks complete? errors resolved? follow-up work needed? Respond: {\"decision\": \"approve\"|\"block\", \"reason\": \"...\"}",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

**Key Differences from Command Hooks**:
- `type: "prompt"` instead of `command`
- LLM responds with structured JSON (decision, reason, continue, etc.)
- Timeout in seconds (default: 30)
- Only supported for: Stop, SubagentStop, UserPromptSubmit, PreToolUse, PermissionRequest

**Response Schema**: LLM returns JSON with `decision` (approve/block), `reason`, optional `continue` (false to stop), `stopReason`, `systemMessage`.

Load prompt-hooks-guide.md for complete documentation on prompt-based hooks including response schema, examples, and decision patterns.

### Step 4: Write Hook Script

Choose script language (bash or python) and implement:

**Bash Script Template**:
```bash
#!/bin/bash
set -e

# Read JSON input from stdin
INPUT=$(cat)

# Parse required fields (use jq if available, or basic parsing)
TOOL_NAME=$(echo "$INPUT" | grep -o '"tool_name":"[^"]*"' | cut -d'"' -f4)

# Implement hook logic here

# Exit with appropriate code
exit 0  # Success
# exit 2  # Block operation
```

**Python Script Template**:
```python
#!/usr/bin/env python3
import json
import sys

# Read input from stdin
input_data = json.load(sys.stdin)

tool_name = input_data.get("tool_name", "")
tool_input = input_data.get("tool_input", {})

# Implement hook logic here

# Exit appropriately
sys.exit(0)  # Success
# sys.exit(2)  # Block operation
```

**Script Requirements**:
- Shebang line at top
- Read JSON from stdin
- Handle missing fields gracefully
- Quote all variables in bash
- Use absolute paths
- Include error handling
- Make executable: `chmod +x script-name.sh`

Load script-examples.md for complete examples from Claude cookbooks including audit logging, safety checks, and validation patterns.

### Step 5: Security Validation

**Critical Security Checks**:

✅ **Input Validation**:
- Validate all inputs before use
- Check file paths for traversal attempts (`../`, absolute paths)
- Sanitize user-provided strings
- Reject unexpected input patterns

✅ **Command Safety**:
- Quote all variables: `"$VARIABLE"` not `$VARIABLE`
- Use absolute paths for commands
- Avoid `eval` or dynamic command construction
- Validate before executing shell commands

✅ **Data Protection**:
- Never log sensitive data (API keys, passwords)
- Check if hook could exfiltrate credentials
- Avoid writing sensitive data to files
- Be careful with environment variables

✅ **Path Security**:
- Block path traversal: `../../../etc/passwd`
- Use absolute paths or validated relative paths
- Check file permissions before writing
- Avoid world-writable locations

✅ **Error Handling**:
- Fail safely (don't expose system details)
- Log errors appropriately
- Don't leak sensitive info in error messages

Load security-checklist.md now for detailed validation requirements before deploying any hook.

### Step 6: Test and Deploy

**Testing Steps**:
1. Test script independently (provide sample JSON via stdin)
2. Add configuration to appropriate settings file
3. Restart Claude Code to load hooks
4. Verify registration: `/hooks` command
5. Trigger hook with appropriate action
6. Check behavior and output
7. Enable debug mode: `claude --debug` for detailed logs

**Validation**:
- [ ] Hook appears in `/hooks` output
- [ ] Hook activates on expected triggers
- [ ] Hook blocks operations correctly (if PreToolUse)
- [ ] Hook produces expected output
- [ ] No errors in debug logs
- [ ] Security validation passed
- [ ] Script has execute permissions

**Deployment**:
- Personal hooks: `~/.claude/settings.json` and `~/.claude/hooks/`
- Project hooks: `.claude/settings.json` and `.claude/hooks/` (commit to git)
- Document hook purpose and behavior for team

Load debugging-guide.md for troubleshooting common issues.

## Workflow 2: Analyzing Existing Hooks

### Step 1: Load Hook Configuration

Read the hooks configuration from settings files:

1. Use Read tool on settings files:
   - `~/.claude/settings.json`
   - `.claude/settings.json`
   - `.claude/settings.local.json`

2. Parse hooks structure:
   - Identify all configured hook events
   - List matchers for each hook
   - Note script paths for each hook

3. List hook scripts:
   - Use Glob tool: `**/*.sh` and `**/*.py` in `.claude/hooks/`
   - Use Read tool to load each script

### Step 2: Review Hook Scripts

Analyze each hook script for:

**Functionality**:
- What does the hook do?
- Is the logic clear and appropriate?
- Are there unnecessary operations?

**Code Quality**:
- Is input parsing robust?
- Is error handling adequate?
- Are variables properly quoted (bash)?
- Is the script maintainable?

**Best Practices**:
- Does it use proper shebang?
- Are exit codes used correctly?
- Is JSON output formatted properly?
- Are environment variables used appropriately?

**Efficiency**:
- Could it be simplified?
- Are there redundant operations?
- Is execution time reasonable?

### Step 3: Security Assessment

Apply security checklist to each hook:

**Input Validation**:
- [ ] All inputs validated before use
- [ ] Path traversal prevention implemented
- [ ] User input sanitized appropriately

**Command Safety**:
- [ ] Variables properly quoted
- [ ] No dynamic command construction
- [ ] Absolute paths used
- [ ] No dangerous commands (eval, etc.)

**Data Protection**:
- [ ] No sensitive data in logs
- [ ] No credential exfiltration risk
- [ ] Appropriate file permissions
- [ ] Secure temporary file handling

**Configuration Security**:
- [ ] Matchers appropriately scoped
- [ ] Timeouts reasonable
- [ ] Tool restrictions make sense
- [ ] No overly permissive patterns

Load security-checklist.md for comprehensive assessment criteria.

### Step 4: Suggest Improvements

Categorize findings:

**Critical Issues** (must fix):
- Security vulnerabilities
- Broken functionality
- Invalid configuration
- Missing security checks

**Major Improvements** (should fix):
- Poor error handling
- Inefficient logic
- Unclear code
- Missing validation

**Minor Enhancements** (nice to have):
- Code clarity improvements
- Better comments
- Optimization opportunities
- Additional features

Provide specific recommendations:
- What to change
- Why it improves the hook
- How to implement
- Updated code if applicable

## Workflow 3: Updating Hooks

### Step 1: Identify Update Needs

Determine what needs updating:

**Outdated Patterns**:
- Old hook event types (pre-deprecation)
- Changed JSON input structure
- Updated security requirements
- New best practices

**New Features**:
- Additional validation needed
- New tools to match
- Enhanced error handling
- Better logging

**Bug Fixes**:
- Incorrect logic
- Security issues
- Edge cases not handled
- Performance problems

### Step 2: Plan Updates

Design the update strategy:

**Preserve Functionality**:
- Identify working behavior to maintain
- List dependencies on current implementation
- Plan backward compatibility if needed

**Update Approach**:
- Can update in place or needs rewrite?
- Configuration changes required?
- Script changes required?
- Testing strategy

**Risk Assessment**:
- What could break?
- Impact on existing workflows?
- Rollback plan if needed?

### Step 3: Implement Changes

Execute the update:

**Configuration Updates**:
1. Use Edit tool to modify settings.json
2. Update matcher patterns if needed
3. Adjust timeouts or tool restrictions
4. Add new hooks or remove deprecated ones

**Script Updates**:
1. Use Edit tool to modify hook scripts
2. Add new validation logic
3. Improve error handling
4. Update security measures
5. Add or improve comments

**Testing**:
1. Restart Claude Code to reload hooks
2. Verify hooks load without errors
3. Test updated functionality
4. Validate security improvements

### Step 4: Validate Updates

Ensure updates are successful:

- [ ] Hook configuration valid JSON
- [ ] Scripts have no syntax errors
- [ ] Hooks load successfully (check `/hooks`)
- [ ] Hooks activate appropriately
- [ ] New functionality works as expected
- [ ] No regressions in existing behavior
- [ ] Security improvements verified
- [ ] Documentation updated if needed

## Workflow 4: Working with Plugin Hooks

Plugin hooks enable distributed hook composition across installed plugins.

### Plugin Hook Basics

**Locations**:
- Plugin hooks defined in: `plugin-root/hooks/hooks.json` or custom path
- Environment variables available:
  - `${CLAUDE_PLUGIN_ROOT}`: Absolute path to plugin directory
  - `${CLAUDE_PROJECT_DIR}`: Project root directory
  - All standard environment variables

**Key Differences from Project/User Hooks**:
- Automatically merged when plugin is enabled
- Run alongside user and project hooks (not instead of)
- Support both command and prompt-based types
- Use plugin-relative paths with `${CLAUDE_PLUGIN_ROOT}`

### Plugin Hook Configuration

```json
{
  "description": "Plugin hook description",
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/format.sh",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

### Plugin Hook Execution Order

When multiple hooks match an event:
1. All matching hooks execute in parallel
2. Plugin hooks run alongside user hooks (both active)
3. If hook blocks (exit 2), blocking hook behavior applies
4. Multiple hooks don't cancel each other

Load plugin-hooks-guide.md for comprehensive coverage including plugin hook composition patterns, multi-plugin scenarios, and integration examples.

## Workflow 5: Suggesting Hook Creation

When evaluating whether current logic should become a hook:

**Evaluation Criteria**:
- Is this logic repeated frequently?
- Should it happen automatically vs. relying on LLM?
- Does it enforce a policy or requirement?
- Would it improve consistency?
- Is it tied to specific tool usage?

**Good Hook Candidates**:
- Automated formatting after file writes
- Security validation before operations
- Compliance tracking and logging
- Environment setup/teardown
- Permission enforcement
- Desktop notifications

**Poor Hook Candidates**:
- One-time operations
- Complex decision-making (use LLM instead)
- Highly context-dependent logic
- Frequently changing requirements

If appropriate, explain:
- Which hook type would work
- What the hook would do
- Benefits of automation
- Implementation approach

Then offer to create the hook using Workflow 1.

## Progressive Disclosure References

Load these files when detailed guidance is needed:

**Core References**:
- **hook-schemas-reference.md**: Complete input/output schemas for all 9 hook event types, including event-specific fields, matcher behaviors, and response fields for each event
- **official-response-schema.md**: Complete official Claude Code hook response schema with all fields, advanced structured JSON in additionalContext, field purposes, and migration guide
- **hook-types-reference.md**: Complete specifications for all 9 hook event types, input/output fields, matchers, and use cases

**Advanced Topics**:
- **prompt-hooks-guide.md**: Comprehensive guide to prompt-based hooks (type: "prompt"), LLM decision making, response schemas, examples, and use cases for intelligent decision-making
- **plugin-hooks-guide.md**: Complete coverage of plugin hook composition, distributed hook systems, environment variables, multi-plugin scenarios, and integration patterns
- **configuration-guide.md**: Detailed JSON structure, matcher patterns, tool restrictions, timeout configuration, MCP integration

**Implementation & Examples**:
- **script-examples.md**: Complete bash and python examples from Claude cookbooks including audit logging, safety validation, and automation patterns
- **security-checklist.md**: Comprehensive security validation requirements, common vulnerabilities, prevention techniques
- **debugging-guide.md**: Troubleshooting activation issues, using /hooks command, debug mode, common errors and solutions
- **templates/**: Ready-to-use templates for hook configuration JSON, bash scripts, and python scripts
- **real-world-examples/**: Practical examples from Claude projects including prompt-based stop hooks, plugin hooks, and MCP tool validation

## Quick Reference

**Environment Variables**:
- `$CLAUDE_PROJECT_DIR`: Project root path
- `$CLAUDE_ENV_FILE`: Environment persistence file (SessionStart only)
- `$CLAUDE_CODE_REMOTE`: Remote execution indicator
- `${CLAUDE_PLUGIN_ROOT}`: Plugin directory

**Exit Codes**:
- `0`: Success, allow operation
- `2`: Block operation (behavior varies by event)
- Other: Non-blocking error

**Common Matchers**:
- Single tool: `"Bash"` or `"Write"`
- Multiple tools: `"Bash|Write|Edit"`
- All MCP tools from server: `"mcp__server-name__.*"`
- Specific MCP tool: `"mcp__server__tool-name"`

**Security Red Flags**:
- Unquoted variables in bash
- Path concatenation without validation
- Logging sensitive data
- Using `eval` or dynamic commands
- Missing input validation
- World-writable file operations

## Validation Checklist

Before deploying any hook:

**Configuration**:
- [ ] Valid JSON syntax
- [ ] Appropriate hook event type chosen
- [ ] Matcher correctly targets intended tools
- [ ] Script path correct and uses `$CLAUDE_PROJECT_DIR` if needed
- [ ] Timeout appropriate for operation

**Script**:
- [ ] Shebang line present
- [ ] Executable permission set (`chmod +x`)
- [ ] Reads JSON from stdin
- [ ] Parses required fields
- [ ] Handles missing fields gracefully
- [ ] Uses correct exit codes
- [ ] Outputs JSON if needed

**Security**:
- [ ] All inputs validated
- [ ] Variables quoted properly
- [ ] No path traversal vulnerabilities
- [ ] No command injection possible
- [ ] No sensitive data exposure
- [ ] Fail-safe error handling

**Testing**:
- [ ] Hook loads without errors
- [ ] Hook activates on correct triggers
- [ ] Hook behaves as expected
- [ ] Debug logs show no errors
- [ ] Team tested (for project hooks)

## Common Patterns

**Pre-Write Safety Hook** (Command):
- Validate file paths
- Warn about protected files
- Check directory conventions

**Post-Tool Audit Hook** (Command):
- Log tool usage
- Track file modifications
- Maintain compliance history

**Session Setup Hook** (Command):
- Verify environment dependencies
- Check configuration files
- Display status information

**Bash Command Safety Hook** (Command):
- Detect dangerous commands
- Warn about destructive operations
- Suggest best practices

**Intelligent Stop Decision** (Prompt):
- Analyze conversation to decide if tasks complete
- Check for unresolved errors
- Determine if follow-up work needed

**Context-Aware Permission** (Prompt):
- Let LLM evaluate if tool use is appropriate
- Consider conversation context
- Make natural language decisions

See prompt-hooks-guide.md for detailed prompt-based patterns with examples.

## Anti-Patterns to Avoid

- Hooks with complex business logic (use LLM instead)
- Hooks that fail silently without logging
- Overly broad matchers that catch unintended tools
- Synchronous operations that slow down workflow
- Hooks without security validation
- Hardcoded paths instead of environment variables
- Missing error handling

## Output Format

When completing hook management tasks:

1. **Summary**: What was done
2. **Configuration**: JSON structure created/modified
3. **Scripts**: Scripts created/modified with paths
4. **Security**: Security considerations addressed
5. **Testing**: How to test the hook
6. **Deployment**: Where to place files and how to activate
