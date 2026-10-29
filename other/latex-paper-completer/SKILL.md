---
name: latex-paper-completer
description: >-
  Complete and enhance draft LaTeX research papers in pure mathematics to
  improve self-containedness, intuition, and progressive complexity. Use this
  skill whenever a user uploads a .tex file or section and asks to
  complete/improve a draft, add intuitive explanations, define missing concepts,
  fill in proofs, reduce jargon or proof fragmentation, or restructure for
  progressive disclosure. Works on papers at any stage and offers three levels
  of enhancement: (1)
  Self-containedness—identify undefined concepts, create glossaries, ensure
  consistency; (2) Intuition—suggest and write rigorous examples, illustrations,
  and intuitive explanations without vagueness; (3) Complexity levels—restructure
  proofs and results with simplified versions first, proof sketches before
  details, and hierarchical organization. Essential for creating expository
  papers that serve as references.
---

# LaTeX Paper Completer: Self-Containedness, Intuition, and Progressive Complexity

Systematically enhance a draft research paper to maximize self-containedness, build reader intuition, and present technical content at multiple levels of complexity. This skill transforms manuscripts into expository references that educate while proving theorems.

## How to Use This Skill

The user provides either a full `.tex` file or a specific section. Follow the complete workflow below:

If the user provides a PDF review file produced by `scripts/skim_notes_to_review.py`, treat it as an
edit queue. For each annotation, use the mapped SyncTeX location as a starting point, verify the
selected PDF text against the nearby TeX source, apply the requested improvement conservatively,
and mark any ambiguous or stale annotation in the final response instead of guessing.

### Step 0: Scope and Strategy

Ask the user (if not specified):
1. **Scope**: Are we working on the entire paper, specific sections, or both?
2. **Priorities**: Which of the three goals (self-containedness, intuition, complexity levels) matters most?
3. **Existing structure**: Does the paper already have appendices, or should we create them?

---

## Step 1: Self-Containedness Audit

### 1.1 Identify Missing or Vague Definitions

Read through the paper and flag every concept that is:
- Used before being defined
- Defined informally without precision
- Defined in a hard-to-find location
- Used inconsistently with its definition

Create a structured list:
```
MISSING/VAGUE DEFINITIONS AUDIT:

Concept: [Name]
Status: [Used before definition | Informally defined | Inconsistently used | Missing]
Location: [Where first used]
Current definition (if any): [Quote]
Severity: [Critical | Important | Minor]
Fix: [Recommendation]
```

### 1.2 Notation Consistency

- Create a **Notation Table** organizing all symbols used
- Check for notation used without introduction
- Flag notation that changes meaning between sections
- Identify where notation could be simplified or made clearer
- Require a mathematical definition, not only an English gloss. For a central
  functional, norm, operator, or auxiliary quantity, record its domain,
  formula, constraints, and normalization. Preserve a short interpretation
  alongside the formula.
- Treat the table as a first-use surface. It must be intelligible on its own,
  but a central definition should also be stated consistently at the later
  proof-level point of use.

Template for notation table:
```
| Symbol | Definition | First Used | Page |
|--------|-----------|-----------|------|
| $\mathcal{X}$ | Underlying measure space | Section 2.1 | 3 |
```

### 1.3 Create/Enhance Glossary and Notation Appendix

If the paper lacks a glossary:
- **Create Appendix A: Notation and Symbols** — organized by type (sets, functions, operators, constants)
- **Create Appendix B: Glossary of Key Terms** — alphabetical list of technical terms with one-sentence definitions and section references

Example format:
```
APPENDIX A: NOTATION AND SYMBOLS

Sets and Spaces:
- $\mathcal{X}$ : underlying sample space (Section 2)
- $\mathbb{R}^d$ : $d$-dimensional Euclidean space
- $\mathcal{B}(\mathcal{X})$ : Borel σ-algebra on $\mathcal{X}$ (Definition 2.1)

Operators:
- $P_C$ : Euclidean projection onto set $C$ (Definition 3.2)
- $\nabla f$ : gradient of function $f$
```

### 1.4 Cross-References and Forward References

- Add a forward reference section after abstract or introduction listing main definitions
- Example: "Main definitions: see Definition 2.1 (Wasserstein distance), Definition 3.4 (regularity condition)..."
- Ensure all main results reference the definitions they depend on

