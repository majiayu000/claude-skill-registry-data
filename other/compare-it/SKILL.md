---
name: compare-it
description: "Produce structured architectural comparison documents that evaluate two tools, technologies, or solutions against weighted criteria. Use when asked to compare tools, evaluate alternatives, write a technology assessment, create a build-vs-buy analysis, or produce a recommendation report. Also use when someone says 'which should we use', 'should we adopt X or keep Y', 'compare X vs Y', 'evaluate X against Y', or 'is X better than Y'. Handles evaluation framework design, weighted scoring, cost analysis, risk assessment, gap analysis, and actionable recommendations with reversal conditions."
metadata:
  author: Serghei Iakovlev
  version: "1.1"
  category: research
---

# Tool comparison evaluation

Produce publication-grade architectural comparison documents that evaluate two solutions against weighted criteria derived from organizational requirements. The output follows a 12-section structure with quantified scoring, bidirectional gap analysis, Mermaid architecture diagrams, cost projections, risk matrices, and reversal conditions for every recommendation.


## Workflow

### Phase 1: Research both solutions

Gather enough context to write authoritative profiles. Research is front-loaded. Weak research produces weak evaluations.

Research checklist:

- [ ] Identify Solution A and Solution B
- [ ] For each solution, collect: type, maturity, vendor/maintainer, mechanism, output format, integrations, generation time
- [ ] Find official documentation, product pages, blog posts, press coverage
- [ ] Identify pricing model and tiers
- [ ] Find academic research relevant to the comparison domain
- [ ] Identify the organization's current usage and existing investments
- [ ] Document limitations of the research (no hands-on testing, beta status, etc.)

**Source priority:**

1. Official documentation and technical specs
2. Academic research papers (arXiv, conference proceedings)
3. Press coverage and analyst reports
4. Community discussions and case studies

### Phase 2: Define evaluation framework

Design criteria and weights before scoring. The framework must reflect the organization's priorities, not generic equal-weight distribution.

Framework checklist:

- [ ] Identify 6-10 evaluation criteria from organizational requirements
- [ ] Assign percentage weights that sum to exactly 100%
- [ ] Write a one-sentence rationale for each weight
- [ ] Define the 1-5 scoring scale with semantic anchors
- [ ] Verify the highest-weighted criteria reflect the organization's primary constraints

See [evaluation methodology](references/evaluation-methodology.md) for scoring frameworks, weight calibration, and sensitivity analysis techniques.

### Phase 3: Write the document

Follow the 12-section structure. Each section has a specific purpose. Do not merge, skip, or reorder sections.

Use the [comparison template](assets/comparison-template.md) as a starting point. Copy it and fill in the placeholders. See [document structure](references/document-structure.md) for section-by-section guidance with examples.

#### Metadata and framing (Sections 1-2)

- [ ] Document metadata (status, date, classification, authors)
- [ ] Section 1: Executive summary (scope + finding + recommendation)
- [ ] Section 2: Scope and methodology (in/out table, assumptions, limitations)

#### Solution profiles (Section 3)

- [ ] Section 3: Solution profiles (symmetric fields for both solutions)

#### Scoring and analysis (Sections 4-5)

- [ ] Section 4: Evaluation framework (criteria, weights, matrix, sensitivity check)
- [ ] Section 5: Architectural fit analysis (Mermaid diagrams, integration topology)

See [evaluation methodology](references/evaluation-methodology.md) for scoring frameworks and sensitivity analysis.

#### Cost, risk, and gaps (Sections 6-8)

- [ ] Section 6: Total cost of ownership (assumptions, formulas, multi-year projection)
- [ ] Section 7: Risk assessment (risk matrix covering both solutions)
- [ ] Section 8: Gap analysis (bidirectional: A-has/B-lacks AND B-has/A-lacks)

#### Synthesis and recommendation (Sections 9-10, Appendices)

