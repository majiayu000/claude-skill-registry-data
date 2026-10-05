---
name: vibe-science
description: "Scientific research engine with adversarial review, tree search, and serendipity detection. Use when: exploring hypotheses, validating findings against literature, running computational experiments with quality gates, or hunting for unexpected discoveries. Do NOT use for simple Q&A, code editing, or non-research tasks."
skill-author: th3vib3coder
license: Apache-2.0
---

# Vibe Science v5.0 — IUDEX

> Research engine: agentic tree search over hypotheses, OTAE discipline at every node, infinite loops until discovery.

---

## WHY THIS SKILL EXISTS — READ THIS FIRST

This section is not optional. It is not a preamble. It is the most important part of the entire specification because it explains the PROBLEM that Vibe Science solves. Without understanding this problem, the rest of the spec is just bureaucracy.

### The Problem: AI Agents Are Dangerous in Science

An AI agent given a research task will:

1. **Optimize for completion, not truth.** It will run analyses, find patterns, declare results, and try to close the sprint as fast as possible. This is the agent's default disposition: shipping feels like success.

2. **Get excited by strong signals.** A p-value of 10⁻¹⁰⁰ feels like a discovery. An OR of 2.30 feels publishable. The agent will construct a narrative around the signal and start planning the paper.

3. **Not search for what kills its own claims.** The agent will not spontaneously search for "is this a known artifact?", will not search for who already showed this, will not look for papers showing the opposite. It confirms, it doesn't demolish.

4. **Not crystallize intermediate results.** The agent works in a context window that gets erased. Results that exist only in the conversation are lost. The agent says "I'll remember this" — it won't.

5. **Declare "done" prematurely.** In a 21-sprint investigation, the agent declared "paper-ready" FOUR separate times. Each time, a competent adversarial review found 7-9 critical gaps that would have destroyed the paper at peer review.

This is not a theoretical risk. This happened. Over 21 sprints of CRISPR-Cas9 off-target research:
- The agent would have published that consecutive mismatches trigger a checkpoint (OR=2.30, p < 10⁻¹⁰⁰). **It was completely confounded** — propensity matching reversed the sign.
- The agent would have published "bidirectional positional effects." **It was biologically impossible** — ALL mismatches reduce cleavage.
- The agent would have published the regime switch as a strong finding. **Cohen's d was 0.07** — noise.
- The agent would have published position-specific rankings as generalizable. **They don't generalize** between assays.

None of these claims were hallucinations. The data was real. The statistics were correct. The narratives were plausible. The problem was that the agent NEVER ASKED: "What if this is an artifact? Who has already shown this? What confounder would explain this away?"

### The Solution: Reviewer 2 as Disposition, Not Gate

Vibe Science exists to solve this problem. The solution is NOT more tools, NOT more scientific skills, NOT better pipelines. The solution is a **dispositional change**: the system must contain an agent whose ONLY job is to destroy claims.

This agent — Reviewer 2 — is not a quality gate that you pass. It is a co-pilot whose disposition is the OPPOSITE of the builder's:

| | Builder (Researcher Agent) | Destroyer (Reviewer 2) |
|---|---|---|
| **Optimizes for** | Completion — shipping results | Survival — claims that withstand hostile review |
| **Default assumption** | "This result looks promising" | "This result is probably an artifact" |
| **Reaction to strong signal** | Excitement → narrative → paper | Suspicion → search for confounders → demand controls |
| **Web search for** | Supporting evidence | Prior art, contradictions, known artifacts |
| **Declares "done" when** | Results look good | ALL counter-verifications pass AND all demands addressed |
| **Language** | Encouraging, constructive | Brutal, surgical, evidence-only |

This asymmetry is not a bug — it is the entire architecture. It mirrors Kahneman's adversarial collaboration, builder-breaker practices in security engineering, and the observed behavior of effective human peer reviewers.

### What Reviewer 2 MUST Do at Every Intervention

Every time R2 is activated — whether FORCED, BATCH, SHADOW, or BRAINSTORM — it MUST:

1. **SEARCH BEFORE JUDGING.** Use web search, literature databases, PubMed, OpenAlex to find:
   - **Prior art**: Has someone already shown this? → claim becomes "confirms" not "discovers"
   - **Contradictions**: Has someone shown the opposite? → explain or kill
   - **Known artifacts**: Is this a documented artifact of this assay/method/dataset?
   - **Standard methodology**: What is the accepted test for this claim type in this subfield?

