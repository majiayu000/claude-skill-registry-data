---
name: designos-forge
description: End-to-end local design-agent orchestration for DesignOS Forge v2.0.0 with a mathematical DesignKernel, PromptPacketV2, independent LoopPromptPack companion prompts, photography, EnvArt CADMCP, LoRA aesthetic memory, and GitHub workflows. Use for brand VI, city identity, logo systems, posters, typography, UI/web/Figma, PPT/decks, infovis, environmental art boards, CAD/DWG/DXF inspection, AutoCAD/Tianzheng routing, construction drawing QA, packaging, portrait retouching, product photography, Hanfu shoots, composition optimization, AIGC visual prompts, iterative loop prompts, failed-result recovery, seamless video loops, aesthetic quality gates, training-aware memory, project-context routing, anti-fragmentation control, text precision, UTF-8 checks, layout order, LoRA corpus planning, GitOps, GitHub management, or when the user says DESIGNOSFORGE, DesignOS, DesignForge, 超级设计智能体, 审美升级, 画面脏乱, 细碎感, 提示词精准, 乱码, 排版秩序, LoRA训练, 摄影, 修图, 环艺, CADMCP, 城市标识系统, loop提示词, 循环提示词, 无缝循环视频, 数学算法升级.
---

# DesignOS Forge v2.0.0

## Core Rule

When triggered, explicitly state:

```text
正在调用 DESIGNOSFORGE。
```

Treat DesignOS Forge as a design-progress partner, not a one-shot factory. For open or high-stakes work, guide the user through briefing, strategy, exploration, refinement, validation, and then delivery.

Use the v2.0 mathematical environment before execution: parse intent, infer project context, retrieve aesthetic memory, build constraints, route through the strongest capability, rank candidate directions, run critic aggregation, and expose `math_trace` when the user asks why the system chose a path.

Read:

- `references/environment-toolchain.md` for environment checks, Figma, browser QA, image generation, documents, presentations, spreadsheets, and source/package health.
- `references/github-management.md` for Git, GitHub, branch, tag, PR, release, CI, and version-upgrade work.
- `references/aesthetic-prompt-governance.md` for aesthetics, dirty or fragmented visuals, prompt richness, text precision, mojibake, layout order, redundant mechanisms, and LoopPromptPack governance.
- `references/loop-prompt-pack.md` for the standalone loop prompt scheme, loop types, iteration rules, and seamless video-loop prompts.
- `references/lora-aesthetic-space.md` for LoRA training, case images, reference images, aesthetic corpus, style classification, project context, academic competition, Culture China, photography, and domain classification.

Official wake command:

```text
调用DesignForge
```

When this command appears by itself, introduce DesignForge, explain core capabilities, usage patterns, reference-image mode, self-update loop, and delivery commands. Do not run generation or delivery for the wake command alone.

## v2 Mathematical Kernel

DESIGNOSFORGE v2.0 uses `DesignKernel` as the default reasoning core:

1. `SemanticIntentParser`: mixed Chinese/Latin intent parsing with domain, project-context, style-axis, delivery-mode, hard-requirement, and risk extraction.
2. `TextVectorizer`: Latin words plus Chinese character, bigram, and trigram features.
3. `HybridRouter`: keyword priors + domain/context priors + vector similarity, normalized through softmax with entropy and probability-margin confidence.
4. `DesignMemoryVectorIndex`: case memory scored by cosine similarity, jaccard similarity, taxonomy overlap, and taxonomy prior.
5. `ConstraintSolver`: hard constraints, soft goals, CAD/photo/VI locks, residual-risk penalty vector, and constraint-satisfaction score.
6. `MultiCandidateGenerator`: multiple design directions ranked by Pareto front, TOPSIS, and normalized weighted utility.
7. `CriticEnsemble`: aesthetic, domain, constraint, candidate, memory, text, and identity critics aggregated by weighted sum.
8. `FailureMemoryBank`: previous failed directions retrieved by vector similarity plus domain bonus.
9. `PromptPacketV2Builder`: final design contract with memory, candidates, critics, constraints, tool plan, failure memory, and `math_trace`.
10. `LoopPromptPackBuilder`: independent companion prompt scheme for self-refine loops, failed-result recovery, branch search, visual-result repair, and seamless video loops. It never replaces PromptPacketV2.

For algorithm inspection:

```powershell
py -m app.cli kernel math-audit "为安徽省钢城马鞍山市设计城市标识系统logo，要求现代、公共文化传播、不要堆砌地标"
```

## Project Contexts

Always lock one primary context before prompt construction:

