---
name: oss:issue-discovery
description: Phase 1 of OSS contribution - Find and evaluate suitable issues matching your skills, time, and learning goals. Filters by labels, assesses project health, and provides structured recommendations. Use when starting OSS contribution, looking for beginner-friendly issues, or evaluating multiple issue options.
---

# Phase 1: Issue Discovery & Triage

Find and evaluate suitable issues to work on in open source projects.

## Purpose

Help contributors identify issues that match their:
- Skill level and experience
- Available time commitment
- Learning goals
- Interest areas

## When to Use

**Triggers:**
- "좋은 이슈 찾아줘"
- "beginner-friendly 이슈 추천"
- "이 프로젝트에서 뭘 할 수 있을까?"
- "이 이슈가 나한테 맞을까?"

**Use when:**
- Starting contribution to a new project
- Looking for next issue after completing one
- Evaluating multiple issue options
- Unsure which issue to tackle

## Discovery Process

### Step 1: Understand Contributor Profile

Ask or infer:
- **Experience level:** First-time, intermediate, experienced
- **Tech stack familiarity:** Languages, frameworks, tools
- **Time availability:** Quick fix, moderate, substantial project
- **Goals:** Learn, build portfolio, fix personal pain point, give back
- **Preferences:** Bug fix, feature, docs, tests, refactoring

### Step 2: Project Assessment

Before searching issues, evaluate project health and read contribution guidelines:

**MANDATORY: Read CONTRIBUTING.md**
- **MUST read and understand** the repository's CONTRIBUTING.md file
- Note required workflow, branch naming, commit conventions
- Identify testing requirements and code style guidelines
- Check for CLA (Contributor License Agreement) requirements
- Understand PR submission process and review expectations
- **All subsequent phases MUST follow these guidelines**

**Health indicators:**
- Recent commit activity (last 7-30 days)
- Responsive maintainers (issue/PR response time)
- Clear contribution guidelines (CONTRIBUTING.md present)
- Active community (discussions, recent merges)
- Good documentation

**Red flags:**
- No activity for 6+ months
- Many ignored PRs or issues
- Hostile or dismissive maintainer responses
- No CONTRIBUTING.md or unclear guidelines
- Constant breaking changes

Output format:
```markdown
### Project Health Check
- **Activity:** [recent commits/releases]
- **Responsiveness:** [avg maintainer response time]
- **Community:** [# contributors, discussion activity]
- **CONTRIBUTING.md:** ✅ Read and understood / ⚠️ Unclear / ❌ Missing
  - Key requirements: [workflow, testing, style, etc.]
- **Assessment:** ✅ Good to contribute / ⚠️ Proceed with caution / ❌ Not recommended
```

### Step 3: Issue Filtering

Use multiple filters to find candidates:

**Critical filters (MUST apply):**
- **No linked PR:** Exclude issues that already have associated pull requests
  - Check issue references, linked PRs in GitHub UI
  - Skip issues marked "has-pr" or with PR links in comments
- **Beginner-friendly priority:** Focus on accessible issues
  - Labels: `good first issue`, `beginner-friendly`, `help wanted`
  - Labels: `up-for-grabs`, `easy`, `low-hanging-fruit`
- **High priority labels:** Prioritize important work
  - Look for: `priority: high`, `high-priority`, `important`, `urgent`
  - Repository-specific priority indicators
  - Issues referenced in roadmap or milestones

**By issue type:**
- `documentation`, `bug`, `enhancement`
- Prefer well-scoped, clearly defined issues

**By complexity:**
- **Simple (1-4 hours):** Typos, docs, simple bugs, config changes
- **Moderate (1-2 days):** Feature additions, refactoring, moderate bugs
- **Complex (1+ weeks):** Architecture changes, major features, complex bugs

**By recency:**
- Prefer issues updated within last 30 days
- Check for assigned developers
- Look for maintainer engagement

### Step 4: Individual Issue Evaluation

For each candidate issue, assess:

#### Quality Indicators ✅

**Clear description:**
- Problem statement is specific
- Expected behavior defined
- Actual behavior described
- Steps to reproduce (for bugs)

**Good context:**
- Relevant error messages/logs
- Environment details (version, OS, browser)
- Screenshots or examples
- Links to related issues/discussions

**Maintainer engagement:**
- Maintainer has commented
- Issue is confirmed/triaged
- No one currently assigned
- Not marked as "wontfix" or "blocked"

#### Warning Signs ⚠️

- **Has linked PR** - Issue already being worked on
- Vague or unclear requirements
- No maintainer response
- Already assigned to someone
- Marked as "blocked", "on-hold", or "needs-discussion"
- Very old issue (6+ months) with no activity
- Duplicate of another issue
- Controversial or disputed approach

#### Evaluation Template

For each candidate issue:

