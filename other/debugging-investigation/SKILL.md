---
name: debugging-investigation
description: Debugging guidance and structured report template for thorough bug investigation, evidence gathering, and root cause documentation.
compatibility: opencode
metadata:
  audience: debugging
  purpose: investigation-guidance
---

## Core approach

- Reproduce the problem if feasible.
- Gather evidence before drawing conclusions.
- Separate observations, hypotheses, and confirmed root causes.
- Narrow the failure surface methodically.
- Prefer the smallest fix that addresses the actual cause.

## Practical guidance

- **Ground before you guess.** Before proposing a diagnosis, fix, or design, enumerate the load-bearing claims it depends on (what specific code does, what payloads contain, where errors originate, how working siblings of the same shape behave). Mark each `read` (you've inspected the actual source in this session) or `assumed`. Read the assumed ones — or downgrade the proposal to "still investigating" — before writing it down. Output the claim list visibly in your summary. A proposal that departs structurally from working in-tree siblings of the same shape (plugin, provider, integration, form, migration, adapter, command) treats the deviation as the first hypothesis to disprove, not a feature.
- Look at logs, tests, stack traces, configuration, recent changes, and runtime assumptions together.
- Pay attention to environment differences, race conditions, stale state, and boundary failures.
- When reproduction is incomplete, be explicit about what is inferred.
- Trace the complete end-to-end code flow — from user interaction or trigger through every layer to where the bug manifests. Do not stop at the immediate method.
- Read every file in the flow. Do not skim or assume.
- Look for secondary defects in the same flow — other bugs that aren't the reported issue but would cause problems.
- Check all code paths that could trigger the issue (different input formats, config modes, error handling branches).

## Investigation report template

Use this template when documenting investigation findings. All sections are required unless explicitly not applicable. Add additional sections for information that doesn't fit the template.

```markdown
## Summary

### Categorization
| Attribute | Assessment |
|-----------|------------|
| **Criticality** | [critical/high/medium/low] — [short explanation] |
| **Ease of Fix** | [easy/moderate/hard] — [short explanation] |
| **Caused by our codebase?** | [Yes/No] — [short explanation] |
| **Needs more research?** | [Yes/No] — [short explanation] |

### Background
[Simple text description of what this bug is, its complexity, criticality, and estimated fix effort]

### Analysis
[Simple description of why it is occurring]

### Root Cause
[Simple description of the root cause]

### Source
[Simple description of what code is involved]

### Fix Direction
[Simple description of what is needed to fix the issue — high level only, no implementation details]

---

## Problem Statement
[Full research details on the issue and cause. Include reproduction steps if available. Reference specific error messages, logs, stack traces.]

## Environment Details
[List any relevant setup, config, or environmental details or factors. If not applicable, say so.]

---

## Root Cause Analysis
[Full root cause analysis with evidence. Cite specific code, conditions, and data that prove the root cause. Separate confirmed findings from hypotheses.]

---

## Code Flow (End to End)
[Numbered list of the complete code flow from the entry point (user interaction, API call, job trigger) through every layer to where the bug manifests. Include file paths and line numbers at each step.]

1. `path/to/file.ext:NN` — [what happens at this step]
2. `path/to/file.ext:NN` — [next step in the flow]
3. ...

---

## Key Files

[Group by logical area. Each area gets a table.]

### [Area name, e.g., "API Layer" or "Storage Service"]
| File | Lines | Relevance |
|------|-------|-----------|
| `path/to/file.ext` | NN–MM | [description of relevance] |

### [Next area]
| File | Lines | Relevance |
|------|-------|-----------|
| `path/to/file.ext` | NN–MM | [description of relevance] |

---

## Secondary Defects
[Other bugs or concerns discovered during investigation that aren't the reported issue but exist in the same code flow. If none found, state "None identified."]

---

## Notes
[Any additional observations, context, or concerns not covered above]

---

## Recap
[2-3 sentence recap of the investigation: what the bug is, what causes it, and how severe it is]
```
