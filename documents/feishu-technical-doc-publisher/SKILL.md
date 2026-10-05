---
name: feishu-technical-doc-publisher
description: Turn a local authoritative Markdown design or conclusion into a reader-ready Feishu technical document using the authenticated browser, including editorial restructuring, native blocks, diagrams, table layout, safe cloud editing, and publish verification. Use when the user asks to write, publish, or synchronize a local Markdown technical document to Feishu; do not use for ordinary Markdown editing without Feishu delivery.
---

# Feishu Technical Doc Publisher

Publish a self-contained Feishu technical document for readers who do not share the author's prior conversation context. Preserve a local authoritative source and treat the Feishu page as a reviewed publication surface, not the only copy of the design.

## Purpose

Turn a local engineering conclusion into a durable publication package and a visually verified Feishu document without losing the source of truth, leaking private context, inventing undecided contracts, or damaging existing cloud content.

## When To Use

- The user asks to write, publish, republish, or synchronize a local Markdown technical design to Feishu.
- A discussion-derived engineering document needs reader-first restructuring and native Feishu layout.
- An existing Feishu technical document needs to be reconciled with a maintainable local source and revalidated after edits.

## When Not To Use

- Ordinary Markdown editing, proofreading, or architecture review with no Feishu deliverable.
- Reading a Feishu page without publishing or synchronizing local content.
- Publishing to another document platform whose block model and recovery path differ materially.
- Clearing or replacing a populated target when the user has not authorized that scope.

## Inputs To Infer Or Request

- **Authoritative local source:** infer from the named file or repository convention; stop if multiple conflicting candidates remain.
- **Target Feishu page:** must be explicit before cloud mutation.
- **Publication mode:** when the user supplies an initially blank target page for publication, treat that assignment as standing authority to edit and replace content on that page throughout the publication task. Require explicit replacement authority only when the target was already populated with content that may matter.
- **Reader and purpose:** infer from the document and user request, then choose a primary emphasis: general reader narrative, architecture review, implementation contract, or a mixed publication. State material assumptions in the local draft.
- **Reference documents and style constraints:** inspect when the user supplies them; do not copy their business content.
- **Deferred content:** preserve the user's latest instruction exactly, commonly as `待定`.

## Execution Model Gate

Full cloud publication is a high-interaction browser task when it includes UML Board insertion, content-aware table sizing, or recovery from partial edits. Prefer `gpt-5.6-sol` with `high` or `xhigh` reasoning for that mutation phase. An equivalent current frontier model is acceptable only when it can reliably inspect screenshots, reacquire changing UI state, and complete the validation gates below.

Do not use `gpt-5.6-terra` at `medium` reasoning, or a weaker execution profile, for the final Feishu mutation phase. Such a profile may prepare the local package or perform read-only inspection, but it must stop before cloud edits and ask the user to continue with the recommended model/effort. A skill cannot silently change its own model, so state this requirement before beginning the publication mutation.

## Evidence Hierarchy

1. The user's latest explicit instruction, including target and mutation scope.
2. The authoritative local design, current code/schema/specification evidence, and settled local decision records.
3. The current Feishu page after reload and visible browser verification.
4. Repository documentation, publishing records, and prior reader reviews.
5. Reference documents used only for narrative and layout patterns.
6. Inference, clearly labeled and never used to fill an intentionally undecided contract.

## Reference Navigation

Read only the reference needed for the current stage:

| Need | Read |
| --- | --- |
| Turn engineering conclusions into a public-facing narrative, choose sections, remove discussion artifacts, or conduct a no-context reader review | [Editorial workflow](references/editorial-workflow.md) |
| Prepare a publish package, edit Feishu native blocks, size tables, insert PlantUML, recover from unsafe edits, or run cloud verification | [Feishu publishing playbook](references/feishu-publishing-playbook.md) |
| Choose advanced Feishu components, inspect nested menus, or decide whether a synced, interactive, data, project, or embed block belongs in a technical document | [Component selection and nesting](references/component-selection-and-nesting.md) |

