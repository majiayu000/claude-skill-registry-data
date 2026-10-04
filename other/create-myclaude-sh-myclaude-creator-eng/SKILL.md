---
name: create
description: >-
  Scaffold a new product with MCS-1 valid structure and WHY comments. Supports all
  13 types. Use when the creator says 'new skill', 'create', 'scaffold', 'start
  building', or wants to start a new product.
argument-hint: "[product-type]"
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - AskUserQuestion
---

# Scaffolder

Generate complete, MCS-1-valid project structure for any product type with guidance comments baked in.

**When to use:** Starting a new product — any of the 13 types.

**When NOT to use:** When the product already exists in `workspace/` and you want to add content (use `/fill`). Do not use to overwrite an existing scaffold unless `--force` is specified.

---

## Activation Protocol

0. **Shared preamble:** Load `references/quality/activation-preamble.md` — context assembly, persona adaptation, deterministic routing rules.
1. Read `creator.yaml` — load defaults. Check `schema_version`:
   - **`< 3`** → invoke `/onboard` skill to run Phase 2.5d silent migration first. Migration is atomic + backed up to `creator.yaml.bak.v2`. After migration succeeds, re-read the v3 file and continue.
   - **Missing** → **micro-onboard**: scan silently, infer defaults, ask ONE name question, generate minimal `creator.yaml` (v3). Never block.
2. **Persona**: Adapt to `profile.type` + `technical_level`. Load `references/quality/engine-voice-core.md`. Load the full `references/quality/engine-voice.md` only when composing peak moments (scaffold celebration, Step 10 proposal rendering, first-product WOW).
2c. **Exemplar load:** Load `references/quality/exemplar-outputs.md` section E3 only — the scaffold celebration reference. Your scaffold announcement MUST carry the same visual rhythm (Frame + pipeline position + portfolio context + 🎯 next action). Adapt to this creator's language and journey position.
2d. **Load proactives:** Load `references/engine-proactive.md` — wire #1 (pipeline guidance: after scaffold, guide to /fill), #18 (WOW moment for first product scaffold), #21 (portfolio pattern detection on brownfield check).
2b. **Load architectural DNA:** Read `structural-dna.md`. The 10 architectural principles and the Tier 1 DNA patterns (D1-D4, D13, D14) govern every scaffold — the skill applies them during Step 11 template generation and flags any violation before the scaffold is written to disk.
3. **Discovery Mode Routing (W3.2 — PRIMARY ROUTER):** Load `${CLAUDE_SKILL_DIR}/references/create-router.md` **Section 0** — the 12-step discovery walk. Apply the Mode Selection table (Express vs Guided) based on `creator.profile.technical_level` + `creator.preferences.workflow_style` + any `--express`/`--discovery` flag.
   - **Express mode** → run the "12 Steps — Express Mode Fast Path" section of create-router.md Section 0. Reads type + sub-type flags, applies defaults from `config.yaml routing.{type}.intent_topology`, skips interactive questions, derives the full 19-field `intent_declaration` in one pass, and writes it at Step 11 of the walk.
   - **Guided mode** → run the "12 Steps — Guided Mode Walk". Asks Q1 (verb family) interactively, reads `creator.intent_profile` silently for Steps 2/3/6, escalates at Step 6 if cognitive justification incomplete, proposes form at Step 10 with confirmation, writes `intent_declaration` at Step 11.
   - **Discovery returns unroutable (Step 9 zero-match)** → fall through to create-router.md **Section 1** legacy Q1/Q2/Q3 tree (Contract C4). The creator is never blocked. `unroutable: true` + `unroutable_reason` recorded in `intent_declaration`.
   - **Creator chose "I don't know yet" at Step 1** → route to `/scout` suggestion OR legacy tree, at creator's choice.
