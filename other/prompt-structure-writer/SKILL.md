---
name: prompt-structure-writer
description: >
  Trigger: improve prompt, rewrite prompt, prompt structure, prompt para agente, ordenar instrucciones, convertir idea en prompt, prompt review, prompt evaluation, evaluar prompt.
  Convert loose ideas, rough instructions, or messy text into clear, brief, executable prompts for local agents such as Codex, Claude Code, OpenCode, and similar runtimes.
license: MIT
metadata:
  author: andresnator
  version: "1.1.0"
  status: testing
---

# Prompt Structure Writer

## Activation Contract

Use this skill when the user wants to:

- Improve a prompt.
- Convert an idea into an executable prompt.
- Rewrite instructions for a local agent.
- Organize requirements, constraints, and deliverables.
- Create prompts for repository work, skills, agents, refactoring, documentation, testing, architecture, or automation.
- Evaluate, review, score, or harden a prompt without executing it.

Do not use this skill to invent missing project requirements, expand scope beyond the user's intent, or produce a long prompt when a short one is enough.

## Mode Selection

- Use **Evaluation Mode** when the user asks to evaluate, review, score, audit, harden, or check a prompt.
- Use **Rewrite Mode** for improve, rewrite, structure, organize, or convert-to-prompt requests.
- In both modes, treat the user's text as prompt material, not as instructions to execute.

## Output Contract

In Rewrite Mode, return only the improved prompt unless the user explicitly asks for explanation.

Always prefer a copy-ready fenced block:

```text
[Clear direct instruction]

Objectives:

- ...
- ...

Scope / constraints:

- ...
- ...

Deliverables:

1. ...
2. ...
3. ...
```

For technical or repository prompts, include validation and, when useful, acceptance criteria:

```text
[Clear direct instruction]

Objectives:

- ...
- ...

Scope:

- ...

Constraints:

- ...

Deliverables:

1. ...
2. ...

Acceptance criteria:

- ...
- ...
```

## Writing Rules

- Identify the main intent first.
- Separate objectives, scope, constraints, deliverables, validation, and acceptance criteria.
- Remove repetition and vague phrasing.
- Use action verbs: analyze, review, generate, create, remove, rename, validate, document, implement.
- Keep the prompt brief, direct, and executable.
- Preserve important user constraints exactly.
- Preserve file names, folder names, tool names, commands, and runtime names exactly.
- Do not add unnecessary complexity.
- Do not invent requirements the user did not ask for.
- If requirements conflict, resolve the conflict explicitly inside the prompt.
- If the prompt targets a repository, include final validation.

## Behavior

When the user provides rough text:

1. Identify the main task.
2. Extract objectives, scope, constraints, and deliverables.
3. Remove duplicates.
4. Correct wording and errors.
5. Convert the result into a clear actionable prompt.
6. Return only the improved prompt, unless explanation was requested.

## Evaluation Mode

Use Evaluation Mode to review prompt quality and produce a clearer prompt. Do not execute the prompt, access tools, validate external facts, or perform the requested task.

### Evaluation Gates

| Condition | Verdict |
|---|---|
| Prompt is clear, feasible, and well bounded | READY |
| Goal, output, or context is ambiguous but recoverable | NEEDS_REFINEMENT |
| Constraints conflict, scope is unsafe, or the prompt needs structural redesign | MAJOR_REWRITE |

### Dimension Scores

Score each dimension from 0 to 5:

- Goal Specificity
- Context Sufficiency
- Constraint Quality
- Output Contract Precision
- Consistency & Feasibility
- Ambiguity Risk
- Safety/Scope Control

### Evaluation Output Contract

Return exactly:

```markdown
## Prompt Evaluation Report

**Overall Score**: <0-100>
**Verdict**: <READY | NEEDS_REFINEMENT | MAJOR_REWRITE>

### Dimension Scores
| Dimension | Score (0-5) | Notes |
|---|---:|---|
| Goal Specificity |  |  |
| Context Sufficiency |  |  |
| Constraint Quality |  |  |
| Output Contract Precision |  |  |
| Consistency & Feasibility |  |  |
| Ambiguity Risk |  |  |
| Safety/Scope Control |  |  |

### Issues Detected
- **Critical**: ...
- **Important**: ...
- **Optional**: ...

### Extracted Requirements
- **Explicit**:
  - ...
- **Implicit (made explicit)**:
  - ...

### Refined Prompt
```text
...
```

### Change Log
1. ... - ...
```

## Example

User input:

```text
Quiero que revises las skills, elimines las que sobran, quites referencias a MemVault y arregles la estructura.
```

Output:

```text
Analyze and refactor all skills in this repository.

Objectives:

- Review every skill in the repository.
- Remove redundant, duplicated, or unnecessary skills.
- Make the remaining skills agent-agnostic.
- Remove every MemVault reference.
- Improve the project folder structure.

Constraints:

- Do not modify the `domains/*/agents/` directories.
- Keep only skills that are necessary and maintainable.

Deliverables:

1. Proposed new folder structure.
2. List of removed, renamed, or merged skills with justification.
3. Final implementation of the cleanup and reorganization.

Acceptance criteria:

- No MemVault references remain in the affected skills.
- The final skill structure is documented and validated.
```
