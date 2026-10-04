---
name: super-lab-lite
description: Lightweight multi-agent research orchestration using one coordinator, three domain leads, and three lightweight research agents. Use for medium-size research, market scans, competitor comparisons, prior-art style exploration, report planning, and any task that benefits from parallel domain decomposition without running a full high-cost research lab.
---

# Super Lab Lite

Super Lab Lite is a small public orchestration pattern for splitting a research request into three domains, gathering evidence in parallel, and synthesizing the result into one useful answer.

It is designed for practical research tasks where a single model pass is too shallow, but a large multi-agent workflow is too expensive.

## When To Use

- Medium-size research questions with 3 to 5 natural subtopics.
- Market scans, competitor comparisons, product research, and technical surveys.
- Report drafts where evidence gathering and synthesis should be separated.
- Public-safe exploratory analysis with a clear audit trail.
- Cost-sensitive work that does not need a full premium-agent stack.

Do not use it for:

- one-off simple questions,
- high-security work with sensitive data,
- tasks requiring strict legal, medical, or financial conclusions,
- research that cannot be decomposed into clear domains.

## Public Model Pattern

Use the following roles. The exact model names can be adapted to the user's provider.

```text
Coordinator:
  - breaks the request into three domains
  - assigns domain prompts
  - merges final results
  - resolves conflicts

Domain leads:
  - analyze one domain each
  - request supporting facts or examples
  - write domain reports

Research agents:
  - gather facts, links, snippets, or local-file evidence
  - avoid final judgment
  - return structured notes to domain leads
```

## Workflow

### 1. Plan

Ask the coordinator to produce:

- the main research question,
- three non-overlapping domains,
- a domain prompt for each lead,
- an evidence request for each research agent,
- the final output format.

### 2. Gather

Run the three research agents in parallel where possible. Keep their job narrow:

- collect facts,
- inspect files,
- summarize sources,
- list uncertainties,
- return structured notes.

### 3. Analyze

Each domain lead turns one research packet into:

- domain summary,
- key evidence,
- risks or gaps,
- recommended follow-up.

### 4. Synthesize

The coordinator merges the domain reports:

- remove duplicates,
- surface disagreements,
- identify missing evidence,
- write the final answer,
- include a short audit note.

## Output Structure

Prefer this final shape:

```markdown
## Executive Summary

## Domain Findings

### Domain 1
### Domain 2
### Domain 3

## Cross-Domain Synthesis

## Gaps and Uncertainties

## Recommended Next Actions
```

## Scripts

- `scripts/lite_orchestrator.py`: standalone Python skeleton using the Anthropic SDK.
- `scripts/claude_code_runner.md`: Claude Code / agent-tool usage pattern.

The Python script expects an API key in `ANTHROPIC_API_KEY` when run directly. Do not hard-code keys in the repo.

## Quality Checks

Before returning the final result:

- confirm that all three domain reports were included,
- mark missing or weak evidence,
- separate facts from judgment,
- avoid unsupported certainty,
- include the most useful next action.

## Safety Boundary

This public version is a lightweight orchestration recipe. It does not include private scoring rules, protected workflows, tuned internal prompts, private datasets, or proprietary research benchmarks.