4. **Gates**: Read `config.yaml → gates.confirm_create`. Confirm if `true`; proceed if `false`.
5. **Brownfield check**: Glob `workspace/*/`. If same `product.type` or overlapping tags found, surface slugs and ask before continuing.
6. **Exemplar guard**: Glob `references/exemplars/{category}*`. If found: show condensed preview. If not: skip gracefully — never halt.
7. Load `product-dna/{category}.yaml` → DNA requirements.
7b. **Load entity ontology (squad/system/agent/workflow/minds):** If type ∈ {squad, system, agent, minds, workflow}, read `references/entity-ontology.md`. This substrate governs:
    - Which agent ROLES to suggest during composition discovery (§AGENT_ROLES — 7 functional archetypes with tool boundaries)
    - The heritage chain — what this type inherits from and composes with (§HERITAGE, §COMPOSITION)
    - The 8 squad anatomy components that MUST appear in the scaffold (§SQUAD_ANATOMY)
    - The intelligence gradient — where this type sits in the determinism↔autonomy spectrum (§INTELLIGENCE_GRADIENT)
    - The distinction between workflow (YAML decides) and squad (LLM decides) coordination (§WORKFLOW_VS_SQUAD)
    - Promotion/demotion heuristics — is this really the right type? (§HEURISTICS)
    - Runtime behavior — how this type activates and its token cost (§RUNTIME_BEHAVIOR)
    - For /scout-informed creates: type recommendation matrix (§SCOUT_INTELLIGENCE)
    - Isomorphic human↔CC mapping for creator-facing explanations (§ISOMORPHIC)
    - For type=system ONLY: the 13 functional gears (§SYSTEM_ENGINES) — ask which gears the creator wants active, scaffold coupling declarations
    - The intelligence pipeline that governs how scout research enters the product (§INTELLIGENCE_PIPELINE)
    - The foundational thesis: restrictions generate intelligence flow — ask "What should this NEVER do?" (§FOUNDATIONAL_THESIS)
    - Transversal axes: after type selection, calibrate Delivery × Nature × Depth (§TRANSVERSAL_AXES)
    - Composition principles: how products think together — convergence by independence, symbiosis > aggregation (§COMPOSITION_PRINCIPLES)
8. Load `${CLAUDE_SKILL_DIR}/references/discovery-questions.md` → category questions.
9. Load `references/product-specs/{category}-spec.md` + `templates/{category}/`.
10. Load `workspace/domain-map.md` if exists → prefill scaffold sections.
10b. **Link scout report** if used — `scout_source` is already recorded in `intent_declaration.scout_source` by Section 0 Step 11. No additional action needed here; the canonical home for scout_source is `intent_declaration`, not a parallel field.
10c2. **CLI contract:** Load `references/cli-contract.md` for unified error handling. This skill has minimal CLI surface — one command at Step 1.5. Severity map:
   - **Silent-skip:** `search --category {type} --sort downloads --limit 3` — marketplace scan for competitive context. Skip without warning on failure. **First-product guard:** skip entirely if `is_first_product` (already documented at Step 1.5)
   - **All queries:** append `--json 2>/dev/null`, 15s timeout
10c. **Portfolio intelligence (back-reference from /validate)**: Read `STATE.yaml → workspace.products[]` AND `STATE.yaml → mcs_results`. Group by domain. If domain has existing products:
   - Show: "Your {domain} portfolio: {slugs}. This will be product #{N}."
   - If N >= bundle threshold (`config.yaml → intelligence.portfolio.bundle_suggestion_threshold`): suggest bundling.
   - If complementary type opportunity exists: surface composition suggestion.
   - **MCS target calibration**: If domain has 0 products → default MCS-1 (ship fast, test market). If domain has 2+ validated products → default MCS-2 (quality matters, audience exists).
   - Record `intelligence.domain` and `intelligence.market_position` in `.meta.yaml`.
