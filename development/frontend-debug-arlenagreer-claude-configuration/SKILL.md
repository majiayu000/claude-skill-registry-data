---
name: frontend-debug
description: Autonomously debug frontend issues through empirical browser observation using Chrome DevTools MCP. This skill should be used when debugging UI/UX issues, visual bugs, interaction failures, console errors, or network problems in web applications. Provides systematic 6-phase debugging workflow with GitHub integration, automated verification, and knowledge retention.
---

# Frontend Debug

## Overview

Enable autonomous frontend debugging through empirical browser observation and systematic investigation. This skill implements a structured 6-phase workflow that combines Chrome DevTools MCP for real-world browser testing with automated root cause analysis, fix implementation, and verification. No issue is considered resolved until empirically verified through direct browser interaction.

**Core Principle**: Evidence-based debugging requires direct browser observation. Never assume a fix works without browser verification.

## When to Use This Skill

Invoke this skill for:

- Visual bugs: Elements missing, misaligned, or incorrectly styled
- Interaction failures: Clicks not working, forms not submitting, navigation broken
- Console errors: JavaScript errors, warnings, or unexpected log messages
- Network issues: Failed API requests, incorrect payloads, timeout errors
- Regression detection: Features that stopped working after changes
- GitHub issue debugging: When issue numbers or URLs are referenced

**Activation patterns**:
```bash
# Direct invocation with issue description
@~/.claude/skills/frontend-debug/SKILL.md "Login button not responding"

# With flags for complex issues
@~/.claude/skills/frontend-debug/SKILL.md "Form validation broken" --ultrathink --loop

# From GitHub issue (automatically fetches details)
@~/.claude/skills/frontend-debug/SKILL.md --github-issue 123
@~/.claude/skills/frontend-debug/SKILL.md "#123"  # Shorthand
```

## Workflow Architecture

Execute debugging through 6 systematic phases:

**Phase 0**: Initialization & Context Gathering
**Phase 1**: Browser Investigation & Observation
**Phase 2**: Root Cause Analysis & Fix Strategy
**Phase 3**: Implementation
**Phase 4**: Empirical Verification (MANDATORY)
**Phase 5**: Reporting & Cleanup

**Loop Flag**: If `--loop` is specified, automatically retry Phase 1-4 on verification failure (max 3 iterations).

---

## Phase 0: Initialization & Context Gathering

**Objective**: Establish debugging session and gather complete issue context.

### Step 1: Determine Issue Source

If GitHub issue reference detected (e.g., `--github-issue 123`, `"#123"`, GitHub URL):
1. Load `@contexts/github-integration.md` for GitHub workflow guidance
2. Fetch issue details via gh CLI: `gh issue view <number> --json title,body,labels`
3. Extract reproduction steps, expected vs actual behavior

If inline description provided:
1. Use description as-is for investigation
2. Ask clarifying questions if ambiguous

If no description:
1. Request user to describe: symptoms, steps to reproduce, expected behavior

### Step 2: Detect Project Context

Check for special project configurations:

**SoftTrak Detection**:
- Check if `package.json` contains "softtrak" OR `.softtrak/` directory exists
- If detected → Load `@contexts/softtrak.md` for credentials and auto-correction details

**Git Worktree Detection**:
- Run: `git rev-parse --git-dir | grep "\.git/worktrees"`
- If in worktree → Load `@contexts/worktree.md` for multi-session management

### Step 3: Initialize Session

Create debugging session with tracking:

```bash
# Generate session ID
SESSION_ID="{project-name}-{timestamp}"  # or "{worktree-name}-{timestamp}"

# Create checkpoint file for crash recovery
touch .debug-session-${SESSION_ID}.json

# Initialize TodoWrite with 6-phase tracking
# - Phase 0: Initialization ✅
# - Phase 1: Investigation (pending)
# - Phase 2: Root Cause Analysis (pending)
# - Phase 3: Implementation (pending)
# - Phase 4: Verification (pending)
# - Phase 5: Reporting (pending)
```

### Step 4: Check for Incomplete Sessions

Look for existing checkpoint files:
```bash
ls -la .debug-session-*.json
```

If found, offer to resume from last checkpoint with session state.

**Checkpoint Criteria**: Session initialized, issue understood, TodoWrite created, ready for browser investigation.

---

## Phase 1: Browser Investigation & Observation

**Objective**: Systematically investigate issue through direct browser observation.

**Primary Tool**: Chrome DevTools MCP (MANDATORY - always use `--isolated` flag)

