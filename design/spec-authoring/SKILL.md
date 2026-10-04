---
name: spec-authoring
category: architecture
description: Use when you write the `context` and `design` sections of an analiz report - components, exact interfaces, data flow, errors, decision record, out of scope
source: obra/superpowers (MIT), adapted
---
# Spec Authoring

## Overview

The spec is not a document of its own any more: it is the `context` and `design` sections of the ONE analysis report the analiz task produces (analiz-html-report) — an HTML document attached with `add_task_document`, `format: "html"`, titled `analiz: <YYYY-MM-DD> <topic>`. Never attach a separate `spec: …` document, never write it to a file and never commit it; shelling out to `echo`/heredoc to fake a file is how a run gets killed for repeating itself. The spec is the contract the plan section and every implementation task will be checked against.

These sections must name real files, symbols, and interfaces you found with `codebase_search` / `grep_code` / `get_repo_tree` / `expand_symbol_context`. A run that attaches an analiz document without a single successful exploration call is rejected by the system, not by a reviewer.

## Structure

Where each part lives in the report: Context / Goal feeds `summary` and `context`; Architecture through Out of scope are subsections of `design` (each an `<h3>` with its own id). Scale each part to its complexity — a few sentences if straightforward, up to 200–300 words if nuanced; Decision record and Security & data are each written only when they apply (see their conditions below):

1. **Context / Goal** — the problem, who has it, what outcome closes it.
2. **Architecture** — the chosen approach, and in one line why it beat the alternatives.
3. **Components** — each unit with clear boundaries: what it does, its interface (exact names and types), what it depends on.
4. **Data flow** — how a request/value moves through the components, including where validation happens.
5. **Error handling** — what fails, how each failure surfaces, what the user sees.
6. **Testing approach** — what proves each component works: unit, integration, end-to-end.
7. **Decision record** — for a choice worth remembering (new dependency or framework, a datastore or schema shape, an API/contract pattern, auth or security architecture, a cross-repo integration — skip it for a bug fix or config change): `<h3 id="design-decision">` with Problem (1–2 sentences) · Decision drivers (bullets) · Options (table: option | fits drivers | cost/risk) · "Chosen: X, because …" · Consequences (Good, because … / Bad, because …). If the repo keeps its own ADRs (`docs/adr`, `docs/decisions`, `adr/`), add a plan step in that repository that writes `NNNN-<title>.md` in the repo's own format.
8. **Security & data** — who may call each new interface, which inputs are attacker-controlled, what data leaves the system (to a log, a third party, a client bundle), and what is logged (security-review has the full checklist for any new endpoint or data flow). Any schema or contract change also gets its expand/contract shape and consumer list here (migration-and-contract-review).
9. **Out of scope** — explicitly named items deferred or excluded.

**UI design (web UI analyses only):** when the analysis includes web UI, the design section also covers: the pages and their sections; the component inventory by atomic level (reuse existing vs. new, naming each); design tokens/brand direction (or "use the existing system"); responsive behaviour per breakpoint for anything non-trivial; and the states each view needs (loading/empty/error, form states).

## Writing Rules

- State decisions, not options: the exploration happened in technical-analysis-workflow; the spec records what WILL be built.
- Every interface names its exact functions, parameters, and return types — implementers must not have to invent names.
- Copy project-wide constraints (versions, naming/locale rules, layer boundaries) verbatim — they become the plan's Global Constraints block.

## Worked Example (a Components entry done right)

```html
<h3 id="design-task-exporter">Component: TaskExporter (application service)</h3>
<ul>
  <li><strong>Does:</strong> turns a project's tasks into CSV bytes.</li>
  <li><strong>Interface:</strong> <code>Export(ctx, projectID uuid.UUID) ([]byte, error)</code> — errors: <code>domain.ErrProjectNotFound</code>, <code>domain.ErrForbidden</code></li>
  <li><strong>Depends on:</strong> <code>TaskRepository.ListByProject(ctx, projectID) ([]Task, error)</code></li>
  <li><strong>Data flow:</strong> handler validates projectID → TaskExporter.Export → repo.ListByProject → encode CSV (header + one row per task, columns: id,title,status,created_at).</li>
  <li><strong>Out of scope:</strong> PDF, scheduled export, column selection.</li>
</ul>
```

An implementer reading only this can build it: the exact signature, the exact dependency it consumes, the column order, and the errors it raises. That is the bar for every Components entry.

## Self-Review (mandatory, before handoff)

Look at the finished design sections with fresh eyes and fix issues inline:

1. **Placeholder scan** — no "TBD", "TODO", incomplete sections, or vague requirements.
2. **Internal consistency** — no section contradicts another; the architecture matches the component descriptions.
3. **Scope check** — focused enough for ONE implementation plan? If not, decompose into sub-specs.
4. **Ambiguity check** — could any requirement be read two different ways? When the code or the brief settles it, pick one reading and state it explicitly. When only the human can settle it — a genuine product choice, not a detail you can infer — record it with `record_open_questions` instead of guessing: non-blocking with your recommended reading when a default is defensible (the usual case), blocking only when proceeding on either reading would waste the implementation (open-questions-protocol).

A design that fails any check is not ready — fix it before writing the plan section (implementation-plan-authoring).
