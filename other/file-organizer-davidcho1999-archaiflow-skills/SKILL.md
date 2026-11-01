---
name: file-organizer
description: "Sorts a disorganized folder into a target tree, by writing a move plan you read and approve before any file is touched. Trigger on \"organize this folder\", \"sort these files\", \"clean up this directory\", \"tidy this handoff folder\", \"file organizer\", or a pasted path plus an organizing verb. Matches on filename, extension, size, and modified date, never on file contents. Finds duplicates by hash and routes them for review rather than deleting anything. Every run writes a plan first, executes only against the approved plan, and appends an audit log that a rollback can read backwards. The taxonomy is yours: the skill will draft one from what it finds, but it does not invent target folders you did not agree to."
license: MIT
metadata:
  title: "File Organizer"
  summary: "Sort a messy folder into a taxonomy you approve first"
  discipline: "practice-contracts"
  tags: "Project Management, Catalog Tooling"
---

# File Organizer

Nothing moves until you have read the plan. The plan is a CSV, one row per file,
and the run executes that file and nothing else.

## Scope and limits — read first

**What this does.**

- Moves or copies files from a source folder into a target tree you define.
- Matches on filename glob, filename regex, extension, size threshold, and
  modified-date range, combined with and/or inside a slot.
- Optional rename per slot, from a regex capture into a format string.
- Finds duplicates by SHA-256 across the source set and routes them to a review
  folder, keeping one copy in the slot.
- Writes `move-plan.csv` before touching anything, and executes only that file.
- Appends `audit.log` per run: timestamp, action, source, destination, hash,
  result.

**What this does not do.**

- **It does not delete anything.** Duplicates and collisions go to review
  folders. What to discard is your call, made afterwards, by hand.
- It does not read file contents to classify. Filename, extension, size, and
  date only. For content-based sorting, extract metadata first with `doc-reader`
  or `drawing-reader` and feed the result in as rename pairs.
- It does not invent target folders. It will draft a taxonomy from what it finds
  and show you, but a slot you did not approve does not get created.
- It does not follow symlinks more than once, cross filesystem boundaries, touch
  anything outside the declared target root, or work on a network path unless
  you say so explicitly.
- It does not execute a plan you have not read.

**What you need before starting.** The source folder, where the result should
go, and either a taxonomy or ten minutes to review the one it drafts.

## Workflow

### Step 1. Set up the run folder

Every run gets its own folder so plans and audit logs never overwrite each
other:

```
docs/file-organizer/<YYYY-MM-DD>-<run-id>/
  taxonomy.yml
  move-plan.csv
  audit.log
```

Create it before anything else. If the project has no `docs/` folder, confirm
before creating one.

### Step 2. Identify source and target

Ask for the source root and the target root, as absolute paths. Confirm both
exist. Confirm they are on the same filesystem, and say so if not, because a
cross-device move is a copy followed by a delete and the rollback story changes.

List the source and report what is there: file count, total size, extensions
present, date range. Show this before proposing any structure.

### Step 3. Get the taxonomy

Three routes, in order of preference.

1. **The user has one.** Read it, and show back the slots and rules as you
   understood them.
2. **The user names an existing folder to imitate.** Read that tree and derive
   slots from it.
3. **Draft one.** Group by what is actually in the source, propose slots with
   the rule for each, and show the draft. Do not create a slot you cannot write
   a rule for, and do not create a slot for a file type the source does not
   contain.

Write the agreed taxonomy to `taxonomy.yml` in the run folder. Its shape:

```yaml
target_root: /abs/path
allow_network: false
slots:
  - path: 01-drawings/current
    match:
      any:
        - ext: [".dwg", ".pdf"]
          name_glob: "A-*"
    rename: null
  - path: 02-specs
    match:
      all:
        - ext: [".docx", ".pdf"]
          name_regex: "(?i)spec"
```

### Step 4. Build the move plan

Walk the source. For each file, find the first slot whose rule matches, and
write a row:

| source | destination | slot | action | sha256 | note |
|--------|-------------|------|--------|--------|------|

- Files matching no slot get `action: unmatched` and no destination. They stay
  where they are.
- Files whose hash already appeared get `action: duplicate` and a destination
  under `_duplicates/<slot>/`.
- Two different files landing on the same destination name get
  `action: collision` and a destination under `_collisions/<slot>/`.

Write it to `move-plan.csv`. Touch nothing.

### Step 5. Show the summary and get approval

Report, before asking:

- Rows by action: move, copy, duplicate, collision, unmatched.
- The slots that got nothing, which usually means a rule is wrong.
- The unmatched list if it is short, or its extensions and count if it is long.
- The largest ten files being moved.

Then ask plainly whether to execute, and say that nothing has been touched yet.
If the answer is anything other than yes, stop and leave the plan on disk.

### Step 6. Execute

Read `move-plan.csv` row by row. For each row with `action: move` or `copy`:

1. Create the destination parent if needed.
2. Perform the action.
3. Verify the destination exists and the hash matches.
4. Append a line to `audit.log`.

On any failure, stop. Do not continue past an error, and do not roll back
automatically. Report the row number reached; the audit log records everything
completed up to that point.

Execute only rows in the CSV. If the source changed since the plan was written,
say so and offer to rebuild the plan rather than working around it.

### Step 7. Roll back, if asked

Read `audit.log` in reverse and move each file back to its recorded source path.
Verify each hash on arrival. Append the reversal to the same log rather than
deleting lines, so the folder's history stays readable.

### Step 8. Report

Counts by action, where the plan and the audit log are, the unmatched list, and
what is sitting in `_duplicates/` and `_collisions/` waiting on a decision.

## Rules

- **Nothing moves before the plan is approved.** The plan is a file the user can
  read, not a summary in chat.
- **Execute the CSV, not the intention.** If a row looks wrong, stop and ask;
  do not correct it in flight.
- **Never delete.** Route to a review folder and let the user decide.
- **Verify by hash after every move**, and stop on the first mismatch.
- **An unmatched file stays where it is.** Never invent a slot at execution time
  to catch a straggler.
- Confirm before creating `docs/` in a project that does not have one.

## Anti-patterns

- Executing a plan the user has not seen because the summary looked clean.
- Deleting a duplicate because it is obviously a duplicate.
- Adding a catch-all slot so the unmatched count reads zero.
- Continuing past a failed move to finish the run.
- Rolling back automatically on error, which turns one problem into two.
- Classifying by opening the file. This skill matches on names and metadata; if
  that is not enough, the answer is a different tool upstream, not guessing.

## Resources

None. This skill is one file. The run folder, the taxonomy, the plan, and the
audit log are written directly at the paths above.
