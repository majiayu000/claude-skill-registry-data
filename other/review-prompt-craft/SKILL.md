---
name: review-prompt-craft
description: |
  Write effective code review prompts, review context documents, and AI-assisted
  review infrastructure for any project. Covers: writing `.roborev.toml`-style
  negative-space context docs that teach reviewers what NOT to flag; designing
  multi-agent review matrices (when and why to use multiple models); structuring
  the review-fix-re-review loop with numbered findings and traceable fix commits;
  and conducting individual PR reviews with project-aware prompts. Use when
  setting up automated review for a repo, writing review instructions or
  guidelines, crafting prompts for AI code reviewers, deciding what reviewers
  should and should not flag, or debugging noisy/unhelpful AI review output.
  Also use when a review produces too many false positives, reviewers miss real
  bugs while flagging style nits, or review findings are vague and unactionable.
---

# Review Prompt Craft

Good review context tells a reviewer which project decisions are intentional. Without it, AI reviewers often flag generic concerns about authentication, rate limits, validation, and error handling that do not fit the deployment model. Capture these decisions and the real risks so reviews focus on actionable bugs.

Choose the workflow that matches the request:

- **Setup**: create or improve review context, a reviewer matrix, or CI integration.
- **Review**: assess a PR or diff using the project's context; if no context exists, gather it from project instructions and the README.

## Setup: Build review infrastructure

### 1. Learn the project and its false positives

Read the relevant code, existing review configuration, project instructions, PR history, and issue discussions. Establish:

1. Who runs the software: one person on localhost, an internal team, or public users?
2. Where trust boundaries lie: loopback, authenticated API, isolated container, or local files?
3. Which unusual design choices are intentional?
4. Which findings have reviewers repeatedly raised incorrectly?

Use concrete evidence from the codebase to answer these questions before writing configuration.

### 2. Write the negative-space context

Use a root `.roborev.toml` with a `review_guidelines` multi-line string when the review tool accepts that format. The context document is the main review artifact: explain the deployment model, what reviewers should not flag, and what would be a real defect.

```toml
review_guidelines = """
<PROJECT> is <description, including deployment model>.
<Key architectural constraint, such as local-only or single-user operation.>

Key assumptions reviewers must account for:

1. <CATEGORY>: <what the project does and why it is correct>.
   Do not flag <specific false-positive pattern>.
   DO flag <the actual failure condition>.

2. <CATEGORY>: <another intentional design decision>.
   Do not flag <recurring false positive>.

Do not flag issues that apply only to <inapplicable deployment model>.
Focus on <the project's actual correctness and risk concerns>.
"""
```

Make each item specific: name functions, middleware, and configuration keys. Pair each “do not flag” case with the condition that would make it a real bug. Number the items so a finding or fix can refer to a stable guideline number. Include recurring false positives only when they apply to this project, such as:

- Authentication or authorization in single-user or loopback-only paths.
- Rate limiting on services that are not public.
- Validation of trusted local input.
- TOCTOU concerns for user-owned local files.
- Display of user-owned data when that display is the feature.
- Intentional subprocess environment inheritance.
- Missing TLS when the user is responsible for transport security.

Explain schema constraints that rule out a suspected state and control flow that makes a path unreachable. Cite real code where possible; for example, identify the sanitizer that makes a particular rendering call safe. Keep the document focused, usually 50–150 lines. Describe categories rather than listing names that change often, and avoid vague security advice or positive-only checklists.

### 3. Choose the reviewer count

A single reviewer is usually enough for a small or familiar project, regression-focused reviews, or when speed matters most. Use two or three independent models when the change crosses subsystems, the security surface is complex, or you need complementary review strengths.

One possible division of focus is:

| Reviewer | Focus |
| --- | --- |
| Claude Code | Architecture, logic errors, subtle bugs |
| Codex | Code quality, project patterns, missing edge cases |
| Gemini | Security surface, API design, documentation |

Give each reviewer the same context. Merge, deduplicate, and prioritize their independent findings.

### 4. Define the review-fix-re-review loop

1. Give each finding a unique ID within the review, plus severity, file and line, category, explanation, and a concrete suggested fix.
2. Make fixes in traceable commits that reference finding IDs, for example:

   ```text
   fix: address review finding #13915 and #13917 on PR #314
   ```

3. Re-review the fix commits for correctness and regressions.
4. Stop when no blockers remain or the remaining findings are accepted trade-offs.

Use this finding shape:

```markdown
### Finding #<ID> [<SEVERITY>]

**File**: `<path>:<line>`
**Category**: <bug | security | logic | performance | style | docs>

<What is wrong and why it matters.>

**Suggested fix**:
<A concrete change or approach.>
```

Use severity consistently:

- **BLOCKER**: correctness, security, or data-loss issue that must be fixed before merge.
- **HIGH**: issue that should be fixed, such as a meaningful performance problem or missing edge case.
- **LOW**: issue worth considering, such as maintainability or documentation.
- **NIT**: optional consistency, naming, or formatting change.

