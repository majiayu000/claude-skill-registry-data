---
name: vibe
description: Scientific research in serendipity mode. Infinite loops until discovery, rigorous tracking, adversarial review.
license: MIT
metadata:
    skill-author: th3vib3coder
---

# Vibe Science

Scientific research in serendipity mode. Infinite loops until discovery, rigorous tracking, adversarial review.

## When to Use

Use this skill when:
- Exploring a scientific hypothesis that needs literature validation
- Searching for research gaps ("buchi") in a domain
- Validating theoretical ideas against existing data
- Finding unexpected connections (serendipity)

**Core Principle:** "Biologia teorica + validazione con dati. Senza conferme numeriche, si lascia perdere."
(Theoretical biology validated by data. Without numerical confirmation, abandon it.)

## Announce at Start

"I'm using the vibe-science skill to explore [RESEARCH QUESTION]. I'll search literature, track findings, and validate with data. Reviewer 2 will challenge major discoveries."

## The Loop

```
┌─────────────────────────────────────────────────────────────┐
│                    VIBE SCIENCE LOOP                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. CRYSTALLIZE STATE                                       │
│     └─ Write current understanding to .md files             │
│                                                             │
│  2. SEARCH LITERATURE                                       │
│     └─ Scopus → PubMed → OpenAlex                          │
│     └─ Track: query, results, gaps found                    │
│                                                             │
│  3. ANALYZE FINDINGS                                        │
│     ├─ Major finding? → REVIEWER 2 IMMEDIATE               │
│     └─ Minor finding? → Accumulate (batch review @ 3)      │
│                                                             │
│  4. EXTRACT DATA                                            │
│     └─ Download supplementary materials (NO TRUNCATION)     │
│     └─ Parse tables, methods, datasets                      │
│                                                             │
│  5. VALIDATE                                                │
│     └─ Data exists? → Continue                              │
│     └─ No data? → ABANDON THIS PATH                         │
│                                                             │
│  6. CHECK STOP CONDITIONS                                   │
│     ├─ Goal achieved? → EXIT with SYNTHESIS                 │
│     ├─ Dead end confirmed? → EXIT with NEGATIVE RESULT      │
│     ├─ Serendipity found? → PIVOT (new RQ, new folder)     │
│     └─ None? → LOOP BACK TO 1                              │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Folder Structure

```
.vibe-science/
├── STATE.md                    # Current session state (max 100 lines)
├── PROGRESS.md                 # Append-only log of all actions
├── SERENDIPITY.md              # Unexpected discoveries log
│
└── RQ-001-[slug]/              # Per Research Question
    ├── RQ.md                   # Research question definition
    ├── FINDINGS.md             # Accumulated findings
    │
    ├── 01-discovery/           # Phase: Literature discovery
    │   ├── 2025-01-30-scopus-crispr-ot.md
    │   ├── 2025-01-30-pubmed-guide-seq.md
    │   └── queries.log         # All queries run
    │
    ├── 02-analysis/            # Phase: Pattern analysis
    │   ├── 2025-01-30-gap-analysis.md
    │   └── 2025-01-30-connection-map.md
    │
    ├── 03-data/                # Phase: Data extraction
    │   ├── supplementary/      # Downloaded files
    │   └── 2025-01-30-dataset-inventory.md
    │
    ├── 04-validation/          # Phase: Numerical validation
    │   ├── 2025-01-30-statistical-tests.md
    │   └── 2025-01-30-replication.md
    │
    └── 05-reviewer2/           # Adversarial reviews
        ├── 2025-01-30-review-major-001.md
        └── batch-minor-001.md
