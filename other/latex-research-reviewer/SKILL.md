---
name: latex-research-reviewer
description: Provide comprehensive expert peer review and revision guidance for LaTeX research papers in advanced mathematics and machine learning. Use whenever a user asks to review, evaluate, revise, or assess the journal readiness of one paper or a companion-paper series. Check mathematical correctness, proof rigor, convention shifts, definition placement, jargon and proof fragmentation, prose, structure, series cohesion, novelty and provenance, notation, citations, and rendered presentation; support both referee-report and review-and-implement workflows.
---

# LaTeX Research Paper Reviewer

Conduct a thorough, expert-level peer review of a LaTeX research paper in advanced mathematics or machine learning. This skill mimics the detailed, rigorous feedback style of official conference/journal reviewers.

## How to Use This Skill

When the user provides a `.tex` file for review, follow this complete workflow:

### Step 1: Parse and Understand the Paper
1. Read the entire paper in true reading order, resolving every relevant
   `\input` and `\include`; do not review only the root file
2. Identify the paper structure: abstract, introduction, main sections, proofs,
   appendices, and references
3. If a current PDF exists, map source sections to rendered pages before
   assigning locations or judging layout
4. Get a sense of the paper's scope, contributions, intended venue, and
   intended readership
5. For a series or companion-paper set, first make a one-page dependency map:
   what each part assumes, proves, repeats, and hands to the next part

### Step 2: Comprehensive Review Analysis

Examine the paper systematically across these dimensions:

**Mathematical Correctness & Rigor**
- Verify that all theorems, lemmas, and propositions are stated precisely
- Check proofs for logical completeness (no unjustified steps, all cases covered)
- Verify that definitions are consistent throughout
- Check for unstated assumptions or implicit constraints
- Verify that cited results are applied correctly
- **Convention audit:** explicitly check the shifts and edge cases that often
  survive ordinary proofreading: ideal versus quotient Betti indexing,
  homological versus cohomological degree, reduced versus unreduced homology,
  complements and Alexander duals, total versus multigraded degree, the empty
  face/empty complex, purity, nonemptiness, and coefficient-field assumptions.
- **Compressed calculations:** for generating functions, coefficient
  extractions, recurrences, and enumerative formulas, verify every summation
  range, reindexing, truncation, and parity claim.  A skeptical reader should be
  able to reconstruct the displayed identity locally.  Small computations are
  useful diagnostics, never substitutes for the written proof.
- **Imported-theorem contract:** whenever a proof invokes a substantial cited
  theorem, check the exact hypotheses, convention, and conclusion against the
  source.  State any specialization needed in the paper rather than hiding it
  under “standard.”

**Clarity & Readability**
- Assess whether notation is introduced clearly and used consistently
- Check for undefined symbols or notation changes mid-paper
- Evaluate paragraph flow and transitions between ideas
- Identify dense or convoluted explanations that should be simplified
- Look for prose that could be tightened or improved
- **First-use surfaces:** audit the abstract, introduction, main theorem box,
  and summary tables separately.  These often use an acronym, named subclass,
  invariant, or complement notation before the formal setup.  Expand acronyms
  and give a one-line mathematical gloss at first use; a later full definition
  does not repair an opaque abstract.
- **Definition adequacy:** an English description is not a mathematical
  definition. In notation tables and at first use, require the domain, formula,
  constraints, measure or normalization, and endpoint conventions for central
  objects. Preserve interpretation alongside the formula. Check that the
  concise introductory definition agrees exactly with the later proof-level
  definition.