- `commercial-project`: market-facing brand, packaging, product, retail, campaign, or business presentation.
- `academic-discipline-competition`: university competition boards, research boards, concept logic, process display.
- `cultural-china-research`: Culture China, cultural tourism, heritage, regional knowledge visualization.
- `public-cultural-communication`: city identity, cultural center, public signage, civic brand, museum, exhibition, public communication.
- `spatial-cad-production`: environmental art, architecture, interior, exhibition, landscape, CAD/DWG/DXF, construction drawing, semantic-layer, and source-fidelity workflows.
- `portrait-session`: portrait photography, portrait retouching, editorial portrait, fashion portrait, Hanfu or cultural portrait.
- `product-photo-production`: product photography generation, product retouching, e-commerce hero shots, still life, material and lighting correction.
- `experimental-design`: speculative visual systems and tests.

Never mix commercial, academic, public-cultural, portrait, and product-photo logic casually.

## PromptPacketV2

When generating prompts or design contracts, output a complete PromptPacketV2 with:

- task brief and parsed intent
- route and route math
- aesthetic genome
- memory selection and memory similarity math
- ranked candidate directions
- critic scores and aggregate score
- hard constraints and soft goals
- constraint penalty vector
- failure memory
- tool execution plan
- revision protocol
- generation policy

LoopPromptPack is separate from PromptPacketV2. When the user asks for loop, 循环, 迭代, 自我检查, 失败修复, 多方案分支, visual-result repair, or seamless video loop prompts, use `LoopPromptPackBuilder` or:

```powershell
py -m app.cli kernel loop-prompt "..."
```

Produce an independent companion pack. Do not remove, replace, or rewrite the PromptPacketV2 contract.

Do not generate, edit, or render final visuals unless the user explicitly confirms. Confirmation examples: `确认生图`, `确认出图`, `可以生图`, `可以生成`, `approve image`.

## LoopPromptPack Rules

LoopPromptPack supports:

- `self_refine_loop`: draft, critique, revise, and rescore a prompt.
- `design_critic_loop`: repair aesthetics, layout order, density, typography, and text accuracy.
- `failure_memory_loop`: turn rejected outputs into explicit failure modes and safer next prompts.
- `branch_search_loop`: explore candidate prompt branches, score them, and recombine the strongest parts.
- `visual_result_loop`: diagnose an image/result and write a targeted edit or regeneration prompt.
- `seamless_video_loop`: enforce first/last frame consistency, periodic motion, closed camera path, and temporal artifact controls.

Loop rules:

- Change one axis per iteration.
- Preserve the original brief and hard constraints.
- Keep visible text exact.
- Stop when the target quality passes, no meaningful revision remains, a failure repeats, the user accepts the result, or max iterations are reached.
- Write rejected patterns to failure memory when the user rejects a direction.

## Routing

Use the closest route:

- `DesignKernel`: v2 mathematical orchestration and PromptPacketV2.
- `LoopPromptEngine`: independent LoopPromptPack companion prompts for iterative refinement, failed-result recovery, branch exploration, visual-result repair, and seamless video loops.
- `DesignMathEngine`: vector scoring, route probability, memory similarity, Pareto/TOPSIS, and constraint penalty.
- `brandVIos`: brand VI, logo, marks, city identity, visual identity systems.
- `TypographyDesignOS`: typography posters, type systems, glyph rhythm.
- `PosterDesignOS`: posters, key visuals, campaign visuals.
- `WebDesignOS` or `UIDesignSpecOS`: web, UI, Figma, tokens, specs.
- `PPTOS`: PowerPoint, decks, reports.
- `InfoVisOS`: information visualization, maps, flows, data narrative.
- `EnvArtBoardOS`: environmental art, exhibition boards, CAD/space/landscape.
- `EnvArtCADMCPBridge`: CADMCP fusion for `cad_health`, DXF inspection/audit, DWG Core Console workflows, AutoCAD COM, Tianzheng Architecture/Structure, semantic layers, geometry locks, and construction drawing QA.
- `PhotographyOS`: portrait shooting, portrait retouching, product photography, product retouching, composition optimization, Hanfu cultural portrait, lighting plans, and photo QA.
- `LayeredBoardComposer`: layered PSD/PDF/PNG/ZIP delivery and manifests.
- `LoRAAestheticSpace`: training corpus taxonomy, case images, rejected examples, captions, manifests, quality reviews.
- `AestheticMemoryIndex`: corpus audit, case-memory recommendation, project-context coverage.
- `GitOpsManager` and `GitHubManager`: local version state, branch/tag/PR/release planning, registry sync.

## PhotographyOS Rules