For a full local-Markdown-to-Feishu task, read both references before mutating the target page.

## Authority And Source Of Truth

1. Confirm the authoritative local Markdown, target Feishu URL, and whether the user authorized replacing existing cloud content or only editing selected sections.
2. Read repository instructions and relevant local design sources before writing. Distinguish settled decisions, evidence, unresolved items, rejected alternatives, and implementation guesses.
3. Keep a maintainable local publication source. By default, place derived publication artifacts under the repository's existing ignored agent/document area, commonly `.manifest/feishu/<document-slug>/`; follow an existing convention when present.
4. Never make the Feishu page the only source of a diagram DSL, schema, payload, or settled decision.
5. Do not expose local paths, private evidence, secrets, authenticated commands, cookies, tokens, or browser storage in the public document.

### Blank target standing authority

If the user initially gives a blank Feishu page as the publication destination, the original request authorizes all ordinary edits needed to complete that document: full-body paste or replacement, heading conversion, block insertion, UML creation, table resizing, placeholder deletion, corrections, retries, removal of broken blocks, and restoration through Edit History. Do not repeatedly ask “是否确认写入” or “是否现在执行” between those steps.

This standing authority remains limited to the named page and the requested publication. It does not authorize editing other pages, changing sharing or permissions, deleting the page itself, or publishing unrelated material. Ask again only if the page was not actually blank, unrelated content appears, the requested scope materially changes, Edit History is unavailable for a risky recovery, or another authority boundary is reached.

## Browser Boundary

Prefer the Codex in-app browser for all Feishu UI work. Load and follow the `browser:control-in-app-browser` skill before browser actions, and reuse an authenticated in-app session when one is available. If the user explicitly requests the in-app browser, that choice is binding.

Fall back to another browser surface only when the in-app browser is unavailable, lacks the required authenticated session, or cannot complete the required Feishu operation after a bounded attempt. Before falling back, tell the user the concrete limitation; do not silently switch browser surfaces. If the user required the in-app browser, stop and request direction instead of falling back.

Reuse an already authenticated browser session when available, but never inspect or persist cookies, tokens, passwords, local storage, or profile data. Authentication permits the requested document operation only; it does not authorize editing other pages, changing sharing, deleting unrelated content, or creating extra documents unless the user asked for it.

When several agents are authorized to publish experiments or independent variants, parallelize local preparation and read-only review, but treat Codex in-app-browser mutation as a single-writer resource. Serialize page creation and all cloud-editing workers, and assign each worker an exact target URL before its first write. Each worker must re-read the assigned URL, title, and initial body state and must stop if they do not match the assignment. Never infer page ownership from the newest `Untitled document`, a shared browser's selected tab, or a title prefix.

## Side-Effect Policy

- **Default level:** `local-files` for publication drafts, generated packages, extracted DSL, and publish records.
- **Maximum normal level:** `publish` when the user explicitly asks to write to a named Feishu destination.
- Treat target-page inspection as read-only until the user has requested the cloud edit.
- Preview the local reader-facing draft and generated package before publication. Existing generated files require an explicit `--force`; an existing populated Feishu page requires explicit replacement authority.
- An initially blank target with Edit History enabled does not require separate confirmations for successive publication actions or bounded recovery attempts. Continue until the document passes its gates or encounters a genuine blocker.
- Use only the intended authenticated account and page. Do not expose credentials or private source material.
- Establish Edit History as the cloud recovery path before broad replacement. Do not perform unrelated deletion as cleanup.

## Core Workflow

### Recommended Default Order

Prefer phase batching for a complete local-Markdown-to-Feishu publication:

1. Finish and freeze the exact reader-facing artifact that will be published, including generated appendices and schemas, then derive or reconcile the manifest, table inventory, code-block inventory, and diagram DSL from that exact artifact. If publication uses several paste fragments, create one composite ledger covering all fragments.
2. When the target is blank, prove that focus belongs to the intended main-document root block, then insert the complete ordinary body in one rich-text paste: headings, prose, lists, tables, code, and diagram slots.
3. Validate the complete outline and heading levels. Apply native Feishu numbering only when the current editor exposes a reliable control; never add manual numeric prefixes or experiment with list shortcuts section by section.
4. Process all diagrams in one diagram pass, while keeping every diagram atomic: insert, preview, confirm, remove its slot, and mark the ledger before moving to the next diagram.
5. Apply deliberate Callout, Timeline, column, or other presentation refinements after the main structure is stable.
6. Process all inventoried tables in one table pass, establishing a common outer boundary and then setting content-aware internal widths.
7. Run cleanup, save checks, reload, and complete diagram/table reconciliation.

This is a recommended execution shape, not a rigid requirement. A small scoped patch can operate on one section. A headings-only skeleton can help when cloud-authored content cannot be assembled locally, but keep prose and component slots as ordinary sibling blocks and defer numbering until the structure is complete. Do not use strict section-at-a-time publication or a numbered skeleton by default: both increase editor-context switching, focus risk, and cleanup work. One complete-body paste is the default; split a main body and appendix only for a demonstrated size, generation, or editor limitation, and include every fragment in the composite ledger.

### 1. Build The Publication Package

- Preserve the authoritative source unchanged unless the user also requested a source edit.
- Create or update a reader-facing draft, publishable Markdown/HTML, extracted diagram DSL, and a short publish result record.
- When useful, run:

```powershell
python scripts/prepare_feishu_publish.py <source.md> --output-dir <publish-dir> --dry-run
python scripts/prepare_feishu_publish.py <source.md> --output-dir <publish-dir>
```

The script extracts PlantUML fences, generates rich-text-ready Markdown/HTML, records a source hash, and reports editorial warnings. It does not edit Feishu. Diagram slots are local publication markers linked to manifest entries by ordinal/slot ID; their visible wording is not an API and must not be treated as a fixed string.

The manifest must describe the exact final publish artifact, not an earlier editorial draft. If a project-specific generator appends schemas, payloads, directories, or another fragment after the helper runs, regenerate the package from the assembled publication source or independently reconcile the final fragment set before cloud mutation. Never accept an intermediate manifest whose heading, table, diagram, placeholder, or code-block counts differ from the payload that will actually be pasted.

Use the generated table inventory as a completion checklist. Its width percentages are starting suggestions, not proof of cloud layout. Resolve PlantUML compatibility warnings before insertion, and still require a successful Feishu preview because static checks cannot prove renderer compatibility.

Before cloud mutation, create a publication ledger from the exact final artifact. Record expected heading counts by level; one pending row per table and diagram; identifying table headers; the diagram placeholder/DSL mapping; code-block count; a source-derived tail marker for every long code block; temporary-placeholder count; and intentionally deferred markers. Counts inferred from the visible first screen are not sufficient.

### 2. Rewrite For A No-Context Reader

- Start with background, purpose, scope, and an overview before detailed fields or APIs.
- Choose the reading emphasis before choosing blocks. For a mixed audience, keep a reader-first main path, use only the core diagrams needed to establish flow, and place contract detail after the reader understands ownership and behavior.
- Explain ownership and end-to-end flow before schema and implementation structure.
- Convert conversation-dependent reasoning into stable conclusions. Remove oral estimates, rejected names, superseded options, and phrases meaningful only to prior participants.
- If a section is intentionally undecided, write `待定` rather than inventing a contract from discussion fragments.
- Keep the main path concise. Move large schemas, payloads, and implementation directories to an appendix or sub-document.

Use [Editorial workflow](references/editorial-workflow.md) for the detailed narrative and cleanup gates.

### 3. Choose Native Feishu Blocks Deliberately

