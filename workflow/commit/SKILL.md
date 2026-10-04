---
name: commit
description: Create a semantic commit message — works in SDD pipeline, vibe coding, and git-only workflows
allowed-tools: Bash(git status:*), Bash(git diff:*), Bash(git rev-parse:*), Bash(git log:*), Bash(git commit:*), Bash(git add:*), Bash(find .specwork:*), Bash(grep:*), Bash(test -f:*), Bash(python3:*), Write
---

# Git Commit

**Load**: `view ${CLAUDE_PLUGIN_ROOT}/skills/commit/SKILL.md`

---

## What It Does

| Step | Action |
|------|--------|
| 1 | Reads current branch, git status, and staged diff |
| 2 | If nothing staged → offers to stage modified/new files from `git status` (see Auto-Stage Offer) |
| 3 | **Test-coverage gate (STRICT)** — blocks if a changed production class has no matching test (see below) |
| 4 | Proposes a semantic commit message and waits for confirmation — **does not auto-commit** (see Format below) |
| 5 | Makes the commit on approval |
| 6 | Gets the short commit hash via `git rev-parse --short HEAD` |
| 7 | Offers to push the branch (see Push Offer) |

### Step 0 — Whose pipeline is this? (run before anything else)

`/sdd:commit` works in three modes — pipeline, standalone, and *someone else's
pipeline is still on disk*. Resolve which one before staging or committing:

```bash
BRANCH="$(git rev-parse --abbrev-ref HEAD)"
STATUS="$(python3 ${CLAUDE_PLUGIN_ROOT}/lib/gates.py pipeline-branch-status "$BRANCH")"
```

`STATUS` is one JSON object: `has_any_pipeline`, `owns_pipeline`, `slug`,
`recorded_branch`, `recorded_base_branch`, `is_base_branch`.

- **`owns_pipeline` is `true`** — pipeline mode. `SLUG` is `slug`; proceed normally.
- **`has_any_pipeline` is `false`** — standalone / vibe-coding mode. `SLUG` is empty;
  proceed normally, silently. This is a first-class flow, not a problem.
- **`has_any_pipeline` is `true`, `owns_pipeline` is `false`, `is_base_branch` is
  `false`** — a *different* branch's pipeline is sitting on disk. **Warn, then
  continue in standalone mode** (`SLUG` empty). Do not adopt it, and do not block
  the commit — the work in front of you is legitimate, it just is not that pipeline:

  ```
  ⚠ .specwork/ belongs to '<recorded_branch>' (slug '<slug>'), not '<BRANCH>'.
    It's gitignored, so it didn't move when you switched branches.

    Committing anyway, treated as standalone: no spec, no plan, and the coverage
    gate uses repo-level waivers only — '<slug>'s waivers do not apply here.

    To clean this up:
      • /sdd:pause  — stash '<slug>' to resume it later (its MR is still open)
      • /sdd:close  — clear it (its MR merged, or the work was abandoned)
      • /sdd:start  — begin a pipeline for '<BRANCH>' instead
  ```

  Print it once per `/sdd:commit` run, before the commit-message proposal, so the
  developer sees it while there is still a decision to make.
- **`is_base_branch` is `true`** — you are on the pipeline's own base branch (post-merge
  cleanup). Treat as standalone, no warning: `/sdd:close` is meant to be run from here.

Then rehydrate auto mode from **this branch's** state only:

```bash
if [ "${SDD_NON_INTERACTIVE:-0}" != "1" ] && [ -n "$SLUG" ]; then
  SDD_MODE="$(python3 ${CLAUDE_PLUGIN_ROOT}/lib/gates.py non-interactive "$SLUG" 2>/dev/null || echo 0)"
  [ "$SDD_MODE" = "1" ] && export SDD_NON_INTERACTIVE=1
fi
```

`non_interactive` is a property of *one* pipeline. Inheriting it from another
branch's leftover state would drop this commit's confirmation prompt — auto-committing
on a branch that never opted into `/sdd:auto`.

---

## Test-Coverage Gate (STRICT)