**Diagnose harmful forward references.** Walk the document in true reading order (resolving the `\input`/`\include` tree) and flag every `\ref`/`\autoref`/`\cref` whose target `\label{}` is defined *later*. Then **triage** — not all forward references are bad:
- *Intentional and helpful:* proof roadmaps ("we prove X below"), reading guides, "see §X" navigation, a terminology table that points forward to formal definitions. **Keep these.** Do not optimize the raw forward-reference count — a glossary that helps the reader will *increase* it.
- *Harmful:* a term, object, or notation that is genuinely opaque at first use because its definition is far ahead. **Fix these**, preferring (in order): (a) reorder so the definition precedes the use; (b) add a forward-declared definition or a one-line "define-lite" gloss at first mention (e.g. "a *checked space* means …; its full construction is Def. X"); (c) add the term to a point-of-use terminology table (see §1.6).
- The goal is **"no term opaque at first use,"** not zero forward references.

### 1.5 Output for Self-Containedness

Provide specific guidance:
```
SELF-CONTAINEDNESS REPORT:

CRITICAL ISSUES (must fix):
1. Theorem 3 uses the concept "regularity condition" which is never formally defined
   → Recommendation: Add Definition X formally stating the condition

2. Notation $\rho(x,y)$ appears in Eq. (5) without introduction
   → Recommendation: Introduce in Section 2 with definition and intuition

IMPORTANT ADDITIONS:
1. Create Appendix with notation table (currently missing)
2. Add cross-references from Theorem 2 to Definition 1.5

MINOR ENHANCEMENTS:
1. Glossary is present but incomplete—add 3 more terms
```

Then provide the actual text additions/edits.

---

### 1.6 Structural Navigability and Jargon Hygiene

Long papers (especially multi-`\input` ones) accrete two problems that hurt self-containedness even when every result is correct: **giant flat files** and **dense bespoke jargon**. Treat these explicitly.

**Measure first.** Build a structural map before editing: list each section/file with its line count and the number of theorem-like environments and headers it contains. A file with dozens of results but only one or two headers is a flat wall and a prime target.

