---
name: simple-restructure
description: Reorganize the repo file tree by grouping files into domain folders, without changing code behavior. Use when the user asks to restructure, reorganize, or group files and folders.
disable-model-invocation: true
metadata:
  author: denniemok
  version: "1.0.0"
license: MIT
---

# Simple Restructure

Make the repo tree organised by moving files into folders that match what they belong to. Move files and fix imports. Do not change logic. The golden rule is to move only what helps. If a folder is already clear, leave it.

## What organised means

Group by domain (the thing a file is about), inside the layers the repo already has. One domain name is reused across layers.

```
src/
├── components/
│   ├── book/
│   ├── bookshelf/
│   └── ui/          # generic, no domain
├── hooks/
│   ├── book/
│   └── bookshelf/
└── utils/
    ├── book/
    └── text/
```

## Workflow

1. Read the current tree and detect the existing conventions (layers, naming, aliases).
2. Find domains. Look for files sharing a name prefix, a feature, or an entity.
3. Propose the move plan as an old path to new path list. Wait for approval before moving.
4. Move files with `git mv` when in a git repo, so history is kept.
5. Update every import, alias, config path, and test path that points to a moved file.
6. Run the build, type check, or tests. If you cannot, say what should be run.

## Rules

- Follow the repo's current layout and naming. Only add structure where it is missing.
- Create a domain folder only when it has 3 or more files. Fewer stay flat.
- Generic or shared code goes in a shared folder like `ui` or `common`, not in a domain.
- Keep folders shallow, about 2 levels below a layer.
- Move only. Do not rename exports, split or merge files, or edit logic. Suggest those as follow-ups.
- Never move entry points, config files, or files the tooling expects at a fixed path.
- Folders that define routes (Next.js `app/` and `pages/`, Astro `src/pages/`) also define URLs, so do not move or rename them. Group the code they import instead, such as `components/`, `lib/`, and `hooks/` by domain.
- Leave third-party, generated, and build output folders alone.

## Output

The final tree of what changed, plus any risks or things to verify.
