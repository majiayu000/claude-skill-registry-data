---
name: feishu-visual-notes
description: Analyze, create, or update structured visual notes from complete classroom PPTs, OCR screenshots, image-based handouts, lecture transcripts, mock-interview transcripts, and Feishu/Lark documents. Use when the user asks to organize course material, preserve or edit an existing Feishu document, mark retrieval-critical points, add course-grounded extensions or interview questions, or build editable Feishu whiteboards using the relationship-appropriate flow, loop, hierarchy, timeline, comparison, decision, swimlane, funnel, quadrant, or cause-effect layout. On first Feishu use, scan runtime MCP/plugin capabilities and guide the user through any missing CLI, whiteboard, authentication, or permission setup before reading or writing documents.
---

# Feishu Visual Notes

## Goal

Turn the complete source into faithful, structured notes with only the editable diagrams that materially reduce comprehension cost.

## First-Use Capability Gate

Before the first Feishu read or write on a computer:

1. Inspect the host's available MCP, connector, app, and plugin tools for Feishu/Lark document read, document write, and editable-whiteboard capabilities.
2. Record verified runtime capabilities using the schema in `references/runtime-capabilities.md`. Do not infer capabilities from a plugin name alone.
3. Run `python scripts/preflight.py --check-feishu --interactive --save`; use `python3` on macOS when `python` is unavailable. Pass `--capabilities-file` when a runtime report was created.
4. If required tools are missing, show the platform-specific installation and authentication instructions emitted by preflight, then rerun the check.
5. Do not silently install software, copy credentials, authenticate an account, or switch between CLI, MCP, user, and bot identities.
6. Select the Feishu backend before accessing user data. The CLI path is the tested default. Use an MCP path only when all required capabilities were verified and the user approved that path.
7. For local-only analysis with no Feishu access, run `python scripts/preflight.py --offline` and continue when it passes.

Run the shorter noninteractive preflight on later Feishu tasks as a smoke check. Show the full setup guide again whenever a required capability becomes unavailable.

## Select the Operating Mode

Choose exactly one mode before taking action.

1. **Analyze mode**
   - Use when the user asks to scan, inspect, review, or show the framework first.
   - Read the complete source and report the proposed framework only.
   - Do not create or update a Feishu document.

2. **Create mode**
   - Use when the user asks for a finished deliverable and does not ask to modify an existing document.
   - Create one new enhanced document and leave the source unchanged.

3. **Update mode**
   - Use when the user explicitly says to edit the source, original, current, or existing document.
   - Fetch the latest version immediately before editing and update that same document only.
   - Preserve the user's deletions, rewrites, manual formatting, and unrelated sections.
   - Patch only the requested blocks or sections. Do not recreate the document, create a replacement document, or restore previously deleted content.
   - Verify after writing that the document token is unchanged.

Treat a request for a deliverable as Create mode unless it explicitly identifies an existing document as the write target. Treat a request to "先扫描/先看看/先梳理" as Analyze mode.

## Hard Rules

- Read the entire source before producing final notes. Do not infer the theme from early pages or sections.
- Preserve source meaning. Reorder only to repair hierarchy, duplication, or clear logical jumps.
- Ignore non-course content in screenshots: physical whiteboards, blackboards, handwriting, classroom background, app chrome, chat windows, borders, and clutter.
- Mark unresolved OCR as `识别不确定`; do not guess.
- Keep source-derived notes, extensions, and interview content visibly separate. Never present an extension as an original course statement.
- Highlight every distinct retrieval-critical concept, conclusion, condition, threshold, risk, and method choice. Never highlight headings, whole paragraphs, repeated occurrences, or non-essential connective text.
- Do not create diagrams as decoration. Make each diagram answer one concrete comprehension question.
- Do not force every relationship into one diagram type or visual style. Select both the diagram type and its layout variant from the source relationship.
- Prefer prose or a table when it communicates the relationship more clearly than a diagram.
- For Feishu diagrams, use editable SVG whiteboards. Do not insert Mermaid as a code block.
- Never silently replace editable whiteboards with PNG/JPEG images, text arrows, Markdown diagrams, or another non-editable format.
- Never switch from user identity to bot identity without explicit user approval.
- Never improvise a different write path or output format after a failure. Follow the failure policy below.

