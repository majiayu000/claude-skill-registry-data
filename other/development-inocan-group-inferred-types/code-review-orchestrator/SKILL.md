---
name: Code Review Orchestrator
description: Delegate specialized reviews to subagents and synthesize their findings. Use when reviewing code.
---

# Code Review Orchestrator

## Overview

This skill orchestrates specialized review subagents to analyze code and documentation. Each subagent applies a specific review skill and returns focused findings. The orchestrator collects and presents results.

## When to Use

- Reviewing skills in .claude/skills/
- Evaluating CLAUDE.md files
- Assessing slash command prompts in .claude/commands/
- Any AI prompt or LLM instruction content review

## Process

### 1. Identify Files to Review

Determine scope:
- Single or multiple files
- File type (skill, CLAUDE.md, command)
- Relevant review dimensions

### 2. Select Review Skills

Map content type to review skills:

**For AI Prompt Content** (skills, CLAUDE.md, commands):
- `prompt-brevity/SKILL.md` - Token efficiency and clarity

**For Python Files** (skills, CLAUDE.md, commands):
- `python-code-review-types/SKILL.md` - Ensuring python types are used correctly.

**For all Pull Request Files** (changed files in PRs):
- `pr-file-review/SKILL.md` - Identify unnecessary test artifacts and temporary files
  - Give this agent a list of files in the PR or a command to find the list of files.

**IMPORTANT**: If no specific review skill exists for the file type being reviewed, **STOP** and inform the user:

```
No specific review skill exists for [file type/category]. Available review skills:
- prompt-brevity (for AI prompts, skills, CLAUDE.md, slash commands)

To review [file type], create a new review skill at:
.claude/skills/collaboration/reviews/[skill-name].md

Use /create-skill to generate a new review skill template.
```

**DO NOT** perform any direct code review. Only delegate to existing review subskills.

### 3. Launch Subagents in Parallel

For each selected review skill, launch a general-purpose subagent:

```
You are a specialized code reviewer. Apply the following skill to review the specified files.

**Skill to Apply**: [Read and follow .claude/skills/collaboration/reviews/[skill-name].md]

**Files to Review**: [list of file paths]

**Output Format**:

For each issue found, output:

---
**File**: [file path]
**Lines**: [line range, e.g., "45-52" inclusive or "78"]
**Issue**: [brief description]
**Suggestion**: [exact multiline replacement; omit if no specific change]
**Reason**: [why this improves the code]
---

Return ONLY the issues found. No commentary or summary.
```

### 4. Collect Subagent Results

Wait for all subagents to complete.

### 5. Present Findings

Output subagent results directly:

```markdown
## Review Results

### Prompt Brevity Review

[paste subagent output]

### [Future Review Type]

[paste subagent output]
```

**Do not add**: Commentary, summaries, severity rankings, or additional suggestions.

## Example

### Example 1: Single Skill File Review

**Input**: Review `.claude/skills/testing/test-driven-development.md`

**Subagent Task**:
```
You are a specialized code reviewer. Apply the following skill to review the specified files.

**Skill to Apply**: Read and follow .claude/skills/collaboration/reviews/prompt-brevity.md

**Files to Review**: .claude/skills/testing/test-driven-development.md

**Output Format**:

For each issue found, output:

---
**File**: [file path]
**Lines**: [line range inclusive]
**Issue**: [brief description]
**Suggestion**: [exact replacement; omit if no specific change]
**Reason**: [why this improves the code]
---

Return ONLY the issues found.
```

**Orchestrator Output**:
```markdown
## Review Results

### Prompt Brevity Review

---
**File**: .claude/skills/testing/test-driven-development.md
**Lines**: 12-15
**Issue**: Verbose explanation with redundant phrasing
**Suggestion**: Test-driven development: write tests before implementation code
**Reason**: 68% token reduction (23 → 7 tokens) while preserving core message
---

---
**File**: .claude/skills/testing/test-driven-development.md
**Lines**: 45
**Issue**: Fluff phrase "you should make sure to"
**Suggestion**: run the tests
**Reason**: Direct imperative is clearer and saves 5 tokens
---
```

### Example 2: Multiple File Review

**Input**: Review all skills in `.claude/skills/collaboration/`

**Action**: Launch one subagent with all file paths

**Orchestrator Output**:
```markdown
## Review Results

### Prompt Brevity Review

---
**File**: .claude/skills/collaboration/writing-commit-messages.md
**Lines**: 8-10
**Issue**: Ceremonial phrase "in order to"
**Suggestion**: to write good commit messages
**Reason**: Standard brevity pattern saves 2 tokens
---

---
**File**: .claude/skills/collaboration/writing-commit-messages.md
**Lines**: 67-72
**Issue**: Redundant examples demonstrating same concept
**Reason**: Reduces redundancy by 40 tokens without information loss (no specific replacement provided - requires context-aware consolidation)
---

---
**File**: .claude/skills/collaboration/code-review.md
**Lines**: 34
**Issue**: Hedge words "you might want to consider"
**Suggestion**: consider
**Reason**: Removes unnecessary hedging, saves 4 tokens
---
```

## Anti-patterns

- ❌ **Don't**: Perform direct code reviews when no subskill exists
  - ✅ **Do**: Inform user and suggest creating appropriate review skill

- ❌ **Don't**: Add your own commentary or summary
  - ✅ **Do**: Present subagent findings exactly as returned

- ❌ **Don't**: Filter or editorialize subagent results
  - ✅ **Do**: Trust subagent expertise and show all findings

- ❌ **Don't**: Combine findings from different review types
  - ✅ **Do**: Keep each review skill's findings separate

- ❌ **Don't**: Launch subagents sequentially
  - ✅ **Do**: Launch all subagents in parallel for efficiency

- ❌ **Don't**: Add severity ratings or prioritization
  - ✅ **Do**: Let findings speak for themselves

## Testing This Skill

### Test Scenario 1: Single File Review

1. Select one skill file to review
2. Launch prompt-brevity subagent
3. Present results
4. Success: Only subagent findings displayed

### Test Scenario 2: Parallel Multi-File Review

1. Select 3+ files for review
2. Launch subagent with all files in single task
3. Verify parallel execution (not sequential)
4. Success: All findings collected and presented cleanly

### Test Scenario 3: No Issues Found

1. Review a well-written, concise skill file
2. Launch subagent
3. Verify proper handling of "No issues found"
4. Success: Clean output without inventing issues

## Extensibility

To add new review dimensions:

1. Create new review skill in `.claude/skills/collaboration/reviews/[new-skill].md`
2. Update "Select Review Skills" section to include new skill
3. Launch additional subagent with new skill
4. Present findings in separate section

Example future skills:
- `reviews/security-practices` - Check for security anti-patterns
- `reviews/accessibility` - Verify inclusive language and examples
- `reviews/consistency` - Ensure style consistency across skills

## Related Skills

- `collaboration/reviews/prompt-brevity` - Token efficiency review skill
- `collaboration/pr-file-review` - Pull request file artifact review
- `meta/creating-skills` - Skill creation guidelines

---

**Remember**: Orchestrate, don't review. Delegate to experts and present findings.
