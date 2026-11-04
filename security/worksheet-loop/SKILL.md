---
name: worksheet-loop
description: |
  Shared markdown task document for human↔agent collaboration.
  The agent creates a `.worksheets/ws-<epoch>-<slug>.md`, writes progress
  into it, and re-reads it when the human edits it.  Normal chat still works.
---

# Shared worksheet (`.worksheets/`)

You share a **markdown worksheet** with the human.  It lives in `.worksheets/`
and follows the naming convention `ws-<epoch>-<slug>.md`.

## How it works — first turn

1. Each Pi session must explicitly select its worksheet. Do not assume the
   newest file is yours: parallel sessions share `.worksheets/` and implicit
   selection causes cross-session pollution. Use **`/worksheet start`**,
   **`/worksheet open <name>`**, or **`/worksheet attach <path>`**:

   - `/worksheet start fix-auth` — creates `.worksheets/ws-<epoch>-fix-auth.md`,
     selects it for this session, and opens it in a herdr split.
   - `/worksheet start` with no slug — prompts you for a kebab-case slug.
   - `/worksheet attach path/to/document.md` — selects and watches an existing
     Markdown file for this session.
   - `/worksheet list` — lists project worksheets; `/worksheet search <text>`
     searches their saved Markdown content.
   - Other subcommands: `open [name]` (select and open a named worksheet in a
     split), `path [name]` (print its path), `status`, `pause`, `resume`.

   A session with no explicit selection stays in normal chat mode and ignores
   worksheet edits. This is intentional isolation behavior.

   Or create one manually:
   - Grab the current epoch: `date +%s`
   - Pick a short kebab-case slug from the task (e.g. `fix-auth`, `refactor-middleware`)
   - Run `mkdir -p .worksheets` first
   - Create `.worksheets/ws-<epoch>-<slug>.md` structured like this:

     ```markdown
     # Fix auth module — 2026-07-15 14:30

     ## Task
     <what the human asked>

     ## Human notes
     <!-- goals, constraints, feedback, or a requested action -->

     ## Todos
     - [ ] Define the next concrete step

     ## Progress
     - Started analysis

     ## Findings
     <durable research or review results>

     ## Decisions
     <durable decisions made during the collaboration>

     ## Questions / Next steps
     <anything you want to ask or do next>
     ```

2. Work on the task.  After each significant milestone **update the selected
   file** — add completed items under `## Progress`, refine next steps, note questions.

3. When the human edits a worksheet and saves, you'll receive a
   `[Worksheet update — filename]` message containing the changed Markdown
   sections and additions/removals. Use it as steering input. Read the file
   when you need broader context or when the message looks stale; the full
   document remains the source of truth on disk.

4. Treat `## Human notes` as human-owned input. Do NOT overwrite it. Keep
   durable agent state in `## Progress` and `## Findings`, and preserve existing
   entries by appending or adding dated updates. Use `## Questions / Next steps`
   for unresolved decisions and proposed follow-up.

5. Treat a worksheet update as saved human steering input, not as a request to
   merely acknowledge the file. Decide whether it calls for review, research,
   implementation, or clarification, and act accordingly.

6. When the worksheet is the shared source of truth, record durable progress,
   findings, decisions, and next steps back into it so the human can continue
   from the document without reconstructing state from chat.

7. Treat checkbox changes as task-state changes. An unchecked todo is work to
   plan or perform; a checked todo is a completion claim to verify. Treat
   deliberate deletions or replacements as human feedback, not as missing text.

8. Stay Markdown-centric: prefer headings, paragraphs, blockquotes, and
   checkboxes over hidden HTML metadata. For auditability, record a rejected or
   superseded suggestion as a short entry under `## Decisions` or `## Progress`
   before removing it. A deletion can then mean “remove from the active plan”
   without erasing the historical reason.

## Stable semantics for comments, questions, and todos

These are the machine-meaning contracts for the shared sections. The extension
surfaces the *transitions* that matter (checkbox state changes) explicitly in
the steering message as `Semantics:`; treat that call-out as authoritative over
a raw diff.

- **Comments** — a `> ` blockquote is a direct human comment to Pi. Everything
  under `## Human notes` is human-owned and never overwritten; Pi replies go
  under `## Agent response` (append-only).

- **Questions** — line items under `## Questions / Next steps` are open steering
  asks. Tick an item (`- [ ] ...?` → `- [x] ...?`) to close/answer it. An item
  that ends with `?` and stays blank/unticked is a question still awaiting your
  answer. Deleting a question removes it from the active plan — it does not mean
  “answer and stop”; answer first if it was still open.

- **Todos** — `- [ ]` is open (work to do), `- [x]` is done (a *claim* to verify,
  not proof). A check is an assertion of completion; verify before moving on. An
  item flipped back to `- [ ]` is a reopen — treat it as in-progress again, not
  a fresh addition.

## Not your only interface

The human can still talk to you directly in chat.  The worksheet is an additional
collaboration channel for long-running, multi-turn tasks.  If the human types
something in chat, respond normally.

If you are mid-task and see a worksheet update, incorporate the changes and
continue.  If the human marks a step as done or changes direction, follow that.