## Source Completion Gate

Maintain an internal coverage record before outlining.

For PPTs or image sets, record:

- total page/image count;
- original order;
- pages successfully read;
- pages inspected at original resolution;
- pages containing `识别不确定`;
- pages containing important tables, formulas, or diagrams.

For Feishu documents or transcripts, record:

- resolved document token and current revision when available;
- complete heading/section inventory;
- sections successfully fetched and reviewed;
- unresolved blocks or inaccessible attachments.

Do not proceed to final writing until all available pages or sections have been reviewed. If part of the source is inaccessible, state the exact missing range and stop before claiming a complete result.

For sources with more than 40 pages/images, or whenever one-pass review is unreliable:

- Split the source into ordered, non-overlapping batches while retaining original page numbers.
- Save one structured OCR/output file per batch.
- Maintain the manifest defined in `references/workflow-spec.md`.
- Run `scripts/audit_batch_manifest.py --strict` before merging batches or building the final framework.
- Do not treat batch completion as source completion until the manifest has no missing or overlapping pages and every uncertain or important visual page has been checked at original resolution.

## Workflow

1. **Preflight**
   - Select Analyze, Create, or Update mode.
   - Complete the first-use capability gate when required.
   - For Feishu work, locate the CLI with `python scripts/resolve_lark_cli.py`; `scripts/resolve-lark-cli.ps1` is the Windows compatibility entry.
   - Read the version-matched CLI instructions listed under Feishu Execution in the current turn. Do not rely on remembered flags from an earlier turn or another CLI version.
   - Confirm that user-identity reads work. Do not use bot identity as an automatic fallback.
   - Resolve wiki links to their current document target before reading or writing.

2. **Read the complete source**
   - OCR every image-based page, then review the OCR output as one corpus.
   - Inspect original images whenever text, tables, formulas, or diagrams are unclear.
   - Complete the source coverage record.
   - For long sources, process ordered batches and pass the strict batch-manifest audit before synthesis.

3. **Build the framework**
   - Identify the core theme, chapter hierarchy, and knowledge spine.
   - Merge repeated points and place scattered content under the correct topic.
   - Keep source-specific chapter names when they are clearer than generic labels.
   - Record any meaningful reordering and its reason.

4. **Create a diagram opportunity inventory**
   - For each candidate, record the related section, comprehension question, diagram type, layout variant, and why text or a table is insufficient.
   - Use a flowchart for sequence, iteration, stages, or a closed loop.
   - Use a knowledge map for hierarchy, classification, or a course spine.
   - Use a matrix for meaningful comparison across multiple dimensions.
   - Use a decision chart for conditional selection.
   - Use a timeline for lifecycle or timing relationships.
   - Use a swimlane for responsibilities and cross-role handoffs.
   - Use a funnel for filtering, conversion, or progressive narrowing.
   - Use a quadrant for classification by two independent dimensions.
   - Use a cause-effect diagram for structured root-cause analysis.
   - Reject candidates that merely repeat a simple list or already-clear table.
   - Determine diagram count from accepted opportunities. Never target a fixed number.
   - Read `references/diagram-spec.md` when at least one candidate is accepted.
   - Read `references/workflow-spec.md`, record explicit relationship signals, and run `scripts/score_diagram_candidates.py` whenever two or more visual forms are plausible.
   - Reject the diagram when `prose` or `table` receives the highest score unless the source contains additional visual structure not captured by the signals.
   - Use `variant: auto` unless the relationship clearly requires a particular layout. Review the selected variant before insertion.

