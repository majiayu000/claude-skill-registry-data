---
name: review-tidy
description: Coordinate comment cleanup through review-comments and fix the mechanical loose ends a change leaves behind — docs, examples and config that name a symbol, flag or path the change renamed or removed; imports, private helpers and files it orphaned; test names that no longer match; and the project's own formatter and lint autofixes. Use before a review or PR so reviewers see tidy code. code-review runs it as a preflight.
argument-hint: '[targets...] [--staged | --unpushed | --changed | --all] [--fix]'
effort: medium
---

<!-- Generated from https://github.com/nielsmadan/agentic-coding — edits here are overwritten. -->

# Review Tidy

Coordinate comment cleanup through `review-comments`, then fix the mechanical loose ends a change leaves behind. Mechanical fixes must have exactly one correct answer, deterministic or checkable by grep; other mechanical findings are reported for a decision. Comment removals and rewrites follow `review-comments` safety rules.

## Flags

- `--staged` - git staged files
- `--unpushed` - files changed across all unpushed commits
- `--changed` - git unstaged changes
- `--all` - entire codebase
- `--fix` - apply safe comment cleanup and every mechanical fix without prompting
- `targets` - one or more files or directories; overrides scope flags
- Default: `--staged --changed` combined

## Usage

```
/review-tidy                  # staged + changed (default)
/review-tidy --staged --fix   # fix what the staged change left behind
/review-tidy src/auth         # a file or directory
```

## The test for "mechanical"

A mechanical fix belongs here only if all of these hold:

- **One right answer.** The diff itself supplies the replacement (a rename gives the new name, a move gives the new path), or the fix is a deletion that grep proves safe.
- **No behaviour change.** The program does the same thing before and after.
- **Local.** It touches the stale line, not the design around it.

Everything else is a report item, never an edit. Rewriting prose about behaviour that changed is a report item. So is deleting something that looks unused but could be reached by name at runtime.

## Gotchas

- **Grep misses references built from strings.** Registries, dynamic imports, reflection, templates, routes and config files reach code by name. Before deleting anything, search for the bare name as a string literal too. If the name is generic (`get`, `data`, `handler`), you cannot rule out a reference: report it.
- **History is correct as written.** CHANGELOG entries, release notes, migration guides and ADRs describe the old name on purpose. Never edit them.
- **Code comments belong to `review-comments`.** Invoke it once as part of this workflow; keep its rubric there. The mechanical checks below cover docs, examples, config, help text and test names.
- **Never touch generated files** (lockfiles, `*.generated.*`, build output, vendored code). If one is stale, report that it needs regenerating.
- **`--staged` edits land unstaged.** Say so in the summary and never run `git add`.

## Workflow

### Step 1: Resolve scope

Parse flags and targets as `review-comments` does: the default is staged plus unstaged changes, a target overrides scope flags, and `--unpushed` uses the range `"$(git rev-list HEAD --not --remotes | tail -1)^"..HEAD`. If nothing is unpushed, or there is no upstream, stop and ask the user for another scope.

Capture the resolved file list and original diff before cleanup; retain both throughout this workflow even when edits change git status. If the caller supplied a resolved file list and diff, reuse them. A supplied file list does not discard the caller's diff-based scope.

### Step 1a: Comment cleanup

Invoke `review-comments` exactly once on the existing source files in the resolved list, passing `--fix` only when this invocation has `--fix`. Skip it when there are no source files, but continue the mechanical checks. Use its comment rubric and preserve its removal, rewrite and deferred counts for the combined report.

When a Skill tool is unavailable, read `review-comments/SKILL.md` and apply it in this session; a skill name is not a subagent name. Without `--fix`, follow its interactive choices for comment-only edits; leave executable-code refactors for a separate decision outside this cleanup.

Complete comment cleanup before mechanical edits. Both can touch the same files, so do not run their writers concurrently. Defer formatting and lint autofix to Check 4 after all approved cleanup edits. `review-comments` remains independently callable; do not invoke `code-review` from this skill.

### Step 2: List what the change removed or renamed

Read the original diff captured for the resolved scope (`git diff --cached`, `git diff`, or the unpushed range). Collect every name the change removed or renamed:

- identifiers: functions, classes, types, constants, exported names
- CLI commands and flags, environment variables, config keys, routes, event names
- file and directory paths (moved, renamed, or deleted files)

A rename is an old name paired with its new name in the same diff. Anything else that disappeared is a removal.

With `--all` or a standalone target without a caller-supplied diff, there is no diff. Skip to the orphan, path and formatter checks: run Check 2 over the scoped files, check that every repo path named in a doc file exists, and run Check 4.

### Step 3: Run the checks

**Check 1: Stale references.** For each removed or renamed name, search the whole repo outside the changed code: READMEs, `docs/`, `AGENTS.md` and `CLAUDE.md`, examples, config templates, CLI help and usage text, and skill or prompt files.

- A rename with an unambiguous new name: replace it.
- A moved path: update it.
- A removal with no successor, or a passage that describes behaviour the change altered: report it with the line and what changed.

**Check 2: Orphans.** For each import, function, constant, type or file whose last use the diff removed, search for remaining references, including string literals.

- File-private or unexported, with zero references: delete it.
- Exported, public, an entry point, or a reference you cannot rule out: report it.

**Check 3: Test names.** A test name or description that names a symbol the diff renamed: update the name. One that describes behaviour the change altered: report it.

**Check 4: Formatter and lint autofix.** Find the project's own configured tools in `package.json` scripts, `lefthook.yml`, `.pre-commit-config.yaml`, `pyproject.toml`, `Makefile`/`justfile`, or the language's standard formatter when its config is present (`rustfmt.toml`, `.swift-format`, `.rumdl.toml`). Identify the commands now; execute them once in Step 5 on the scoped files only, after every other edit.

- Never install a tool, change its config, or run a repo-wide format that touches files outside scope.
- Report lint errors the autofix left behind; do not hand-fix them here.

### Step 4: Report

```markdown
## Tidy: {scope}

### Comments
- {comments removed} removed · {comments rewritten} rewritten
- {deferred comment findings, if any}

### Fixed
- {file}:{line} — {what changed} ({check})

### Needs a decision
- {file}:{line} — {what is stale and why it is not mechanical}

### Formatter
- {tool}: {files changed} · {lint errors left, or "clean"}
```

Omit empty sections. If nothing was found, say `Nothing to tidy.`

### Step 5: Apply

**With `--fix`:** apply every mechanical item under Fixed without prompting, then run Check 4 exactly once, after comment cleanup and mechanical edits. Leave "Needs a decision" items unchanged.

**Without `--fix`:** if anything is fixable, ask whether to apply the fixes (all, or skip). Apply exactly what the user picks, then run Check 4 once after all approved edits. Do not repeat comment cleanup.

## Example

The staged diff renames `--dry` to `--dry-run` and deletes `formatLegacyDate`, the only caller of `padYear`.

- `README.md:41` shows `tool sync --dry` → replaced with `--dry-run` (Check 1).
- `docs/cli.md:12` says "`--dry` skips writes and prints a diff"; the new flag no longer prints a diff → reported (behaviour changed).
- `padYear` is unexported with no references left → deleted (Check 2).
- `prettier --write` on the four scoped files reformats one line → reported under Formatter.
