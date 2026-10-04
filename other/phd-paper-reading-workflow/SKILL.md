---
name: phd-paper-reading-workflow
description: Orchestrate Chinese-first PhD application paper reading into per-paper folders under WBG_PhD_Application/03_paper_reading/PaperReading. Use when Codex is asked to read academic papers for PhD/supervisor fit, produce a single deep HTML reading artifact, recommend and confirm reading mode, generate compact long-term research notes, or update topic-organized literature memory only after human confirmation.
---

# PhD Paper Reading Workflow

## Purpose

Use this skill as the controller for application-oriented literature reading. It coordinates:

- `paper-pdf-to-structured-html` for PDF extraction, figure/table coverage, and the self-contained HTML artifact.
- A user-confirmed reading-mode gate before full deep reading.
- A single primary deep-reading artifact: `paper.html`.
- A compact durable Markdown research index: `paper_review.md`.
- A candidate research-memory update that must be approved by the user before any long-term note is modified.
- A topic-organized cumulative literature tree that is updated only after approved merges.
- `codex-completion-loop` as the execution discipline for full delivery and verification.
- `codex-visual-acceptance` when HTML figures, tables, screenshots, or long visual pages need human-visible validation.

The core design principle is: one main reading surface, not several overlapping notes. The user should be able to do first-pass and deep-pass reading primarily from `paper.html`.

## Language And Encoding

Default to Simplified Chinese for all generated reading artifacts unless the user explicitly asks for another language.

Apply these encoding rules to every stage:

- Write generated Markdown, HTML, JSON, and text files as UTF-8.
- For HTML outputs, include `<meta charset="UTF-8">` in the document head.
- For Python file writes or helper scripts, use `encoding="utf-8"` when reading or writing generated text.
- Do not paste mojibake, broken CJK text, or obviously corrupted PDF extraction text into final notes. Mark it as extraction noise and recover from another source when possible.
- Keep technical terms bilingual on first use when helpful, for example `Bayesian Neural Network (BNN, 贝叶斯神经网络)` or `uncertainty quantification (不确定性量化)`.
- Preserve standard English names for papers, datasets, methods, metrics, venues, code identifiers, formulas, and citation keys when translation would reduce precision.

## Windows Chinese Path Handling

When a local path contains Chinese or other non-ASCII characters, avoid passing the literal path through a shell pipeline, heredoc, or inline Python command if the command will be interpreted by a non-UTF-8 console.

Default strategy:

- In Python snippets, construct Chinese path segments with Unicode escapes or code points, for example `"\u6bd5\u8bbe\u76f8\u5173"` instead of pasting `毕设相关` into a PowerShell heredoc.
- Prefer `Path("C:/Users/30254/Desktop").joinpath("\u6bd5\u8bbe\u76f8\u5173", "reference", "BNN\u8865\u5168", "paper.pdf")` for PDF paths under Chinese folders.
- If using PowerShell, prefer `-LiteralPath`, `Resolve-Path -LiteralPath`, and path objects over string-built commands.
- Do not trust mojibake paths copied from older manifests, for example paths containing `姣曡` or `琛ュ`. Re-resolve the real path from the user's provided location or reconstruct it with Unicode escapes.
- When writing manifests, store valid UTF-8 paths, and if there is any chance of console corruption, also store a normalized ASCII-safe field such as `source_pdf_unicode_segments`.
- For temporary extracted text, write to a workspace path with ASCII-only names when possible, then read it with `encoding="utf-8"`.

This rule is especially important for local PDFs under folders such as `毕设相关` or `BNN补全`.
## Output Root

Always place generated paper-reading files under:

`F:\Learning\VSCode Program\WBG_PhD_Application\03_paper_reading\PaperReading\`

Maintain the cumulative literature tree at:

`F:\Learning\VSCode Program\WBG_PhD_Application\03_paper_reading\PaperReading\research_literature_tree.md`

For each paper, create a new folder named from the paper title:

`PaperReading\<sanitized-paper-title>\`

Sanitize the folder name conservatively:

- Keep the recognizable paper title.
- Replace Windows-invalid characters `< > : " / \ | ? *` with spaces or hyphens.
- Collapse repeated whitespace.
- Limit excessive length while preserving the main title.
- If the title is unknown, ask the user before using a guessed title unless a PDF metadata/title extraction is reliable.

