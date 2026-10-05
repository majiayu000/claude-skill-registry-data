---
name: checkpro
description: Audit essays, reports, literature reviews, dissertations, proposals, and source-backed assignments for high-score academic quality. Use when the user asks whether a paper can get a high grade, wants teacher/rubric feedback addressed, needs a pre-submission review, or needs checks for strict rubric compliance, academic standards, prompt/rubric alignment, argument quality, comparative analysis, evidence hierarchy, table/figure integration, citation specificity, conclusion strength, academic language, source-claim integrity, or evidence boundaries.
---

# CheckPro

Use this skill to find grade-relevant academic weaknesses that ordinary formatting, citation, or completeness checks miss. The goal is to identify whether a written assignment is only complete or is actually strong enough to target a high score.

Do not promise a grade. Give a conservative quality judgement and a targeted repair plan.

High-score readiness is a blocking judgement, not a courtesy label. If a fixable weakness remains in prompt alignment, rubric coverage, evidence support, analysis depth, citation integrity, or final argument quality, do not call the work high-score ready or `90+ plausible`.

## Inputs

Prefer, in this order:

1. assignment brief, rubric, marking criteria, or teacher feedback
2. current `.docx`, `.pdf`, Google Doc text, or pasted draft
3. source list or reference list
4. any rewriting constraints, if relevant

If no rubric is available, infer the likely academic criteria from the genre and state that the audit is rubric-inferred.

If the prompt, rubric, or assignment question is unavailable and the document's required task cannot be reconstructed confidently, do not give a `90+ plausible` judgement. Mark prompt/rubric alignment as unresolved and ask for the missing brief or audit only against inferred criteria.

## Default Audit Order

Run the audit in this order unless the user asks for a narrower check:

1. reconstruct the exact assignment task
2. build a rubric ledger from the brief, rubric, marking criteria, teacher feedback, and required format rules
3. map the draft against each rubric item
4. check academic standards and formatting conventions
5. check source-claim integrity for the major claims
6. check argument quality, synthesis, visuals, and conclusion strength
7. give the most conservative score-risk judgement
8. produce a targeted repair plan

Do not start with a broad quality impression. The rubric and academic-standard checks control the final judgement.

## Rubric Compliance Ledger

When a rubric, marking criteria, assignment brief, teacher feedback, or required question is available, create a rubric ledger before judging quality.

Each rubric item should be separated into a distinct check with:

- `criterion`: the exact requirement, question, or marking criterion
- `source`: where it came from, such as rubric row, brief line, teacher comment, or template requirement
- `weight_or_importance`: explicit mark weight if provided, otherwise inferred importance
- `draft_location`: section, paragraph start, page, table, figure, or appendix where the answer appears
- `status`: `pass`, `partial`, `fail`, or `not assessable`
- `evidence`: why the status was assigned
- `repair`: the smallest fix needed if status is `partial`, `fail`, or `not assessable`

Rubric rules:

- do not merge multiple rubric criteria into one broad judgement
- do not treat a general discussion as satisfying a specific required question unless the answer is visible and direct
- do not call the paper high-score ready if any high-weight rubric item is `fail` or `not assessable`
- do not call the paper `90+ plausible` when multiple low- or medium-weight rubric items remain `partial`
- if no rubric is provided, create a `rubric-inferred` ledger and mark the limitation clearly
- if teacher feedback exists, treat each actionable feedback point as a rubric item until it is addressed or explicitly not applicable

## Academic Standards Gate

Check academic conventions as a strict gate, not as cosmetic polish.

The audit must verify when relevant:

- citation style is identified from the assignment rather than guessed
- in-text citations and reference-list entries match each other
- reference-list ordering, punctuation, capitalization, italics, hanging indents, numbering, or superscripts match the required style when assessable
- source author names, initials, years, titles, journal/proceedings/book details, DOI/URL, and access details are not simplified or invented
- every borrowed idea, statistic, definition, method, framework, table, figure, or distinctive claim is cited
- paragraphs follow academic reasoning: claim, evidence, analysis, and implication
- core terms, scope boundaries, comparison criteria, methodology, and framework choices are defined before evaluative claims use them
- headings, captions, tables, figures, appendices, page layout, word count, and file format follow the brief or template
- figures and tables are referred to in the text, captioned correctly, and interpreted in prose
- figures in papers do not duplicate the title inside the image when an external figure caption already supplies it
- language is formal, precise, and field-appropriate without generic filler or unsupported exaggeration

