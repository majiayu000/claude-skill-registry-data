---
name: workflow-challenger
description: Critical review and gap analysis skill that can be invoked at any workflow stage. Use to challenge decisions, identify missing specifications, verify coherence, and surface unaddressed questions in CDC, findings, plans, or any deliverable. Acts as a devil's advocate by deeply analyzing codebase, project documentation ([DOC]-* folders), and context.
---

# Workflow Challenger Skill

## Purpose

Act as a critical reviewer and devil's advocate at any stage of the feature workflow. This skill performs deep analysis to:

- Challenge assumptions and decisions
- Identify gaps and missing specifications
- Surface unanswered questions
- Verify coherence between documents and codebase
- Ensure nothing has been overlooked

**Key principle:** Better to surface issues early than discover them during implementation or testing.

## When to Use This Skill

Use this skill:

- After completing CDC.md to verify specification completeness
- After research to challenge technical decisions
- After planning to verify plan coherence with requirements
- Before implementation to catch missing details
- After test failures to understand root causes
- Anytime something feels incomplete or uncertain
- When user wants a second opinion on approach

## IMPORTANT: User Interaction

**Use the `AskUserQuestion` tool when clarification is needed on identified gaps.**

After analysis, use AskUserQuestion to:
- Confirm critical issues need resolution
- Get user input on ambiguous findings
- Prioritize which gaps to address first

```
AskUserQuestion:
  questions:
    - question: "I found that the CDC doesn't address error handling. How should we proceed?"
      header: "Gap Found"
      options:
        - label: "Add to CDC now"
          description: "Update the specification before continuing"
        - label: "Note for later"
          description: "Document as known gap, address during implementation"
        - label: "Not needed"
          description: "This case won't occur in practice"
      multiSelect: false
```

This ensures:
- User is aware of identified issues
- Clear decision-making on how to proceed
- Gaps are explicitly acknowledged or resolved

## Analysis Sources

The challenger analyzes multiple sources to build comprehensive context:

### 1. Project Documentation
```
Look for documentation folders at project root:
- [DOC]-{ProjectName}/
- docs/
- documentation/
- .doc/
- wiki/
```

Read all relevant documentation to understand:
- Project architecture
- Business rules
- Existing conventions
- Historical decisions

### 2. Codebase Analysis
```
Analyze existing code to understand:
- Current implementation patterns
- Data models and schemas
- API contracts
- Service dependencies
- Configuration patterns
```

### 3. Workflow Deliverables
```
Review current workflow documents:
- CDC.md (specification)
- findings.md (research)
- Plan.md (implementation plan)
- test-plan.md (test strategy)
```

### 4. Obsidian/Knowledge Base
```
If Obsidian MCP is available:
- Search for related notes
- Find linked concepts
- Discover historical context
```

## Challenge Workflow

### Phase 1: Context Gathering

1. **Identify current stage** - What deliverable is being challenged?
2. **Read the deliverable** - Understand what has been documented
3. **Explore project docs** - Find [DOC]-* folders and read relevant files
4. **Analyze codebase** - Understand existing patterns and constraints
5. **Build mental model** - Synthesize all information

```
Example context gathering:
1. Read CDC.md for "email notifications" feature
2. Found [DOC]-Backend/ with architecture.md
3. Found existing NotificationService in codebase
4. Found EmailTemplate component already exists
5. Mental model: Feature partially exists, CDC doesn't mention this
```

### Phase 2: Gap Analysis

Systematically check for gaps in each category:

**2.1 Missing Requirements**
- Are all user stories covered?
- Are edge cases addressed?
- Are error scenarios defined?
- Are non-functional requirements specified?

**2.2 Unclear Specifications**
- Are there ambiguous terms?
- Are there assumptions not validated?
- Are there "TBD" or placeholder sections?
- Are acceptance criteria measurable?

**2.3 Incoherence Detection**
- Does the document contradict itself?
- Does it contradict project documentation?
- Does it contradict existing codebase?
- Does it contradict other workflow documents?

**2.4 Missing Context**
- Is existing functionality acknowledged?
- Are dependencies identified?
- Are integration points clear?
- Is the scope realistic?

See `references/gap-analysis-guide.md` for detailed checklist.

### Phase 3: Challenge Formulation

For each identified issue, formulate a clear challenge:

**Structure:**
```
## Challenge: [Title]

**Type:** Gap / Ambiguity / Incoherence / Missing Context
**Severity:** Critical / Major / Minor
**Location:** [Document section or code location]

**Observation:**
[What was found or missing]

**Question:**
[Specific question to resolve the issue]

**Recommendation:**
[Suggested resolution or investigation]
```

**Example:**
```
## Challenge: Existing Email System Not Addressed

**Type:** Missing Context
**Severity:** Critical
**Location:** CDC.md Section 4 (Functional Requirements)

**Observation:**
The CDC specifies creating an EmailService, but the codebase already
has `src/services/NotificationService.ts` with email capabilities.
The CDC doesn't mention whether to extend, replace, or ignore it.

**Question:**
Should we extend the existing NotificationService or create a
separate EmailService? What happens to existing email functionality?

**Recommendation:**
Update CDC to explicitly address the existing NotificationService.
Consider extending it rather than creating parallel functionality.
```