5. **Write the notes**
   - Use the user's requested structure; otherwise use the default framework below.
   - Keep the document understandable without diagrams.
   - Place each diagram directly beside the section it clarifies.
   - Distinguish the content layers defined below.
   - Select complete semantic highlights according to the key-point highlight standard below.
   - Build a highlight inventory using the schema in `references/workflow-spec.md`; every required item must name the exact phrase highlighted in the XML.

6. **Audit before writing**
   - Confirm every major source section maps to the draft or is intentionally omitted with a reason.
   - Confirm no extension is attributed to the source.
   - Confirm all requested sections and minimum item counts are present.
   - Review the highlight inventory and remove decorative, repeated, or low-value highlights.
   - Run `scripts/audit_highlight_coverage.py --strict` and stop if any required key point is missing, repeated, or absent from the inventory.
   - Render supported diagrams with `scripts/build_feishu_diagram.py` and validate each one with `scripts/validate_svg_layout.py --strict`.
   - Run `python scripts/validate_visual_source.py --input <file>` on Feishu XML/SVG source before any write. The Create and Update wrappers must repeat these checks automatically.

7. **Write to Feishu**
   - Follow the mode-specific Feishu procedure below.
   - Use user identity for reads and writes.
   - Keep the same output format throughout the operation.

8. **Validate after writing**
   - Re-fetch the document outline and inspect the resulting structure.
   - Re-fetch enough content to verify headings, important facts, required sections, and item counts.
   - Fetch XML and confirm all meaningful key points are highlighted while headings, repeated occurrences, and whole passages remain unhighlighted.
   - Export and visually inspect every whiteboard preview.
   - Confirm the chosen diagram type and variant still match the relationship after seeing the rendered preview; replace the SVG with a better supported variant when they do not.
   - Query at least one representative whiteboard as raw SVG/data and confirm Chinese labels are editable text nodes rather than an image-only block.
   - In Update mode, confirm the target token is unchanged and unrelated content remains intact.

## Content Boundaries

Use three explicit content layers:

1. **Source notes**
   - Preserve facts, definitions, cases, formulas, terminology, and conclusions from the source.
   - Add only headings, transitions, concise explanations, and ordering needed for coherence.

2. **Course-grounded extensions**
   - Label the section `拓展内容`.
   - Connect every extension to a topic present in the source.
   - Add practical implications, checklists, risks, scenarios, or implementation considerations without claiming they appeared in the source.
   - Avoid unstable facts, unrelated theory, and fabricated examples.

3. **Interview questions and answers**
   - Derive questions from the source topics and realistic role scenarios.
   - Provide answer logic, key points, and relevant source examples; do not invent personal experience for the user.
   - Flag missing personal evidence as a point the user must customize.

## Key-Point Highlight Standard

Use highlighting as a retrieval aid, not as decoration. Semantic coverage takes priority over a fixed highlight count.

- Highlight every distinct definition, decisive conclusion, important threshold, non-obvious constraint, critical risk, method choice, and first occurrence of essential terminology.
- Use `<span background-color="light-yellow">...</span>` as the default highlight.
- Use `light-red` only for errors, prohibitions, or material risks. Do not create a multicolor highlighter system unless the user asks for one.
- Use `<b><span background-color="light-yellow">...</span></b>` only when a highlighted term also needs strong emphasis. Follow the required XML nesting order.
- Prefer a keyword or phrase of roughly 3-12 Chinese characters. Highlight a complete sentence only when it is a standalone conclusion and keep it concise, usually no more than 40 Chinese characters.
- Do not impose a fixed number of highlights per paragraph or section. If several independent key points appear together, mark each one separately.
- Keep highlighted text at or below 30% of body text as a document-level guardrail. This is a maximum, not a target; do not force highlights where no distinct retrieval anchor exists.
- If highlighting would cover most of a paragraph, rewrite or split the paragraph so the key points can be marked precisely instead of coloring the passage as a whole.
- Highlight the first meaningful occurrence of a repeated term, not every occurrence.
- Do not highlight headings, entire paragraphs, every list item, whole table rows, code, citations, or diagram labels.
- Reserve `<callout>` for a rare critical warning that would cause an error if missed; do not use callouts as ordinary highlighting.
- In Update mode, preserve the document's existing emphasis style unless the user explicitly asks to restyle it. Add highlights only within requested sections.

