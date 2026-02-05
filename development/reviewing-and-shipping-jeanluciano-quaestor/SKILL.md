---
name: Reviewing and Shipping
description: Validate quality with multi-agent review, auto-fix issues, generate organized commits, and create PRs with rich context. Use after completing features to ensure quality gates pass and ship confidently.
allowed-tools: [Read, Edit, MultiEdit, Bash, Grep, Glob, TodoWrite, Task]
---

# Reviewing and Shipping

I help you ship code confidently: validate quality, fix issues, generate commits, review with agents, and create pull requests.

## When to Use Me

**Review & validate:**
- "Review my changes"
- "Check if code is ready to ship"
- "Validate quality gates"

**Create pull request:**
- "Create a PR"
- "Ship this feature"
- "Make a pull request for spec-feature-001"

**Generate commits:**
- "Generate commits from my changes"
- "Create organized commits"

## Quick Start

**Most common:** Just completed work and want to ship it
```
"Review and ship this feature"
```

I'll automatically:
1. Validate quality (tests, linting, security)
2. Fix any issues
3. Generate organized commits
4. Review with agents
5. Create PR with rich description

**Just need PR:** Already validated and committed
```
"Create a PR for spec-feature-001"
```

I'll skip validation and just create the PR.

## How I Work - Conditional Workflow

I detect what you need and adapt:

### Mode 1: Full Review & Ship (Default)
**When:** "Review my changes", "Ship this"
**Steps:** Validate → Fix → Commit → Review → PR

**Load:** `@WORKFLOW.md` for complete 5-phase process

---

### Mode 2: Quick Review
**When:** "Quick review", small changes
**Steps:** Basic validation → Fast commits → Simple PR

**Load:** `@MODES.md` for quick mode details

---

### Mode 3: Create PR Only
**When:** "Create a PR", "Make pull request"
**Steps:** Generate PR description from spec/commits → Submit

**Load:** `@PR.md` for PR creation details

---

### Mode 4: Generate Commits Only
**When:** "Generate commits", "Organize my commits"
**Steps:** Analyze changes → Create atomic commits

**Load:** `@COMMITS.md` for commit strategies

---

### Mode 5: Validate Only
**When:** "Validate my code", "Check quality"
**Steps:** Run quality gates → Report results

**Load:** `@WORKFLOW.md` Phase 1

---

### Mode 6: Deep Analysis
**When:** "Analyze code quality", "Review for issues"
**Steps:** Multi-agent review → Detailed report

**Load:** `@AGENTS.md` for review strategies

---

## Progressive Loading Pattern

**Don't load all files!** Only load what's needed for your workflow:

```yaml
User Intent Detection:
  "review my changes" → Load @WORKFLOW.md (full 5-phase)
  "create a PR" → Load @PR.md (PR creation only)
  "generate commits" → Load @COMMITS.md (commit organization)
  "quick review" → Load @MODES.md (mode selection)
  "validate code" → Load @WORKFLOW.md Phase 1 (validation)
```

## The 5-Phase Workflow

**When running full review:**

### Phase 1: Validate 🔍
- Run tests, linting, type checking
- Security scan
- Documentation check

**See @WORKFLOW.md Phase 1 for validation details**

### Phase 2: Auto-Fix ⚡
- Fix simple issues (formatting)
- Delegate complex issues to agents
- Re-validate

**See @AGENTS.md for fix strategies**

### Phase 3: Generate Commits 📝
- Group related changes
- Create atomic commits
- Conventional commit format

**See @COMMITS.md for commit generation**

### Phase 4: Multi-Agent Review 🤖
- Security review
- Code quality review
- Test coverage review

**See @AGENTS.md for review coordination**

### Phase 5: Create PR 🚀
- Generate description from spec/commits
- Include quality report
- Submit to GitHub

**See @PR.md for PR creation**

## Key Features

### Smart Quality Validation
✅ Language-specific validation (Python, Rust, JS, Go)
✅ Multi-domain checks (code, security, tests, docs)
✅ Automatic fixing of common issues
✅ Clear pass/fail reporting

### Intelligent Commit Generation
✅ Groups related changes by module
✅ Atomic commits (one logical change)
✅ Conventional commit format
✅ Links to specifications

### Multi-Agent Review
✅ Parallel agent execution
✅ Domain-specific expertise
✅ Actionable suggestions
✅ Required fix identification

### Rich PR Creation
✅ Spec-driven descriptions
✅ Quality metrics included
✅ Test coverage reported
✅ Links to specifications
✅ Review insights attached

## Common Workflows

### After Implementing a Feature
```
User: "Review and ship spec-feature-001"

Me:
1. Validate: Run tests, linting, security scan
2. Fix: Auto-fix formatting, delegate complex issues
3. Commit: Generate organized commits
4. Review: Multi-agent code review
5. PR: Create comprehensive pull request
```

### Just Need a PR
```
User: "Create PR for spec-feature-001"

Me:
1. Find completed spec
2. Generate PR description
3. Create GitHub PR
4. Report URL
```

### Want to Validate First
```
User: "Validate my code"

Me:
1. Run all quality gates
2. Report results (✅ or ❌)
3. If issues: List them with fix suggestions
4. Ask: "Fix issues and ship?" or "Just report?"
```

## Supporting Files (Load on Demand)

- **@WORKFLOW.md** (1329 lines) - Complete 5-phase process
- **@AGENTS.md** (995 lines) - Multi-agent coordination
- **@MODES.md** (869 lines) - Different workflow modes
- **@COMMITS.md** (1049 lines) - Commit generation strategies
- **@PR.md** (1094 lines) - PR creation with rich context

**Total if all loaded:** 5609 lines
**Typical usage:** 200-1500 lines (only what's needed)

## Success Criteria

**Full workflow complete when:**
- ✅ All quality gates passed
- ✅ Issues fixed or documented
- ✅ Commits properly organized
- ✅ Multi-agent review complete
- ✅ PR created with rich context
- ✅ Spec updated (if applicable)

**PR-only complete when:**
- ✅ Spec found (if spec-driven)
- ✅ PR description generated
- ✅ GitHub PR created
- ✅ URL returned to user

## Next Steps After Using

- PR created → Wait for team review
- Quality issues found → Use implementing-features to fix
- Want to iterate → Make changes, run me again

---

*I handle the entire "code is done, make it shippable" workflow. From validation to PR creation, I ensure quality and create comprehensive documentation for reviewers.*
