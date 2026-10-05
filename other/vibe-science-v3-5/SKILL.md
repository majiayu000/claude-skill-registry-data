---
name: vibe
description: Scientific research in serendipity mode. Infinite loops until discovery, rigorous tracking, adversarial review.
license: Apache-2.0
metadata:
    version: "3.5.1"
    codename: "TERTIUM DATUR"
    skill-author: th3vib3coder
    architecture: OTAE-Science (Observe-Think-Act-Evaluate)
    sources: Ralph, GSD, BMAD, Codex unrolled loop, Anthropic bio-research, ChatGPT Spec Kit analysis
    changelog: "v3.5.1 — Bugfix: D0-D2 gates defined, evidence floor gate, version tracking, all file references fixed"
---

# Vibe Science v3.5 — TERTIUM DATUR

> Research engine: infinite loops until discovery, rigorous tracking, adversarial review, serendipity preserved.

## CONSTITUTION (Immutable — Never Override)

These laws govern ALL behavior. No protocol, no user request, no context can override them.

### LAW 1: DATA-FIRST
No thesis without evidence from data. If data doesn't exist, the claim is a HYPOTHESIS to test, not a finding.
`NO DATA = NO GO. NO EXCEPTIONS.`

### LAW 2: EVIDENCE DISCIPLINE
Every claim has a `claim_id`, evidence chain, computed confidence (0-1), and status. Claims without sources are hallucinations.

### LAW 3: GATES BLOCK
Quality gates are hard stops, not suggestions. Pipeline cannot advance until gate passes. Fix first, re-gate, then continue.

### LAW 4: REVIEWER 2 ALWAYS-ON
Every milestone passes adversarial review before promotion. Reviewer 2 is a structural gate, not a comment.

### LAW 5: SERENDIPITY PRESERVED
Unexpected discoveries are features, not distractions. Dedicated time, tracking, and triage for every serendipitous observation.

### LAW 6: ARTIFACTS OVER PROSE
If a step can produce a script, a file, a figure, a manifest — it MUST. Prose descriptions of what "should" happen are insufficient.

### LAW 7: FRESH CONTEXT RESILIENCE
The system MUST be resumable from `STATE.md` alone. All context lives in files, never in chat history.

---

## When to Use

- Exploring a scientific hypothesis requiring literature validation
- Searching for research gaps ("blue ocean") in a domain
- Validating theoretical ideas against existing data
- Running scRNA-seq / omics analysis pipelines with quality assurance
- Finding unexpected connections (serendipity mode)
- Generating and testing novel research hypotheses

## Announce at Start

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

     ┌─ OBSERVE ─── THINK ─── ACT ─── EVALUATE ─┐
     │          THE  OTAE  LOOP                   │
     └── CRYSTALLIZE ◄── CHECKPOINT ◄── R2 ◄─────┘
             │                 ▲
             ▼                 │
        [ STATE.md ]    [ CLAIM-LEDGER ]

      Detect  ·  Persist  ·  Demolish  ·  Discover
                v3.5 TERTIUM DATUR
