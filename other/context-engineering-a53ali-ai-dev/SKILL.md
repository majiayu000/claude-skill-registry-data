---
name: context-engineering
description: Design, structure, and optimize the context you give AI coding agents. Covers system prompts, repo-level context files (CLAUDE.md, AGENTS.md, COPILOT-INSTRUCTIONS.md), what to include vs. exclude, MCP as just-in-time context, sub-agent context scoping, and treating context like code — versioned, tested, and reusable. Improves agent trust, speed, and code quality. Grounded in LeadDev and industry practice.
triggers:
  - "context engineering"
  - "agent keeps making wrong assumptions"
  - "how do I give the agent more context"
  - "write a CLAUDE.md"
  - "write an AGENTS.md"
  - "write a system prompt"
  - "agent doesn't know our codebase"
  - "agent is ignoring our conventions"
  - "too much context"
  - "context window is full"
  - "improve my system prompt"
  - "agent gives generic answers"
  - "make the agent aware of"
audience: engineer, manager
---

# Context Engineering

## Context

Context engineering is the practice of supplying **relevant, optimized information** to AI coding agents to improve their awareness and output quality. It's distinct from prompt engineering:

| | Prompt Engineering | Context Engineering |
|---|---|---|
| **Focus** | The instruction you type | What the model has access to under the hood |
| **Scope** | Single conversation turn | Persistent across sessions |
| **Output** | Refined phrasing | Structured knowledge and tool access |
| **Analogy** | Telling a colleague what to do | Giving a new hire all the docs, codebase knowledge, and tools they need |

> *"Without context, no amount of clever prompting will get you a reliable answer."*  
> — Guy Gur-Ari, Augment Code

> *"The core best practice is to treat context like code: explicit, consistent, and testable."*  
> — LeadDev, What is Context Engineering

---

## The Context Balance Problem

Context is a double-edged sword:

```
Too little context                    Too much context
──────────────────                    ────────────────
Generic boilerplate answers           Confused, unfocused answers
Ignores your conventions              Bloated context window
Misses domain knowledge               Wasted tokens / cost
Needs constant re-explanation         Slow responses
```

**The goal:** give agents exactly what they need — no more, no less — for the task at hand.

---

## What Belongs in Context

### The Seven Context Categories (LeadDev)

| Category | Examples | Format |
|----------|----------|--------|
| **System behaviors** | Codebase conventions, coding standards, architectural patterns | Markdown, code snippets |
| **System architecture** | DB schemas, service map, deployment topology, environment config | Markdown, JSON, YAML |
| **Code events** | Recent commits, open PRs, review threads, changelogs | Plain text, structured JSON |
| **Error information** | Stack traces, build output, linter warnings, incident tickets | Plain text, JSON |
| **Rationale** | ADRs, design docs, chat history summaries, meeting notes | Markdown |
| **Business rules** | Compliance policies, SLAs, feature flag states, operating procedures | Markdown, YAML |
| **Team behaviors** | Common workflows, naming conventions, PR checklist, branching strategy | Markdown |

### Priority rules

```
ALWAYS include:
  ✅ Coding conventions (naming, file structure, patterns used)
  ✅ The specific files/modules being changed
  ✅ Acceptance criteria or task description
  ✅ Relevant error messages or test failures

INCLUDE when relevant:
  ✅ Related ADRs (why this was built this way)
  ✅ API contracts or schema definitions
  ✅ Team-specific processes (PR checklist, deploy steps)

EXCLUDE:
  ❌ Entire codebase dumps (use targeted file references instead)
  ❌ Unrelated modules or services
  ❌ Old, superseded documentation
  ❌ Verbose logs when a summary is enough
```

---

## Repo-Level Context Files

The most impactful context engineering investment is a well-written **repo-level context file**. Each AI agent reads a specific file at the start of every session:

| Agent | File | Location |
|-------|------|----------|
| Claude Code | `CLAUDE.md` | Repo root (or `~/.claude/CLAUDE.md` for global) |
| Codex CLI | `AGENTS.md` | Repo root |
| GitHub Copilot | `.github/copilot-instructions.md` | Repo root |
| Cursor | `.cursorrules` | Repo root |

### What to put in a repo context file

```markdown
# Project Context — <Project Name>

## What this is
<One paragraph: what the system does, who uses it, why it exists>

## Architecture
- **Stack:** <languages, frameworks, databases>
- **Structure:** <monorepo / polyrepo, key directories>
- **Services:** <list of main services and their purposes>
- **Deployment:** <how it deploys, environments>

## Coding conventions
- **Naming:** <camelCase, snake_case, file naming patterns>
- **Patterns:** <DI container used, error handling pattern, logging pattern>
- **Testing:** <unit test framework, where tests live, coverage target>
- **Commits:** <conventional commits, squash on merge, etc.>

## Key constraints
- <"Never modify X without Y">
- <"Always use the internal HTTP client, not fetch directly">
- <"Feature flags are required for all user-facing changes">

## How to run
- **Dev:** `<command>`
- **Test:** `<command>`
- **Lint:** `<command>`

## Key files to know
- `<path>` — <what it is>
- `<path>` — <what it is>

## Out of scope for this agent
- <"Don't touch the legacy billing module">
- <"Don't regenerate migrations — ask a human first">
```

### Anti-patterns in context files

