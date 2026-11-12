---
name: instruction-review
description: Review a project's instruction file (CLAUDE.md or AGENTS.md) against recent work and propose a minimal evidence-backed diff without applying it. Use when the user asks to improve or review project instructions or invokes instruction-review, for example "improve CLAUDE.md", "review the project instructions", "what should go in CLAUDE.md".
license: MIT
compatibility: "Claude Code"
argument-hint: "[--prune]"
---

# Instruction review

1. Read the project instruction file (`CLAUDE.md` or `AGENTS.md`); when `CLAUDE.md` only imports `@AGENTS.md`, review and edit `AGENTS.md`, never add rules beside the import. Also read any project context file the repository documents, the project's active plan, and recent git history and diffs.
2. Keep only durable instructions supported by repeated work, a concrete defect, or an explicit user correction.
3. Exclude code-discoverable facts, one-off debugging history, rules already present in the developer-os core rules or the user's global instructions, and unsupported preferences.
   Flag existing entries that are stale or contradict the current code for removal, each with its reason. Keep the resulting file under 100 lines, the target the project templates set; when it would exceed that, propose moving the excess to project documentation with a one-line pointer.
4. Before proposing a line, search the file's history for its key phrase (`git log -p -S '<phrase>' -- <file>`). If the change reverses an earlier commit, show that commit and ask whether to reverse it. A mistake made at least twice that a lint rule, test or script can detect is proposed as that check, not as a line.
5. Propose a minimal unified diff. Apply nothing without explicit approval.
6. Give three bullets linking each proposal to evidence and naming removed duplication.

If no durable improvement exists, output exactly: `NO CHANGES`.

## `--prune` mode

Cuts instead of adds. Use it when the user invokes `instruction-review --prune` or asks to prune the file, when the default model changes, and every six months.

Scope: the project's `CLAUDE.md` or `AGENTS.md`. Review `plugin/rules/core.md` only inside the developer-os repository itself; elsewhere it belongs to the plugin, not the project.

1. Read the same sources as step 1. Give every non-blank line that is not a heading one verdict:
   - **DELETE**: code-discoverable, duplicated in the core rules or global instructions, stale or contradicted by the code, or a hedge that changes no behaviour ("verify twice", "don't overthink", "be careful").
   - **REWRITE**: a real rule that is vague, hedged, or contradicts another line. Give the new text.
   - **KEEP**: everything else.
2. Every DELETE and REWRITE names its source: `file:line`, a commit, the duplicated rule, or for a contradiction the other line's number. Flag both lines of a contradicting pair.
3. Never DELETE a truthfulness rule: a line that requires evidence, forbids claiming unverified results, or requires reporting failures. REWRITE it only for clarity, keeping its meaning.
4. List under `NOT RUN` every check you could not make (a command you did not execute, a path outside the repository, history older than what you read). A line whose check did not run stays KEEP.
5. ADD only rules that pass step 2 of the review above.

```
| line | text | verdict | reason / source |
|---|---|---|---|
| 14 | Verify twice before committing. | DELETE | hedge; core rules "Before each commit, run the fast check" |
| 22 | Use pnpm. | REWRITE → "Use pnpm (pnpm-lock.yaml)." | contradicts line 31 "npm install" |
| 31 | Run npm install after pulling. | DELETE | contradicts line 22; package manager is pnpm (pnpm-lock.yaml) |
NOT RUN: `make e2e` (line 40) not executed
Totals: DELETE 2 · REWRITE 1 · ADD 0 · KEEP 37
```

Show the table and the resulting diff; apply nothing without explicit approval. If every line is KEEP and nothing is added, output exactly: `NO CHANGES`.

## Stop point

Stops after the proposed diff (or the `--prune` table and diff) and its evidence, or after `NO CHANGES`. Applies the diff only after the user approves it, then reports the changed file. Inside the developer-os repository, a change to `plugin/rules/core.md` also adds its row (date | change | target | reason) to the Rules history in `docs/product/decisions.md`, in the same approved diff.

## Never

- Apply a change to the instruction file before the user approves the diff.
- DELETE a truthfulness rule.
- Mark a line DELETE or REWRITE without naming its source.