**Split and signpost giant flat blocks.**
- Split an over-grown file at its natural conceptual seams into several `\input` sub-files; promote the largest clusters to their own `\section`s, and add `\subsection`/`\subsubsection`/`\paragraph` signposts so a reader can navigate.
- Cut at clean boundaries (a blank line between an environment's `\end{}` and the next environment/prose) so no environment is split.
- Make the cut points match the configured `tocdepth`: headers deeper than `tocdepth` improve in-body reading but will not appear in the table of contents — choose the level accordingly.

**Also audit over-fragmentation.** Build the local use graph of theorem-like
statements. If several short lemmas or propositions are used exactly once, in
order, only to prove the next item, consolidate them into one proof with
descriptive steps. Keep a named intermediate result only when it has a
standalone formulation, is reused, isolates a genuine proof contract, or is
likely to be cited independently. Do not make theorem numbering reproduce a
proof outline.

**Build a point-of-use terminology table.** For a section that introduces many coined terms, add a short "Vocabulary for this section" table at its head: each term, a one-line plain-language gloss, and an `\autoref` to its formal definition. This front-loads meaning so nothing is opaque on first reading, and it is the single highest-value, lowest-risk jargon fix.

**Prefer data over coined names.** If an object is only a function, set, or
measure satisfying a short list of properties, state those properties directly
instead of inventing a noun phrase. Put plain mathematical content in
subsection and theorem titles. When a specialist term is standard and useful,
give the formula or optimization problem first and identify the standard name
second; do not ask the name to carry the definition.

**Rename opaque terms carefully (optional, with author sign-off).** Evocative-but-vague coined nouns can be renamed to more explicit ones — but only the *displayed* term. **Keep `\label` keys stable** and change prose/title text only, so every cross-reference still resolves. Protect `\label{}`/`\ref{}`/`\autoref{}` contents from any global search-and-replace, prefer whole-word boundaries, and scan afterwards for doubled-word artifacts (e.g. a swap turning "X cycle" into "Y cycle cycle"). Prefer a glossary over a rename when a term is precise and heavily used; do not degrade a carefully written note just to remove a word.

**Operational discipline (do this for every restructuring edit).**
1. Keep content byte-identical when only moving/retitling — the split should not change a single line of mathematics.
2. After each change, **rebuild** and compare the `\label` multiset before and
   after. For moves and retitles it must be unchanged. When consolidating
   one-use results, record the intentionally removed labels and update every
   reference to them; no unexplained label loss is acceptable.
3. Confirm there are no new undefined or multiply-defined references.
4. Preserve file history with `git mv` when renaming/splitting files.

---

## Step 2: Intuition Enhancement

### 2.1 Identify Concepts Lacking Intuition

For each major definition, theorem, or technique, check:
- Is there a plain-language explanation before or after the formal statement?
- Are there concrete examples?
- Is the geometric/intuitive meaning explained?
- Could a simple illustration help?

### 2.2 Write Rigorous but Accessible Explanations

For each concept, provide:

**Format:**
```
CONCEPT: [Name]
Location: [Section X]

INTUITIVE EXPLANATION (Rigorous but non-technical):
[2-4 sentences explaining the core idea. Use analogies and geometric language, but ensure mathematical precision.]

SIMPLE EXAMPLE:
[Concrete, worked example with actual numbers or simple objects]

WHAT IT MEANS:
[One sentence capturing the essence]

ILLUSTRATION SUGGESTION:
[Description of helpful figure or diagram]
```

### 2.3 Examples: Suggested Additions

For definitions, theorems, and techniques, add examples at multiple levels:

**Example 1 (Simple)**: Minimal case, easy to follow, builds intuition
- Location in text: right after definition
- Example type: toy problem, 1D or 2D case, or $n=2$ case

**Example 2 (Instructive)**: Moderately complex, illustrates non-trivial aspects
- Location: after proof or main result
- Example type: shows why assumptions matter, or contrast with boundary case

**Example 3 (Applied)**: Connects to practice or other areas
- Location: applications section or remarks
- Example type: real-world application or link to well-known problem

### 2.4 Illustrations and Visualizations

Suggest figures/diagrams for:
- Geometric concepts (e.g., cones, projections, intersections)
- Algorithm flow
- Intuition diagrams (e.g., convergence behavior, phase diagrams)

Format:
```
FIGURE SUGGESTION: [Title]
Where: [Section/subsection]
Description: [What the figure shows]
Type: [Geometric diagram | Algorithm flowchart | Behavior visualization | etc.]
Rough sketch:
[ASCII art or brief verbal description]
```

### 2.5 Intuition Addition: Paragraph Template

When adding intuitive explanation to an existing definition, use this template:

**Before formal definition:**
```
\paragraph{Intuition.}
[Explain the idea in plain language. What problem does this concept solve? Why do we care? Mention key special cases.]
```

**After formal definition and before/after first use:**
```
\begin{remark}[Geometric interpretation]
Geometrically, [explanation]. In the special case where [simple case], this reduces to [simple result].
\end{remark}
```

---

## Step 3: Progressive Complexity (Hierarchical Presentation)

### 3.1 Identify Opportunities for Layered Presentation

Look for:
- Theorems or results that could be stated in simplified form first
- Proofs that are dense and could benefit from a sketch
- Definitions that could be motivated or presented at increasing levels of generality
- Results with many assumptions that could be presented in increasingly general versions

### 3.2 Restructure with Proof Sketches

**For substantial proofs**, add a **Proof Sketch** before the full proof:

```
\begin{theorem}[...]
  [Statement]
\end{theorem}

\begin{proof}[Proof Sketch]
We prove this in three steps:
1. [High-level idea for step 1]
2. [High-level idea for step 2]
3. [High-level idea for step 3]

The key insight is [main idea]. Technical details follow.
\end{proof}

\begin{proof}[Full Proof]
[Detailed, line-by-line proof with all steps justified]
\end{proof}
```

### 3.3 Simplify-First Structure

**For complex theorems**, structure as:

```
\begin{theorem}[Simple Case / First Version]
Assume [simplified assumptions]. Then [simplified statement].
\end{theorem}

\begin{proof}
[Proof with minimal technical machinery]
\end{proof}

\begin{remark}
This simpler version illustrates the main idea. The general result extends to [describe generalization].
\end{remark}

\begin{theorem}[General Version]
Under [general assumptions], we have [general statement].
\end{theorem}

\begin{proof}
[Complete proof. The simple case above gives intuition; we now handle the general case by [key new technique].]
\end{proof}
```

### 3.4 Hierarchical Organization

Reorganize the paper structure to support progressive reading:

**Main Narrative (Sections 1-4):**
- Introduction
- Definitions (key concepts only, intuitive explanations)
- Main Results (simplified statements first, then general)
- Proof sketches of main theorems

**Appendices:**
- Appendix A: Notation and Symbols
- Appendix B: Glossary
- Appendix C: Detailed Proofs (full versions, with all technical details)
- Appendix D: Extended Examples (further worked examples)
- Appendix E: Omitted Proofs (results used but not central to prove)

### 3.5 Reading Roadmap

Add a section early in the paper:

```
\subsection*{Reading Guide}

\textit{For intuition}: Read Sections 1-3 and Example 1 in Section 4. Proof sketches are sufficient.

\textit{For complete understanding}: Also read the full proofs in Appendix C.

\textit{For connections to related work}: See Remarks throughout and discussion in Section 5.

\textit{For advanced readers}: Begin with Section 3 and proceed directly to Appendix C.
```

### 3.6 Cross-Referencing for Levels

Use hyperref and thoughtful structure to support different reading paths:
- Link proof sketches to full proofs: "See Appendix C for details"
- Link simple cases to general: "See Theorem X (General Version) for extensions"
- Link remarks to background material: "See Appendix B for definition of [term]"

---

## Step 4: Synthesis and Output

### 4.1 Comprehensive Completion Report

Provide the user with:

```
PAPER COMPLETION REPORT: [Title]

=== SELF-CONTAINEDNESS ===
Issues identified: [count]
Critical (must fix): [list with locations]
Important (should add): [list with suggestions]
Minor improvements: [list]

Proposed additions:
- Appendix A (Notation): [summary of what will be added]
- Appendix B (Glossary): [summary]
- Enhanced definitions: [specific locations]

=== INTUITION ENHANCEMENTS ===
Concepts needing explanation: [list]
Examples to add: [count and list]
Suggested figures: [list and descriptions]

=== PROGRESSIVE COMPLEXITY ===
Theorems to restructure: [list]
Proofs needing sketches: [list]
Simple/General splits: [list]
Recommended appendix structure: [outline]

=== IMPLEMENTATION PLAN ===
Phase 1: Self-containedness fixes (estimated XX changes)
Phase 2: Intuition additions (estimated XX additions)
Phase 3: Restructuring (estimated XX reorganizations)
```

### 4.2 Deliverable Format

Provide:
1. **Annotated version** of the paper with suggestions marked as comments
2. **Rewritten sections** with all enhancements integrated
3. **New appendix content** ready to paste in
4. **Specific line-by-line changes** with explanations

Example annotation format:
```
% [CHANGE 1]: Definition of X is too vague. Replace with:
\begin{definition}[Regularity Condition]
We say that [precise statement].
\end{definition}
For intuition, [explanation]. See Example 2.1.

% [INSERTION 1]: Add example after Definition 3.2
\begin{example}[The case where X=Y]
...
\end{example}
```

---

## Guidelines and Principles

### Balancing Self-Containedness with Length
- **Principle**: Put intuition, extended examples, and detailed proofs in appendices
- **Main text**: Definitions, proof sketches, simple examples, intuitive remarks
- **Appendices**: Full proofs, extended examples, advanced topics, background material

### Writing Style for Intuitive Explanations
- **Do**: Use geometric language, appeal to intuition, give simple cases first
- **Do**: Explain WHY a definition or theorem matters
- **Don't**: Use vague metaphors ("think of it like...") without mathematical substance
- **Don't**: Oversimplify to the point of inaccuracy

### Proof Structure
- **Proof sketches**: Key ideas and main steps, not all details. ~30-50% of full proof length
- **Full proofs**: Every step justified. Can reference lemmas in appendix
- **Examples in proofs**: Where a concrete case illustrates the general argument

### Example Quality
- **Simple example**: Should be verifiable by hand without sophisticated calculations
- **Instructive example**: Should illustrate why assumptions matter or show non-trivial behavior
- **Applied example**: Should connect to real applications or well-known problems

---

## Implementation Priority

Work in this order:

1. **Self-Containedness First** — Get the definitions right and consistent
2. **Intuition Second** — Add explanations and examples once concepts are clear
3. **Complexity Levels Last** — Restructure and organize after content is complete

This ensures each layer builds on the previous one.

---

## Output Files

After enhancement, provide:
- `paper_completed.tex` — Full enhanced paper with appendices
- `CHANGES.md` — Annotated list of all changes and additions
- `appendices_only.tex` — Just the appendix content (can be pasted into original)
- Specific section rewrites with before/after comparisons
