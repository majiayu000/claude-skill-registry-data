---
name: investigate
description: Deep investigation of bugs, performance issues, or unexpected behavior
argument-hint: "<issue-to-investigate>"
---

# Deep Investigation

Thorough investigation of issues with root cause analysis and recommendations.

**OUTPUT: Detailed report with findings, root cause, and recommendations.**

## Arguments

- `$ARGUMENTS` - Issue description, error message, or area to investigate

## Phase 1: Define the Problem (Parallel: Hypotheses + Data Gathering)

Launch **two parallel agents** immediately. Both can work simultaneously since forming hypotheses from the issue description is independent from gathering raw data.

**Agent 1 - Hypotheses Formation:**

> Analyze the issue description: `$ARGUMENTS`
>
> Form 3-5 ranked hypotheses about what might be causing this issue. For each hypothesis, state:
> - The suspected cause
> - Why this is plausible given the symptoms
> - What evidence would confirm or refute it
>
> Return a numbered list of hypotheses with supporting reasoning.

**Agent 2 - Data Gathering:**

> Gather all available data about: `$ARGUMENTS`
>
> Collect in parallel where possible:
> - Error messages and stack traces (search logs, output files, CI artifacts)
> - Recent changes to affected areas (`git log --oneline -30 -- path/to/affected/`)
> - Related issues or discussions (search issue trackers if available)
> - Current state of affected code paths (read the relevant source files)
> - Environment and configuration state
>
> Return all raw findings organized by category.

Wait for both agents to complete. Combine their outputs to form the investigation plan for Phase 2.

## Phase 2: Evidence Collection (Parallel: 4 Independent Agents)

Launch **four parallel agents**, one per evidence dimension. These are completely independent investigations that share no dependencies.

**Agent 1 - Code Analysis:**

> Investigate the code paths related to: `$ARGUMENTS`
>
> Using the hypotheses: [insert hypotheses from Phase 1]
>
> Analyze:
> - All code paths involved in the issue (read source files, trace call chains)
> - Recent changes to affected areas (`git log -p --since="2 weeks ago" -- path/to/affected/`)
> - Dependencies and their versions
> - Integration points between components
> - Any relevant design patterns or architectural decisions that could contribute
>
> For each hypothesis, note which code evidence supports or contradicts it.
> Return detailed code-level findings with exact file paths and line numbers.

**Agent 2 - Log and Error Analysis:**

> Analyze logs and error output related to: `$ARGUMENTS`
>
> Search for:
> - Error patterns matching the reported symptoms (use Grep across log files)
> - Timestamp correlations (what happened before, during, and after the error)
> - Frequency and distribution of errors
> - Stack traces and their common frames
> - Warning messages that might indicate preconditions
>
> Return a timeline of events and all error patterns found, with file locations.

**Agent 3 - Test Behavior:**

> Investigate test behavior related to: `$ARGUMENTS`
>
> Perform:
> - Run existing tests for affected areas and capture results
> - Write a minimal exploratory test that attempts to reproduce the issue
> - Check test coverage of the affected code paths
> - Look for flaky tests or tests with known issues in the affected area
> - Try to create the smallest possible reproduction case
>
> Return test results, reproduction status, and any newly written test code.

**Agent 4 - External Factors:**

> Investigate external factors related to: `$ARGUMENTS`
>
> Check:
> - Database state and schema (if applicable)
> - Third-party service status and API changes
> - Configuration differences between working and broken environments
> - Environment variables and their values
> - Infrastructure or platform changes (OS updates, dependency updates, CI changes)
> - Network conditions or connectivity issues
>
> Return all external factor findings, noting which factors changed recently.

Wait for all four agents to complete. Merge all evidence into a unified evidence set.

## Phase 3: Root Cause Analysis (Parallel: Hypothesis Testing)

Launch **one parallel agent per hypothesis** from Phase 1. Each agent independently evaluates a single hypothesis against the full evidence set from Phase 2.

**For each hypothesis, launch an agent:**