### Investigation Sequence

#### 1. Launch Browser Session

```bash
# CRITICAL: Always use --isolated flag to prevent browser conflicts
# Launch new isolated Chrome instance
# Navigate to application URL
# Handle authentication if required (use login helpers if available)
# Navigate to problematic page/feature
```

#### 2. Capture Initial State

Execute all baseline captures:

```yaml
required_captures:
  - take_snapshot: Document current DOM/UI state
  - take_screenshot: Visual baseline for comparison
  - list_console_messages: Capture all console output (errors, warnings, info)
  - list_network_requests: Capture all network activity (status codes, payloads)
```

#### 3. Reproduce Issue

Follow reproduction steps systematically:
- Execute each step from issue description
- Use browser interaction tools: `click`, `fill`, `hover`, `navigate`
- Observe behavior vs expected behavior at each step
- Document exact failure mode and symptoms

#### 4. Deep Investigation

Execute comprehensive checks:

```yaml
mandatory_checks:
  console_analysis:
    - Identify errors (stack traces, error messages)
    - Note warnings related to issue
    - Check for missing dependencies or failed imports

  network_analysis:
    - Identify failed requests (4xx, 5xx status codes)
    - Inspect request/response payloads
    - Check for timeout errors or slow requests

  dom_analysis:
    - Verify elements exist in DOM via snapshot
    - Check element visibility and styling
    - Validate event listeners are attached

  state_analysis:
    - Inspect localStorage, sessionStorage
    - Check cookies and authentication state
    - Validate application state in console
```

#### 5. Parallel Analysis (if needed)

For complex issues, invoke additional analysis:

- **Sequential MCP**: Multi-step reasoning for complex root cause analysis
- **Context7 MCP**: Framework-specific patterns and debugging approaches
- **Codebase Exploration**: Read relevant source files for context

**Checkpoint Criteria**: Issue reproduced in browser, root cause hypothesis formed with confidence score.

---

## Phase 2: Root Cause Analysis & Fix Strategy

**Objective**: Determine why issue occurs and formulate fix strategy.

### Step 1: Invoke Troubleshooting Analysis

Use SuperClaude troubleshoot command:

```bash
/sc:troubleshoot [detailed-issue-description] --validate --c7 --seq --persona-analyzer
```

This provides structured analysis using:
- Sequential MCP for systematic reasoning
- Context7 MCP for framework patterns
- Analyzer persona for root cause investigation

### Step 2: Formulate Hypothesis

Structure analysis output:

```yaml
root_cause_analysis:
  primary_cause: "Why the issue occurs (e.g., event listener not attached)"
  contributing_factors:
    - "Factor 1 (e.g., async timing issue)"
    - "Factor 2 (e.g., missing dependency)"
  confidence_score: 0.75  # 0.0-1.0 scale
  evidence:
    - "Console error showing specific failure"
    - "Network request returning 404"
    - "DOM element missing expected class"
```

### Step 3: Generate Fix Candidates

Develop 1-3 potential fixes ranked by confidence:

```yaml
fix_candidates:
  option_1:
    approach: "Primary fix strategy"
    confidence: 0.8
    risk: "low"
    rollback: "Easy - single file change"

  option_2:
    approach: "Alternative fix strategy"
    confidence: 0.6
    risk: "medium"
    rollback: "Moderate - multiple files"
```

### Step 4: Request Confirmation (if needed)

If confidence < 70%:
1. Present analysis and proposed fix to user
2. Explain uncertainty and alternatives
3. Request approval before proceeding

**Checkpoint Criteria**: Root cause identified with acceptable confidence, fix strategy approved.

### Step 5: Complexity Escalation Assessment

**After root cause analysis, evaluate debugging complexity for potential agent delegation:**

**Escalation Indicators** (if ANY are true, consider agent delegation):

1. **Low Confidence**: Root cause confidence score **<60%**
2. **Multi-Domain Issue**: Multiple interacting systems involved
   - Example: Network (API) + State (Redux) + UI (rendering)
3. **Systemic Problem**: Issue affects multiple components or features
4. **Deep Investigation**: Requires analysis across **>5 files**
5. **Specialized Analysis**: User explicitly requests domain-specific investigation
6. **Multiple Issues**: User reports 2+ unrelated problems to debug

**Decision Logic**:

