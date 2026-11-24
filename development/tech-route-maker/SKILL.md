---
name: tech-route-maker
description: Create evidence-grounded editable technical route diagrams for research and engineering projects. Use when the user asks to draw, generate, visualize, render, export, or revise a technical route diagram, research route, paper method framework, publication figure, thesis proposal route, engineering system route, software or agent workflow, pipeline, architecture roadmap, process diagram, editable PPTX/SVG/Draw.io/Mermaid/HTML diagram, or copyable Draw.io XML code. Supports implicit invocation when the user asks for route diagrams and explicit invocation with $tech-route-maker.
---

# Tech Route Maker

## Purpose

Use this skill to turn source materials into evidence-grounded editable technical route diagrams for research and engineering projects across multiple disciplines.

Primary users are researchers, students, academic writers, engineering teams and agent/tool builders preparing paper framework figures, method overview diagrams, thesis proposal routes, defense visuals, course-design diagrams, engineering system routes and workflow pipelines.

Campaign or advertising routes are legacy/experimental use cases. Do not make them the default direction unless the user explicitly asks for them.

## Portability

This skill is intentionally agent-agnostic. `SKILL.md` is the source of truth for Codex/OpenAI-style skill loaders and any agent that understands skill folders. Other adapters in the repository point back here:

- `AGENTS.md` for generic coding agents.
- `CLAUDE.md` for Claude-style project context.
- `GEMINI.md` and `.gemini/settings.json` for Gemini CLI.
- `.cursor/rules/tech-route-maker.mdc` for Cursor.
- `.github/copilot-instructions.md` for GitHub Copilot coding agent.
- `.aider.conf.yml` for Aider-style workflows.

## Default Interaction Policy

Do not interrupt the user with a long sequence of questions, but do not guess domain or delivery preferences from a field-agnostic request.

Before final rendering, explicitly establish the domain context and confirm the requested output format, target medium, layout family and visual style. Present one concise grouped choice with sensible defaults; allow single or multiple output formats. If the source explicitly proves a domain fact, extract it with an evidence locator instead of asking the user to repeat it.

Default behavior:

- Never render a final technical route diagram from a field-agnostic request such as "draw a technical route diagram" without first identifying the discipline, subfield, project type, research object, method family and evaluation logic.
- If source files are available, extract domain context only from explicit source evidence. Ask one concise field-specific clarification question for every material gap rather than silently inventing it.
- If the user asks for a quick draft before the field is complete, mark `domain_context.confidence` as `low`, keep missing items in `unresolved_questions`, and report that the output is not final.
- If the user asks in Chinese for 开题, 课题申报, 项目申请, 基金, 论文技术路线图, or a Chinese research route diagram, prefer the Chinese academic presets below.
- If the user asks for an editable presentation figure, generate `pptx`, `svg` and `json`.
- If the user asks for a paper or research figure, generate `svg`, `pptx` and `json`.
- If the user asks for a maintainable system diagram, generate `drawio`, `svg` and `json`.
- If the user asks for Draw.io, diagrams.net, online editing, import code, copyable code, or "能复制到draw.io的代码", include `drawio-code` and explain how to paste the XML into diagrams.net.
- If the user asks for documentation output, generate `markdown`, `mermaid` and `json`.
- If the user asks for long-term maintenance, add `drawio`.
- If the user asks for all formats, render `pptx`, `svg`, `drawio`, `drawio-code`, `excalidraw`, `mermaid`, `html`, `markdown` and `json`.

Always record the selected preset and output formats in `selected_preset` and `metadata.selected_output_formats`.
Always record the discipline-specific context in `domain_context`.
Always state that generated editable files are drafts that require factual, wording and visual revision before publication or submission.

## Contest-Orchestrator Adapter

When this skill is invoked from `contest-orchestrator`, read [contest-adapter.md](references/contest-adapter.md) and use it as the local route contract. This adapter has priority over generic presets for mathematical-modeling projects.

