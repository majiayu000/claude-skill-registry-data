---
name: analiz-html-report
category: architecture
description: Use when you write or revise the analiz deliverable - the ONE self-contained HTML report (spec and plan as sections) a human reviews passage by passage
---
# Analiz HTML Report

## Overview

An analiz task produces exactly ONE document: an analysis report written as a self-contained HTML page, attached with `add_task_document` and `format: "html"`, titled `analiz: <YYYY-MM-DD> <topic>`. The design (what spec-authoring describes) and the implementation plan (what implementation-plan-authoring describes) are SECTIONS of this report — never separate `spec: …` / `plan: …` documents.

The human reads the report in the task drawer, selects passages and comments on them, then sends every comment back at once. That shapes how you write it:

- **Every claim a reviewer might question is plain text** — a paragraph, a table cell, a list item. Text inside an SVG or an image cannot be selected and commented on, so a diagram illustrates a point the prose already makes; it never carries a decision alone.
- **Every section and every plan step has a stable `id`** (`summary`, `context`, `design`, `plan`, `step-3`, …). A revision keeps them; the implementation tasks you create later can cite `#step-3`, and a reviewer's comments stay findable.
- **Developers read it as text.** Implementation tasks derived from this analysis get the report's text rendition in their run context (headings, paragraphs, lists, table rows, code blocks — markup dropped). Structure it so that rendition reads well: real headings, real lists, real tables.
- **Open questions are not part of this document.** A genuine product decision the code can't settle is recorded with `record_open_questions` (open-questions-protocol), never written here and never asked with `ask_user`. The system renders every open question as an answer box above this report automatically — the `risks` section below is risks only.

## Required sections (in this order, with these ids)

1. **`summary` — Summary.** What is being built and why, in 3–6 sentences, then one `callout decision` stating the chosen approach. A reviewer who reads only this knows what they are approving.
2. **`context` — Context & current state.** What exists today, grounded in code you read: a table of real file paths and symbols (`internal/application/task/service.go` — `TaskService.ListByProject`) with what each does now. No path or symbol you did not see in this run.
3. **`design` — Proposed design.** Components with exact interfaces (names, parameter and return types), data flow, error handling, what the user sees, and the 2–3 approaches you weighed with the one-line reason the chosen one won. A decision worth remembering (new dependency, datastore/schema shape, API/contract pattern, auth/security architecture, cross-repo integration) gets a `<h3 id="design-decision">` decision record (spec-authoring); skip it for a bug fix or config change. A **Security & data** subsection names who may call each new interface, which inputs are attacker-controlled, and what data leaves the system. Out-of-scope items are listed explicitly.
4. **`diagrams` — Diagrams** (only where they help: a request flow, a state machine, a component boundary). Inline `<svg>` with a `<title>` — its title is what the text rendition shows. Omit the section rather than draw a box that restates a sentence.
5. **`plan` — Implementation plan.** Numbered steps (`<ol class="steps">`, each `<li id="step-N">`): files to create/modify/test with exact paths, the interfaces each step consumes and produces, and the TDD cycle with the actual test code and the command to run. No placeholders — "add error handling", "similar to step 2" and "TBD" are plan failures (implementation-plan-authoring).
6. **`split` — Task split.** One row per project/repository: the repository, the layer, the one-line scope of its implementation task, the plan steps it owns, and its order (`blocked_by` / `deploy_depends_on`). This is what the human is approving you to create.
7. **`risks` — Risks.** Each risk with its mitigation. Open questions do not go here (or anywhere in the HTML) — record them with `record_open_questions` instead (open-questions-protocol); the system renders them above the report as answer boxes.

## HTML rules

- One complete document: `<!DOCTYPE html>`, `<html>`, `<head>` with `<meta charset="utf-8">` and an inline `<style>`, `<body>`.
- **No `<script>`, no external fonts, stylesheets, scripts or images.** Everything the page needs is inline. The server sanitizes on save and removes scripts, iframes, objects/embeds, `<link>`, `<base>`, forms and form controls, every `on*` attribute and `javascript:` URLs — anything that depends on them silently disappears.
- Images only as `data:image/…` URIs, and only when a screenshot is the evidence; prefer inline SVG.
- Light and dark: colours are CSS variables with a `prefers-color-scheme: dark` override, as in the template. Never hard-code a text colour on a background you did not also set.
- Size: derived tasks and the reviewer get the report's TEXT rendition cut at 24,000 bytes from the end — `plan` and `split` are the first to go. After attaching, call `list_task_documents` with this task, the `document_id` and `limit: 22000` (text, not raw): if the result carries `next_offset`, the report is too long — cut code bodies to signatures and test assertions (implementation-plan-authoring) and shorten `context`, then check again. HTML itself stays under ~150 KB (hard limit 1 MB) — summarize, cite files and symbols instead of pasting them, keep code blocks to the lines that matter.

## Template