If escalation indicators detected:
```yaml
action: delegate_to_agent
reason: "Complex debugging requires specialized sub-agent coordination"
next_step: "Invoke Task tool with frontend-debug-agent"
confidence_requirement: "<60% OR multi_domain:true OR systemic:true"
```

**Agent Invocation Pattern**:
```
Tool: Task
Description: "Complex frontend debugging requiring specialized analysis: [issue-summary]"
Agent Type: root-cause-analyst
Context: {
  browser_evidence: "[screenshots, console logs]",
  reproduction_steps: "[steps from Phase 1]",
  hypothesis: "[from Phase 2 analysis]",
  confidence: "[confidence score]",
  domains_affected: "[network|state|ui|performance]"
}
```

Agent will spawn specialized debugging sub-agents and coordinate investigation.

If escalation indicators NOT detected:
```yaml
action: continue_with_skill
reason: "Confidence acceptable, single-domain issue, skill-based debugging appropriate"
next_step: "Proceed to Phase 3: Implementation"
```

---

**Proceed with skill-based fix implementation:**

## Phase 3: Implementation

**Objective**: Apply fix to codebase following best practices.

### Step 1: Code Modification

Execute fix using appropriate tools:

```yaml
file_operations:
  single_file: Use Edit tool
  multiple_files: Use MultiEdit tool for atomic changes

code_standards:
  - Follow existing code patterns and conventions
  - Add inline comments explaining fix
  - Consider edge cases and error handling
  - Maintain consistent formatting
```

### Step 2: Backend Verification (if applicable)

For issues involving backend changes:

```bash
# Test API endpoints with curl
curl -X POST http://localhost:3000/api/endpoint \
  -H "Content-Type: application/json" \
  -d '{"test": "data"}'

# Check database state if relevant
# Verify server logs for errors
```

### Step 3: Build & Restart (if required)

Execute build process if needed:

```bash
# Rebuild application
npm run build  # or appropriate build command

# Restart dev server
# Clear browser cache if needed
# Verify server is running
```

**Checkpoint Criteria**: Fix implemented in code, application ready for empirical testing.

---

## Phase 4: Empirical Verification (MANDATORY)

**Objective**: Verify fix through direct browser observation.

**CRITICAL**: This phase is MANDATORY. Never skip browser verification. Use Chrome DevTools MCP exclusively.

### Verification Criteria (ALL must pass)

Execute comprehensive verification:

#### 1. UI State Verification ✅

```yaml
checks:
  - Visual appearance matches expected state
  - Elements present and correctly positioned
  - Styling applied correctly
  - Responsive behavior works
  - Screenshot comparison (before/after)
```

#### 2. Console Verification ✅

```yaml
checks:
  - No errors related to the fix
  - No new warnings introduced
  - Expected log messages present
  - Clean console output
```

#### 3. Network Verification ✅

```yaml
checks:
  - All requests succeed (200/201/204 status)
  - Payloads correct in structure and content
  - Response times acceptable
  - No timeout errors
```

#### 4. Interaction Verification ✅

```yaml
checks:
  - Complete user flow works end-to-end
  - All clickable elements respond
  - Forms submit successfully
  - Navigation functions correctly
  - State persists appropriately
```

#### 5. Regression Check ✅

```yaml
checks:
  - Related features still work
  - No new issues introduced
  - Core workflows unaffected
  - Edge cases handled
```

### Verification Process

Execute verification systematically:

```yaml
step_1_prepare:
  - Hard reload browser (Cmd+Shift+R / Ctrl+Shift+R)
  - Clear cached state if needed
  - Return to starting point of user flow

step_2_execute:
  - Reproduce original issue scenario
  - Observe UI state and behavior at each step
  - Monitor console for errors
  - Monitor network for failures

step_3_validate:
  - Compare actual behavior against expected
  - Take final screenshot for evidence
  - Document verification results
  - Note any unexpected observations
```

### Verification Failure Handling

If ANY verification criterion fails:

**With `--loop` flag** (Enhanced with Agent Escalation):

**Iteration 1** (Skill-based):
- Automatically restart from Phase 1
- Re-investigate with new observations in skill context

**If Iteration 1 fails** → Escalation Decision:
```yaml
iteration_1_failed: true
action: "Evaluate complexity for agent delegation"
threshold: "If confidence <50% OR new domains discovered → delegate"
```

**Iterations 2-3** (Agent-based if escalated):
- Invoke frontend-debug-agent for deeper investigation
- Agent spawns specialized sub-agents as needed
- Agent coordinates up to 2 additional iterations
- Maximum total: 1 skill iteration + 2 agent iterations = 3 total

