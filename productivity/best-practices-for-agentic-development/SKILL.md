---
name: best-practices-for-agentic-development
description: Use when designing, building, reviewing, testing, or improving agents, agentic workflows, agent skills, MCP servers, tool interfaces, subagent systems, or agent-development methodology
metadata:
  last_updated: "2026-08-18"
---

# Best Practices for Agentic Development

Use this as the master routing skill for agentic-development work. Load the reference file that matches the task before making design or implementation decisions.

Core principle: Agentic systems are engineered through behavior, context, tools, evals, and operational guardrails. Do not solve every problem with a larger prompt.

## Route First

Pick the relevant reference:

| Task | Read |
| --- | --- |
| Creating, editing, packaging, auditing, or testing skills | `references/skill-development.md` |
| Designing an agent product, tool-using assistant, memory layer, eval loop, or agent architecture | `references/general-agent-development.md` |
| Building multi-step software-development workflows with planning, subagents, verification, reviews, worktrees, and delivery gates | `references/agentic-development.md` |
| Designing or implementing MCP servers, MCP tools, tool schemas, resources, prompts, or context-efficient MCP workflows | `references/mcp-development.md` |

If more than one applies, read the most specific file first, then read others only for missing concerns.

## Universal Practices

Apply these across all agentic-development work:

1. **State the behavior.** Define what the agent should do in observable terms.
2. **Choose the right enforcement surface.** Use skills for judgment, tools/scripts for deterministic checks, hooks for runtime gates, and evals for behavioral confidence.
3. **Use progressive disclosure.** Keep always-loaded context small; load details on demand.
4. **Prefer gates over rules.** A gate blocks progress until objective evidence exists.
5. **Test behavior under pressure.** Normal prompts do not prove adherence.
6. **Capture rationalizations.** Convert observed excuses into red flags and counters.
7. **Verify before claiming.** Completion claims need fresh evidence.
8. **Design for harness reality.** Detect available tools, sandbox limits, worktree state, subagents, hooks, and native capabilities before acting.
9. **Match guidance form to the failure shape.** Prohibition, positive recipe, structural required field, or condition. Prohibition is not a universal fix. See skill-development.md.

## Enforcement Surface Decision

| Need | Use |
| --- | --- |
| Reusable judgment, workflow, or pattern | Skill |
| Large reference or examples | Markdown reference file |
| Repeated deterministic operation | Script or CLI |
| Runtime stop/continue/approval decision | Hook or wrapper |
| Agent-visible external capability | MCP tool |
| Large API or data processing without context bloat | MCP-exec-style fetch/filter/summarize workflow |
| Confidence that behavior holds | Eval harness with transcripts and assertions |
| Durable behavioral rule that must survive across turns | Re-inject into system prompt every turn (mutable rules file), not a one-time note or memory — see general-agent-development.md |

## Red Flags

Stop and re-evaluate when you think:

- "This is just prompt wording."
- "The agent will probably infer the right thing."
- "We can test later."
- "A bigger instruction block will fix it."
- "The tool schema can be verbose because context is large."
- "The subagent can just read the whole conversation."
- "The happy path worked once."
- "A prohibition list will fix this."

These are signs you need routing, gates, sharper context, or evals.

## Completion Criteria

Before considering agentic-development work complete:

- Relevant reference file has been applied.
- Behavior is stated in observable terms.
- Triggering/discovery path is clear.
- Context-loading strategy is explicit.
- Failure modes and rationalizations are addressed.
- Deterministic checks are automated where possible.
- Verification or eval evidence exists for behavior-changing work.