- Handle only problem-analysis flowcharts and model technical-roadmap diagrams.
- Use the project's `problem_condition_ledger.yaml`, task cards, `model_blueprint.yaml`, `model_contract.yaml`, `symbol_table.md` and `result_registry` as the source boundary.
- Keep every visible node and edge traceable to a source locator; do not invent models, variables, algorithms, tests, results or conclusions.
- Default paper outputs are `SVG + PNG` with `tech-route.json` as the editable semantic source. Produce PPTX, Draw.io, HTML or other formats only when the user explicitly requests them.
- Perform screenshots/rendering review and visual QA by default for every generated route diagram. Check spacing, alignment, clipping, overlap, hierarchy, text legibility and clean composition in addition to schema, source, text and provenance checks; the user may perform a final visual review as an additional check.
- Register the output as `kind=flowchart`, `generator=tech-route-maker`, with `diagram_role=problem_analysis_flowchart` or `technical_roadmap`.
- Return the shared node handoff fields: `status`, `active_mode`, `task_card`, `artifacts`, `evidence`, `checks`, `blockers`, and `next_node`; keep all outputs under the project workspace.
- Treat generated diagrams as project artifacts, not evidence by themselves. Captions, labels and visible claims must be source-bound and free of agent discussion, review messages, debugging, failed attempts, old versions and other negative echo.

## Domain Context Policy

Technical route diagrams are domain-sensitive. A diagram for computer vision, materials science, energy engineering, biomedical research, mechanical control, environmental field studies and social science should not share the same semantic grammar.

Before final rendering, establish:

- `discipline`: broad field.
- `subfield`: specific direction.
- `project_type`: paper figure, thesis proposal, grant application, engineering report, system architecture, experiment workflow, review framework, or similar.
- `research_object`: concrete object under study.
- `method_family`: main method type.
- `application_area`: intended use context.
- `data_or_materials`: source data, samples, materials, devices, documents, or field records.
- `technical_objects`: algorithms, modules, variables, devices, experiments, mechanisms, controls, or system components.
- `domain_constraints`: sample size, equipment, standards, deployment, ethics, cost, timeline, or data-quality constraints.
- `evaluation_metrics`: measurable success criteria.
- `expected_outputs`: figure, model, prototype, report, mechanism, dataset, application plan, or deliverable.

Read `references/domain-profiles.md` when the domain is unclear, unfamiliar, or likely to affect node semantics.

Examples:

- Computer vision / PV defect detection: separate dataset, annotation, augmentation, model architecture, training, ablation, evaluation and deployment.
- Materials science: separate material design, preparation, characterization, performance testing, mechanism analysis and application validation.
- Energy systems: separate system boundary, source/load data, optimization model, operation strategy, scenario validation and engineering deliverables.
- Biomedical research: separate sample/cohort, grouping/intervention, assays, mechanism/statistics, validation and biological or clinical significance.
- Social science: separate theory, hypotheses, variables, data collection, empirical model, robustness and implications.

## Default Presets

Use these presets unless the user explicitly chooses a different layout, format bundle or visual style.

```yaml
academic-method:
  purpose: Academic method framework
  trigger_hints: [paper, manuscript, review, method, experiment, publication figure, academic figure]
  outputs: [pptx, svg, json]
  layout: academic-method-framework
  style: academic-blue

thesis-proposal:
  purpose: Thesis/proposal technical route
  trigger_hints: [proposal, research plan, thesis, grant, topic application, opening report]
  outputs: [pptx, svg, drawio, json]
  layout: proposal-matrix-route
  style: presentation-clean

engineering-system:
  purpose: Engineering system route
  trigger_hints: [engineering system, energy system, control system, hardware system, platform design, architecture]
  outputs: [pptx, svg, drawio, html, json]
  layout: engineering-architecture-route
  style: dark-technical

workflow-pipeline:
  purpose: Workflow or tool pipeline
  trigger_hints: [software tool, agent skill, pipeline, workflow, automation, documentation]
  outputs: [svg, markdown, mermaid, json]
  layout: horizontal-stages
  style: minimal-gray

chinese-thesis-proposal:
  purpose: Chinese thesis/proposal poster route
  trigger_hints: [中文技术路线图, 开题报告, 课题申报, 论文技术路线, 研究方案, 毕设, 学位论文]
  outputs: [pptx, svg, drawio, html, json]
  layout: cn-proposal-poster-route
  style: cn-polished-pastel-academic

chinese-grant-application:
  purpose: Chinese grant or project application route
  trigger_hints: [基金申请, 项目申请, 申报书, 科研项目, 研究内容, 科学问题]
  outputs: [pptx, svg, drawio, html, markdown, json]
  layout: cn-grant-application-route
  style: cn-soft-grant-report

academic-paper-framework-cn:
  purpose: Chinese academic method framework
  trigger_hints: [中文论文方法框架, 研究框架图, 方法路线图, 论文图, 技术路线]
  outputs: [pptx, svg, drawio, json]
  layout: cn-research-method-matrix
  style: cn-blue-green-proposal

engineering-project-report-cn:
  purpose: Chinese engineering project report route
  trigger_hints: [工程项目, 项目汇报, 系统路线图, 能源系统, 平台建设]
  outputs: [pptx, svg, drawio, html, json]
  layout: cn-ppt-mainline-route
  style: research-ppt-blue
```

