---
name: agent-creator
description: Create new Claude Code subagents (the .claude/agents/ kind, NOT skills). Use this skill whenever the user wants to create a subagent, agent, persona, specialist, role, or delegatable worker. Also use when the user says "create an agent", "make me an agent for X", "I need a specialist for Y", "set up a subagent", or wants to define a reusable AI persona with specific tool access, model selection, or permission boundaries. This skill ensures agents are created in the correct directory (.claude/agents/) with valid frontmatter — NOT as skills, NOT as "roles", NOT in any invented directory.
---

# Agent Creator

A skill for creating Claude Code subagents correctly — using the official directory structure, file format, and frontmatter schema that Claude Code actually recognizes.

## Critical: Agents Are NOT Skills

**Skills** live in `.claude/skills/` and use `SKILL.md` files. They provide knowledge and instructions that load into the main conversation context.

**Agents** (subagents) live in `.claude/agents/` and use plain `.md` files (any filename). They run in their own isolated context window with their own system prompt, tool restrictions, model, and permissions.

**NEVER:**
- Create a `roles/` directory — this is not a Claude Code concept
- Create a `ROLE.md` file — this format does not exist in Claude Code
- Put agent definitions in `.claude/skills/` — agents go in `.claude/agents/`
- Use `AGENT.md` as a filename convention — just use `{agent-name}.md`
- Invent frontmatter fields that Claude Code does not support

## When to Create an Agent vs a Skill

| User wants... | Create a... | Why |
|---------------|-------------|-----|
| A specialist persona (reviewer, architect, security auditor) | **Agent** | Needs its own context, system prompt, tool restrictions |
| Cross-domain task orchestration (migration planning, technology selection) | **Agent** | Needs to load multiple skills, run in isolation |
| Reusable knowledge/instructions (coding standards, API docs, templates) | **Skill** | Enhances main conversation, no isolation needed |
| A workflow that runs in the main conversation context | **Skill** | Skills inject into current context |
| Something that should have restricted tool access | **Agent** | Only agents support `tools` / `disallowedTools` |
| Something that should use a different model (e.g., Haiku for speed) | **Agent** | Only agents support `model` field |
| A persona with persistent memory across sessions | **Agent** | Only agents support `memory` field |

## Agent File Format

### Location and Naming

```
# Project-scoped (shared with team via version control)
.claude/agents/{agent-name}.md

# User-scoped (personal, available in all projects)
~/.claude/agents/{agent-name}.md

# Plugin-scoped (distributed via plugin)
{plugin-root}/agents/{agent-name}.md
```

- Filename uses lowercase kebab-case: `code-reviewer.md`, `security-expert.md`
- The `name` field in frontmatter is the canonical identifier (not the filename)
- When names collide, higher-priority scope wins (managed > CLI > project > user > plugin)

### Required Frontmatter Structure

```yaml
---
name: agent-name-here
description: When Claude should delegate to this agent. Write this like a routing rule — describe exact phrases and situations that should invoke this agent.
---
```

Only `name` and `description` are required. Everything else is optional.

### Complete Frontmatter Schema

```yaml
---
name: agent-name                    # REQUIRED. Lowercase letters and hyphens only
description: "When to use this"     # REQUIRED. Routing trigger for auto-delegation
tools: Read, Grep, Glob, Bash      # Optional. Allowlist of tools. Inherits all if omitted
disallowedTools: Write, Edit        # Optional. Denylist. Applied before tools allowlist
model: sonnet                       # Optional. sonnet | opus | haiku | inherit | full model ID
                                    #   Defaults to inherit (parent conversation's model)
permissionMode: default             # Optional. default | acceptEdits | auto | dontAsk | bypassPermissions | plan
maxTurns: 20                        # Optional. Max agentic turns before stopping
skills:                             # Optional. Skills to preload into agent context
  - api-conventions                 #   Full skill content is injected at startup
  - error-handling-patterns         #   Agents do NOT inherit parent skills
mcpServers:                         # Optional. MCP servers scoped to this agent
  - playwright:                     #   Inline definition (connected on agent start)
      type: stdio
      command: npx
      args: ["-y", "@playwright/mcp@latest"]
  - github                          #   String reference to existing server
hooks:                              # Optional. Lifecycle hooks scoped to this agent
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate.sh"
memory: project                     # Optional. user | project | local
                                    #   Enables persistent cross-session learning
background: false                   # Optional. true = always run as background task
effort: high                        # Optional. low | medium | high | max (Opus only)
isolation: worktree                 # Optional. "worktree" for isolated git worktree
color: blue                         # Optional. UI color: red|blue|green|yellow|purple|orange|pink|cyan
initialPrompt: "/some-command"      # Optional. Auto-submitted first turn when run via --agent
---
```

