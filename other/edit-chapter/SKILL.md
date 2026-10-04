---
name: edit-chapter
description: Invoke this skill before making substantive edits to any file in guide/ — changing content, titles, template references, or canonical terms. Follow this workflow proactively when editing chapters, not only when the user explicitly requests it. Ensures structural changes propagate to all dependent files.
---

# Edit Chapter

Guided workflow for safely editing a guide chapter. Ensures structural changes propagate to all dependent files.

## Before Editing

1. Read the entire chapter file
2. Note the current H1 title (line 1)
3. Note any template paths referenced (lines mentioning `templates/`)
4. Note any canonical terms used ("five-tier context hierarchy", "document cascade")

## During Editing

- Maintain prescriptive voice — no hedging phrases (see `.claude/rules/guide-chapter.md`)
- Preserve required sections: Principles, What the Human Should Do, What the Agent Should Do
- Use **RecipeVault** for examples (not "Beacon")
- Keep heading hierarchy: `##` for major sections, `###` for subsections
- Use fenced code blocks with language identifiers

## After Editing

Check each condition and take action if true:

**If the H1 title changed:**

1. Update `README.md` chapter listing (lines 45-93)
2. Update `CLAUDE.md` if the chapter is referenced there
3. Update the "Next:" link in the prior chapter's footer

**If template references changed:**

1. Verify each referenced template path exists in `templates/`
2. If a path was removed or renamed, grep for the old path across the repo

**If a canonical term changed:**

1. Search all `.md` files for the old term
2. Update every occurrence to match the new term

**Always (every edit):**

1. Verify the chapter ends with a `Next:` footer linking to the correct successor chapter, unless the file is
   `11-failure-modes.md`
2. The footer must follow this format:
   ```markdown
   ---

   Next: [Chapter NN -- Title](NN-slug.md)
   ```

**If any structural change was made** (title, file references, canonical terms):

1. Run the `cross-reference-check` skill to verify consistency
