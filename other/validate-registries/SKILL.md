---
name: validate-registries
description: "Scan the registries (.claude/registries/MECHANISMS.md with MECHANISMS/*.md, and VOCABULARY.md with VOCABULARY/*.md) for dead file references, and with --check-structure lint their layout (bodiless entries, duplicate titles, project content in the Universal root, digest freshness). Reports any backticked path entries whose files no longer exist. Use to prevent the reusable mechanism registry from rotting when files are renamed or deleted. Use when: user says /validate-registries, 'check the registry', 'find dead links in MECHANISMS', or as a weekly sanity check."
user_invocable: true
---

# /validate-registries -- Registry Dead-Link Check

When invoked, run the `validate_registries.py` script and present its output to the user.

## Step 1: Run the validator script

```bash
py -3 ".claude/scripts/validate_registries.py"
```

Optional flags the user may pass:
- `--root <path>` — an extra repo root to resolve paths against (can be repeated)
- `--json` — structured JSON output instead of the human report

Example with an explicit repo root:
```bash
py -3 ".claude/scripts/validate_registries.py" --root "<absolute path to the repository root>"
```

## Step 1b: Structure lint (`--check-structure`)

The same script lints the registries' layout. It reads the three root files and their domain files (`MECHANISMS/*.md`, `VOCABULARY/*.md`, `JOURNAL/*.md`) through the shared reader:

```bash
py -3 ".claude/scripts/validate_registries.py" --check-structure --project "$CLAUDE_PROJECT_DIR"
```

- `--strict` makes the R4 advisory fail the run as well (exit 1). Without it R4 never changes the exit code.
- The findings: R1 bodiless entry, R2 duplicate title (every location is listed), R3 project content in the Universal root, R5 invalid domain file, R6 stale digest, A1 malformed entry. **R4 is an advisory:** a backticked path in a registry file that resolves under neither the project root nor the installed plugin root prints `advisory: R4 <file>:<line> <path>`. Paths under the consumer-only or generated prefixes are skipped: `.claude/settings.json`, `.claude/settings.local.json`, `.claude/.sync-config.json`, `.claude/.sync-state/`, `.claude/hook-registration-profile.json`, `.claude/.scout-cache/`, `.claude/cache/`, `.claude/logs/` and `.codegraph/`.
- A project not yet on registry layout 2 (the registry layout state is `pending`, `stale-sync` or `unknown`) gets every finding as an advisory plus one `advisory: registry layout <state>` line, and exit 0. On a `current` project the exit is 1 on any R1, R2, R3, R5, R6 or A1 finding, else 0. Exit 2 means the check could not run; show the message.
- The registries are append-only: the lint reports, it never rewrites. A bodiless entry is not fixed by this skill; its remedy line names the `registry_append.py` command (`--archive-title-only`) the operator runs.

## Step 2: Present the report

The script's output already has the shape you want — pass it through verbatim. It lists:

- Candidate repo roots it checked
- For each registry file: total references / alive / dead
- For each dead reference: line number, path, surrounding context

The script exits with code `1` if any dead references were found, `0` otherwise.

## Step 3: If dead references exist, propose fixes

For each dead entry, ask the user:

- Was this file **renamed**? If yes, record the new path as a correction to the registry entry.
- Was this file **deleted** because the mechanism was removed? If yes, record that as a correction to the registry entry.
- Was this file **moved to another project** or is it in a location the script's root hints don't cover? If yes, re-run the skill with `--root` pointing at the correct repo.

Use `AskUserQuestion` with the dead-link list pre-filled as options. Do NOT blindly update the registry without the user confirming the intent.

## Step 4: Apply the fixes

After the user confirms:

Registry entries are append-only: an entry is never rewritten or removed, so a fix is a correction line added by `registry_append.py`. Find the script with the standard lookup block that `/journal-add` Step 3 carries (the same text, only `--registry` differs), then for each confirmed fix write the correction text to `.claude/cache/registry-appends/<slug>.md` and run:

```
py -3 "$RAP" --project "$CLAUDE_PROJECT_DIR" --registry mechanisms --correction-of "<entry title>" --from-file .claude/cache/registry-appends/<slug>.md
```

(`--registry vocabulary` for a vocabulary entry; `--date` and `--source` set the correction's date and source.) The correction text states the old path, the new path (or that the file was removed) and why. Show the printed `file:line`. On a project not yet on registry layout 2 it appends to a domain file and prints an advisory line; that is success. Exit 2: fix the entry file and re-run. Exit 3: stop and show the message to the user. The original dead reference stays in the entry, so the validator keeps listing it; the user decides whether a given dead path is worth a correction.

## Step 5: Archive stale follow-up stubs

After the registry pass, run the stub archiver as a dry-run first to show the user what would be archived:

```bash
py -3 ".claude/scripts/archive_stale_stubs.py"
```

Stubs older than 30 days that still have `Status: stub` are reported. If the dry-run lists any, ask the user:

> "Should I archive these stubs? They'll be renamed to `<slug>.followup.archived.md` but remain on disk for historical reference."

If the user confirms, re-run with `--apply`:

```bash
py -3 ".claude/scripts/archive_stale_stubs.py" --apply
```

## Step 6: Report done

Summarize for the user: "X dead references found, Y corrected, Z stubs archived; structure lint: <exit code and finding count>."

## Notes on the script's resolution logic

The script builds a candidate root list from:
- The current working directory
- Each folder under `.claude/concepts` with known install hints (`d:/Dev/HIPALANET/<project>`, `~/Dev/<project>`, etc.)
- Any `--root` passed on the command line

If a project lives in a non-standard location and the script can't find it, pass `--root`.