```
❌ "Please be helpful and accurate" — meaningless filler
❌ Pasting the entire README verbatim
❌ Listing every file in the repo
❌ Using jargon without definition ("use the standard pattern" — what pattern?)
❌ Outdated information that hasn't been maintained

✅ Specific conventions with examples
✅ Explicit constraints ("never", "always")
✅ Key file paths with one-line descriptions
✅ Updated when architecture changes
```

---

## Just-in-Time Context with MCP

Instead of front-loading everything, use MCP to give agents context *at the moment they need it*:

```
Static context (always loaded)          Just-in-time context (via MCP)
───────────────────────────             ──────────────────────────────
Coding conventions                      The specific Jira ticket being worked on
Architecture overview                   The Confluence page for this feature
Team workflows                          The current sprint's open issues
Key constraints                         Recent commits to the affected file
                                        The runbook for the service being changed
```

**MCP servers that provide context:**

| MCP Server | Context it provides | When to use |
|------------|--------------------|-|
| `github-mcp-server` | PRs, commits, issues, reviews | Code changes, code review, debugging |
| `jira-mcp` | Tickets, sprints, acceptance criteria | Planning, refinement, implementation |
| `confluence-mcp` | Specs, ADRs, runbooks, docs | Architecture decisions, on-call, documentation |
| `filesystem-mcp` | Local files, configs, schemas | Any file-aware task |
| `postgres-mcp` / `sqlite-mcp` | Schema, sample data, query results | Data modeling, migrations, debugging |

**The sub-agent pattern for large contexts:**

Instead of one agent with 200k tokens of context:
```
Orchestrator agent
  → lightweight catalog index
  → spawns Sub-agent A (only the files it needs)
  → spawns Sub-agent B (only the service docs it needs)
  → spawns Sub-agent C (only the error logs it needs)
  → aggregates results
```
Each sub-agent has a lean, focused context. Prevents confusion and controls costs.

---

## Skill Files as Context Engineering

The SKILL.md files in this library are a form of context engineering — they define what the agent knows about a domain, what to do, and how to respond. When writing a new skill:

**Context engineering principles applied to SKILL.md:**

| Principle | In a SKILL.md |
|-----------|--------------|
| Relevant, not exhaustive | Include only what the agent needs for this specific skill |
| Structured format | Use consistent headers: Context, Steps, Output Template, Agent Instructions |
| Testable | Triggers should be specific enough to avoid false positives |
| Versioned | Track changes in git; update when practices evolve |
| Just enough | Avoid pasting full frameworks — reference them, apply them |
| Explicit constraints | "Agent should NOT X" is as important as "Agent should Y" |

---

## Testing Your Context

Treat context like code — test it, iterate on it.

### Evaluation checklist

```
□ Does the agent correctly follow naming conventions without being reminded?
□ Does the agent avoid the explicitly excluded areas?
□ Are responses specific to the codebase, not generic?
□ Does the agent cite the right ADRs or docs when relevant?
□ Does the agent produce code that passes lint/tests on first attempt?
□ Does the agent ask for clarification on genuinely ambiguous requests?
□ Does the agent stay within its defined scope?
```

### Red flags (context is underperforming)

```
⚠️  Agent uses different naming conventions than the codebase
⚠️  Agent suggests patterns the team explicitly deprecated
⚠️  Agent asks for information that's in the context file
⚠️  Responses feel generic, not project-specific
⚠️  Agent repeatedly hits the same error in the same module
```

### Red flags (context is overloaded)

```
⚠️  Agent contradicts itself mid-response
⚠️  Responses are slower than expected
⚠️  Agent cites irrelevant sections
⚠️  Token costs are unexpectedly high
⚠️  "Lost in the middle" — ignores content at the center of a long context
```

---

## Context Engineering Maturity Levels

| Level | What you have | Impact |
|-------|--------------|--------|
| **0 — None** | No context files, paste everything manually | Generic answers, constant repetition |
| **1 — Repo file** | CLAUDE.md / AGENTS.md with conventions and architecture | Agent follows your patterns |
| **2 — Structured** | Context file + scoped MCP for Jira, Confluence, GitHub | Answers grounded in real work items |
| **3 — Just-in-time** | Sub-agents with targeted context, RAG for large doc sets | Precise, cost-efficient, scalable |
| **4 — Tested** | Context evaluated with golden examples, updated on each arch change | Trusted, consistent, production-quality |

---

## Agent Instructions

When applying this skill, the agent should:

1. Ask what the user is trying to improve (agent output quality, system prompt, context file, or MCP setup)
2. Audit the existing context (if provided) against the priority rules and anti-patterns above
3. Generate or improve the appropriate context file (`CLAUDE.md`, `AGENTS.md`, `copilot-instructions.md`)
4. Recommend which MCP servers would provide just-in-time context for this team's workflow
5. Identify context that is missing, stale, or overloaded
6. Produce a concise, structured context file with explicit constraints — not a wall of text

---

## References

- LeadDev: [What is Context Engineering](https://leaddev.com/ai/what-is-context-engineering)
- LeadDev: [AI won't fix developer productivity unless you fix context first](https://leaddev.com/technical-direction/ai-wont-fix-developer-productivity-unless-you-fix-context-first)
- Anthropic: [Claude Code — CLAUDE.md best practices](https://docs.anthropic.com/en/docs/claude-code)
- OpenAI / Codex: [AGENTS.md specification](https://openai.com/codex)
- Model Context Protocol: [MCP servers for context](https://modelcontextprotocol.io)
- Andrej Karpathy: ["Context engineering" — the new prompt engineering](https://twitter.com/karpathy)
- Mrinal Wadhwa (Autonomy): Sub-agent context scoping pattern
