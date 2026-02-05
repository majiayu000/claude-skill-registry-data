---
name: obsi-knowledge-refiner
description: Standards for elevating raw notes to Gold Standard knowledge assets.
---

# Knowledge Refiner Standards

## Core Principles
**"Gold Standard or Nothing"**
To move notes from "Transient" to "Permanent" status by adding structure, depth, connectivity, and hygiene.

## Quality Standards (The Gold Standard)
1.  **Definitions**: Must be clear and jargon-free (ELI5 if needed).
2.  **Examples**: Concrete code snippets or real-world use cases are mandatory.
3.  **Comparisons**: contrast with similar concepts (e.g., `Thread` vs `Process`).
4.  **Insights**: Must conclude with "Key Takeaways" or "Pattern recognition".
5.  **External Validation**: Key claims must be backed by official docs or reputable engineering blogs.

## Refinement Modes
- **Standardize**: Apply `concept-template.md`.
- **Enrich (Search & Analyze)**: Proactively search the web to fill content gaps.
- **Elaborate**: Add depth to weak sections.
- **Link**: Auto-link to existing concepts in `20_Learning` ONLY. **Do NOT link to `90_Archive` or `Projects`.**
- **Prune (Cleanup)**: Detect and remove links to non-existent files (Dead Links).
- **Convert (Notebooks)**: If target is `.ipynb`, perform **Deep Conversion**:
  - **Structure**: Maintain original headers and markdown logic.
  - **Code**: Include all executable Python code in code blocks.
  - **Outputs**: Capture key text outputs (print, dataframes) in blocks.
  - **Images**: Describe the content/trend of charts if extraction is not possible.
  - **Synthesis**: Add analysis/explanation for "Why this result matters".
- **Integration Protocol**:
- **Integration Protocol**:
  - **Merge**: If the notebook covers an existing concept, merge findings into the existing note's "Examples" section.
  - **Auxiliary**: Otherwise, rename to `{Concept}_Lab.md` and link it as auxiliary material.
  - **Plan Cleanup**: If `Plan_*.md` exists alongside the Content Note:
    - **Absorb**: Move useful context (Objectives, TODOs) to the Content Note.
    - **Delete**: Delete the Plan file (Maintain 1 Source of Truth).

## Research Standards
- **Source Selection**: Official Docs > Engineering Blogs > StackOverflow.
- **Citation**: Add `## References` with links.

## Checklist
- [ ] **Structure**: Does it follow the Concept Template?
- [ ] **Hygiene**: Are there any dead links (`[[Red Link]]`)?
- [ ] **Validation**: Are external claims cited?