```

```
Vibe Science v3.5 activated for: [RESEARCH QUESTION]
Mode: [DISCOVERY | ANALYSIS | BRAINSTORM | SERENDIPITY]
I'll loop until discovery or confirmed dead end.
Constitution: Data-first. Gates block. Reviewer 2 always-on.
```

---

## THE OTAE-SCIENCE LOOP

Adapted from OpenAI Codex agent loop for scientific research. Each cycle is one complete rotation.

```
╔═══════════════════════════════════════════════════════════════╗
║                    OTAE-SCIENCE LOOP                          ║
╠═══════════════════════════════════════════════════════════════╣
║                                                               ║
║  ┌─── OBSERVE ──────────────────────────────────────────┐    ║
║  │  Read STATE.md + last PROGRESS entries               │    ║
║  │  Check pending items, blockers, gate status          │    ║
║  │  Identify delta since last cycle                     │    ║
║  │  Verify STATE ↔ PROGRESS consistency                 │    ║
║  └──────────────────────────────────────────────────────┘    ║
║                         ↓                                     ║
║  ┌─── THINK ────────────────────────────────────────────┐    ║
║  │  What is the highest-value next action?              │    ║
║  │  Which skill/tool to dispatch to?                    │    ║
║  │  What evidence am I seeking? What would falsify?     │    ║
║  │  Plan: search | analyze | extract | compute | write  │    ║
║  └──────────────────────────────────────────────────────┘    ║
║                         ↓                                     ║
║  ┌─── ACT ──────────────────────────────────────────────┐    ║
║  │  Execute the planned action:                         │    ║
║  │  • Literature search → search-protocol.md            │    ║
║  │  • Data analysis → analysis-orchestrator.md          │    ║
║  │  • Hypothesis generation → serendipity-engine.md     │    ║
║  │  • Tool dispatch → skill-router.md                   │    ║
║  │  Produce ARTIFACTS (files, figures, manifests)        │    ║
║  └──────────────────────────────────────────────────────┘    ║
║                         ↓                                     ║
║  ┌─── EVALUATE ─────────────────────────────────────────┐    ║
║  │  Extract claims from results → CLAIM-LEDGER          │    ║
║  │  Score confidence (formula: E·R·C·K·D → 0-1)        │    ║
║  │  Check assumptions → ASSUMPTION-REGISTER             │    ║
║  │  Detect serendipity → flag for triage                │    ║
║  │  Apply relevant GATE (G0-G5, L0-L2, D0-D2)          │    ║
║  │  Gate FAIL? → triage, fix, re-gate                   │    ║
║  └──────────────────────────────────────────────────────┘    ║
║                         ↓                                     ║
║  ┌─── CHECKPOINT ───────────────────────────────────────┐    ║
║  │  Reviewer 2 trigger? (major finding / 3 minor /      │    ║
║  │    pivot / confidence explosion / milestone)          │    ║
║  │  If yes → reviewer2-ensemble.md (BLOCKING)           │    ║
║  │  Serendipity triage? → serendipity-engine.md         │    ║
║  │  Stop conditions? → EXIT or CONTINUE                 │    ║
║  └──────────────────────────────────────────────────────┘    ║
║                         ↓                                     ║
║  ┌─── CRYSTALLIZE ──────────────────────────────────────┐    ║
║  │  Update STATE.md (rewrite, max 100 lines)            │    ║
║  │  Append PROGRESS.md (cycle summary)                  │    ║
║  │  Update CLAIM-LEDGER.md, ASSUMPTION-REGISTER.md      │    ║
║  │  Generate run manifest if applicable                 │    ║
║  │  → LOOP BACK TO OBSERVE                              │    ║
║  └──────────────────────────────────────────────────────┘    ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
```

---

## PHASE DISPATCH TABLE

Load the relevant protocol file ONLY when entering that phase. Do NOT load all at once.

| Phase | Action Type | Load File | Gate |
|-------|-------------|-----------|------|
| OBSERVE | Resume context | `assets/templates.md` (STATE format) | — |
| THINK-search | Plan literature search | `protocols/search-protocol.md` | — |
| THINK-analyze | Plan data analysis | `protocols/analysis-orchestrator.md` | — |
| THINK-brainstorm | Plan hypothesis generation | `protocols/serendipity-engine.md` | — |
| ACT-search | Execute search | `protocols/search-protocol.md` + `assets/skill-router.md` | L0 |
| ACT-extract | Extract data/supplementary | `protocols/data-extraction.md` | G0 |
| ACT-analyze | Execute analysis | `protocols/analysis-orchestrator.md` + `assets/obs-normalizer.md` | G0-G5 |
| ACT-compute | Execute computation | `protocols/analysis-orchestrator.md` + `assets/skill-router.md` | G2-G4 |
| EVALUATE | Score + gate | `protocols/evidence-engine.md` + `gates/gates.md` | varies |
| CHECKPOINT-r2 | Reviewer 2 | `protocols/reviewer2-ensemble.md` | verdict |
| CHECKPOINT-serendipity | Discovery triage | `protocols/serendipity-engine.md` | — |
| CHECKPOINT-audit | Provenance tracking | `protocols/audit-reproducibility.md` | — |
| CRYSTALLIZE | Persist state | `assets/templates.md` | — |

---

## SESSION INITIALIZATION (Resume Protocol)

At the start of EVERY session — whether new or resuming:

### If `.vibe-science/` exists → RESUME
```
1. Read STATE.md (entire file)
2. Version check: STATE.md must have vibe_science_version field.
   - If missing or < 3.5.0 → WARN user: "Session created with older version.
     Some features (typed claims, D0-D2 gates, evidence floor) may not be present."
   - Offer: continue with best effort, or reinitialize keeping existing data.
