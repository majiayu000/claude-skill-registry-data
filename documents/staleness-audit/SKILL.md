---
name: staleness-audit
description: Pre-commit audit. Invoke before every git commit. Diffs the staged change against the repo's "canaries" (README, decision log, roadmap, public API, doc comments, release notes, test discipline) and surfaces anything that's drifted out of sync. Updates the obvious drifts in place; flags judgement calls for the operator.
---

# Staleness audit

Run this before every commit. The goal is simple: **a commit should leave the docs, types, and roadmap in a state consistent with the code it ships**. Drift between code and its surrounding narrative is how projects rot.

Don't be lazy, actually run the checks. Each one is a `grep` or a `diff`. The whole audit should take under 30 seconds.

## How to invoke

You (the model) invoke this skill yourself, before staging the final commit. The rule: *every commit goes through this checklist*. If you're amending or splitting commits, run it per commit.

## Inputs

- `git diff --staged --stat`, what's about to be committed
- `git diff --staged`, the actual hunks (only read the ones you need)
- `git status`, what's unstaged or untracked that might also be drift
- The repo working tree for the canary files listed below

## Procedure

Work through the checks in order. For each finding, either **fix it now** (if the fix is mechanical and in scope) or **note it explicitly** in the commit body / the response to the user (if it's a judgement call).

### 1. README staleness

The `README.md` is the project's storefront. After every commit, ask:

- **Status line**: does `## Status` (or the equivalent line) still match reality? Words like "pre-alpha", "bootstrapping", "WIP", "coming soon", "not yet implemented" need to age out as features ship. If this commit moves the needle, update the status text.
- **Roadmap checkboxes**: `- [ ] X` for things that *just shipped* in this commit (or earlier ones not yet ticked) should become `- [x] X`. Conversely, anything ticked that's been ripped out needs to be re-opened or removed.
- **Code examples**: if a public-API signature changed, do the README code blocks still compile and reflect the new shape? Grep the README for the renamed/removed identifier.
- **Badge accuracy**: if a CI workflow or license changed, the badges still point at the right thing.

### 2. Decision log integrity

If the project has a decision log (ADRs in `docs/decisions/`, RFCs, or equivalent), check:

- Any new decision file that isn't in the index. Add it.
- Any decision whose `Status:` says "Accepted" but is actually superseded by a later one, update status on both.
- Cross-references that point at filenames that no longer exist.

If the project has no decision log, skip this check.

### 3. Public API sync

If the project has a single public entry point, verify exports are in sync after every commit touching source files. The entry point varies by language:

- **TypeScript:** `src/index.ts` (or the barrel specified in `package.json#exports`)
- **Python:** `<package>/__init__.py`
- **Rust:** `src/lib.rs` (`pub use` re-exports)
- **Go:** exported symbols in the package's public files

For every export newly added in non-entry source files, is it re-exported from the entry point? For every removed export, is the entry point cleaned up?

If the project has no single entry point (e.g. a CLI tool, not a library), skip or adapt this check.

### 4. Doc comment completeness on public symbols

For the project's documentation format, spot-check staged source files:

- **TypeScript:** any new `export class / function / interface / type / const` without a leading `/** … */`?
- **Python:** any new public function/class without a docstring?
- **Rust:** any new `pub fn / pub struct / pub trait` without `///` doc comments?
- **Other:** apply the language's equivalent convention.

Flag any new public symbol without documentation. Flag existing doc comments that still say `TODO` or `@todo`.

### 5. Release note for user-facing changes

If the commit touches source files, ask: is this user-observable?

- If yes, verify it's captured in the project's changelog mechanism:
  - **Changesets:** a `.changeset/*.md` file (run `pnpm changeset` or `npx changeset` to draft)
  - **towncrier:** a `changelog.d/` fragment
  - **Manual CHANGELOG:** a new entry in `CHANGELOG.md`
  - **Conventional commits:** the commit message itself is the record, verify it's descriptive enough
- If no (pure internal refactor / test / docs / tooling), no release note is needed, but note that explicitly.

### 6. Contributor guide hygiene

If the project has a `CONTRIBUTING.md` (or equivalent), after any commit that adds or removes tooling:

- Search for references to tools that are no longer in the project's dependency manifest (`package.json`, `Cargo.toml`, `pyproject.toml`, `go.mod`, etc.).
- If a workflow changed (CI job, hook, script), make sure the contributor guide reflects it.

### 7. Test name discipline

Test names should describe **behaviour**, not method names. Grep newly added/changed test files for:

- `it("works")`, `test("test 1")`, `it("should work correctly")`, `it("returns the value")`, vague or method-centric. Flag.
- Good names: `it("rejects an out-of-range index with a RangeError carrying the attempted value")`.

This applies regardless of framework (Jest, Vitest, pytest, RSpec, Go test, etc.).

### 8. Stale markers in new code

Grep the staged diff for tokens that shouldn't ship:

- `TODO`, `FIXME`, `XXX`, `HACK`, `@todo`, fine if they reference an issue (`TODO(#42)`); not fine if naked.
- `console.log`, `debugger`, `.only`, `.skip` in test files.
- Leftover lint-suppression comments without an explanation.

### 9. Research catalog

If external research was conducted during this session (WebFetch, WebSearch, or Explore-agent fetches of URLs outside the repo) and the findings informed this commit:

- Was `/flagrare:research-catalog` invoked before the synthesis was returned? If not, run it now before committing.
- Does the consuming artifact (ADR, code comment, doc) cross-link back to the catalog file? If not, add the cross-link.

If no external research was conducted this session, skip this check.

### 10. Agent memory crosslinks


If the project uses a `~/.claude/projects/<path>/memory/` directory with `[[name]]` crosslinks, and this commit touches docs or memory files, check:

- Every `[[some-name]]` resolves to a file `some-name.md` in the memory directory for this project.
- The `MEMORY.md` index has an entry for every `.md` file (other than itself).

To find the memory path: derive it from `pwd`, the project memory dir is `~/.claude/projects/<pwd-with-slashes-replaced-by-dashes>/memory/`. If the directory doesn't exist, skip this check.

### 11. Commit message format

Before invoking `git commit`, verify the message matches the project's commit convention. Check the recent `git log` to identify what convention is in use, then verify the new message follows it. Common conventions:

- **gitmoji + conventional commits:** `✨ feat(scope): subject`
- **Conventional commits:** `feat(scope): description`
- **Free-form:** whatever the project's history establishes

Regardless of convention: subject should be ≤ 72 chars; body explains *why* when the change is non-obvious.

### 12. Automated-committer message format

If this commit touches CI/CD config or dependency management config, verify that any automated committers (Renovate, Dependabot, release bots, merge bots) produce messages that match the project's commit convention.

Check the relevant config files for the project's CI platform:
- **GitHub Actions:** `.github/workflows/`, `.github/renovate.json`, `.github/dependabot.yml`
- **GitLab CI:** `.gitlab-ci.yml`, `.gitlab/`
- **Other:** whatever config files control automated commits

The rule of thumb: if a tool can push a commit, its message template must satisfy the project's commitlint rules, or the merge strategy must ensure a manually-written squash message.

### 13. CI config drift

Whenever this commit touches CI config files:

- Check for version conflicts between tool inputs and config files in the repo (e.g. a package manager version pinned in CI that diverges from the one in the project's toolchain manifest).
- Confirm any pinned action/image versions are consistent across CI jobs.
- If a prerequisite tool was removed from the project, the corresponding CI step should go in the same commit.

## Output

When you're done, give the user a concise audit line for each check, `✓` if clean, `→ fixed: …` if you applied a mechanical fix, `⚠ needs decision: …` if it's a judgement call. Don't pad with checks that found nothing.

If any check found a real issue, *fix it before committing* unless the user explicitly opted out of fixing this round.

## Invoke `/flagrare:write-docs` for documentation drift

If any of checks 1, 2, 4, 5, or 6 surfaced drift (README staleness, decision log issues, missing doc comments, missing release notes, contributor guide hygiene), invoke `/flagrare:write-docs` to rewrite the affected sections. Pass it the specific files and the nature of the drift so it can apply craft-level prose rather than mechanical patching.

Skip this step when:
- The fix is purely mechanical (e.g. ticking a checkbox, updating a number).
- The affected file has its own writing guidelines that should take precedence. Check for: a style/voice section in the file itself, a repo-level writing guide (e.g. `docs/style-guide.md`, `WRITING.md`), or user instructions in `CLAUDE.md` / memory that specify how that file should be written. When project-specific or user-specific writing rules exist, follow those directly instead of delegating to `/flagrare:write-docs`.

If neither exception applies and the fix requires rewriting prose, descriptions, or explanations, `/flagrare:write-docs` owns the quality of that output.

## Anti-patterns (what this skill is not)

- It is not a substitute for the project's test/lint/build gate. That gate still runs.
- It is not a place to add new tests or refactors, those belong in the commit they relate to.
- It is not a license to chase every TODO across the repo, only the drift caused or revealed by *this* commit.

## After this skill: invoke `/flagrare:release-check`

Once the commit lands, invoke `/flagrare:release-check` immediately. That skill answers the post-commit question "is a release due?" and drafts a value-focused CHANGELOG entry when one is. Cheap when nothing's pending.

## Why this exists

Project rot starts when README says "pre-alpha" three months after v1.0, when the decision log shows choices nobody remembers the reasons for, when the roadmap shows boxes already ticked elsewhere. Catching drift at commit time costs ~30 seconds. Catching it at "why is our README lying" time costs hours and credibility.