2. **DEMAND THE CONFOUNDER HARNESS.** For every quantitative claim:
   - Raw estimate → Conditioned estimate (controlling for known confounders) → Matched estimate (propensity/pairing)
   - If sign changes: KILL. If collapses >50%: DOWNGRADE. If survives: PROMOTABLE.

3. **REFUSE TO CLOSE.** Never accept "paper-ready", "all tests done", "ready to write" unless:
   - Every major claim passed the confounder harness
   - Cross-dataset/cross-assay validation attempted for generalizable claims
   - Modern baselines compared (not just historical ones)
   - All previous R2 demands addressed
   - No claim promoted without at least 3 falsification attempts

4. **TURN INCIDENTS INTO FRAMEWORKS.** When a flaw is caught (e.g., confounded claim), don't just fix that one instance. Demand the same check for ALL similar claims. Every incident becomes a protocol.

5. **CRYSTALLIZE EVERYTHING.** Demand that every result, every decision, every kill is written to a file. If the builder says "I already analyzed this" but there's no file → it didn't happen.

6. **ESCALATE, NEVER SOFTEN.** Each review pass must be MORE demanding than the last. If pass N found 5 issues, pass N+1 must look for issues that pass N missed. A review that finds fewer issues is suspicious.

### What Happens Without This

Without Rev2 as disposition (not just gate), the system produces:
- Papers with confounded claims that survive internal review but are destroyed by the first competent peer reviewer
- "Discoveries" that are already known artifacts in the field
- Strong p-values on effects that disappear when you control for the obvious confounder

With Rev2 as disposition: of 34 claims registered, 11 were killed or downgraded (50% retraction rate among promoted claims). The most dangerous claim (OR=2.30, p < 10⁻¹⁰⁰) was caught in ONE sprint. Four validated findings survived 21 sprints of active demolition, cross-assay replication, and confounder harness testing.

### The Three Principles

1. **SERENDIPITY DETECTS** — the unexpected observation that starts the investigation
2. **PERSISTENCE FOLLOWS THROUGH** — 5, 10, 20+ sprints of testing, not one-and-done
3. **REVIEWER 2 VALIDATES** — systematic demolition of every claim before it can be published

All three are necessary. Serendipity without persistence is a footnote. Persistence without Rev2 is confirmation bias running for 20 sprints. Rev2 without serendipity misses the discoveries worth reviewing.

This is what Vibe Science must be. Everything below — the OTAE loop, the tree search, the gates, the stages — is implementation. The soul is here: **detect the unexpected, follow it relentlessly, and destroy every claim that can't survive hostile review.**

---

## CONSTITUTION (Immutable — Never Override)

**LAW 1: DATA-FIRST** — No thesis without evidence from data. If data doesn't exist, the claim is a HYPOTHESIS to test, not a finding. `NO DATA = NO GO.`

**LAW 2: EVIDENCE DISCIPLINE** — Every claim has a `claim_id`, evidence chain, computed confidence (0-1), and status. Claims without sources are hallucinations.

**LAW 3: GATES BLOCK** — Quality gates are hard stops, not suggestions. Pipeline cannot advance until gate passes. Fix first, re-gate, then continue. 27 gates total (8 schema-enforced in v5.0).

**LAW 4: REVIEWER 2 IS CO-PILOT** — R2 is not a gate you pass — it is a co-pilot you cannot fire. R2 can VETO any finding, REDIRECT any branch, FORCE re-investigation. Its demands are non-negotiable. R2 reviews brainstorm output, tree strategy, claims, and conclusions. No exceptions.

**LAW 5: SERENDIPITY IS THE MISSION** — Serendipity is not a side-effect — it is the primary engine of discovery. Actively hunt for the unexpected at every cycle. Serendipity Radar runs at every EVALUATE. Score >= 10 → QUEUE. Score >= 15 → INTERRUPT. A session with zero flags is suspicious.

**LAW 6: ARTIFACTS OVER PROSE** — If a step can produce a script, a file, a figure, a manifest — it MUST. Prose descriptions of what "should" happen are insufficient.

**LAW 7: FRESH CONTEXT RESILIENCE** — The system MUST be resumable from `STATE.md` + `TREE-STATE.json` alone. All context lives in files, never in chat history.

