---
name: wikicommit-remove
description: Mark a wiki page (and its translations) as removed and prepare a removal PR. Use this only when someone explicitly asks to remove or delete a specific wiki page. It marks the page to come off the published site once merged, so do not use it to correct a page or to find pages nothing links to — wikicommit-fix corrects a page and wikicommit-status finds orphans without writing.
disable-model-invocation: true
---

# wikicommit-remove

> **Paths in this file.** `references/…`, `scripts/…` and `../<other-skill>/…` are relative to this Skill's directory — the one holding this `SKILL.md`, which the runtime names when it loads the Skill — not to the repository root, because the Skills may be installed under `.claude/skills/` or `.agents/skills/`. Commands still run from the repository root, so spell the path out from there (`python <this Skill's directory>/scripts/…`). Paths starting with `.wikicommit/` are repository-root paths as before.

Skill for removing a wiki page. Does not physically delete the file — it only performs a soft delete by setting `status: removed` on the target page. This hides the page from the published wiki while preserving Git history and rollback capability.

## Usage

```
/wikicommit-remove <page>   # e.g. /wikicommit-remove .wikicommit/entity/ja/Person/yamada-taro.md
/wikicommit-remove <page>   # a view page too, e.g. /wikicommit-remove .wikicommit/view/ja/agent-loops.md
```

`<page>` may be an entity page (`.wikicommit/entity/<lang>/<Type>/<slug>.md`) or a view page written by `/wikicommit-synthesize` (`.wikicommit/view/<lang>/<slug>.md`). Both are removed the same way; Step 2 says where the two differ. Do not delete a view page's file directly instead: without `status: removed` the quality gate cannot block new links to it, and its line stays in the view index.

## Processing Flow

### Step 1: Confirm the Removal Reason

Confirm the removal reason with the user:

- `obsolete` (content is outdated or no longer needed)
- `merged` (merged into another page — also confirm the path of the merge target page)
- `gdpr` (personal data removal request, etc.)

If the target page doesn't exist, or already has `status: removed`, this is detected in step 2 — here, only confirm the reason.

### Step 2: Run `remove_page.py`

If `.wikicommit/scripts/remove_page.py` does not exist (`.wikicommit/scripts/` older than this Skill), stop and tell the user to run `/wikicommit-update` first.

```bash
python .wikicommit/scripts/remove_page.py <page> --reason <reason> [--merged-into <path>]
```

- When `--reason merged`, always add `--merged-into <path of the merge target page>`.
- On exit code `1` (error), present the output as-is to the user and stop. Expected errors:
  - The target page doesn't exist
  - The target page already has `status: removed`
  - `--reason merged` was given but `--merged-into` was not
  - The file pointed to by `--merged-into` doesn't exist

This script automatically does the following:

1. Sets `status: removed` / `removed_at` / `removed_reason` (and `merged_into` for `merged`) on the target page's frontmatter
2. Finds the translated pages that have the target page as their parent via `translated_from`, and applies the same `status: removed` etc. to them — for an entity page, across that Type's directory in every language; for a view page, across the view tree in every language
3. Removes the page's line from the index it is listed in — for an entity page, the `index.md` of its Type directory; for a view page, the `index.md` directly under its language directory (`.wikicommit/view/<lang>/index.md`, since the view tree has no Type directories) — and the same for each translation

`--merged-into` may name an entity page or a view page, whichever kind the page being removed is — a view page can be merged into an entity page and the other way round.

### Step 3: Report Results

Extract the `REMOVED: <path>` lines from `remove_page.py`'s stdout and report them to the user as a list, including both the original page and any translated pages.

### Step 4: Guidance on Next Steps

```
Next steps:
- Run /wikicommit-merge to perform quality checks, PR creation, and merge
  (if any broken WikiLinks are detected, they will be shown as warnings.
   They won't block the merge, but if needed, use /wikicommit-remove separately
   to remove the referencing pages too, or fix the links manually)
```

## Notes

- Do not commit or create a PR against `main` or any branch (that is `wikicommit-merge`'s responsibility)
- Do not physically delete files (only sets the `status: removed` flag)
- Do not write to `.wikicommit/schema/` (read-only)
