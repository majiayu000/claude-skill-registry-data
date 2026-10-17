---
name: docs-checker
description: Audit context files (CLAUDE.md, .claude/ tree, READMEs, docs) for broken references and verifiably stale content. Runs a deterministic offline link/path checker first, then a bounded semantic review where every finding must cite evidence. Reports findings; fixes only on request. Use when the user says "docs check", "/docs-checker", "check the docs for stale content", "audit CLAUDE.md", or when a scheduled cloud routine fires.
argument-hint: "[paths...] [--repo=NAME:DIR]"
---

# Docs Checker

Audit the repository's context files — `CLAUDE.md` at any depth, the `.claude/` tree (skills, rules, commands), READMEs, and the docs tree — for correctness. This is a **conservative audit**: report findings with evidence, do not rewrite anything unless the user asks. Style, tone, and level of detail are the author's choices and are out of scope.

## Prerequisites

- Node.js >= 22 (the bundled script uses `fs.globSync`)

## Workflow

### 1. Deterministic pass

Run the bundled checker from the repo root:

```bash
node ${CLAUDE_SKILL_DIR}/scripts/docs-check.mjs $ARGUMENTS
```

It needs no config and no dependencies. What it does:

- Checks relative/absolute markdown links and image assets against the working tree
- Checks backticked source paths in prose (`src/foo.ts`, `@alias/bar`) against the codebase, resolving tsconfig/package.json aliases
- Scans the paths you name (or the repo's docs tree by default), plus every `CLAUDE.md` and the whole `.claude/` tree automatically
- Cross-repo docs: pass `--repo=NAME:DIR` for each sibling checkout the docs reference

Exit 0 is clean, 1 means findings (printed as `line:col rule message` with did-you-mean hints), 2 is bad invocation. Its findings are ground truth — do not second-guess them.

### 2. Semantic pass

Read the context files the script scanned — but keep this pass on a **scoped diet**: `CLAUDE.md` files, the `.claude/` tree, and top-level READMEs. Do not crawl the whole docs tree unless the user asked; the script already covered the wide surface.

Look only for claims you can **verify against the repo right now**:

- Commands or scripts quoted in docs that don't exist (check `package.json` scripts, `Makefile`, bundled scripts)
- Described behavior that contradicts the code it points at (read the code before claiming this)
- Instructions that contradict each other across context files
- Sections duplicated between files (e.g. README and CLAUDE.md drifting apart)
- References to tools, versions, or structures the repo no longer uses

Rules that keep this pass honest:

- **Every finding must cite its evidence** — the file and line that proves the claim stale. If you cannot point at proof, it is not a finding.
- No style or wording opinions. "Could be clearer" is not a finding.
- When unsure whether something is stale or intentional, list it under "unverified" rather than asserting it.

### 3. Report

Present one combined report:

1. **Deterministic findings** — the script output, summarized by file
2. **Semantic findings** — each as: claim, evidence (file:line on both sides), suggested resolution
3. **Unverified observations** — only if any; clearly separated

End with the totals. **Do not edit any file.** If findings exist, offer to fix them — deterministic findings (broken links, moved paths) are safe to fix mechanically once the user agrees; semantic findings need the user to decide the correct current truth first.

## Suppressions

The script honors inline suppressions the user may already have in place:

- `<!-- docs-check-ignore -->` at the end of a line
- `<!-- docs-check-disable -->` … `<!-- docs-check-enable -->` around a region
- `--no-agent-docs` flag to skip CLAUDE.md/.claude/ scanning