### 5. Add CI when useful

For automated PR reviews, store the context in `.roborev.toml`, run the selected reviewer or reviewers from a `pull_request` CI job, and publish findings as comments or a review. Re-run review when fix commits arrive. Update the context in the same PR when the architecture changes.

### 6. Reuse project instructions

Make review context complement `CLAUDE.md`, `AGENTS.md`, or equivalent instructions. Builder instructions explain how to change the project; review context explains which existing decisions are intentional. Link to or summarize relevant conventions instead of copying them.

## Review: Assess a PR or diff

### 1. Gather the evidence

Collect the diff (`git diff <base>...HEAD` or `gh pr diff <number>`), the PR's intent, relevant project review context, CI status, and prior review comments. Look for `.roborev.toml`, `CLAUDE.md`, `AGENTS.md`, or equivalent files at the project root.

### 2. Read context before the diff

Apply the numbered assumptions in the review context before evaluating code. This keeps known intentional choices from becoming false positives. If there is no dedicated context document, use the project instructions and README to understand the deployment model and conventions.

### 3. Review in risk order

Prioritize:

1. Correctness: logic errors, off-by-one errors, nil dereferences, and material race conditions. Ignore local-file TOCTOU concerns when the project's ownership model makes them irrelevant.
2. Security issues that apply to the actual deployment model; do not raise generic authentication advice without evidence it applies.
3. Persistent-state integrity.
4. Unintended API or ABI breaks.
5. Missing tests for new behavior, rather than for every helper.
6. Performance issues with measurable, significant impact.
7. Maintainability problems that make code genuinely hard to follow.
8. Style issues that conflict with established project patterns.

### 4. Write actionable findings

Use the finding format above. Number findings sequentially within the review, give severity honestly, include a precise file and line, explain the impact, and suggest a fix. A developer should be able to act without asking what the finding means.

**Good finding**:

```markdown
### Finding #3 [HIGH]

**File**: `internal/server/sessions.go:142`
**Category**: bug

The error from `db.GetSession()` is checked, but the handler does not check
whether the session is nil. If the query returns no rows without an error,
accessing `session.ID` on line 145 will panic.

**Suggested fix**: Return `http.NotFound(w, r)` when `session == nil` after
the error check.
```

**Bad finding**:

```markdown
### Finding #3 [HIGH]

**File**: `internal/server/sessions.go`
**Category**: security

Consider adding authentication to this endpoint.
```

The bad example has no precise location or actionable evidence and may ignore a loopback-only auth model.

### 5. Summarize the review

End with a short summary using this shape:

```markdown
## Summary

Reviewed <N> files, <M> additions, <K> deletions.

- **Blockers**: <count> (must fix before merge)
- **High**: <count> (should fix)
- **Low/Nit**: <count> (consider fixing)

<One sentence on the overall assessment.>
```

## Failure patterns to catch

- **Context-free flag flooding**: generic warnings about auth, rate limits, or validation that ignore architecture. Read project context first; if it is missing, gather context from project instructions and the README.
- **Style-only review**: focus on bugs first. Keep style findings below 20% of findings; if only style issues remain, say so without inflating their severity.
- **Severity inflation**: most findings are LOW or NIT. Reconsider a review with more than two or three BLOCKER findings.
- **Vague findings**: state what is wrong, why it matters, where it occurs, and how to fix it.
- **Stale context**: update review guidance when architecture changes or a recurring false positive appears.
- **Overlong PR descriptions**: describe what the change does now; avoid duplicating test plans, checklists, or change logs. The code and tests carry those details.
- **Stale findings on reworked PRs**: credit the original community PR and explain what changed, but review the new code fresh rather than carrying findings forward.

## Evaluate an existing review setup

Check whether:

- [ ] Context describes the deployment model.
- [ ] Context addresses the leading false-positive categories with both “do not flag” and “DO flag” conditions.
- [ ] Context cites real functions, configuration, or other code evidence.
- [ ] Context stays under 150 lines.
- [ ] Findings have sequential IDs, severity, file and line, category, explanation, and suggested fix.
- [ ] Fix commits reference finding IDs.
- [ ] Fewer than 30% of findings are false positives.
- [ ] Fewer than 20% of findings are style-only.
- [ ] Context was revisited in the last 10 PRs that changed architecture.

## One-off review prompt

When no `.roborev.toml` context exists, use this structure:

```text
Review the following PR diff for <REPO_NAME>.

## Project Context
<1–3 sentences: what the project is, who runs it, and its deployment model.>

## Do Not Flag
<Numbered list of accepted design decisions and known false positives.>

## Focus Areas
<Specific subsystems, risk areas, or concerns from the PR author.>

## Diff
<The diff or a pointer to it.>

## Output Format
Number every finding sequentially. Use severity levels: BLOCKER, HIGH,
LOW, NIT. Include file:line, category, description, and suggested fix
for each finding. End with a summary count by severity.
```

This structure works with Claude, Codex, Gemini, and other AI reviewers.
