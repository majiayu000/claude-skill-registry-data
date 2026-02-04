---
name: pal-preflight
description: Pre-flight verification for PAL MCP server availability
---

# PAL Pre-flight Check Skill

Use this skill to verify PAL MCP server is available before starting workflows that depend on it.

## When to Check

- Before `pr-review-manager` starts code review workflow
- Before `architecture-lead` starts architecture analysis
- Before any agent uses `mcp__pal__*` tools

## Required Tools

The following PAL tools must be available:

| Tool | Purpose | Used By |
|------|---------|---------|
| `mcp__pal__codereview` | Multi-model code review | code-reviewer |
| `mcp__pal__consensus` | AI consensus building | architecture-lead |
| `mcp__pal__thinkdeep` | Deep analysis | debug-analyst |
| `mcp__pal__debug` | Debugging assistance | debug-analyst |
| `mcp__pal__analyze` | Code analysis | architecture-analyst |

## Pre-flight Check Protocol

Before starting a workflow, orchestrators MUST:

1. **Attempt to use a PAL tool** (e.g., list models)
2. **If PAL unavailable, ABORT with clear message:**

```
★ CHECKPOINT: Missing Required Dependency

**Required:** PAL MCP Server
**Status:** Not available

The PAL MCP server is required for this workflow.

### Installation
1. Clone PAL: git clone <pal-repo>
2. Install dependencies: npm install
3. Configure in Claude Code settings

### After Installation
Run this workflow again.

### Options
- **A) Abort** - Stop workflow (recommended)
- **C) Continue** - Proceed without PAL (limited functionality)

**[WAIT FOR USER INPUT]**
```

## Degradation is NOT Allowed

Per ADR-003, PAL is a **hard dependency**. Multi-model consensus is a core value proposition.

If user selects "Continue without PAL":
- Warn that code review quality will be severely degraded
- Skip any steps that require PAL tools
- Log warning in workflow output

## Integration Example

Add to orchestrator prompt:

```markdown
## Phase 0: Pre-flight Check

Before starting the workflow:
1. Verify PAL MCP server is available
2. If not available, present the PAL Pre-flight checkpoint
3. Only proceed after confirming PAL availability or user override
```