**Rationale**: Keep simple retries in main context, escalate complex cases to agents.

**Without `--loop` flag**:
1. Report verification failure with details
2. Explain which criteria failed and why
3. Request user guidance on next steps

**Checkpoint Criteria**: All 5 verification criteria passed, fix confirmed working.

---

## Phase 5: Reporting & Cleanup

**Objective**: Document findings and close debugging session.

### Step 1: Generate Investigation Report

Create comprehensive report:

```markdown
# Frontend Debug Report: {Issue Title}

## Summary
[One-line description of issue and fix]

## Root Cause
[Detailed explanation of why issue occurred]

## Fix Applied
[What was changed and why it resolves the issue]

## Verification Results
- ✅ UI State: [Details]
- ✅ Console: [Details]
- ✅ Network: [Details]
- ✅ Interactions: [Details]
- ✅ Regression: [Details]

## Evidence
- Before Screenshot: [path]
- After Screenshot: [path]
- Console Logs: [relevant logs]
- Network Activity: [relevant requests]

## Recommended Tests
[Suggested regression tests to prevent future issues]

## Session Details
- Session ID: {session-id}
- Duration: {elapsed-time}
- Iterations: {loop-count}
```

### Step 2: GitHub Integration (if applicable)

If debugging from GitHub issue:

```bash
# Post resolution comment with report
gh issue comment <number> --body "[report-content]"

# Add resolved label to indicate fix has been applied and verified
gh issue edit <number> --add-label "resolved-by-claude"

# Remove automated-debug label if present
gh issue edit <number> --remove-label "automated-debug"

# DO NOT automatically close the issue
# Let human developers review the fix and close manually
# This ensures proper validation and prevents premature closure
```

### Step 3: Session Cleanup

Clean up debugging artifacts:

```bash
# Mark all TodoWrite tasks as completed
# Delete checkpoint file: rm .debug-session-${SESSION_ID}.json
# Close browser session via Chrome DevTools MCP
# Save final report to appropriate location
```

### Step 4: Knowledge Base Update (optional but recommended)

Store learning for future debugging:

```json
{
  "issue_pattern": "description of issue type",
  "root_cause_category": "async timing | network | state management | etc",
  "solution_pattern": "approach that resolved issue",
  "detection_signals": ["symptom 1", "symptom 2"],
  "fix_template": "reusable solution approach"
}
```

**Checkpoint Criteria**: Report generated, GitHub issue updated (if applicable), session cleaned up.

---

## Error Handling

### Browser Session Failures

```yaml
chrome_devtools_unavailable:
  symptom: "MCP connection fails"
  action: "Check Chrome DevTools MCP configuration in .mcp.json"
  fallback: "Request user to verify MCP setup and Chrome installation"

browser_already_running:
  symptom: "Port conflict or existing instance"
  cause: "--isolated flag not used"
  solution: "Always use --isolated=true for new debugging sessions"

navigation_timeout:
  symptom: "Page load timeout"
  action: "Increase timeout or check network connectivity"
  fallback: "Request user to verify application is running and accessible"

authentication_required:
  symptom: "Login page or auth wall"
  action: "Use project-specific login helper if available"
  fallback: "Request user credentials or authentication approach"
```

### Verification Failures

```yaml
fix_does_not_work:
  with_loop_flag:
    action: "Automatically restart Phase 1 (max 3 iterations)"
    logging: "Document why previous fix failed"

  without_loop_flag:
    action: "Report failure with detailed explanation"
    next_step: "Request user guidance on alternative approaches"

new_issue_introduced:
  action: "Rollback changes to previous working state"
  logging: "Document regression details"
  next_step: "Re-analyze with different fix strategy"

partial_success:
  action: "Document which criteria passed vs failed"
  decision: "Discuss with user whether partial fix is acceptable"
```

### GitHub Integration Failures

```yaml
gh_cli_not_available:
  symptom: "gh command not found"
  action: "Warn user to install: brew install gh"
  fallback: "Continue with manual issue description"

issue_not_found:
  symptom: "Issue number doesn't exist"
  action: "Verify issue number and repository"
  fallback: "Request user to provide issue details manually"

authentication_failed:
  symptom: "gh auth required"
  action: "Guide user through: gh auth login"
  fallback: "Continue without GitHub integration"
```

### Tool Reference Failures

If encountering errors with Chrome DevTools MCP tools:
1. Load `@references/mcp-tools.md` for detailed tool documentation
2. Review proper tool usage and parameters
3. Check for MCP configuration issues

