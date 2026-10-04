---
name: research-paper-figure-skill-factory
license: MIT-0
description: "Use when the user wants a research-paper figure Skill Factory: build, patch, package, or use reusable specialized paper-figure-making skills from lawful literature/corpus evidence. Generated skills must use a specialized-skill-first workflow, full-feasible local PDF coverage where available, startup-plan-only first replies, target-paper candidate/final image isolation, mandatory image-embedded visual-structure explanation, mandatory non-target concept/modeling example display for abstract visual decisions, saved subtype/style illustration atlases, ChatGPT web Create image / ChatGPT Images 2.0 rendering, Codex $imagegen-first rendering, sample-image transfer rules, all-step/current-position state footers, and a mandatory first-round diverse candidate board followed by P6b/P6c paper-local best-practice optimization before final prompt construction."
metadata:
  display_name: Research Paper Figure Skill Factory
  version: "2.0.5"
  author: OpenAI
  tags: research-figure, paper-figure, figure-skill-builder, figure-skill-factory, scientific-illustration, figure-taxonomy, meta-skill, image-prompt, imagegen, chatgpt-images-2, clawhub, openclaw, visual-style, figure-studio
  compatibility: ChatGPT web, Codex, OpenClaw, ClawHub marketplace. Requires image-generation capability for rendering.
  openclaw:
    skillKey: research-paper-figure-skill-factory
---

# Research Paper Figure Skill Factory

This skill is a two-layer research-paper figure Skill Factory.

1. **Skill Builder layer:** build or patch a reusable specialized figure-making skill for one paper-figure class by acquiring lawful source material, extracting figure evidence, building a taxonomy, generating the skill package, testing it, and locking it.
2. **Figure Production layer:** after a specialized skill is locked, use that generated skill to design, compare, render, review, and integrate concrete figures for arbitrary target papers of the same figure class.

Version 2.0.5 adds a stricter visual-structure-as-image gate for generated specialized skills. When a generated skill explains or defines visual structure, layout skeleton, panel choreography, module topology, arrow grammar, candidate-board structure, second-round optimization geometry, or final content architecture in a text turn, it must show that structure with an embedded saved reference image or non-target concept/modeling example image. It must not substitute a prose-only or bullet-only visual-structure description. The existing hard gates remain: abstract visual decisions require inline reference/concept images, and after P6 selects the strongest first-round direction, P6b/P6b-IMAGE/P6c must run a paper-local best-practice optimization round before P7 final prompt construction. Target-paper candidate images, draft figures, final figures, and revisions still remain isolated in dedicated `IMAGE_ONLY` turns.

## Non-Negotiable Contract

### First Trigger

On first trigger, output only a startup plan. Do not analyze a paper, build a taxonomy, create candidate schemes, draft prompts, or generate images. The first reply is `STARTUP_PLAN_ONLY (TEXT_ONLY)`.

If the first user message asks for images, record the request as pending only. The first reply must not call Create image, `$imagegen`, an image API, or include image artifacts.

### Specialized-Skill-First Builder Rule

The normal route is:

`figure-class goal -> corpus plan -> lawful acquisition/local corpus -> evidence extraction -> taxonomy -> specialized skill blueprint -> generated specialized skill -> tests/patches -> locked skill -> target-paper production`.

Do not jump from source papers directly to one concrete figure unless the user explicitly chooses a full production fast-track. If fast-tracking, record the skipped builder steps and fallback skill/taxonomy.

### Full-Feasible Corpus Rule

When local PDFs, a paper index, or retrieval manifests exist, enumerate the full relevant candidate set and process as many accessible relevant PDFs as feasible. A small sample can support only a limited/pilot/fallback lock unless the user explicitly accepts that limitation. Representative rendered pages are audit aids only, not the corpus size.

### Mandatory Candidate-Image Bridge

Every generated specialized figure-making skill must include a hard workflow bridge after any multi-option text decision:

1. `TEXT_ONLY` candidate text turn: present 4-6 text candidates, normally 6.
2. `TEXT_ONLY` visual candidate setup turn: define candidate count, varied axis, fixed elements, rendering route, and what the user should compare.
3. `IMAGE_ONLY` candidate-board turn: generate/display 4-6 candidate images or schematic candidates, normally 6.
4. `TEXT_ONLY` candidate-review turn: record the previous image batch, compare candidates, recommend one direction, and ask the user to select, revise, or request another board.

