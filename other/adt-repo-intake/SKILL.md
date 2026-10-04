---
name: repo-intake
description: Onboard into an unfamiliar repository fast before making any changes
triggers:
  - new repo
  - onboard
  - what is this project
  - explore codebase
  - repo overview
---

# Repo Intake

Read local docs, detect the stack, summarize the structure, and flag blockers — before touching any code.

## Steps

1. **Read local instructions** — check README.md, AGENTS.md, CLAUDE.md, CONTRIBUTING.md
2. **Detect the stack** — scan package manifests, lockfiles, Dockerfiles, CI configs
3. **Map the structure** — identify entrypoints, source layout, test directories, scripts
4. **List primary commands** — run, test, build, lint, deploy (only what actually exists)
5. **Flag blockers** — missing env files, auth, broken deps, unclear setup steps

## Output

```text
Repo:      <name>
Stack:     <language, framework, package manager>
Commands:  <run | test | build | lint>
Blockers:  <missing auth | broken deps | none>
Next:      <top 1-3 actions>
```

## Rules

- Read docs before scanning code
- Never guess commands that are not present in the repo
- Stop if the repo root is unclear or ambiguous
- Flag missing setup steps instead of inventing them