11. Generate scaffold in `workspace/{product-slug}/` with DNA patterns + WHY comments. The scaffold's type + structure come from the `matched_cell.canonical_form` decided at Section 0 Step 10.
    **Ontology-aware scaffold verification (requires entity-ontology.md loaded at step 7b):**
    For type=squad: verify scaffold contains all 8 anatomy components from entity-ontology.md §SQUAD_ANATOMY:
      1. Agent roster (agents/) — each specialist as separate .md file with role-appropriate frontmatter
      2. Routing table (config/routing-table.md) — IF intent → agent mapping with judgment points
      3. Handoff protocols (config/handoff-protocol.md) — structured envelope format (from, to, task, state, constraints)
      4. Workflows (workflows/) — multi-agent sequences with gates and loops
      5. Skills-as-instruments (skills/) — reusable fragments agents invoke
      6. Checklists — deterministic verification section in SQUAD.md
      7. Templates — output format standards in kernel/
      8. Escalation/quality gates — confidence thresholds and loop limits in SQUAD.md
    For type=agent or type=minds: apply §AGENT_ROLES — the role selected during discovery determines frontmatter tool boundaries (`allowed-tools`/`denied-tools`) and handoff format expectations. Generate role-appropriate frontmatter.
    For type=workflow: verify scaffold distinguishes from squad per §WORKFLOW_VS_SQUAD — workflows use skills (not agents), fixed sequence (not LLM routing), deterministic gates (not judgment). If scaffold looks like a squad, surface heuristic coaching.
    For type=system: apply §HERITAGE — system inherits all squad DNA + adds CLAUDE.md fragment, hooks, output-style, STATE.yaml. Scaffold must include provisions for all composed types per §COMPOSITION.
    For type=system: apply §SYSTEM_ENGINES — scaffold a `gears_declaration` section in the system's primary file. Ask the creator: "Which of these organism capabilities do you want active?" Present the 13 gears grouped by function:
      - Boundary: E0 (clausura) — always required
      - Metabolism: E1 (token budget), E2 (constitution re-injection)
      - Memory: E3 (triple memory), E10 (persistent state)
      - Perception-Reflex: E4 (hooks perception), E5 (cognitive reflex)
      - Judgment-Coordination: E6 (isolated judgment), E7 (coordination network)
      - Identity: E8 (external voice)
      - Integrity: E9 (recursive validation), E11 (longitudinal self-observation — advanced, MCS-3)
      - Lifecycle: E12 (reversible install/uninstall)
      For each active gear, the scaffold includes a section with WHY comment and its counterpart declaration.
11b. **Locale-adaptive clause substitution (W3.6 — MANDATORY for 6 certified types):** For each template file written (SKILL.md, AGENT.md, SQUAD.md, CLAUDE.md for system, AGENT.md for minds, OUTPUT-STYLE.md), perform placeholder substitution for `{{LOCALE_ADAPTIVE_CLAUSE}}`:
    a. Read the canonical clause block from `references/locale-adaptive-clause.md §2` (the fenced markdown block between `<<< LOCALE-ADAPTIVE CLAUSE ... >>>` and `<<< END CLAUSE >>>`, inclusive).
    b. Read the localized header from `config.yaml → routing.common.locale_adaptive_clause.localized_header_catalog.{creator.language}`. If the creator's language is not in the catalog, use the `fallback` entry and emit an advisory note.
    c. Build the substitution block: `<!-- {localized_header} -->\n\n{canonical_clause}`.
    d. Replace the literal string `{{LOCALE_ADAPTIVE_CLAUSE}}` in each written template file with the substitution block. Use a literal-string replace, not a regex — the placeholder is unique and must not be interpreted.
    e. Verify post-substitution: the forged file must contain both marker strings (`<<< LOCALE-ADAPTIVE CLAUSE (runtime contract, do not edit) >>>` and `<<< END CLAUSE >>>`). If either marker is missing after substitution, the forge fails + rollback.
    e2. **Duplication guard:** Before substitution in step (d), check if the target file ALREADY contains the marker `<<< LOCALE-ADAPTIVE CLAUSE`. If found, skip substitution for that file and emit advisory: "Locale clause already present in {file} — skipping to prevent duplication." This handles re-forge (`--force`) scenarios where the template already carried a clause from a prior run.
    f. For type `squad`, also perform the substitution on every file in `workspace/{slug}/agents/*.md` (sub-agents inherit the clause per `references/locale-adaptive-clause.md §4`).
    g. For type `system`, also perform the substitution on every sub-part file (claude-md fragment, sub-agents, sub-squads) per §4.
    h. Record `intent_declaration.language` (already populated at Section 0 Step 11) as the source language used for the lookup — this becomes the `source_language` field in vault.yaml at /package time.
