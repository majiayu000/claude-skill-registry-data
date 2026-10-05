---
name: code-generate-docs
description: Generate or update documentation. Use when asked to add comments, docstrings, module docs, README sections, or reference documentation.
---

Generate documentation that matches existing project conventions.

## Process

### Step 1 - Identify Context

- Check for code changes via `jj diff -s`, then target specific files/directories with `jj diff -- path`.
- Focus on user-specified files, modules, target audience, or requirements.
- Identify the documentation type (e.g., inline comments, docstrings, module/file docs, README sections, or reference guides).

### Step 2 - Research and Plan

Apply a scout lens to identify existing documentation style, naming, structure, examples, and relevant code context for `{files or requirements}`:

- Map relevant files, conventions, and call paths.
- Cite file paths and line numbers.
- Distinguish confirmed patterns from one-offs.
- Stay read-only.
- Keep it concise and task-relevant.

Apply a planner lens to draft the minimal documentation structure to explain behavior, intent, data flow, or tradeoffs:

- Prefer simple, boring solutions.
- Preserve existing project patterns.
- Make tradeoffs and assumptions explicit.
- Scope the plan to the current problem.

Apply a reviewer lens to review the proposed documentation for clarity, convention fit, accuracy, and unnecessary detail:

- Ground findings in file paths and line numbers.
- Prioritize the requested lens.
- Distinguish confirmed findings from speculative risks.
- Explain why each issue matters.

### Step 3 - Inspect Conventions

- Inspect adjacent code and documentation to match layout, heading style, naming, and depth of detail.
- Check `README.md`, `CONTRIBUTING.md`, `AGENTS.md`, `GEMINI.md`, or `CODEX.md`.

### Step 4 - Generate Documentation

- Match existing documentation style and structure.
- Explain design intent and _why_ choices were made, not obvious mechanics.
- Provide concise, verified examples based on actual code.
- Avoid changelog-style comments.

### Step 5 - Verify

- Run formatting, markdown linting, doc builds, or link checks if configured and relevant.
- Otherwise, review new documentation against current code for accuracy.

### Step 6 - Report

Report to the user:

1. **Documentation Scope**
2. **Conventions Detected**
3. **Documentation Added / Files Changed**
4. **Verification Results**
5. **Remaining Follow-up**
