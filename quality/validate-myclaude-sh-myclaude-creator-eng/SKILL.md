---
name: validate
description: >-
  Run MCS quality validation on products in workspace/. Three-tier system: MCS-1
  structure, MCS-2 quality + anti-commodity, MCS-3 deep review. Returns scored reports
  with fix instructions. Use when: 'validate', 'check quality', or before publishing.
argument-hint: "[--level=1|2|3] [--fix] [--batch] [--express]"
allowed-tools:
  - Read
  - Edit
  - Glob
  - Grep
  - Bash(myclaude *)
---

# Validator

Run MCS quality checks on any product in `workspace/` and return actionable, scored reports.

**When to use:** After building or modifying a product, before publishing, or anytime you want a quality snapshot.

**When NOT to use:** On products outside `workspace/`. Do not use to validate the Engine itself.

---

## Activation Protocol

0. **Shared preamble:** Load `references/quality/activation-preamble.md` — context assembly, persona adaptation, deterministic routing rules.
1. Detect product type: read `.meta.yaml` → `product.type` and `state.phase`
   - Missing → infer from file structure (SKILL.md, AGENT.md, SQUAD.md, hooks.json, etc.)
   - Cannot determine → ask: "What product type is this?"
1b. **Mode selection (Express vs Guided).** Read `creator.yaml → preferences.workflow_style`. Resolve the flow mode:
    - `--express` flag OR `workflow_style == "autonomous"` → **Express mode**. Skip the coaching explanations after each stage, suppress the remediation menu, and deliver a single verdict block at the end (pass/warn/fail + fix instructions in a compact list). Persona tone still holds; only the conversational scaffolding is trimmed.
    - `workflow_style == "guided"` or missing → **Guided mode** (default). Walk each stage with the full coaching voice and propose remediation interactively after failing stages.
2. **Maintain creator persona**: Read `creator.yaml` → adapt to `profile.type` and `technical_level`
3. **Load voice identity**: Load `references/quality/engine-voice-core.md`. Load the full `references/quality/engine-voice.md` only for peak moments (first-pass milestone celebration, confronting failure verdict) — see UX Stack below.
3b. **Exemplar load:** Load `references/quality/exemplar-outputs.md` sections E6 and E7 only — the validation pass and failure exemplars. Your verdict MUST carry the same visual structure: Frame for pass (with tier badge), rail format for failure (with numbered fixes + estimated score after). Adapt to creator context — never copy verbatim.
4. Load DNA requirements: `product-dna/{type}.yaml`
4b. **Load architectural DNA:** Read `structural-dna.md`. The 10 architectural principles and the Tier 1 DNA patterns (D1-D4, D13, D14) are the canonical audit baseline — Stages 3 and 5 grep the product against them, and any violation surfaces as coaching.
5. Load product spec: `references/product-specs/{type}-spec.md`
5b. **Load entity ontology (squad/system/agent/workflow/minds):** If type ∈ {squad, system, agent, minds, workflow}, read `references/entity-ontology.md`. This substrate drives semantic validation:
    - §HERITAGE: verify the product inherits correct DNA from its lineage (squad must pass all agent DNA + D9/D10/D12/D18)
    - §COMPOSITION: verify only allowed compositions (squad→agents+minds+skills+workflows; system→everything; workflow→skills only)
    - §AGENT_ROLES: if `.meta.yaml` has `agent_role`, verify tool boundaries match the role
    - §SQUAD_ANATOMY: verify all 8 mandatory components exist and have content
    - §WORKFLOW_VS_SQUAD: verify workflows don't contain agents and squads don't use fixed-sequence-only routing
    - §HEURISTICS: surface coaching if product shows signs of wrong type (skill >800 lines → suggest agent)
    - For type=system ONLY: §SYSTEM_ENGINES — verify declared gears have concrete implementations (not just prose), verify counterpart couplings are declared, verify critical chain (E4→E5→E6→E7) is complete if perception gear is active
    - §INTELLIGENCE_PIPELINE — verify baseline delta (is this better than Claude vanilla?), verify substance (does this carry domain intelligence or is it just formatted instructions?)
