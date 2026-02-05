---
name: cc-development-workflow
description: This skill should be used when starting any feature or bug fix, exploring unfamiliar code, making commits or PRs, or when unsure which agent or approach to use. Covers agent routing, git discipline, testing workflow, and proactive quality practices.
---

# Development Workflow

**Purpose:** Establish efficient, high-quality development practices using AI code assistant agents and tools.

**Category:** Meta-Skill (Development Process)

---

## When to Use This Skill

This skill applies **throughout the entire development lifecycle**:

- Starting any new feature or bug fix
- Exploring unfamiliar code
- Making architectural decisions
- Committing changes
- Creating pull requests
- Reviewing code quality

**Triggers:**
- User requests a new feature
- User asks "where is..." or "how does..." questions
- You're about to implement without planning
- You're about to commit changes
- User asks for a PR

---

## Core Principle

**Use the right tool for the job.** Don't do manually what specialized agents can do better.

---

## Workflow 1: New Feature Development

### Triggers
- "Add...", "Build...", "Create...", "Implement [new thing]"
- User describes functionality that doesn't exist yet

### Decision Point: Should I use `/feature-dev`?

**Use `/feature-dev` if:**
- ✅ Feature requires multiple files
- ✅ Unclear how it should integrate with existing code
- ✅ Need to understand existing patterns first
- ✅ User hasn't specified exact implementation approach

**Skip `/feature-dev` if:**
- ❌ Trivial change (typo fix, single-line tweak)
- ❌ User provided extremely detailed implementation instructions
- ❌ Pure research/exploration task (use code-explorer instead)

### Workflow

**If using `/feature-dev`:**

```
1. Invoke Skill tool with skill="feature-dev:feature-dev"
2. Let the feature-dev workflow handle:
   - Codebase exploration
   - Clarifying questions
   - Architecture design
   - Implementation
   - Code review
3. Done - feature-dev handles end-to-end
```

**If NOT using `/feature-dev` (simple change):**

```
1. Read relevant files to understand current implementation
2. Ask clarifying questions if anything is ambiguous
3. Implement the change
4. Run build/lint/tests
5. Consider code-reviewer agent for non-trivial changes
```

**Anti-pattern:**
```
❌ User: "Add a new selector component"
   Assistant: *immediately starts writing code*

✅ User: "Add a new selector component"
   Assistant: "I'll use /feature-dev to explore the codebase,
              understand existing patterns, and design the implementation."
```

---

## Workflow 2: Code Exploration & Understanding

### Triggers
- "Where is...", "Explain how X works", "Map the project", "Find usage of..."
- Questions about code structure or flow

### Decision Point: Manual search vs code-explorer?

**Use code-explorer agent if:**
- ✅ Question requires understanding code flow across multiple files
- ✅ Need to trace execution paths
- ✅ "How does X work?" questions
- ✅ Finding all usages of a pattern

**Manual search (Glob/Grep) if:**
- ✅ Needle query - looking for specific file/class/function name
- ✅ You know exactly what to search for
- ✅ Single-file investigation

### Workflow

**For exploration (use code-explorer):**

```
1. Launch Task tool with subagent_type="Explore"
2. Provide clear question: "How does authentication work?"
3. Specify thoroughness: "medium" or "very thorough"
4. Read files identified by agent
5. Summarize findings
```

**For needle queries (manual search):**

```
1. Use Glob for file patterns: "**/*auth*.js"
2. Use Grep for code patterns: "getUser.*session"
3. Read matched files
4. Provide answer
```

---

## Workflow 3: Architecture & Planning

### Triggers
- "Plan...", "Design...", "Refactor strategy", "How should I structure..."
- Before implementing non-trivial features

### Decision Point: Should I enter plan mode?

**Use EnterPlanMode if ANY of:**
- ✅ New feature with multiple valid approaches
- ✅ Architectural decisions required
- ✅ Changes affect multiple files (3+)
- ✅ Unclear requirements need exploration first
- ✅ User preferences matter for implementation approach

**Skip plan mode if:**
- ❌ Single-line fix
- ❌ User provided very specific instructions
- ❌ Pure research task

### Workflow

```
1. Use EnterPlanMode tool
2. In plan mode:
   a. Explore codebase thoroughly
   b. Understand existing patterns
   c. Identify decision points
   d. Use AskUserQuestion for clarifications
   e. Design implementation approach
   f. Write plan to plan file
   g. Use ExitPlanMode
3. Wait for user approval
4. Implement according to approved plan
```

---

## Workflow 4: Code Quality & Review

### Triggers
- Completed non-trivial implementation
- Before creating PR
- User asks "review this"

### Decision Point: When to use code-reviewer?

**Use code-reviewer proactively when:**
- ✅ Just completed a feature (before user asks)
- ✅ Added >50 lines of new code
- ✅ Modified critical paths (update handlers, hooks, migrations)
- ✅ About to create PR
- ✅ Touched performance-sensitive code

**Workflow**

```
1. Complete implementation
2. Launch Task tool with subagent_type="pr-review-toolkit:code-reviewer"
3. Specify files to review (usually unstaged git diff)
4. Review agent findings
5. Fix high-priority issues
6. Commit changes
```

---

## Workflow 5: Version Control & Commits

### Triggers
- User asks to commit changes
- User asks to create PR
- Feature is complete and tested

### Git Discipline Rules

**NEVER:**
- ❌ Run raw `git commit` via Bash without crafted message
- ❌ Skip commit message template (must include attribution)
- ❌ Commit without running git status + git diff first
- ❌ Commit files with secrets (.env, credentials)
- ❌ Use `--no-verify` to skip hooks (unless user explicitly requests)
- ❌ Force push to main/master