## Required Clarification

Ask one concise clarification question when:

- No source material or topic is available.
- The discipline, subfield, project type, research object, method family or evaluation metrics are missing and cannot be inferred from source evidence.
- The user requests a final figure but gives no target audience or use case and several presets fit equally well.
- The user asks for a specific output environment but the format is ambiguous.
- A requested format conflicts with editability or with available renderer support.
- The source evidence is too weak to decide whether a node is source-supported or inferred.

Do not ask repeated setup questions when reasonable defaults are available. Start from a draft route, expose assumptions, and let the user revise.

## Advanced Options

Show advanced choices only when the user asks to choose formats, style, layout, presets, or says advanced mode.

Advanced output formats:

1. `pptx` - editable in PowerPoint or WPS.
2. `svg` - editable in Figma, Illustrator or Inkscape.
3. `drawio` - editable in diagrams.net.
4. `drawio-code` - copyable Draw.io XML for diagrams.net / draw.io.
5. `excalidraw` - editable whiteboard-style scene.
6. `mermaid` - text-editable Markdown diagram.
7. `html` - interactive preview with node details.
8. `markdown` - project documentation page.
9. `json` - structured source file for re-rendering.

Advanced layout families:

1. `academic-method-framework`
2. `proposal-matrix-route`
3. `engineering-architecture-route`
4. `horizontal-stages`
5. `vertical-research-route`
6. `layered-architecture`
7. `timeline-swimlane`
8. `wide-collaboration-map`
9. `cn-proposal-poster-route`
10. `cn-grant-application-route`
11. `cn-research-method-matrix`
12. `cn-wide-project-map`
13. `cn-monochrome-linework-route`
14. `cn-ppt-mainline-route`
15. `cn-a4-stage-route`

Advanced visual styles:

1. `academic-blue`
2. `blue-green-research`
3. `monochrome-paper`
4. `presentation-clean`
5. `minimal-gray`
6. `nature-style-editorial`
7. `high-contrast-accessible`
8. `dark-technical`
9. `schematic-precision`
10. `premium-scientific`
11. `cn-polished-pastel-academic`
12. `cn-blue-green-proposal`
13. `cn-soft-grant-report`
14. `cn-reviewer-linework`
15. `cn-defense-poster`

## Workflow

1. Confirm the source scope: current repository, a specific directory, a document set, or pasted project notes. When local files are available, run `trm ingest <sources> --output-dir evidence-pack` to freeze their paths and SHA-256 hashes before extraction.
2. Inspect project evidence before diagramming:
   - README, docs, notebooks, papers, reports, briefs or notes.
   - PDF, LaTeX, manuscript text, method sections, supplements, proposal documents or task briefs.
   - Directory structure, manifests and config files.
   - Entrypoints, API routes, model/training/inference scripts, data-processing scripts and deployment files when they clarify the system.
   - Tests, examples and outputs when they clarify validation or deliverables.
3. Build a source-grounded foundation:
   - Problem, gap, objective, assumptions, audience and intended reader effect.
   - Discipline, subfield, project type, research object, method family, application area and evaluation metrics.
   - Ordered method/process steps and non-droppable core substeps.
   - Inputs, outputs, artifacts, variables, metrics, claims, evidence and risk items.
   - For papers: figure slot, reader question, caption burden and terminology/acronym integrity.
   - For engineering: system boundary, modules, data/energy/material flow, validation and deliverables.