- [ ] Section 9: Improvement candidates (features from rejected solution worth adopting)
- [ ] Section 10: Recommendation (primary recommendation, reversal conditions, next steps, re-eval date)
- [ ] Appendix A: Sources (grouped by solution + research, with inline citation context)
- [ ] Appendix B: Evaluation criteria weight justification

### Phase 4: Validate

Use the **Quality Checklist** below. Do not skip the arithmetic verification.

See [writing guidelines](references/writing-guidelines.md) for style, voice, formatting, and diagram conventions.

## Document architecture

The 12-section structure follows a deliberate argument arc: situate the reader (1-2), present the candidates (3), evaluate systematically (4), analyze architecture (5), quantify cost (6), assess risk (7), identify gaps (8), extract improvements (9), recommend (10), support with evidence (A-B).

| #    | Section                | Purpose                              | Key output                                                       |
| ---- | ---------------------- | ------------------------------------ | ---------------------------------------------------------------- |
| Meta | Document metadata      | Provenance and status                | Status, date, classification, authors                            |
| 1    | Executive summary      | Orient the reader in 30 seconds      | Evaluation scope + Finding + Recommendation                      |
| 2    | Scope and methodology  | Establish boundaries and credibility | In/out scope table, methodology, assumptions, limitations        |
| 3    | Solution profiles      | Present candidates symmetrically     | Type, mechanism, output structure, integrations, timing          |
| 4    | Evaluation framework   | Score with full transparency         | Weighted criteria, rubric, matrix, totals, sensitivity check     |
| 5    | Architectural fit      | Analyze structural compatibility     | Mermaid diagrams, integration topology, governance analysis      |
| 6    | Cost analysis          | Quantify the cost differential       | Assumptions, multi-year projection table, cost multiplier        |
| 7    | Risk assessment        | Identify and classify risks          | Risk matrix (probability x impact x solution x mitigation)       |
| 8    | Gap analysis           | Map what each solution lacks         | Bidirectional capability comparison with "addressable?" column   |
| 9    | Improvement candidates | Extract value from rejected solution | Specific improvements with effort estimates                      |
| 10   | Recommendation         | Decide clearly                       | Primary recommendation, reversal conditions, next steps, re-eval |
| A    | Sources                | Support every claim                  | Grouped by solution + research, inline citation context          |
| B    | Weight justification   | Defend the framework                 | Per-criterion rationale for weight assignment                    |

## Executive summary structure

The executive summary contains exactly three elements in this order:

1. **Evaluation scope** - What is being compared and why. Correct false equivalences upfront. If one solution covers two stages of the other's pipeline, say so here. This prevents unfair downstream comparisons.
2. **Finding** - Neutral factual summary of what the evaluation discovered. No recommendation yet. State the structural relationship between the solutions.
3. **Recommendation** - Decisive action with quantified evidence. "Retain Solution B. Do not adopt Solution A." followed by the key numbers and structural reasons.

## Core principles

### Symmetry

Every data point for Solution A must exist for Solution B. Asymmetric profiles produce biased comparisons. If data is unavailable for one solution, note it as unavailable rather than omitting the field entirely.

### Quantification

Numbers replace adjectives. "42x cost differential" not "significantly more expensive". "4.45/5.00 vs 2.05/5.00" not "scored much higher". Show calculations so readers can verify the arithmetic independently.

### Intellectual honesty

- State limitations of the analysis upfront (Section 2.4)
- Include a sensitivity check that stress-tests the conclusion
- Provide reversal conditions: what circumstances would change this recommendation
- Set a re-evaluation date

### Bidirectional gap analysis

Section 8 answers both questions:

- What does A have that B lacks?
- What does B have that A lacks?

Each gap entry needs an "Addressable?" column explaining whether the gap can be closed internally. One-sided analysis is advocacy, not evaluation. The asymmetry between addressable and structural gaps often tells the real story.

### Improvement extraction