- Use native H1/H2/H3. Validate all headings through the complete outline before applying numbering. Prefer Feishu-native numbering when a reliable control is visible; if it is not, keep semantic headings unnumbered instead of adding hand-maintained prefixes or trying list shortcuts against an uncertain cursor focus.
- Use Callout or quote blocks only for short positioning statements, hard constraints, or risks. Give a rule one primary expression; do not repeat the same sentence in an opening paragraph, Callout, quote, and table.
- Use native tables for repeated mappings and comparisons; use code blocks for compact payloads and configuration.
- Use a native Table of Contents for long pages only when it improves in-page onboarding; the native outline may already be sufficient. Use Equation for genuine mathematical notation; keep both full-width.
- Keep diagrams, wide tables, Timeline, and long code full-width. Use at most two columns, only for short paired summaries.
- Prefer one visual per relationship: PlantUML for architecture/flow/ER, Timeline for a small phase sequence whose chronology matters, and tables for exact mappings. Start with the smallest set of diagrams that explains the system; add another only when it represents a distinct relationship rather than repeating a table.
- Choose UML rendering style by complexity. Board Style suits simple diagrams with short labels and limited branching; use Classic Style directly for dense branching, high-degree center nodes, or long edge labels.
- Treat Synced Block, Poll, Button, Templates, Sheets/Base views, sub-documents, project cards, and external embeds as conditional capabilities. Read [Component selection and nesting](references/component-selection-and-nesting.md) before using them. Menu visibility alone does not prove stable behavior or authorize creation of persistent cloud objects.
- Expect `Insert Below` to change by container. If a block type disappears inside a column, Callout, or Synced Block, insert it as a sibling rather than forcing unsupported nesting.

### 4. Publish Safely

- Inspect the target page and its current structure before changing it. When existing content matters, note the page title and last-modified state and know how to reach Edit History.
- Prefer block-level operations and `Insert Below`. Use rich-text paste for ordinary headings, lists, tables, and code; insert extracted PlantUML diagrams separately through UML Board.
- Before any broad rich-text paste, click the visible empty-body prompt or an explicitly created root-level sibling, type and undo a harmless focus probe, and verify that editing focus belongs to the main document rather than a comment composer, list, table, code block, or embedded component. Never select a generic or last `contenteditable` as the paste target.
- Process every diagram as an atomic transaction: locate its manifest slot, insert and validate the diagram, return to the document, confirm the rendered block is in the intended position, compare the adjacent heading and outline text with the final artifact, then delete that entire slot block. Never leave a local insertion instruction or filename in the public page.
- Complete an individual outer-width and content-aware column-width pass for every table in the generated inventory. Sampling representative tables is insufficient for publication completion. Clicking an autofit/distribute command is not completion until the resulting widths are visually checked in document view.
- In the PlantUML modal, do not click `Insert` unless the preview shows the intended diagram with no syntax-error panel. A Board block existing in the document is not evidence that its diagram rendered.
- Never use global `Ctrl+A` in the Feishu document, code block, or table editor. It can select and overwrite the entire document.
- Use native Find/Replace only for narrowly scoped, exact replacements. After removing text, delete empty headings, numbered items, and table formatting left behind.
- Do not change sharing, permissions, comments, or unrelated pages unless explicitly requested.

Use [Feishu publishing playbook](references/feishu-publishing-playbook.md) for the stable insertion, table, diagram, and recovery procedures.

### 5. Validation Requirements

Verify the published page as a reader, not merely as an editor:

- the first screen explains why the document exists and what it proposes;
- the outline is coherent, and Feishu-native numbering is continuous when numbering is enabled;
- every inventoried table retains its headers and representative cell content, was individually adjusted, shares the document's chosen outer boundary, and allocates internal columns by content; an empty-looking or default equal-width import is incomplete unless the content and uniform sizing are both intentionally correct;
- every diagram rendered successfully in the Feishu preview and remains a real diagram after insertion and reload, with no syntax-error image, overlapping labels, or duplicate board objects;
- every diagram's adjacent heading and outline text still match the final artifact, with no Board chrome or editor text mixed into public content;
- the actual heading counts by level and code-block count match the final-artifact ledger; long independently scrollable code blocks reach a source-derived tail marker and valid closing structure after reload;
- unresolved sections say `待定` and no invented detail appears;
- process-only phrases, local paths, diagram placeholders, and removed field names do not remain;
- the page reports `Saved to cloud`.