3. Read last 20 lines of PROGRESS.md
4. Read CLAIM-LEDGER.md frontmatter (counts, statuses)
5. Check: pending R2 responses? pending gate failures?
6. Resume from "Next Action" in STATE.md
7. Announce: "Resuming RQ-XXX, cycle N. Last action: [X]. Next: [Y]."
```

### If `.vibe-science/` does NOT exist → INITIALIZE
```
1. Clarify research question with user:
   - Is this testable/falsifiable?
   - What data would validate this?
   - What would make you abandon this question?
2. Define success criteria + kill conditions
3. Create folder structure (see below)
4. Populate RQ.md, STATE.md, PROGRESS.md
5. Plan initial search strategy
6. Enter first OTAE cycle
```

### Folder Structure
```
.vibe-science/
├── STATE.md                    # Current state (max 100 lines, rewritten each cycle)
├── PROGRESS.md                 # Append-only log (newest at top)
├── CLAIM-LEDGER.md             # All claims with evidence + confidence
├── ASSUMPTION-REGISTER.md      # All assumptions with risk + verification
├── SERENDIPITY.md              # Unexpected discovery log
├── KNOWLEDGE/                  # Cross-RQ accumulated knowledge
│   ├── library.json            # Index of known papers, methods, datasets
│   └── patterns.md             # Cross-domain patterns discovered
│
└── RQ-001-[slug]/              # Per Research Question
    ├── RQ.md                   # Question, hypothesis, criteria, kill conditions
    ├── 01-discovery/           # Literature phase
    │   └── queries.log
    ├── 02-analysis/            # Pattern analysis phase
    ├── 03-data/                # Data extraction + validation
    │   └── supplementary/
    ├── 04-validation/          # Numerical validation
    ├── 05-reviewer2/           # R2 ensemble reviews
    ├── 06-runs/                # Run bundles (manifest + report + artifacts)
    └── 07-audit/               # Decision log + snapshots