### Phase 4: Coherence Verification

Cross-check between documents and reality:

**CDC vs Codebase:**
- Are referenced components real?
- Do proposed integrations make sense?
- Are technology choices consistent?

**CDC vs Project Docs:**
- Does it follow documented architecture?
- Does it respect documented constraints?
- Is terminology consistent?

**Findings vs CDC:**
- Does research address all CDC requirements?
- Are POC results aligned with specifications?
- Are chosen patterns appropriate?

**Plan vs Findings:**
- Does plan implement research recommendations?
- Are dependencies correctly sequenced?
- Is scope consistent?

### Phase 5: Report Generation

Compile findings into a structured report:

```markdown
# Challenge Report: [Deliverable Name]

**Date:** [Date]
**Stage:** [Specification / Research / Planning / etc.]
**Challenger:** Claude Code

## Summary

[Brief overview of findings]

- **Critical Issues:** X
- **Major Issues:** X
- **Minor Issues:** X

## Critical Issues

[Must be resolved before proceeding]

## Major Issues

[Should be resolved, but not blocking]

## Minor Issues

[Nice to address, low impact]

## Coherence Check

| Source A | Source B | Status | Notes |
|----------|----------|--------|-------|
| CDC | Codebase | ⚠️ | [Issue] |
| CDC | Project Docs | ✅ | Aligned |

## Questions for User

1. [Question 1]
2. [Question 2]

## Recommendations

1. [Recommendation 1]
2. [Recommendation 2]

## Conclusion

[Overall assessment and suggested next steps]
```

## Challenge by Stage

### Challenging CDC.md (Specification)

Focus on:
- Requirement completeness
- Scope clarity
- Acceptance criteria measurability
- Alignment with project architecture
- Existing functionality conflicts

Key questions:
- "Is this already partially implemented?"
- "Does this conflict with existing features?"
- "Are all personas addressed?"
- "What happens in failure scenarios?"

### Challenging findings.md (Research)

Focus on:
- Technical decision rationale
- Alternative evaluation completeness
- POC validity
- Integration feasibility
- Risk identification

Key questions:
- "Why this approach over alternatives?"
- "Was the POC representative?"
- "Are performance implications understood?"
- "What could go wrong?"

### Challenging Plan.md (Implementation)

Focus on:
- Step granularity appropriateness
- Dependency correctness
- Parallelization opportunities
- Missing steps
- Validation criteria clarity

Key questions:
- "Is this step too vague to implement?"
- "What if step X fails?"
- "Can these steps run in parallel?"
- "How do we know this step is complete?"

### Challenging test-plan.md (Testing)

Focus on:
- Coverage completeness
- Test priority appropriateness
- Edge case coverage
- Performance test inclusion
- Realistic test scenarios

Key questions:
- "Are negative scenarios tested?"
- "Is this test redundant with another?"
- "What's the most likely failure mode?"
- "Are integration points tested?"

## Context Discovery Patterns

### Finding Project Documentation

```bash
# Common documentation locations
Glob: [DOC]-*/**/*.md
Glob: docs/**/*.md
Glob: documentation/**/*.md
Glob: *.md (root level)
Glob: .github/**/*.md
```

### Finding Related Code

```bash
# Based on feature name/domain
Grep: "feature-keyword"
Glob: **/*Service*.ts
Glob: **/*Controller*.cs
Glob: **/models/**/*
```

### Using Obsidian MCP

```
If Obsidian available:
- Search notes for feature keywords
- Find linked architecture decisions
- Discover related past implementations
```

## Challenge Intensity Levels

### Quick Review (5-10 min)
- Scan document structure
- Check for obvious gaps
- Verify key sections present
- Spot-check coherence

### Standard Review (15-30 min)
- Full document read
- Cross-reference with codebase
- Check project documentation
- Formulate key questions

### Deep Review (30-60 min)
- Comprehensive analysis
- Full codebase exploration
- All documentation reviewed
- Detailed challenge report

## Tips for Effective Challenging

1. **Be constructive** - Goal is improvement, not criticism
2. **Be specific** - Vague concerns aren't actionable
3. **Prioritize** - Focus on critical issues first
4. **Suggest solutions** - Don't just identify problems
5. **Consider context** - Time/resource constraints matter
6. **Trust but verify** - Check claims against reality
7. **Document findings** - Create actionable report
8. **Ask, don't assume** - Formulate questions when uncertain

## Integration with Workflow

The challenger can be invoked:

- **Explicitly:** User requests challenge review
- **At transitions:** Between workflow phases
- **On demand:** Anytime during development

```
Phase 0: Specification → [Challenge CDC] → Phase 1: Research
Phase 1: Research → [Challenge Findings] → Phase 2: Planning
Phase 2: Planning → [Challenge Plan] → Phase 3: Implementation
...
```

## Bundled Resources

- `references/challenge-checklist.md` - Comprehensive checklist by stage
- `references/gap-analysis-guide.md` - Detailed gap analysis methodology
