---
name: agent-builder
description: Guide for designing and creating effective Claude Code custom agents (subagents). Use when users want to create, update, or optimize agents defined in .claude/agents/. Triggers on requests like "make an agent", "create a subagent", "build a reviewer agent", "add a custom agent", or "define an agent for code review".
---

# Agent Builder

Create well-designed Claude Code custom agents by following a structured process: define the role, select the right architecture, configure frontmatter, write an effective system prompt, and create the agent file.

## Agent Creation Process

1. **Clarify the agent's purpose** with concrete use cases
2. **Choose the architecture** (standalone, subagent, or team member)
3. **Design frontmatter** (tools, model, permissions)
4. **Write the system prompt**
5. **Create and validate**

### Step 1: Clarify Purpose

Ask the user:

- **What the agent does** — one sentence ("Reviews PRs for security vulnerabilities")
- **When it triggers** — specific scenarios ("After code changes to auth modules")
- **2-3 concrete examples** of tasks it would handle

### Step 2: Choose Architecture

| Pattern | When to Use | Example |
|---------|-------------|---------|
| **Standalone** | User invokes directly via Task tool | "Security reviewer I run on demand" |
| **Subagent** | Parent agent auto-delegates based on description | "Explorer spawned for codebase search" |
| **Team member** | Coordinates with peers via shared task list (agent teams) | "Frontend dev alongside backend dev" |

**Use a single agent** when: the task is sequential, context must persist across steps, or the change is small.

**Use subagents** when: you want tool/permission isolation, the work is verbose, or parallel research is needed.

**Use agent teams** when: peers must communicate directly, work decomposes into file-disjoint units, or competing hypotheses benefit from parallel investigation.

### Step 3: Design Frontmatter

See `references/claude-code-agents.md` for the complete frontmatter field reference with examples.

#### description — Trigger Mechanism

The `description` field determines when the parent agent delegates to this agent. Write it comprehensively:
- What the agent does (capabilities)
- When to use it (trigger scenarios)
- When NOT to use it (if ambiguous with other agents)

See `references/claude-code-agents.md` > "Writing Effective Descriptions" for Bad/Good examples.

#### Role — Single Responsibility

Each agent should have one clear job. As instruction complexity increases, adherence degrades.

| Role | tools | model | Use Case |
|------|-------|-------|----------|
| Explorer/Researcher | Read, Glob, Grep | haiku | Codebase search, doc lookup |
| Implementer | Read, Edit, Write, Bash | inherit | Writing code, making changes |
| Reviewer/Critic | Read, Glob, Grep, Bash | sonnet or opus | Code review, security audit |
| Planner/Architect | Read, Glob, Grep | opus | Design decisions, decomposition |
| Tester | Read, Bash, Glob, Grep | inherit | Running tests, writing tests |
| Debugger | Read, Edit, Bash, Grep, Glob | inherit | Diagnosing and fixing issues |

#### tools — Minimal Set

Apply the principle of least privilege:
- **Allowlist** only tools the agent needs via `tools` field
- **Denylist** dangerous tools via `disallowedTools` when inheriting all tools
- Fewer tools = better focus (tools are prominent in the context window)
- To restrict subagent spawning: `Task(worker, researcher)` limits which agents can be launched

#### model — Match to Task

- **haiku**: search, lookup, simple formatting (fast, cheap)
- **sonnet**: code review, implementation, debugging (balanced)
- **opus**: architecture, complex multi-step reasoning (strongest)
- **inherit**: use parent's model (default)

#### permissionMode

- **default**: asks user for permission on file writes and commands
- **acceptEdits**: auto-approves file edits, still asks for Bash
- **delegate**: delegates permission decisions to team lead (for team members)
- **dontAsk**: auto-approves file edits and Bash commands (fully trusted agents)
- **plan**: requires plan approval before making changes (good for architects)
- **bypassPermissions**: no permission prompts (use only in trusted automation)

#### Other Frontmatter

- **maxTurns**: cap agentic turns to prevent runaway agents (default: ~25)
- **skills**: preload specific skills into the agent's context
- **mcpServers**: attach MCP servers for external integrations
- **hooks**: lifecycle hooks (PreToolUse, PostToolUse, Stop) for validation guardrails
- **memory**: persistent learning scope — `user`, `project`, or `local`

### Step 4: Write the System Prompt

See `references/design-patterns.md` for detailed patterns, examples, and anti-patterns.

**Structure the prompt body (after frontmatter) in this order:**

```
1. Identity and role (1-2 sentences)
2. When invoked / trigger conditions
3. Step-by-step workflow (numbered)
4. Constraints and guardrails
5. Output format expectations
```

**Key principles:**

- **Be directive, not descriptive** — "Run tests before committing" not "It's important to run tests"
- **Use imperative form** — "Check for...", "Verify that...", "Report..."
- **Include concrete examples** over abstract rules
- **Set explicit boundaries** — what the agent should NOT do matters as much as what it should do
- **Give permission to express uncertainty** — reduces hallucination
- **Keep it under 500 words** — long prompts dilute important instructions

### Step 5: Create and Validate

Create the agent file at `.claude/agents/<agent-name>.md` using the frontmatter designed in Step 3 and the system prompt from Step 4. See `references/claude-code-agents.md` for full annotated examples to use as a starting point.

Then:

1. **Test with real tasks** — run 2-3 concrete examples from Step 1
2. **Check tool usage** — is the agent using unexpected tools or missing needed ones?
3. **Review output quality** — does the agent stay in role and follow its workflow?
4. **Tune the prompt** — add guardrails for observed failures, remove unused instructions
5. **Adjust model/tools** — slow? try haiku. Inaccurate? try opus

After two failed prompt corrections, restructure the architecture (split into multiple agents or change the workflow) rather than adding more prompt patches.

## Quick Reference: Agent Recipes

**Code Reviewer**
```yaml
name: code-reviewer
description: Reviews code for bugs, style issues, and security. Use after implementation or when explicitly asked to review.
tools: Read, Glob, Grep
model: sonnet
permissionMode: default
```
Checklist-driven review with severity ratings. Report only, never modify files.

**Test Runner**
```yaml
name: test-runner
description: Discovers and runs tests, reports failures with context. Use after code changes or when asked to verify test status.
tools: Read, Bash, Glob, Grep
model: inherit
```
Discover test framework, run tests, parse results, report failures.

**Refactoring Agent**
```yaml
name: refactorer
description: Refactors code while preserving behavior. Use for restructuring, renaming, or extracting functions. Requires plan approval.
tools: Read, Edit, Write, Bash, Glob, Grep
model: opus
permissionMode: plan
```
Preserve behavior, run tests after each change. Requires plan approval.

**Explorer**
```yaml
name: explorer
description: Fast codebase search and analysis. Use when finding files, searching patterns, or understanding code structure.
tools: Read, Glob, Grep
model: haiku
maxTurns: 15
```
Fast codebase search and documentation lookup. Read-only.

## Resources

- **Claude Code agent format reference**: See `references/claude-code-agents.md` for all frontmatter fields, file locations, and full annotated examples
- **Design patterns and anti-patterns**: See `references/design-patterns.md` for architecture patterns, prompt engineering depth, and common mistakes
