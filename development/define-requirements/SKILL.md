---
name: define-requirements
description: "Guides users through Jobs-to-be-Done discovery to define feature requirements before implementation. Use when user wants to define, document, or plan a new feature or enhancement. Interviews for problem and jobs, analyzes codebase, produces TDD-focused implementation plan ready for GitHub issue creation."
---

# Define Requirements

## Purpose

This skill guides agentic coders through a structured Jobs-to-be-Done (JTBD) discovery process to ensure features are well-defined before implementation. It interviews the user to understand the problem and jobs, analyzes the codebase for implementation impact, and prepares everything needed for GitHub issue creation.

## Core Principles

### 1. Problem First, Always
Never jump to solutions. Understand what problem exists and why it matters before discussing how to solve it.

### 2. Jobs-to-be-Done Framework
Features exist to help users accomplish jobs. Map every feature to the specific jobs it satisfies.

### 3. Engineering Excellence
Recommendations follow best practices: TDD, security-first, existing patterns, and project conventions.

### 4. No Blind Spots
Systematically cover all aspects: problem, jobs, functionality, codebase impact, security, testing.

### 5. Efficient for the User
Ask smart questions, build on answers, don't repeat. Do the heavy lifting of analysis.

## When to Use

**Activate when user:**
- Wants to define or document a new feature
- Says "let's plan this feature" or "help me define requirements"
- Needs to think through what a feature should do
- Wants to create a well-structured GitHub issue for a feature

**Don't use for:**
- Quick bug fixes with obvious solutions
- Pure research or exploration tasks
- Implementation (use after requirements are defined)

## Workflow Overview

```
1. Problem Definition
   ↓
2. JTBD Interview (functional jobs + optional depth)
   ↓
3. CHECKPOINT: Confirm understanding
   ↓
4. Read CLAUDE.md for project conventions
   ↓
5. Codebase Analysis (deep, comprehensive)
   ↓
6. Implementation Recommendations (TDD-focused)
   ↓
7. CHECKPOINT: Summary + ready for GitHub issue?
   ↓
8. Handoff to github-issue-creator skill
```

## Phase 1: Problem Definition

Start every session by understanding the problem. Ask ONE question at a time.

### Opening Question
> "What problem are you trying to solve? Describe what's not working or what's missing today."

### Follow-up Probes (as needed)
- "Who experiences this problem?"
- "How often does this occur?"
- "What's the impact when this problem isn't solved?"
- "What triggered you to address this now?"

### Red Flags to Challenge
If user jumps to solutions:
> "I hear you want to build [feature]. Before we go there—what problem does this solve? What's painful today without it?"

If problem is vague:
> "Can you give me a specific example of when this problem occurred?"

## Phase 2: Jobs-to-be-Done Interview

Once the problem is clear, map the jobs users need to accomplish.

### Core Question
> "When users encounter this problem, what are they trying to accomplish? What job are they hiring this feature to do?"

### Functional Jobs (Always Ask)
- "What specific task does the user need to complete?"
- "What does success look like when that job is done?"
- "Are there multiple jobs, or variations of the same job?"

### Offer Depth Choice
After capturing functional jobs:
> "I have a good understanding of the functional jobs. Would you like to explore:
> 1. **Just functional** (faster) — proceed with what we have
> 2. **Include emotional/social** (fuller picture) — how users want to feel, how they want to be perceived"

### If User Chooses Deeper Exploration
- "How do users want to feel when doing this? (Confident? In control? Relieved?)"
- "Is there a social dimension? (Looking competent to others? Meeting expectations?)"

### Map Functionality to Jobs
For each job identified:
> "What specific functionality would satisfy this job? Let's map it out."

