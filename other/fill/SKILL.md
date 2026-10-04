---
name: fill
description: >-
  Guide content filling for scaffolded products. Walks sections, asks domain questions,
  writes expertise into files. Use after /create in 'scaffold' state, or when the creator
  says 'fill', 'add content', or 'help me complete this'.
argument-hint: "[product-slug] [--express]"
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - AskUserQuestion
---

# Content Filler

Extract domain expertise from creator conversation and inject into product files.

**When to use:** After /create has generated a scaffold. Product state should be "scaffold" or "content".

**When NOT to use:** If the product doesn't exist yet (use /create first). If the product is already validated (edits will regress state).

> Full protocol details (section walker, sparring, extraction modes, type-specific coaching, research injection, progress tracking, completion flow) are in:
> `${CLAUDE_SKILL_DIR}/references/fill-protocol.md` — Read this file before executing the section walk.

---

## Activation Protocol

0. **Shared preamble:** Load `references/quality/activation-preamble.md` — context assembly, persona adaptation, deterministic routing rules.
1. Identify target product:
   - If `$ARGUMENTS` provided, use as product slug → look in `workspace/{slug}/`
   - If `workspace/{slug}/` does not exist → "Product `{slug}` not found in workspace/. Run `/create` first or check `workspace/` for available slugs."
   - If not, glob `workspace/*/` and list products in scaffold/content state
   - If no products in scaffold/content state found → "No products ready to fill. Run `/create {type}` to scaffold one first."
   - If multiple products found, ask which one to fill
1b. **Mode selection (Express vs Guided).** Read `creator.yaml → preferences.workflow_style`. Resolve the flow mode:
    - `--express` flag OR `workflow_style == "autonomous"` → **Express mode**. Skip the three Discovery front-loaded questions, skip the Pitfall Check interactive prompt, skip Extraction Mode menu (default to Standard), skip the Deepening menu after each section, run the section walker with type defaults, and fall straight through to Completion. Interactive prompts are replaced by type-based defaults + one-line advisory notes. Proactive brainstorm prompts are suppressed.
    - `workflow_style == "guided"` or missing → **Guided mode** (default). Run the full protocol as documented in fill-protocol.md.
    Record `fill_config.mode: express | guided` in `.meta.yaml` so later skills can reason about the creator's chosen rhythm.
2. Read `.meta.yaml` from product directory → get type, state, mcs_target, AND the `intent_declaration` block if present.
   - **Intent-aware calibration:** If `intent_declaration` is present, extract `engine_parsed.{depth, nature, delivery_mechanism}`. These three fields drive section walker routing, tone calibration, and question shape — see `fill-protocol.md → INTENT-AWARE CALIBRATION` for the full rubric. Record `fill_config.intent_aware: true` in `.meta.yaml` when the calibration fires.
   - **Legacy fallback:** If `intent_declaration` is absent (legacy product) OR if `intent_declaration.mode == legacy_fallback` with all engine_parsed fields null, fall back to type-based defaults. Emit one advisory line: *"This product lacks intent metadata — /fill will use type-based defaults. Re-run /create to unlock intent-aware filling."* Record `fill_config.intent_aware: false`.
