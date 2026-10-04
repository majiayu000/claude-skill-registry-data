---
name: cross-reference-check
description: Invoke this skill after any structural change to the repository — renaming files, changing chapter H1 titles, adding or removing chapters or templates, updating canonical terms, or modifying template paths. Also invoke when the user asks to "check cross-references", "validate links", or "verify chapter titles match README". The guide-chapter rule directs you to run this after structural edits.
---

# Cross-Reference Check

Validate all cross-references across the repository.

## Step 1: Run the Automated Checks

Execute the validation script:

```bash
python3 .claude/skills/cross-reference-check/scripts/validate.py
```

The script checks:

- Internal `.md` link resolution (do all `[text](path.md)` links point to existing files?)
- Chapter H1 title format (does every chapter start with `# Chapter`?)
- Chapter listing in README.md (is every chapter file referenced?)
- Template path consistency (do paths referenced in guide chapters exist?)
- Checklist file references (is every `checklists/*.md` file referenced somewhere?)
- Canonical term presence (do `CLAUDE.md` and `README.md` contain required terms?)
- Chapter title wording (do README.md and CHEATSHEET.md entries match each chapter's H1?)
- Next: footer title match (does each Next: link's text match the target chapter's H1?)
- Canonical terms registry drift (does the script's dict match `references/canonical-terms.md`?)

Output is pipe-delimited: `TYPE|FILE|LINE|ISSUE|FIX`. If all checks pass, the script exits 0.

**False positives are expected.** The script cannot distinguish real links from illustrative examples (e.g.,
`` `[Chapter 02](02-project-bootstrap.md)` `` shown as a formatting convention, or `[text](path.md)` used as a
pattern example). Review each finding before reporting it — read the surrounding context to determine whether the
flagged link is an actual reference or example text.

## Step 2: Report

Present all findings (automated + manual) as a table:

| File | Line | Issue | Fix |
|------|------|-------|-----|
| ...  | ...  | ...   | ... |

If everything passes, output: **All cross-references valid.**
