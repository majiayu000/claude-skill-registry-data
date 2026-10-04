---
name: install-from-remote-library
description: Use when installing skills from a shared ai-agent-skills library repo. Inspect with `--list` first, prefer `--collection`, and preview with `--dry-run` before installing.
category: workflow
version: 4.1.0
---

# Install From Remote Library

## Goal

Install from a shared library repo without guessing, over-installing, or skipping the preview step.

## Invariants

- Always inspect the remote library first with `install <source> --list`.
- Prefer `--collection` when the library clearly exposes a starter pack or focused bundle.
- Always run `--dry-run` before the real install.
- Keep the install small. Do not pull a whole library when the user only needs a narrow slice.

## Workflow

1. Inspect the source library.

```bash
npx ai-agent-skills install <owner>/<repo> --list
```

2. Choose the smallest fitting target.

- Prefer `--collection starter-pack` or another named collection when it matches the user's need.
- Use `--skill <name>` only when the user needs one specific skill or the library has no useful collection.
- Do not combine `--collection` and `--skill`.

3. Preview the install plan before mutating anything.

```bash
npx ai-agent-skills install <owner>/<repo> --collection starter-pack --dry-run -p
```

or

```bash
npx ai-agent-skills install <owner>/<repo> --skill <skill-name> --dry-run -p
```

4. If the plan looks right, run the real install with the same scope.

```bash
npx ai-agent-skills install <owner>/<repo> --collection starter-pack -p
```

## Decision Rules

- If the library has a curated collection that already matches the user's stack, use it.
- If the remote library is empty or the list output is unclear, stop and report that instead of guessing.
- If the install path throws an `ERROR` / `HINT`, surface that verbatim and follow the hint before retrying.
- If the user is exploring a large library, keep them in browse mode first rather than installing immediately.

## Done

Return:

- what source library you inspected
- which collection or skill you chose
- the dry-run result
- the exact final install command you used
