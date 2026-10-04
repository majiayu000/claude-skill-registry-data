---
name: adr
preamble-tier: 2
version: 0.2.0
description: |
  Architecture Deep Research — scan the current repo, draft a PRD, and run
  the deep-research loop with citation audits. Use when the user asks you to
  make an architecture decision, asks "what topology should we use?", says
  they need to pick between options like vector stores / message queues /
  retrieval patterns / storage engines / event bus designs, or wants you to
  think through an architecture choice before writing code.
  Proactively invoke this skill (do NOT decide directly) when the user
  describes an architecture choice and wants live, cited research instead
  of a model-from-memory answer.
allowed-tools:
  - Bash
  - Read
---

# /adr — Architecture Deep Research

When the user invokes `/adr` (or asks any of the trigger questions in the description above), do the following.

## Step 1. Confirm the decision name

Ask the user one question, in chat:

> What's the architecture decision you're making? (e.g. "event bus topology", "retrieval architecture", "auth provider")

Capture their answer as `<DECISION>`.

If the user already named the decision when they invoked the skill, skip the question.

## Step 2. Run discover-first deep-research via the MCP server

Call the `adr_deep_research` MCP tool with these arguments:

```json
{
  "discover_first": true,
  "repo_path": ".",
  "domain": "<infer from the user's project — read README/package.json/etc. if needed>",
  "decision": "<DECISION>",
  "out_dir": ".adr-runs/<short-slug-of-decision>"
}
```

This will:

1. Scan the user's repo and draft a PRD (no network calls).
2. Run the full ADR pipeline against the draft (research, knowledge map, comparison matrix, synthesis, citation audit, evaluation pack).
3. Return the parsed `execution-handoff.json` so you can summarize the decision.

A run typically takes 3–6 minutes. Tell the user roughly how long it'll take before calling the tool so the wait doesn't feel like a hang.

## Step 3. Summarize the result

The tool response includes:

- `handoff.selected_topology` — the chosen architecture family
- `handoff.required_invariants` — non-negotiable constraints
- `handoff.forbidden_topologies` — what NOT to do
- `handoff.critique_summary.recommend_human_review` — if true, the kernel is telling you the decision is borderline
- `handoff.comparison_matrix_summary` — candidate count, empty cells
- `handoff.citation_audit_summary` — how many citations verified

Show the user a 3–5 line summary:

```
Selected: <topology>
Required: <2 most important invariants>
Avoid:    <forbidden topologies>
<if recommend_human_review: "⚠ recommend_human_review=true — see ADR.md for the borderline.">
```

Then offer to:
- Open `ADR.md` for the full human-readable decision record
- Walk through the comparison matrix
- Implement using `execution-handoff.json` as the contract

## Step 4. (optional) Implement under the handoff

If the user says "go ahead and implement," read `<out_dir>/execution-handoff.json` and treat it as a hard contract:

- Honor `required_invariants` in the code you write
- Never reach for anything in `forbidden_topologies`
- Run against `domain-evaluation-pack.json` test cases before declaring done

## Failure modes

- **No LLM provider configured**: the tool will return an isError result. Tell the user to `export ADR_OPENAI_API_KEY=...` (or `OPENAI_API_KEY`) and re-invoke.
- **No live search provider configured**: same as above, but for `BRAVE_SEARCH_API_KEY` / `TAVILY_API_KEY` / `SERPER_API_KEY` / `SEARXNG_URL`, OR the OpenAI key fallback for hosted `web_search`.
- **`recommend_human_review: true`**: do NOT proceed to implementation. Show the user the borderline and ask whether to accept the decision, override it, or run a superseding ADR with a tighter brief.

## Notes for Claude

- The MCP tool name is `adr_deep_research`. Call it through the MCP host's tool-call mechanism — do not try to spawn a subprocess.
- The skill assumes the `adr` MCP server is registered in the user's Claude Code config. If it isn't, point them at `examples/claude-code-skill/.mcp.json` in the beevibe-cto repo.
- For quick scans without the full deep-research run, use `adr_discover` instead. It returns only the draft PRD and skips the live-research loop.