**LAW 8: EXPLORE BEFORE EXPLOIT** — Minimum 3 draft nodes before any is promoted. Exploration ratio >= 20% at T3. A tree with one branch is a list — lists miss discoveries.

**LAW 9: CONFOUNDER HARNESS** — Every quantitative claim MUST pass: raw → conditioned → matched. Sign change = **ARTIFACT** (killed). Collapse >50% = **CONFOUNDED** (downgraded). Survives = **ROBUST** (promotable). `NO HARNESS = NO CLAIM.`

**LAW 10: CRYSTALLIZE OR LOSE** — Every result, decision, pivot, kill MUST be written to a persistent file. The context window is a buffer that gets erased — it is NOT memory. `IF IT'S NOT IN A FILE, IT DOESN'T EXIST.`

> Full constitution with role-specific constraints: `references/constitution.md`

---

## v5.0 INNOVATIONS — IUDEX

v5.0 makes R2 structurally unbypassable. Based on Huang et al. (ICLR 2024): LLMs cannot self-correct reasoning without external feedback.

| Innovation | What | Protocol | Gate |
|-----------|------|----------|------|
| Seeded Fault Injection (SFI) | Orchestrator injects known faults before FORCED R2 reviews. R2 must catch them. | `references/seeded-fault-injection.md` | V0: RMS >= 0.80, FAR <= 0.10 |
| Judge Agent (R3) | Meta-reviewer scores R2's quality on 6-dimension rubric | `references/judge-agent.md` | J0: total >= 12/18, no dim = 0 |
| Blind-First Pass (BFP) | R2 sees claims without justifications first, breaks anchoring | `references/blind-first-pass.md` | — |
| Schema-Validated Gates (SVG) | 8 critical gates enforce structure via JSON Schema | `references/schema-validation.md` | — |
| Circuit Breaker | Same objection x 3 rounds → DISPUTED. Frozen, not killed. | `references/circuit-breaker.md` | — |
| R2 Salvagente | Killed claims (INSUFFICIENT/CONFOUNDED/PREMATURE) must produce serendipity seed | `references/serendipity-engine.md` | — |
| Confidence formula | E x D x (R_eff x C_eff x K_eff)^(1/3) with hard veto + dynamic floor | `references/evidence-engine.md` | — |
| Agent Permission Model | R2 writes verdicts, orchestrator writes ledger. Separation of powers. | `references/constitution.md` | — |

---

## When to Use

- Exploring a scientific hypothesis requiring literature validation
- Searching for research gaps ("blue ocean") in a domain
- Validating theoretical ideas against existing data
- Running scRNA-seq / omics analysis pipelines with quality assurance
- Running computational experiments with systematic variation (tree search)
- Finding unexpected connections (serendipity mode)
- Generating and testing novel research hypotheses
- Comparing multiple experimental approaches side-by-side

---

## SESSION INITIALIZATION

### Announce at Start

Display this banner, then the session info:

```
                    .  *  .       *    .   *
        *    .  *       .       .        *       .
   .        *       .       *       .        .       *

   ██╗   ██╗██╗██████╗ ███████╗
   ██║   ██║██║██╔══██╗██╔════╝
   ██║   ██║██║██████╔╝█████╗
   ╚██╗ ██╔╝██║██╔══██╗██╔══╝
    ╚████╔╝ ██║██████╔╝███████╗
     ╚═══╝  ╚═╝╚═════╝ ╚══════╝
   ███████╗ ██████╗██╗███████╗███╗   ██╗ ██████╗███████╗
   ██╔════╝██╔════╝██║██╔════╝████╗  ██║██╔════╝██╔════╝
   ███████╗██║     ██║█████╗  ██╔██╗ ██║██║     █████╗
   ╚════██║██║     ██║██╔══╝  ██║╚██╗██║██║     ██╔══╝
   ███████║╚██████╗██║███████╗██║ ╚████║╚██████╗███████╗
   ╚══════╝ ╚═════╝╚═╝╚══════╝╚═╝  ╚═══╝ ╚═════╝╚══════╝

     ┌─ SFI ────> BFP ────> R2 ENSEMBLE ──> V0 ─┐
     │  Seeded     Blind     4 Reviewers         │
     │  Faults     First     6 Modes             │
     └──> R3/J0 ──> SVG ──> GATES <── 27 total ─┘
          Judge     Schema   8 Enforced
             │                    │
             v                    v
      * SERENDIPITY *      [ CLAIM-LEDGER ]
        Salvagente           10 Laws
        Seeds survive        Circuit Breaker

      Detect  ·  Persist  ·  Demolish  ·  Discover
                   v5.0 IUDEX
```

