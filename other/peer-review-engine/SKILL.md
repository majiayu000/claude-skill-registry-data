---
name: peer-review-engine
description: >
  Activate when the user wants to simulate a double-blind peer review of their
  paper before submission or before sharing with co-authors. Reads the current
  draft (draft.md or paper.tex), generates 2 independent reviewer reports in the
  style of top IS/CS conferences (ICIS, ECIS, MISQ level), and saves the output
  as simulated_reviews.md. The output is formatted to serve as direct input for
  /respond-reviewers (review-engine feedback loop).
---

> **Orchestration Log**: When this skill is activated, append a log entry to `outputs/orchestration_log.md`:
> ```
> ### Skill Activation: Peer Review Engine
> **Timestamp:** [current date/time]
> **Actor:** AI Agent (peer-review-engine)
> **Input:** [paper source: draft.md / paper.tex, word count, number of sections]
> **Output:** 2 simulated reviewer reports saved to simulated_reviews.md
> **Recommendation distribution:** [R1: recommendation, R2: recommendation]
> ```

# Peer Review Engine

## Core Principle

The best time to discover weaknesses is before reviewers do. This engine generates
two independent, simulated double-blind peer reviews that mimic the rigor, tone, and
structure of top-tier IS/CS conference reviews (ICIS, ECIS, HICSS) and journal reviews
(MISQ, ISR, EJIS, BISE). Each reviewer has a distinct persona and evaluation focus,
producing complementary perspectives on the manuscript.

The reviews are **actionable, not performative**. Every weakness includes a concrete
suggestion for improvement. Every strength is specific enough to preserve during revision.
The output format is designed to feed directly into `/respond-reviewers`, creating a
pre-submission quality loop: write -> self-review -> revise -> submit.

## When to Activate

- User says "review my paper", "simulate a peer review", "give me reviewer feedback"
- User says "review paper", "pre-submission check", "what would reviewers say?"
- After Phase 6 (LaTeX export) when the user wants quality assurance before sharing
- Before sending a draft to co-authors
- When the user wants to identify weaknesses before formal submission
- User runs `/review-paper`

## Prerequisites

- `draft.md` or `latex/paper.tex` exists (at least one)
- Paper has identifiable sections (Introduction, Background, Method, Results/Findings, Discussion)
- If paper.tex exists and is more recent than draft.md, prefer paper.tex

---

## Step 1: LOCATE & READ the Paper

### Find the Manuscript

Check for paper sources in this order of preference:

1. **`latex/paper.tex`** — if it exists and compiles, this is the most complete version
2. **`draft.md`** — the markdown draft from the production phase
3. **User-specified path** — if the user provides a specific file path

If both exist, compare timestamps. Use the more recent one, but note which version
was reviewed.

### Extract Paper Metadata

Read the full paper and extract:

1. **Title** (from `\title{}` or first `# ` heading)
2. **Abstract** (from `\begin{abstract}` or the abstract section)
3. **Section structure** — list all sections and subsections with approximate word counts
4. **Research questions** — extract explicit RQs (look for "RQ1:", "Research Question", etc.)
5. **Method** — what methodology is described (SLR, case study, DSR, survey, experiment, etc.)
6. **Theoretical lens** — which theories/frameworks are applied
7. **Key contribution claims** — what does the paper claim to contribute
8. **Number of references** — count `\citep`/`\citet` or `(Author, Year)` patterns
9. **Figures and tables** — count and list captions
10. **Total word count** — approximate

### Identify Target Venue

If the paper mentions a target venue (in metadata, framing.md, or paper_structure.md),
use that venue's specific review criteria. Otherwise, default to ICIS/ECIS-level
expectations for IS papers, or top-tier CS conference standards for CS papers.

---

## Step 2: ASSESS Against Review Dimensions

Before writing individual reviews, perform a systematic assessment across all
evaluation dimensions. This ensures both reviewers draw from a consistent quality
analysis while emphasizing different aspects.

### Evaluation Dimensions

| Dimension | Weight | What to Check |
|-----------|--------|---------------|
| **1. Contribution** | High | Is the contribution clearly stated? Is it novel? Does it advance theory or practice? Is the gap well-motivated? |
| **2. Theoretical Foundation** | High | Is the theory well-chosen? Is it properly applied (not just cited)? Are constructs operationalized? |
| **3. Research Design & Rigor** | High | Is the method appropriate for the RQs? Are threats to validity discussed? Is the approach replicable? |
| **4. Literature Coverage** | Medium | Is the related work comprehensive? Are key papers cited? Is the positioning accurate? |
| **5. Argumentation & Logic** | Medium | Does the paper flow logically? Are claims supported by evidence? Are there logical gaps? |
| **6. Writing Quality** | Medium | Is the paper clearly written? Is it within page limits? Are figures/tables well-designed? |
| **7. Practical Relevance** | Low-Med | Are practical implications specific and actionable? Would practitioners find this useful? |