Reload the page and repeat targeted checks. A successful paste or visible save indicator before reload is not sufficient proof.

Reconcile the exact-final-artifact ledger transactionally: heading counts by level match; `content-verified and adjusted tables == ledger tables`; `rendered diagrams == ledger diagrams`; code-block count and long-block tail checks pass; and `remaining temporary placeholders == 0`. If any equality fails, publication is incomplete regardless of how much prose was successfully pasted.

Feishu may virtualize off-screen blocks after reload. Verify the outline, then use native Find plus targeted anchor navigation or scrolling to inspect representative early, middle, and tail sections; a first-screen snapshot does not prove that the full document survived.

### 6. Synchronize And Record

After cloud refinements, update the maintainable local publication source so a later republish does not restore stale wording. Record:

- target URL and publication time;
- local source and generated artifact paths;
- diagrams inserted and the retained DSL paths;
- table layout completion as `adjusted/total`, including any explicit exceptions;
- diagram render completion as `rendered/total`, including the Feishu preview and reload check;
- representative sections visually checked;
- heading/code-block reconciliation and long-block tail checks performed;
- exact cloud-save/reload verification performed;
- any intentionally deferred content.

Report only validation actually performed.

## Output Contract

Return or link:

- the Feishu page, when publication was authorized and completed;
- the maintainable local reader-facing source;
- the generated publish package and retained diagram DSL;
- the publish result record;
- executed validation, skipped checks, deferred sections, and any recovery action.

Do not claim cloud completion when only local artifacts were prepared.

## Failure And Recovery Rules

- If content on an initially blank publication target becomes missing, duplicated, or broadly replaced during the task, use Edit History to restore the nearest known-good revision, reload, verify the outline, and continue without requesting another confirmation. Stop for user direction only when the history does not contain a safe recovery point or unrelated pre-existing content is at risk.
- Use Board Style for simple editable diagrams. For dense branching, high-degree center nodes, or long edge labels, choose Classic Style up front. If a Board attempt remains unreadable after one bounded simplification pass, switch to Classic rather than repeatedly rewriting a sound diagram to fit the Board layout engine. If Board first reports a syntax or converter-compatibility failure for otherwise sound PlantUML, prefer Classic after one bounded attempt instead of repeatedly deleting valid DSL merely to satisfy Board Style.
- Feishu's embedded PlantUML may lag the current release. Prefer established syntax and treat the modal's displayed renderer as authoritative. Do not use standalone `diamond` declarations for decisions; use activity-diagram `if / then / else / endif` or supported structural nodes. If preview fails, fix or replace the DSL before insertion.
- Do not infer that Feishu lacks PlantUML because it is absent from the initial UML template panel or a top-right overflow menu. In the opened Board, use the left floating toolbar's nine-dot/More menu, then choose `PlantUML Diagram`. Reacquire the current screenshot and semantic labels at each menu boundary; do not replay stale coordinates through several changing menus.
- Do not silently substitute draw.io, Graphviz, or static images for requested native UML. If the documented PlantUML entry still cannot be reached after one fresh-state retry, leave the local slot intact, make no substitute cloud insertion, and report that diagram publication is incomplete.
- If a table cannot show all used columns after width adjustment, reduce the table zoom or reopen full-screen editing; do not mistake the viewport edge for the table boundary.
- If the user has not authorized overwriting a populated target, do not clear it. Prepare local artifacts and request that authority.
- If authentication is missing in the selected browser, stop and ask the user to sign in there; do not bypass it through another account or browser.

## Before Finishing

Confirm that the local source and publication artifacts exist, the target URL is correct, the document survives reload, every table and diagram passed its explicit layout/render gate, the outline and representative prose were inspected, no sensitive data was published, deferred content is explicit, and the final response links both the Feishu page and the maintainable local source. If any table or diagram remains unchecked or broken, report publication as incomplete rather than downgrading it to a skipped representative check.