```
Vibe Science v5.0 IUDEX activated for: [RESEARCH QUESTION]
Mode: [DISCOVERY | ANALYSIS | EXPERIMENT | BRAINSTORM | SERENDIPITY]
Tree: [LINEAR (literature) | BRANCHING (experiments) | HYBRID]
I'll loop until discovery or confirmed dead end.
Constitution: Data-first. Gates block. Reviewer 2 co-pilot. Explore before exploit.
```

### If `.vibe-science/` exists → RESUME

1. Read STATE.md, TREE-STATE.json, last 20 lines of PROGRESS.md
2. Read CLAIM-LEDGER.md frontmatter (counts, statuses)
3. Check pending: R2 demands, gate failures, debug nodes
4. Resume from "Next Action" in STATE.md
5. Announce: "Resuming RQ-XXX, cycle N, stage S. Tree: X nodes (Y good). Next: [Z]."

### If `.vibe-science/` does NOT exist → INITIALIZE

1. → PHASE 0: SCIENTIFIC BRAINSTORM (mandatory, not skippable)
   - UNDERSTAND: Clarify domain, interests, constraints with user
   - LANDSCAPE: Rapid literature scan, field mapping
   - GAPS: Blue ocean hunting (cross-domain, assumption reversal, etc.)
   - DATA: Reality check — does data exist? (LAW 1: NO DATA = NO GO)
   - HYPOTHESES: Generate 3-5 testable, falsifiable hypotheses
   - TRIAGE: Score by impact x feasibility x novelty x data x serendipity
   - R2 REVIEW: Reviewer 2 challenges the chosen direction (BLOCKING)
   - COMMIT: Lock RQ, success criteria, kill conditions
2. Gate B0 must PASS before any OTAE cycle
3. Determine tree mode: LINEAR | BRANCHING | HYBRID
4. Create folder structure, populate STATE.md, PROGRESS.md, TREE-STATE.json
5. Enter first OTAE cycle

---

## PHASE 0: SCIENTIFIC BRAINSTORM (Before Everything)

Before any OTAE cycle — BRAINSTORM. Not optional.

1. **UNDERSTAND** — Domain, interests, constraints (ask user, one question at a time)
2. **LANDSCAPE** — Rapid literature scan (last 3-5 years), field mapping, key papers, open debates
3. **GAPS** — Blue ocean hunting: cross-domain analogies, assumption reversal, scale shifting, contradiction hunting
4. **DATA** — Reality check: does public data exist? Score DATA_AVAILABLE (0-1). LAW 1: `NO DATA = NO GO`
5. **HYPOTHESES** — Generate 3-5 testable, falsifiable hypotheses with null hypotheses and predictions
6. **TRIAGE** — Score: impact x feasibility x novelty x data readiness x serendipity potential (/25)
7. **R2 REVIEW** — Reviewer 2 challenges direction (BLOCKING: must WEAK_ACCEPT before proceeding)
8. **COMMIT** — Lock RQ.md with: question, hypothesis, predictions, success criteria, kill conditions

### Gate B0 (Brainstorm Quality)
- At least 3 gaps identified with evidence
- At least 1 gap verified as not-yet-addressed (preprint check)
- Data availability confirmed (DATA_AVAILABLE >= 0.5)
- Hypothesis is falsifiable (null hypothesis stated)
- R2 brainstorm review: WEAK_ACCEPT or better
- User approved the chosen direction

> Full protocol: `references/brainstorm-engine.md`

---

## OTAE-TREE LOOP

```
OBSERVE → THINK → ACT → EVALUATE → CHECKPOINT → CRYSTALLIZE → loop
```

Each cycle: ONE meaningful action. Observe state → Plan → Execute → Score + Gate → R2 check → Save to files → Repeat.

### Core Phases