Start from this and fill it in. Keep the class names — the styles already cover callouts, tables, code and step lists.

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>analiz: 2026-09-26 CSV export</title>
<style>
:root{--bg:#fff;--fg:#1f2328;--muted:#59636e;--line:#d1d9e0;--panel:#f6f8fa;--accent:#0969da;--ok:#1a7f37;--warn:#9a6700;--risk:#cf222e;
--sans:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;--mono:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace}
@media (prefers-color-scheme:dark){:root{--bg:#0d1117;--fg:#e6edf3;--muted:#9198a1;--line:#3d444d;--panel:#151b23;--accent:#4493f8;--ok:#3fb950;--warn:#d29922;--risk:#f85149}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);font:15px/1.6 var(--sans)}
main{max-width:920px;margin:0 auto;padding:32px 24px 64px}
h1{font-size:26px;line-height:1.25;margin:0 0 4px}
h2{font-size:20px;margin:40px 0 12px;padding-bottom:6px;border-bottom:1px solid var(--line)}
h3{font-size:16px;margin:24px 0 8px}
a{color:var(--accent)}
.meta{color:var(--muted);font-size:13px;margin-bottom:20px}
nav.toc{background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:10px 16px;font-size:14px}
nav.toc ol{margin:0;padding-left:20px}
code{font:13px/1.5 var(--mono);background:var(--panel);border:1px solid var(--line);border-radius:4px;padding:0 4px}
pre{background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:12px 14px;overflow:auto}
pre code{border:0;padding:0;background:none}
table{width:100%;border-collapse:collapse;font-size:14px;margin:12px 0}
th,td{text-align:left;vertical-align:top;border-bottom:1px solid var(--line);padding:6px 8px}
th{color:var(--muted);font-weight:600}
.callout{border-left:4px solid var(--accent);background:var(--panel);border-radius:6px;padding:10px 14px;margin:14px 0}
.callout.decision{border-left-color:var(--ok)}.callout.warn{border-left-color:var(--warn)}.callout.risk{border-left-color:var(--risk)}
ol.steps{list-style:none;padding:0;counter-reset:step}
ol.steps>li{counter-increment:step;position:relative;border:1px solid var(--line);border-radius:8px;padding:12px 14px 12px 50px;margin:12px 0}
ol.steps>li::before{content:counter(step);position:absolute;left:14px;top:12px;width:24px;height:24px;border-radius:50%;background:var(--accent);color:var(--bg);font:600 13px/24px var(--sans);text-align:center}
ol.steps h3{margin-top:0}
.tag{display:inline-block;border:1px solid var(--line);border-radius:999px;padding:0 8px;font-size:12px;color:var(--muted)}
figure{margin:16px 0}figcaption{color:var(--muted);font-size:13px}
svg{max-width:100%;height:auto}
svg text{fill:var(--fg);font:12px var(--sans)}
svg .node{fill:var(--panel);stroke:var(--line)}
svg .edge{stroke:var(--muted);stroke-width:1.5;fill:none}
</style>
</head>
<body><main>
<header id="top">
  <h1>CSV export of a project's tasks</h1>
  <div class="meta">analiz · A-12 · 2026-09-26 · repositories: backend-api, web</div>
</header>
<nav class="toc"><ol>
  <li><a href="#summary">Summary</a></li><li><a href="#context">Context &amp; current state</a></li>
  <li><a href="#design">Proposed design</a></li><li><a href="#diagrams">Diagrams</a></li>
  <li><a href="#plan">Implementation plan</a></li><li><a href="#split">Task split</a></li>
  <li><a href="#risks">Risks</a></li>
</ol></nav>

<section id="summary">
  <h2>Summary</h2>
  <p>Project owners need their tasks in a spreadsheet. …</p>
  <div class="callout decision"><strong>Decision:</strong> build the CSV in an application service and stream it from a new endpoint; the web board gets a download button.</div>
</section>

<section id="context">
  <h2>Context &amp; current state</h2>
  <table>
    <thead><tr><th>Where</th><th>What it does today</th></tr></thead>
    <tbody><tr><td><code>internal/application/task/service.go</code> — <code>TaskService.ListByProject</code></td><td>Returns a project's tasks, newest first; used by the board page.</td></tr></tbody>
  </table>
</section>

<section id="design">
  <h2>Proposed design</h2>
  <h3 id="design-components">Components</h3>
  <p><code>TaskExporter.Export(ctx, projectID uuid.UUID) ([]byte, error)</code> — …</p>
  <h3 id="design-alternatives">Alternatives considered</h3>
  <table><thead><tr><th>Approach</th><th>Why not</th></tr></thead><tbody><tr><td>Stream from the handler</td><td>Untestable without HTTP.</td></tr></tbody></table>
  <h3 id="design-decision">Decision record</h3>
  <p><strong>Problem:</strong> need a reusable, testable export path. <strong>Drivers:</strong> testability without HTTP, reuse by a future scheduled export. <strong>Chosen:</strong> an application service returning bytes, because it is unit-testable and the handler stays thin. <strong>Consequences:</strong> Good, because tests don't need an HTTP harness. Bad, because large exports hold the full CSV in memory (mitigated in risks).</p>
  <h3 id="design-security">Security &amp; data</h3>
  <p>Only the project's owner may call the export endpoint (reuses the existing project-scoped auth middleware); no new data leaves the system beyond what the user already sees in the board.</p>
  <p><strong>Out of scope:</strong> PDF, scheduled export, column selection.</p>
</section>

<section id="diagrams">
  <h2>Diagrams</h2>
  <figure id="fig-flow">
    <svg viewBox="0 0 560 90" role="img" aria-label="Export request flow">
      <title>Export request flow</title>
      <rect class="node" x="10" y="25" width="140" height="40" rx="6"/><text x="80" y="50" text-anchor="middle">GET /export</text>
      <path class="edge" d="M150 45H210"/>
      <rect class="node" x="210" y="25" width="140" height="40" rx="6"/><text x="280" y="50" text-anchor="middle">TaskExporter</text>
      <path class="edge" d="M350 45H410"/>
      <rect class="node" x="410" y="25" width="140" height="40" rx="6"/><text x="480" y="50" text-anchor="middle">TaskRepository</text>
    </svg>
    <figcaption>The handler validates the id; the exporter owns the CSV shape.</figcaption>
  </figure>
</section>

<section id="plan">
  <h2>Implementation plan</h2>
  <ol class="steps">
    <li id="step-1">
      <h3>TaskExporter service <span class="tag">backend-api</span></h3>
      <p><strong>Files:</strong> create <code>internal/application/export/service.go</code>; test <code>internal/application/export/service_test.go</code></p>
      <p><strong>Consumes:</strong> <code>TaskRepository.ListByProject(ctx, id) ([]Task, error)</code> · <strong>Produces:</strong> <code>Export(ctx, projectID uuid.UUID) ([]byte, error)</code></p>
      <p><strong>Failing test first:</strong></p>
      <pre><code>func (s *ExportSuite) TestExport_encodesHeaderAndRows() { … }</code></pre>
      <p><strong>Run:</strong> <code>go test ./internal/application/export/... -run TestExport</code> → FAIL, implement, → PASS.</p>
    </li>
  </ol>
</section>

<section id="split">
  <h2>Task split</h2>
  <table>
    <thead><tr><th>Repository</th><th>Layer</th><th>Task</th><th>Steps</th><th>Order</th></tr></thead>
    <tbody><tr><td>backend-api</td><td>backend</td><td>Export endpoint and service</td><td>1–2</td><td>first</td></tr></tbody>
  </table>
</section>

<section id="risks">
  <h2>Risks</h2>
  <div class="callout risk"><strong>Risk:</strong> large projects — mitigation: stream rows, cap at 50k.</div>
</section>
</main></body></html>
```

## Revising the report

The report is revised in place, never replaced. After a review (the task comes back from `need_revision`):

1. Read the comments — they are in your run context under "Review comments on your analysis document", and `list_document_annotations` (status `submitted`) returns them all with the quoted passage.
2. Read the report's source: `list_task_documents` with the analiz task, its `document_id` and `raw: true`; follow `next_offset` until you have all of it.
3. Fix every comment at its root — re-read the code where a comment questions a fact — with `update_task_document` on the same `document_id`: `edits` (each `old_text` copied exactly from the source, occurring once) for targeted changes, `content` for a rewrite. Keep the section and step ids, and keep the document's TITLE unchanged — a new date in the title creates a second document instead of revising this one, since `add_task_document`/`update_task_document` match by exact title. Do not touch `split` unless a comment or a code re-read gives you a reason to — the human already approved its shape once.
4. Answer every comment with `resolve_document_annotations`: one line per comment saying what changed and where (`"Switched to a cron job — see #design and #step-2"`), or why you deliberately kept it.

## Self-review (before the run ends)

- All seven sections present with their ids; the `plan` steps are `step-1…step-N`.
- **Grounding pass** — before attaching, re-verify every claim, not just that you made some exploration call earlier: every path in `context` and `plan` exists (`get_repo_tree`/`grep_code`) or the step says *create*; every consumed symbol's signature matches what `get_symbol_skeleton` shows now; every third-party call matches the version locked in the lockfile; every verify command appears in `list_component_checks` or `get_project_brief`. Anything you cannot verify this way is removed from the plan; if it's a risk worth flagging, note it in `risks`; if only the human can decide it, record it with `record_open_questions` (open-questions-protocol) — never left in as an assumption.
- No `<script>`, no external URL in `<link>`/`<img>`/`@import`/fonts.
- Every decision and requirement is readable as text, not only inside a diagram.
- Nothing is readable two ways; no TBD/TODO; the `split` table matches the plan's steps.