12. Create `.meta.yaml` (see template below). The `intent_declaration` block is already populated from Section 0 Step 11; the rest of the template is filled by this step (product, state, history, intelligence).
13. Move `workspace/domain-map.md` → `workspace/{product-slug}/domain-map.md` if loaded.
14. **Atomic commit (Contract C5):** write order matters — `.meta.yaml` first (it is the local source of truth), then `STATE.yaml decisions_history` append.
    - If `.meta.yaml` write fails: abort, announce failure. Nothing else proceeds.
    - If `STATE.yaml` append fails after `.meta.yaml` succeeds: **do not roll back the scaffold**. The scaffold on disk is recoverable; a deleted scaffold is not. Instead: log `state.tracking_sync: false` in `.meta.yaml`, emit Engine-fault voice line — *"Scaffold forged but Engine lost tracking. Run /status to resync."* — and continue. `/status` will detect the orphan on next run and surface it for recovery.
    - Only report `forge_ready` when both writes succeed without error.
15. Engine voice: "Scaffold ready. {N} sections with WHY guidance. Run /fill to start." In Guided mode, also include one-line summary of the cell matched and why: *"Forjado como {canonical_form} — {rationale}."*

---

## Router Logic

**Read `${CLAUDE_SKILL_DIR}/references/create-router.md`** — the file has two sections:

- **Section 0 — DISCOVERY MODE (PRIMARY ROUTER, W3.2):** the 12-step decision algorithm from `references/capability-matrix.md §3`. Runs in either Express or Guided mode per Activation Protocol step 3. Writes the 19-field `intent_declaration` to `.meta.yaml`. This is the primary path for **every** /create invocation in schema v3.
- **Section 1 — LEGACY DECISION TREE (FALLBACK):** the Q1/Q2/Q3 tree preserved verbatim from pre-Wave-3. Runs when Section 0 Step 9 returns `unroutable` (Contract C4) or when the creator explicitly picks "I don't know yet" at Section 0 Step 1 or invokes `--legacy-router`. Also contains: per-category scaffold structures (Section 2), prefilling strategy (Section 3).

**Direct sub-commands** trigger Express mode (skip the interactive walk, apply type+sub-type defaults, write `intent_declaration` with `mode: express`):
`/create skill [my-tool]` | `/create agent` | `/create squad` | `/create workflow` | `/create ds` | `/create claude-md` | `/create app` | `/create system` | `/create bundle` | `/create statusline` | `/create hooks` | `/create minds` | `/create output-style`

**Depth flags** (Express mode only, pairs with type sub-command):
`--procedural` | `--advisory` | `--cognitive` | `--genius [profile_name]` (for minds)

**Mode override flags:**
`--express` — force Express mode regardless of creator profile
`--discovery` — force Guided walk (synonym: `--guided`) regardless of creator profile
`--legacy-router` — skip Section 0 entirely, go straight to Section 1 legacy tree
`--quick` — Express mode + skip marketplace scan + skip exemplar preview (legacy alias, retained for backward compatibility)

For experienced creators who know exactly what they want, Express mode + sub-command is the one-motion path. For creators discovering what to build, Guided mode walks them through. For creators in unmapped territory, Section 1 legacy fallback guarantees they always have a path forward.

---

## Universal Creation Flow

