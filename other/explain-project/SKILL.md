---
name: explain-project
description: Explain what a project does, the problem it solves, and its end-to-end flow.
trigger: when the user uploads a project or asks what a codebase does / how it flows
---
## When to use
The user uploaded a repo (often a `.zip`) or asks what a whole codebase does and
how it flows.

## How
1. **Map it** — `list_dir` (plus `grep`/`find` if available) for the structure;
   read the `README`.
2. **Find entry points** — `main`/`app`/`cli`/server/`index`/`__main__` — and
   read them.
3. Explain in order: the **problem it solves** → the **end-to-end flow**
   (input → processing → output, naming the files) → **key components** →
   notable tech and risks.
4. For a large repo, `delegate` the exploration, then synthesise the findings.

## Avoid
- Inventing features; cite real files and paths.
- A file-by-file dump instead of the actual flow.

## Done well
A newcomer understands, in a few minutes, why the project exists and how a
request flows through it — grounded in real files.