## Per-Paper File Contract

Default files for a formal reading folder:

- `paper.html`: the primary, standalone, layered deep-reading artifact. This is the main learning surface.
- `paper_review.md`: compact durable research index for Obsidian/long-term knowledge use; it must not duplicate the full HTML walkthrough.
- `candidate_research_update.md`: proposed updates to accumulated research notes; never merge automatically.
- `manifest.json`: source, extraction, reading-mode recommendation, user confirmation, decisions, uncertainty, and approval status.
- `extraction_manifest.json`: PDF text/figure/table extraction and coverage audit record.
- `assets/`: extracted figures, page renders, crops, and copied local images used by the HTML.

Do not generate `quick_review.md`, `comprehensive_review.md`, `foundation_walkthrough.md`, or `principle_walkthrough.md` by default. Their former functions must be integrated into `paper.html` as sections. Create extra Markdown files only when the user explicitly asks for a separate export or external tool requires it.

Do not scatter generated files directly under `03_paper_reading` or `PaperReading`; every paper gets its own title folder.

## Reading Mode Gate

Before writing the full reading artifacts, make a short recommendation and wait for user confirmation.

The pre-reading recommendation must include:

1. What the paper roughly does in 5-8 sentences.
2. Year, venue/type when available, and why that matters.
3. Content type: survey, foundation/classic, method, system, benchmark, application, critique, or reproduction candidate.
4. Recommended reading mode and brief rationale.
5. A direct confirmation question: use the recommended mode or switch mode.

Available reading modes:

- `foundation`: for surveys, tutorials, classic/foundational papers, and first-contact papers in a new field. Focus on field background, basic principles, motivation, terminology, common routes, common failure modes, and how this paper prepares later reading.
- `frontier-mechanism`: for concrete methods, systems, architectures, algorithms, and recent/frontier papers once the user has basic context. Focus on why the authors designed it this way, what bottleneck each module solves, what would fail without it, design tradeoffs, evidence, and relation to prior routes.
- `reproduction-candidate`: for papers that may be useful as future research or implementation targets. Mark possible reproduction value, missing details, and likely effort, but do not generate a reproduction plan.
- `reproduction`: only when the user explicitly confirms reproduction mode. Then produce reproduction-oriented artifacts or invoke a reproduction workflow if requested.

Never enter `reproduction` mode automatically. It is acceptable to say a paper is a good reproduction candidate, but the reproduction plan itself requires explicit user confirmation.

If the user has already clearly specified the mode in the same request, record that as the confirmation and proceed.

## `paper.html` Contract

`paper.html` is the single primary deep-reading document. It must explain the paper, not merely summarize it or point back to the PDF.

It should be long enough to teach the paper, but structured enough to remain readable. Do not build it by dumping several Markdown files into one page. Generate it section by section and remove overlap.

Required sections, adapted to the confirmed reading mode:

- `30 秒定位`: title, authors, year/venue, paper type, recommended/confirmed reading mode, and why the paper matters.
- `这篇文章做了什么`: concise but concrete overview of the paper's contribution.
- `领域背景与问题动机`: what problem space this belongs to, why the problem matters, and what bottleneck or knowledge gap motivates the work.
- `基础概念与前置知识`: especially important for `foundation`; explain terms and assumptions needed before reading the method.
- `作者思路 walkthrough`: reconstruct the path from naive solution to the paper's design. Explain why each step is introduced.
- `核心原理 / 方法机制`: explain the key algorithm, architecture, system, dataflow, mathematical model, or experimental logic in plain language with precise technical terms.
- `关键图表逐图讲解`: include important figures/tables from `assets/`; for each, explain what to look at, how data/control flows, what claim it supports, and what it does not prove.
- `实验与证据链`: map claims to datasets/tasks/baselines/metrics/results and explain whether the evidence supports the claims.
- `设计取舍、局限与容易误解之处`: include author-stated limits, inferred limits, and common misreadings.
- `快速复习卡片`: short recall bullets and self-test questions; this replaces the old default `quick_review.md`.
- `导师交流准备`: likely supervisor questions and concise answers; this replaces the old default `comprehensive_review.md`.
- `后续阅读 / 研究连接`: how this paper connects to the user's PhD direction, adjacent papers, open questions, and whether it is only a reproduction candidate.