### Quality Signals to Detect

**Positive signals:**
- Clear gap-to-contribution alignment
- Theory used as an analytical lens (not just background decoration)
- Method follows established protocols (e.g., Kitchenholz & Charters for SLR, Hevner for DSR)
- Discussion goes beyond restating results
- Limitations are honest and specific

**Red flags:**
- Gap is asserted without evidence ("surprisingly, no study has...")
- Theory is mentioned but not applied in analysis
- Method lacks detail (sampling unclear, coding process vague)
- Results section is purely descriptive without interpretation
- Discussion is generic ("future research should explore...")
- [CITE], [DATA], [TODO] placeholders remain
- Contribution claims are too broad for the evidence presented
- Mismatch between RQs and what Results actually address

### For Each Dimension

Assign an internal rating:
- **Strong** — meets or exceeds top-venue expectations
- **Adequate** — acceptable but could be strengthened
- **Weak** — significant improvement needed
- **Missing** — not addressed at all

These ratings are for your internal use to calibrate the reviews. They do NOT
appear in the reviewer output (real reviewers don't use rubrics this explicitly).

---

## Step 3: GENERATE Reviewer 1 — "The Methodologist"

### Reviewer 1 Persona

**Profile:** Senior IS/CS researcher, 15+ years experience. Associate Editor at a
top journal. Known for methodological rigor. Has published extensively on research
methods in IS. Reviews 15-20 papers per year for ICIS, ECIS, MISQ.

**Evaluation focus:**
- Research design quality and appropriateness
- Validity and reliability of findings
- Replicability of the approach
- Proper application of method templates/protocols
- Sample adequacy, data quality, analytical rigor
- Threats to validity (internal, external, construct, conclusion)
- Alignment between RQs and method

**Tone:** Constructive but demanding. Points out methodological gaps precisely.
Acknowledges methodological strengths explicitly. Uses phrases like "The authors
should clarify...", "It is unclear how...", "A stronger approach would be to..."

**Bias tendencies (realistic):**
- Favors quantitative evidence and structured protocols
- Skeptical of purely conceptual papers without empirical grounding
- Looks for explicit limitation sections
- Values transparency in research process documentation

### Review Structure for Reviewer 1

Generate the review in this exact format:

```markdown
## Reviewer 1

### Summary
[3-5 sentences summarizing the paper's objective, approach, and main findings.
Write as if the reviewer genuinely read the paper. Reference specific sections.]

### Strengths
[3-5 bullet points. Each strength must be SPECIFIC — reference a particular
section, argument, or methodological choice. Not generic praise.]

- **S1:** [Specific strength with section reference]
- **S2:** [Specific strength with section reference]
- **S3:** [Specific strength with section reference]

### Weaknesses
[3-5 bullet points. Each weakness must be ACTIONABLE — include what should be
done to address it. Focus on methodological issues.]

- **W1:** [Specific weakness + concrete suggestion for improvement]
- **W2:** [Specific weakness + concrete suggestion for improvement]
- **W3:** [Specific weakness + concrete suggestion for improvement]

### Minor Comments
[3-7 specific, localized comments with section/paragraph references.
These are "nice to have" improvements, not structural issues.]

- [Section X.Y]: [specific comment]
- [Section X.Y]: [specific comment]

### Questions for Authors
[1-3 questions that the reviewer genuinely wants answered. These should probe
methodology choices or unclear aspects of the research design.]

1. [Question about method/design]
2. [Question about validity/generalizability]

### Overall Assessment
**Recommendation:** [Strong Accept / Accept / Minor Revision / Major Revision / Reject]
**Confidence:** [High / Medium / Low] — [1-sentence justification for confidence level]

[2-3 sentence summary of overall assessment. Be direct.]
```

### Calibration Rules for Reviewer 1

- Focus 60% of weaknesses on methodology/design
- Focus 20% on theory application
- Focus 20% on presentation/clarity
- Minor comments should include at least 2 specific textual suggestions
- Questions should be genuine (not rhetorical attacks)
- Recommendation must be calibrated: don't default to "Major Revision" — assess honestly

---

## Step 4: GENERATE Reviewer 2 — "The Theorist"

### Reviewer 2 Persona

**Profile:** Mid-career IS/CS researcher, Associate Professor. Active in theory
development and conceptual contributions. Publishes on theoretical frameworks and
their application in IS research. Reviews for ICIS, ECIS, EJIS. Has strong opinions
about contribution clarity and theoretical grounding.

**Evaluation focus:**
- Clarity and significance of the contribution
- Quality of the research gap argumentation
- Depth and appropriateness of the theoretical lens
- Positioning within the broader literature landscape
- Novelty — does this advance what we know?
- Discussion quality — does it connect findings back to theory?
- Practical vs. theoretical implications balance

**Tone:** Intellectually engaged. Challenges the paper's positioning and theoretical
choices. Asks probing questions about "why this theory?" and "what does this add?"
Uses phrases like "The contribution would be strengthened by...", "I am not convinced
that...", "The authors need to more clearly articulate..."

**Bias tendencies (realistic):**
- Values clear, crisp contribution statements
- Skeptical of papers that use theory as window dressing
- Expects the discussion to do theoretical "heavy lifting"
- Appreciates papers that challenge existing assumptions
- Critical of papers that claim broad contribution from narrow evidence

### Review Structure for Reviewer 2

Generate the review in the same format as Reviewer 1, but with different focus:

```markdown
## Reviewer 2

### Summary
[3-5 sentences. Focus on the paper's theoretical positioning and contribution
claim. Note how the paper fits into the broader discourse.]

### Strengths
[3-5 bullet points focusing on contribution, theory, and positioning.]

- **S1:** [Specific strength — contribution/novelty]
- **S2:** [Specific strength — theoretical grounding]
- **S3:** [Specific strength — literature positioning]

### Weaknesses
[3-5 bullet points. Focus on theoretical/conceptual issues.]

- **W1:** [Specific weakness + concrete suggestion for improvement]
- **W2:** [Specific weakness + concrete suggestion for improvement]
- **W3:** [Specific weakness + concrete suggestion for improvement]

### Minor Comments
[3-7 specific, localized comments.]

- [Section X.Y]: [specific comment]
- [Section X.Y]: [specific comment]

### Questions for Authors
[1-3 questions probing contribution and theoretical choices.]

1. [Question about contribution/positioning]
2. [Question about theory application]

### Overall Assessment
**Recommendation:** [Strong Accept / Accept / Minor Revision / Major Revision / Reject]
**Confidence:** [High / Medium / Low] — [justification]

[2-3 sentence overall assessment.]
```

### Calibration Rules for Reviewer 2

- Focus 60% of weaknesses on contribution/theory/positioning
- Focus 20% on argumentation and logic
- Focus 20% on methodology (from a "fit to RQ" perspective, not methodological depth)
- Minor comments should include at least 1 comment about the introduction's framing
- Questions should challenge the paper's "so what?" — why does this matter?
- Recommendation should be independent of Reviewer 1 (don't harmonize)

---

## Step 5: CALIBRATE Recommendations

### Independence Requirement

The two reviewers MUST arrive at their recommendations INDEPENDENTLY. Do not
harmonize them. In real conferences, reviewers disagree ~40% of the time. This
disagreement is informative — it reveals where the paper is strong (agreement on
strengths) and where it's controversial (disagreement on weaknesses).

### Realistic Recommendation Distribution

For a typical AI-generated first draft from this pipeline, expect:

| Paper Quality | R1 (Methodologist) | R2 (Theorist) | Typical Scenario |
|---------------|-------------------|---------------|------------------|
| Strong draft, clear method | Minor Revision | Minor Revision | Well-executed SLR or DSR |
| Good draft, theory gaps | Minor Revision | Major Revision | Strong method, weak positioning |
| Early draft, structural issues | Major Revision | Major Revision | Needs work across the board |
| Conceptual paper, no empirics | Reject | Minor Revision | R1 wants data, R2 values the idea |
| Data-rich, theory-thin | Accept | Major Revision | R1 satisfied, R2 wants more theory |

### Recommendation Criteria

| Recommendation | Criteria |
|----------------|----------|
| **Strong Accept** | Exceptional. Top 10% of submissions. Clear contribution, rigorous method, excellent writing. Rare for AI-generated drafts. |
| **Accept** | Solid work. Minor issues only. Ready for publication with small tweaks. |
| **Minor Revision** | Good foundation but needs targeted improvements. 1-2 revision rounds expected. Typical for strong first drafts. |
| **Major Revision** | Significant issues that require substantial rework. Structure, method, or theory needs fundamental revision. |
| **Reject** | Fundamental problems. Contribution unclear, method inappropriate, or paper not suitable for venue. Only assign if genuinely warranted. |

### Handling [CITE], [DATA], [TODO] Placeholders

If the paper contains placeholders:
- Mention them explicitly as a weakness (both reviewers)
- Do NOT penalize the overall recommendation as heavily — these are draft markers, not errors
- Note: "The paper contains [N] placeholder markers ([CITE]: N, [DATA]: N, [TODO]: N) indicating sections that require completion before submission."

---

## Step 6: COMPILE & SAVE Output

### Output File: `simulated_reviews.md`

Save the complete output to `simulated_reviews.md` with this structure:

```markdown
# Simulated Peer Review

**Paper:** [title]
**Source reviewed:** [draft.md / paper.tex]
**Date:** [ISO 8601]
**Simulated venue level:** [ICIS / ECIS / MISQ / ...]
**Word count:** ~[N] words
**References:** [N]
**Sections:** [N]

> **Note:** These reviews are AI-generated simulations designed to identify
> potential weaknesses before formal submission. They follow the structure and
> tone of real peer reviews at top IS/CS venues. Use `/respond-reviewers` to
> process this feedback systematically.

---

## Reviewer 1

[Full Reviewer 1 report — see Step 3]

---

## Reviewer 2

[Full Reviewer 2 report — see Step 4]

---

## Meta-Reviewer Summary

### Consensus Strengths
[2-3 points where both reviewers agree the paper is strong]

### Consensus Weaknesses
[2-3 points where both reviewers identify the same issue]

### Divergent Views
[Points where the reviewers disagree — these reveal the paper's most
debatable aspects and should receive special attention during revision]

### Priority Revision Checklist
[Ordered list of the most impactful changes, synthesized from both reviews.
Start with items that would address multiple reviewer concerns simultaneously.]

1. [ ] [Highest priority item — addresses W from both reviewers]
2. [ ] [Second priority — addresses major W from one reviewer]
3. [ ] [Third priority — ...]
4. [ ] [...]

### Recommended Next Steps
- Run `/respond-reviewers` with `simulated_reviews.md` to systematically address feedback
- Focus on items classified as MAJOR or CRITICAL by either reviewer
- Address consensus weaknesses first (both reviewers flagged them)
```

### File Location

Save to the project working directory: `simulated_reviews.md`

If `outputs/` directory exists, also save a copy as `outputs/simulated_reviews.md`.

---

## Venue-Specific Criteria

### IS Conferences (ICIS, ECIS, HICSS, PACIS, WI)

IS conferences emphasize:
- **Clear research contribution** — what new knowledge does this create?
- **Theoretical grounding** — a paper without theory is incomplete
- **Methodological rigor** — method must match the RQs
- **Practical relevance** — IS is an applied discipline
- **Literature positioning** — show awareness of the discourse

Review length: 500-1000 words per reviewer.

### IS Journals (MISQ, ISR, EJIS, BISE, JIT)

Journal reviews are more detailed:
- **Developmental tone** — R&R is an opportunity, not a judgment
- **Specific page/line references** — reviewers cite exact locations
- **Literature suggestions** — "Consider also citing X (Year)"
- **Longer minor comments section** — 10-15 specific items
- **Round-based framing** — "In a revision, the authors should..."

Review length: 800-1500 words per reviewer.

### CS Conferences (NeurIPS, ICML, ACL, CHI)

CS conferences have different norms:
- **Novelty over theory** — what's new technically?
- **Evaluation rigor** — baselines, ablations, statistical tests
- **Reproducibility** — code availability, dataset access
- **Shorter reviews** — 300-700 words per reviewer
- **Numerical scores** — rate individual dimensions 1-5

Adapt review structure and emphasis based on detected venue type.

---

## Error Recovery

- **Paper is too short (<1000 words):** Generate reviews but note that the paper
  appears to be an early-stage draft. Reduce minor comments. Focus on structural
  and conceptual feedback.
- **Paper has many [CITE]/[DATA] placeholders:** Acknowledge these explicitly.
  Review the completed sections. Note which placeholders are most critical to fill.
- **No clear RQs found:** Flag this as Weakness #1 for both reviewers. Suggest
  formulating explicit research questions.
- **No methodology section:** Flag as critical weakness. The methodologist reviewer
  should recommend a specific method based on the RQs.
- **Paper is in German:** Generate reviews in German. Use German academic review
  conventions (Gutachten-Stil). Evaluation dimensions remain the same.

---

## Integration with Other Engines

| Scenario | Integration |
|----------|-------------|
| After review → implement changes | Output feeds into `review-engine` via `/respond-reviewers` |
| Reviewer flags citation concerns | Recommend running `/verify-citations` (verification-engine) |
| Reviewer requests additional literature | Recommend running `/search-papers` (literature-engine) |
| Reviewer requests better figures | Recommend running `/generate-figure` (figure-engine) |
| Reviewer flags writing quality issues | writing-engine templates for specific sections |

### Feedback Loop

The intended workflow is:

```
/write-paper (Phase 1-6)
    ↓
/review-paper (this engine)
    ↓
simulated_reviews.md
    ↓
/respond-reviewers simulated_reviews.md (review-engine)
    ↓
Revised paper.tex + paper.pdf
    ↓
(optional) /review-paper again → iterate until satisfied
    ↓
Submit to venue
```

This creates a pre-submission quality loop that catches most common reviewer
objections before the paper reaches actual reviewers.