| Step | Action | Detail |
|------|--------|--------|
| 1 | Name + Description | Derive slug: lowercase, hyphens, validate `^[a-z0-9][a-z0-9-]{2,39}$`. Existing `workspace/{slug}/` → offer `/fill` or `--force`. CLI init: vault.yaml but no .meta.yaml → import into Engine workspace. Suggest `/map` if deep domain knowledge involved. |
| 1.5 | Marketplace Scan | `myclaude search --category {type} --sort downloads --limit 3 --json 2>/dev/null`. Show top 3 with downloads + "What will yours do differently?" Coaching only — never blocking. **First-product guard:** If `is_first_product`, SKIP this step — a first-timer seeing competitor data before articulating their own idea causes second-guessing. Show marketplace context AFTER scaffold, not before. |
| 2 | Discovery Questions | Load + ask from `${CLAUDE_SKILL_DIR}/references/discovery-questions.md`. Ask conversationally. `workflow_style=guided` → AskUserQuestion; `autonomous` → plain text. |
| 3 | Load Defaults | From `creator.yaml`: license, version (always 1.0.0), author, quality target. |
| 4 | Generate Scaffold | **Structure only** — files, YAML frontmatter, section headers with WHY comments, template vars for metadata. Never generate substantive prose. Leave `[To be filled — run /fill]` for expertise sections. See router.md for per-category structures. |
| 5 | MCS-1 Structural Validation | Silently verify: required files present, metadata fields populated, README.md follows `templates/readme/README.md.template` structure (Hero, Install, "Is this for me?", Quick Start, Features, How It Works, type-specific, Requirements, Compatibility, Language, License — trilingual EN/PT-BR/ES with anchor nav), no YAML/JSON syntax errors. Auto-fix and note corrections. |
| 6 | Print Next Steps — Cognitive UX | **Load full UX stack:** `references/ux-experience-system.md` (§1 context assembly, §2.3 moment awareness for "first scaffold"), `references/ux-vocabulary.md` (type naming), `references/quality/engine-voice.md` (brand DNA). Output is REASONED, not templated — adapt based on creator context. |

**Step 6 Cognitive Output Protocol:**

Assemble context from creator.yaml + STATE.yaml, then REASON about output:

```
IF is_first_product:
  → Full journey map. Warm tone. "Your first product exists."
  → Show all 4 pipeline steps explicitly.
  → Use encouraging language: "I'll guide you through each step."

IF products_published >= 5:
  → Compact. "✦ {name} scaffolded. {N} files. /fill when ready."
  → Skip journey map (they know the pipeline).
  → Surface only non-obvious: portfolio position, domain intelligence.

IF scout_source exists:
  → Reference the research: "Scaffolded from your {domain} research. {gaps_found} gaps mapped."

IF same domain has existing products:
  → Surface composition: "This joins {existing_slugs} in your {domain} portfolio."

ALWAYS:
  → Use ux_type_name from ux-vocabulary.md (e.g., "Deep Intelligence" not "minds")
  → Brand frame: ✦ marker, MyClaude Studio box (for first product or guided mode)
  → Pipeline position: "scaffold → ▸ fill → validate → test → package → publish"
  → Clear next action: "/fill" (always the next step after create)
  → VOCABULARY GUARD: Before emitting ANY creator-facing text, grep output for internal terms (MCS-N, DNA, D1-D20, scaffold, forge, substrate, habitable cell, intent_declaration, Sparring Protocol). If creator.profile.type is NOT "developer" or "hybrid", replace per ux-vocabulary.md. If "developer" or "hybrid", internal terms MAY appear but MUST be accompanied by context.
```

**Default frame (guided mode or first 3 products):**
```
┌─ MyClaude Studio ───────────────────────────┐
│  ✦ {product_name} — {ux_type_name}          │
│                                              │
│  {cognitive_insight based on context}        │
│                                              │
│  ▸ scaffold → fill → validate → test → ship │
│  Next: /fill                                │
└──────────────────────────────────────────────┘
```

**Compact frame (autonomous mode or 5+ products):**

For developers:
```
✦ {product_name} scaffolded. {N} files. {cognitive_insight}. /fill
```

For non-developers (profile.type != developer):
```
✦ {product_name} is ready. {N} files created. {cognitive_insight}. Add your expertise next → /fill
```

---

## .meta.yaml Template

Create `workspace/{product-slug}/.meta.yaml`:

```yaml
# Product metadata — not distributed, stripped during /package
product:
  slug: "{product-slug}"
  type: "{category}"               # skill|agent|squad|workflow|design-system|claude-md|application|system|bundle|statusline|hooks|minds|output-style
  created: "{YYYY-MM-DD}"
  mcs_target: "{MCS-1|MCS-2|MCS-3}"
  # NOTE: For type=minds, cap mcs_target at MCS-2 (Tier 3 DNA patterns are mostly N/A).
  # Show: "Minds ceiling is MCS-2 (Tier 3 DNA patterns not applicable). Setting target to MCS-2." (G015)
  # Minds-specific (only when type=minds):
  # minds_depth: "advisory|cognitive"
  # minds_sub_type: "self|genius|domain"  # cognitive only
  # genius_profile: "{name}"              # genius only

state:
  phase: "scaffold"                # scaffold | content | validated | packaged | published
  last_validated: null
  last_validation_score: null
  dna_compliance:
    tier1: null                    # 0-100
    tier2: null
    tier3: null
  overall_score: null
  last_tested: null
  test_result: null              # "pass" | "fail" | null
  test_scenarios: null           # "{passed}/{total}" | null

history:
  created_at: "{YYYY-MM-DD}"
  validated_at: []                 # append timestamps
  packaged_at: null
  published_at: null
  version: "1.0.0"

# Intent Declaration — the canonical record of how /create reasoned from creator intent
# to forged form. Written by /create at Step 11 of the 12-step algorithm (express or
# guided mode). Consumed by: /validate Stage 0 (Intent Coherence), /fill (natureza-aware
# section walks), /package (manifest shape), and STATE.yaml decisions_history
# (longitudinal feedback loop per capability-matrix.md §6).
#
# Schema source of truth: references/capability-matrix.md §3 Step 11 (19 fields).
# Enum sources:
#   - references/intent-topology.md §2 (delivery, nature, depth axis enums)
#   - references/intent-topology.md §4 (habitable cells v1)
#   - references/capability-matrix.md §3 Step 1 (verb_family enum)
#   - references/capability-matrix.md §3 Step 9 (unroutable_reason enum)
#   - references/capability-matrix.md §4 (mode enum: express | guided)
#
# Null-safe discipline (Contract C9): every field is populated on every forge. Fields
# not applicable to the current mode/path are set to null (single-value) or [] (list).
# Never omit a field — downstream consumers must not distinguish "absent" from "null".
#
# This block is the canonical home for scout_source (Activation Protocol step 9b).
intent_declaration:
  captured_at: null       # ISO-8601 when /create resolved the triple (Step 11)
  creator_said: null      # verbatim intent text (guided mode), or "(express mode)"
  mode: null              # express | guided (see references/capability-matrix.md §4)
  mode_switches: []       # appended by §5 transition protocol; each entry: {from, to, trigger, at_step, at_time}
  language: null          # mirror of creator.yaml → creator.language at forge time (drives locale-adaptive clause + announcements)
  scout_source: null      # "scout-{slug}.md" if a scout report informed this forge (canonical location for Activation Protocol step 9b)

  # engine_parsed — per-step outputs of the 12-step algorithm. In express mode, these
  # are populated from sub-command flags + type defaults. In guided mode, from the walk.
  engine_parsed:
    verb_family: null         # do_X | advise_on_X | coordinate_X | observe_X | enforce_X | react_to_X  (Step 1)
    continuity_bias: null     # parent | isolated | unclear  (Step 2)
    invocation_mode: null     # remembered | needs_auto  (Step 3)
    pollution_risk: null      # pollutes | safe  (Step 4)
    output_shape: null        # amplified_reasoning | structured_report  (Step 5)
    depth: null               # procedural | advisory | cognitive  (Step 6)
    nature: null              # executor | advisor | orchestrator | observer  (Step 7)
    delivery_mechanism: null  # ambient_constitutional | ambient_path_scoped | invoked_slash_command | invoked_task_spawn | reflex_hook_binding | composed_system  (Step 8 primary)
    host_set: []              # derived from (delivery, nature) per references/runtime-host-dag.md §2 — NEVER declared, always computed

  # Canonical cell lookup result (Step 9)
  matched_cell: null          # habitable cell id from intent-topology.md §4 (e.g. "reasoning_skill_cognitive"), or null if unroutable
  ranked_alternatives: []     # up to 2 alternative cell ids surfaced in the proposal

  # Creator-facing proposal (Step 10)
  proposed_form: null         # canonical_form from matched_cell, or null if unroutable
  creator_choice: null        # accepted | overridden
  override_to: null           # creator's chosen form if overridden
  override_reason: null       # creator's one-line explanation if overridden

  # Unroutable handling (Contract C4 — fall-through is a feature, not a failure)
  unroutable: false
  unroutable_reason: null     # no_habitable_cell | v2_cell_deferred | blocked_by_composition_gap | ambiguous_between_cells
  unroutable_gap_id: null     # gap marker from composition-anatomy.md (e.g. "GAP-COMPOSITION-1") when unroutable_reason == blocked_by_composition_gap

  # Audit markers for post-hoc schema evolution + default-tracking
  discriminators_applied: [] # which of [continuity, invocation, pollution, output, depth] actually fired (not just defaults)
  defaults_applied: []       # intent_profile field names that fell back to declared defaults (schema v3 gap tracking)

# Intelligence Layer fields (populated by /validate Stage 8, /scout, /package)
# Reference: references/intelligence-layer.md + config.yaml intelligence section
intelligence:
  domain: null                     # inferred from scout or content (e.g., "kubernetes-security")
  market_position: null            # blue_ocean | moderate | saturated
  value_score: null                # 0-12 composite (depth + uniqueness + coverage + market)
  value_score_breakdown: null      # { depth: N, uniqueness: N, coverage: N, market: N }
  suggested_price_range: null      # [min, max] USD
  pricing_strategy: null           # free | signal | solid | premium | rare
  distribution_channels: []       # ranked channels for this product type
  portfolio_role: null             # anchor | complement | extension | standalone
  scored_at: null                  # ISO-8601 timestamp of last intelligence computation
```