Mode-specific emphasis:

- In `foundation`, spend more space on field map, terminology, motivation, historical role, and common technical routes.
- In `frontier-mechanism`, spend more space on design causality, module-level rationale, tradeoffs, ablation evidence, and what changed relative to prior work.
- In `reproduction-candidate`, add a compact section on reproducibility signals and missing implementation details, but do not produce a full reproduction plan.
- In `reproduction`, add or link a user-confirmed reproduction plan.

## `paper_review.md` Contract

`paper_review.md` is a compact long-term research index, not a second deep-reading note.

It should contain:

- Paper identity and source link back to `paper.html`.
- Confirmed reading mode.
- One-sentence contribution.
- Research-topic branch placement.
- Key claims and the strongest evidence for each.
- Relation to nearby papers or directions.
- Reusable ideas for the user's research.
- Open questions or limitations worth remembering.

It should not repeat the full walkthrough, figure-by-figure explanation, quick review layer, or supervisor Q&A. Those belong in `paper.html`.

## Candidate Research-Memory Updates

Write `candidate_research_update.md` from `references/candidate-update-template.md` when a paper has possible long-term value.

Include target topic-tree branch, proposed additions, source evidence, confidence, relation type, and merge risk. Mark every proposed update as `status: candidate`.

Do not edit `research_literature_tree.md`, long-term notes, MOCs, supervisor-fit notes, or accumulated research summaries without explicit approval in the current conversation.

## Cumulative Literature Tree Contract

Keep one primary cumulative tree organized by research topic, not by supervisor, chronology, or source folder. The tree is the user's approved research memory map, so only user-approved items may enter it.

Use `research_literature_tree.md` for:

- Top-level research areas.
- Subtopics and method branches.
- Key papers attached to the most relevant branch.
- One-line contribution and evidence summary for each merged paper.
- Relationship labels such as `foundation`, `method`, `benchmark`, `survey`, `application`, `critique`, or `open-problem`.
- Open questions and gaps that survive across papers.

Do not create parallel supervisor/lab indexes unless the user explicitly asks later. The default is a single topic tree to avoid maintenance drift.

## Workflow

