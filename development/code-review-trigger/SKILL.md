---
name: code-review-trigger
description: Natural language wrapper for code review - automatically triggers /code-review when users express intent to review code, check for bugs, or validate code quality
schema_version: 1.0
---

# code-review-trigger

**Type:** ANALYSIS-ONLY
**DAIC Modes:** DISCUSS, ALIGN, IMPLEMENT, CHECK (all modes)
**Priority:** High

## Trigger Reference

This skill activates on:
- **Keywords:** "review code", "code review", "check for bugs", "validate code", "find issues", "analyze code", "check quality", "code quality", "review this", "check this code", "inspect code", "audit code", "review changes", "review file"
- **Intent Patterns:** `(review|check|validate|analyze).*?(code|file|changes|this)`, `(find|detect|look for).*?(bug|issue|problem|error)`, `code.*?quality`, `(inspect|audit).*?(code|file|changes)`

From: `skill-rules.json` - code-review-trigger configuration

## Purpose

Automatically trigger the `/code-review` slash command when users express intent to review code, check for bugs, or validate code quality using natural language. This skill eliminates the need to remember the exact `/code-review` syntax.

## Core Behavior

In any DAIC mode:

1. **Natural Language Detection**
   - Detect when user wants code review without using slash command
   - Examples: "Review this code", "Check for bugs", "Is this code good?"
   - Automatically invoke `/code-review` with appropriate arguments

2. **Context Extraction**
   - Extract what should be reviewed from user's message
   - Examples: "Review src/auth.js" → args: "src/auth.js"
   - "Check for bugs in recent changes" → args: "recent changes"
   - "Review this" (with file in context) → args: infer from context

3. **Slash Command Invocation**
   - Call `/code-review` command with extracted arguments
   - Pass through to multi-aspect parallel code review system
   - Return results to user

## Natural Language Examples

**Triggers this skill:**
- ✓ "Review this code"
- ✓ "Check for bugs in src/"
- ✓ "Validate code quality"
- ✓ "Find issues in my changes"
- ✓ "Analyze this file for problems"
- ✓ "Code review the recent commits"
- ✓ "Inspect the authentication logic"
- ✓ "Audit the API endpoints"

**Does NOT trigger (too generic):**
- ✗ "Code" (just mentions code)
- ✗ "Files" (no review intent)
- ✗ "What changed?" (status check, not review)

## Safety Guardrails

**ANALYSIS-ONLY RULES:**
- ✓ NEVER call write tools (Edit, Write, MultiEdit)
- ✓ Only invokes /code-review command which is read-only
- ✓ Safe to run in any DAIC mode
- ✓ Provides analysis and suggestions only

**Invocation Rules:**
- Only invoke /code-review when clear review intent detected
- Extract specific targets from natural language when possible
- Default to reviewing recent changes if no target specified
- Never auto-fix issues (code-review is analysis-only)

## Implementation Notes

This skill acts as a natural language wrapper around `/code-review`. The actual code review logic lives in `.claude/commands/code-review.md`, which:
- Launches parallel code-review-expert agents
- Analyzes code quality, security, performance, etc.
- Returns comprehensive review findings

This skill simply detects the intent and routes to that command.
