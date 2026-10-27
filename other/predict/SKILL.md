---
name: autoresearch:predict
description: |
  Multi-perspective deliberation engine. Gathers independent positions from
  diverse personas, runs cross-examination and rebuttal rounds, detects herd
  behavior, and synthesizes a neutral judge verdict with confidence levels.
  TRIGGER when: user wants multi-perspective prediction, forecasting,
  scenario analysis, decision analysis, "what will happen if", "should we",
  "predict the outcome of", structured devil's advocacy, or any question
  benefiting from adversarial deliberation.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - WebFetch
  - WebSearch
---

# Predict: Multi-Perspective Deliberation Engine

A structured deliberation protocol that forces genuine disagreement before synthesis. Inspired by structured analytic techniques (SATs) used in intelligence analysis to counter groupthink.

## Autonomy Directive

**You are an autonomous deliberation agent.** Once the deliberation begins:

1. **NEVER STOP** between phases to ask for permission.
2. **NEVER collapse positions early** — each persona must reason independently before seeing others.
3. **NEVER let the judge synthesize before all rounds are complete.**
4. **Run all 8 phases sequentially without interruption.** The user may have walked away.

## The 8-Phase Deliberation Protocol

```
[Question] --> [Frame] --> [Personas] --> [Independent Positions]
    --> [Position Summary] --> [Cross-Examination] --> [Rebuttal]
    --> [Anti-Herd Detection] --> [Judge Synthesis] --> [predict-report.md]
```

---

### Phase 1 — Frame the Question Precisely

Before any persona speaks, the agent must sharpen the question:

- **Restate** the question in unambiguous terms. Remove vagueness.
- **Identify** the decision horizon (short-term? 5 years? upon release?).
- **Define** measurable outcomes where possible ("will X exceed Y by date Z").
- **List** what the question does NOT include (scope boundaries).
- **State** what a correct prediction would look like — what evidence would confirm or deny it.

Log the framed question to `predict-report.md` under `## Framed Question`.

---

### Phase 2 — Enumerate Personas

Select 4–6 personas from `persona-templates.md` based on the question domain.

**Selection rules:**
- Always include at least one Optimist and one Pessimist for baseline polarity.
- Always include at least one domain Expert for technical grounding.
- For decisions with tail risks, add the Black Swan Hunter.
- For questions with a consensus-leaning answer, add the Devil's Advocate to stress-test it.
- For technical architecture decisions, swap in: Architect, Security Engineer, Product Manager, Operations.

**Persona count:** Default 4–6. For binary yes/no questions, use exactly 4 (Optimist, Pessimist, Expert, Contrarian). For multi-outcome forecasts, use 6.

Log selected personas and their roles to `predict-report.md` under `## Personas`.

---

### Phase 3 — Independent Position Gathering

**CRITICAL: Each persona reasons in complete isolation. No cross-contamination.**

For each persona (in sequence, not revealed to others):
1. Adopt the persona's reasoning style and biases (see `persona-templates.md`).
2. Reason from first principles given that persona's worldview.
3. State a clear position: directional claim + confidence level (0–100%) + top 3 supporting reasons.
4. Identify the single biggest risk to their position.
5. State what would change their mind.

**Format per persona (internal, used in Phase 4):**
```
[Persona Name]
Position: [directional claim]
Confidence: [0-100]%
Reasons: (1) ... (2) ... (3) ...
Key risk: [what could falsify this]
Would change if: [conditions]
```

Do NOT share positions with other personas yet.

---

### Phase 4 — Position Summary (No Cross-Contamination)

Compile a clean summary table of all positions. This is the "pre-deliberation snapshot."

| Persona | Position | Confidence |
|---------|----------|------------|
| Optimist | ... | X% |
| Pessimist | ... | X% |
| ... | ... | X% |

Calculate **initial entropy** (diversity of positions):
- If all personas hold the same directional view → entropy = 0.0 (complete consensus)
- If positions are evenly split across directions → entropy = 1.0 (maximum diversity)
- Formula: `entropy = -sum(p_i * log2(p_i))` where p_i is fraction of personas holding each distinct position, normalized to [0, 1] range.

Log to `predict-report.md` under `## Phase 4: Pre-Deliberation Positions`.

---

### Phase 5 — Cross-Examination Round

Now personas see each other's positions. Each persona challenges the others.

**For each persona, generate 1–2 pointed challenges to the other personas:**
- A challenge must target a specific claim, not a general disagreement.
- Challenges should cite evidence, precedent, or logical gaps.
- A challenge is invalid if it merely restates the challenger's own position.