This bridge is mandatory after candidate schemes, subtype choices, layout choices, style choices, metaphor choices, density choices, and prompt alternatives. The generated skill must not move directly from 4-6 text candidates to final prompt construction, final image generation, caption writing, or text-only locking unless the user explicitly says to skip image candidates and stay text-only. If skipped, record `visual_candidate_board_skipped_by_user: true`.

Generated skill lock/test must fail if:

- the workflow lacks a dedicated visual candidate setup step;
- the workflow lacks a dedicated `IMAGE_ONLY` candidate-board step before direction lock;
- examples show text candidates followed directly by final prompt or final image generation;
- the state footer cannot record `visual_candidate_board_status`, `candidate_image_batch_id`, and `selected_visual_candidate`;
- multi-option next prompts do not ask the user to generate/display multiple candidate images or schematic candidates, normally 6.

### Target-Paper Image Isolation And Required Inline Reference Display

Every response must distinguish target-paper figure production from explanatory reference display:

- `TEXT_ONLY`: planning, intake, diagnosis, candidate text, candidate-board setup, prompt writing, critique, status, next prompts, and inline display of allowed reference images.
- `IMAGE_ONLY`: target-paper candidate-board generation, draft/formal figure generation, final figure generation, and target-paper revision image generation only. No prose, captions, critique, prompt text, or state footer.

Allowed reference images inside a `TEXT_ONLY` reply:

- already-saved package-local subtype/style atlas or reference images;
- non-target concept diagrams used to explain an abstract visual grammar, workflow, taxonomy axis, or modeling pattern;
- non-target example images created while building or demonstrating the specialized skill itself, as long as they do not represent the user's target paper, are not offered as selectable candidates, and are not treated as draft/final paper figures.

Required abstract-decision trigger:

- If a `TEXT_ONLY` step explains or compares figure subtype, layout grammar, visual style, density, metaphor, modeling pattern, candidate scheme differences, or final content architecture, the generated skill must display at least one relevant saved atlas/reference image or non-target `concept_example` / `non_target_reference` image with Markdown image syntax.
- This applies especially to P2, P3, P4, P6b, and P7; it also applies to P1, P6, or P9 when those steps contain abstract visual comparison or final content-architecture reasoning.
- Pure state synchronization, caption/body text drafting, simple confirmation, and ordinary restatement of an already registered image batch do not require a new concept/example image.
- If no suitable saved reference exists and live inline generation is unavailable, record `concept_example_required: true`, `concept_example_status: generation_pending` or `missing_recorded`, `concept_example_role`, and `concept_example_trigger_reason`, then make the repair action explicit.

Required visual-structure-as-image trigger:

- If a `TEXT_ONLY` step explains, compares, or defines visual structure, layout skeleton, panel choreography, module topology, arrow grammar, content architecture, candidate-board structure, second-round optimization geometry, or final image-brief structure, the generated skill must display a structure image with Markdown image syntax in that same text reply when technically possible.
- The displayed image must be an already-saved atlas/reference image or a non-target `concept_example` / `non_target_reference` generated for explanation. It may use generic placeholders, but it must not contain the user's target-paper-specific modules, claims, data, or final labels unless the user explicitly supplied them as detached generic examples.
- Do not use prose, tables, bullets, ASCII diagrams, Mermaid, SVG, or code-rendered sketches as the only representation of a visual structure. Text may name the structure role, fixed elements, and varied axes, but the structural form itself must be shown as an embedded image.
- If the only useful structure preview would be paper-specific, defer that preview to the next target-paper `IMAGE_ONLY` step (`P5`, `P6b-IMAGE`, or `P8`) and embed only a generic structure/reference image in the text reply. Do not embed paper-specific candidate, second-round, formal, final, or revision images in prose.
- State must record `visual_structure_image_required`, `visual_structure_image_status`, `visual_structure_image_role`, and `visual_structure_image_trigger_reason` in addition to the `concept_example_*` fields. Missing status is temporary only; production lock fails until an available saved reference or generated non-target structure image is embedded or a host-rendering block is explicitly recorded with repair action.

