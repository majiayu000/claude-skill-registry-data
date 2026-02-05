---
name: workflows-review
description: This skill should be used when performing exhaustive code reviews using multi-agent analysis, ultra-thinking, and Git worktrees for deep local inspection. It applies to PR reviews, branch comparisons, and comprehensive code quality assessments.
---

# Review Workflow

Perform exhaustive code reviews using multi-agent analysis, ultra-thinking, and Git worktrees for deep local inspection.

## Role

Senior Code Review Architect with expertise in security, performance, architecture, and quality assurance.

## Prerequisites

- Git repository with GitHub CLI (`gh`) installed and authenticated
- Clean main/master branch
- Proper permissions to create worktrees and access the repository
- For document reviews: Path to a markdown file or document

## Workflow

### 1. Determine Review Target & Setup

First, determine the review target type and set up the code for analysis.

**Immediate Actions:**

- [ ] Determine review type: PR number (numeric), GitHub URL, file path (.md), or current branch
- [ ] Check current git branch
- [ ] If ALREADY on the PR branch → proceed with analysis on current branch
- [ ] If DIFFERENT branch → use @skill/git-worktree for isolated analysis
- [ ] Fetch PR metadata using `gh pr view --json` for title, body, files, linked issues
- [ ] Set up language-specific analysis tools
- [ ] Prepare security scanning environment
- [ ] Ensure the correct branch is checked out (use `gh pr checkout` if needed)

Ensure the code is ready for analysis before proceeding.

### 2. Parallel Agent Reviews

Spawn sub-agents in parallel for comprehensive review. Each sub-agent should focus on a specific aspect of the code.

**Core Review Agents (run all in parallel):**

1. Spawn a sub-agent to review Rails conventions using @guidance/review/kieran-rails-reviewer
2. Spawn a sub-agent to review DHH-style Rails patterns using @guidance/review/dhh-rails-reviewer
3. If Turbo is used: Spawn a sub-agent for Turbo expertise using @guidance/review/rails-turbo-expert
4. Spawn a sub-agent to analyze git history using @guidance/review/git-history-analyzer
5. Spawn a sub-agent to investigate dependencies using @guidance/review/dependency-detective
6. Spawn a sub-agent for pattern recognition using @guidance/review/pattern-recognition-specialist
7. Spawn a sub-agent for architecture review using @guidance/review/architecture-strategist
8. Spawn a sub-agent for code philosophy using @guidance/review/code-philosopher
9. Spawn a sub-agent for security analysis using @guidance/review/security-sentinel
10. Spawn a sub-agent for performance review using @guidance/review/performance-oracle
11. Spawn a sub-agent for DevOps concerns using @guidance/review/devops-harmony-analyst
12. Spawn a sub-agent for data integrity using @guidance/review/data-integrity-guardian
13. Spawn a sub-agent to verify agent-accessibility using @guidance/review/agent-native-reviewer

### 3. Conditional Agents

Run these agents ONLY when the PR matches specific criteria:

**If PR contains database migrations (`db/migrate/*.rb`) or data backfills:**

14. Spawn a sub-agent using @guidance/review/data-migration-expert to validate ID mappings, check for swapped values, verify rollback safety
15. Spawn a sub-agent using @guidance/review/deployment-verification-agent to create Go/No-Go deployment checklist with SQL verification queries

**Trigger conditions:**
- PR includes files matching `db/migrate/*.rb`
- PR modifies columns that store IDs, enums, or mappings
- PR includes data backfill scripts or rake tasks
- PR changes how data is read/written
- PR title/body mentions: migration, backfill, data transformation, ID mapping

### 4. Ultra-Thinking Deep Dive

For each phase, spend maximum cognitive effort. Think step by step. Consider all angles. Question assumptions.

#### Stakeholder Perspective Analysis

1. **Developer Perspective**
   - How easy is this to understand and modify?
   - Are the APIs intuitive?
   - Is debugging straightforward?
   - Can this be tested easily?

2. **Operations Perspective**
   - How to deploy this safely?
   - What metrics and logs are available?
   - How to troubleshoot issues?
   - What are the resource requirements?

3. **End User Perspective**
   - Is the feature intuitive?
   - Are error messages helpful?
   - Is performance acceptable?
   - Does it solve the problem?

4. **Security Team Perspective**
   - What's the attack surface?
   - Are there compliance requirements?
   - How is data protected?
   - What are the audit capabilities?

5. **Business Perspective**
   - What's the ROI?
   - Are there legal/compliance risks?
   - How does this affect time-to-market?
   - What's the total cost of ownership?

#### Scenario Exploration

