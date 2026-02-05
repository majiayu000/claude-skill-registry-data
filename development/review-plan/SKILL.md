---
name: review-plan
description: Critically review implementation plans before execution. Use when validating plans, checking standards compliance, or before running implement-plan.
license: MIT
metadata:
  author: agent-kit
  version: "2.0.0"
---

# Review Plan

Critically review implementation plans using Codex CLI with high-reasoning capabilities.

## Purpose

Validate implementation plans to ensure they:
- Make logical sense and are achievable
- Follow project standards and conventions
- Have proper structure and completeness
- Won't cause issues during implementation

## When to Use

- Before executing a plan with `implement-plan`
- After creating a plan with `create-plan`
- When reviewing someone else's plan
- To validate plan updates or changes

## CRITICAL: Third-Party Review Required

**This skill MUST delegate to Codex CLI.** The review cannot be performed by the agent creating the plan - an independent third-party model must validate the work.

Why third-party review matters:
- Catches blind spots the author missed
- Validates assumptions against actual codebase state
- Provides independent verification of feasibility
- Reduces confirmation bias in self-review

**If Codex CLI is not available, inform the user and do not proceed with a self-review.**

## Codex CLI Invocation

Use the dedicated `codex review` command for non-interactive review:

```bash
# Pass instructions directly as argument
codex review "Review the plan at docs/plans/0042_feature.md for feasibility and completeness"

# Or read instructions from stdin
cat <<'PROMPT' | codex review -
Review the implementation plan at docs/plans/0042_feature.md

Check for: logical coherence, completeness, standards compliance, feasibility.
Provide PASS/FAIL/NEEDS_REVISION verdict.
PROMPT
```

**Key options:**
- Use `[PROMPT]` argument for simple instructions
- Use `-` to read longer instructions from stdin
- Use heredoc with `'PROMPT'` (quoted) to prevent variable expansion

**Note:** When reviewing plans (not code changes), use the `[PROMPT]` form since `--base`, `--commit`, and `--uncommitted` flags are for reviewing code diffs.

## Workflow

### Step 1: Locate the Plan

**If plan path provided:** Use the specified path directly.

**If no path provided:**
1. Check current conversation context for a plan being discussed
2. Look in `docs/plans/` for the most recently modified plan
3. Ask user which plan to review

### Step 2: Gather Context

Before invoking Codex, gather relevant context:

1. **Read the plan file** completely
2. **Identify referenced files** mentioned in the plan
3. **Load relevant standards:**
   - Project instructions: `CLAUDE.md` or `AGENTS.md`
   - Applicable standards from `content/standards/` based on tech stack
4. **Explore codebase** as needed to validate plan assumptions

### Step 3: Invoke Codex Review

**MANDATORY:** You must invoke Codex CLI. Do not perform the review yourself.

First, verify Codex is available:

```bash
which codex || echo "Codex CLI not installed"
```

If not available, stop and inform the user they need to install Codex CLI.

Build the review prompt and invoke Codex using stdin:

```bash
cat <<'PROMPT' | codex review -
Review the implementation plan at {plan-path}

Check against these criteria:
1. Logical Coherence - Do phases flow logically? Dependencies correct?
2. Completeness - All steps included? Testing strategy adequate?
3. Standards Compliance - Follows project conventions?
4. Feasibility - File paths correct? Referenced files exist?
5. Risk Assessment - What could go wrong?

Provide:
1. PASS/FAIL/NEEDS_REVISION verdict
2. Summary of findings
3. Specific issues with severity (HIGH/MEDIUM/LOW)
4. Recommended changes
PROMPT
```

**Important:** Let Codex read the plan file itself - it has filesystem access. This allows it to:
- Verify file paths mentioned in the plan actually exist
- Check referenced modules and their exports
- Validate assumptions about codebase state

**Do NOT paste plan content into the prompt** - this wastes tokens and prevents Codex from exploring the codebase.

### Step 4: Compile Review Report

After Codex returns, format the results:

```markdown
## Plan Review: {plan-name}

**Verdict:** PASS | FAIL | NEEDS_REVISION
**Reviewed by:** Codex (gpt-5.1-codex-max)
**Date:** {timestamp}

### Summary
{Brief overview of findings}

### Issues Found

| Severity | Issue | Location | Recommendation |
|----------|-------|----------|----------------|
| HIGH | {issue} | {section} | {fix} |
| MEDIUM | {issue} | {section} | {fix} |
| LOW | {issue} | {section} | {fix} |

### Standards Compliance
- [x] Follows project conventions
- [ ] Testing strategy adequate
- [x] Architecture aligned

### Questions for Author
1. {clarifying question}

### Recommendation
{Next steps - proceed, revise, or reject}
```

## Review Criteria Reference

See [references/review-criteria.md](references/review-criteria.md) for the complete checklist.

## Standards Sources

The review checks against:

1. **Project Instructions**
   - `CLAUDE.md` or `AGENTS.md` in project root
   - `.claude/` configuration

2. **Content Standards** (based on tech stack)
   - `content/standards/backend/java/` - Java backend standards
   - `content/standards/frontend/react/` - React frontend standards

3. **Plan Format Requirements**
   - Token limit: < 5000 tokens
   - Required sections: Testing Strategy, Dependency Graph
   - Proper numbering: `{NNNN}_{name}.md`

## Examples

### Example: Review a specific plan

```
User: Review the plan at docs/plans/0042_user-auth.md

Claude: I'll review this plan using Codex CLI for independent validation.

[Runs: which codex]
/opt/homebrew/bin/codex

[Runs: cat <<'PROMPT' | codex review -
Review the implementation plan at docs/plans/0042_user-auth.md
...
PROMPT]

Codex returned:

Verdict: NEEDS_REVISION

Summary: The plan is well-structured but missing integration tests
and has an incorrect dependency ordering in Phase 3.

Issues:
- HIGH — Missing integration tests (Testing Strategy section)
- MEDIUM — Task 3.2 depends on 3.4 but is ordered before it (Phase 3)

Recommended changes:
- Add API integration tests to Testing Strategy
- Reorder Phase 3 tasks so 3.4 comes before 3.2

---

Based on Codex's review, you should address the HIGH severity issue
before proceeding with implementation.
```

### Example: Codex not available

```
User: Review the plan

Claude: I need to invoke Codex CLI for third-party review.

[Runs: which codex]
codex not found

I cannot proceed with the review. This skill requires Codex CLI
for independent third-party validation. Please install it:

  npm install -g @openai/codex

Then run /review-plan again.
```

## Output

The skill produces:
- Formatted review report in conversation
- Verdict: PASS, FAIL, or NEEDS_REVISION
- Specific actionable feedback

## Related Skills

- `create-plan` - Creates plans that this skill reviews
- `implement-plan` - Executes plans after review passes
- `skill-validator` - Similar validation pattern for skills
