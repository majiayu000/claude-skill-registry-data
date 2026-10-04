---
name: agent-tooling
description: Choosing among agent tooling surfaces — when to add an MCP server vs use a CLI/WebFetch, when to render a diagram with Mermaid vs another approach, and when a piece of behavior belongs in a skill vs a dedicated agent. Use when deciding whether to wire up a new MCP server, picking a diagramming approach, or drawing the skill/agent boundary for a new capability.
---

# Agent Tooling

Dispatcher skill for three recurring "which surface" decisions when building out an
agent-driven workflow. Each heading below is a short teaser — read the linked
`references/*.md` file for the full criteria, tables, and gotchas.

## MCP Server Selection

Whether a new capability belongs behind an MCP server versus a CLI call, a `WebFetch`, or no
new tooling at all — plus the concrete anti-patterns (duplicating a CLI already in reach,
unauthenticated public APIs, always-on connections, unmaintained servers) that should stop you
before you wire one up.
Read [`references/mcp-selection.md`](references/mcp-selection.md).

## Mermaid Diagram Rendering

`mmdc` (mermaid-cli) as the sanctioned local renderer, the syntax gotchas that silently break a
diagram (`<br/>` vs `\n`, comments inside subgraphs, special characters in edge labels), and why
generating a Mermaid Live URL as a shortcut is a trap, not a convenience.
Read [`references/mermaid-diagrams.md`](references/mermaid-diagrams.md).

## Skill vs Agent Mapping

How to decide whether a piece of reusable behavior should ship as a skill (on-demand knowledge
loaded into an existing agent's context) or a dedicated agent (a separately-dispatched actor
with its own tool scope and context window), plus the discovery patterns an agent uses to find
skills at all.
Read [`references/skill-vs-agent-mapping.md`](references/skill-vs-agent-mapping.md).

## Thinking Patterns (frame before acting)

1. **Config presence != runtime liveness.** An MCP server listed as "connected," or a skill
   cited in a routing table, both describe *intent to run* — not *confirmation it ran*. Before
   trusting a mechanism, verify it actually fired (a log line, a matcher test, a liveness
   check) rather than trusting that it's configured.
2. **A benchmark number is a claim about a specific comparison, not a universal ranking.** A
   token-cost or latency benchmark for tool A vs tool B is only valid while that comparison
   holds — if the compared-against tool changes or disappears, the number needs re-measuring,
   not re-quoting.
3. **An interactive CLI's silence about non-interactive flags is not permission to loop.**
   Piping confirmation answers into a prompt that reads from the terminal directly (not stdin)
   doesn't fail loudly — it hangs or silently no-ops. Run `--help` once and look for
   `--yes`/`--no-interactive`/`--force` before piping anything at an unfamiliar CLI.
