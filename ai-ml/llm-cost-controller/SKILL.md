---
name: llm-cost-controller
description: "LLM cost controller: audits all LLM API calls in a codebase, detects cost anti-patterns (expensive models, unlimited tokens, no caching, batchable calls), and estimates monthly spend with optimization savings. Read-only. Trigger: /llm-cost"
trigger: /llm-cost
---

## What this is for

LLM costs accumulate silently. Common anti-patterns drive costs without value:
expensive models for trivial tasks, unlimited output tokens, high temperature,
uncached repeated calls, and individual calls that should be batched.

**Audience:** Senior
- Platform/ML engineers use it for cost governance across AI features.
- Engineering leads use it to project and reduce LLM spend.

### Trigger: `/llm-cost`


## PROTECTION RULE - never ~/.claude/

Read-only skill. Guard required if write mode added later.

## What You Must Do When Invoked
During analysis, assign a confidence level to each finding: proven (confirmed by evidence), likely (strong signal, needs review), or suspected (weak signal).

### Step 1 - `-help`/`-h` check
Print usage block and stop.

### Step 2 - Run collector
```powershell
& .\scripts\llm-cost-scan.ps1 -ProjectDir "<path>" [-MonthlyCallEstimate 50000]
```

### Step 3 - Validate each finding
Read context, confirm the optimization is real, calculate savings.

### Step 4 - Prioritize by savings potential
Sort by estimated monthly savings.

### Step 5 - Produce report
Write `llm-cost-report.md`:

```
# LLM Cost Report - <project>

## Summary
- <N> API calls, est. $X/mo, potential savings $Y/mo
- <H> high, <M> medium, <L> low findings

## High Impact
### 1. Expensive models
### 2. Unlimited max_tokens

## Medium Impact
### 3. High temperature
### 4. No retry backoff
### 5. No caching
### 6. Batchable calls in loops

## Low Impact
### 7. Large context windows
### 8. Streaming not used

## Call Catalog
Per call: file, line, model, params, est. cost/call

## Savings Projection
What-if scenarios per optimization.
```

## Usage

```powershell
& .\scripts\llm-cost-scan.ps1 -ProjectDir "C:\Projects\my-ai-app"
& .\scripts\llm-cost-scan.ps1 -ProjectDir "C:\Projects\my-ai-app" -MonthlyCallEstimate 50000
```