3. **Maintain creator persona**: Read `creator.yaml` → adapt language, depth, and examples to `profile.type` and `technical_level` throughout this skill's execution. A developer gets code examples; a domain expert gets plain language.
4. **Load UX stack (in order)**:
   - `references/quality/engine-voice-core.md` — the micro voice contract carried through every question, section signal, and sparring line in /fill. This is where the Creator spends the most time; the voice cannot drift.
   - `references/ux-experience-system.md` §1 Context Assembly (build creator context), §2.2 Archetype-Aware Insights (adapt emphasis to creator goals), §2.3 Moment Awareness (mid-fill coaching)
   - `references/ux-vocabulary.md` — translate terms in any creator-facing output
   **Vocabulary enforcement (mandatory):** Every question, section signal, sparring challenge, and progress message passes through ux-vocabulary.md translation before reaching the creator. Internal terms (Sparring, Pitfall, MCS, DNA tier, extraction mode) are replaced for non-dev creators. For dev/hybrid creators, terms may appear but always with context ("MCS-2 quality checks — these verify craft and expertise depth").
   - `references/quality/engine-voice.md` — full voice substrate. Load when composing section quality signals, sparring pressure, milestone celebrations, or brand moments.
   - `references/quality/exemplar-outputs.md` sections E4 and E5 only — the section question and sparring exemplars. These show the exact visual rhythm and warmth your questions must carry: progress sandwich (bar → celebration → question → escape hatch), warm framing, 💡 scaffolding offers.
   - `references/ux-experience-system.md` §11 Deep Elicitation Protocol — MANDATORY for all AskUserQuestion calls. Apply: experience-based questions (not abstractions), one question at a time, mirror to confirm, escalate progressively, offer scaffolding when stuck, celebrate depth.
   /fill is where the creator spends the MOST time. The experience must be warm coaching, not interrogation. Adapt: beginners get encouragement + examples. Experts get peer-level sparring. Celebrate section completions with progress visibility ("4/7 sections filled. Core identity locked in."). Hyper-personalize using creator.yaml fields — name, goals, expertise areas.
4b. **Load proactives:** Load `references/engine-proactive.md` — wire #1 (pipeline guidance: after fill completes, guide to /validate), #17 (lost creator: if stuck on a section for 3+ questions, offer /think or skip), #19 (error recovery: if fill encounters malformed scaffold, suggest re-scaffolding).
5. Load product spec from `references/product-specs/{type}-spec.md`
6. Load product DNA from `product-dna/{type}.yaml`
6b. **Load entity ontology (squad/system/agent/workflow/minds):** If type ∈ {squad, system, agent, minds, workflow}, read `references/entity-ontology.md`. This substrate drives semantic elicitation:
    - §AGENT_ROLES: suggest specific roles during composition discovery, adapt questions per role (EXECUTOR gets tool/output questions, ADVISOR gets reasoning questions, VALIDATOR gets criteria questions)
    - §SQUAD_ANATOMY: verify all 8 components are addressed during fill — flag any missing component before completion
    - §COMPOSITION: know what this type can compose with and what's forbidden — guide toward valid compositions
    - §HERITAGE: explain to the creator why certain DNA patterns apply (squad inherits from agent lineage)
    - §INTELLIGENCE_GRADIENT: calibrate autonomy level in routing questions — workflows get deterministic, squads get judgment-based
    - §WORKFLOW_VS_SQUAD: when filling a workflow, enforce YAML-decides (not LLM routing). When filling a squad, surface LLM judgment points
    - §HEURISTICS: if evidence suggests wrong type (e.g., squad with 1 useful agent), surface demotion heuristic as coaching
    - §RUNTIME_BEHAVIOR: calibrate token budget expectations and explain context isolation to the creator
    - §ISOMORPHIC: use human cognitive analogies to explain product role to non-dev creators
    - For type=system ONLY: §SYSTEM_ENGINES — the 13 functional gears. Walk each active gear during fill, ask for concrete implementation decisions, verify counterpart coupling
    - §INTELLIGENCE_PIPELINE — governs how scout research ACTIVELY enters product content (not passively). For EVERY section: check if scout report has relevant findings → propose content from research → creator validates/refines → sparring challenges generic answers. This is the soul of the Engine — condensing intelligence, not just filling templates.
    - §FOUNDATIONAL_THESIS — for EVERY product, ask: "What should this NEVER be able to do?" The answer generates the intelligence flow. Use to guide frontmatter restrictions (denied-tools, paths: scoping).
    - §TRANSVERSAL_AXES — calibrate Nature (procedural/advisory/executive/orchestrative) and Depth (surface/functional/cognitive) during fill. A skill CAN be cognitive-depth. Don't assume type=depth.
    - §CONSTITUTIONAL_PRIMITIVES — for agents and minds, suggest criticalSystemReminder when the product must maintain identity over long conversations (50+ turns). Especially for cognitive minds.
    - §COMPOSITION_PRINCIPLES — when filling a squad or system, apply convergence-by-independence (specialists don't see each other's work until synthesis) and symbiosis rules.
