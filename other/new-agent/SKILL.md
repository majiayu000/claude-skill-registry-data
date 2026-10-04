---
name: new-agent
description: Scaffold a new Claude Code sub-agent definition under .claude/agents/. Use when the project needs a new dispatchable specialist (e.g. a domain-specific reviewer or implementer).
---

# Create a New Sub-Agent

Sub-agents are dispatchable specialists with their own tool access and
context. Use one when a chunk of work is worth delegating out of the main
session's context (its intermediate output isn't worth keeping around), or
when a domain needs a repeatable, narrowly-scoped specialist (e.g. "the
agent that reviews i18n completeness", "the agent that implements one task
end-to-end with TDD").

## Steps

1. Pick a name (kebab-case, becomes `subagent_type`).
2. Create `.claude/agents/<name>.md` with this shape:

```markdown
---
name: <name>
description: |
  <One paragraph: what this agent owns and when to dispatch it.>

  Examples:

  - user: "<a realistic request>"
    assistant: "I'll use the <name> agent to ..."
    <launches <name> agent>

  - user: "<another realistic request that should NOT dispatch this agent>"
    assistant: "<why this agent is the wrong fit / what to do instead>"
tools: <comma-separated tool list, or "All tools">
---

# <Name> Agent

<System-prompt-style body: scope, conventions to follow, what it must NOT
do, what it returns (a bounded digest, not a raw dump), and any hard
boundaries — e.g. "never pushes, never opens PRs" for an implementer
agent.>
```

3. Keep the tool list as narrow as the job allows — a reviewer agent
   probably needs `Read, Grep, Glob, Bash` and NOT `Edit`/`Write`; an
   implementer agent needs the opposite plus test-running `Bash`.
4. Write 3-5 concrete examples in the description, including at least one
   "when NOT to use this" example — that's what lets the main agent (or a
   human) route correctly without guessing.
5. Add the new agent to `.claude/agents/README.md`'s index.

## Reference agents in this template

- `.claude/agents/coder.md` — default implementer: read → RED test →
  GREEN implement → typecheck → run tests → commit → self-review → digest.
  Does NOT push, open PRs, or touch any issue tracker.
- `.claude/agents/reviewer.md` — generic code reviewer: reads a diff,
  checks it against `.claude/rules/*.md`, reports findings without editing.

Both are deliberately generic — adapt their body text (test commands,
typecheck commands, language-specific conventions) once your stack is
decided.
