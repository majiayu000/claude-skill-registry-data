---
name: orchestrating-subagents-and-mcp
kind: skill
status: ready
provenance:
  principles:
  - P005
  - P008
  - P009
  - P013
  - P023
  - P029
  - P031
  - P043
  - P049
  - P051
  - P052
  - P057
  - P059
  - P060
  - P063
  - P064
  - P065
  - P068
  - P073
  - P074
  - P075
  - P076
  - P082
  - P084
  - P088
  - P093
  - P095
  - P097
  - P102
  - P103
  - P105
  - P106
  - P107
  - P114
  - P115
  - P118
  - P121
  - P125
  - P126
  - P127
  - P128
  - P129
  - P130
  - P131
  - P132
  - P135
  - P146
  - P148
  - P149
  - P150
  claims:
  - C00024
  - C00026
  - C00028
  - C00029
  - C00033
  - C00034
  - C00036
  - C00037
  - C00038
  - C00039
  - C00042
  - C00043
  - C00045
  - C00046
  evidence: []
  source_anchors: []
  authored_from_digest: b548e9d92d0dcbed038603cfb921f195507d811cf309a0516c598051b3716e26
---


# Skill: orchestrating-subagents-and-mcp

## Purpose

Choose and compose the right building block — a skill, a subagent, an MCP server, a hook, a loop, or a workflow — and engineer the surrounding harness and tools. It assigns responsibilities by layer, offloads isolated side tasks to subagents, extends reach through MCP servers referenced by fully-qualified name, designs tools as clear token-efficient contracts, budgets context as a scarce resource, enforces must-happen behaviour deterministically with hooks, and reserves multi-agent orchestration for high-value parallel work while accounting for its token cost.

## When to use

- Deciding whether a capability should be a skill, a subagent, an MCP server, a prompt, or an instruction file, and how to compose them.
- Isolating a side task in a forked or subagent context, or standing up an orchestrator-worker or loop-based workflow.
- Extending an agent's reach with MCP servers and engineering the tool descriptions, schemas, and output bounds.
- Budgeting context and token cost across a long-running or multi-agent harness and guarding its dominant failure modes.

## Procedure

Work the practices the situation engages; each restates a promoted principle — apply it and cite the principle id.

