---
name: code-debug
description: Debug issues by researching errors and proposing minimal fixes. Use when user asks to troubleshoot or debug a runtime/production error or symptom. For test/lint/format check-command failures, use `code-check` instead.
---

Troubleshoot problems with focused research and risk review.

## Process

### Step 1 - Identify Error

- Identify the error message, log, or symptom from the user's request or context.

### Step 2 - Research Error

Apply a researcher lens to investigate the error or failure in {context}:

- Prefer official documentation over blog posts.
- Cite sources with URLs.
- Separate confirmed facts from plausible interpretations.
- Note version requirements.
- Lead with the single most actionable recommendation.

Find likely root causes, official docs or known issues, minimal fixes, and verification steps with sources.

### Step 3 - Synthesize Findings

- Synthesize findings into actionable steps.

### Step 4 - Apply Fix and Verify

- If requested, apply the minimal fix and verify using the most specific command.

### Step 5 - Report

Report to the user:

1. **Likely cause**
2. **Evidence** (links or doc references)
3. **Fix**
4. **Verify**

## Stop Condition

- If a proposed fix fails twice, stop, re-evaluate the diagnosis, and ask for guidance.
