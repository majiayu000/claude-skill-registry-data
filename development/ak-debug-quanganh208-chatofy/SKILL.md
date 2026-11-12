---
name: ak-debug
description: "Debug failing or misbehaving code by proving the root cause before any fix; diagnose why something fails, gives wrong output or is flaky in CI."
when_to_use: "Invoke before editing code for any error, stack trace or failing test; writing new tests is ak-test."
category: workflow
keywords: [debug, root-cause, bugs, test-failures]
languages: all
argument-hint: "[error or issue description] [--ultra]"
metadata:
  author: agentkit
  version: "4.2.0"
---

# Debugging & System Investigation

Comprehensive framework combining systematic debugging, root cause tracing, defense-in-depth validation, verification protocols, and system-level investigation (logs, CI/CD, databases, performance).

## Core Principle

**NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST**

Random fixes waste time and create new bugs. Find root cause, fix at source, validate the failure path and affected boundaries, verify before claiming success.

## When to Use

**Code-level:** Test failures, bugs, unexpected behavior, build failures, integration problems
**System-level:** Server errors, CI/CD pipeline failures, performance degradation, database issues, log analysis
**At completion:** Verify the repaired behavior with relevant evidence; a full diagnostic workflow is needed only for unresolved failures.

## Techniques

### 1. Systematic Debugging (`references/systematic-debugging.md`)

Four-phase framework: Root Cause Investigation → Pattern Analysis → Hypothesis Testing → Implementation. Complete each phase before proceeding. No fixes without Phase 1.

**Load when:** Any bug/issue requiring investigation and fix

### 2. Root Cause Tracing (`references/root-cause-tracing.md`)

Trace bugs backward through call stack to find original trigger. Fix at source, not symptom. Includes `scripts/find-polluter.sh` for bisecting test pollution.

**Load when:** Error deep in call stack, unclear where invalid data originated

### 3. Defense-in-Depth (`references/defense-in-depth.md`)

Inspect relevant boundaries: entry validation, business logic, environment guards or instrumentation. Add a check only where it discriminates between plausible causes or protects the repaired contract.

**Load when:** After finding root cause, need comprehensive validation

### 4. Verification (`references/verification.md`)

**Iron law:** NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE. Run command. Read output. Then claim result.

**Load when:** About to claim work complete, fixed, or passing

### 5. Investigation Methodology (`references/investigation-methodology.md`)

Five-step structured investigation for system-level issues: Initial Assessment → Data Collection → Analysis → Root Cause ID → Solution Development

**Load when:** Server incidents, system behavior analysis, multi-component failures

### 6. Log & CI/CD Analysis (`references/log-and-ci-analysis.md`)

Collect and analyze logs from servers, CI/CD pipelines (GitHub Actions), application layers. Tools: `gh` CLI, structured log queries, correlation across sources.

**Load when:** CI/CD pipeline failures, server errors, deployment issues

### 7. Performance Diagnostics (`references/performance-diagnostics.md`)

Identify bottlenecks, analyze query performance, develop optimization strategies. Covers database queries, API response times, resource utilization.

**Load when:** Performance degradation, slow queries, high latency, resource exhaustion

### 8. Reporting Standards (`references/reporting-standards.md`)

Structured diagnostic reports: Executive Summary → Technical Analysis → Recommendations → Evidence

**Load when:** Need to produce investigation report or diagnostic summary

### 9. Investigation Tracking (`references/task-management-debugging.md`)

For multi-step investigations, discover the live task-management surface and
use it to track dependencies, ownership, and parallel evidence collection when
available. Otherwise, update the active plan. Plan files are the durable source of truth,
so debugging never depends on a particular client's task API.

**Load when:** Multi-component investigation (3+ steps), parallel log collection, coordinating debugger subagents

### 10. Frontend Verification (`references/frontend-verification.md`)

Visual verification of frontend implementations via `ak-agent-browser`, `ak-chrome-profile`, Chrome MCP / `chrome-devtools-mcp`, or project-native browser tests. Use `ak-chrome-profile` and its exact tab binding when real Chrome profile state matters; raw Chrome MCP navigation is only for generic/profile-independent inspection. Detect if frontend-related -> check browser tool availability -> screenshot + console error check -> report. Skip if not frontend.