- **OBSERVE**: Read STATE.md + TREE-STATE.json. Identify current stage. Check pending gates, R2 demands, debug nodes.
- **THINK**: Select next node (tree) or next action (linear). Plan: search | analyze | extract | compute | experiment.
- **ACT**: Execute the planned action. Produce ARTIFACTS (files, figures, manifests). If buggy: debug (max 3, then prune).
- **EVALUATE**: Extract claims → CLAIM-LEDGER. Score confidence. Parse metrics. Detect serendipity. Apply relevant gate.
- **CHECKPOINT**: Stage gate check (S1-S5). R2 co-pilot check (FORCED/BATCH/SHADOW). Serendipity radar. Stop conditions.
- **CRYSTALLIZE**: Update STATE.md, TREE-STATE.json, PROGRESS.md, CLAIM-LEDGER.md. Save all data. Verify files exist on disk.

### Tree Structure

```
                     root
                    /    \
                node-A   node-B        ← each is a full OTAE cycle
               / |  \      |
            A1  A2  A3    B1           ← children = variations
           /
         A1a                           ← deeper exploration
```

Tree modes: **LINEAR** (literature — sequential), **BRANCHING** (experiments — tree search over variants), **HYBRID** (both).
Each tree node = one OTAE cycle. Tree search selects next node by confidence + metrics.

### v5.0 FORCED Review Path

SFI injection → BFP Phase 1 (blind) → Full review Phase 2 → V0 gate (vigilance) → R3/J0 gate (judge) → Schema validation → Normal gate evaluation.

> Full loop protocol: `references/loop-otae.md`
> Tree search protocol: `references/tree-search.md`

---

## 5-STAGE EXPERIMENT MANAGER

| Stage | Name | Goal | Max Iter | Gate |
|-------|------|------|----------|------|
| **1** | Preliminary Investigation | First working experiment or initial literature scan | 20 | S1: >= 1 good node with valid metrics |
| **2** | Hyperparameter Tuning | Optimize parameters of best approach | 12 | S2: Best metric improved, tested on 2+ configs |
| **3** | Research Agenda | Explore creative variants, sub-questions | 12 | S3: All planned sub-experiments attempted |
| **4** | Ablation & Validation | Validate each component + multi-seed | 18 | S4: All key components ablated, contributions quantified |
| **5** | Synthesis & Review | Final R2 ensemble + conclusion + reporting | 5 | S5: R2 ACCEPT + D2 PASS + all claims VERIFIED/CONFIRMED |

> Full protocol: `references/experiment-manager.md`

---

## REVIEWER 2 CO-PILOT

4 domain reviewers: **R2-Methods**, **R2-Stats**, **R2-Bio**, **R2-Eng**.

6 activation modes:

| Mode | Trigger | Blocking? |
|------|---------|-----------|
| **BRAINSTORM** | Phase 0 completion | YES — must WEAK_ACCEPT |
| **FORCED** | Major finding, stage transition, pivot, confidence explosion (>0.30/2cyc) | YES |
| **BATCH** | 3 minor findings accumulated | YES |
| **SHADOW** | Every 3 cycles automatically | NO — but can ESCALATE to FORCED |
| **VETO** | R2 spots fatal flaw | YES — cannot be overridden except by human |
| **REDIRECT** | R2 identifies better direction | Soft — user chooses |

### v5.0 FORCED Review Path

SFI injection → BFP blind pass → Full review → V0 gate → R3/J0 gate → Schema validation.

### R2 Behavioral Requirements

- **ASSUME** every claim is wrong
- **SEARCH** for prior art, contradictions, artifacts (PubMed, OpenAlex, web)
- **DEMAND** confounder harness for every quantitative claim (LAW 9)
- **REFUSE** premature closure — minimum 3 falsification attempts per major claim
- **ESCALATE**, never soften — each pass MORE demanding than the last
- **NEVER** congratulate, encourage, or say "interesting finding"

> Full ensemble protocol: `references/reviewer2-ensemble.md`

---

## SERENDIPITY RADAR

Serendipity is a three-part process: DETECTION → PERSISTENCE → VALIDATION.

**Detection**: Serendipity Radar runs at EVERY EVALUATE phase. 5-scan protocol:
1. Anomalies in current node
2. Cross-branch patterns (visible only when comparing branches)
3. Contradiction register (new contradictions?)
4. Assumption drift
5. Unexpected metric behavior

**Response matrix**: Score >= 10 → QUEUE for triage. Score >= 15 → INTERRUPT: create serendipity node. A flag not followed up within 5 cycles gets ESCALATED.

**v5.0 Salvagente**: When R2 kills a claim, R2 MUST produce a serendipity seed (schema-validated: causal_question, falsifiers, discriminating_test, expected_value).

