---
name: register-context
description: >
  Use this skill to register an existing file as context in CLAUDE.md so content skills
  can discover and load it for future work.
  Invoke when the user says "register this as context", "promote to context",
  "add this to context", "add this file to the context table", "reference this in CLAUDE.md",
  or "make this a context file".
allowed-tools: Read, Write, Edit, Bash
argument-hint: "[optional: path to the file to register as context]"
---

# Promote to Context

You are registering an existing file as context in `CLAUDE.md` so content skills can
discover and load it for future work.

## Step 1: Identify the file and target

If `$ARGUMENTS` contains a file path, use it. Otherwise ask:

> "Which file would you like to register as context? (Provide the file path.)"

If `$ARGUMENTS` also names a target `CLAUDE.md` explicitly (e.g. "register x in
`myproject/press/2026/CLAUDE.md`"), record that path. An explicit target is a deliberate
choice — Step 4 uses it directly, no placement questions asked.

Read the file.

## Step 2: Suggest a label

Generate a short, descriptive label (2–5 words) based on the file content. Good labels
are specific enough to distinguish this file from similar ones in the same project:

- Too generic: "Writing style"
- Good: "Brand voice – recruiting"
- Good: "Whitepaper – AI in HR (Q3 2025)"
- Good: "Audience – enterprise buyers"

Present the suggestion and ask the owner to confirm or change it:

> "Suggested label: **[label]**
> (or enter your own — no restrictions)"

## Step 3: Generate a summary

Write a one-sentence summary (10–25 words) from the file content. The summary is the key
signal skills use to decide which file to load for a given task — be specific:

- Too vague: "Writing style guidelines"
- Good: "Formal German, em-dash preferred, no exclamation marks — all corporate copy"
- Good: "Whitepaper on AI in HR published Q3 2025 — use as reference for follow-up content"
- Good: "Three enterprise buyer personas: CHROs, IT directors, and works councils"

Present the suggestion and ask the owner to confirm or change it:

> "Suggested summary: [summary]
> (or enter your own)"

## Step 4: Determine the target CLAUDE.md

If an explicit target was named in `$ARGUMENTS` (Step 1), use it directly and skip to Step 5 —
no placement question, that's the point of naming it explicitly.

Otherwise, scan for candidates:

```bash
find . -name "CLAUDE.md" -not -path '*/.git/*' -not -path '*/node_modules/*' | sort
```

Find the nearest ancestor `CLAUDE.md` to the file (the root file counts as the outermost
ancestor).

**Use it without asking** only when there's no real choice to make: it's the only `CLAUDE.md`
found anywhere in the project, and it's in the file's own directory or one level above it.

**Otherwise ask** — either the nearest ancestor is more than one directory level above the file,
or other `CLAUDE.md` files exist at different levels, so a vague command genuinely leaves the
level open:

> "`[file]` could be registered at more than one level:
>
> - `[nearest ancestor path]` (closest existing file)
> - `[other candidate path]` (repeat for each other CLAUDE.md found)
> - or a new `[file's directory]/CLAUDE.md`, scoped just to that folder
>
> Which should I use?"

- Owner picks an existing path: use it as the target.
- Owner picks "new": treat this as "target CLAUDE.md does not exist" in Step 5.

## Step 5: Add the row

Make the `File` path relative to the target CLAUDE.md's own directory (not the project root —
see the repo's context-architecture convention).

Show the proposed row before writing:

> "I'll add this row to `[target CLAUDE.md path]`:
>
> | [label] | [file path] | [summary] |
>
> Proceed? (yes / edit / skip)"

- **Yes**, target CLAUDE.md exists: add the row to its `## Context files` table.
  If the section does not exist yet, create it first:

  ```markdown
  ## Context files

  Skills read all registered files and load what's relevant for each task.

  | Label | File | Summary |
  | ----- | ---- | ------- |
  ```

  Then append the row. Confirm: "✓ Registered `[file path]` as context in `[target CLAUDE.md path]`."

- **Yes**, target CLAUDE.md does not exist (no ancestor found, or the owner chose to create a
  new nested one in Step 4): ask "There is no CLAUDE.md at `[target folder]` yet. What should
  its heading say — a project, client, or campaign name?", then create it:

  ```markdown
  # [Name]

  ## Context files

  Skills read all registered files and load what's relevant for each task.

  | Label   | File        | Summary   |
  | ------- | ----------- | --------- |
  | [label] | [file path] | [summary] |
  ```

  Confirm: "✓ `[target CLAUDE.md path]` created and `[file path]` registered."

- **Edit**: ask what to change, update label/summary/path, show again.

- **Skip**: say "Registration cancelled — nothing was written." and exit.