The rejected solution exists for a reason. Section 9 extracts specific features worth adopting into the recommended solution. Each improvement needs:

- Problem statement (what's missing)
- Proposed approach (how to add it)
- Effort estimate (small/medium/large with one-sentence reasoning)

This transforms a "don't adopt X" conclusion into a "retain Y and strengthen it with ideas from X" action plan.

## Diagrams

Use Mermaid for all architecture diagrams. Include at minimum:

1. **Integration topology for each solution** - how each connects to the broader system. Side-by-side comparison reveals structural differences.
2. **Governance/knowledge propagation** - how project context, rules, and constraints flow through the system.

**Color coding (mandatory):**

- Red (`fill:#f4cccc,stroke:#cc0000`): Problems, risks, manual steps, gaps
- Green (`fill:#d9ead3,stroke:#38761d`): Advantages, automation, knowledge sources

**Label connections** when the relationship is not self-evident:

```plaintext
A -- "manual copy/paste" --> B
```

**Use subgraphs** to group related elements:

```plaintext
subgraph knowledge["Project Knowledge"]
    direction LR
    F["AGENTS.md"]
    G["Rules"]
end
```

Keep each diagram focused on one concept. Two clear diagrams communicate more than one crowded diagram.

## Anti-patterns

| Pattern                     | Problem                                          | Fix                                                                    |
| --------------------------- | ------------------------------------------------ | ---------------------------------------------------------------------- |
| Feature checklist           | Compares features, not outcomes                  | Compare what each solution achieves, not what it has                   |
| Scores without evidence     | Unverifiable claims                              | Every score needs inline justification in the evaluation matrix        |
| One-sided gap analysis      | Reads as advocacy                                | Always show gaps in both directions                                    |
| Vague mitigations           | "Address the issue" is not actionable            | Specify concrete action, estimated cost/effort, and owner              |
| Missing sensitivity check   | Conclusion may depend on one criterion           | Remove highest-weight criterion and verify the winner still holds      |
| Orphan recommendations      | No path to reconsider                            | Every recommendation needs reversal conditions and re-evaluation date  |
| Hedged conclusions          | "Perhaps consider not adopting" lacks conviction | "Do not adopt. Here's why." State the position, then defend it.        |
| Equal-weight distribution   | 20/20/20/20/20 ignores actual priorities         | Weights reflect organizational constraints, not fairness               |
| Hidden cost calculations    | "$17,280" without showing the math               | Show formula: $24 x 20 x 36 = $17,280                                  |
| Aesthetic-only diagrams     | Pretty diagram with no analytical insight        | Every diagram must reveal a structural difference or integration issue |
| Merged research and scoring | Writing profiles and scoring simultaneously      | Complete Phase 2 (framework) before scoring; complete Phase 1 before 2 |

## Quality checklist

Before finalizing, verify every item:

### Structure

- [ ] All 12 sections present and in correct order
- [ ] Solution profiles are symmetric (same fields for both)
- [ ] Gap analysis is bidirectional (A has / B lacks AND B has / A lacks)

### Arithmetic

- [ ] Weights sum to 100%
- [ ] Weighted score calculations are arithmetically correct
- [ ] Cost projections show formulas, not just totals

### Analytical rigor

- [ ] Sensitivity check included (remove highest-weight criterion, verify winner holds)
- [ ] Every score has inline evidence (no naked numbers)
- [ ] Risk matrix covers both solutions
- [ ] Every recommendation has reversal conditions
- [ ] Every recommendation has a re-evaluation date

### Visual and source integrity

- [ ] Mermaid diagrams render correctly
- [ ] Sources cited inline where used and collected in Appendix A

### Writing standards

- [ ] No AI-marker words (see [writing guidelines](references/writing-guidelines.md))
- [ ] No hedging phrases
- [ ] Third person throughout
- [ ] Active voice throughout
- [ ] Sentence case headings

## Language

Write all evaluation documents in English. Communicate with the user in their language during the research and drafting process.
