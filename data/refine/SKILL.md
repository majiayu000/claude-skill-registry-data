---
name: refine
description: Refine or update an existing implementation plan; use when asked to improve or adjust a plan file.
---

# Refine Plan

## Overview

Use CLI subagents to review an existing plan and propose refinements, then update the plan file.

## Inputs

- Plan file path
- Refinement criteria (optional)

## Workflow

1. Read the existing plan and extract its structure.
2. Ensure `plans/context/` exists for any agent notes.
3. Run refinement subagents (Codex, Gemini, Claude) using the commands below.
4. Synthesize changes and update the plan file.

## Refinement Subagent Commands

### Codex (detail pass)

```bash
codex exec -m gpt-5.2 -c model_reasoning_effort="high" -c thinking="enabled" --skip-git-repo-check \
  "Refine this plan based on {CRITERIA}. Return specific changes for requirements, architecture, steps, tests, and risks. PLAN: {PLAN_TEXT}"
```

### Gemini (architecture and gaps)

```bash
CLOUDSDK_CORE_PROJECT="" GOOGLE_CLOUD_PROJECT="" GCLOUD_PROJECT="" GEMINI_API_KEY=${GEMINI_API_KEY} \
  gemini -m gemini-3-pro-preview -o text "Refine this plan based on {CRITERIA}. Identify gaps and improvements. PLAN: {PLAN_TEXT}"
```

### Claude (review pass)

```bash
claude --model opus -p "Review and refine this plan based on {CRITERIA}. Return concise edits and risk notes. PLAN: {PLAN_TEXT}"
```

## Output

- Updated plan file and a summary of changes