### System Prompt (Markdown Body)

Everything after the frontmatter `---` becomes the agent's system prompt. This REPLACES the default Claude Code system prompt — the agent receives ONLY this text plus basic environment details.

Write it as if you're briefing a specialist:

```markdown
---
name: security-expert
description: "Application and infrastructure security specialist. Use when the user mentions hardening, CIS benchmarks, IAM, secrets management, agent permissions, compliance (SOC2, NIST, ISO 27001), or security audits. Use proactively after infrastructure changes."
tools: Read, Grep, Glob, Bash
model: sonnet
memory: project
---

You are a senior security architect with deep expertise in infrastructure hardening, identity management, and zero-trust design.

## Your Approach

1. **Scope the security domain** — classify: hardening, IAM, agent permissions, secrets, compliance
2. **Identify technologies** — determine which platforms, services, and tools are in play
3. **Assess current posture** — gather configuration info, identify gaps against benchmarks
4. **Produce deliverable** — hardening checklist, IAM policy design, compliance mapping

## Guardrails

- Default to deny — least privilege unless the user explicitly specifies otherwise
- Never weaken security for convenience without explicit user acknowledgment
- Always flag when a recommendation trades security for usability
- Agent permissions must be scoped to specific operations, never wildcard access

## Output Format

Structure findings as:
- **Critical** (must fix) — active vulnerabilities or misconfigurations
- **Warning** (should fix) — deviations from best practice
- **Advisory** (consider) — improvements for defense in depth
```

## Creating an Agent: Step by Step

### 1. Understand Intent

Ask the user:
- What task or domain should this agent specialize in?
- Should it be read-only (reviewer, researcher) or have write access (fixer, implementer)?
- Does it need specific tool restrictions?
- Should it use a particular model (Haiku for speed, Opus for complex reasoning)?
- Should it persist learnings across sessions (memory)?
- Project-scoped or user-scoped?

If the user already described what they want in the conversation, extract answers from context first. Don't re-ask what's already been said.

### 2. Choose Scope

| Scope | Location | Use when |
|-------|----------|----------|
| Project | `.claude/agents/` | Agent is specific to this codebase, team should share it |
| User | `~/.claude/agents/` | Personal agent, available everywhere |

Default to **project** scope unless the user says otherwise.

### 3. Design Tool Access

Common patterns:

| Pattern | Tools | Use case |
|---------|-------|----------|
| Read-only researcher | `Read, Grep, Glob` | Code review, analysis, exploration |
| Read + execute | `Read, Grep, Glob, Bash` | Diagnostics, testing, validation |
| Full access | *(omit tools field)* | Implementation, refactoring, fixes |
| Full minus writes | `disallowedTools: Write, Edit` | Analysis that can run commands but not modify files |

### 4. Write the Agent File

Create the file at the appropriate location:

```bash
# Project-scoped
mkdir -p .claude/agents
# Then create .claude/agents/{name}.md

# User-scoped
mkdir -p ~/.claude/agents
# Then create ~/.claude/agents/{name}.md
```

### 5. Validate

After creating the agent file, verify:

- [ ] File is in `.claude/agents/` (project) or `~/.claude/agents/` (user) — NOT in `.claude/skills/`
- [ ] File extension is `.md`
- [ ] Frontmatter has `---` delimiters
- [ ] `name` field exists and uses lowercase-kebab-case
- [ ] `description` field exists and describes WHEN to delegate (not just WHAT it does)
- [ ] `tools` field (if present) only lists valid Claude Code tools
- [ ] `model` field (if present) uses a valid value: sonnet, opus, haiku, inherit, or full model ID
- [ ] `memory` field (if present) uses: user, project, or local
- [ ] No invented/unsupported frontmatter fields
- [ ] System prompt is clear, actionable, and written for a specialist audience
- [ ] No references to "ROLE.md", "roles/", or other non-standard conventions

### 6. Test

Tell the user they can test the agent immediately:

```
# In Claude Code, reload agents
/agents

# Or invoke directly
@agent-name do the thing

# Or let Claude auto-delegate by describing the task naturally
```

## Valid Tool Names Reference

These are the tool names Claude Code recognizes in `tools` and `disallowedTools`:

**File operations:** `Read`, `Write`, `Edit`, `MultiEdit`
**Search:** `Glob`, `Grep`
**Execution:** `Bash`
**Agent orchestration:** `Agent`, `Agent(specific-agent-name)`
**Other:** `WebFetch`, `TodoRead`, `TodoWrite`, `AskUserQuestion`
**MCP tools:** Referenced by their MCP tool name (e.g., `mcp__github__create_issue`)

## Example Agents

### Minimal: Code Reviewer

```markdown
---
name: code-reviewer
description: "Expert code reviewer. Use proactively after code changes to check quality, security, and best practices."
tools: Read, Grep, Glob, Bash
model: sonnet
---

You are a senior code reviewer. When invoked:

1. Run `git diff` to see recent changes
2. Focus on modified files
3. Review for: clarity, error handling, security, performance, test coverage

Provide feedback organized by priority:
- **Critical** (must fix)
- **Warning** (should fix)
- **Suggestion** (consider improving)

Include specific examples of how to fix issues.
```

### With Memory: Architecture Consultant

```markdown
---
name: architecture-consultant
description: "Technology selection and architecture design specialist. Use when the user needs help choosing technologies, designing system architecture, evaluating trade-offs between approaches, or planning technical strategy. Use proactively when the user mentions 'which database', 'what stack', 'architecture review', or 'technology comparison'."
tools: Read, Grep, Glob, Bash
model: opus
memory: project
skills:
  - database
  - cloud-platforms
---

You are a principal architect with 20+ years across distributed systems, databases, cloud platforms, and enterprise architecture.

## Your Process

1. **Gather requirements** — workload type, scale, consistency needs, team expertise, budget, compliance
2. **Map the solution space** — identify candidate technologies, reference your memory for past decisions in this project
3. **Evaluate trade-offs** — produce a comparison matrix with weighted scoring
4. **Recommend** — ranked options with clear rationale and risk callouts

## Communication Style

- Lead with the recommendation, then justify
- Use concrete numbers where possible (latency, throughput, cost)
- Flag assumptions explicitly
- When trade-offs exist, present them as choices for the user, not decisions

## Memory

Update your memory after each consultation with:
- Technologies evaluated and decisions made
- Constraints discovered (compliance, team skills, budget)
- Architecture patterns established for this project
```

### With Hooks: Database Query Validator

```markdown
---
name: db-reader
description: "Execute read-only database queries for analysis and reporting. Use when the user wants to query data, generate reports, or analyze database contents."
tools: Bash
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate-readonly-query.sh"
---

You are a database analyst with read-only access. Execute SELECT queries to answer questions about the data.

When asked to analyze data:
1. Identify which tables contain the relevant data
2. Write efficient SELECT queries with appropriate filters
3. Present results clearly with context

You cannot modify data. If asked to INSERT, UPDATE, DELETE, or modify schema, explain that you only have read access and suggest the user perform the operation directly.
```

### Plugin-Distributed Agent

When creating agents for a plugin:

```
my-plugin/
├── .claude-plugin/
│   └── plugin.json
├── agents/
│   ├── security-expert.md
│   └── migration-planner.md
├── skills/
│   ├── database/
│   │   └── SKILL.md
│   └── security/
│       └── SKILL.md
└── README.md
```

Note: Plugin agents cannot use `hooks`, `mcpServers`, or `permissionMode` frontmatter. These are stripped for security. If you need those features, the user must copy the agent into `.claude/agents/` or `~/.claude/agents/`.

## Common Mistakes to Avoid

1. **Creating a `roles/` directory** — This does not exist in Claude Code. Use `.claude/agents/`
2. **Using `ROLE.md` or `AGENT.md`** — Just use `{name}.md`
3. **Putting agents in `.claude/skills/`** — Skills and agents are different. Agents go in `.claude/agents/`
4. **Inventing frontmatter fields** — Only use fields from the schema above. `capabilities`, `workflow`, `type: role`, `domains`, `persona` are NOT valid frontmatter
5. **Forgetting the description is a routing rule** — Claude uses the description to decide auto-delegation. Write it like trigger criteria, not a job title
6. **Making the system prompt too vague** — The agent gets ONLY this prompt. Include specific instructions, not just a persona description
7. **Over-granting tool access** — If the agent only needs to read, don't give it Write/Edit. Least privilege
8. **Not testing** — After creating, run `/agents` or `@agent-name` to verify it loads