## Default Note Framework

Use this structure unless the user requests another structure. Rename generic headings to match the actual topic or source type.

1. **一、整体框架**
   - State the core theme and logical relationships.
   - Add an editable knowledge-map whiteboard only when it improves understanding.
   - Include a compact outline or table of modules.

2. **二、课程主体**
   - Rename this heading to the real main topic, such as `二、评测方法` or `二、模拟面试复盘`.
   - Preserve the source-derived chapter hierarchy.
   - Insert accepted editable whiteboards beside the relevant sections.

3. **三、核心知识点整理**
   - Summarize concepts, definitions, workflows, comparisons, and easy-to-confuse points as a table or structured list.

4. **四、拓展内容**
   - Include at least 5 source-grounded items unless the user explicitly asks to omit this section.
   - Prefer practical supplements such as acceptance criteria, metric design, dataset construction, evidence management, output quality, risk control, or scenario judgment.

5. **五、面试问题**
   - Include at least 5 questions unless the user explicitly asks to omit this section.
   - Use headings such as `题目 1：...` and provide complete, concise answer points below each question.
   - Keep questions tightly connected to the source and likely role scenarios.

Do not add `PPT内容识别与归纳`, `重点与难点`, or `复习建议` by default. Add them only when the user explicitly requests OCR traceability, difficulty analysis, or review planning.

## Feishu Execution

### Prerequisites

- Require a working Lark/Feishu CLI and authenticated user identity. The skill does not bundle credentials or the CLI binary.
- Locate and smoke-test the executable with `python scripts/resolve_lark_cli.py`; do not hardcode one machine's npm, npx, Homebrew, or user path.
- Always read `lark-cli skills read lark-shared SKILL.md` and `lark-cli skills read lark-doc references/lark-doc-fetch.md` before Feishu access in the current turn.
- For Create mode, also read `lark-doc-create.md`, `lark-doc-xml.md`, `style/lark-doc-style.md`, and `style/lark-doc-create-workflow.md` through `lark-cli skills read`.
- For Update mode, also read `lark-doc-update.md`, `lark-doc-xml.md`, `style/lark-doc-style.md`, and `style/lark-doc-update-workflow.md` through `lark-cli skills read`.
- When diagrams are involved, also read `lark-doc-whiteboard.md` through `lark-cli skills read`.
- Inspect command `--help` after reading the matching embedded instructions so flags remain version-matched.
- Stop if the user identity cannot read the source or edit the requested target. Do not change identity or format.

### Create mode

- Build the complete document as UTF-8 XML when it contains whiteboards.
- Run `python scripts/invoke_feishu_create.py` from the directory containing the XML and pass relative `--content-file` and `--highlight-inventory-file` paths whenever the XML contains highlights. Windows may use `scripts/invoke-feishu-create.ps1` with equivalent parameters.
- Run without `--commit` first, inspect the dry-run, then run the same arguments with `--commit`.
- Require the wrapper to validate user identity, XML, highlight density, highlight-inventory coverage, all inline or referenced SVG files, and the created document outline.
- Use `<whiteboard type="svg">...</whiteboard>` for every diagram.
- Generate supported SVG diagrams from JSON specifications with the bundled builder instead of hand-writing each layout from scratch.

### Update mode