Target-paper images must not be embedded in text replies. If an image is meant for choosing or locking a visual direction for the target paper, refining a paper-specific figure, or producing a formal/final paper figure, the generated skill must use the P5/P8-style `IMAGE_ONLY` boundary. A concept/example image embedded in text must be labeled in state as `non_target_reference`, must not set or reuse `candidate_image_batch_id`, and must not be used as evidence that the candidate-image bridge has been satisfied.

If the host cannot generate and embed a non-target concept/example image in the same text response, generate/save it first and embed it in a later `TEXT_ONLY` reply. Do not relax the `IMAGE_ONLY` boundary for target-paper candidate or final outputs.

### Mandatory Best-Practice Divergence After P6

The first target-paper candidate-board round should be deliberately diverse. P4/P5 should vary high-level direction-setting axes such as subtype, layout grammar, metaphor, density, panel rhythm, or style family so the user can choose a promising direction.

P6 records the first-round `candidate_image_batch_id`, compares candidates, and selects the strongest current direction. P6 is not allowed to jump directly to P7. After P6, generated skills must run a paper-local best-practice optimization round:

1. `P6b` `TEXT_ONLY`: propose 4-6 optimization axes, normally 6, based on best practices and the selected paper-local details: local module relationships, evidence/case anchors, label economy, panel transitions, color semantics, callout placement, and reviewer-facing readability. State exactly which elements stay fixed from the first-round winner and which local details vary.
2. `P6b-IMAGE` `IMAGE_ONLY`: generate/display 4-6 second-round target-paper variant images, normally 6. This uses a new `second_round_candidate_batch_id`; it must not reuse `candidate_image_batch_id` or any concept/example image id.
3. `P6c` `TEXT_ONLY`: record the second-round batch, compare variants, select or combine the final direction, and only then allow P7 final image brief construction.

Generated skill lock/test must fail if P6 selects a first-round image and then enters P7/P8 without completing this second-round gate. If the user explicitly rejects the second round, the skill may record the override as a nonstandard limitation, but default production examples and production-grade lock must still require P6b/P6c.

### Off-Recommended-Prompt State Mapping

Generated specialized skills must not depend on the user using the recommended next prompt verbatim. For every user request, including free-form requests, shortcuts such as "继续/出图/改成更简洁", partial asks, or requests that jump ahead, do this before ending the text reply:

1. Interpret the user's actual action request.
2. Decide whether it is valid, missing required inputs, unsafe, or conflicts with the target-paper image isolation and inline-reference contract.
3. If valid, execute as much as the current modality allows.
4. Map the completed or deferred work to the closest original workflow step (`S0`, `B1-B9`, `P1-P6`, `P6b`, `P6b-IMAGE`, `P6c`, or `P7-P9`).
5. Update the state footer with the step before the user request, the step after handling it, the reason for the transition, and any pending bridge or image-only action.

This mapping is mandatory even when the user asks for a task out of order. Do not restart the workflow, ignore state, or answer without assigning a current position. If the request jumps ahead, record prerequisites that were inferred, satisfied, missing, or deliberately skipped by the user. If the request asks for target-paper candidate/final/revision image generation in a text turn, stop at the closest `TEXT_ONLY` setup/confirmation step and make the next recommended action the required `IMAGE_ONLY` step.

### Rendering Route

For target-paper candidate boards, draft candidates, final diagrams, and revisions:

1. ChatGPT web must use **Create image** through **ChatGPT Images 2.0**.
2. Codex must use the `$imagegen` skill first.
3. If `$imagegen` is unavailable in Codex, use ChatGPT Images 2.0 API or another approved image-generation API.
4. Native bitmap outputs such as PNG, JPG, JPEG, and WebP are allowed when produced by the approved image route.
5. Do not use SVG, Mermaid, TikZ, Graphviz, HTML/CSS, canvas, matplotlib, filesystem code drawing, or code-rendered/exported figures as target-paper candidate images, draft images, final visuals, or fallbacks.

For non-target concept diagrams, visual-structure examples, or skill-modeling example images embedded in text, use the same approved image route when live generation is needed. These images are explanatory references only and must not contain target-paper-specific claims, data, module names, or final labels unless the user explicitly supplied them as generic examples detached from the target paper.

### Reference Images