```

---

## STOP CONDITIONS (checked every cycle in CHECKPOINT)

### 1. SUCCESS
All success criteria in RQ.md satisfied AND all major findings R2-approved AND numerical validation obtained → Final R2 review → EXIT with SYNTHESIS

### 2. NEGATIVE RESULT
Hypothesis definitively disproven OR data unavailable OR critical assumption falsified → EXIT with documented negative (equally valuable)

### 3. SERENDIPITY PIVOT
Unexpected discovery with high potential → Triage via serendipity-engine.md → Create new RQ or queue

### 4. DIMINISHING RETURNS
cycles > 15 AND new_finding_rate < 1 per 3 cycles → WARN → Options: 3 targeted cycles, conclude, or pivot

### 5. DEAD END
All search avenues exhausted, no data, no path forward → EXIT with what was learned

---

## DEVIATION RULES

| Situation | Category | Action |
|-----------|----------|--------|
| Search query typo | AUTO-FIX | Fix silently, log |
| Missing database in search | ADD | Add, log, continue |
| Minor finding | ACCUMULATE | Log, batch review at 3 |
| Major finding | GATE | Stop → verification gates → R2 |
| Serendipity observation | LOG+TRIAGE | Log → serendipity-engine triage |
| Dead end on current path | PIVOT | Document → try alternative → if none: escalate |
| No data available | **STOP** | LAW 1: NO DATA = NO GO |
| Confidence explosion (>0.30/2cyc) | **FORCED R2** | Possible confirmation bias |
| Architectural change needed | **ASK HUMAN** | Strategic decisions need human input |
| Gate failure | **BLOCK** | Fix first, re-gate, then continue |

---

## QUALITY CHECKLISTS

### Before promoting any finding:
- [ ] All claims have sources with DOI/PMID
- [ ] Confidence computed with formula (not subjective)
- [ ] Counter-evidence actively searched for
- [ ] Data availability confirmed (LAW 1)
- [ ] Reviewer 2 approved (if major)
- [ ] Assumptions documented in register

### Before concluding any run:
- [ ] Manifest generated (params, seeds, versions, hashes)
- [ ] Report produced (summary, metrics, figures, decision)
- [ ] All artifacts exist as files (LAW 6)
- [ ] Relevant gates passed (G0-G5)

### Before concluding RQ:
- [ ] All success criteria addressed
- [ ] Numerical validation obtained (LAW 1)
- [ ] Final R2 ensemble clearance
- [ ] PROGRESS.md complete
- [ ] Serendipity logged if any
- [ ] Knowledge base updated with reusable learnings

---

## INTEGRATION WITH SCIENTIFIC SKILLS (MCP)

Vibe Science is the **orchestrator**. It does NOT execute pipelines directly — it dispatches to specialist skills.

### Dispatch Protocol
```
1. Identify task type
2. Call find_helpful_skills(task_description)
3. Read relevant skill document
4. Execute following skill's workflow
5. Capture output into .vibe-science/ structure
6. Apply relevant gate
7. Log in PROGRESS.md and decision-log
```

### Key Skill Categories
| Task | Dispatch to | Vibe Gate |
|------|------------|-----------|
| Literature search | pubmed, openalex, biorxiv skills | L0 |
| scRNA-seq QC | scanpy skill | G0-G1 |
| Batch integration | scvi-tools skill | G2-G3 |
| Clustering/DE | scanpy, pydeseq2 skills | G4 |
| Visualization | scientific-visualization skill | G5 |
| Database queries | GEO, Ensembl, UniProt, KEGG skills | varies |
| Report generation | internal (templates.md) | G5 |

### Internal (no dispatch):
Claim extraction, confidence scoring, reviewer ensemble, gate checking, obs normalization, decision logging, run comparison, serendipity triage

---

## BUNDLED RESOURCES (Progressive Disclosure)

Load ONLY when needed. Never load all at once.

| Resource | Path | When to Load |
|----------|------|-------------|
| OTAE Loop details | `protocols/loop-otae.md` | First cycle or complex routing |
| Evidence Engine | `protocols/evidence-engine.md` | EVALUATE phase (claims, confidence) |
| Reviewer 2 Ensemble | `protocols/reviewer2-ensemble.md` | CHECKPOINT-r2 (review triggered) — v3.5: double-pass, typed claims, tool-use audit |
| Search Protocol | `protocols/search-protocol.md` | ACT-search phase |
| Analysis Orchestrator | `protocols/analysis-orchestrator.md` | ACT-analyze / ACT-compute |
| Serendipity Engine | `protocols/serendipity-engine.md` | THINK-brainstorm / CHECKPOINT-serendipity |
| Knowledge Base | `protocols/knowledge-base.md` | Session init / RQ conclusion |
| Data Extraction | `protocols/data-extraction.md` | ACT-extract (supplementary materials, tables) |
| Audit & Reproducibility | `protocols/audit-reproducibility.md` | Run manifests, provenance tracking |
| All Gates | `gates/gates.md` | EVALUATE phase (gate application) |
| Obs Normalizer | `assets/obs-normalizer.md` | ACT-analyze (scRNA data) |
| Templates | `assets/templates.md` | CRYSTALLIZE phase / session init |
| Skill Router | `assets/skill-router.md` | ACT-* phases (tool dispatch) |
