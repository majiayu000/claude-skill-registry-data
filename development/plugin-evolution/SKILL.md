---
name: plugin-evolution
description: "Use this skill when improving As You plugin, suggesting enhancements, analyzing plugin usage patterns, or planning meta-development tasks for the plugin itself."
version: 0.1.0
license: MIT
---

# Plugin Evolution Skill

A skill to support improvement and evolution of the As You plugin itself.

## Overview

This skill supports meta-development of the As You plugin. It analyzes usage patterns, proposes improvements, and designs new features.

## When to Use

Use this skill in the following cases:

- **Proposing Plugin Improvements**: Identify improvement points in existing features
- **Designing New Features**: Consider new features based on user feedback
- **Usage Pattern Analysis**: Analyze usage trends from pattern_tracker.json etc.
- **Performance Optimization**: Optimize scripts and hooks for efficiency
- **Documentation Improvement**: Propose updates to help and README

## Guidelines

### 1. Improvement Proposal Principles

**Propose Only, Do Not Auto-Apply**:
- Present improvement proposals clearly
- Let users decide whether to implement
- Don't impose, provide options

**Data-Driven**:
- Utilize pattern_tracker.json
- Base proposals on actual usage patterns
- Propose from facts, not assumptions

**Incremental Improvement**:
- Stack small improvements
- Avoid large-scale changes
- Maintain backward compatibility

### 2. Analysis Methods

**Usage Frequency Analysis**:
```bash
# Command usage frequency (workflow execution count)
# Memo recording frequency (memos per session)
# Pattern detection rate (knowledge base creation success rate)
```

**User Behavior Patterns**:
- Which features are frequently used
- Which patterns appear often
- Which features are unused

### 3. Proposal Categories

#### A. Feature Improvements
- Enhance usability of existing commands
- Optimize script performance
- Strengthen error handling

#### B. New Feature Addition
- Consider implementing WIP (Work in Progress) feature
- Evaluate RAG integration possibilities
- Determine MCP integration priorities

#### C. Documentation Improvements
- Enrich help content
- Add usage examples
- Create troubleshooting guide

#### D. Quality Enhancement
- Test coverage
- Robustness of error handling
- Security strengthening

### 4. Proposal Format

```markdown
## Improvement Proposal: [Title]

### Current Issue
[What is the problem]

### Proposal Content
[How to improve]

### Expected Benefits
[Benefits gained from improvement]

### Implementation Difficulty
- Difficulty: Low/Medium/High
- Estimated Effort: [time]
- Dependencies: [if any]

### Priority
- Priority: High/Medium/Low
- Reason: [Why this priority]
```

## Examples

### Example 1: Proposal from Usage Frequency Analysis

```
Analysis of pattern_tracker.json revealed the following trends:

- `memo` command is frequently used (average 8 times per session)
- However, `memo-history` is rarely used (0.5 times/week)

**Proposal**: Improve memo-history command
- Current: Displays all history (verbose)
- Improvement: Add keyword search functionality
- Implementation: Add Bash/grep search to `memo-history.md`
```

### Example 2: New Feature Proposal from Patterns

```
Pattern analysis confirmed demand for "work interruption/resumption".

**Proposal**: Implement WIP (Work in Progress) feature
- Reference: doc/10_session_resume_continuity.md Option B
- Priority: Medium (consider for v0.2.0)
- Reason: Demand indicated by frequent "Implementing Phase X" memos
```

## Implementation Notes

### How to Trigger This Skill

This skill is automatically triggered when users ask:

- "I want to improve the As You plugin"
- "Analyze usage patterns"
- "Do you have ideas for new features?"
- "How can we improve this plugin's usability?"

### Analysis Data Sources

- `.claude/as_you/pattern_tracker.json` - Pattern frequency
- `commands/` - Number and types of commands
- `skills/` - Number of skills
- `agents/` - Number of agents
- `doc/` - Design documentation

### Constraints

- **Proposals Only**: Do not automatically modify files
- **Data-Focused**: Base on actual data, not speculation
- **User-Led**: Leave final decisions to users

## Related Files

- [Session Resume Continuity](./reference/session-resume.md) - Design proposals for work resumption
- [Roadmap](./reference/roadmap.md) - Future feature plans

---

Use this skill to continuously improve the As You plugin.
