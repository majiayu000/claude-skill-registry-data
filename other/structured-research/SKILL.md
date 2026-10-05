---
name: structured-research
description: Standalone skill for validating an explicit assumption with structured research. Use when a user holds a belief that is still an assumption — a technical claim, a library's behavior, a "this is probably how X works" — and wants it investigated methodically before it leaks into planning or code. Recommends a research methodology (non-binding) and returns an evidence-backed, graded verdict (Confirmed / Refuted / Inconclusive). Trigger on "structured-research", "validate this assumption", "is it true that", "research whether", "verify my assumption", "check this claim", "I assume X — is that right?". Standalone like bug-hunting / hotfix / brand-design — no pipeline required.
---

# Structured Research

Validate an explicit assumption against evidence before it becomes a planning input. Take the "thing the user still treats as an assumption", frame it as a falsifiable question, research it with a chosen methodology, and return a **graded, evidence-backed verdict** with a **non-binding recommendation** the maintainer may adopt, adapt, or replace.

**Core principle:** An assumption is not evidence. Evidence is not a verdict. A verdict is advisory, not a decree.

**Violating the letter of this process is violating the spirit of structured research.**

## When to Use

Trigger when:
- A belief is still an assumption — "I think X works this way", "this library probably supports Y", "Z is the fast path"
- An assumption is about to enter planning/development unvalidated and the cost of being wrong is real
- The user says "validate this", "is it true that…", "research whether…", "verify my assumption"

Do NOT use:
- To generate or explore ideas (→ `pocket-pitching` / `pocket-grinding` — those diverge, this validates)
- To fix a known defect (→ `bug-hunting`)
- When the claim is already settled and just needs implementing (→ `hotfix`)

## Boundary with pitching / grinding

| structured-research | pocket-pitching / pocket-grinding |
|---------------------|-----------------------------------|
| Tests whether a stated assumption holds | Generates and explores ideas |
| Convergent — narrows to a verdict | Divergent — widens the option space |
| Output: graded verdict + evidence | Output: directions / spec |
| Single explicit assumption in | Vague problem in |

## The Three Iron Laws

```
LAW 1: NO VERDICT WITHOUT EVIDENCE
       A graded conclusion must cite the sources/observations behind it.

LAW 2: SEEK REFUTATION, NOT JUST CONFIRMATION
       At least one selected method must actively try to disprove the assumption.

LAW 3: THE VERDICT IS ADVISORY
       Output a recommendation, never a mandate. The maintainer decides.
```

## Hard Gates

```
GATE 0: PREFLIGHT MUST COMPLETE BEFORE GREETING.
        Scan project context silently. No output until greeting.

GATE 1: NO RESEARCH without a confirmed, operationalized assumption.
        Phase 1 ends with the user confirming the restated, falsifiable question.
        Silence or vague approval is not confirmation.

GATE 2: AT LEAST ONE REFUTATION METHOD selected (Law 2).
        A research run that only seeks confirmation is invalid.

GATE 3: CURATION GATE before grading.
        After evidence is gathered, run the curation pass (advisor) — see Phase 4.
        Do not grade straight from raw evidence.

GATE 4: VERDICT MUST BE GRADED + ADVISORY.
        Confirmed / Refuted / Inconclusive, with cited evidence, framed non-binding.
```

---

## Phase 0: Preflight

**Goal:** Understand context silently before greeting.

**Scan (silent — no output yet):**
- Stack: detect from root files (package.json, Cargo.toml, requirements.txt, go.mod, pom.xml)
- Whether the assumption touches a library/API present in the project (so a code/version check is possible)
- Recent commits: `git log --oneline -10` (the assumption may already be answered in history)

**Then greet:**
```
Project: [name] · Stack: [detected]
What assumption would you like to validate?
```

---

## Phase 1: Assumption Intake

**Goal:** Turn a fuzzy belief into one confirmed, falsifiable question.

**Process:**
1. User states the assumption.
2. Operationalize it — restate as a precise, testable claim (use the `Operationalization` method from the catalog). Strip vague terms; name the measurable condition.
3. Confirm:
   ```
   Assumption under test: [precise, falsifiable restatement]
   What would make it FALSE: [the disconfirming observation]
   Is this the right question before I research?
   ```

