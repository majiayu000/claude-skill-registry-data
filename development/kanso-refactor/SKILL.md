---
name: kanso-refactor
description: Use when the user asks to clean up, tighten, simplify, de-bloat, de-slop, or refactor code. Also use when acting on findings from /kanso-audit or /kanso-nuclear. Behaviour-preserving only.
argument-hint: "[scope: diff|path|audit-report|current-file]"
disable-model-invocation: true
allowed-tools: Bash(git *) Bash(rg *) Bash(find *)
---

# kanso-refactor

Behaviour-preserving cleanup. Removes dilution, tightens code, deletes cruft. Never changes behaviour. If a change would alter behaviour, the skill surfaces it as a question instead of making the change.

The principles from `kanso-principles` apply. The anti-dilution taxonomy is the primary target.

## Always run inline

This skill runs in the calling chat — including when invoked as the follow-up to `/kanso-audit`. Never dispatch via the Agent or Task tool, never run as a subagent, never split work into a parallel runner whose output lands in a side window. Edits, summaries, and any clarifying questions all happen in the user's current transcript.

## The hard rule

**Refactoring must not alter behaviour. Behaviour changes must avoid refactoring.**

Mixing the two obscures intent, breaks cherry-picking, and ruins git bisect. If a task requires both, do them in separate commits, each with a single purpose.

Before making any change, ask: would this change produce different outputs for any input the existing tests or usage patterns cover? If yes, it's not a refactor. Stop and ask the user.

Cases where the boundary is tested:

- Removing a defensive try/catch that swallowed errors silently → behaviour change. The caller now sees the error. Ask.
- Inlining a filler variable → refactor. Identical behaviour.
- Replacing a manual loop with `itertools.chain` → refactor only if the iterator semantics are identical. Double-check laziness.
- Removing dead code that was unreachable → refactor.
- Removing dead code that was reachable but had no test coverage → behaviour change. Ask.
- Collapsing a premature abstraction → refactor if call sites are updated atomically. Verify.
- Renaming a variable → refactor if scope is local. If the name is exported, it's a behaviour change (API change). Ask.

When in doubt, treat it as a behaviour change and ask.

## Resolve the scope

`$ARGUMENTS` is one of:

- `diff` → the working tree changes (default)
- a path like `src/billing/invoice.ts` → that file or directory
- `audit-report` → the user will paste or reference a prior `/kanso-audit` report; act on its Tier 1 and Tier 2 refactor-category findings
- `current-file` → whatever file is in focus

If no scope is given and there's no obvious focus, ask.

## Calibrate before changing

Get the lay of the land in one turn before reading anything:

- Working tree state: `!git status --short`
- What's actually changed: `!git diff --stat`
- Recent commits for voice: `!git log -n 10 --oneline`

Then read surrounding code. Refactor decisions must fit the repo's existing style, not impose a new one. Check:

- Naming conventions (`get_*` vs `fetch_*`, camelCase vs snake_case)
- Error handling patterns (exceptions vs result types vs error returns)
- Comment density (some codebases genuinely warrant more comments)
- Formatter and linter configs — anything they enforce is not your job

If the repo has a test suite, note how to run it — the verify step below will use it.

## The refactor targets

Attack in this order. Stop when the signal-to-cost ratio drops.

### High value

1. **Delete dead code.** Unreachable branches, unused imports, unused parameters, unused variables, commented-out code. Git remembers.
2. **Delete tautological comments.** Comments that restate the code. Keep comments that carry business context, constraint reasoning, or non-obvious tradeoffs.
3. **Delete step-marker comments.** `// Step 1:`, `// Now do X`, `// Add retry as requested`. Always artefacts.
4. **Inline filler variables.** `const result = x(); return result;` → `return x();`. Keep the variable only if it adds a meaningful name or is referenced more than once.
5. **Collapse defensive theatre.** Remove nested try/catch blocks that return None on failure. Surface the failure case to the user as a question: "This swallows errors from `db.query()`. Should those propagate, be logged, or be wrapped?"

### Medium value

6. **Rename zero-entropy identifiers.** `userDataProcessingResult` → something that says what it is. Only if the scope is local; exported names are API changes.
7. **Replace vanilla reimplementations.** Manual `flatten` → `itertools.chain`. Hand-rolled `groupBy` → `lodash.groupBy` if already a dependency. Only if the replacement is genuinely equivalent.
8. **Collapse premature abstractions.** One-implementation factory, one-consumer interface, one-subclass base class. Inline them. Verify no external caller relies on the abstraction.

### Lower value