---

## Quality Gate

Generated scaffold must pass MCS-1 before being shown to the creator:
- All required files for the product type are present
- All required metadata fields are populated (even with placeholders)
- README.md skeleton follows the structure from `templates/readme/README.md.template` — required sections: Hero (problem hook + description), Install, "Is this for me?", Quick Start, Features, How It Works, type-specific section, Requirements, Compatibility, Language, License, Footer. Trilingual structure (EN, PT-BR, ES) with anchor navigation. /create scaffolds section headers with WHY comments; /fill populates content.
- No syntax errors in any generated YAML or JSON
- `.meta.yaml` is valid and contains all required fields

---

## Anti-Patterns

1. **Generating content during scaffold** — /create generates structure only. Substantive prose, domain knowledge, examples: all /fill's job. Content here bypasses the Sparring Protocol → generic latão polido.
2. **Blocking on missing creator.yaml** — Always micro-onboard and continue.
3. **Overwriting without --force** — Never touch existing workspace products without explicit flag.
4. **Skipping brownfield check** — Always check same-type products before scaffolding.
5. **Skipping portfolio intelligence (step 9c)** — Domain grouping and bundle suggestions must fire when threshold is met.

---

## Decision Notes

**CE-D12:** WHY comments (`<!-- WHY: ... -->`) explain what the creator must fill in. Stripped during `/package`. Creators should NOT remove them — harmless in workspace.

**Pre-validate at scaffold time:** Starting at MCS-1 means creators never fix basics. Scaffold failures are bugs in the Scaffolder, not creator errors.

**Sub-command routing:** `/create skill` etc. skip the menu for experienced creators. Menu exists for first-time users who don't know the vocabulary.

**Scaffold vs content separation:** Content generated by /create bypasses /fill's Sparring Protocol → zero unique expertise. Structure (scaffold) and content (expertise) must stay separate. That separation is what makes the Engine produce gold.