Run **after staging, before proposing the commit**. It is the deterministic
counterpart to `/sdd:implement`'s prose "Test Coverage" step: every changed
production class must have a matching test, or the commit is blocked.

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/lib/coverage.py check $SLUG
```

`$SLUG` comes from [Step 0](#step-0--whose-pipeline-is-this-run-before-anything-else)
and is left unquoted so an empty value passes no argument at all — the standalone
path, which reads the repo-level `.sdd-coverage-waivers.json`. Only a pipeline that
records *this* branch contributes its `_test/<slug>-coverage-waivers.json`; another
branch's leftover waivers must never silently excuse classes here.

- **Exit 0** → continue to the commit-message proposal.
- **Exit 1** → **do not commit.** Print the offender list verbatim from the
  command's output and stop.

What it checks (stack-aware, via `detect-stack`):

| Stack | Production file | Accepted test |
|-------|-----------------|---------------|
| Java | `src/main/.../FooService.java` | `FooService{Test,Tests,IT,ITCase}.java` anywhere under `src/test` |
| Frontend | `Foo.tsx` | `Foo.{test,spec}.*` (sibling) or `__tests__/Foo.{test,spec}.*` |

It is intentionally conservative — pure data/wiring types are **not** flagged:
Java `*Dto/*Request/*Response/*Entity/*Config/*Exception`, `package-info`, and
`config/`/`dto/`/`entity/`/`model/` packages; frontend `*.d.ts`, barrels
(`index.ts`), `*.styles/*.types/*.config/*.stories`. Unknown/node stacks pass.

**Escape hatch (the only one — "add a test or justify"):** a class with no
testable surface is waived by listing it with a written reason in a JSON file:

- In a pipeline: `.specwork/_test/<slug>-coverage-waivers.json`
- Standalone (vibe coding, no `.specwork/`): `.sdd-coverage-waivers.json` at the repo root

```json
{ "src/main/java/com/acme/SecurityConfig.java": "pure Spring wiring, no testable logic" }
```

This gate applies in every mode (interactive, non-interactive, and standalone).
There is no blanket skip — the waiver requires naming the file and the reason.

---

## Commit Format

```
[TICKET-ID] <type>: <concise description>

<optional body explaining why, not what>
```

Ticket extraction and subject formatting are done in code — decide the `<type>` and
`<description>` (judgment), then assemble the subject with:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/lib/titles.py commit-subject "$(git rev-parse --abbrev-ref HEAD)" "<type>" "<description>"
# → [PROJ-123] <type>: <description>   (or [NO-TICKET] when the branch has none)
```

**Commit types**

| Type | When to use |
|------|-------------|
| `feat` | New feature or behavior |
| `fix` | Bug fix |
| `refactor` | Code change with no behavior change |
| `docs` | Documentation only |
| `test` | Test code only |
| `perf` | Performance improvement |

---

## Commit Discipline

One logical change per commit.

Good:
```
[PROJ-15535] feat: add Flyway migration V23 for consent_flag column
[PROJ-15535] feat: add ConsentService with saveConsent logic
[PROJ-15535] feat: add ConsentController POST /api/v1/consent
[PROJ-15535] test: add unit and integration tests for consent flow
```

Bad:
```
[PROJ-15535] feat: consent stuff
```

---

## Auto-Stage Offer

Triggered when `git diff --staged` is empty. Reads the working tree state via `git status --porcelain` and lists every modified or new file:

```
Nothing staged. Files with unstaged changes:

  M  src/main/java/com/example/leads/service/ConsentService.java
  A  src/main/java/com/example/leads/dto/ConsentRequest.java
  A  src/test/java/com/example/leads/service/ConsentServiceTest.java

Stage these files? (yes / no / edit)
```

- **yes**: run `git add <file> ...` for each listed file, then continue to the commit message proposal
- **no**: skip staging, fall through to Reconcile Mode
- **edit**: show the list, let the user remove lines, re-display, ask again

If `git status --porcelain` returns no modified or new files, skip the prompt and fall through to Reconcile Mode.

---

## Push Offer

If nothing is staged and nothing to auto-stage, abort with:

```
Nothing to commit.
Stage your changes first, or run /sdd:implement to continue.
```

Otherwise, after committing, ask:

```
Push branch to origin now? (yes / no)
```

- **yes**: run `git push -u origin HEAD`
  - If the push is rejected (divergent history), surface the error and stop — do NOT force-push
  - Print the remote URL on success
- **no**: skip silently

This step is skipped entirely during Reconcile Mode (nothing to push — no new commit was made).

> **Inside an active SDD pipeline** (`.specwork/` present) the `PreToolUse(git push)`
> quality-gate hook blocks a push whose HEAD has not passed `commands/check.sh`.
> `/sdd:commit` does not run `check.sh`, so this push offer can be gated. If it is
> blocked, push via `/sdd:mr` (it validates, then pushes) or run `bash commands/check.sh`
> followed by `python3 ${CLAUDE_PLUGIN_ROOT}/lib/validation.py record` first. Outside a
> pipeline (no `.specwork/`) the hook no-ops and the push proceeds normally.

---

## Related Skills

- `state` — reads git state and spec to show pipeline progress
- `mr` — reads commit history to generate the MR description
