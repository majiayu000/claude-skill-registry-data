---
name: to-tickets
description: Break a plan, spec, or the current conversation into tracer-bullet tickets with blocking edges, filed as local markdown files on the tickets board (to do / in progress / done / blocked).
disable-model-invocation: true
---

# To Tickets

Break a plan, spec, or conversation into **tickets** — tracer-bullet vertical slices, each declaring the tickets that **block** it — and file them onto the local **tickets board**.

## The board

The board lives in `.tickets/`, relative to the repository root, with four columns: `to do`, `in progress`, `done`, `blocked`. Create any that don't already exist.

Every ticket file is named `<id>-<slug>.md`, where `<id>` is a zero-padded 3-digit number unique across all four columns, and `<slug>` is a short kebab-case version of the title.

The board is local scratch space, not committed history. Before writing any ticket file, check the repository's `.gitignore` for a `/.tickets/` entry and add one if it's missing.

## Process

### 1. Gather context

Work from whatever is already in the conversation context. If the user passes a reference (a spec path, an issue number or URL) as an argument, fetch it and read its full body and comments.

### 2. Explore the codebase (optional)

If you have not already explored the codebase, do so to understand the current state of the code. Ticket titles and descriptions should use the project's domain glossary vocabulary, and respect ADRs in the area you're touching.

Look for opportunities to prefactor the code to make the implementation easier. "Make the change easy, then make the easy change."

### 3. Draft vertical slices

Break the work into **tracer bullet** tickets.

<vertical-slice-rules>

- Each slice cuts a narrow but COMPLETE path through every layer (schema, API, UI, tests) — vertical, NOT a horizontal slice of one layer
- A completed slice is demoable or verifiable on its own
- Each slice is sized to fit in a single fresh context window
- Any prefactoring should be done first

</vertical-slice-rules>

Give each ticket its **blocking edges** — the other tickets that must complete before it can start. A ticket with no blockers can start immediately.

**Wide refactors are the exception to vertical slicing.** A **wide refactor** is one mechanical change — rename a column, retype a shared symbol — whose **blast radius** fans across the whole codebase, so a single edit breaks thousands of call sites at once and no vertical slice can land green. Don't force it into a tracer bullet; sequence it as **expand–contract**. First expand: add the new form beside the old so nothing breaks. Then migrate the call sites over in batches sized by blast radius (per package, per directory), each batch its own ticket blocked by the expand, keeping CI green batch to batch because the old form still exists. Finally contract: delete the old form once no caller remains, in a ticket blocked by every migrate batch. When even the batches can't stay green alone, keep the sequence but let them share an integration branch that all block a final integrate-and-verify ticket — green is promised only there.

### 4. Assign IDs and starting columns

Scan every column in `.tickets/` for existing ticket filenames, and take the highest 3-digit number found across all of them (start at `001` if none exist). Assign the new tickets the next consecutive numbers, in dependency order (blockers first).

A ticket starts in `to do` if it has no blockers, or all its blockers are already in `.tickets/done`. Otherwise it starts in `blocked`.

Done when: every new ticket has a unique ID and a column consistent with its blocking edges.

### 5. Quiz the user

Present the proposed breakdown as a numbered list. For each ticket, show:

- **Title**: short descriptive name
- **Blocked by**: which other tickets (if any) must complete first
- **What it delivers**: the end-to-end behaviour this ticket makes work
- **Starting column**: to do or blocked

Ask the user:

- Does the granularity feel right? (too coarse / too fine)
- Are the blocking edges correct — does each ticket only depend on tickets that genuinely gate it?
- Should any tickets be merged or split further?

Iterate until the user approves the breakdown.

### 6. Write the ticket files

Write one file per ticket to `.tickets/<column>/<id>-<slug>.md` using this template:

<local-ticket-template>

# <id> — <Ticket title>

**What to build:** the end-to-end behaviour this ticket makes work, from the user's perspective — not a layer-by-layer implementation list.

**Blocked by:** the IDs/titles of the tickets that gate this one, or "None — can start immediately".

- [ ] Acceptance criterion 1
- [ ] Acceptance criterion 2

</local-ticket-template>

Avoid specific file paths or code snippets in the template — they go stale fast. Exception: if a prototype produced a snippet that encodes a decision more precisely than prose can (state machine, reducer, schema, type shape), inline it and note briefly that it came from a prototype. Trim to the decision-rich parts — not a working demo, just the important bits.

### 7. Validate

Before finishing, verify that:

- Every ticket file's ID is unique across all four columns.
- Every ticket's "Blocked by" references another ticket actually written this run or already on the board.
- Every ticket in `blocked` has a non-empty "Blocked by".
- Every ticket in `to do` has no unmet blockers.

## Final response

Report:

- Ticket files created, with their paths and columns.
- The frontier — tickets in `to do` ready to start now.
- Any tickets filed to `blocked`, and what they're waiting on.
