---
name: ak-tech-graph
description: "Generate publish-grade SVG+PNG technical diagrams such as architecture, data flow, flowchart, sequence or concept maps in 7 visual styles."
when_to_use: "Invoke for illustrated diagrams; use /ak-preview --diagram to self-review, /ak-mermaidjs-v11 for inline docs."
category: engineering
keywords: [diagrams, architecture, flowchart, sequence, svg, png, agent, memory, visualization]
license: Proprietary; includes MIT-licensed third-party material, see LICENSE
argument-hint: "[diagram-type or system description]"
metadata:
  author: agentkit
  version: "1.1.1"
  attribution: "Vendored from fireworks-tech-graph by yizhiyanhua-ai (MIT)"
  upstream: "github.com/yizhiyanhua-ai/fireworks-tech-graph"
  upstream_sha: "7b22cdd"
  imported_at: "2026-04-28"
---

# Tech Graph

Generate production-quality SVG technical diagrams exported as PNG via `rsvg-convert`.

> Vendored from upstream `fireworks-tech-graph` (yizhiyanhua-ai, MIT). Do not
> install it separately with upstream's `npx skills add` flow. `rsvg-convert`
> remains a runtime prerequisite and must be verified before use.

## Vendoring Notes

For source updates, follow the repository
[source freshness policy](../../../../docs/operations/maintainer-sync-workflow.md#source-freshness-policy)
and discover the active source manifest rather than hard-coding a maintainer
home. Verify `rsvg-convert` through the current install/runtime contract before
claiming the dependency is available.

## Helper Scripts (Recommended)

Four helper scripts in `scripts/` provide stable SVG generation and validation:
`generate-diagram.sh` (validate SVG + export PNG), `generate-from-template.py` (create a
starter SVG from a template), `validate-svg.sh` (validate SVG syntax), and
`test-all-styles.sh` (batch test all styles). Load `references/helper-scripts.md` for
their exact invocations, options, and when to prefer hand-written SVG.

## Workflow

1. Recover the diagram's entities, edges and claims from source evidence or the user's description; mark uncertain relationships.
2. Preserve a supplied style/brand or select the default Flat Icon style. Load the matching style and diagram-type layout reference.
3. Generate using the helper that fits the input. Preserve semantic arrow meaning, readable labels, shape boundaries and self-contained SVG assets.
4. Use `generate-diagram.sh` for validation plus export when suitable; do not repeat its successful validation on unchanged bytes. Use the direct commands in `references/helper-scripts.md` when generating by hand.
5. Inspect the exported image for collisions, clipping, legibility and correct relationships. Repair and re-export when needed. If image inspection is unavailable, state that visual quality remains unverified.
6. Return the source SVG and exported PNG paths with actual validation status.

## Diagram Types & Layout Rules

Load `references/diagram-type-layout-rules.md` once the diagram type is classified: it
holds the per-type layout rules, shape choices, spacing, and viewBox sizes for
architecture, data flow, flowchart, agent architecture, memory architecture, sequence,
comparison matrix, timeline, mind map, class (UML), use case (UML), state machine (UML),
ER, and network topology diagrams.

## Drawing references

Load `references/drawing-recipes.md` for UML mappings, semantic shapes/arrows, spacing, SVG syntax and recovery recipes. Load only the matching style and diagram-type reference.

## Output

- **Default**: `./[derived-name].svg` and `./[derived-name].png` in current directory
- **Custom**: user specifies path with `--output /path/` or `输出到 /path/`
- **PNG export**: `rsvg-convert -w 1920 file.svg -o file.png` (1920px = 2x retina)

## Styles

| # | Name | Background | Best For |
|---|------|-----------|----------|
| 1 | **Flat Icon** (default) | White | Blogs, docs, presentations |
| 2 | **Dark Terminal** | `#0f0f1a` | GitHub, dev articles |
| 3 | **Blueprint** | `#0a1628` | Architecture docs |
| 4 | **Notion Clean** | White, minimal | Notes and documentation |
| 5 | **Glassmorphism** | Dark gradient | Product sites, keynotes |
| 6 | **Claude Official** | Warm cream `#f8f6f3` | Anthropic-style diagrams |
| 7 | **OpenAI Official** | Pure white `#ffffff` | OpenAI-style diagrams |

Load the matching numbered style reference for exact color tokens and SVG patterns.

## Style Selection

**Default**: Style 1 (Flat Icon) for most diagrams. Load `references/style-diagram-matrix.md` for detailed style-to-diagram-type recommendations.

These patterns appear frequently — internalize them:

**RAG Pipeline**: Query → Embed → VectorSearch → Retrieve → Augment → LLM → Response
**Agentic RAG**: adds Agent loop with Tool use between Query and LLM
**Agentic Search**: Query → Planner → [Search Tool / Calculator / Code] → Synthesizer → Response
**Mem0 / Memory Layer**: Input → Memory Manager → [Write: VectorDB + GraphDB] / [Read: Retrieve+Rank] → Context
**Agent Memory Types**: Sensory (raw input) → Working (context window) → Episodic (past interactions) → Semantic (facts) → Procedural (skills)
**Multi-Agent**: Orchestrator → [SubAgent A / SubAgent B / SubAgent C] → Aggregator → Output
**Tool Call Flow**: LLM → Tool Selector → Tool Execution → Result Parser → LLM (loop)
