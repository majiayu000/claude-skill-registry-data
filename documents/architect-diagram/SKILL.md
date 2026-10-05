---
name: architect-diagram
description: Use when the user asks for a diagram of a system, integration, flow, state, data model, deployment topology, roadmap, prioritization matrix, or decomposition. Triggers on "show me", "draw", "diagram of", or artifact-shaped nouns like "sequence", "C4 Container view", "state machine", "roadmap", "2×2", "mind map". Produces Mermaid diagrams (flowchart, sequenceDiagram, C4, stateDiagram-v2, erDiagram, plus timeline, quadrantChart, and mindmap for roadmaps, prioritization, and hierarchical decomposition) routed by intent. Cloud-aware (AWS, Azure, GCP, and primitives providers like Hetzner) and agentic-platform-aware (Bedrock AgentCore, AI Foundry, Vertex Agent Engine). Do NOT use for full design-doc drafting (use `architect-design`), critique (use `architect-review`), or comparison tables (use plain Markdown).
---

# Skill: architect-diagram

Produce Mermaid diagrams that survive enterprise wiki rendering and stay
readable at a glance. Structural discipline (boundaries, technology labels,
trust zones) beats pretty.

## Mode detection — pick one at entry

Read the user's message and route once. Don't ask the user to flag intent.

| Signal | Mode |
| --- | --- |
| Vague idea, no code or paths in scope. "Draw me how a checkout flow could look." | **design** |
| Repo path, file list, or "the system as it is today" in scope. | **document** |
| Diagram pasted into the conversation + "is this ok / what's wrong". | **review** |
| Existing diagram + a diff request ("add a caching layer", "remove X"). | **update** |

If two modes plausibly fit, ask once which the user wants.

- **design** — generate from the user's words. Fabricate component
  names only where the user hasn't named one; flag fabrications.
- **document** — read the code or paths first; only diagram what is
  actually there. Never invent names.
- **review** — quick rubric pass against `references/diagram-rubric.md`;
  if the user wants severity-tagged findings, route to the
  `architect-review` skill (if installed) for the full critique.
- **update** — apply the requested diff. Surface side-effects the user
  didn't ask for (orphaned nodes, broken trust boundaries).

## Procedure

1. **Route by mode** (above). For *document* mode, read before drawing.

2. **In document or update mode — extend "read the repo" to "read the
   landscape."** *Only* in these two modes, and *only* when the as-is system
   integrates **beyond the repo boundary** and an *internal* knowledge-retrieval
   surface is reachable this session (an enterprise-knowledge MCP tool, an
   internal CLI, an in-repo doc set — public web does **not** count), load
   `references/knowledge-surfaces.md` and consult the descriptive current-system
   facets (current landscape, interfaces, operational reality) to ground the
   beyond-repo boxes, arrows, and edge labels. **Name what you drew from** (the
   surface, or "repo only / none"). A node or edge you can't ground stays
   `<unnamed>` or becomes a question — never a guess (this strengthens the
   never-fabricate-names rule below); a surface-derived edge the repo
   contradicts is **flagged**, not silently drawn over. This step does **not**
   apply in **design** mode (you're drawing the user's hypothetical —
   fabrication is allowed-but-flagged) or **review** mode (route to
   `architect-review`).

3. **Pick the notation from intent.** Always load
   `references/notation-routing.md` — it carries the intent → notation
   decision table, the split-when-too-big rule, and the *don't draw*
   cases (comparison, checklist, two-component flow).

4. **Load the syntax reference for the chosen notation** —
   `references/mermaid-{flowchart,sequence,c4,state,er}.md`, one file
   per notation, on demand. For the three newer product/roadmap
   grammars, load `references/mermaid-{timeline,quadrant,mindmap}.md`
   — each carries the rendering caveat, the table/bullet-list fallback,
   and the per-type complexity budget. For C4 Container drafts, the
   starter shape is in `assets/c4-container.mmd`.

5. **Load cross-cloud patterns for any cloud-aware diagram.** Load
   `references/cloud-patterns.md` whenever the diagram crosses cloud
   boundaries — boundary stack, public-vs-private subnets, async vs.
   sync edges, trust-boundary labeling, storage shapes. Then layer
   the vendor-specific reference:

   - **Any AWS / Azure / GCP service — or a primitives provider
     (Hetzner and its class)** → load `references/cloud-<cloud>.md`
     (incl. `cloud-primitives.md`) for boundary vocabulary, subgraph
     nesting, and gotchas. Multi-cloud → load multiple references.
   - **Agentic platform named** → load
     `references/agentic-<platform>.md` (`bedrock-agentcore`,
     `ai-foundry`, `vertex-agent-engine`). A diagram of AgentCore is
     *not* "AWS with a Lambda in it".

6. **Draft the diagram inline.** Default to `flowchart TB` with
   subgraph nesting and emoji or text markers — renders cleanly in
   GitHub, Confluence, Azure DevOps Wiki, and GitLab. Only if the
   user's target renderer is known to support it, mention Mermaid's
   newer `architecture-beta` syntax as an alternative — load
   `references/mermaid-architecture-beta.md` for the trade-offs and
   skeleton before offering. Do not default to it; rendering is
   inconsistent across enterprise wikis. **When the diagram
   distinguishes more than one category of thing or relationship, load
   `references/visual-encoding.md`** — map each visual channel (shape,
   grouping, position, edge style, marker) to meaning by data type, and
   keep colour as reinforcement only, never the sole carrier.

7. **Self-check against `references/diagram-rubric.md`.** Fix
   violations before showing the user. The non-negotiables: every
   Container has a technology label; no bare relation labels; fits
   one screen (≤15 nodes); document mode never fabricates names;
   trust boundaries are visible (dashed subgraph border or explicit
   comment).

8. **Offer to save.** Scan for an obvious home (`docs/architecture/`,
   `diagrams/`, `docs/`). Suggest a kebab-case `.mmd` filename.
   Saving is an offer, never automatic.

## Anti-patterns to refuse

- **Drawing without naming the trust boundary.** A cross-account or
  cross-tenant arrow without a labeled boundary is a security hazard
  rendered as art. Add the boundary, then draw.
- **Picking the notation the user named when the intent disagrees.**
  If the user asks for a "sequence diagram" of *what talks to what*,
  the right answer is a Container view. Push back; offer both.
- **Defaulting to `architecture-beta` because it looks nicer.**
  Enterprise wikis render flowchart consistently; architecture-beta
  is uneven. Mention it as an option, not the default.
- **Fabricating service or component names in document mode.** Read
  the code; if a name isn't there, mark the node `<unnamed>` or ask.