- Fetch the latest target section with `--detail full`, and record the target document token, block IDs, and revision immediately before modification.
- Update only the requested blocks with `docs +update`; use `block_replace` for diagram placeholders or requested section replacements.
- Pass the fetched revision through `--revision-id`; never use the default latest revision for an in-place edit.
- Use `python scripts/invoke_feishu_update.py` for supported update commands. Windows may use `scripts/invoke-feishu-update.ps1`. Pass the highlight inventory whenever the patch contains highlights. Run without `--commit` first, inspect the dry-run, then run the same arguments with `--commit`.
- Require the wrapper to validate XML/SVG/highlight content and confirm every target or source block ID exists at the expected revision before dry-run.
- The wrapper must re-fetch and compare the revision after dry-run. On a mismatch, stop, fetch again, and recompute block IDs and the patch.
- Immediately before a committed update, the wrapper must save the complete expected revision through `snapshot_feishu_document.py`. Report the backup path with the update result.
- Treat snapshots as recovery inputs, not permission to restore automatically. Re-check the current revision and ask before overwriting content from a snapshot.
- Do not rebuild the whole document when a block-level update is possible.
- If the document changes between read and write, fetch it again and recompute the patch.
- Do not create a new document as a workaround.

### UTF-8 and SVG safety

- Put long XML in a local UTF-8 file; do not place it directly on the command line.
- Do not pass Chinese XML/SVG through fragile shell stdin pipelines.
- Run `python scripts/validate_visual_source.py --input <file>` before writing.
- Run `scripts/validate_svg_layout.py --strict` on every standalone SVG before inserting it.
- Use native inline `<span background-color="light-yellow">...</span>` for text highlights; do not simulate highlights with images, emoji, or repeated callout blocks.
- Keep SVG self-contained: no external images, scripts, filters, masks, clip paths, patterns, or gradients.
- Use explicit text, rectangles, circles, simple paths, and arrows.

## Diagram Visual Standard

Use the bundled diagram system for repeatable structure without reducing every diagram to the same look.

- Supported semantic types are flow, knowledge map, timeline, matrix, decision chart, swimlane, funnel, quadrant, and cause-effect diagram.
- Supported layout variants include horizontal flow, vertical flow, closed loop, radial map, layered map, linear timeline, alternating timeline, comparison matrix, branching decision chart, role lanes, descending funnel, 2x2 quadrant, and fishbone analysis.
- Select the semantic type first, then the visual variant. Use `auto` for the common case and override only when the source relationship justifies it.
- Use semantic signal scoring from `references/workflow-spec.md` when the best type is ambiguous; do not select from a single keyword.
- For a supported type, build from a JSON specification using `scripts/build_feishu_diagram.py`; see `references/diagram-spec.md`.
- For a genuinely custom relationship that the bundled types cannot express accurately, follow the version-matched whiteboard workflow instead of distorting the content to fit a template.

- Use `canvas: auto` by default. It centers content on a `1600 x 1600` working area to match Feishu's square whiteboard preview. Use `canvas: wide` only when the user explicitly prefers a 16:9 diagram.
- Reject off-center diagrams or diagrams that use less than 45% of both canvas dimensions unless the sparse composition is intentional and manually approved.
- Use at least `64 px` outer margins, `24 px` node gaps, and `20-28 px` internal node padding.
- Use approximately `34-40 px` for the diagram title, `22-26 px` for node text, and no text smaller than `20 px`.
- Limit one diagram to one core relationship and usually no more than 7 primary nodes.
- Limit node copy to a short title plus no more than 3 concise lines. Split dense content into multiple diagrams.
- Use a light neutral canvas, dark text, and no more than 3 semantic accent colors. Avoid dark header bands and gradients.
- Draw connectors before nodes so lines sit behind shapes. Avoid crossings and route arrows consistently.
- Keep repeated nodes equal in size and align them to a visible grid.
- Leave generous width for CJK text and use separate text lines instead of overflowing text.
- Do not nest decorative cards or add icons that do not encode meaning.

## Validation Checklist

