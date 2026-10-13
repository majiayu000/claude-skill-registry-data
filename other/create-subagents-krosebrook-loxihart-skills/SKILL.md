---
name: create-subagents
description: Expert guidance for creating, building, and using Claude Code subagents and the Task tool. Use when working with subagents, setting up agent configurations, understanding how agents work, or using the Task tool to launch specialized agents.
metadata:
  version: "1.0.0"
---

<objective>
Subagents are specialized Claude instances that run in isolated contexts with focused roles and limited tool access. This skill teaches you how to create effective subagents, write strong system prompts, configure tool access, and orchestrate multi-agent workflows using the Task tool.

Subagents enable delegation of complex tasks to specialized agents that operate autonomously without user interaction, returning their final output to the main conversation.
</objective>

<when_to_use>
**Subagents are black boxes that cannot interact with users.** They run in isolated contexts and return only their final output. They:
- ✅ Can use Read, Write, Edit, Bash, Grep, Glob, and MCP/non-interactive tools
- ❌ **Cannot** use AskUserQuestion or any tool requiring user interaction
- ❌ **Cannot** present options or wait for user input
- ❌ The user never sees the subagent's intermediate steps

Use the **main chat (direct)** for:
- Gathering requirements from the user (AskUserQuestion)
- Presenting options or decisions
- Any task needing user confirmation/input
- Work where the user needs visibility into progress

Use a **subagent** for:
- Research tasks (API doc lookup, code analysis)
- Code generation from pre-defined requirements
- Analysis and reporting (security review, test coverage)
- Context-heavy operations that don't need user interaction

**Example workflow pattern:**
```
Main Chat: Ask user for requirements (AskUserQuestion)
  ↓
Subagent: Research API and create documentation (no user interaction)
  ↓
Main Chat: Review research with user, confirm approach
  ↓
Subagent: Generate code based on confirmed plan
  ↓
Main Chat: Present results, handle testing/deployment
```
</when_to_use>

<creation_procedure>
1. Run the `/agents` command
2. Select "Create New Agent"
3. Choose project-level (`.claude/agents/`) or user-level (`~/.claude/agents/`)
4. Define the subagent frontmatter:
   - **name**: lowercase-with-hyphens, unique
   - **description**: when this subagent should be used (drives automatic routing)
   - **tools**: optional comma-separated list (inherits all if omitted) — apply least privilege
   - **model**: optional (`sonnet`, `opus`, `haiku`, or `inherit`)
5. Write the system prompt using **pure XML structure** — remove ALL markdown headings (`##`, `###`) from the body; keep markdown formatting *within* content (bold, lists, code blocks). Use semantic tags: `<role>`, `<constraints>`, `<focus_areas>`, `<workflow>`, `<output_format>`, `<success_criteria>`, `<validation>`.
6. Tailor instructions to the specific task. Don't build generic "helper" subagents.
   - ❌ "You are a helpful assistant that helps with code"
   - ✅ "You are a React component refactoring specialist. Analyze components for hooks best practices, performance anti-patterns, and accessibility issues."

For file locations, full field parameters, configuration tables, XML-tag intelligence rules, invocation, and management, see **[references/subagent-api.md](references/subagent-api.md)**.
</creation_procedure>

<example_subagent_types>

**1. Simple — single focused task (role + constraints + workflow):**
```markdown
---
name: code-reviewer
description: Expert code reviewer. Use proactively after code changes to review for quality, security, and best practices.
tools: Read, Grep, Glob, Bash
model: sonnet
---

<role>
You are a senior code reviewer focused on quality, security, and best practices.
</role>

<focus_areas>
- Code quality and maintainability
- Security vulnerabilities
- Performance issues
- Best practices adherence
</focus_areas>

<output_format>
Provide specific, actionable feedback with file:line references.
</output_format>
```

**2. Analysis/review — domain-specialized (add focus + severity workflow):**
```markdown
---
name: security-reviewer
description: Reviews code for security vulnerabilities. Use after auth, input-handling, or API changes.
tools: Read, Grep, Glob, Bash
model: sonnet
---

<role>
You are a senior code reviewer specializing in security.
</role>

<focus_areas>
- SQL injection vulnerabilities
- XSS attack vectors
- Authentication/authorization issues
- Sensitive data exposure
</focus_areas>

<workflow>
1. Read the modified files
2. Identify security risks
3. Provide specific remediation steps
4. Rate severity (Critical/High/Medium/Low)
</workflow>
```

**3. Research + generation — multi-step (add workflow + output_format + success_criteria):**
```markdown
---
name: api-researcher
description: Researches an external API and produces integration documentation. Use when adding a new third-party integration.
tools: Read, Grep, Glob, Bash, WebFetch
model: sonnet
---

<role>
You are an API integration researcher. You read docs and source, then produce a precise integration spec.
</role>

<workflow>
1. Identify the API surface needed for the task
2. Fetch and read the relevant official documentation
3. Confirm auth model, rate limits, and required parameters
4. Produce endpoint-by-endpoint integration notes
</workflow>

<output_format>
A markdown spec: auth setup, each endpoint (method, params, response shape), and example calls.
</output_format>

<success_criteria>
Every endpoint the task needs is documented with verified parameters and a working example.
</success_criteria>
```

Match model to complexity: **Sonnet** for reasoning-heavy work, **Haiku** for simple, high-volume tasks.
</example_subagent_types>

<success_criteria>
A well-configured subagent has:
- Valid YAML frontmatter (name matches file; description includes trigger language)
- Clear role definition in the system prompt
- Appropriate tool restrictions (least privilege)
- XML-structured prompt with role, approach, and constraints
- Description field optimized for automatic routing
- Successful testing on representative tasks
- Model selection appropriate for task complexity
</success_criteria>

<references>
**API & configuration**: [references/subagent-api.md](references/subagent-api.md) — file structure/precedence, full field parameter lists, configuration tables, XML tag intelligence rules, invocation, and management.

**Usage & config depth**: [references/subagents.md](references/subagents.md) — file format, model orchestration, tool security, prompt caching, examples.
**Writing prompts**: [references/writing-subagent-prompts.md](references/writing-subagent-prompts.md) — XML structure, description routing, extended thinking, constraints.
**Evaluation & testing**: [references/evaluation-and-testing.md](references/evaluation-and-testing.md)
**Error handling & recovery**: [references/error-handling-and-recovery.md](references/error-handling-and-recovery.md)
**Context management**: [references/context-management.md](references/context-management.md)
**Orchestration patterns**: [references/orchestration-patterns.md](references/orchestration-patterns.md)
**Debugging agents**: [references/debugging-agents.md](references/debugging-agents.md)
</references>

---

## CLAIMS
<!-- [SOURCED] or [GENERATED] labels for assertions in this skill. None yet — footer added by audit fix pass. -->

## COUNTEREXAMPLE
<!-- Known cases where this skill should NOT activate or may produce wrong output -->

## CONTRADICTIONS
<!-- ! Conflicts with other skills or system prompts -->