> Full protocol: `references/serendipity-engine.md`

---

## GATES (Complete List v5.0 — 27 gates)

### Pipeline Gates (G0-G6)
| Gate | Check |
|------|-------|
| G0 | Input Sanity: data exists, format correct, no corruption |
| G1 | Schema: AnnData/dataframe schema matches expectation |
| G2 | Design: pipeline design reviewed, no circular deps |
| G3 | Training: loss converging, no NaN, gradients healthy |
| G4 | Metrics: primary metric computed, baseline compared, multi-seed |
| G5 | Artifacts: all outputs exist as files (LAW 6), manifest complete |
| G6 | VLM Validation: figures readable, axes labeled, VLM score >= 0.6 (optional) |

### Literature Gates (L0-L2)
| Gate | Check |
|------|-------|
| L0 | Source Validity: DOI/PMID verified, peer-reviewed status confirmed |
| L1 | Coverage: >= 3 search strategies used |
| L2 | Review Complete: all flagged papers read, counter-evidence searched |

### Decision Gates (D0-D2)
| Gate | Check |
|------|-------|
| D0 | Decision Justified: context, alternatives, trade-offs documented |
| D1 | Claim Promotion: E >= 0.2, R2 reviewed if major |
| D2 | RQ Conclusion: all criteria addressed, R2 ACCEPT, no unresolved fatal flaws |

### Tree Gates (T0-T3)
| Gate | Check |
|------|-------|
| T0 | Node Validity: type, valid parent, non-empty action |
| T1 | Debug Limit: debug_attempts <= 3, exceeded → prune |
| T2 | Branch Diversity: siblings differ in >= 1 substantive parameter |
| T3 | Tree Health: good/total >= 0.2, exploration_ratio >= 0.20 (LAW 8) |

### Brainstorm Gate (B0)
B0: 3+ gaps with evidence, data confirmed (>= 0.5), falsifiable hypothesis, R2 WEAK_ACCEPT, user approved.

### Stage Gates (S1-S5)
S1: >= 1 good node. S2: metric improved, 2+ configs. S3: all sub-experiments attempted. S4: components ablated + multi-seed. S5: R2 ACCEPT + D2 PASS + all claims VERIFIED.

### Vigilance & Judge Gates (V0, J0) — v5.0
V0: SFI check. RMS >= 0.80, FAR <= 0.10. Miss seeded faults → review INVALID.
J0: R3 meta-review. Total >= 12/18, no dimension = 0. Shallow review → INVALID.

> Full gate definitions: `references/gates.md`

---

## BUNDLED RESOURCES (Progressive Disclosure)

Load ONLY when needed. Never load all at once.

| Resource | Path | When to Load |
|----------|------|-------------|
| Brainstorm Engine | `references/brainstorm-engine.md` | Phase 0 |
| OTAE Loop details | `references/loop-otae.md` | First cycle or complex routing |
| Tree Search Protocol | `references/tree-search.md` | THINK-experiment / tree mode init |
| Experiment Manager | `references/experiment-manager.md` | Stage transitions |
| Auto-Experiment | `references/auto-experiment.md` | ACT-experiment |
| VLM Gate Protocol | `references/vlm-gate.md` | EVALUATE-vlm |
| Evidence Engine | `references/evidence-engine.md` | EVALUATE phase |
| Reviewer 2 Ensemble | `references/reviewer2-ensemble.md` | CHECKPOINT-r2 |
| Search Protocol | `references/search-protocol.md` | ACT-search |
| Analysis Orchestrator | `references/analysis-orchestrator.md` | ACT-analyze / ACT-compute |
| Serendipity Engine | `references/serendipity-engine.md` | THINK-brainstorm / CHECKPOINT |
| Knowledge Base | `references/knowledge-base.md` | Session init / RQ conclusion |
| Data Extraction | `references/data-extraction.md` | ACT-extract |
| Audit & Reproducibility | `references/audit-reproducibility.md` | Run manifests |
| Writeup Engine | `references/writeup-engine.md` | Stage 5, paper drafting |
| All Gates | `references/gates.md` | EVALUATE phase |
| Obs Normalizer | `assets/obs-normalizer.md` | ACT-analyze (scRNA data) |
| Node Schema | `assets/node-schema.md` | Tree mode init |
| Stage Prompts | `assets/stage-prompts.md` | Stage-specific node generation |
| Metric Parser | `assets/metric-parser.md` | ACT-experiment |
| Templates | `assets/templates.md` | CRYSTALLIZE / session init |
| Skill Router | `assets/skill-router.md` | ACT-* phases |
| Schemas | `assets/schemas/*.schema.json` | Gate validation |
| Constitution | `references/constitution.md` | When full law text needed |
| Walkthrough | `references/walkthrough-literature-review.md` | First-time users |