- [ ] **Happy Path**: Normal operation with valid inputs
- [ ] **Invalid Inputs**: Null, empty, malformed data
- [ ] **Boundary Conditions**: Min/max values, empty collections
- [ ] **Concurrent Access**: Race conditions, deadlocks
- [ ] **Scale Testing**: 10x, 100x, 1000x normal load
- [ ] **Network Issues**: Timeouts, partial failures
- [ ] **Resource Exhaustion**: Memory, disk, connections
- [ ] **Security Attacks**: Injection, overflow, DoS
- [ ] **Data Corruption**: Partial writes, inconsistency
- [ ] **Cascading Failures**: Downstream service issues

### 5. Multi-Angle Review Perspectives

**Technical Excellence:**
- Code craftsmanship evaluation
- Engineering best practices
- Technical documentation quality
- Tooling and automation assessment

**Business Value:**
- Feature completeness validation
- Performance impact on users
- Cost-benefit analysis
- Time-to-market considerations

**Risk Management:**
- Security risk assessment
- Operational risk evaluation
- Compliance risk verification
- Technical debt accumulation

**Team Dynamics:**
- Code review etiquette
- Knowledge sharing effectiveness
- Collaboration patterns
- Mentoring opportunities

### 6. Simplification Review

Spawn a sub-agent using @guidance/review/code-simplicity-reviewer to identify simplification opportunities.

### 7. Findings Synthesis and Todo Creation

ALL findings MUST be stored in the `.opencode/todos/` directory. Create todo files immediately after synthesis.

#### Step 1: Synthesize All Findings

- [ ] Collect findings from all parallel agents
- [ ] Categorize by type: security, performance, architecture, quality, etc.
- [ ] Assign severity levels: 🔴 CRITICAL (P1), 🟡 IMPORTANT (P2), 🔵 NICE-TO-HAVE (P3)
- [ ] Remove duplicate or overlapping findings
- [ ] Estimate effort for each finding (Small/Medium/Large)

#### Step 2: Create Todo Files

Use @skill/file-todos for structured todo management. Create todo files for ALL findings immediately.

**For large PRs with 15+ findings:** Spawn sub-agents in parallel to create finding files simultaneously.

**File naming convention:**
```
{issue_id}-{status}-{priority}-{description}.md

Examples:
- 001-pending-p1-security-vulnerability.md
- 002-pending-p2-performance-optimization.md
- 003-pending-p3-code-cleanup.md
```

**Status values:**
- `pending` - New findings, needs triage/decision
- `ready` - Approved, ready to work
- `complete` - Work finished

**Priority values:**
- `p1` - Critical (blocks merge, security/data issues)
- `p2` - Important (should fix, architectural/performance)
- `p3` - Nice-to-have (enhancements, cleanup)

**Tagging:** Always add `code-review` tag, plus: `security`, `performance`, `architecture`, `rails`, `quality`, etc.

#### Step 3: Summary Report

After creating all todo files, present:

```markdown
## ✅ Code Review Complete

**Review Target:** PR #XXXX - [PR Title]
**Branch:** [branch-name]

### Findings Summary:
- **Total Findings:** [X]
- **🔴 CRITICAL (P1):** [count] - BLOCKS MERGE
- **🟡 IMPORTANT (P2):** [count] - Should Fix
- **🔵 NICE-TO-HAVE (P3):** [count] - Enhancements

### Created Todo Files:

**P1 - Critical (BLOCKS MERGE):**
- `001-pending-p1-{finding}.md` - {description}

**P2 - Important:**
- `003-pending-p2-{finding}.md` - {description}

**P3 - Nice-to-Have:**
- `005-pending-p3-{finding}.md` - {description}

### Next Steps:
1. Address P1 Findings: CRITICAL - must be fixed before merge
2. Triage all todos in `.opencode/todos/`
3. Work on approved todos using @workflows/work
4. Track progress by updating todo status
```

### 8. End-to-End Testing (Optional)

After presenting the Summary Report, offer appropriate testing based on project type:

**Detect project type from PR files:**
- iOS/macOS: `*.xcodeproj`, `*.xcworkspace`, `Package.swift`
- Web: `Gemfile`, `package.json`, `app/views/*`, `*.html.*`
- Hybrid: Both iOS and web files

**For Web Projects:** Offer to spawn a sub-agent for Playwright browser tests on affected pages.

**For iOS Projects:** Offer to spawn a sub-agent for Xcode simulator tests.

**For Hybrid Projects:** Offer web only, iOS only, or both.

## Important: P1 Findings Block Merge

Any **🔴 P1 (CRITICAL)** findings must be addressed before merging the PR. Present these prominently and ensure resolution before accepting the PR.

## Related Workflows

- @workflows/plan - Create implementation plans
- @workflows/work - Execute work items systematically
- @workflows/compound - Document solved problems
- @skill/file-todos - Structured todo management
- @skill/git-worktree - Isolated worktree management