9. **Tighten over-long functions.** Extract a helper only if the extraction is used or makes the caller clearer. Don't extract for extraction's sake.
10. **Align with repo conventions.** Normalise mixed `get`/`fetch`/`load` patterns. But only within the touched scope — don't drift into unrelated files.

### Never targets

- Formatting that a formatter handles
- Style preferences not codified anywhere in the repo
- "Modernisation" that a linter could do
- Anything that changes a public API
- Anything that changes a test's pass/fail outcome

## Working process

1. **Identify candidates.** List what would change, grouped by target category above.
2. **Confirm the scope with the user if the list is large.** "I've found 23 things to clean up in this file. Want all of them, or just Tier 1?" Don't bulk-edit silently.
3. **Make changes one logical group at a time.** Each group should be commit-able independently (even though this skill doesn't commit).
4. **Preserve voice.** Match the author's existing code style, indentation habits, and comment density within the repo.
5. **Verify mentally.** For each change, walk through: does this produce the same output for the same input? If not, roll back.
6. **Verify.** Run the project's verification command (see below) and capture the result. A refactor that breaks the build isn't a refactor — it's a regression in disguise.
7. **Report what was done.** Summary at the end: what was deleted, what was inlined, what was renamed, with file:line references. Include the verify result. Flag anything deferred as a question for the user.

## Verify

A refactor is only behaviour-preserving if you can show it. Run the project's verification command after edits land and paste the exit code.

In Claude Code, kanso's PostToolUse hook already lint-checks each edited file as it lands. In a harness without edit hooks, that safety net did not run — the verification here is the only check, so never skip it there.

### Discover the command

In priority order:

1. **`AGENTS.md` / `CLAUDE.md`** — explicit commands. Use these first.
2. **`package.json` scripts** — `test`, `typecheck`, `lint`, `check`.
3. **`pyproject.toml`, `tox.ini`, `Makefile`** — `pytest`, `make test`, `make check`, `ruff`, `mypy`.
4. **`go.mod`** — `go test ./...`, `go vet ./...`.
5. **`Cargo.toml`** — `cargo test`, `cargo check`, `cargo clippy`.

Pick the narrowest command that covers the touched files. Typecheck plus the relevant test file is usually enough; a full suite is fine when the refactor is broad.

The command may prompt for permission on first run — that's expected. Don't reroute around it.

### Report the result

On pass:

```
✓ Verified — <command>
exit 0
<last meaningful lines>
```

On fail:

```
✗ Verification failed — <command>
exit <n>
<failing output>
```

Failure means the refactor altered behaviour. Roll back the edit and surface the surprise to the user — don't iterate silently to make the failure go away.

### When no command exists

```
⚠ No verification command found.
Checked: AGENTS.md, package.json, pyproject.toml, Makefile.
The refactor is applied but unverified — review the diff manually before committing.
```

Never silently skip. Either verify, or say you didn't and why.

## Output format

After making edits, produce a summary like:

```markdown
## Refactor summary

**Scope:** <what was refactored>
**Files touched:** <list>

### Changes made

- Deleted 14 tautological comments across `src/billing/*`
- Inlined 6 filler variables in `invoice.ts`
- Collapsed `UserProcessorFactory` into `processUser` (only one implementation existed)
- Removed dead import: `./legacy/unused-helper`

### Deferred — needs your decision

- `src/auth/session.ts:42` wraps `db.query()` in a try/catch that returns null on failure. Removing this would change behaviour. Should the error propagate, be logged, or be wrapped in a typed error?
- `src/api/user.ts:89` contains a `fetch_user` function while the rest of the module uses `get_*`. Renaming would be an API change if this is exported. Is it safe to rename?

### Verification

✓ Verified — `<command>`
exit 0
<last meaningful lines of output>

### Next steps

- Review the diff before committing
- Use `/kanso-commit` to stage and message the changes
```

## Framing

- Never use `git commit` directly. That's `/kanso-commit`'s job. This skill produces a clean working tree, nothing more.
- Never delete tests to make them pass. If a test breaks, the refactor altered behaviour. Roll back.
- Don't refactor and add features in the same session. If the user asks for both, do the refactor first, commit it, then move on.
- Don't touch files outside the requested scope unless a change is mechanically required (e.g. a callsite update for a rename). Scope creep is a leading indicator of a broken refactor.

## Failure modes to avoid

- Silently changing behaviour because the change "felt safe". Ask.
- Aggressive renaming that breaks imports elsewhere. Grep for usages first.
- Deleting comments that looked tautological but carried business context ("Legal requirement: 18+"). Read the comment fully before deleting.
- Refactoring a file the user didn't ask about because it was open in the session.
- Producing a giant changeset that can't be reviewed as a single logical refactor. Split.
