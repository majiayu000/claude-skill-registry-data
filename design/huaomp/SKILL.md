---
name: huaomp
description: Maximum epistemic breadth -- 6 analytical lenses (Holistic, Universal, Absolute, Omni, Meta, Paradigmatic) for intent-to-spec generation and scope expansion.
version: 0.1.0
execution-mode: advisory
argument-hint: "<spec \"intent\" | holistic | universal | absolute | omni | meta | paradigmatic | full | off>"
category: fleet-ops
status: candidate
providers:
  required: [python]
---
# HUAOMP -- Maximum Epistemic Breadth

Six analytical lenses that sweep from concrete to abstract, surfacing blind spots and generating structured specifications from raw intent.

## Usage

```bash
[huaomp] spec "I want agents to coordinate without a central bus"
[huaomp] full "should we migrate from SQLite to Postgres?"
[huaomp] holistic "notification system for multi-agent platform"
[huaomp] meta "why do our tests keep getting flaky?"
```

## Task

$ARGUMENTS

## The Six Lenses (H-U-A-O-M-P)

| Lens | Core Move | Questions It Forces |
|------|-----------|-------------------|
| **H**olistic | Trace feedback loops, find leverage points | What's connected? Second-order effects? Where's the highest leverage? |
| **U**niversal | Extract context-free invariants | What's true regardless of context? Has this been solved in another domain? What composes? |
| **A**bsolute | Draw hard boundaries | What's physically impossible? What must NEVER happen? What must EVENTUALLY happen? |
| **O**mni | Rotate through all perspectives | All stakeholders? All timescales? All failure modes? What does the attacker see? |
| **M**eta | Step up one abstraction level | What kind of problem IS this? Are we solving the right problem? Is there a strange loop? |
| **P**aradigmatic | Name the paradigm, imagine alternatives | What paradigm are we in? What anomalies are we ignoring? What would make this approach obsolete? |

## Execution

### Mode: `spec` (Intent-to-Spec Pipeline)

Run all 6 lenses sequentially against raw user intent. Output a structured specification.

1. State the raw intent verbatim
2. For each lens H → U → A → O → M → P:
   - Apply the lens questions to the intent
   - Surface 1-3 findings (not philosophy -- concrete observations)
   - Emit a `Spec constraint` for each finding
3. Synthesize into a Generated Spec with:
   - Numbered constraints from all lenses
   - Open questions requiring human judgment
   - Base120 models activated (cite codes)
4. If the codebase has `agent_intent.py`, map output to AgentSpecification fields:
   - Holistic findings → `design.architecture`
   - Universal findings → `design.components` (composable pieces)
   - Absolute findings → `acceptance_criteria`
   - Omni findings → stakeholder list, threat surface
   - Meta findings → `reasoning.alternatives_considered`, ADR
   - Paradigmatic findings → `reasoning.chosen_approach`, `reasoning.mental_models`

### Mode: Single Lens (`holistic`, `universal`, `absolute`, `omni`, `meta`, `paradigmatic`)

Apply one lens deeply. Use when you know which angle is missing.

1. State the problem
2. Apply the lens's 3-5 core questions
3. Map to relevant Base120 models
4. Output: Findings, Blind spots caught, Spec constraints

### Mode: `full`

Apply all 6 lenses but produce a compressed summary (not full spec format). Use for quick epistemic sweep before a decision.

### Mode: `off`

Clear HUAOMP analytical context. Return to default mode.

## Base120 Model Mapping

| Lens | Primary Models |
|------|---------------|
| H | SY1 (Leverage Points), RE2 (Feedback Loops), SY6 (Feedback Structure Mapping) |
| U | SY1 (Leverage Points), CO2 (Chunking), CO9 (Interface Contracts) |
| A | P1 (First Principles), IN7 (Boundary Testing), DE13 (FMEA) |
| O | P2 (Stakeholder Mapping), P7 (Perspective Switching), IN10 (Red Teaming) |
| M | P4 (Lens Shifting), P10 (Context Windowing), RE2 (Feedback Loops) |
| P | P15 (Assumption Surfacing), IN1 (Subtractive Thinking), IN3 (Problem Reversal) |

## Output Format

### Spec Mode
```
HUAOMP Spec | "<intent>"
═══════════════════════════════════

Intent: <raw intent verbatim>

── H (Holistic) ──────────────────
<findings>
▸ Spec constraint: <concrete constraint>

── U (Universal) ──────────────────
<findings>
▸ Spec constraint: <concrete constraint>

── A (Absolute) ──────────────────
<findings>
▸ Spec constraint: <concrete constraint>

── O (Omni) ───────────────────────
<findings>
▸ Spec constraint: <concrete constraint>

── M (Meta) ───────────────────────
<findings>
▸ Spec constraint: <concrete constraint>

── P (Paradigmatic) ───────────────
<findings>
▸ Spec constraint: <concrete constraint>

── Generated Spec ─────────────────
1. <constraint>
2. <constraint>
...
Open questions: <items requiring human judgment>
Base120 models activated: <codes>
```

### Single Lens / Full Mode
```
HUAOMP | <lens> | "<problem>"
═══════════════════════════════════

Findings:
  1. <concrete observation>
  2. <concrete observation>

Blind spots caught:
  - <what you'd miss without this lens>

Base120: <relevant model codes>

Spec constraints:
  - <actionable constraint>
```

## Integration

- **/brainstorm**: Run `[huaomp] full` before Phase 1 to expand the option space
- **/apex**: HUAOMP provides the scope; MTSMU provides the rigor
- **/base120**: HUAOMP activates specific Base120 models per lens; `[base120] apply` goes deeper on any one
- **/threat-model**: The Omni lens (adversarial perspective) feeds directly into STRIDE analysis
- **agent_intent.py**: Spec mode output maps to AgentSpecification fields

## Constraints

- Do NOT produce philosophy. Every lens must yield concrete findings and spec constraints.
- Do NOT force all 6 lenses when fewer suffice. If a lens adds nothing, say "No additional constraints from this lens."
- Do NOT fabricate Base120 model codes. Use only official codes from the Base120 reference.
- Keep each lens section to 3-8 lines. Brevity is a feature.
- The spec is a DRAFT for human review, not a final document. Flag uncertainty explicitly.