1. Identify the paper and target folder.
   - Accept local PDF path, DOI, arXiv URL/ID, paper title, or existing extracted notes.
   - Resolve title, authors, venue/year, and source provenance.
   - Create `PaperReading\<sanitized-paper-title>\`.

2. Extract and inspect before deep writing.
   - Use `paper-pdf-to-structured-html` when available; load and follow its `SKILL.md` for PDF extraction and figure/table coverage.
   - Audit embedded images and vector/page-crop candidates so important figures are not silently lost.
   - Record extraction details in `extraction_manifest.json`.

3. Run the reading-mode gate.
   - Present the short paper summary and recommended mode.
   - Wait for user confirmation unless the user already specified the mode.
   - Record recommendation, rationale, and confirmation in `manifest.json`.

4. Plan the HTML structure.
   - Create a section outline matched to the confirmed mode.
   - Ensure quick recall and supervisor-Q&A content are sections of `paper.html`, not separate default MD files.

5. Generate `paper.html` section by section.
   - Use Simplified Chinese by default and include `<meta charset="UTF-8">`.
   - Preserve English paper titles, methods, datasets, metrics, venues, and code identifiers.
   - Include important figures/tables from `assets/` with explanatory captions.
   - Explain principle, motivation, mechanism, design choices, evidence, and limitations.

6. Generate compact `paper_review.md`.
   - Use `deeppapernote` only if it can respect this compact-index contract and output location.
   - If unavailable or too verbose, produce the compact index directly using `references/research-note-template.md` as a loose guide, not a mandate to duplicate HTML.

7. Generate candidate research-memory updates.
   - Write `candidate_research_update.md` from `references/candidate-update-template.md`.
   - Keep proposed updates separate and unmerged until user approval.

8. Verify.
   - Check file presence and absence of deprecated default MD files unless explicitly requested.
   - Check all HTML image links exist.
   - Check HTML parses and contains the required sections.
   - Use `codex-visual-acceptance` for screenshot/browser validation when figures/tables or layout quality matter.
   - If using `codex-completion-loop`, finish only after these checks pass or blockers are explained.

9. Ask for user approval before merging long-term memory.
   - Present a concise summary of proposed updates.
   - Ask which updates to approve, reject, revise, or mark as pending.
   - Ask before creating a new top-level research area.

10. Merge only approved updates.
   - Preserve source links back to `paper_review.md` and `paper.html`.
   - Mark merged items as `approved` or `merged` with date and source paper.
   - Keep rejected or pending items recorded in `candidate_research_update.md`.
   - Update `research_literature_tree.md` in the same merge step using `references/literature-tree-template.md` if the tree does not exist yet.

## Confirmation Gates

Ask the user before proceeding when:

- The reading mode has not been confirmed and the user did not explicitly specify one.
- The paper title is ambiguous and would determine the folder name.
- The workflow would enter `reproduction` mode or create a reproduction plan.
- A proposed update would modify an existing long-term note or supervisor-fit summary.
- A proposed update would modify `research_literature_tree.md`.
- A proposed update would create a new top-level research area in the tree.
- A paper appears weakly related to the current research direction.
- The workflow would create many new concept notes or extra output files.
- Evidence is insufficient and the note would require speculation.
- The user has not defined the destination for approved accumulated notes.

Do not ask before low-risk actions such as creating the per-paper folder, extracting PDF text, auditing figures, drafting `paper.html`, drafting compact `paper_review.md`, or writing candidate updates after mode confirmation.

## Research-Memory Rules

- Treat long-term notes as user-approved research memory, not a scratchpad.
- Distinguish paper claims, author evidence, and Codex inference.
- Never turn a single paper's claim into field consensus unless the source supports that.
- Prefer `supports`, `extends`, `contrasts`, `background`, or `weakly-related` relation labels.
- Use confidence labels: `high`, `medium`, `low`, or `needs manual check`.
- Keep source provenance close to every durable claim.
- Keep the cumulative literature tree compact: one paper should add a small branch entry, not a full paper review duplicated from `paper.html`.
- Preserve unsettled disagreements as explicit `open question` or `conflict` entries instead of forcing a fake synthesis.

## Auxiliary Skill Policy

Use auxiliary skills as execution support, not as a reason to create more overlapping files:

- Use `codex-completion-loop` when the user asks Codex to carry the reading workflow through implementation, verification, and final evidence.
- Use `codex-visual-acceptance` when `paper.html` has important figures/tables or visual readability matters.
- Use `codex-consensus-plan` before major workflow redesigns.
- Do not invoke paper reproduction skills unless the user explicitly confirms `reproduction` mode.

## DeepPaperNote Integration

If `deeppapernote` is installed, load and follow its `SKILL.md` only for the compact research-index stage, while overriding its output location and verbosity with this controller:

- Output must remain under `PaperReading\<sanitized-paper-title>\`.
- The durable note must be named `paper_review.md` unless the user asks otherwise.
- `paper_review.md` must remain compact and must not duplicate the full HTML deep reading.
- Candidate updates must remain separate and require approval.

If `deeppapernote` cannot comply with the compact-index contract, write `paper_review.md` directly.

## References

Read only the references needed for the current stage:

- `references/research-note-template.md`: compact durable research-index structure.
- `references/candidate-update-template.md`: approval-gated research-memory diff.
- `references/literature-tree-template.md`: topic-organized cumulative literature tree.
- `references/quick-review-template.md`: legacy quick review template; use only when the user explicitly requests a separate `quick_review.md` export.
- `references/comprehensive-review-template.md`: legacy comprehensive review template; use only when the user explicitly requests a separate `comprehensive_review.md` export.