- **Forward references:** flag any term, object, or notation *used before it is defined*. Distinguish these from intentional, helpful forward references (proof roadmaps, "see §X" navigation, "we prove below") — only the term-before-definition kind is a defect. Do not treat the raw count of references-to-later-labels as the metric; a good terminology table legitimately points forward. The target is "no term opaque at first use."
- **Jargon density:** flag bespoke or evocative-but-vague terms that carry heavy load but lack a crisp early definition or glossary entry. Recommend a clearer/more explicit name, or at minimum a one-line gloss at first use plus a glossary entry.
- **Data-versus-name test:** when a coined term denotes only a function, set,
  measure, or minimizer satisfying a short displayed list of properties, prefer
  stating those properties directly. If removing the name loses no
  mathematical information, remove it. For a legitimate standard term, state
  the defining formula or optimization problem before relying on the name.
- **Cross-field standard terms:** even legitimate specialist terms may need a
  short parenthetical gloss when the paper connects several communities.  Keep
  the standard term, but do not force a reader from the adjacent field to infer
  it from later context.
- **Table anaphora:** flag rows beginning with “the same condition,” “such a
  class,” or similarly vague pointers.  A recap table should be intelligible
  when read independently and should state the scope of every row.
- **AI-like proof-process jargon:** in abstracts, introductions, conclusions, and theorem summaries,
  flag terms that sound like internal proof-management labels rather than standard mathematical
  prose. Examples include "proof spine", "proof package", "mechanism", "route", "pipeline",
  "stratum" when no stratification is actually defined, "architecture", "engine", "certificate"
  when no formal certificate is specified, "finite certificate", "proof debt", "proof obligation",
  "gate", "assay", and similar phrases. Generic use of "obstruction" should also be flagged unless
  the obstruction is named, located, and mathematically contextualized. Generic use of "boundary"
  should likewise be flagged unless the paper specifies which boundary is meant, such as a
  topological boundary, graph boundary, boundary operator, measure-theoretic boundary, boundary
  stratum, or boundary condition. Generic use of "sector" should also be flagged unless the sector
  is a defined geometric region, parameter regime, decomposition class, or standard term in the
  relevant field. These often gesture at a real idea but use the wrong register. Recommend replacing
  them with the actual mathematical
  content: "the main reduction", "the induction scheme", "the auxiliary construction", "the
  invariant", "the decomposition into cases", "the comparison lemma", "the remaining lemma to
  prove", "the necessary condition", "the counterexample family", or a formally defined term. Do
  not ban standard terms such as "stratum", "filtration", "certificate", "obstruction",
  "boundary", "sector", or "mechanism" when they are conventional in the field or explicitly
  defined; the defect is unsupported, generic, AI-flavored abstraction.

**Overall Structure**
- Does the paper have a clear narrative arc?
- Are contributions clearly stated and well-motivated?
- Does the introduction adequately set up the main results?
- Are sections organized logically?
- Does the conclusion adequately discuss implications and future work?
- Write a one-sentence question and one-sentence answer for each section.  If
  either sentence is unavailable, the section probably needs a clearer opening,
  a sharper title, or a transition explaining why it belongs.
- Check that the abstract, introduction, recap table, and conclusion emphasize
  the same main results in the same order.  These four summaries should not tell
  competing stories.

**Series Cohesion** (when reviewing multiple papers together)
- Require each part to be standalone at the level promised by its abstract,
  while avoiding repeated proofs and long repeated background.
- Check titles, notation, terminology, theorem names, provenance language, and
  companion-paper citations for consistency across parts.
- Make every handoff exact: say what the earlier part proves, what the present
  part adds, and what the later part studies.  Avoid generic phrases such as
  “crosses the boundary” when “studies the first failure under conditioning” is
  the actual statement.
- Check that exploratory questions have not leaked into theorem-driven papers
  as if they were established results.

**Structural Navigability** (especially for long, multi-file papers)
- Flag any single section or source file that has become a long, *flat* wall of results — many theorems/lemmas with almost no `\subsection`/`\subsubsection` or signpost structure. These are a readability emergency even when each result is correct.
- Flag the opposite failure as well: a chain of short theorem-like
  environments, each used once only by the next, makes a full proof read like a
  dependency map. Build the local citation/use graph. Recommend one proof with
  named steps unless an intermediate statement is reusable, independently
  citable, or isolates a genuine proof contract.