```markdown
## Issue: [Title] (#[number])
**URL:** [link]
**Labels:** [labels]
**Created:** [date] | **Updated:** [date]

### Quick Assessment
- **Clarity:** ⭐⭐⭐⭐☆ (4/5) - [brief note]
- **Scope:** 🔵 Small | 🟡 Medium | 🔴 Large
- **Difficulty:** 🟢 Easy | 🟡 Moderate | 🔴 Hard
- **Time estimate:** [hours/days]

### Requirements Understanding
- **What needs to be done:** [1-2 sentences]
- **Success criteria:** [how to know it's complete]
- **Unknowns:** [what's unclear or needs investigation]

### Skill Match
- **Required skills:** [list]
- **Your match:** ✅ Good fit / ⚠️ Stretch goal / ❌ Too advanced
- **Learning opportunity:** [what you'll learn]

### Decision
✅ **Good choice because:** [reasons]
⚠️ **Consider if:** [conditions]
❌ **Skip because:** [reasons]

**Recommendation:** [Proceed / Ask maintainer first / Choose another]
```

### Step 5: Multi-Issue Comparison

When evaluating multiple issues, create comparison table:

```markdown
## Issue Comparison

| Issue | Difficulty | Time | Learning Value | Impact | Priority |
|-------|-----------|------|----------------|--------|----------|
| #123  | 🟢 Easy    | 2h   | ⭐⭐☆         | Medium | 🥇 High  |
| #456  | 🟡 Medium  | 1d   | ⭐⭐⭐        | High   | 🥈 Med   |
| #789  | 🔴 Hard    | 1w   | ⭐⭐⭐⭐     | High   | 🥉 Low   |

### Recommendation
Start with **#123** because:
1. Quick win to familiarize with codebase
2. Clear requirements, low risk
3. Sets foundation for #456 later

**Progression path:** #123 → #456 → #789
```

## Strategic Considerations

### First Contribution Strategy

For first-time contributors to a project:

1. **Start small:** Choose simple issue to learn workflow
2. **Build trust:** Demonstrate quality before tackling complex work
3. **Learn codebase:** Use first PR to understand conventions
4. **Engage community:** Interact respectfully with maintainers

**Recommended progression:**
```
First PR: Documentation fix or typo
  ↓
Second PR: Simple bug fix or small feature
  ↓
Third PR: Moderate complexity work
  ↓
Ongoing: Complex features, architecture improvements
```

### Learning-Oriented Selection

When goal is learning:

- **Choose stretch issues:** Slightly above comfort level
- **Look for patterns:** Issues that teach transferable skills
- **Seek feedback:** Projects with detailed code reviews
- **Diverse types:** Mix bugs, features, refactoring, docs

### Impact-Oriented Selection

When goal is maximizing value:

- **User-facing issues:** Direct user benefit
- **Bug fixes:** Immediate problem resolution
- **Documentation:** Helps many future contributors
- **Performance:** Benefits all users

### Portfolio Building

For building public portfolio:

- **Substantial features:** Show design skills
- **Complex bugs:** Show debugging ability
- **Cross-cutting work:** Show system understanding
- **Leadership:** Help triage, review others' PRs

## Engagement Before Starting

Before beginning work, **always:**

1. **Comment on issue:**
   ```
   "Hi! I'd like to work on this issue.

   My understanding is: [brief summary]

   I'm planning to: [approach]

   Does this sound good? Any guidance appreciated!"
   ```

2. **Wait for confirmation:**
   - Maintainer gives go-ahead
   - No one else is assigned
   - Approach is approved

3. **Ask questions:**
   - Clarify unclear requirements
   - Confirm edge cases
   - Request guidance on approach

**Why this matters:**
- Avoids duplicate work
- Ensures approach is correct
- Builds relationship with maintainers
- Shows respect for project process

## Common Pitfalls

**Avoid:**

❌ **Starting without commenting** - Someone else might be working on it
❌ **Choosing glamorous but too-hard issues** - Will frustrate you and waste time
❌ **Ignoring "needs discussion" label** - Issue might not be ready
❌ **Taking assigned issues** - Respect others' claimed work
❌ **Multiple issues at once** - Finish one before starting next
❌ **Stale issues** - May be outdated or deprioritized

## Output Format

Provide structured recommendation:

```markdown
# 🎯 Issue Discovery Results

## Selected Issue
**Title:** [Issue title]
**URL:** [link]
**Status:** [open/triaged/confirmed]

### Why This Issue?
1. [Reason 1: skill match, learning, impact, etc.]
2. [Reason 2]
3. [Reason 3]

### What You'll Do
[1-2 sentence summary of the work]

### Prerequisites
- [ ] Comment on issue to claim
- [ ] Wait for maintainer approval
- [ ] Fork repository
- [ ] Set up development environment

### Next Steps
Ready to move to **Phase 2: Issue Analysis**?

---

## Alternative Options

If this doesn't work out, consider:
1. **[Issue #]** - [brief description, why alternative]
2. **[Issue #]** - [brief description, why alternative]
```

## Integration with Main Framework

When invoked from main framework:

1. **Receive context:** User profile, project URL, preferences
2. **Execute discovery:** Filter and evaluate issues
3. **Return recommendation:** Selected issue + reasoning
4. **Update tracker:** Mark Phase 1 complete
5. **Transition:** Prepare context for Phase 2

Can be re-invoked at any time if selected issue becomes unavailable or user wants different option.