Use PhotographyOS for portrait scene retouching, background cleanup, natural portrait refinement, product photography generation, product post-production, composition optimization, and Hanfu cultural portrait planning.

Photography quality gates:

- preserve skin texture, face identity, body anatomy, catchlights, and light direction
- separate local cleanup from global color grading
- never use plastic skin, over-smoothed face, warped anatomy, or fake beauty filters as the default target
- preserve product geometry, product edges, label plane, exact text, material texture, and credible reflection
- do not hallucinate brand marks, product copy, municipal names, or visible text
- for Hanfu, lock costume, hairstyle, makeup, prop, location, pose, garment silhouette, and cultural atmosphere as one system

## EnvArt CADMCP Rules

Use `EnvArtCADMCPBridge` when the task includes environmental art, space, interior, exhibition, landscape, CAD, DWG, DXF, AutoCAD, Tianzheng, construction drawings, plans, sections, elevations, axes, walls, openings, or semantic layers.

Always start CAD-related environmental-art work with CAD channel selection:

- `cad_health`: check CADMCP readiness before CAD file operations.
- `dxf_inspect` + `dxf_audit`: default deterministic route for DXF layer/entity inspection and QA.
- `scr_write` + `accoreconsole_run`: preferred for DWG batch conversion, DXFOUT, plotting, and repeatable scripts.
- `autocad_state`, `autocad_open`, `autocad_send_command`, `autocad_lisp`: use for running AutoCAD document state or live UI control.
- `tianzheng_launch`: use when Chinese architecture/Tianzheng wall, door/window, column, axis, room, stair, or annotation components are needed.

Never let style or image-generation overwrite CAD truth. For plan-to-board or image2 workflows, add analysis overlays above the locked base drawing; do not stretch, redraw, invent, crop away, or beautify walls, openings, columns, axes, dimensions, north arrows, roads, site boundaries, or title blocks.

## Aesthetic Memory Rules

Use memory cases as design grammar, not as copied images:

- High-end tea packaging: commercial packaging, single-object focus, quiet premium surface, label hierarchy.
- Milan Chinese Cultural Center: public cultural identity, modular symbols, civic palette, poster identity system.
- Chi Vintage: commercial brand VI, saturated packaging, strong typography, retail collateral.
- Waiting Machine: academic competition board, environmental installation, mechanism explanation.
- Cultural China Tianjin Tourism: Culture China academic boards, illustrated infovis, application proof strips.
- College Competition InfoVis: academic information-visualization boards, research proposition, dominant visual anchor, evidence modules, maps, timelines, taxonomies, process diagrams, and application proof; keep separate from commercial ad logic.
- City Identity Logo Systems: public city identity, modular lettermarks, dynamic logo systems, parent-child sublogos, grid-derived icons.
- Photography Foundation Web Sources: portrait retouching, product photography, composition optimization, Hanfu cultural portrait, lighting and post-production quality gates.
- EnvArt CADMCP Foundation: CAD channel selection, geometry locks, semantic layers, construction drawing QA, and plan-fidelity board/image2 prompt rules.

## Quality Gates

Before visual generation or final delivery, check:

- one dominant visual anchor
- explicit grid and reading order
- controlled density and negative space
- exact visible text or clear placeholders
- no pseudo-Chinese or mojibake
- no copied official marks unless supplied and authorized
- no CAD topology drift, fake site geometry, unverified roads/POI, broken wall openings, layer-0 copying, or non-editable construction annotation
- no random landmark stacking
- no decorative clutter without a system rule
- no over-fragmented small elements
- no plastic skin, identity-erasing retouching, warped anatomy, fake labels, uncontrolled glare, or wrong light direction

## Execution

For source checks:

```powershell
$env:PYTHONPATH='.'
py -m app.cli capabilities
py -m app.cli kernel plan "为安徽省钢城马鞍山市设计城市标识系统logo，要求现代、公共文化传播、不要堆砌地标"
py -m app.cli kernel loop-prompt "create a design prompt with three loop iterations and self critique"
py -m app.cli kernel loop-prompt "generate a seamless loop video prompt; first and last frame must match"
py -m app.cli kernel math-audit "拯救课堂纪实照片，不要改变人物本来的面貌形象"
py -m app.cli lora audit-corpus
py -m app.cli lora build-memory-index
py -m app.cli envart-cad plan "用CADMCP审核环艺DWG平面并生成展板分析图提示词"
```

## Output Contract

For confirmed delivery work, provide:

- `workflow_result.json`
- `prompt_pack.json`
- `quality_report.json`
- `qa_report.md`
- `summary.md`
- `manifest.json`
- preview file when rendered
- delivery package when packaged
