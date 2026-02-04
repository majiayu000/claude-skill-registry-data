---
name: create-issue
description: Investigate the codebase and draft a well-structured GitHub issue with evidence; use when asked to file or write an issue.
---

# Create Issue

## Overview

Use CLI subagents to investigate the codebase, then synthesize a complete GitHub issue.

## Inputs

- Issue description
- Scale (1-6, default 3)
- Issue type (bug, feature, enhancement) optional

## Workflow

1. Parse issue description, scale, and type.
2. Run scout subagents (see Scout commands) to find relevant files.
3. Run analysis subagents to assess scope and propose a fix or implementation.
4. Synthesize into a GitHub issue with title, summary, steps, expected, actual, impact, and affected files.

## Analysis Subagent Commands

### Codex (scope and fix)

```bash
codex exec -m gpt-5.2 -s read-only -c model_reasoning_effort="medium" --skip-git-repo-check \
  "Analyze the issue: {ISSUE_DESC}. Use the repo to identify scope, affected files, and suggested fix. Return a structured issue draft."
```

### Gemini (scope and risks)

```bash
CLOUDSDK_CORE_PROJECT="" GOOGLE_CLOUD_PROJECT="" GCLOUD_PROJECT="" GEMINI_API_KEY=${GEMINI_API_KEY} \
  gemini -m gemini-3-pro-preview -o text "Analyze: {ISSUE_DESC}. Identify scope, risks, and affected files. Return an issue draft."
```

### Claude (summary pass)

```bash
claude --model haiku -p "Review the issue analysis for: {ISSUE_DESC}. Provide a concise issue draft with steps and impact."
```

## Output

- Issue title and body ready to paste into GitHub
- Suggested labels and priority