- Offload discrete specialized work to subagents for context isolation and parallelism [P005].
- Assign responsibilities by layer [P008].
- For batch or destructive operations, have the agent produce a structured plan, validate it against a source of truth [P009].
- Expose many tools cheaply through deferred loading [P013].
- Extend Claude's reach with MCP servers for internal tools, data sources [P023].
- Delegate complex subtasks that should run in isolation from the main agent to subagents [P029].
- Do not rely on context compaction alone to preserve continuity across sessions; add explicit externally-persisted state [P031].
- Prefer scripts-as-tools over opaque built-in tools and capture recurring ones [P043].
- Reference MCP tools by fully qualified ServerName:tool_name to avoid tool-not-found errors, especially when multiple MCP servers are available [P049].
- As model capability improves, re-evaluate the harness against tested task performance, removing scaffolding that is no longer load-bearing and adding only pieces that unlock demonstrated capability [P051].
- Keep tool and script output predictable and context-safe with bounded summary defaults, filtering or range selection, truncation guidance [P052].
- For quality-critical refinement workflows, define a validation gate, check results immediately, fix concrete failures [P057].
- Match the building block to the need [P059].
- Use programmatic tool calling for workflows where code can reduce context bloat, inference round-trips, or fragile manual synthesis [P060].
- Prefer a runtime dependency-resolving tool runner [P063].
- Prefer a dynamic workflow over the single-context default harness when a task is long-running, massively parallel, highly structured, or adversarial [P064].
- Persist a progress file alongside git history so a fresh-context agent can quickly reconstruct the state of work and use git to revert bad changes and recover working states; this also removes wasted effort re-deriving prior [P065].
- For behavior that must happen reliably or must be blocked, enforce it deterministically with hooks [P068].
- Apply progressive disclosure [P073].
- Avoid irreversible retain/discard context decisions on long-horizon tasks [P074].
- Use tool input examples to teach conventions that schemas cannot express, including optional-field patterns, nested object usage, correlated parameters [P075].
- Write precise, context-rich prompts [P076].
- Reserve a multi-agent orchestrator-worker architecture for high-value, breadth-first tasks with heavy parallelization, information exceeding one context window, or many complex tools; do not use it for work that requires all [P082].
- Check runtime and plan prerequisites before choosing a block [P084].
- Treat skills and MCP as complementary rather than substitutes [P088].
- On difficult, policy-heavy domains, pair the think tool with an optimized prompt that gives domain-specific reasoning examples [P093].
- Do not couple session, harness [P095].
- Prefer judgement-anchored guidance over rigid rules for newer-generation models [P097].
- Budget context as a scarce resource [P102].
- Design agent tools as clear, non-overlapping, token-efficient contracts with robust behavior and unambiguous parameters [P103].
- Start with the simplest LLM design that can solve the task [P105].
- Choose workflows for predictable predefined paths and choose autonomous agents only when flexible, model-directed control is needed for an open-ended task [P106].
- Justify adopting the think tool by task complexity rather than adding it universally [P107].
- Use a subagent to isolate a side task whose intermediate output you will not reuse [P114].
- Right-size context for capable models [P115].
- Choose a skill when the need is multi-step tool workflows, consistency-critical processes, capturing and sharing domain expertise, or preserving institutional knowledge against team attrition [P118].
- Keep MCP-server instructions generic and scoped to how to operate the server and its tools correctly [P121].
- Avoid custom output styles unless a significant role change is required; prefer the built-in Proactive/Explanatory/Learning styles [P125].
- Recommend custom agents for projects or processes with distinct stages that need specialized capability, tool restrictions, or strict handoffs; define the persona at the correct location [P126].
- Use turn-based loops for short, irregular tasks [P127].
- Improve loop output quality by maintaining a clean codebase, accessible technical documentation, explicit verification [P128].
- Manage loop cost by selecting the right primitive and model, defining clear stop criteria, piloting large runs, scripting deterministic work, tuning intervals [P129].
- Rely on live agentic search rather than a maintained embedding index [P130].
- Exploit the filesystem model [P131].
- Diagnose MCP call failures in layers [P132].
- Use MCP to connect Codex to capabilities outside the local repo [P135].
- Design explicit mechanisms against the two dominant long-task failure modes [P146].
- Position the think tool as an in-flight reconsideration step used after generation has begun [P148].
- Budget for multi-agent token cost explicitly [P149].
- Virtualize an agent into independently swappable components -- a session [P150].

## Inputs

- The task or workflow to build, the building blocks and tools available, and the context, parallelism, and reliability constraints it runs under.
- The target surface(s) and any observed behaviour or failure, plus the current SKILL.md, instruction files, or layout under review.

## Output

A prioritized set of recommendations. Per finding: name the specific skill mechanism (frontmatter field, bundled file, header, flag, command, or building block), give the correction, cite the governing principle id, and state the residual trade-off or the referral. Highest-impact first. This advises how to build and operate the skill; it does not write the domain feature, edit the caller's canonical files, or assert effectiveness without an evaluation.

## Anti-patterns to flag

- Overlooking [P005]: Offload discrete specialized work to subagents for context isolation and parallelism.
- Overlooking [P008]: Assign responsibilities by layer.
- Overlooking [P009]: For batch or destructive operations, have the agent produce a structured plan, validate it against a source of truth.
- Overlooking [P013]: Expose many tools cheaply through deferred loading.
- Overlooking [P023]: Extend Claude's reach with MCP servers for internal tools, data sources.
- Overlooking [P029]: Delegate complex subtasks that should run in isolation from the main agent to subagents.

## References

See `../../references/skill-format-and-frontmatter-reference.md`, `../../references/platform-customization-matrix.md`, `../../references/context-and-harness-engineering-reference.md` for lookup detail, and `../../principles/principles.yaml` for the full statement behind every cited id.

## Grounding

Derived from P005, P008, P009, P013, P023, P029, P031, P043, P049, P051, P052, P057, P059, P060, P063, P064, P065, P068, P073, P074, P075, P076, P082, P084, P088, P093, P095, P097, P102, P103, P105, P106, P107, P114, P115, P118, P121, P125, P126, P127, P128, P129, P130, P131, P132, P135, P146, P148, P149, P150, grounded in the fifty-nine ingested distillation-only sources on Agent Skills, subagents, MCP, evaluation, and context engineering across the Claude (Code + API), OpenAI Codex, and GitHub Copilot surfaces and the open Agent Skills standard. The frontmatter `provenance` block lists the exact principle and claim ids, which resolve into `principles/principles.yaml` and `analysis/claims.jsonl`. Distillation-only: no verbatim source quotation.
