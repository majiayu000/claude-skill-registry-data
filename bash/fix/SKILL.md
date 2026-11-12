---
name: fix
description: >
  Auto-repair what /claude-wiki-pages:lint reports. Idempotent — running
  twice on a clean tree produces no diff. Trigger when the user says "fix the
  lint errors", "repair the wiki", "auto-fix", or invokes
  /claude-wiki-pages:fix directly. Expects a fresh lint report in
  context, or runs its own lint pass internally.
allowed-tools: Read Write Edit Glob Grep Bash
disable-model-invocation: true
---

# LLM Wiki — Fix

Apply the repairs `/claude-wiki-pages:lint` identified.

## When to invoke

- The user has just run lint and asks to fix what it found.
- The `claude-wiki-pages-curator-agent` agent is orchestrating the lint → fix → lint cycle.
- The user is confident enough to fix without a prior lint pass (in which
  case this skill runs lint internally first).

## Inputs

One of:

- A recent lint report in conversation context.
- A fresh lint pass run internally (no report in context).

In both cases, the schema (`vault/CLAUDE.md`) is read first.

## Reading contract

- `vault/CLAUDE.md` — the schema.
- `vault/wiki/**/*.md` — every wiki page that a lint rule flagged.
- The lint report, when provided.

## Writing contract

Writes are confined to what the specific lint finding authorizes:

| Finding                           | Repair                                                                                 |
| --------------------------------- | -------------------------------------------------------------------------------------- |
| Missing required frontmatter      | Backfill with the schema default. If no sane default exists, escalate to the user.     |
| Dangling wikilink                 | Replace with the nearest matching alias; or comment out with `<!-- unresolved: ... -->` and flag as a remaining warning. |
| Plain-string `sources:` entry     | Convert to `[[wikilink]]` if the matching source page exists; otherwise leave and flag. |
| Missing `parent` / `path`         | Derive from file location under `wiki/`.                                               |
| MOC missing member                | Add the page or subfolder to `children:` / `child_indexes:` of its per-folder MOC (the folder note `<folder>/<folder>.md`, or legacy `_index.md` if present), as quoted `"[[wikilink]]"` entries. |
| Missing per-folder MOC            | Create the folder note at its canonical name `<folder>/<folder>.md` (`type: index`). Never create a new `_index.md`. |
| Legacy index filename (`legacy-index-filename` WARN) | Leave in place — this skill **never renames** an existing `_index.md`; the rename is `engine.sh migrate --write`'s job. Reconcile its fields like any folder note. |
| Banned legacy value               | Rewrite: `type: moc` → `type: index`; `_MOC.md` → the folder-note name; `child_mocs:` → `child_indexes:`. |
| Strict-tree drift (non-spine / cross-tree edge / cycle, `tree-lint` ADR-0036) | Run `bash scripts/strict-tree-reduce.sh --target <vault> --apply` (git-checkpointed) — it demotes every non-spine `[[wikilink]]` to prose and adds `topic/<tree>` de-cycle tags so the graph draws only the `parent:` spine. A deterministic graph-shape repair, not a per-page edit; **never hand-rewrite links to fake conformance**. Detect first with `bash scripts/tree-lint.sh --target <vault>`. |
| Vault MOC drift                   | Escalate to `/claude-wiki-pages:index`; do not edit `wiki/index.md` directly.     |

Always append one log entry:

```
## [YYYY-MM-DD] fix | repaired <N>, deferred <M>
```

This skill MUST NOT:

- Repair contradictions (warning-severity; needs human judgment).
- Invent a `sources:` entry when none exists.
- Delete a page because it is orphaned. Orphans are warnings, not garbage.

## Idempotency

Every repair this skill applies must be safe to run twice. After a fix pass:

- Re-running lint shows strictly fewer or equal errors.
- Re-running fix on the result produces zero file modifications.

If a repair is not idempotent, mark it as deferred and list it in the
completion summary with an explanation.

## Workflow

1. **Schema.** Read `vault/CLAUDE.md`.
2. **Load findings.** Consume the provided lint report, or run lint inline.
3. **Group.** Bucket findings by rule.
4. **Apply.** Walk each bucket; apply the authorized repair; let
   `PreToolUse` hooks enforce the schema on every write.
5. **Escalate.** For findings not authorized above (contradictions, fabricated
   sources, vault-MOC rebuilds), surface with a one-line explanation.
6. **Re-lint.** Invoke lint internally; confirm the error count is strictly
   lower.
7. **Log.** Append the fix entry to `wiki/log.md`.

## Hook enforcement

Every write passes through `PreToolUse`: frontmatter, wikilinks, raw
immutability, attachments. A failing hook means the proposed repair is wrong;
do not retry the same content — adjust it.

When this skill is invoked inside the `claude-wiki-pages-curator-agent` agent, `SubagentStop`
runs a final lint gate. The agent blocks completion if that gate returns a
non-zero exit.

## Completion signal

```
READY: repaired <N>, deferred <M>. Re-lint: <K> errors (was <E>).
```

If `K >= E`, print:

```
FAILED: fix pass did not reduce error count. Inspect deferred items.
```

and exit non-zero.