**ALWAYS:**
- ✅ Use Skill tool for commits: `skill="commit-commands:commit"`
- ✅ Run `git status` and `git diff` in parallel first
- ✅ Draft commit message based on actual changes (not assumptions)
- ✅ Follow commit message style from git log
- ✅ Include attribution footer
- ✅ Verify no unintended files are staged

### Commit Workflow

```
1. Run in parallel:
   - git status (see untracked files)
   - git diff (see staged + unstaged changes)
   - git log -10 --oneline (see commit style)

2. Analyze changes and draft commit message:
   - Type: feat/fix/refactor/docs/chore/test
   - Summary: What changed and why (focus on "why", not "what")
   - Keep under 72 characters for summary line

3. Stage relevant files (git add)

4. Commit with proper message and attribution

5. Run git status after commit to verify success
```

---

## Workflow 6: External Knowledge & Research

### Triggers
- Uncertain about API usage
- Need current information (library versions, recent changes)
- User asks about external tools/libraries

### Decision Point: Search vs Assume

**ALWAYS search (don't assume) for:**
- ✅ Framework API usage (changes between versions)
- ✅ Recent library features
- ✅ Browser compatibility issues
- ✅ Security best practices
- ✅ Anything you're unsure about

**Safe to assume (from training):**
- ✅ JavaScript/ES6 syntax
- ✅ General web development patterns
- ✅ Git fundamentals
- ✅ Common npm commands

### Workflow

```
1. Identify knowledge gap
2. Use WebSearch or documentation tools
3. Cite sources in response
4. Apply findings to implementation
```

---

## Workflow 7: Testing & Verification

### Triggers
- After implementing any feature
- Before committing
- Before creating PR

### Testing Checklist

**Minimum (ALWAYS):**
```
1. Build (if applicable)
2. Lint (if applicable)
3. Describe what to test manually
```

### Workflow

```
1. Implement feature
2. Run build/lint commands
3. Describe manual testing steps
4. If update handlers involved:
   - Review safety checklist
   - Recommend appropriate tests
```

---

## Decision Trees

### "Should I use an agent?"

```
Feature request
├─ Trivial (1-5 lines)? → Implement directly
├─ Exploration needed? → code-explorer
├─ Architecture decision? → feature-dev (includes exploration + planning)
├─ Just planning? → EnterPlanMode
└─ Implementation done? → code-reviewer (proactive)

Code question
├─ Needle query (know what to find)? → Glob/Grep
├─ "How does X work?" → code-explorer
└─ "Where is X?" → code-explorer

Commit/PR
├─ Ready to commit? → Use commit skill (never raw git)
├─ Ready for PR? → Analyze full diff, draft description
└─ Unsure if ready? → code-reviewer first
```

### "Should I search or assume?"

```
Knowledge question
├─ Framework API? → SEARCH (changes between versions)
├─ Recent library features? → SEARCH
├─ Security concern? → SEARCH
├─ Browser compatibility? → SEARCH
├─ Basic JavaScript? → Assume (from training)
└─ Git basics? → Assume
```

---

## Anti-Patterns to Avoid

### 1. Skipping Exploration

**Problem:** Implementing without understanding existing patterns

```
❌ User: "Add a new field component"
   Assistant: *immediately writes new code from scratch*

✅ User: "Add a new field component"
   Assistant: *uses code-explorer to understand existing patterns first*
```

### 2. Manual Work Over Agents

**Problem:** Doing manually what agents do better

```
❌ User: "Where are errors handled?"
   Assistant: *manually greps for "error", reads 3 files*

✅ User: "Where are errors handled?"
   Assistant: *launches code-explorer to trace error handling comprehensively*
```

### 3. Assuming Knowledge

**Problem:** Using outdated or incorrect API information

```
❌ Assistant: "I'll use the deprecated API pattern"

✅ Assistant: "Let me verify the current API pattern..."
```

### 4. Sloppy Commits

**Problem:** Raw git commands, poor messages, no attribution

```
❌ Assistant: *runs bash* `git commit -m "fix"`

✅ Assistant: *uses commit skill*
   Assistant: *analyzes changes, drafts message, includes attribution*
```

### 5. No Testing Guidance

**Problem:** Declaring done without verification steps

```
❌ Assistant: "Feature complete!"

✅ Assistant: "Feature complete. To test:
   1. Run the build
   2. Open the application
   3. Verify the new feature works"
```

---

## Quick Reference Checklist

### Starting Work
- [ ] Is this a feature? → Consider `/feature-dev`
- [ ] Is this exploration? → Use `code-explorer`
- [ ] Is this complex? → Use `EnterPlanMode`
- [ ] Do I need external knowledge? → Search first

### During Implementation
- [ ] Reading existing code before modifying
- [ ] Following existing patterns
- [ ] Using project conventions

### Before Committing
- [ ] Run build (if applicable)
- [ ] Run lint (if applicable)
- [ ] Proactive code review (if non-trivial)
- [ ] Git status + git diff reviewed
- [ ] Commit message drafted with attribution
- [ ] Testing guidance provided

### Creating PR
- [ ] Analyzed FULL diff (not just latest commit)
- [ ] PR description drafted with test plan
- [ ] Build and lint passing

---

## Success Criteria

You're following this workflow correctly when:

- ✅ Features are explored before implementing
- ✅ Code is reviewed proactively (before user asks)
- ✅ Commits are clean with proper messages
- ✅ PRs include comprehensive descriptions
- ✅ Testing guidance is always provided
- ✅ External knowledge is verified, not assumed
- ✅ Specialized agents are used appropriately

---

**Last Updated:** 2026-01-04
**Status:** Active - use throughout development lifecycle
