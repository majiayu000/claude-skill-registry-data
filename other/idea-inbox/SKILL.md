---
name: idea-inbox
description: Capture a raw idea as a dated, tagged markdown file in an ideas folder and keep an index up to date. Cleans filler words from the dump while preserving the substance, so capture stays fast and retrieval stays possible. Use when the user says "idea:", "capture this idea", "save this idea", or "add to my ideas".
---

# Idea Inbox

Capture ideas at the speed they arrive and still find them later. One idea per file, dated and tagged, in a dedicated folder with an index. Dump fast, refine later.

## Step 0: Locate the ideas folder (once)

1. Look for an `IDEAS_INDEX.md` anywhere in the project; its folder is the ideas folder.
2. Otherwise look for a folder named `ideas/`, `Ideas/`, or similar.
3. Otherwise ask the user where ideas should live, create the folder, and create an `IDEAS_INDEX.md` in it.

Never save idea files to the project root. A pile of loose dated files in the root is how ideas get deleted in the next cleanup.

## Step 1: Capture

1. Get today's date from the current-date context (format `YYYY-MM-DD`).
2. Distill a 3 to 5 word kebab-case slug from the idea, e.g. `etsy-pinterest-autonomous-pins`.
3. Clean up the raw input: remove filler words and false starts, keep every substantive detail. Tighten, do not summarise. If the user wrote three rough sentences, the file should contain three clean sentences, not one.
4. Pick 1 to 3 tags from the index categories (see Step 2), plus `idea`.

Create `<ideas-folder>/<date>-<slug>.md`:

```markdown
---
tags: [idea, <category-tag>]
date: <date>
---

# <Idea title in plain words>

<cleaned idea text>
```

## Step 2: Update the index

`IDEAS_INDEX.md` keeps one line per idea under a category heading. Default categories (create on first use, let the user rename them):

```markdown
# Ideas Index

## Business
## Automation & Tools
## Design & Creative
## Client Work
## Misc
```

Add the new idea under the best-fitting category:

```markdown
- [<Idea title>](<date>-<slug>.md) <date>: one-line hook
```

If an idea clearly fits a category that does not exist yet, add the category rather than forcing it into Misc.

## Step 3: Confirm

Report the file path, the category it was filed under, and the one-line hook used in the index.

## Rules

- One idea per file. If the user dumps three ideas in one message, create three files and say so.
- Never edit or delete existing idea files. The inbox only grows; pruning is the user's call.
- Preserve the user's meaning exactly. Cleaning filler is fine, replacing their thinking is not.
- Keep the index sorted newest first within each category.
