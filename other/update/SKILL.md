---
name: update
description: Integrate external info (research, status changes, reference material, deliverables) into the ops repo's knowledge base. Drop files in .update/ or pass content inline.
argument-hint: <content to integrate, or empty to process .update/ folder>
---

# Update

Ingest external information into this ops repo's knowledge base. Two modes depending on whether arguments are provided.

## Detect Mode

- **If `$ARGUMENTS` is non-empty** → **Inline mode**: the arguments contain the information to integrate.
- **If `$ARGUMENTS` is empty or blank** → **Inbox mode**: process files from `.update/`.

---

## Inline Mode

The user provided content directly: $ARGUMENTS

1. **Load context.** Read `CLAUDE.md` and `MEMORY.md` to understand the repo structure, goals, and current state.

2. **Classify the information.** Apply the whole-file test from CLAUDE.md — *fact about the world, or decision/framework?*
   - **Fact about the world** (status, metric, inventory) → `state/`
   - **Decision / strategy / framework / guardrails / research** → `references/`
   - **Specific actions to do next** → `backlog/`
   - **Delivered output** → `artifacts/`
   - **Strategic insight** → may also warrant a MEMORY.md Key Learnings update
   - **Mixed** → split

   Trap: "current strategic posture" content feels state-shaped but is forward-looking strategy → `references/`.

3. **Integrate.** For each piece of information:
   - Read the target file first — never overwrite blindly. Merge or append.
   - When updating state files, update the `_Last updated: YYYY-MM-DD_` line.
   - When adding backlog items, insert in priority order (highest first), not at the end.
   - If placement is ambiguous, apply the Whole-File Test and place it anyway — then note the call in a clause when you report. Ask the user only when the ambiguity is about what the information *means* for the project: a fact you can't reconcile with existing state, or a claim that changes a stated goal. Never ask which folder something belongs in.

4. **INDEX.md cascade.** For every file created or significantly changed, update that folder's `INDEX.md`. If the folder's overall summary changed, cascade to the parent `INDEX.md`.

5. **MEMORY.md check.** If the information shifts the project's strategic understanding — a new constraint, a key learning, a changed goal — add or update an entry under Key Learnings. Don't add specific data points (those belong in state/references); only add general insights.

6. **Summarize.** Lead with one sentence on what the project now knows that it didn't, or what changed in its picture of reality. Then tell the user what was placed where.

---

## Inbox Mode

Process all files in the `.update/` directory.

1. **Load context.** Read `CLAUDE.md` and `MEMORY.md`.

2. **List files.** Check `.update/` for files (skip `.gitkeep`). If empty, tell the user "No files in `.update/` to process" and stop.

3. **Process each file.** For each file in `.update/`:

   a. **Read and understand** the file's contents. Consider the filename, format, and content to determine what it is.

   b. **Classify** — same categories as inline mode (status update, research, task, deliverable, mixed).

   c. **Extract and integrate** relevant information into the knowledge base:
      - Create or update files in `state/`, `references/`, `backlog/`, or `artifacts/` as appropriate.
      - Read target files before writing — merge, don't overwrite.
      - Update `_Last updated:_` dates on state files.
      - Insert backlog items in priority order.

   d. **INDEX.md cascade** — update every affected INDEX.md.

   e. **Dispose of the source file:**
      - **Delete** if all useful information has been extracted into structured knowledge (the common case — raw notes, status emails, data dumps).
      - **Move to `references/`** if the file itself is a useful reference to keep (e.g., a PDF report, a detailed analysis document).
      - **Move to `artifacts/`** if the file is a deliverable or work product (e.g., a submitted application, a finalized spec). Date-prefix it if it's been delivered.
      - If unsure whether to keep or delete, keep it — move it to `references/` and note the call in a clause when you report. Deleting is irreversible; keeping costs a file. Ask only when what's at stake is a judgement the user owns: the file contradicts something the project treats as settled, or it looks like a deliverable that may already have gone out.

4. **MEMORY.md check** — same as inline mode. Update Key Learnings if warranted.

5. **Summarize.** Lead with one sentence on what the project now knows that it didn't, or what changed in its picture of reality. Then list each file processed, where its information was placed, and whether the file was deleted or moved. (A sub-agent running this skill returns whatever format its caller asked for instead.)

---

## Rules

- **State vs. backlog separation** — facts about current reality go in `state/`. Actions and opportunities go in `backlog/`. Don't mix them.
- **Don't duplicate** — before creating a new file, check if an existing file already covers that topic. Extend the existing file rather than creating a parallel one.
- **Preserve structure** — follow the repo's existing organizational patterns. If grants info lives in `references/grants/`, new grant research goes there too.
- **Cite sources** — if the incoming information references external sources (URLs, documents, people), preserve those citations in the integrated output.
- **Be conservative with MEMORY.md** — most updates don't warrant a Key Learnings entry. Only add entries that change the project's strategic understanding.