- Ask of every named result: "Would a later reader cite this statement without
  citing the enclosing proof?" If not, consider demoting it to a proof step.
- Recommend splitting an over-grown file at its natural conceptual seams, promoting the largest clusters to their own sections, and adding in-body navigation headers so a reader can locate an argument.
- Check that the table of contents (at the configured `tocdepth`) actually reflects the conceptual structure; recommend headers at the depth that will surface.
- When recommending a restructure, note the safety discipline the author
  should follow: for moves or retitles, keep content and `\label` keys
  byte-identical. For deliberate consolidation, record removed labels, update
  all references, and verify the before/after label-set delta and final build.

**Citation Accuracy & Completeness**
- Verify that all citations are formatted consistently
- Check that referenced results actually exist in cited works
- Identify any missing citations (e.g., related work that should be mentioned)
- Flag if important predecessors are omitted
- Do not trust an attribution merely because it already appears in the draft.
  Verify the exact definition or theorem in a primary source, including theorem
  number, scope, hypotheses, and publication metadata.  Distinguish “this
  source contains a related idea” from “this source proves the formulation used
  here.”
- Locate the common library with `shared-literature`; if it has durable packets or reading notes, consult
  them before searching or downloading the source again.  When a genuinely new
  source is inspected, preserve enough durable information—metadata, source
  location or extracted text, and the exact key result—to prevent repeated
  rediscovery.
- Flag superseded, questioned, or counterexampled statements explicitly.  A
  valid lemma from a paper may still be cited even if another theorem there is
  false, but the manuscript must identify precisely which result it uses.

**Novelty & Provenance Calibration**
- Classify every result highlighted in the abstract, introduction, or conclusion
  as one of: new theorem; new proof of a known theorem; new explicit
  translation; synthesis of known results; formal corollary; or recalled
  background.  Do not let useful translations or syntheses masquerade as new
  structure theorems.
- Check whether consequences become classical once a new classification is
  established.  Credit the classification separately from inherited
  enumerative, topological, or algebraic consequences.
- Match the prose to the classification: use “prove” for new results,
  “deduce” for corollaries, “translate” for dictionary statements, “assemble”
  for combinations, and “recall” for known facts.  This calibration improves
  credibility without diminishing the paper's contribution.