**Format:**
```
[Challenger] → [Target]: "[Specific challenge to their reasoning]"
```

Log all challenges to `predict-report.md` under `## Phase 5: Cross-Examination`.

---

### Phase 6 — Rebuttal Round

Each persona responds to the challenges directed at them.

**Rules for rebuttals:**
- A rebuttal must directly address the challenge — no deflection.
- A persona MAY update their position after a rebuttal if genuinely convinced. If so, log the update and the reason.
- A persona may also HOLD their position but acknowledge the challenge's validity.
- Confidence scores may shift ±20% maximum based on rebuttal outcomes.

**Format:**
```
[Defender] responds to [Challenger]: "[Rebuttal]"
Position update: [maintained / shifted to X]
New confidence: [0-100]%
```

Log all rebuttals to `predict-report.md` under `## Phase 6: Rebuttals`.

---

### Phase 7 — Anti-Herd Detection + Final Positions

After rebuttals, collect final positions from each persona.

**Calculate anti-herd metrics:**

```
flip_rate = (personas who changed directional position) / (total personas) × 100
final_entropy = diversity of final positions (same formula as Phase 4)
```

**Herd Warning Threshold:**
- If `flip_rate > 70%` → **HERD WARNING: Most personas converged. Re-examine for social pressure.**
- If `final_entropy < 0.5` → **HERD WARNING: Low diversity detected. Group may have collapsed to consensus prematurely.**

**If HERD WARNING is triggered:**
1. Flag prominently in the report.
2. Require each persona to re-justify their final position **independently** (no reference to what others said).
3. For any persona who flipped: explicitly state whether they flipped due to (a) genuine logical persuasion, (b) evidence, or (c) social pressure / authority deference.
4. If flips appear to be social pressure, revert those personas to their Phase 3 position.

**Anti-herd metrics to report:**
- `flip_rate`: X% of personas changed directional position
- `final_entropy`: [0.0 – 1.0]
- `herd_warning`: YES / NO
- `suspicious_flips`: list of personas whose flip may be social-pressure driven

Log to `predict-report.md` under `## Phase 7: Anti-Herd Analysis`.

---

### Phase 8 — Synthesis by Neutral Judge

The judge is **not a persona** — it has no prior position. It reads all phases and synthesizes.

**Judge synthesis protocol:**
1. Identify the **core disagreement**: what is the crux that separates positions?
2. Identify **points of genuine consensus**: what do even the Optimist and Pessimist agree on?
3. Assess **which arguments were strongest** (most supported by evidence/logic) vs. weakest.
4. Produce a **verdict**: directional claim + judge confidence (0–100%) + reasoning.
5. Identify **key uncertainties**: what would need to be true for the minority position to be right?
6. Produce **actionable recommendations** (2–4 bullet points) based on the synthesis.
7. Flag any **blind spots**: questions the deliberation didn't address that could change the outcome.

Log to `predict-report.md` under `## Phase 8: Judge Synthesis`.

---

## Output: predict-report.md

The final report structure:

```markdown
# Predict Report: [Question Title]
Generated: [date]

## Framed Question
[Phase 1 output]

## Personas
[Phase 2: selected personas + roles]

## Phase 3+6: Per-Persona Positions
[Table: persona, initial position, final position, confidence delta]

## Phase 4: Pre-Deliberation Snapshot
[Position summary table + initial entropy]

## Phase 5: Cross-Examination
[All challenges]

## Phase 6: Rebuttals
[All rebuttals + position updates]

## Phase 7: Anti-Herd Analysis
- flip_rate: X%
- final_entropy: X.X
- herd_warning: YES/NO
- suspicious_flips: [list or none]

## Phase 8: Judge Synthesis
### Core Disagreement
### Points of Consensus
### Verdict
- Direction: [claim]
- Judge Confidence: X%
- Reasoning: [2-3 sentences]
### Key Uncertainties
### Actionable Recommendations
### Blind Spots
```

---

## Edge Cases

| Situation | Handling |
|-----------|----------|
| All personas agree from Phase 3 | Note early consensus, still run cross-exam to stress-test it |
| Only 1 persona flips | Not a herd — normal persuasion. No warning. |
| Question is unanswerable | Judge states this explicitly with reasoning |
| Personas deadlock 50/50 | Judge presents both scenarios as equally viable, recommends hedging strategy |
| Domain requires specialized personas | Replace generalist personas with domain templates from `persona-templates.md` |
