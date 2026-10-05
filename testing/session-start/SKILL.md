---
name: session-start
description: 'Use this skill at the start of every session to orient in the codebase, load relevant context, and warm up before any task. Invoke when the user says "start session", "begin work", "orient yourself", "what is the state of the project", or at the very beginning of a new conversation.'
---

### Session Start Protocol

Run these steps at the beginning of every session, before any task work.

#### 1. Load directives

Review available agent context and configuration for this project:
- Check `AGENTS.md`, `CLAUDE.md`, or equivalent agent instruction files for durable directives, preferences, workflow defaults, coding standards, and model strategy.
- Load global rules that apply across all sessions.

Then load project-specific context:
- Review `README.md`, `CONTRIBUTING.md`, and any relevant `docs/agent-guides/` files.
- Identify repository conventions, architecture patterns, key commands, known failures, and recurring patterns.

#### 2. Load mental models

Review the architectural overview of the project:
- What are the main primitives, agents, and workflows?
- How do integrations connect (MCP, databases, LLM providers)?
- What is the current state of the codebase (recent commits, open PRs, open issues)?

Use `git log --oneline -10` to see recent changes and understand current momentum.

#### 3. Recall task-specific context (if task is known)

If a specific module, feature, or component is the target, locate it in the codebase:
- Find the relevant source files and test files.
- Check for related documentation in `docs/`.
- Look for any open issues or TODOs related to the target area.

#### 4. Orient with code analysis

Confirm the codebase structure is as expected:
- Run `find ttadev/ -name "*.py" | wc -l` to confirm the graph is current.
- If the task involves specific files or functions, locate them and understand their position in the dependency graph.
- Check for any failing tests: `uv run pytest --tb=no -q 2>&1 | tail -5`

#### 5. Acknowledge

State briefly what you loaded — active directives, architectural context, current codebase stats — so the user knows the session started warm. Include:
- Key conventions in effect
- Any known issues or blockers
- Your understanding of the immediate task

#### Session End: Retain

Before ending the session or after completing a significant task, document:
- Key decisions made and their rationale
- Patterns discovered or established
- Failures encountered and how they were resolved
- Architectural insights relevant to future sessions

Save this as an atomic note (see `create-atomic-note` skill) or document it in the appropriate `docs/` location.

Use this format for session notes:
```
[type: decision|pattern|failure|insight] <what happened>
Rationale/why: <the reason>
Context: <module or area affected>
```