- Source coverage is complete or missing content is explicitly reported.
- The selected operating mode matches the user's request.
- Create mode leaves the source unchanged.
- Update mode keeps the original document token and preserves unrelated user edits.
- Required framework sections and minimum counts are present.
- No source statement has been materially changed without disclosure.
- Extensions and interview content are clearly separated from source notes.
- Highlights cover every distinct retrieval-critical point, remain at or below the configured 30% density limit, and do not cover entire paragraphs or headings.
- The strict highlight inventory audit passes with no missing, duplicate, or unexplained highlighted phrases.
- Long-source batch manifests pass with complete, non-overlapping page coverage and all required original-resolution checks.
- Every diagram answers a documented comprehension question.
- Ambiguous diagram opportunities have a recorded semantic score and rationale.
- Diagram types and variants are selected from source semantics rather than visual repetition.
- Every generated SVG passes `scripts/validate_svg_layout.py --strict` before insertion.
- Canvas occupancy and centering pass the static validator before insertion.
- Every whiteboard is editable SVG, nonblank, legible, and free of overlap.
- No Chinese text appears as `????` or replacement characters.
- Every whiteboard preview has been exported and visually inspected.
- The final response includes the Feishu URL and any unresolved limitation.

## Failure Policy

If editable SVG whiteboards, user-identity access, or the requested in-place update fails:

1. Stop before substituting another identity, format, or document.
2. Record the exact command/path attempted and the relevant error or validation evidence.
3. Try only the same approved method when correcting implementation mistakes such as encoding, block IDs, or SVG layout.
4. Ask the user before switching to a bot, image, new document, or other fallback.

## Skill Self-Test

- Run `python scripts/self_test.py` after modifying or installing this skill and before packaging it for another user.
- The self-test must cover all bundled diagram types, automatic layout selections, highlight coverage, diagram scoring, and long-source manifest rejection paths without writing to Feishu.
- Test Feishu Update mode only with the update wrapper's default dry-run. Never use `-Commit` for a self-test.

## Installation and Portability

- Require Python 3.10+, Node.js 18+, Lark/Feishu CLI 1.0.67+, and Whiteboard CLI 0.2.12 for the tested CLI backend.
- Support Windows 10/11 through Python and PowerShell entry points.
- Support macOS Intel and Apple Silicon through Python and Bash entry points. Public CI covers both architectures, pinned CLI smoke tests, Unicode-path installation, and archive permissions; keep real-machine Feishu authentication and document writes marked as unverified until tested on physical Macs.
- When platform behavior fails, classify the failure before changing anything. On Windows check PowerShell parsing, `.cmd` wrappers, `LOCALAPPDATA`, path quoting, execution policy, UTF-8, CLI compatibility, authentication, and document permission. On macOS check CPU architecture, PATH or Homebrew location, executable mode, UTF-8, CLI compatibility, authentication, and document permission.
- Correct Skill-owned code and temporary outputs iteratively, then rerun the failing command, preflight, installed-Skill self-test, the relevant platform smoke test, and the full public CI matrix. Preserve the failure evidence and the result of each retry.
- Do not hide a platform failure by switching identity, replacing editable whiteboards with images, using an operating-system-specific workaround on another platform, relaxing a required validation, or silently editing the user's shell profile, PowerShell policy, Homebrew setup, credentials, or authorization.
- If the cause is an external dependency or user permission, stop at the capability boundary, provide the exact detected state and repair command, and continue only after the dependency or permission is available.
- Install with `python scripts/install.py`; Windows may use `scripts/install.ps1`, and macOS may use `scripts/install.sh`.
- Keep credentials, authentication state, document snapshots, temporary OCR batches, generated previews, and `.feishu-backups` outside the installed Skill.

## Invocation Examples

- "Use feishu-visual-notes to scan this PPT and show me the framework first."
- "Use feishu-visual-notes to create a new Feishu study note from this courseware."
- "Use feishu-visual-notes to update this source document in place."
- "Use feishu-visual-notes to organize this mock-interview transcript with editable whiteboards."