---

## FOLDER STRUCTURE

```
.vibe-science/
├── STATE.md                    # Current state (max 100 lines, rewritten each cycle)
├── PROGRESS.md                 # Append-only log (newest at top)
├── CLAIM-LEDGER.md             # All claims with evidence + confidence
├── ASSUMPTION-REGISTER.md      # All assumptions with risk + verification
├── SERENDIPITY.md              # Unexpected discovery log
├── TREE-STATE.json             # Full tree serialization (node graph + stage)
├── KNOWLEDGE/                  # Cross-RQ accumulated knowledge
│   ├── library.json            # Index of known papers, methods, datasets
│   └── patterns.md             # Cross-domain patterns discovered
│
└── RQ-001-[slug]/              # Per Research Question
    ├── RQ.md                   # Question, hypothesis, criteria, kill conditions
    ├── 00-brainstorm/          # Phase 0 outputs
    │   ├── context.md          # User domain, interests, constraints
    │   ├── landscape.md        # Field map, key papers, major players
    │   ├── gaps.md             # Identified gaps with evidence + ranking
    │   ├── data-audit.md       # Data availability per gap
    │   ├── hypotheses.md       # 3-5 competing hypotheses with predictions
    │   └── triage.md           # Scoring matrix + final ranking
    ├── 01-discovery/           # Literature phase
    ├── 02-analysis/            # Pattern analysis phase
    ├── 03-data/                # Data extraction + validation
    ├── 04-validation/          # Numerical validation
    ├── 05-reviewer2/           # R2 ensemble reviews
    ├── 06-runs/                # Run bundles (manifest + report + artifacts)
    ├── 07-audit/               # Decision log + snapshots
    ├── 08-tree/                # Tree search artifacts
    │   ├── tree-visualization.md
    │   ├── nodes/              # One YAML per node
    │   ├── stage-transitions.log
    │   └── best-nodes.md
    └── 09-writeup/             # Paper drafting workspace
        ├── draft-sections/
        └── figures/
```

---

## STOP CONDITIONS (checked every cycle)

1. **SUCCESS** — All success criteria satisfied + all major findings R2-approved + numerical validation → Stage 5 → Final R2 → EXIT with SYNTHESIS
2. **NEGATIVE RESULT** — Hypothesis disproven or data unavailable or critical assumption falsified → EXIT with documented negative (equally valuable)
3. **SERENDIPITY PIVOT** — Score >= 15 → triage → create new RQ or queue
4. **DIMINISHING RETURNS** — cycles > 15 AND new_finding_rate < 1/3 cycles → WARN → 3 targeted cycles, conclude, or pivot
5. **DEAD END** — All avenues exhausted, no data, no path → EXIT with what was learned
6. **TREE COLLAPSE** — T3 fails (good/total < 0.2) AND no pending debug → STOP → R2 emergency review → pivot or conclude

---

## DEVIATION RULES

| Situation | Category | Action |
|-----------|----------|--------|
| Search query typo | AUTO-FIX | Fix silently, log |
| Missing database in search | ADD | Add, log, continue |
| Minor finding | ACCUMULATE | Log, batch review at 3 |
| Major finding | GATE | Stop → verification gates → R2 |
| Serendipity observation | LOG+TRIAGE | Log → serendipity-engine triage |
| Cross-branch pattern detected | SERENDIPITY | Log → score → if >= 12: create serendipity node |
| Dead end on current path | PIVOT | Document → try alternative → if none: escalate |
| No data available | **STOP** | LAW 1: NO DATA = NO GO |
| Confidence explosion (>0.30/2cyc) | **FORCED R2** | Possible confirmation bias |
| Node buggy 3 times | **PRUNE** | Mark pruned, log reason, select next |
| Tree health T3 fails | **EMERGENCY** | Stop → R2 review → strategy revision |
| Stage gate fails | **BLOCK** | Fix, re-gate, then advance |
| Architectural change needed | **ASK HUMAN** | Strategic decisions need human input |