---

## Conditional Context Loading

**Design Principle**: Load additional context only when detected or needed to optimize token usage.

### When to Load Additional Context

**GitHub Integration** → Load `@contexts/github-integration.md`
- **Trigger**: `--github-issue` flag OR GitHub issue reference detected (#123, URLs)
- **Provides**: Issue lifecycle management, gh CLI commands, automated tracking
- **Token Cost**: +1,000 tokens

**SoftTrak Project** → Load `@contexts/softtrak.md`
- **Trigger**: `package.json` contains "softtrak" OR `.softtrak/` directory exists
- **Provides**: Test credentials, auto-correction, project-specific configurations
- **Token Cost**: +600 tokens

**Git Worktree** → Load `@contexts/worktree.md`
- **Trigger**: `git rev-parse --git-dir | grep "\.git/worktrees"` succeeds
- **Provides**: Multi-session management, browser isolation strategies
- **Token Cost**: +400 tokens

**Tool Reference** → Load `@references/mcp-tools.md`
- **Trigger**: Agent encounters tool errors OR needs specific tool guidance
- **Provides**: Detailed Chrome DevTools MCP tool reference with examples
- **Token Cost**: +2,000 tokens

**Usage Examples** → Load `@references/examples.md`
- **Trigger**: User requests examples OR agent needs workflow clarification
- **Provides**: Example scenarios, expected workflows, common patterns
- **Token Cost**: +1,500 tokens

---

## Resources

This skill includes organized resources for effective debugging:

### scripts/

**`cleanup-sessions.sh`**
- Remove stale debug session checkpoint files
- Execute periodically to prevent workspace clutter
- Usage: `bash scripts/cleanup-sessions.sh`

### references/

**`mcp-tools.md`** - Detailed Chrome DevTools MCP tool reference
- Load when encountering tool errors
- Provides comprehensive tool usage examples
- Includes parameter documentation

**`examples.md`** - Example debugging scenarios
- Load when needing workflow clarification
- Shows realistic debugging sessions
- Demonstrates best practices

### contexts/

**`github-integration.md`** - GitHub issue lifecycle management
- Load when `--github-issue` flag used or issue reference detected
- Provides gh CLI command reference
- Documents automated tracking workflow

**`softtrak.md`** - SoftTrak project configuration
- Load when SoftTrak project detected
- Provides test credentials and auto-correction details
- Documents project-specific patterns

**`worktree.md`** - Git worktree multi-session support
- Load when in git worktree environment
- Provides browser isolation strategies
- Documents concurrent debugging workflows

### templates/

**`investigation-report-template.md`** - Report structure template
**`verification-checklist.md`** - Verification criteria checklist
**`session-state-schema.json`** - Session checkpoint schema
**`mcp-config-example.json`** - Chrome DevTools MCP configuration example

### Knowledge Base

**`knowledge-base.json`** - Stored debugging patterns and solutions
**`framework-quirks.json`** - Framework-specific gotchas and patterns
**`project-contexts/softtrak.json`** - SoftTrak project data

---

## Best Practices

1. **Always Use Chrome DevTools MCP**: Empirical verification requires real browser observation
2. **Always Use --isolated Flag**: Prevents browser conflicts in concurrent debugging sessions
3. **Load Context Conditionally**: Only load additional modules when detection patterns match
4. **Document Thoroughly**: Maintain detailed checkpoint files for crash recovery
5. **Verify Empirically**: Never assume a fix works without browser verification in Phase 4
6. **Loop When Uncertain**: Use `--loop` flag for complex issues requiring iteration
7. **GitHub Integration**: Use issue tracking for accountability and knowledge retention
8. **Session Management**: Create checkpoint files for recovery from crashes or interruptions

---

## Performance & Token Optimization

**Modular Loading Strategy**: Conditional loading minimizes token usage.

**Token Budget**:
- Core Workflow (SKILL.md): ~4,500 tokens
- GitHub Integration: +1,000 tokens (conditional)
- SoftTrak Context: +600 tokens (conditional)
- Worktree Support: +400 tokens (conditional)
- Tool Reference: +2,000 tokens (conditional)
- Usage Examples: +1,500 tokens (conditional)

**Total Range**: 4,500 tokens (minimal) to 10,000 tokens (all modules loaded)

**Optimization**: Load only what's needed based on detection patterns, achieving 30-70% token savings vs loading everything upfront.
