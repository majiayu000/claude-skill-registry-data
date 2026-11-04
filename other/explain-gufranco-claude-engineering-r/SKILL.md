---
name: explain
description: Explain code with educational depth. Generates Mermaid diagrams for architecture and data flow, traces data through the codebase, explains design decisions with rationale, identifies patterns, and suggests improvements. Use when user says "explain", "explain this code", "how does this work", "walk me through", "what does this do", "trace the data flow", or wants to understand a file, directory, or system with educational depth. For code review, use /review; for debugging, use /investigate; for architecture assessment, use /assessment.
argument-hint: "/explain [path] [--depth shallow|deep]"
allowed-tools: "Read, Grep, Glob, Bash, AskUserQuestion"
---

## Overview

Code explanation skill with educational depth. Analyzes code structure, traces data flow, identifies patterns, and produces Mermaid diagrams to make complex systems understandable.

## When to Use

Run when the goal is understanding a file, directory, or flow. Pick `--depth shallow` for a quick orientation and the default `deep` when the reader will change the code next.

### Invocation

| Invocation | Action |
|-----------|--------|
| `/explain` | Explain the current file or most recently discussed code |
| `/explain <path>` | Explain a specific file or directory |
| `/explain --depth shallow` | High-level overview only |
| `/explain --depth deep` | Full analysis with data flow tracing and pattern identification |

If no `--depth` is specified, default to `deep`.

---

## Steps

1. **Identify the target.** Determine what to explain:
   - If no argument: use the most recently discussed file or ask for clarification.
   - If a file path: read the file.
   - If a directory path: read the directory listing, then read key files to understand the module.

2. **High-level overview.** Start with what the code does in plain language:
   - Purpose: what problem does this code solve?
   - Scope: what is included and what is delegated elsewhere?
   - Entry points: where does execution start?
   - Dependencies: what does this code depend on?

3. **Architecture diagram.** Generate a Mermaid diagram showing the component relationships:
   - For a single file: show the file's imports, exports, and how it connects to the rest of the system.
   - For a directory: show module boundaries, dependencies between modules, and data flow.
   - Use `graph TD` for hierarchical relationships, `sequenceDiagram` for request flows, `classDiagram` for type hierarchies.

4. **Data flow trace.** Follow data through the code:
   - Where does data enter the system?
   - What transformations happen at each step?
   - Where does data exit the system?
   - Generate a Mermaid `sequenceDiagram` or `flowchart` showing the data path.

5. **Pattern identification.** Identify design patterns used in the code:

   | Pattern | What to look for |
   |---------|-----------------|
   | Repository | Data access abstraction layer |
   | Strategy | Interchangeable algorithms behind a common interface |
   | Factory | Object creation delegated to a specialized function or class |
   | Observer | Event emitters, listeners, pub/sub |
   | Decorator | Wrapping behavior around existing functions or classes |
   | Middleware | Pipeline of functions processing a request sequentially |
   | State machine | Explicit state transitions with defined valid moves |
   | CQRS | Separate read and write models |
   | Dependency injection | Dependencies provided externally rather than created internally |

   For each pattern found, explain why it was chosen and what alternative would look like.

6. **Design decision analysis.** For non-obvious design choices in the code:
   - What trade-off was made?
   - What would the alternative approach look like?
   - Why was this approach likely chosen?
   - Reference comments, commit messages, or ADRs if they exist.

7. **Improvement suggestions.** If the code has issues, note them:
   - Only suggest improvements that are concrete and actionable.
   - Reference the specific rule from [`../../rules/`](../../rules) that applies.
   - Do not suggest improvements for code that is already well-structured. "No improvements needed" is valid output.

### Shallow mode

When `--depth shallow` is specified, run only steps 1-3. Skip data flow tracing, pattern identification, design decision analysis, and improvement suggestions.

### Output

```
## Explanation: <file or directory name>

### Purpose
<Plain-language description of what this code does and why it exists>

### Architecture
```mermaid
<component diagram>
```

### Data Flow
```mermaid
<data flow diagram>
```

### Patterns
| Pattern | Location | Rationale |
|---------|----------|-----------|
| <name> | <file:line> | <why this pattern was chosen> |

### Design Decisions
1. **<Decision>**: <explanation of the trade-off and reasoning>

### Improvements
| File | Line | Suggestion | Rule |
|------|------|-----------|------|
| <path> | <line> | <what to change> | <rule reference> |
| | | No improvements needed. | |
```

## Rules

- Explain for the reader's level. If the code is simple, keep the explanation short. If the code is complex, go deeper.
- Every Mermaid diagram must be valid syntax. Test by reading it back.
- Never fabricate design rationale. If the reason for a decision is unclear, say so.
- Do not explain language syntax unless the user appears to be learning the language.
- When explaining a directory, focus on the module's public API and responsibilities. Do not explain every internal helper.
- Improvements must reference specific rules. "This could be better" is not actionable.

## Common Rationalizations

- "The name says Strategy, so it is the Strategy pattern": a pattern claim needs the interface and its implementations in view. Cite the `file:line` that shows it.
- "The rationale is obvious, I will state it": invented rationale reads as fact. Cite a comment, commit, or ADR, or say the reason is unclear.
- "The diagram looks right": Mermaid that fails to parse renders nothing. Read it back and check every node and edge against the code.
- "Every helper deserves a line": a directory explanation covers the public API and responsibilities. Internal helpers stay out.
- "An improvement section looks thorough": "No improvements needed" is valid. Each suggestion names a rule.

## Red Flags

- Stop and ask which code to explain when there is no argument and no file was discussed.
- Stop and re-read the source when a diagram node names a function or module that Grep cannot find.
- Stop and mark the decision as unclear when no comment, commit message, or ADR supports a stated rationale.
- Stop at step 3 when `--depth shallow` was passed.

## Verification

- The output follows the Output template with Purpose, Architecture, and, in deep mode, every remaining section.
- Every `file:line` in the Patterns and Improvements tables opens to the cited code.
- Every Mermaid block starts with a valid diagram type such as `graph TD`, `sequenceDiagram`, `flowchart`, or `classDiagram`.
- Every improvement row names a file under [`rules/`](../../rules), or the table holds the single "No improvements needed." row.

## Related skills

- `/review` -- Review code for issues rather than explain it.
- `/assessment` -- Architecture completeness audit.
- `/investigate` -- Debug a specific problem in the code.
- `/plan` -- Plan changes to the code after understanding it.
