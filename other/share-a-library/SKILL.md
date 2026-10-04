---
name: share-a-library
description: Use when a managed library is ready to publish to GitHub and hand to teammates as an install command. Run the GitHub publishing steps, then return the exact shareable install command.
category: workflow
version: 4.1.0
---

# Share A Library

## Goal

Turn a finished local library into a real shared artifact with a repo URL and an install command another agent can use.

## Preconditions

- You are already inside a managed library workspace.
- The library has been sanity-checked.
- `npx ai-agent-skills build-docs` has already run, or you run it now before publishing.

## Workflow

1. Regenerate docs if needed.

```bash
npx ai-agent-skills build-docs
```

2. Publish the workspace to GitHub.

```bash
git init
git add .
git commit -m "Initialize skills library"
gh repo create <owner>/<repo> --public --source=. --remote=origin --push
```

3. Return the exact shareable install command.

If the library has a `starter-pack` collection:

```bash
npx ai-agent-skills install <owner>/<repo> --collection starter-pack -p
```

Otherwise:

```bash
npx ai-agent-skills install <owner>/<repo> -p
```

## Guardrails

- Do not stop at `git init`. A shared library is not shared until the repo exists and the install command is ready.
- If the repo already exists, connect the existing remote and push instead of creating a duplicate.
- Prefer the collection install command when a curated starter pack exists.
- Return the actual repo coordinates you used, not placeholders.

## Done

Return:

- the repo URL
- whether you shared a collection or the whole library
- the exact install command to hand to teammates
