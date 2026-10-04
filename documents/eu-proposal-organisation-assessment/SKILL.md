---
name: eu-proposal-organisation-assessment
description: >-
  Assess a named organisation's role in a Horizon Europe or LIFE proposal.
  Cover leadership, major contributions, partner boundaries, outputs, required technologies and expertise, methodology links, effort, and timing.
  Produce a clear Markdown report with Mermaid journey and Gantt diagrams.
  Do not use for general proposal scoring or evaluation.
---

# EU Proposal Organisation Assessment

Produce a clear, evidence-based account of one organisation's role in a Horizon Europe or LIFE proposal.

The report must answer five questions:

1. Where does the organisation lead or make a major contribution?
2. What is it expected to deliver in practical terms?
3. What technologies and domain knowledge must it bring?
4. Where do its responsibilities stop and another partner's begin?
5. How does its work move through the project from early inputs to final use?

## Inputs

Require:

- the proposal document or documents;
- the target organisation's legal name, acronym, or both.

Accept an optional output path, user-defined scope, and `project_start_date` in `YYYY-MM-DD` format. Use a supplied start date for the Gantt's real calendar timeline; otherwise use a confirmed proposal start date, then the relative-calendar fallback. If the user gives no scope, analyse core roles in depth. Summarise smaller named roles separately. Omit routine all-partner participation from the main assessment.

Discover aliases from participant tables and partner descriptions. Confirm that each alias refers to the same organisation before combining matches.

## Method

Read [references/analysis-method.md](references/analysis-method.md) before analysing the proposal. Follow its evidence and inclusion rules. Use its boundary method and fallback rules.

Read the full proposal. Do not stop after searching for the organisation's name. Roles may be spread across work-package tables, deliverables, effort tables, methodology sections, exploitation plans, and partner descriptions.

Build an internal evidence map before writing. For each possible role, record:

- work package, task, deliverable, milestone, or result;
- formal lead;
- the target organisation's exact stated duty;
- other partners' stated duties;
- timing and effort, when available;
- linked methodology Element, objective, component, result, or key exploitable result;
- required technologies, standards, or domain knowledge, and whether each is stated or implied;
- source location;
- role level: core, supporting boundary, or routine mention.

Resolve differences by reporting them, not by silently choosing one statement. A formal task lead may still build only one subsystem. State both the formal accountability and the detailed implementation split.

Build a separate internal register of every deliverable and milestone formally led by the target organisation, including items outside the core-role assessment. Record its ID, title, timing, practical output, and source.

## Output

Use [references/report-template.md](references/report-template.md). Produce a self-contained Markdown report in the user's language unless asked otherwise.

The report must include:

- a plain-language conclusion near the top;
- the core WP and task assessment;
- explicit responsibility boundaries with named partners;
- links to the proposal's methodology concepts;
- the technologies and domain knowledge the organisation must bring, with the basis for each;
- the organisation's journey through the project;
- a GitHub-compatible Mermaid flowchart;
- a GitHub-compatible Mermaid Gantt;
- a concise list of every milestone and deliverable led by the organisation;
- smaller downstream or supporting roles;
- a final statement of what the organisation does and does not own;
- evidence limitations when the source is incomplete or inconsistent.

## Writing standard

Write for a project manager who has not read the proposal.

- Use short sentences with one main idea.
- Prefer active voice and ordinary words.
- Define acronyms and specialist terms on first use.
- Explain technical names in one short phrase.
- Paraphrase dense proposal language. Do not reproduce bureaucratic prose.
- Separate formal leadership from actual implementation.
- Use bullets and tables for repeated comparisons.
- Keep paragraphs short.
- Split any sentence carrying more than two distinct claims.
- Preserve precision. Do not remove nuance that changes responsibility or ownership.

Before delivering, perform the clarity review in the report template. Rewrite any section that requires the reader to unpack a long sentence or infer who does what.

## Evidence discipline

- Do not infer ownership from a participant list alone.
- Do not use person-months as the sole reason to call a contribution major.
- Do not invent missing dates, deliverables, methodology links, or partner duties.
- Do not derive a required capability from the organisation's sector, track record, or capacity description.
- Do not list a technology that only another partner's duty requires.
- Distinguish proposal facts from reasonable interpretation.
- Cite task IDs, deliverable IDs, table names, section names, or reliable page numbers close to the relevant claim.
- State when OCR, conversion, missing tables, or inconsistent drafting limits confidence.
