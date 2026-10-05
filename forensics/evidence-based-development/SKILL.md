---
name: evidence-based-development
description: "Enforce evidence-based claims through file:line citations, P1/P2/P3 prioritization proportional to evidence, and the ASSERTION/EVIDENCE/VERIFIED pattern for behavioral claims before any recommendation. Use when gathering evidence, presenting findings, or making development decisions. This skill MUST be consulted because confidence is not evidence, and ungrounded claims cause incorrect development decisions."
allowed-tools: Bash, Read, Grep, Glob
---

# Evidence-Based Development

## Iron Law

**EVIDENCE BEFORE CLAIMS, ALWAYS. If you haven't read the code, you don't know what it does.**

No recommendation without a citation. No behavioral claim without verification. Confidence is not evidence.

## Show Before Decide

Never propose a change without first showing the current state: "Here's what I found at `file.rb:42` → here's what I recommend → here's why."

## Citation Requirements

Every claim about code carries a `file_path:line_number` reference. When reviewing diffs, cite the file and the specific hunk. When reporting issues, show the exact code snippet.

## Finding Prioritization

All findings, review comments, and issues use P1/P2/P3. This operationalizes the organizational hard boundary **"No Ungrounded Claims"**: every finding carries evidence (file:line, test output, runtime observation) proportional to its priority.

| Priority | Meaning | Action |
|----------|---------|--------|
| **P1** | Must fix — blocks merge, security issue, data loss risk, broken functionality | Fix before proceeding |
| **P2** | Should fix — logic error, missing edge case, test gap, convention violation | Fix in this PR |
| **P3** | Consider — style preference, optimization opportunity | Fix in-PR by default. Cosmetic P3 in untouched files: fix-if-bounded or document inline (default) / follow-up issue (`minimalScope` mode only). Finding triage is NEVER a valid escalation trigger — see `skills/llm-operator-principles/SKILL.md`. |

## ASSERTION/EVIDENCE/VERIFIED Pattern

For any non-trivial claim about code behavior (behavioral claims, security assessments, performance analysis — not obvious facts):

1. **ASSERTION**: what you believe to be true
2. **EVIDENCE**: the code/output/test that supports it
3. **VERIFIED**: confirmed by running a test, reading the actual code, or checking behavior

## Finding-First Display

Show findings BEFORE recommendations or actions: the finding table (sorted P1 → P2 → P3), then affected files with citations, then proposed actions, then decisions (if needed). Never bury findings after narrative.

## Deduplication

When synthesizing findings from multiple sources (agents, reviews, tools): deduplicate by `file:line`; keep the highest priority; merge descriptions that add context; note each finding's source.

## Verification Methods

Run tests after code changes. Read code or `git diff` before behavioral claims and after edits. Run independent checks as parallel Bash calls. Use Agent(Explore) for unfamiliar code in a separate context.

## Stop Conditions

Stop and reassess when: you've made 2+ claims without file:line citations; you're about to recommend a change to a file you haven't read; evidence contradicts your assumption (update the assumption, don't explain away the evidence); you're writing "should" or "probably" about code behavior — go verify.

## Graceful Degradation

When evidence is unavailable: state what you couldn't verify and why; proceed with reduced confidence, flagging assumptions; never fabricate evidence or cite files you haven't read. "I already checked earlier" is stale — show fresh evidence.