Build a table:
| Job | Functionality Required | Success Criteria |
|-----|----------------------|------------------|
| [Job 1] | [Feature/capability] | [How we know it's done] |

## Phase 3: Checkpoint — Confirm Understanding

Before investing in codebase analysis, confirm alignment.

### Present Summary
```markdown
## Summary: Jobs to be Done

**Problem**: [Concise problem statement]

**Target User**: [Who has this problem]

**Jobs Identified**:
1. **[Job 1]**: [Description]
   - Functionality: [What's needed]
   - Success: [Criteria]

2. **[Job 2]**: [Description]
   - Functionality: [What's needed]
   - Success: [Criteria]

[Continue for all jobs]
```

### Confirm
> "Does this accurately capture what we're trying to accomplish? Any jobs missing or misunderstood? Once confirmed, I'll analyze the codebase to understand implementation impact."

**Wait for explicit confirmation before proceeding.**

## Phase 4: Read Project Conventions

Before analyzing code, read the project's CLAUDE.md to understand:
- Architecture patterns (DAL, tenant isolation, etc.)
- Testing requirements
- Security considerations
- Code organization conventions

Use the Read tool on:
1. Root `CLAUDE.md`
2. `app/CLAUDE.md` (if exists)
3. Any referenced architecture docs

## Phase 5: Codebase Analysis

Perform a comprehensive, deep analysis. Use Explore agent or direct tools.

### What to Analyze

**1. Existing Patterns**
- How does the codebase handle similar features?
- What patterns should this feature follow?
- Are there utilities or helpers to leverage?

**2. Files to Modify**
- Which existing files need changes?
- Specific line numbers where changes occur
- Code snippets showing current state

**3. New Files Needed**
- Components, pages, actions, types
- Where they should live (follow conventions)

**4. Database Impact**
- Schema changes needed?
- New tables, columns, relationships?
- Migration requirements
- RLS policies needed

**5. API/Actions**
- Server actions to create/modify
- API endpoints affected
- Data flow changes

**6. Test Files**
- Existing tests that need updates
- New test files needed
- Test patterns to follow

### Security Review

**CRITICAL**: Flag any security concerns:
- Does this expose sensitive data?
- Are there tenant isolation implications?
- Input validation requirements?
- Authentication/authorization impacts?

If security risk detected:
> "**Security Warning**: This requirement could [specific risk]. I recommend [mitigation]. Do you want to proceed with these safeguards in place?"

### Anti-Pattern Detection

Check requirements against known anti-patterns:
- Bypassing DAL for direct DB access
- Client-side data fetching for sensitive data
- Missing tenant_id enforcement
- Skipping input validation

If anti-pattern detected:
> "**Warning**: The approach you're describing would [anti-pattern]. Best practice is to [correct approach]. Should we adjust the requirement?"

## Phase 6: Implementation Recommendations

Generate TDD-focused, best-practice recommendations.

### Structure
```markdown
## Implementation Plan

### TDD Approach
This feature should be implemented using strict Test-Driven Development:

**Phase 1: [Component/Feature]**
1. Write failing test for [specific behavior]
2. Implement minimal code to pass
3. Refactor while green

**Phase 2: [Next Component]**
[Continue pattern]

### Files to Create
| File | Purpose | Tests |
|------|---------|-------|
| `path/to/file.tsx` | [Purpose] | `__tests__/path/file.test.ts` |

### Files to Modify
| File | Changes | Line References |
|------|---------|-----------------|
| `path/to/existing.tsx` | [What changes] | Lines 45-67 |

### Database Changes
[Migration details if needed]

### Security Considerations
[Any security notes]

### Dependencies
[Prerequisites or related changes]
```

## Phase 7: Checkpoint — Ready for GitHub Issue

Present complete summary before handoff.

### Final Summary
```markdown
# Feature Requirements Summary

## Problem
[Problem statement]

## Jobs to be Done
[Job summary with functionality mapping]

## Implementation Overview
- **Files to create**: [count]
- **Files to modify**: [count]
- **Database changes**: [yes/no + summary]
- **Estimated test files**: [count]

## Key Recommendations
1. [Top recommendation]
2. [Second recommendation]
3. [Third recommendation]

## Security Notes
[Any security considerations]

## TDD Workflow
[High-level TDD phases]
```

### Prompt for Handoff
> "This captures the full requirements and implementation plan. Ready to create the GitHub issue? I'll invoke the `github-issue-creator` skill which will format this for the next developer and include the mandatory TDD workflow."

## Phase 8: Handoff

When user confirms, invoke the `github-issue-creator` skill with all gathered context.

The handoff should include:
- Problem statement
- Jobs-to-be-Done mapping
- All codebase analysis findings
- Specific file references with line numbers
- TDD implementation plan
- Security considerations
- Testing requirements

The github-issue-creator will structure this into a comprehensive issue.

## Interview Style Guidelines

### Do
- Ask one question at a time
- Build on previous answers
- Use the user's language back to them
- Offer choices when appropriate (e.g., depth level)
- Confirm understanding before major transitions

### Don't
- Dump multiple questions at once
- Assume you know what they mean
- Skip the problem to jump to solutions
- Proceed without explicit confirmation at checkpoints
- Ignore security or anti-pattern concerns

## Quality Checklist

Before each checkpoint, verify:

**After JTBD Interview:**
- [ ] Problem is clearly articulated
- [ ] Target user identified
- [ ] All functional jobs captured
- [ ] Functionality mapped to each job
- [ ] Success criteria defined

**After Codebase Analysis:**
- [ ] CLAUDE.md conventions reviewed
- [ ] Existing patterns identified
- [ ] All affected files listed with line references
- [ ] Database impact assessed
- [ ] Security review completed
- [ ] Anti-patterns checked
- [ ] TDD approach defined
- [ ] Test files identified

## Remember

- **You're the expert guide**: Users have basic PM knowledge—provide structure and guardrails
- **Efficiency matters**: Don't ask questions you can answer from context
- **Security is non-negotiable**: Always flag risks, never proceed blindly
- **TDD is mandatory**: Every recommendation should have tests-first approach
- **The goal is clarity**: A developer should be able to implement from the GitHub issue without asking questions