> Evaluate hypothesis: "[Hypothesis N description]"
>
> Against collected evidence:
> [Insert merged evidence from Phase 2]
>
> Perform:
> 1. List all evidence that supports this hypothesis
> 2. List all evidence that contradicts this hypothesis
> 3. Attempt to definitively prove or disprove it (run targeted commands, read specific code, write a focused test)
> 4. If the code path can be traced, follow it from entry point through data transformations, decision points, to exit/error point
> 5. Rate confidence: HIGH / MEDIUM / LOW with justification
>
> Distinguish between:
> - **Proximate cause**: The immediate trigger
> - **Root cause**: The underlying issue
> - **Contributing factors**: Things that made it worse
>
> Return: verdict (confirmed/refuted/inconclusive), confidence level, all supporting evidence, and the causal chain if confirmed.

Wait for all hypothesis agents to complete. Select the hypothesis with the strongest evidence as the root cause. If multiple hypotheses are confirmed, determine whether they are independent issues or parts of the same causal chain.

## Phase 4+5: Documentation and Recommendations (Parallel: 2 Agents)

Launch **two parallel agents**. The report structure and the recommendations are independent deliverables that draw from the same evidence.

**Agent 1 - Investigation Report:**

> Write a complete investigation report for: `$ARGUMENTS`
>
> Using root cause: [insert root cause from Phase 3]
> Using evidence: [insert evidence from Phase 2]
> Using hypothesis results: [insert results from Phase 3]
>
> Format:
>
> ```markdown
> # Investigation Report: [Issue Title]
>
> **Date:** [date]
> **Investigator:** Claude Code
> **Status:** Complete
>
> ## Summary
> [One paragraph summary of the issue and root cause]
>
> ## Problem Statement
> [What was reported/observed]
>
> ## Investigation Steps
>
> ### Step 1: [What was checked]
> **Finding:** [What was discovered]
>
> ### Step 2: [What was checked]
> **Finding:** [What was discovered]
>
> ...
>
> ## Root Cause
> [Detailed explanation of the root cause, distinguishing proximate cause, root cause, and contributing factors]
>
> ## Evidence
> - [Evidence 1 with file:line references]
> - [Evidence 2 with file:line references]
>
> ## Contributing Factors
> - [Factor 1]
> - [Factor 2]
>
> ## Appendix
>
> ### Code References
> - `file1.kt:123` - [description]
> - `file2.kt:456` - [description]
>
> ### Timeline
> - [timestamp] - [event]
> - [timestamp] - [event]
> ```

**Agent 2 - Recommendations and Prevention:**

> Based on root cause: [insert root cause from Phase 3]
> And evidence: [insert evidence from Phase 2]
>
> Produce two deliverables:
>
> **1. Prioritized Actions:**
> - **Critical** - Must do immediately to resolve the issue
> - **Important** - Should do soon to prevent recurrence
> - **Nice to have** - Consider for future resilience
>
> For each action, include specific code changes, file paths, and implementation details.
>
> **2. Prevention Plan:**
> - Testing improvements (specific tests to add, coverage gaps to fill)
> - Monitoring and alerting (what metrics to watch, what thresholds to set)
> - Code review focus areas (patterns to watch for in future reviews)
> - Documentation updates (what to document, where)
>
> Return both deliverables with concrete, actionable items.

Wait for both agents to complete. Merge the recommendations into the report under a `## Recommendations` section.

## Investigation Techniques Reference

These techniques may be used by any agent during any phase:

### Binary Search (Git Bisect)
```bash
git bisect start
git bisect bad HEAD
git bisect good <known-good-commit>
# Test each commit until culprit found
```

### Minimal Reproduction
Create the smallest possible test case that reproduces the issue. Prefer an automated test over manual steps.

### Compare Working vs Broken
Diff configurations, code versions, and environments between working and broken states.

## Test Failure Policy

**IMPORTANT:** If any tests fail during investigation, they must be fixed. There is no such thing as a "pre-existing" test failure - all test failures must be resolved before the task is considered complete. The task always completes with completely passing tests.

## Completion Criteria

- [ ] Problem clearly defined
- [ ] Evidence collected from all four dimensions (code, logs, tests, external)
- [ ] All hypotheses evaluated with evidence-backed verdicts
- [ ] Root cause identified with confidence level
- [ ] Report written with full code references and timeline
- [ ] Recommendations provided with specific, actionable items
- [ ] ALL tests pass (no exceptions for "pre-existing" failures)