7. Load `domain-map.md` if it exists (from /map) → use as knowledge source
8. **Load scout report** if `.meta.yaml` has `intent_declaration.scout_source` field (canonical location) OR `.meta.yaml` root-level `scout_source` field (legacy fallback) → read `workspace/{scout_source}` for research context. Extract: baseline (Section 1), gaps (Section 2), research findings (Section 4). This intelligence drives research injection in the section walk.
8b. **Domain intelligence back-reference:** Read `STATE.yaml → workspace.products[]`. Find products in the same `intelligence.domain` as the current product. If any exist with `intelligence.value_score` populated:
    - Read the most recent sibling's `.meta.yaml → intelligence` and `state.overall_score`
    - If sibling substance_score < 50: "Your last product in {domain} scored {substance}% substance. Focus on depth and real examples this time."
    - If sibling substance_score >= 70: "Your {domain} products have strong substance ({substance}%). Maintain this depth."
    - This closes the feed-back loop: /validate's output informs /fill's approach.
9. Scan product files for template placeholders and WHY comments
10. **Intelligence gap check:** If `.meta.yaml` has NO `scout_source` AND product targets MCS-2+:
    - Show: "No scout report found. Without baseline intelligence, /fill works in creator-knowledge-only mode — no research proposals, no baseline comparison."
    - Suggest: "Run `/scout {inferred_domain}` first for research-backed filling. Or continue with your expertise."
    - Record `fill_config.scout_available: false` in .meta.yaml
    - If creator continues without scout, skip research injection steps in section walker
11. **Structured input for choices**: If `creator.yaml → preferences.workflow_style = guided`, use `AskUserQuestion` for all choice points (enhance/replace/skip, deepening method selection, continue/save progress). Use plain text only for open-ended domain knowledge extraction.
12. **Read fill-protocol.md**: Read `${CLAUDE_SKILL_DIR}/references/fill-protocol.md` now — it contains the full execution protocol for all phases below.
12b. **SELF-CLONE branch (cognitive minds with sub_type=self only).**
    If `.meta.yaml.type == "minds" AND .meta.yaml.minds_sub_type == "self"`:
    - Load the SELF-CLONE content pack: Read `references/fill-content-packs/self-clone.md`
    - The content pack replaces the standard Discovery, Extraction Mode, and generic Section Walk phases
    - Follow the content pack's walker entry point (§1) which handles:
      - Mode selection (distillation vs elicitation based on corpus density)
      - Distillation pass (if applicable) with creator confirm/refine/reject per entry
      - Gap elicitation with the ordered question sequences per dimension
      - Dimensional routing (primary + secondary tagging)
      - Typology mirror (post-elicitation, three-step protocol)
      - Coherence diff generation
      - Honesty floor gates (counter-proofs, signed incaptable list, uncapturable decisions)
      - Writing populated content into the cognitive mind layer files
    - After the SELF-CLONE walker completes, skip to Completion (step 13 standard flow is bypassed)
    - The Sparring, Checkpointing, and Progress phases from the standard flow still apply during the walker — checkpoint after every two dimensions
    - Record `fill_config.self_clone: true` in `.meta.yaml`
    - **Do not run this branch for non-SELF cognitive minds or non-minds products** — all other types continue to step 12c or 13