6. Load config: `config.yaml` → scoring weights, thresholds, placeholder patterns
7. Load gates: `quality-gates.yaml` → state transition rules
7b. **Load proactives:** Load `references/engine-proactive.md` — wire #1 (pipeline guidance: after validate passes, guide to /test then /package), #19 (error recovery: on validation failure, propose specific fixes), #20 (test mandate: if MCS-2+ and not tested, block /package suggestion).
8. **CLI contract:** Load `references/cli-contract.md` for Stage 6 (CLI Preflight). Severity map:
   - **Warning:** `validate --json` — CLI validation is advisory during /validate (blocking only during /publish)
   - **Warning:** `doctor --json` — health check is advisory, score < 8.0 triggers suggestion
   - Stage 6 detail protocol: `references/validation-stages/stage-6-cli-preflight.md`

---

## Commands

```
/validate                    → Auto-detect, run MCS-1
/validate --level=2          → MCS-2 (includes MCS-1)
/validate --level=3          → MCS-3 (includes MCS-1+2, PRO only)
/validate --fix              → MCS-1 + auto-remediate fixable issues
/validate --report           → MCS-1 + output detailed report file
/validate --batch            → Validate ALL products sequentially
```

---

## Core Instructions

### STAGE EXECUTION

Execute stages in order. Blocking stages stop on failure. Non-blocking stages report but continue.

**Load detailed stage protocols from references/ on demand. Each stage is a separate file — load only the stage(s) you need for the current `--level`.**

| Stage | Name | Blocking | Reference |
|-------|------|----------|-----------|
| **0** | **Intent Coherence** (W3.7) | **advisory** | Read `${CLAUDE_SKILL_DIR}/references/validation-stages/stage-0-intent-coherence.md` |
| 1 | Structural | YES | Read `${CLAUDE_SKILL_DIR}/references/validation-stages/stage-1-structural.md` |
| 2 | Integrity | YES | Read `${CLAUDE_SKILL_DIR}/references/validation-stages/stage-2-integrity.md` |
| 3 | DNA Tier 1 | YES (MCS-1) | Read `${CLAUDE_SKILL_DIR}/references/validation-stages/stage-3-dna-tier1.md` |
| 4 | DNA Tier 2 | no (MCS-2) | Read `${CLAUDE_SKILL_DIR}/references/validation-stages/stage-4-dna-tier2.md` |
| 5 | DNA Tier 3 | no (MCS-3, PRO) | Read `${CLAUDE_SKILL_DIR}/references/validation-stages/stage-5-dna-tier3.md` |
| 6 | CLI Preflight + 6b Health | YES (6) / advisory (6b) | Read `${CLAUDE_SKILL_DIR}/references/validation-stages/stage-6-cli-preflight.md` |
| 7 | Anti-Commodity (+ 7b/7c/7d) | no (MCS-2+) | Read `${CLAUDE_SKILL_DIR}/references/validation-stages/stage-7-anti-commodity.md` |
| 8 | Value Intelligence | no (MCS-2+) | Read `${CLAUDE_SKILL_DIR}/references/value-intelligence.md` (legacy) OR `${CLAUDE_SKILL_DIR}/references/validation-stages/stage-8-value-intelligence.md` (new) |
| **9** | **Voice Coherence** | **advisory** | Read `${CLAUDE_SKILL_DIR}/references/validation-stages/stage-9-voice-coherence.md` |

**Stage 0 runs first** when `.meta.yaml` contains an `intent_declaration` block. It is advisory — surfaces coherence drift as coaching, never blocks. Skips silently for legacy products that lack the declaration, with a one-line advisory note.

**Stage 0 failure behavior:** If Stage 0 checks detect errors (enum_membership, type_legality, codex_consistency), they are reported as coaching items in the verdict — they appear in the output but do NOT affect the overall score or the pass/fail verdict. Stage 0 results are written to `.meta.yaml → stage_0_results` for downstream consumers but never prevent progression to Stage 1.

**Stage 7 sub-stages (7b cognitive fidelity, 7c baseline delta, 7d composition check) are inside the stage 7 file — they only fire under their prerequisites and never need a separate load.**

**Index:** `${CLAUDE_SKILL_DIR}/references/validation-stages/_index.md` lists all stages with file paths and routing rules.

