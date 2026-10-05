---
name: analyze-prompt-influence
description: Use when separating prompt-driven behavior from code-driven behavior, understanding what system prompts actually control vs what's hardcoded, or testing how behavior changes under different prompt configurations
---

## Announce at start: "Using codebase-analyzer to analyze prompt influence."

## Overview

Compare two influence sources: (1) what the system prompt instructs, (2) what the code actually enforces. Determine the gap between "told to do" and "forced to do."

**Prerequisite:** Reads `docs/analysis/tool-graph.md` and `docs/analysis/gate-map.md` (from `extract-tool-graph` and `map-feature-gates`).

## The Brilliant Secret

**Prompt is not behavior.** This is the single most important insight for analyzing control architecture. A system prompt that says "don't do X" is a suggestion. Code that removes tool X from the tool registry is enforcement. The gap between them is where the real control architecture lives -- and where the real vulnerabilities hide.

Every "prompt-driven" behavior falls somewhere on this spectrum:

```
Suggestion <-------> Enforcement
    |                    |
    v                    v
 Prompt only         Code only
 "Be concise"     Token limit=500
 "Don't do X"     Tool X not registered
 "Focus on Y"     SQL filter WHERE y=Y
```

Most systems have behaviors scattered across the entire spectrum. The analyst's job is to map each one and find the gaps.

## Part 1: Prompt Control Extraction

1. Find all system prompt templates and instructions
2. Map prompt-driven behaviors: what the prompt tells the system to do
3. Identify prompt variables and conditional sections
4. Find prompt versioning/A-B testing patterns
5. For each prompt instruction, classify its enforcement level:
   - **Suggestion only**: Prompt says it, no code backing (e.g., "be helpful")
   - **Partially enforced**: Prompt + some code checks (e.g., "don't access files" + partial path filtering)
   - **Fully enforced**: Code makes prompt instruction redundant (e.g., "don't use shell" + shell tool removed from registry)

## Part 2: Gap Analysis Methodology

For each behavior dimension, run this three-question protocol:

1. **What does the prompt SAY to do?** (declared control)
2. **What does the code ENFORCE?** (actual control)
3. **What's the gap?** (The gap IS the control architecture. A wide gap means the system relies on the model's compliance, not engineering controls.)

Classify each gap:
- **No gap**: Code enforces exactly what the prompt says. The prompt is documentation, not control.
- **Narrow gap**: Code enforces the spirit of the prompt. Minor edge cases are prompt-only.
- **Wide gap**: Prompt declares a behavior that code does not enforce. This is trust-based control.
- **Reverse gap**: Code restricts something the prompt does not mention. Undeclared control -- often intentional defense-in-depth.

## Part 3: Expanded Comparison Dimensions

Map prompt vs code control across these behavioral dimensions:

| Dimension | Prompt Control (Says) | Code Enforcement (Does) | Gap Type |
|-----------|----------------------|------------------------|----------|
| **Tool usage** | "Use tool X only when Y" | Tool X registered only if gate Y passes | Variable -- check registration |
| **Response style** | "Be concise" / "Use markdown" | Token limit, output schema validation | Usually wide -- style is prompt-only |
| **Safety** | "Don't generate harmful content" | Output classifier + filter pipeline | Critical if prompt-only |
| **Capabilities** | "You can do X" | X only available if feature flag is on | Medium -- flag controls existence |
| **Data access** | "Only access user's own data" | Query-level row filtering, API scope checks | Critical if prompt-only |
| **Error handling** | "Apologize and retry" | Automatic retry with backoff in code | Usually narrow -- code handles it |
| **Rate limiting** | "Don't spam the user" | Hard throttle in middleware | Usually narrow |
| **Context scope** | "Focus on the current project" | File path sandboxing, repo boundary checks | Variable -- check sandbox config |

For each dimension, the analyst must answer: if the model ignores the prompt, what happens? If the answer is "nothing prevents it," that is a wide gap.

## Quick Reference

| Dimension | Prompt Control | Code Enforcement |
|-----------|---------------|-----------------|
| Tool usage | "Use tool X only when Y" | Tool X registered only if gate Y passes |
| Response style | "Be concise" | Token limit in code |
| Safety | "Don't generate harmful content" | Output filter in code |
| Capabilities | "You can do X" | X only available if feature flag on |

## Key Insight

**The gap is the architecture.** Systems with wide gaps in safety-critical dimensions (data access, tool usage, safety) rely on model compliance rather than engineering controls. This is the most important finding in any prompt influence analysis.

## Red Flags

- Treating prompt instructions as guaranteed behavior
- Not finding the code-level enforcement (or lack thereof)
- Missing conditional prompt sections that vary by user type
- Safety behaviors that are prompt-only (wide gap in safety dimension)
- Data access controls that exist only in prompt text
- Assuming "the prompt says no" means "the system cannot"

## Output Contract

Write `docs/analysis/prompt-influence.md` using standard contract.
Include: prompt controls, code controls, gap analysis by dimension, behavioral dimensions with gap classification, and a summary of which dimensions are engineering-controlled vs trust-controlled.