If an academic-standard defect is visible and fixable, treat it as a repair item before high-score signoff.

## Source-Claim Integrity Gate

For source-backed work, audit the relationship between important claims and sources.

At minimum, check:

- major factual, empirical, evaluative, and comparative claims have suitable support
- the cited source actually supports the specific claim attached to it
- the claim preserves the source's direction, magnitude, units, sample, method, population, date range, and conditions when they matter
- broad wording such as `better`, `effective`, `significant`, `sustainable`, `high quality`, or `improved` is tied to a measured or clearly defined outcome
- review articles are not misused as proof of a specific product, intervention, dataset, or formulation result unless they actually contain that evidence
- commercial pages, marketing copy, screenshots, and labels are not used as proof of scientific, nutritional, technical, performance, or sustainability superiority without measured evidence
- uncited claims that would affect the grade are flagged
- suspicious, decorative, mismatched, or invented-looking citations are flagged rather than accepted

If the source text is not available, mark the source-claim check as limited or not assessable. Do not assume the citation supports the claim.

## Audit Gates

Check the document against these gates before calling it high-score ready.

### 1. Prompt, Rubric, And Task Alignment

- The thesis, research question, or central judgement directly answers the assignment prompt.
- Every rubric criterion, required question, and required sub-part has a visible answer in the body.
- The paper does not merely orbit the topic while missing the exact task.
- Required structure, methodology emphasis, case context, word-count expectations, source requirements, and format constraints are traced to the draft when available.
- If any required element is inferred rather than confirmed, that uncertainty is stated and treated as a score risk.

### 1A. Claim, Evidence, And Boundary

- The document states what the work actually demonstrates, argues, or concludes rather than only naming the topic area.
- The main evidence supporting the central claim is visible and proportionate to the importance of that claim.
- The boundary, limitation, or condition where the central claim stops is explicit when the topic requires evaluation, scientific caution, or method-specific interpretation.
- For scientific or manuscript-style work, the paper/report type is identified clearly enough that the argument matches the genre: mechanism, method, resource, benchmark, clinical, engineering, review, or another relevant type.

### 2. Thesis And Judgement

- The central claim is visible early.
- The paper makes a judgement, not just a topic tour.
- The argument answers the assignment question directly.
- The conclusion returns to the central judgement without adding unsupported new claims.

### 3. Section-Level Analytical Purpose

- Every major section has a clear analytical job, such as defining criteria, comparing evidence, applying theory, interpreting data, testing feasibility, or deriving implications.
- For scientific manuscript-style work, sections follow recognizable jobs such as context/problem, gap, approach/design, evidence, interpretation, implication, and limitation rather than reading like a chronological lab diary.
- Headings reflect the argument sequence, not just topic labels.
- No major section remains as generic background filler.
- Background material is limited to what the later analysis actually uses.
- Appendices support the main text and do not substitute for missing analysis.

### 4. Paragraph-Level Reasoning

- Analytical paragraphs connect claim, evidence, and implication.
- Paragraphs explain causes, trade-offs, limits, consequences, or application rather than only describing a source.
- Citations are not used as decoration after broad descriptive statements.
- Topic sentences make the purpose of the paragraph clear.
- Transitions make the argument traceable from prompt to conclusion.

### 5. Comparative Analysis

- Literature is compared across common criteria, not listed source by source.
- Approaches, cases, theories, products, or methods are evaluated against shared dimensions.
- Differences in evidence strength, limitations, feasibility, or context are made explicit.
- The paper explains why one approach is stronger, weaker, or more conditional than another.

### 6. Literature Patterning And Synthesis

- Literature coverage identifies patterns, disagreements, evidence strength, and gaps.
- The synthesis explains how sources relate to each other rather than reporting them one by one.
- Review papers are used for framing and synthesis, not as proof that a specific product, intervention, or formulation works.
- The paper distinguishes established findings from tentative, context-specific, or contested claims.
- Source clusters are organized by analytical criteria, not by the order in which sources were found.

### 7. Visual And Table Integration

For every meaningful table, figure, chart, diagram, or model:

- the visual has a clear label or caption when the genre expects it
- charts or figures embedded in essays, papers, theses, or report-style documents do not repeat the figure title inside the image when an external `Figure X. ...` caption or surrounding prose already names the figure
- removing a duplicate internal chart title must not remove necessary axis labels, legends, tick labels, units, or data annotations
- nearby prose explains what the visual shows
- nearby prose draws a conclusion from it
- the visual advances the argument rather than acting as a decorative or raw information dump
- the table/figure is referenced in the text by name or number when appropriate
- for multi-panel figures, the panels have distinct analytical roles rather than repeating the same question in slightly different forms without a clear reason

Treat this as a high-score blocker for reports and literature reviews. A table that is useful but not interpreted is incomplete as evidence.

### 8. Evidence Hierarchy And Source Quality

- High-stakes factual, scientific, technical, policy, or performance claims rely on peer-reviewed, guideline, official, primary-data, or otherwise authoritative evidence when available.
- Lower-quality evidence may support context, market positioning, examples, availability, or practitioner perspective, but should not carry the main proof burden.
- The source base is recent enough for the topic unless older sources are seminal, foundational, method-defining, guideline-level, or explicitly required.
- Key claims are not over-dependent on a single weak source.
- Claims based on local files, screenshots, interviews, or classroom material are identified with the correct evidence boundary.

### 9. Evidence And Citation Specificity

- Each major factual or evaluative claim is supported by a suitable source.
- Claims such as `better performance`, `improved stability`, `higher quality`, `more effective`, or `more sustainable` identify the measured outcome when possible.
- The stated outcome matches what the cited study actually measured.
- Numerical and empirical claims preserve direction, magnitude, units, groups, experimental conditions, and comparison baselines when those details affect interpretation.
- Product pages, labels, websites, and marketing material are used only for market positioning, ingredient examples, or availability unless they contain measured evidence.
- Every citation corresponds to a real source actually used, and the attached claim is one the source can support.
- Decorative, mismatched, or authority-padding citations are treated as defects.

### 10. Critical Evaluation And Boundaries

- Contrary findings, limitations, uncertainty, trade-offs, or boundary conditions are acknowledged where the topic or rubric expects evaluation.
- The paper does not present advocacy as analysis when the evidence is mixed.
- Scope boundaries are clear: population, geography, period, method, industry, product type, dataset, or case limits are named when relevant.
- Key terms, comparison criteria, framework choices, and methodology assumptions are defined before they are used to make evaluative claims.
- The strength of the conclusion matches the strength of the evidence.

### 11. Theory, Framework, Method, Or Course-Concept Application

- When the assignment provides theories, frameworks, methods, models, course concepts, or case context, the paper applies them explicitly.
- Concepts are used to interpret evidence, not only named in passing.
- Method choices are justified when methodology affects the result.
- The analysis shows how the framework changes the judgement or interpretation.
- Course-specific language is used accurately and sparingly.

### 12. Repetition And Development

- A central mechanism or framework is stated clearly once.
- Later sections develop it through comparison, evidence, application, or limitation.
- Repeated explanations are compressed unless repetition is necessary for section logic.
- Paragraphs have distinct functions rather than restating the same controlling idea.

### 13. Academic Register And Precision

- Remove mistranslated idioms, casual phrasing, machine-like transitions, and grammar defects that reduce credibility.
- Replace vague academic filler with precise claims.
- Keep technical terms consistent.
- Do not over-polish into generic AI-like prose when the user has a low-AI-rate workflow; prioritize correctness and clarity, then let the user's rewriting workflow handle style if requested.
- Avoid turning measured results into vague adjectives.
- Preserve author, source, method, and outcome precision where it affects the claim.
- Calibrate claim verbs and hedging to the evidence strength; flag unsupported absolutes, unwarranted causation, and unverified priority or novelty claims.

### 14. Structure And Navigation

- Long documents include a table of contents when useful or expected.
- Headings match the argument sequence, not just topic labels.
- Tables, figures, references, and appendices are placed where they help the reader.
- Appendices support the main text and do not substitute for missing analysis.

### 15. Conclusion Quality

- The conclusion is shorter and sharper than the analysis.
- It states the final judgement directly.
- It names the conditions, limits, or implications that matter most.
- It avoids repeating every section summary.
- It answers the original prompt.
- It does not introduce unsupported new claims.

## High-Score Readiness Rule

Only call a submission high-score ready or `90+ plausible` when all relevant audit gates are passed or any remaining issue is truly not applicable to the assignment.

