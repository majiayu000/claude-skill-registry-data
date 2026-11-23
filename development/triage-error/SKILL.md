---
name: triage-error
description: >
  Take a live production error, stack trace, or on-call alert and
  systematically locate the fault site, assess blast radius, and recommend a
  mitigation path — the deliverable is fault site plus blast radius plus
  mitigation, not necessarily a code change. Use when the user says "prod is
  down", "we're getting paged", "production is throwing errors", "customers
  are seeing 500s", or "what's the blast radius", or pastes a stack trace
  during an active incident. Not for a routine dev-time bug, failing test, or
  code-review finding — use debug-issue instead, which produces a code fix
  rather than an incident response.
---

# triage-error

## You are an incident triage assistant. Your job is to take a raw error and turn it into a structured, actionable report as fast as possible. Prioritize finding the fault site and the causal commit over exhaustive analysis.

## Step 1 — Parse the error

- **Error type**: the exception class, HTTP status, or error code (e.g., `TypeError`, `500`, `ECONNREFUSED`)
- **Error message**: the human-readable description
- **Stack trace**: the call chain, if present
- **Context identifiers**: user ID, request ID, job ID, trace ID, session ID — anything that scopes the failure
- **Timestamp**: when the error occurred, if known
- **Environment**: production, staging, specific region or pod

If the stack trace is truncated or the error is too vague to investigate, say what additional information is needed before continuing.

---

## Step 2 — Locate the fault site

Using the stack trace or error message, find the originating code:

- identify the top application-owned frame in the stack trace (skip framework and library frames)
- read the relevant source file at the indicated line
- read enough surrounding context (the enclosing function and its callers) to understand what the code is doing

If the stack trace points to a compiled or minified file, look for a source map or the original source in the repository.

Search for the error message string in the codebase:

```
grep for the error message, exception class, or unique identifier
```

Build the call chain from the entry point to the fault site. Identify:

- entry point (route handler, job runner, CLI command, event handler)
- each intermediate layer
- the specific line that threw or returned the error

---

## Step 3 — Check recent changes at the fault site

Inspect the git history for the fault site files:

```bash
git log --oneline -10 -- <fault-site-file>
git blame <fault-site-file>
```

Look for commits in the last 5–10 commits or since the last known-good deployment that:

- modified the failing function or its direct callers
- changed configuration or environment variable handling related to the error
- updated a dependency that the fault site uses

If a likely causal commit is found, read its diff and confirm it plausibly explains the failure.

---

## Step 4 — Assess blast radius

Determine the scope of impact:

- **Who is affected**: all users, a specific user/tenant, requests matching certain conditions, a background job queue
- **Path criticality**: is this blocking a primary user flow (checkout, login, core API) or a secondary feature (notifications, analytics, exports)?
- **Frequency**: is this a hard failure on every request or an intermittent failure?
- **Data integrity risk**: could this have written partial or corrupt data? Are there transactions that may have rolled back or half-committed?
- **Cascading risk**: does this fault affect downstream services, queues, or caches?

Classify blast radius:

- **P1 (critical)**: blocking primary flow for all or many users, data integrity risk
- **P2 (high)**: blocking primary flow for a subset, or secondary flow broadly
- **P3 (medium)**: non-blocking degradation, isolated users, or background-only
- **P4 (low)**: cosmetic, logging, or very rare edge case

---

## Step 5 — Identify immediate mitigation options

Propose 1–3 mitigation options ranked by confidence and reversibility:

| Option               | Description                                             | Reversibility | Risk              |
| -------------------- | ------------------------------------------------------- | ------------- | ----------------- |
| Feature flag off     | Disable the affected feature via env var or flag        | Instant       | Low               |
| Revert causal commit | `git revert <sha>` and redeploy                         | Minutes       | Low if tests pass |
| Hotfix               | Minimal code change targeting the fault site            | Minutes–hours | Medium            |
| Scale / restart      | Restart affected pods/workers if the fault is transient | Instant       | Low               |
| Rollback deployment  | Roll back to the last known-good release                | Minutes       | Low-medium        |

For each option, explain what it does and does not fix.

---

## Step 6 — Report in incident-ready format

```text
TRIAGE REPORT
─────────────────────────────────────────────────────
Error
  Type:     <exception class or code>
  Message:  <error message>
  Time:     <timestamp if known>
  Env:      <environment>

Fault site
  File:     <path>:<line>
  Function: <function or method name>
  Call path: <entry → ... → fault>

Causal commit (most likely)
  SHA:      <hash>
  Author:   <name>
  Date:     <date>
  Summary:  <commit subject>
  Reason:   <why this commit likely caused the failure>

Blast radius
  Severity: <P1 / P2 / P3 / P4>
  Scope:    <who and what is affected>
  Data risk: <yes / no — description if yes>

Recommended mitigation
  1. [fastest] <option and command if applicable>
  2. [safest]  <option and command if applicable>

Open questions
  <anything still unknown that affects the triage>
─────────────────────────────────────────────────────
```

If you cannot confidently identify the causal commit or fault site, say exactly what evidence is missing and what investigation would confirm it.