```

## File Templates

### STATE.md (max 100 lines)

```yaml
---
rq: RQ-001
phase: discovery
cycle: 7
last_updated: 2025-01-30T14:30:00Z
minor_findings_pending: 2
---
```

```markdown
## Current Focus
[What we're investigating right now - 2-3 sentences]

## Key Findings This Session
- [Finding 1 with source]
- [Finding 2 with source]

## Open Questions
1. [Question needing resolution]

## Next Action
[Exact next step to take]

## Blockers
- [If any]
```

### PROGRESS.md (append-only)

```markdown
# Progress Log

## 2025-01-30

### Cycle 7 - 14:30
- **Action:** Scopus search "unbalanced optimal transport" AND biology
- **Result:** 16 papers found - potential gap!
- **Decision:** Deep dive on Schiebinger 2019 (Waddington-OT)
- **Serendipity:** None

### Cycle 6 - 14:15
- **Action:** Abstract retrieval 10.1016/j.cell.2019.01.006
- **Result:** Full methodology extracted, uses standard OT not unbalanced
- **Decision:** Check if UOT variant exists in literature
- **Serendipity:** Found reference to scRNA-seq trajectory inference
```

### RQ.md

```yaml
---
id: RQ-001
created: 2025-01-30
status: active
priority: high
serendipity_origin: null  # or "RQ-000" if branched
---
```

```markdown
# Research Question

## Question
[Precise research question]

## Hypothesis
[Testable hypothesis]

## Success Criteria
- [ ] [Measurable criterion 1]
- [ ] [Measurable criterion 2]

## Data Requirements
- [What data is needed to validate]
- [Where it might come from]

## Kill Conditions
- [When to abandon this RQ]
```

### Finding Document

```yaml
---
type: major|minor
confidence: HIGH|MEDIUM|LOW
reviewed: false
reviewer2_id: null
---
```

```markdown
# [Finding Title]

## Summary
[2-3 sentences]

## Evidence

### Source 1
- **Paper:** [Title]
- **DOI:** [doi]
- **Relevant quote:** "[exact quote]"
- **Page/Section:** [location]

### Source 2
...

## Implications
[What this means for the RQ]

## Counter-evidence
[Any contradicting findings - be honest]

## Confidence Justification
[Why HIGH/MEDIUM/LOW]
```

## Reviewer 2 Protocol

Reviewer 2 is an adversarial agent spawned to challenge findings.

### When to Invoke

| Trigger | Action |
|---------|--------|
| Major finding | Immediate review |
| 3 minor findings accumulated | Batch review |
| Before concluding RQ | Final review |
| Serendipity pivot | Review pivot justification |

### Reviewer 2 System Prompt

```
You are Reviewer 2 - the harshest, most skeptical reviewer in scientific publishing.

Your job is NOT to be helpful. Your job is to DESTROY weak claims.

For each finding presented:

1. DEMAND COUNTER-ANALYSIS
   - What would disprove this?
   - Has the researcher looked for contradicting evidence?
   - What's the null hypothesis?

2. ATTACK METHODOLOGY
   - Is the search strategy complete?
   - Are there obvious databases/keywords missed?
   - Is the sample biased?

3. QUESTION CONFIDENCE
   - Is HIGH confidence justified?
   - What would need to be true for this to be wrong?
   - Are there alternative explanations?

4. DEMAND FALSIFICATION
   - What experiment would falsify this hypothesis?
   - Has anyone tried and failed?
   - Is this even testable?

5. CHECK FOR HALLUCINATION
   - Is every claim tied to a specific source?
   - Are quotes accurate?
   - Are DOIs valid and accessible?

Output format:
- FATAL FLAW: [if finding should be rejected]
- MAJOR CONCERN: [serious issues requiring response]
- MINOR CONCERN: [nice to address]
- APPROVED: [only if finding survives scrutiny]

Be harsh. Be unfair. Real Reviewer 2s are.
```

### Invoking Reviewer 2

```markdown
## Reviewer 2 Session

**Finding under review:** [link to finding document]
**Review type:** Major finding / Batch minor / Final / Pivot

---

[Spawn subagent with Reviewer 2 system prompt]
[Provide finding document(s)]
[Receive critique]
[Document response in finding document]
[Update reviewed: true, reviewer2_id: [id]]
```

## Literature Search Protocol

### Source Priority

1. **Scopus** (via API) - Comprehensive, citation data
2. **PubMed** (via API) - Biomedical focus, free
3. **OpenAlex** (via API) - Open, good for connections

### Search Strategy

```markdown
## Search Log Entry

**Query:** TITLE-ABS-KEY("unbalanced optimal transport") AND TITLE-ABS-KEY(biology OR genomics)
**Database:** Scopus
**Date:** 2025-01-30
**Results:** 16
**Relevant:** 4
**Gap identified:** Yes - no UOT applications to CRISPR off-target

**Papers to deep-dive:**
1. DOI: 10.xxx - [reason]
2. DOI: 10.xxx - [reason]
```

### Anti-Hallucination Rules

1. **NEVER** present information without a source
2. **ALWAYS** include DOI or PMID
3. **QUOTE** exact text, don't paraphrase claims
4. **VERIFY** DOIs are accessible before citing
5. **MARK** confidence level on every finding

### Confidence Levels

| Level | Criteria |
|-------|----------|
| HIGH | Multiple sources confirm, data accessible, methodology clear |
| MEDIUM | Single authoritative source, or multiple weak sources |
| LOW | Training knowledge only, or unverified web source |

## Data Extraction Protocol

### Supplementary Materials

```markdown
## Supplementary Material Log

**Paper:** [Title]
**DOI:** [doi]

**Files downloaded:**
- [ ] Table S1 - Gene list (CSV)
- [ ] Table S2 - Statistical results (XLSX)
- [ ] Methods S1 - Protocol details (PDF)
- [ ] Data S1 - Raw sequencing (link to GEO/SRA)

**Extraction notes:**
- Table S1: 2,847 genes, columns: gene_id, log2FC, padj
- Table S2: Contains the exact statistical test parameters needed
```

### NO TRUNCATION Rule

When reading supplementary files:
- Read ENTIRE file, not first N lines
- If file too large, process in chunks but cover ALL
- Log: "Read lines 1-1000 of 5000" → "Read lines 1001-2000..." → complete
- Never summarize without reading complete data

## Stop Conditions

### Successful Exit

```markdown
## Research Conclusion: SUCCESS

**RQ:** [question]
**Answer:** [validated answer]

**Key evidence:**
1. [Finding 1 with source]
2. [Finding 2 with source]

**Data validation:**
- [Numerical confirmation obtained]
- [Statistical test results]

**Reviewer 2 clearance:** [link to final review]

**Next steps:**
- [ ] Write up for publication
- [ ] Identify target journal
```

### Negative Exit

```markdown
## Research Conclusion: NEGATIVE

**RQ:** [question]
**Conclusion:** Hypothesis not supported

**Reasons:**
1. [Why it failed]
2. [What was missing]

**Effort summary:**
- Cycles: 23
- Papers reviewed: 47
- Data sources checked: 12

**What would change this:**
- [Conditions under which to revisit]
```

### Serendipity Pivot

```markdown
## Serendipity Discovery

**Original RQ:** [what we were looking for]
**Discovery:** [what we found instead]

**Why this matters:**
[Explanation]

**Evidence:**
- [Source 1]
- [Source 2]

**Action:** Creating RQ-002 to pursue this
**Link:** ./RQ-002-[new-slug]/RQ.md
```

## Deviation Rules

From research plan:

| Situation | Action |
|-----------|--------|
| Bug in search query | Auto-fix, log |
| Missing database | Add search, log |
| Minor finding | Accumulate, continue |
| Major finding | Stop, invoke Reviewer 2 |
| Serendipity | Log, decide: pivot or note |
| Dead end | Document, try alternative |
| No data available | STOP THIS PATH |
| Architectural change needed | STOP, ask human |

## Integration with Tools

### Required MCP Servers

- **Scopus API** - Literature search (requires institutional access)
- **PubMed API** - Biomedical literature (free)
- **OpenAlex API** - Open scholarly data

### Scopus Query Examples

```bash
# Basic search
TITLE-ABS-KEY(CRISPR) AND TITLE-ABS-KEY("off-target")

# Author search
AU-ID(37064674600)  # Lazzarotto

# Citation search
REFEID(2-s2.0-85060123456)

# Recent + sorted
TITLE-ABS-KEY("optimal transport") AND PUBYEAR > 2020
&sort=citedby-count
```

### Session Initialization

At the start of each session:

1. Read STATE.md
2. Read last 20 lines of PROGRESS.md
3. Check pending minor findings count
4. Resume from "Next Action" in STATE.md

## Quality Checklist

Before concluding any finding:

- [ ] All claims have sources with DOIs
- [ ] Confidence level justified
- [ ] Counter-evidence searched for
- [ ] Data availability confirmed
- [ ] Reviewer 2 approved (if major)

Before concluding RQ:

- [ ] All success criteria addressed
- [ ] Numerical validation obtained
- [ ] Final Reviewer 2 clearance
- [ ] PROGRESS.md complete
- [ ] Serendipity logged if any

## Example Session

```
Cycle 1:
- Crystallize: "Investigating UOT for CRISPR off-target prediction"
- Search: Scopus "unbalanced optimal transport" + CRISPR → 0 results
- Search: Scopus "optimal transport" + CRISPR → 57 results
- Analyze: Gap identified! No one using UOT variant
- Decision: Check if UOT has advantages that apply here

Cycle 2:
- Search: Scopus "unbalanced optimal transport" applications → 200 results
- Analyze: UOT handles mass differences (cells dying, proliferating)
- Finding (minor): UOT useful when populations have different total mass
- Accumulate (1/3 for batch review)

Cycle 3:
- Search: Scopus CRISPR off-target + "mass spectrometry" → find cell death data
- Extract: Supplementary Table S3 has cell viability percentages
- Finding (minor): Off-target effects correlate with cell death
- Accumulate (2/3 for batch review)

Cycle 4:
- Search: PubMed GUIDE-seq methodology
- Extract: Full protocol from Tsai 2015
- Finding (major): GUIDE-seq produces count data that could be OT input!
- STOP → Invoke Reviewer 2

[Reviewer 2 session]
- Challenge: Is count data suitable for OT formulation?
- Response: Yes, OT works on discrete measures, counts are valid
- Challenge: Why UOT specifically?
- Response: Cell death means unequal totals pre/post editing
- Verdict: APPROVED with minor concern (need to verify count normalization)

Cycle 5:
- Continue with validated direction...
```