Generated specialized skills must support optional sample/reference images. If the user provides multiple images, ask which attributes to borrow from each image: style, layout, panel rhythm, density, content-detail level, labels, color semantics, callout grammar, or negative-reference constraints.

### Subtype Illustration Atlas

Every generated specialized figure-making skill must include a saved subtype/style illustration atlas. The atlas is built during the Skill Builder layer, saved inside the generated skill package, and reused by the generated skill when helping users choose figure subtype, layout, visual grammar, density, or visual communication art style.

The atlas must cover these classification angles at minimum: reader question, narrative role, logical gap, visual rhetoric, visual grammar/layout, paper slot, density/detail level, and visual communication art style. For each supported subtype under each angle, create at least one representative illustration or thumbnail. Prefer labeled composite boards; when there are many subtypes, create hierarchical boards such as one overview board plus per-angle boards. Every board must visibly label subtype names.

The generated skill package must save the atlas under this package-local structure:

```text
assets/subtype-atlas/manifest.json
assets/subtype-atlas/boards/
assets/subtype-atlas/thumbnails/
references/subtype-illustration-atlas.md
```

`manifest.json` must record classification angle, subtype, package-relative image path, generation route, build time or build id, intended use, transferable visual attributes, and limitations for each asset.

Builder-time atlas generation uses the approved rendering route: ChatGPT web uses **Create image** through **ChatGPT Images 2.0**; Codex uses `$imagegen` first; if `$imagegen` is unavailable, use ChatGPT Images 2.0 API or another approved image-generation API.

Generated specialized skills must show all available subtype atlas boards on their first/startup reply when the boards already exist. The first reply remains startup-only: no target-paper analysis and no target-paper image generation. Later `TEXT_ONLY` replies that discuss subtype, layout, visual grammar, density, or visual communication art style must display the relevant saved atlas board or thumbnail when available. If a relevant atlas asset is missing, record the missing asset and suggest generating or repairing the atlas.

Display means an actual Markdown image embed, not a plain file list. A valid text reply contains lines like `![Subtype atlas](<renderable path to package-local board>)`. In Codex, resolve `assets/...` against the active skill root and emit an absolute filesystem path, preferably with forward slashes, for example `![Subtype atlas](C:/Users/<user>/.codex/skills/<skill-name>/assets/subtype-atlas/boards/subtype-overview.png)`. In ChatGPT web with Sources, display the saved source asset or use package-relative Markdown such as `![Subtype atlas](assets/subtype-atlas/boards/subtype-overview.png)` when the host can render it. If the host blocks rendering, record `reference_display_render_status: attempted_host_blocked` and list the exact asset paths; do not silently omit the atlas.

After B6 creates/saves atlas boards, the next factory `TEXT_ONLY` builder reply must display the newly saved atlas boards with Markdown image embeds and record `subtype_atlas_status: displayed`. This does not apply to the factory's first trigger, because no generated specialized-skill atlas exists yet.

### Every Text Reply

Every `TEXT_ONLY` reply from this factory and from generated specialized skills must include:

- `当前执行计划`
- substantive work for the current step
- `默认推荐`
- `当前状态与产物`
- `下一步你可以这样问`

The state footer must list all steps plus the current position and the response mode of every step. The first copyable next prompt must use:

`请使用**<当前skill名称>**，执行，根据当前状态，下一步执行：...`

Always include:

`请使用**<当前skill名称>**，根据当前状态，提供下一步提问建议。`

Every text footer must also include `user_request_interpreted_action`, `workflow_step_before_user_request`, `workflow_step_after_user_request`, `state_transition_reason`, and `off_recommended_prompt_handling`. These fields are required even when the user followed the recommended prompt; in that case record `off_recommended_prompt_handling: not_needed`.

## Skill Builder Workflow

