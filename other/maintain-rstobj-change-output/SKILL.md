---
name: maintain-rstobj-change-output
description: "Change what an existing rstobj class renders (fix a bug in its output, add or rename an option, change indentation or whitespace), update the snapshots, and decide from the snapshot diff whether the change fits a patch, minor, or major release. Use when the user reports wrong or invalid rstobj output, or asks to change how an existing class renders."
---

Change one class's output on purpose, and prove exactly what users will see change.

Read ../maintain-rstobj-base/SKILL.md, then:
- ../maintain-rstobj-base/references/02-rendering-and-indentation.md
- ../maintain-rstobj-base/references/03-templates.md
- ../maintain-rstobj-base/references/04-cases-snapshots-gallery.md
- ../maintain-rstobj-base/references/05-compatibility-and-traps.md

## Step 1: Reproduce with a case

Write the failing input as a case in `rstobj/tests/cases.py` first (`gallery=False` for an edge case). Run its module's test file: a bug in validity fails `assert_valid_rst`; a wrong but valid output needs its snapshot, so state the expected output to the user before changing code.

## Step 2: Change the template or the code

- Template changes follow `03-templates.md`.
- Indentation and nesting changes go through `_indent_line`, `_indent_continuation`, and `_render_nested` in `rstobj/base.py` (`02-rendering-and-indentation.md`); never re-implement indenting in a template.

## Step 3: Update and read the snapshot diff

```bash
RSTOBJ_UPDATE_SNAPSHOTS=1 .venv/bin/pytest tests -q
git diff --stat rstobj/tests/snapshots
git diff rstobj/tests/snapshots
```

Sort every changed snapshot into one of three groups:

1. was invalid reStructuredText, now valid;
2. was valid but wrong (a dropped field, a repr), now right;
3. was valid and right, now different (anything beyond whitespace).

## Step 4: Decide the release

Apply `05-compatibility-and-traps.md` section 1: only groups 1, 2, and whitespace-only changes fit a patch. If anything lands in group 3, stop and show the user those diffs and the release type they need; continue only after the user's yes, or narrow the change (such as an opt-in field) so the old output stays.

## Step 5: Verify

`mise run cov` (100%, no warnings), `mise run lint`, and `mise run build-doc` all pass. If the class is live in the gallery, look at its entry in the built docs.

## Report

The snapshot diff grouped as in Step 3, the release type, and a one-line user-facing changelog entry for `pywf-oss-changelog`. If the change removes a limitation listed in `05-compatibility-and-traps.md` section 2, update that table in the same change.