**Rules:**
- Max 2 clarifying questions. This is intake, not interrogation.
- If the assumption bundles several claims, ask which ONE to validate this session (one assumption per run).

**HARD GATE:** User must explicitly confirm the restatement. Do not proceed on silence.

---

## Phase 2: Method Selection

**Goal:** Recommend 1–3 research methods (non-binding) for this assumption.

**→ Read `references/research-methods.csv`** — the methodology catalog (`category,technique_name,description`).

**Selection heuristic (lean — no separate selection doc):**
- **Always include ≥1 `adversarial` method** (Falsification, Counterexample Hunt, Pre-Mortem…) — satisfies Law 2 / Gate 2.
- Pick the evidence-gathering method that fits the claim's *type*:
  - Library/API/version behavior → `empirical` (Technical Spike, Reproduction Test) + `triangulation` (Documentation vs Reality Check).
  - Factual/published claim → `triangulation` (Source Triangulation, Citation Chaining).
  - Open-ended / "what are the possibilities" → `elicitation` (Verbalized Sampling to surface a distribution of candidate truths with likelihoods, then narrow).
  - Reasoning/causal claim → `analytical` (First-Principles Decomposition, Five Whys).
- For a calibrated final confidence, optionally add a `probabilistic` method (Bayesian Updating).
- 1 method if the claim is simple; 3 max — past 3, synthesis blurs.

**State the recommendation (non-binding):**
```
Recommended methods (you may pick, drop, or combine):
1. [Method] ([category]) — because [1-line reason]
2. [Method] ([category]) — because [reason]   ← refutation method (required)
```
Let the user adjust before gathering evidence.

---

## Phase 3: Evidence Gathering

**Goal:** Apply the selected methods and collect cited evidence.

- Use the right tool per method: **Context7** (library docs / API behavior — preferred for any library claim), **Tavily / WebSearch** (published facts, recency), **code scan / Technical Spike** (project-internal or reproducible behavior).
- For each method, record: what was checked, what was found, and the **source** (URL, doc, file:line, or spike output). No source → not evidence (Law 1).
- Run the refutation method honestly — go looking for the disconfirming case, not around it.
- One unknown blocking the rest? Resolve it with a focused spike before continuing.

Output evidence to the conversation, grouped by method, **before** the curation gate.

---

## Phase 4: Curation Gate

**Goal:** Pressure-test the evidence before grading. (GATE 3)

After ALL evidence is output, run a curation pass with `advisor()` — it reads the full conversation (evidence included) and returns: which evidence is strong vs weak, contradictions, and what is still missing.

**Fallback (advisor unavailable — e.g. Claude Code without the Pi extension):** do the curation pass inline as the main agent — re-read every piece of evidence adversarially, list the strongest support, the strongest counter-evidence, and any gap — and say explicitly that the inline fallback was used. The gate is never skipped; only its executor changes.

---

## Phase 5: Graded Verdict + Recommendation

**Goal:** A graded, evidence-backed, advisory conclusion.

**→ Load `references/verdict-format.md`** for the grading rubric and report template.

**Present:**
```
## Verdict: [Confirmed | Refuted | Inconclusive]   (confidence: [low/medium/high])

Assumption tested: [the operationalized question]

Why: [2-4 sentences tying the verdict to the cited evidence]

Key evidence:
- [finding] — [source]
- [counter-evidence, if any] — [source]

Recommendation (non-binding): [what the maintainer might do — adopt / adapt / investigate further]
What would change this verdict: [the evidence that would flip it]
```

**Save report to:**
```
docs/pocket/research/YYYY-MM-DD-kebab-slug/research-report.md
```

**Handoff (explicit, advisory):**
```
Research report written to: docs/pocket/research/[path]

This verdict is advisory. What next?
  1. Adopt the recommendation as-is
  2. Validate a related assumption (new run)
  3. Carry this into pocket-grinding / pocket-planning as a confirmed input
  4. Save and stop here
```

---

## Reference Triggers

| Reference | When to Load |
|-----------|--------------|
| `references/research-methods.csv` | Phase 2: read to recommend methods |
| `references/verdict-format.md` | Phase 5: grading rubric + report template |