12c. **SQUAD ORGANISM branch (type=squad only).**
    If `.meta.yaml.product.type == "squad"`:
    - **This branch replaces the standard section walker.** Squads are organism-level products — the standard single-file walk is insufficient. The squad walker iterates across the full directory tree.
    - **Phase 1 — Composition Discovery** (if not already answered in /create):
      - Ask archetype if not in `.meta.yaml`: Sequential Pipeline / Parallel Fan-Out / Conditional Router / Iterative Refinement / Hierarchical Delegation
      - **Role-aware composition (entity-ontology.md §AGENT_ROLES):** Instead of generic "how many specialists?", present the 7 functional roles:
        "Each specialist has a functional ROLE that determines tools and output. Select from: EXECUTOR (acts on files), SPECIALIST (deep analysis, read-only), ORCHESTRATOR (coordinates agents), ROUTER (classifies + directs), ADVISOR (thinks, never acts), VALIDATOR (checks quality), TRANSFORMER (converts formats)."
        Ask: "Name each specialist, their domain, and their role. Example: 'researcher=SPECIALIST, strategist=ADVISOR, executor=EXECUTOR, reviewer=VALIDATOR'."
        Record role assignment per agent for Phase 3 frontmatter generation.
      - Ask entity lifecycles: "What objects flow through this squad? (e.g., a CAMPAIGN, a LEAD, an EXPERIMENT). Describe the lifecycle stages."
    - **Phase 2 — Orchestrator Layer** (kernel/):
      - Walk `kernel/orchestration.md` — fill orchestration protocol. Ask: "How does the coordinator decide what to do? Describe its decision cycle step by step."
      - Walk `kernel/elicitation-engine.yaml` — fill progressive elicitation rules. Ask: "What questions does the squad ask the user before acting? How does it adapt based on answers?"
      - Walk `kernel/intelligence-matrix.yaml` — fill scoring/routing intelligence. Ask: "How does the squad score which agents are most relevant for a given request?"
    - **Phase 3 — Specialist Agents** (agents/):
      - For EACH agent file in `agents/*.md`:
        - Walk identity, role, tools, escalation rules
        - **Map to AGENT ROLE from entity-ontology.md §AGENT_ROLES.** The role assigned in Phase 1 determines:
          - Tool boundary: EXECUTOR=Write/Edit/Bash, SPECIALIST/VALIDATOR=Read-only, ORCHESTRATOR=Agent-only (no Write/Edit), ADVISOR=denied-tools
          - Handoff format: EXECUTOR→artifacts, ADVISOR→judgment, ORCHESTRATOR→routing decisions, VALIDATOR→score+verdict, TRANSFORMER→converted output
          - Frontmatter: set `allowed-tools` or `denied-tools` per role mapping in the agent .md file
          - Question shape: EXECUTOR→"What does it produce?", ADVISOR→"What reasoning framework?", VALIDATOR→"What criteria?", TRANSFORMER→"What's the input/output format?"
        - If agent has a mind-clone source in `minds/`: load `minds/{name}/cognitive-model.md` and use as knowledge substrate
        - Apply D1 (activation protocol), D2 (anti-patterns ≥5), D14 (graceful degradation) per agent
        - Sparring: "What would this specialist REFUSE to do? What's outside its boundary?"
    - **Phase 4 — Task Registry** (tasks/):
      - Walk `tasks/task-registry.yaml` — for each specialist, define 3-10 granular tasks with:
        - task_id, description, assigned_agent, input_schema, output_schema, quality_gate
      - Ask per agent: "What are the 3-5 most important things {agent_name} does? For each, what input does it need and what output does it produce?"
    - **Phase 5 — Chains & Workflows** (chains/, workflows/):
      - Walk `chains/chain-registry.yaml` — define micro-workflows (2-4 agent sequences with cadences)
      - Walk `workflows/*.md` — define full pipelines mapping lifecycle stages to agents
      - Ask: "Walk me through the main workflow from start to finish. Which agent handles each step? What passes between them?"
    - **Phase 6 — Routing & Handoff** (config/):
      - Walk `config/routing-table.md` — fill declarative routing rules (IF intent → agent)
      - **Calibrate routing per §WORKFLOW_VS_SQUAD:** Squad routing involves LLM judgment — the orchestrator reads rules BUT interprets contextually. Ensure routing questions surface the judgment points: "When the input is ambiguous, how does the orchestrator decide?" This is what makes it a squad, not a workflow.
      - **Use §INTELLIGENCE_GRADIENT** to calibrate autonomy: "How much should the orchestrator decide autonomously vs. escalate to the human? Where on the deterministic↔autonomous spectrum should routing sit?"
      - Walk `config/handoff-protocol.md` — define handoff envelope format (XML or structured)
      - Sparring: "What happens when the input doesn't match any route? What's the fallback?"
    - **Phase 7 — Quality & Testing** (tests/):
      - Walk test scenarios: happy path, edge case, adversarial, agent failure recovery
    - **Anatomy completeness check (entity-ontology.md §SQUAD_ANATOMY):** Before transitioning to content state, verify all 8 squad anatomy components have been addressed:
      1. Agent Roster — at least 2 agent files in agents/ with substantive content
      2. Routing Table — config/routing-table.md has routing rules (not just placeholder)
      3. Handoff Protocols — config/handoff-protocol.md has envelope format
      4. Workflows — at least 1 workflow with steps defined in workflows/
      5. Skills-as-Instruments — skills/ directory exists (advisory — some squads don't need shared skills)
      6. Checklists — SQUAD.md has quality/checklist section with ≥2 items
      7. Templates — kernel/ has output format standards
      8. Escalation — SQUAD.md has escalation section with confidence thresholds
      If any component is missing, flag it: "Your squad is missing {component}. Without it, {consequence}. Want to add it now or defer?"
    - **Completion:** After all phases, update `.meta.yaml` with `fill_metrics` and transition state to `content`.
    - Record `fill_config.squad_organism: true` in `.meta.yaml`
12d. **Agent ontology-aware elicitation (type=agent only, non-squad).** If type == "agent" AND branch 12c did NOT fire:
    - Entity ontology already loaded at step 6b
    - At the START of the section walk, ask the role question: "What functional role does this agent fill? EXECUTOR (acts on files), SPECIALIST (analysis only), ADVISOR (thinks, never acts), VALIDATOR (checks quality), TRANSFORMER (converts formats)?"
    - Use the selected role to determine:
      - Which tools to suggest in the frontmatter section (EXECUTOR→Write/Edit/Bash, SPECIALIST→Read-only, ADVISOR→denied-tools)
      - What output to expect (artifacts vs reports vs reasoning)
      - What questions to emphasize (EXECUTOR→"What does it produce?", ADVISOR→"What reasoning framework?", VALIDATOR→"What criteria does it check?")
    - Record role in `.meta.yaml → agent_role` for /validate consumption
12e. **Workflow ontology-aware elicitation (type=workflow only).** If type == "workflow":
    - Entity ontology already loaded at step 6b
    - Enforce §WORKFLOW_VS_SQUAD: workflows use SKILLS (not agents), have FIXED sequences (not LLM routing), are DETERMINISTIC (same input → same execution path)
    - During the section walk, ask:
      - "What skills does each step invoke?" (NOT "what agents" — workflows don't use agents)
      - "Is the sequence always the same regardless of input?" (If answer is "it depends" → suggest squad: "This sounds like it needs contextual routing — that's a squad, not a workflow. Want to switch?")
      - "What are the gate conditions between steps?" (pass/fail criteria for proceeding)
    - If evidence suggests LLM judgment needed → surface heuristic from §HEURISTICS as coaching
13. Begin section-by-section guided extraction (see fill-protocol.md → DISCOVERY PHASE)

---

## Core Flow (routing table — details in fill-protocol.md)

| Phase | What happens | Protocol section |
|-------|-------------|-----------------|
| Discovery | 3 front-loaded questions (audience, differentiator, use case) | DISCOVERY PHASE |
| Acceptance Criteria | Define 3 machine-verifiable criteria before section walk | ACCEPTANCE CRITERIA CAPTURE |
| Extraction Mode | Select mode (Standard/Socratic/Adversarial/Archaeological/Council) for MCS-2+ | EXTRACTION MODE SELECTION |
| Pitfall Check | Load meta/pitfalls/pitfalls.json, surface type-relevant warnings | PITFALL CHECK |
| Type Coaching | Platform-specific coaching (claude-md, minds, hooks, skill/agent, system/bundle) | TYPE-SPECIFIC COACHING |
| Section Walk | Per-section: read WHY, check existing, inject research, ask, write, quality signal | SECTION WALKER |
| Sparring | 3 challenges per major section (Generic Test, Inversion, Proof) — mandatory MCS-2+ | SPARRING PROTOCOL |
| Deepening | 5 elicitation methods offered as optional menu after each major section | ELICITATION DEEPENING |
| Checkpointing | Write fill_progress to .meta.yaml after every section (compact-safe) | MID-FILL STATE PERSISTENCE |
| Progress | Pulse every 2-3 sections: filled/total + live MCS estimate | PROGRESS TRACKER |
| Conversational | Narrative extraction mode for non-dev creators | CONVERSATIONAL MODE |
| Size Check | Auto-split primary file if >4K chars; suggest @include for claude-md; **enforce calibration budget** — if intent-aware calibration set a size target, warn when exceeded | INSTRUCTION SIZE OPTIMIZATION |
| Completion | Promote to content, auto-validate MCS-1, **report result honestly** (pass → celebrate; fail → name the failures), clear fill_progress | AFTER ALL SECTIONS FILLED |

---

## Quality Gate

Before promoting to "content" state:
- [ ] Primary file has at least 3 sections with substantive content
- [ ] No sections contain ONLY placeholder/template text
- [ ] README.md follows `templates/readme/README.md.template` structure: Hero (problem hook), Install, "Is this for me?", Quick Start, Features (with depth — heading + what + why per feature), Use Cases (scenario table), How It Works, type-specific section, Requirements, Compatibility, Language, License, Footer. Trilingual (EN, PT-BR, ES) with anchor navigation. Each language block has FULL content — not just translated headers.
- [ ] At least one domain-specific insight encoded (not generic)

**Auto-validate honesty rule:** When the silent MCS-1 check at completion finds failures, the creator-facing message MUST name them. "Looking good" is forbidden when checks fail. Use: "Content captured. {N} structural items need attention before validation passes: {list}. Run `/validate --fix` to resolve."

---

## Anti-Patterns

1. **Robotic Q&A** — Don't be a questionnaire. Be conversational. Reference previous answers. Connect dots between sections.
2. **Overwriting creator edits** — If creator has already manually edited a section, don't overwrite. Ask: "This section has content. Enhance, replace, or skip?"
3. **Generic fill** — If a section reads like any AI could write it, push: "What's YOUR specific approach here? What would surprise someone reading this?"
4. **Section overload** — Don't try to fill everything in one session. After 5-6 sections, offer: "We covered the core. Want to continue or save progress and come back?"
5. **Ignoring domain-map** — If domain-map.md exists, USE it. Don't re-ask questions already answered there.
6. **Thin sections without flagging** — Never leave a <50 word section without telling the creator it's thin. Section quality signals are mandatory.
7. **Skipping acceptance_criteria** — Must-have capture is NOT optional. Without acceptance criteria, /validate has nothing goal-backward to check.
8. **Forgetting persona mid-fill** — Re-read creator.yaml persona BEFORE each major section. A developer gets different questions than a marketer, even for the same section.

---

## Compact Instructions

When context is compressed, preserve:
- Target product slug, type, current phase (scaffold/content)
- `fill_progress.last_completed_section` and `fill_progress.sections_filled`
- Active extraction mode (`fill_config.extraction_mode`)
- Sparring state: `sparring.sections_challenged`, `sparring.skipped`
- Scout availability (`fill_config.scout_available`)
- Any blocking issues found during mid-fill quality signals
- Next section to fill (resume from `last_completed_section + 1`)