**Load when:** Implementation touches frontend files (tsx/jsx/vue/svelte/html/css), UI bugs, visual regressions

## Quick Reference

```
Code bug       → systematic-debugging.md (Phase 1-4)
  Deep in stack  → root-cause-tracing.md (trace backward)
  Found cause    → defense-in-depth.md (add layers)
  Claiming done  → verification.md (verify first)

System issue   → investigation-methodology.md (5 steps)
  CI/CD failure  → log-and-ci-analysis.md
  Slow system    → performance-diagnostics.md
  Need report    → reporting-standards.md

Frontend fix   → frontend-verification.md (agent-browser/chrome-profile/Chrome MCP)
```

## Tools Integration

- **Database:** `psql` for PostgreSQL queries and diagnostics
- **CI/CD:** `gh` CLI for GitHub Actions logs and pipeline debugging
- **Codebase:** `ak-docs-seeker` skill for package/plugin docs; `ak-repomix` skill for codebase summary
- **Scouting:** `/ak-scout` or `/ak-scout ext` for finding relevant files
- **Frontend:** `ak-agent-browser`, `ak-chrome-profile`, Chrome MCP / `chrome-devtools-mcp`, or project-native browser tests for visual verification. For real profile state, let `chrome-profile open --json` create the tab and bind to its returned selector before using MCP inspection tools.
- **Skills:** Activate `ak-problem-solving` skill when stuck on complex issues

## Red Flags

Stop and follow process if thinking:
- "Quick fix for now, investigate later"
- "Just try changing X and see if it works"
- "It's probably X, let me fix that"
- "Should work now" / "Seems fixed"
- "Tests pass, we're done"

**All mean:** Return to systematic process.

## Workflow Position

**Typically follows:** `/ak-scout` (after locating relevant code)
**Typically precedes:** `/ak-fix` (fix the diagnosed issue), `/ak-brainstorm` (explore solutions for complex problems)
**Related:** `/ak-scout` (discover before debugging), `/ak-fix` (fix after diagnosing)

## Ultra Verifier Mode (`--ultra`)

When `--ultra` is present, run the diagnosis as a best-of-5 verifier pass. The
controller gathers the evidence once — symptom, reproduction, logs, stack
traces, scouted code paths — into one immutable evidence packet plus a rubric,
dispatches exactly five independent read-only candidate diagnoses in one
parallel wave, then a single strongest-model verifier scores them.

- **Candidate task:** each candidate produces a complete diagnosis — root-cause
  hypothesis with file:line evidence, elimination of rival hypotheses, blast
  radius, and a verification plan — from the same packet. Candidates only
  analyze. Never fan mutating steps: no candidate runs fixes, edits files, or
  mutates system state.
- **Rubric:** evidence chain strength, rival-hypothesis elimination, specificity
  of the root cause (line/condition, not vibes), and testability of the
  verification plan.
- **Finalizer:** the verifier selects the single winning diagnosis unchanged (or
  rejects all); the controller then verifies the winning root cause with fresh
  evidence (iron law) before any fix. On reject-all, hard-stop and report why.

Full mechanics — evidence packet, anonymization, the five-usable-candidate gate,
reject-all, and the fail-closed runtime rule — are in
`../ak-brainstorm/references/ultra-verifier-mode.md`. It is a best-of-5 verifier
mode inspired by LLM-as-a-Verifier, not the full framework.

## Optional workflow shadow experiment

Only when explicitly requested, inspect `ak eval workflow --help` and prepare
its bounded, reviewed request with workflow `debug`. Default `off`
validates locally. `--mode shadow` additionally requires user-scope master and
provider configuration, explicit `workflow-controller: true` consumer consent,
and the provider credential; never enable or infer consent from an ambient key.
The optional command may send sanitized facts externally and incur charges.

Supply the existing domain decision and complete policy facts first. Keep all
`effective_*` decisions unchanged; record accepted `hypothetical_*` suggestions
only for comparison. Errors, low confidence and unavailable provider evidence
use the existing workflow. Never execute a recommendation or treat it as
permission. Existing caps, user stops, three-failure human checkpoints and
approval/R3 controls remain authoritative. Ordinary skill startup makes no call.

This is a shadow prototype for retry/replan/escalation decisions, not a new loop
or executor. At three failed repairs retain the required human architecture
checkpoint; never reset counters or rename a retry to evade a cap.