**Presentation Quality**
- Check for typos, grammatical errors, or awkward phrasing
- Assess figure/table quality and captions
- Verify equations are properly formatted and numbered if referenced
- Look for consistent terminology (e.g., don't alternate between "matrix" and "tensor")
- Compile after substantive edits, preferably with SyncTeX when annotation is
  part of the workflow.  Scan the final log for undefined citations and
  references, multiply defined labels, overfull boxes, and rerun warnings.
- Inspect every materially changed PDF page visually.  Source review alone
  misses orphaned headings, table overflow, bad page breaks, crowded displays,
  and captions separated from their objects.  Treat bibliography-only
  underfull boxes differently from defects in the mathematical text.

**Handling Incomplete Sections**
- If a section is marked as incomplete or contains placeholders:
  - Do NOT criticize the incompleteness
  - Instead, offer co-author-style suggestions: "This section could discuss X, which would strengthen the argument by..." or "You might consider adding an example here to illustrate..."
  - Provide specific guidance on what the incomplete part should contain

### Step 3: Compile or Implement the Review

Choose the deliverable requested by the user:

- **Review only:** provide the referee report in the structure below.
- **Review and implement:** first form the same issue list internally, then
  apply only well-supported fixes, rebuild, inspect the rendered changes, and
  review the final diff.  The final response should summarize the material
  changes, validation, and any remaining blocker; do not force the full referee
  template into the response unless the user asks for it.
- **Review across a series:** add a short series-level assessment before the
  paper-by-paper issues, and avoid reporting the same shared issue three times.

For a review-only response, use this structure:

#### **OVERALL SUMMARY** (2-3 paragraphs)
Brief assessment of the paper's contributions, strengths, and main weaknesses. State whether the paper makes a solid contribution and is ready for publication (with or without revisions).

#### **ISSUES TO FIX** (Organized by category)

**Mathematical/Technical Issues:**
- [Issue number]. [Statement of issue] (Severity: critical/major/minor)
  - Location: Section X, Page Y
  - Details: Explain what's wrong
  - Suggested fix: Be specific about how to correct it

**Clarity/Presentation Issues:**
- [Issue number]. [Statement of issue] (Severity: critical/major/minor)
  - Location: Section X, Page Y
  - Details: Explain the problem
  - Suggested fix: Specific suggestion

**Structure/Organization Issues:**
- [Issue number]. [Statement of issue] (Severity: critical/major/minor)
  - Location: Section X, Page Y
  - Details: Explain the problem
  - Suggested fix: Specific suggestion

**Citation Issues:**
- [Issue number]. [Statement of issue] (Severity: critical/major/minor)
  - Location: Section X, Page Y
  - Details: Explain the problem
  - Suggested fix: Specific suggestion

#### **GENERAL SUGGESTIONS** (3-5 items)
Constructive recommendations that go beyond fixing specific issues. These might be:
- Ways to strengthen contributions
- Opportunities to clarify concepts or intuitions
- Connections to related work that could enhance context
- Suggestions for examples or visualizations that would help readers
- Ideas for restructuring to improve flow

#### **DETAILED COMMENTS**
Section-by-section comments if needed for major issues. Provide specific line-by-line feedback for any sections with significant problems.

---

## Reviewer Standards

Apply the standards of a top-tier venue (NeurIPS, ICML, JMLR, arXiv for math):

- **Rigor**: Proofs must be complete and correct. All claims must be justified.
- **Clarity**: The paper should be understandable to a reader in the field with reasonable effort
- **Significance**: Contributions should be novel and non-trivial (but as a reviewer, focus on what's actually there)
- **Completeness**: Related work should be adequate; key results shouldn't be missing

Be fair but thorough. Point out strengths alongside weaknesses. Be constructive — every criticism should come with a suggested improvement or clarification.

---

## Example Output Structure

```
# PEER REVIEW: [Paper Title]

## OVERALL SUMMARY
This paper proposes [contribution]. The main strengths are [X] and [Y]. However, there are concerns about [Z]. Overall, [assessment].

## ISSUES TO FIX

**Mathematical/Technical Issues:**
1. Theorem 3 statement is imprecise (Severity: major)
   - Location: Section 3, Page 5
   - Details: The condition "for sufficiently large n" is never formalized...
   - Suggested fix: State the theorem as: "For all n ≥ N₀ where N₀ = ..."

**Clarity/Presentation Issues:**
2. Notation for ρ is used before definition (Severity: minor)
   - Location: Section 2, Equation (4)
   - Details: ρ appears in Eq. (4) but isn't defined until Eq. (7)
   - Suggested fix: Move the definition of ρ to Section 2.1 or add a footnote

...

## GENERAL SUGGESTIONS
1. Consider adding a simple example in Section 2 to illustrate the main concept...
2. The connection to [Related Work] could be made more explicit...
3. A figure showing the algorithm flow would help readers...

## DETAILED COMMENTS
[Section-by-section feedback as needed]
```

---

## Notes for Reviewers

- **Severity levels**: critical (must be fixed), major (should be fixed), minor (nice to fix)
- **Tone**: Professional, respectful, constructive. You're helping improve the work
- **Completeness**: If you find an issue, explain it fully so the author understands
- **Incomplete sections**: Don't penalize; instead suggest how to fill them in
- **Humility**: If you're unsure about a mathematical claim, say so and suggest the author clarify