4. Select the closest preset and output bundle using the default policy.
5. Extract a route model with this minimum logic:
   `problem or objective -> inputs/data -> methods/modules -> implementation/training/inference -> validation/evaluation -> outputs/applications`.
6. Create or update `tech-route.json` before rendering any user-facing format.
7. Run `trm validate tech-route.json --strict`. Treat incomplete domain context, unverified hashes, evidence gaps, inferred nodes and unresolved questions as final-render blockers.
8. Render selected editable formats. Use `--allow-draft` only when the user explicitly requests an unfinished working draft.
9. Report generated files, warnings, quality report findings and recommended manual review steps.

## Route Model

Use `references/route-schema.md` for the JSON schema. Keep every visible node traceable. A final diagram requires at least one hash-verified source evidence item for every visible node. Draft-only inferred nodes must set `is_inferred: true`, link to an assumption, remain separate from evidence coverage and block final rendering until resolved.

Use `references/paper-framework-integration.md` for paper-grounded and publication-figure rules, especially when the input is a manuscript, thesis, proposal, academic project, or method description.

Use `references/domain-profiles.md` to choose field-specific route grammar. Do not apply computer-vision, lab-experiment, engineering-system, biomedical or social-science semantics to each other unless the source explicitly combines them.

Use concise node labels:

- Prefer 3 to 9 words.
- Keep each stage to 2 to 6 nodes when possible.
- Use edge labels for semantic transitions such as `feeds`, `trains`, `validates`, `optimizes`, `deploys`, `supports`, or the user's language equivalent.
- Keep variables, temporary artifacts, scores, metrics, parameters and pass-through states on edges, tags or legends unless the source proves they are actual modules.
- Separate the semantic graph used for audit from the visual graph that will be rendered.
- Compress repeated actors, samples, panels, rows, arrows or equivalent flows unless each visible repetition adds source-grounded meaning.
- Keep edge labels in `tech-route.json`, HTML, Markdown and quality reports by default. Do not render them on the main diagram canvas unless the user explicitly enables `renderer_overrides.show_edge_labels`, because labels on connector lines often collide with arrows and node text.
- Keep node-to-node semantic edges out of the main diagram by default. Render a small number of straight stage-to-stage arrows instead. Only render node-level edges when the user explicitly enables `renderer_overrides.show_node_edges`.

## Output Formats

Read `references/output-options.md` before explaining format tradeoffs.

Editable constraints:

- PPTX: use native shapes, text boxes and connector lines; do not paste a screenshot as the main diagram.
- SVG: use editable text, rectangles, paths and lines; do not rasterize the diagram.
- Draw.io: use editable `mxCell` nodes and edges.
- Draw.io copy code: generate `tech-route.drawio-code.xml` as plain XML. Tell the user to open [diagrams.net / draw.io](https://app.diagrams.net/), create a blank diagram, use **Extras > Edit Diagram**, paste the XML, confirm, and then edit the shapes.
- Excalidraw: use editable scene elements.
- Mermaid: keep the `.mmd` source as text.
- HTML: keep interaction data in structured JSON or embedded object data.
- Markdown: include Mermaid source and evidence tables when useful.
- JSON: keep the route source complete enough to re-render.
- Quality report: include evidence coverage, inferred node count, unresolved questions and manual review suggestions.

## Layout And Style

Read `references/layout-patterns.md` before building `tech-route.json` for an unfamiliar layout.

Read `references/visual-styles.md` before setting a theme.

Read `references/local-style-study.md` when the target is a Chinese academic, thesis, grant, project-application, or research-report technical route diagram.

For proposal and research-report diagrams, prefer polished academic template language: white canvas, clear title, matrix or framework sections, low-saturation logical regions, dashed boundaries where they clarify grouping, and white editable node cards.

Use a left phase axis only when the user explicitly asks for a long vertical route. Do not use the vertical phase-axis layout as the default academic format.

For PPT-facing research and engineering diagrams, prefer `cn-ppt-mainline-route`: 16:9 canvas, five-stage horizontal mainline, enlarged stage/support text, 2 to 3 short support modules under each stage, and a bottom final-output bar.

For Word, thesis, or paper body diagrams that need a portrait figure, prefer `cn-a4-stage-route`: A4-style vertical canvas, no left phase axis, centered numbered stage headers, enlarged module text, 2 to 3 short modules per stage, and clear top-to-bottom arrows.

Use straight stage-to-stage connector arrows as the default. Avoid decorative curved arrows, elbow connectors, and dense auto-routed node connectors in formal academic and engineering technical-route diagrams unless the user explicitly requests them.

For engineering diagrams, separate system boundary, data or energy flow, service/module layers, validation and outputs. Do not force engineering routes into a thesis-proposal layout.

Never copy online template images into outputs. Convert public visual patterns into original editable shapes.

## Legacy / Experimental Use Cases

Campaign strategy routes, creative-production pipelines, customer-journey diagrams and media-channel swimlanes are legacy or experimental. Use them only when the user explicitly asks for campaign, advertising, marketing, conversion funnel, media planning or commercial launch diagrams.

Do not show campaign options in the default preset list. Do not use campaign examples in the main README gallery.

## Open Source References

Read `references/github-projects.md` when deciding what to reuse or cite. Use permissively licensed projects as dependencies or design references when helpful, but do not copy code from projects without a clear compatible license.

## Scripts

All scripts accept a route JSON file and write output files. They use Python standard library only unless clearly stated.

Common legacy commands:

```bash
python scripts/validate_route.py outputs/tech-route.json
python scripts/render_mermaid.py outputs/tech-route.json outputs/tech-route.mmd
python scripts/render_svg.py outputs/tech-route.json outputs/tech-route.svg
python scripts/render_drawio.py outputs/tech-route.json outputs/tech-route.drawio
python scripts/render_drawio_code.py outputs/tech-route.json outputs/tech-route.drawio-code.xml
python scripts/render_excalidraw.py outputs/tech-route.json outputs/tech-route.excalidraw
python scripts/render_html.py outputs/tech-route.json outputs/tech-route.html
python scripts/render_markdown.py outputs/tech-route.json outputs/TECH_ROUTE.md
python scripts/render_pptx.py outputs/tech-route.json outputs/tech-route.pptx
python scripts/render_all.py outputs/tech-route.json outputs --formats pptx,svg,drawio,drawio-code
```

CLI commands, when installed:

```bash
trm validate outputs/tech-route.json
trm validate outputs/tech-route.json --strict
trm render outputs/tech-route.json outputs --formats pptx,svg,drawio,drawio-code,html,markdown,json
trm render outputs/tech-route.json outputs --formats pptx,svg,json --allow-draft
trm ingest source-files --output-dir evidence-pack
trm init --preset academic-method --output tech-route.json
trm doctor
```

## Onboarding Demo

For a low-friction first run, use the academic demo:

```bash
python scripts/validate_route.py examples/academic-paper-demo/outputs/tech-route.json
python scripts/render_all.py examples/academic-paper-demo/outputs/tech-route.json examples/academic-paper-demo/outputs --formats pptx,svg,drawio,html,markdown,json
```

Read `examples/academic-paper-demo/demo-walkthrough.md` to see the simulated user request, route JSON, render commands and generated editable files.

For a Draw.io copy-code example, use:

```bash
python scripts/render_all.py examples/drawio-copy-code-demo/outputs/tech-route.json examples/drawio-copy-code-demo/outputs --formats drawio,drawio-code,svg,json
```

Then copy `examples/drawio-copy-code-demo/outputs/tech-route.drawio-code.xml` into [diagrams.net / draw.io](https://app.diagrams.net/) through **Extras > Edit Diagram**.

## Validation

Run validation before and after rendering. Treat errors as blockers and warnings as items to report.

Validation checks:

- Required route title and stages.
- `route_version` and `selected_preset`.
- `domain_context` exists and is complete enough for the requested final output.
- Unique stage and node IDs.
- Edge endpoints exist.
- Every visible node has hash-verified evidence; inference is reported separately and is allowed only in drafts.
- Every evidence locator names a declared source and is found in extractable source text when applicable.
- Final rendering has no unresolved questions or inferred nodes.
- Confidence values use `high`, `medium` or `low`.
- Node labels are not overloaded.
- Quality report warnings are visible to the user.

## Iteration

When the user asks to change colors, layout, labels, node count or output formats, update `tech-route.json` first and then re-render the selected files. Do not re-scan the whole project unless the user asks for content changes or the current route source is insufficient.