| Step | Layer | Mode | Purpose | Output |
|---|---|---|---|---|
| S0 | Startup | STARTUP_PLAN_ONLY (TEXT_ONLY) | Show the complete two-layer plan only | Startup plan |
| B1 | Skill Builder | TEXT_ONLY | Define target figure class and generated skill goal | Figure-class brief |
| B2 | Skill Builder | TEXT_ONLY | Define corpus scope, venues, keywords, and lawful acquisition route | Corpus plan |
| B3 | Skill Builder | TEXT_ONLY | Acquire or organize open/user-authorized PDFs and manifests | Local corpus + retrieval manifest |
| B4 | Skill Builder | TEXT_ONLY | Extract paper cards, captions, figure inventory, labels, and visual observations | Evidence artifacts |
| B5 | Skill Builder | TEXT_ONLY | Build evidence-backed figure-class taxonomy and define subtype/style atlas coverage | Taxonomy + atlas coverage plan |
| B6 | Skill Builder | TEXT_ONLY | Generate and save subtype/style atlas, display saved boards with Markdown image embeds, then convert taxonomy into specialized skill blueprint | Atlas package + displayed board embeds + blueprint |
| B7 | Skill Builder | TEXT_ONLY | Generate specialized skill package and verify startup/style examples contain Markdown atlas embeds | Skill folder/package |
| B8 | Skill Builder | TEXT_ONLY | Test and patch startup, state, candidate-board, rendering, prompt behavior, and atlas renderability | Test report + patches |
| B9 | Skill Builder | TEXT_ONLY | Lock generated skill for reusable production | Locked skill with version/scope |

## Required Generated Figure-Production Workflow

Every generated specialized figure-making skill must use this expanded production workflow, or a stricter equivalent with the same mandatory candidate-image bridge:

| Step | Mode | Purpose | Output |
|---|---|---|---|
| P1 | TEXT_ONLY | Startup/intake target-paper material, target slot, constraints, optional sample images, and display saved subtype atlas with Markdown image embeds if available | Startup/material status + rendered atlas display |
| P2 | TEXT_ONLY | Diagnose figure need, multi-label subtype routing, and display relevant subtype/layout atlas boards with Markdown image embeds | Subtype candidates + rendered atlas references + default route |
| P3 | TEXT_ONLY | Define reader effect and produce 4-6 text candidate schemes, normally 6; display relevant saved style/layout boards with Markdown image embeds if style or layout is discussed | Text candidates + rendered saved reference boards + required visual-candidate next action |
| P4 | TEXT_ONLY | Set up visual candidate board: candidate count, varied axis, fixed content, route, comparison criteria, and an embedded generic structure/reference image instead of prose-only structure description | Candidate-board brief + structure image embed |
| P5 | IMAGE_ONLY | Generate/display 4-6 first-round candidate images or schematic candidates, normally 6, maximizing direction-level diversity | Diverse first-round image candidates only |
| P6 | TEXT_ONLY | Record the first-round image batch, compare candidates, and select the strongest current direction; do not enter final prompt yet | First-round selected direction + required P6b next action |
| P6b | TEXT_ONLY | From paper-figure best practices, define 4-6 paper-local optimization axes, normally 6; state fixed elements from the first-round winner and local details to vary; embed a generic structure/reference image for the optimization geometry | Paper-local second-round optimization setup + structure image embed |
| P6b-IMAGE | IMAGE_ONLY | Generate/display 4-6 second-round target-paper variants, normally 6 | Second-round variant images only |
| P6c | TEXT_ONLY | Record the second-round image batch, compare variants, and lock the final visual direction | Final selected visual direction |
| P7 | TEXT_ONLY | Build final image brief/prompt for the selected direction after P6c, referring to the selected visual batch and embedding only non-target structure/reference images when architecture needs explanation | Final image brief |
| P8 | IMAGE_ONLY | Generate formal figure candidate or revision batch through the approved image route | Formal image candidates only |
| P9 | TEXT_ONLY | Review, refine, caption, legend, body insertion, and handoff text | Final paper text package |

Rules for this workflow:

- P3 must not ask the user to choose only from text as the primary route. Its first recommended next prompt must be to generate/display 6 candidate images or schematic candidates.
- P4 is required before P5 unless the immediately preceding user message already confirms the board count, varied axis, fixed elements, and rendering route. The P4/P5 first round should maximize visual diversity to establish direction.
- P4, P6b, and P7 must not describe visual structure with text alone. If they discuss layout skeleton, panel choreography, module topology, arrow grammar, or content architecture, they must embed a saved reference or non-target structure/concept image in the text reply.
- P5 is not a final figure stage. It is a direction-setting visual selection stage.
- P6 must happen after P5 and must record the first-round image batch before any final prompt or caption work.
- P6 cannot move directly to P7 after selecting the current best candidate. It must trigger `P6b` best-practice divergence.
- P6b must normally propose 6 paper-local optimization axes and record `best_practice_divergence_status` and `best_practice_divergence_axes`.
- `P6b-IMAGE` must use a new `second_round_candidate_batch_id` and cannot reuse a concept/example id or first-round batch id.
- P7/P8 may only occur after `P6c` records the second-round batch and locks `selected_second_round_candidate`, or after an explicit user override recorded as a limitation.
- Any generated skill may add more domain-specific steps, but it must not remove P4/P5/P6 or collapse them into a mixed text+image response.
- If the user requests a valid action out of recommended order, the generated skill may handle it only after mapping it to the closest workflow step and preserving the required modality boundary. Examples: a request to "直接出图" before P4 maps to P4 setup in a text reply and P5 as the next `IMAGE_ONLY` action; a request to "改成更简洁" after candidates maps to P6/P7 depending on whether an image batch has been reviewed; a request for caption before final visual lock maps to P9 pending prerequisites.

## Generated Skill Package Requirements

Generated specialized skills must include the candidate-image bridge in:

- `SKILL.md`
- `metadata.json`
- `agents/openai.yaml`
- `references/workflow-and-state-contract.md`
- `references/visual-style-and-board-protocol.md`
- `references/subtype-illustration-atlas.md`
- `references/prompt-generation-policy.md`
- `assets/subtype-atlas/manifest.json`
- `assets/subtype-atlas/boards/`
- `assets/subtype-atlas/thumbnails/`
- `templates/state-footer-template.md`
- `templates/figure-brief-template.md`
- `templates/prompt-template.md`
- examples, especially startup, text-candidate, visual-board setup, image-only board, candidate-review, required inline non-target concept/example reference display, visual-structure-as-image display, P6b best-practice divergence setup, P6b-IMAGE second-round variants, P6c second-round selection, and final prompt examples
- release checklist and starter prompts

Startup and style/layout examples must include real Markdown image embed syntax for saved atlas boards. Abstract-decision and visual-structure examples must include real Markdown image embeds for saved reference images or non-target explanatory structure images, or explicitly record the missing concept/example asset and the generation/repair action. A plain bullet list of paths is not a display example when an image is meant to be shown.

The release checklist must fail production lock when a generated skill lacks a saved subtype/style atlas, fails to display available atlas boards on first startup, omits Markdown image embeds for available atlas boards, discusses subtype/layout/style/density/metaphor/modeling/candidate differences/final content architecture in text without displaying available saved reference or non-target concept/example images or recording why they are missing plus the repair action, describes visual structure/layout skeleton/panel choreography/module topology/arrow grammar/content architecture with prose or bullets only, embeds target-paper candidate/final images in a text reply, treats non-target concept/example images as candidate boards, moves from P6 first-round selection directly to P7/P8 without P6b/P6c, or handles a non-recommended user request without mapping the result back to the original workflow step/state.

The release checklist must include a failing test for the exact bug this patch fixes: “after 4-6 text candidates or layout/style-axis setup, the generated skill still has no separate candidate-image generation step.”

## Reference Loading Order

Load references as needed:

1. `references/master-workflow.md`
2. `references/generated-specialized-skill-output-spec.md`
3. `references/generated-skill-multi-candidate-policy.md`
4. `references/visual-first-decision-board-protocol.md`
5. `references/startup-plan-step-output-map.md`
6. `references/planning-state-and-navigation-contract.md`
7. `references/prompt-generation-and-rendering-policy.md`
8. `references/strict-text-image-turn-separation-policy.md`
9. `references/subtype-illustration-atlas-policy.md`
10. `templates/subtype_atlas_manifest_template.json`
11. `templates/specialized_skill_blueprint_template.md`
12. `templates/state_footer_template.md`

## Version Note

Version 2.0.5 requires generated skills to show visual structure as embedded images inside text turns instead of describing structure only in words. It also keeps the existing requirements: non-target concept/example image display for abstract visual decision text turns and a P6b/P6c paper-local best-practice optimization round after the diverse first-round P6 candidate selection. Generated skills must still handle free-form user requests by executing valid work, mapping the outcome to the closest original workflow step, and updating state fields in every text reply. Saved atlas Markdown display, target-paper image isolation, and the candidate-image bridge remain mandatory.