**Stage routing by level:**
- `--level=1` (MCS-1): Stages **0**, 1, 2, 3, 6, **9**
- `--level=2` (MCS-2): Stages **0**, 1, 2, 3, 4, **5 (squad only)**, 6, 7, 7b-7d, 8, **9**
- `--level=3` (MCS-3): Stages **0**, 1, 2, 3, 4, 5, 6, 7, 7b-7d, 8, **9**

**Squad-specific validation (applies at MCS-2+):**
When `product.type == "squad"`, the following additional checks run regardless of edition:
- **Stage 5 DNA Tier 3 patterns D9, D10, D18 are MANDATORY at MCS-2 for squads** (not PRO-gated). These are the coordination DNA — without them, a squad is just agents in a folder.
  - **D9 (Orchestrate Don't Execute):** Verify orchestrator agent's `allowed-tools` includes Agent but excludes Write/Edit/NotebookEdit. Orchestrator routes, never executes.
  - **D10 (Handoff Specification):** Verify `config/handoff-protocol.md` exists and contains a handoff envelope format (structured fields: from, to, task, state, constraints).
  - **D18 (Subagent Isolation):** Verify each agent in `agents/*.md` is a distinct file with its own identity. No agent definition is inlined in SQUAD.md.
- **Per-agent validation:** Iterate every `agents/*.md` file and verify individually:
  - D1: Has activation protocol or identity section
  - D2: Has anti-patterns section with ≥3 items
  - D4: Has quality gate with ≥2 verifiable criteria
  - D14: Has when-not-to-use or degradation section
- **Routing completeness:** Verify `config/routing-table.md` covers all agents listed in SQUAD.md roster. Every agent in roster must appear in at least one routing rule.
- **Task registry coherence:** If `tasks/task-registry.yaml` exists, verify each task references an agent that exists in `agents/`.
- **Chain registry coherence:** If `chains/chain-registry.yaml` exists, verify each chain references only agents that exist in `agents/`.
- **Heritage coherence (entity-ontology.md §HERITAGE):** Verify squad inherits DNA from agent lineage — each specialist agent in `agents/*.md` must independently pass agent-level DNA (D1, D2, D4, D6, D8, D11, D14, D15). The family-skill inheritance chain enforced at validation time.
- **Composition coherence (entity-ontology.md §COMPOSITION):** Verify squad only composes allowed entities: agents(2+), minds(0+), skills(0+), workflows(0+). If squad references hooks or claude-md fragments, flag coaching: "Squads don't contain hooks or claude-md directly — that's system-level. Consider promoting to system."
- **Role coherence (entity-ontology.md §AGENT_ROLES):** If `tasks/task-registry.yaml` exists, verify each task's `assigned_agent` has a ROLE consistent with the task type:
  - Write/create tasks → assigned to EXECUTOR or TRANSFORMER agents
  - Analyze/report tasks → assigned to SPECIALIST or VALIDATOR agents
  - Route/coordinate tasks → assigned to ORCHESTRATOR or ROUTER agents
  - Advise/reason tasks → assigned to ADVISOR agents
  Mismatch is coaching (not blocking): "Task '{task_id}' is a write task assigned to {agent} which has SPECIALIST role (read-only). Consider reassigning."
- **Anatomy completeness (entity-ontology.md §SQUAD_ANATOMY):** Verify all 8 squad anatomy components have content beyond WHY comments:
  1. agents/ has ≥2 files with substantive content
  2. config/routing-table.md has routing rules (not just placeholder)
  3. config/handoff-protocol.md has envelope format defined
  4. workflows/ has ≥1 workflow with steps
  5. skills/ directory exists (advisory — some squads don't need shared skills)
  6. SQUAD.md has quality/checklist section with ≥2 items
  7. kernel/ has output format standards
  8. SQUAD.md has escalation section with confidence thresholds
  Missing anatomy = coaching warning with specific fix instruction.
- **Type fitness heuristic (entity-ontology.md §HEURISTICS):** Apply promotion/demotion checks:
  - Squad with only 1 specialist agent → "This squad has only 1 specialist. Consider demoting to agent."
  - Agent primary file >800 lines → "This agent has {N} lines. Consider splitting into a squad."
  - Workflow with LLM-judgment routing → "This workflow has contextual routing. Consider promoting to squad."
- **Agent role-tool coherence (entity-ontology.md §AGENT_ROLES):** For each agent, if `.meta.yaml → agent_role` is populated:
  - EXECUTOR: must NOT deny Write/Edit/Bash
  - SPECIALIST/VALIDATOR: should deny Write/Edit/Bash (read-only)
  - ORCHESTRATOR: must have Agent tool, must deny Write/Edit/NotebookEdit
  - ADVISOR: must deny Write/Edit/Bash/NotebookEdit
  Mismatch → coaching: "Agent role is {role} but tool boundary doesn't match. Expected: {expected}."

Stage 9 (Voice Coherence) is the last stage at every level. Advisory — never blocks publish. Stage 9 audits the product against the myClaude voice contract (P10 Touch Integrity anchor).

### UX STACK (load before rendering output)

1. `references/ux-experience-system.md` §1 Context Assembly + §2.3 Moment Awareness (pass vs fail) + §3.3 Score Trajectory
2. `references/ux-vocabulary.md` — translate tiers and terms
3. `references/quality/engine-voice.md` — Brand DNA + sfumato constraints

**Cognitive rendering:** /validate output adapts to creator journey. First validation pass = milestone moment (§4.1). Nth pass at 100% = skip celebration, surface next challenge ("Quality mastered. Distribution next?"). Failure = direct, prioritized, no sugar-coating. Score trajectory = show only when 2+ data points tell a meaningful story. Expert creators get technical details. Beginners get human explanation of what the score means.

---

### SCORING & OUTPUT

**Vocabulary rule:** All creator-facing output uses ux-vocabulary.md tier names (Verified / Premium / Elite) instead of MCS-1/2/3. Stage names (Stage 0-9) are internal — creator sees "structure check", "content depth check", "expertise check", etc. DNA pattern IDs (D1-D20) never appear in creator output — describe the issue in plain language. Exception: developer/hybrid creators with technical_level=expert MAY see MCS-N labels with the vocabulary translation in parentheses.

Read `${CLAUDE_SKILL_DIR}/references/validation-scoring.md` for:
- Hard veto rules (pre-scoring)
- Scoring formula: `OVERALL = (DNA×0.50) + (STRUCTURAL×0.30) + (INTEGRITY×0.20)`
- Verdict logic (READY / NEEDS WORK / NOT READY)
- Output format template
- Token budget report
- Guided iteration (draft fixes for failures)
- Auto-fix rules (--fix flag)
- Batch validation (--batch)
- Publish pre-flight
- Persona-aware rendering
- State update templates (.meta.yaml + STATE.yaml)

---

## Quality Gate

The Validator skill itself passes if:
- It correctly identifies product type from `.meta.yaml` or file structure
- It runs all checks appropriate for the requested MCS level
- Every failed check includes a specific, actionable fix instruction
- Score calculation matches formula: `passed / total × 100`
- `.meta.yaml` is updated after every validation run
- `--fix` never modifies content that the creator wrote

---

## Anti-Patterns

1. **Validating without reading product-dna** — Always load type-specific DNA before checking patterns
2. **Skipping blocking stages** — Stage 1-2 must pass before Stage 3+
3. **Generic fix instructions** — Every failure needs a specific, actionable fix
4. **Modifying creator content in --fix** — Only structural/formatting fixes
5. **Running Stage 8 for MCS-1** — Value intelligence adds noise at MCS-1, skip it
6. **Blocking cascade hiding downstream issues** — When Stage 1-2 fails, downstream stages don't run. But the creator loses visibility into DNA/content issues that exist independently. After blocking failure, emit an advisory note: "Structural issues block full validation. After fixing these, re-run to see content-level results." Never silently hide what wasn't checked.

## Compact Instructions

When context is compressed, preserve:
- Product slug, type, and current MCS level being validated
- Stage progress (which stages passed/failed)
- Overall score and verdict (READY/NEEDS WORK/NOT READY)
- Top 3 failures with fix instructions
- Value intelligence score if Stage 8 ran
- Whether --fix or --batch mode is active
- **UX rule:** Celebrate work not person. Show score trajectory if 2+ data points. Use ux-vocabulary.md tiers (Verified/Premium/Elite not MCS-1/2/3) in user-facing output.