Use the most conservative credible judgement:

- if a plausible lower reading remains, use the lower risk judgement
- if prompt/rubric alignment is unresolved, do not call the paper `90+ plausible`
- if evidence support is uncertain, mark it as a score risk rather than assuming the citation works
- if a weakness is fixable, treat it as a repair item before high-score signoff
- if a gate is not applicable, state why instead of silently skipping it
- if any high-weight or central rubric criterion is `fail` or `not assessable`, do not call the paper high-score ready
- if academic-standard compliance cannot be checked because the required style, rubric, source list, or actual file is missing, state the limitation and avoid strong score claims
- if source-claim integrity is uncertain for major claims, cap the judgement at risk-bearing review status rather than `90+ plausible`

## Scoring Discipline

The score judgement must be conservative and evidence-led.

Use these labels unless the user asks for another scale:

- `Low score risk`: all central rubric items pass, academic standards are clean or only minor, and source-claim support is credible
- `Medium score risk`: the paper is mostly complete but has partial rubric coverage, shallow analysis, citation/style issues, weak synthesis, or source-claim uncertainty
- `High score risk`: central rubric criteria are missing, key claims are unsupported, academic standards are visibly broken, or the paper does not answer the task directly
- `Not assessable`: the prompt/rubric, draft, source base, or file format evidence is too incomplete to judge honestly

Do not convert these labels into a guaranteed grade. If giving an estimated band, make it conditional and explain which evidence controls the lower bound.

## Output Format

Return findings in this order:

1. **Score Risk:** conservative estimate such as `high`, `medium`, or `low` risk of losing marks, with one sentence explaining why.
2. **Priority Fixes:** ordered list of the smallest changes with the biggest grade impact.
3. **Rubric Ledger:** criterion-by-criterion `pass / partial / fail / not assessable` when a rubric, brief, required question, or teacher feedback is available.
4. **Academic Standards:** citation style, in-text/reference matching, formatting, structure, figures/tables, and academic register risks.
5. **Source-Claim Integrity:** major unsupported, overbroad, mismatched, or not-assessable claims.
6. **Specific Locations:** section names, table numbers, paragraph starts, or file/page references where possible.
7. **Gate Results:** pass/risk/fail/not-applicable judgement for the relevant audit gates when the user asks for a full check or high-score judgement.
8. **What Not To Change:** content that is already strong and should be preserved.
9. **Repair Plan:** concise sequence for revising without unnecessary rewriting.

If the user asks you to edit the document, make targeted changes rather than rewriting the whole paper. Preserve source meaning and citation boundaries.

## High-Score Blockers

Treat these as blockers for a `90+ plausible` judgement unless the assignment explicitly does not care about them:

- prompt, rubric, required question, or required sub-part coverage is missing or cannot be verified
- any high-weight or central rubric criterion is `fail` or `not assessable`
- multiple rubric criteria remain only partially satisfied
- teacher feedback was provided but actionable items are not visibly addressed
- the thesis or central judgement does not directly answer the assignment prompt
- major sections have no analytical purpose beyond background description
- paragraphs describe sources without explaining implications, trade-offs, limits, or consequences
- tables or figures are inserted but not interpreted
- embedded paper/report figures repeat the same title inside the chart image and again in the external figure caption, unless the assignment/template explicitly requires that duplication
- literature is summarized but not compared
- literature review sections are source-by-source catalogues with no pattern, disagreement, evidence-strength, or gap synthesis
- the conclusion repeats the body instead of stating a final judgement
- claims are broader than the evidence supports
- high-stakes claims rely on weak evidence when stronger evidence is required or available
- source-claim support for major factual or evaluative claims cannot be verified
- in-text citations and reference-list entries do not match
- required citation style or academic formatting is visibly inconsistent
- numerical or empirical claims lose important direction, magnitude, units, groups, conditions, or baselines
- commercial or marketing sources are used as proof of scientific, nutritional, sensory, performance, or sustainability outcomes
- required theories, frameworks, course concepts, methods, or case context are mentioned but not applied
- limitations, counterarguments, uncertainty, or trade-offs are absent when the task expects evaluation
- citations are decorative, mismatched, invented, or attached to claims the source does not support
- repeated central ideas crowd out new analysis
- visible grammar or phrase errors weaken academic professionalism
- rubric requirements are missing, inferred incorrectly, or not traced to the final document
