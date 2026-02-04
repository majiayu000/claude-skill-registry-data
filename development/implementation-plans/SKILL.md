---
name: implementation-plans
description: Creates concise, executable implementation plans for solo developer working with AI agents. Validates assumptions, avoids timelines, focuses on actionable steps with clear human/AI delegation.
---

# Implementation Plans Skill

This skill guides creation of implementation plans for solo implementers working with AI agents (not teams requiring approval).

## Core Principles

### Context
- **Solo implementer**: Bobby + AI agents, not requiring team approvals or stakeholder sign-offs
- **Small team**: 3 engineers with different focus areas
- **Fast execution**: Plans completed in days/hours, not weeks
- **AI execution model**: All implementation steps involve AI agents

### Non-Negotiables
1. **No timelines or estimates** - Provide sequence and dependencies only
2. **Validate assumptions first** - Ask clarifying questions or flag for verification
3. **Brutally concise** - If team ignores it, it's too long
4. **AI-ready steps** - Frame as "Have AI do X" vs "Review/verify Y manually"
5. **No stakeholder theater** - Skip approval phases, sign-off steps, team alignment meetings

## Process

### 1. Start with Clarifying Questions
Before writing any plan, ask questions to validate assumptions:
- What does the actual data look like?
- Do we have confirmed access/permissions?
- Are there known constraints or requirements?
- Which tools/libraries/versions are we using?

### 2. Build the Plan

Structure:
```markdown
## [Task Name]

### Verification Steps (if assumptions can't be validated upfront)
1. Verify [assumption] by [method]

### Implementation
1. Have AI [specific action]
   - Context: [relevant details]
   - Expected output: [what to verify]

2. Review [output] for [specific concerns]

3. Manually verify [critical check]

### Dependencies
- [What must complete first]

### 🚨 Unvalidated Assumptions
- [List assumptions that need verification during execution]
```

Keep total plan under 500 words. If you need more detail, split into main plan + technical appendix.

### 3. Focus on Reality
- If you can't validate something with web search or available context, ASK or FLAG it
- Never confidently declare solutions built on unverified assumptions
- When debugging, check actual data before analyzing code
- Remember: obvious data issues > complex code analysis

## Common Failure Patterns

### ❌ The Assumption Cascade
Building multi-step plans on unverified assumptions that collapse when reality doesn't match.

**Fix**: Front-load verification or flag assumptions explicitly

### ❌ The Confident Wrong Answer
Declaring root cause without seeing actual data or system state.

**Fix**: Include data inspection steps before solution steps

### ❌ The Enterprise Theater
Including approval gates, week-based timelines, team alignment meetings.

**Fix**: Assume work is approved, sequence steps by technical dependency only

## Progressive Disclosure

For detailed guidance, reference these files:

**Validation practices**: `validation-checklist.md`
- Comprehensive assumption checklist
- Common technology gotchas
- Data validation patterns

**AI delegation**: `ai-delegation-patterns.md`
- How to frame steps for AI execution
- When human review is critical
- Context requirements for AI tasks

**Examples**: `examples/`
- Good plan: database migration
- Bad plan: stakeholder-heavy approach
- Complex plan: RAG pipeline implementation

Load these only when additional context would help create a better plan.

## Quick Reference

**Good step**: "Have AI generate migration script adding `preferences JSONB` column with rollback"

**Bad step**: "Update the database" (too vague)

**Good verification**: "Check current schema: `SELECT column_name...`"

**Bad verification**: "Ensure database is ready" (unclear how)

**Good flag**: "🚨 Verify: Azure AI Search tier supports semantic ranking"

**Bad flag**: Assuming it works without checking
