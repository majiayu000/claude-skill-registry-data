---
name: cleanup
description: >
  Scan the repo for dead code, debug artifacts, and other cruft. Reports findings with
  file:line citations, then applies fixes category by category with user confirmation.
  Use when the user says "cleanup", "clean up", "dead code", "remove todos",
  "purge debug logs", "remove console logs", "unused imports", "/cleanup",
  "remove commented code", "clean the repo", or "repo hygiene".
---

# Cleanup

Announce at start: `Running cleanup scan...`

Scan the repo for cruft across 9 categories, write the full report to a markdown artifact, then apply
fixes one category at a time after the user confirms each.

The value of this skill is its false-positive filtering, not its pattern matching. A noisy report the
user has to re-verify is worse than a short one they can trust - prefer fewer, high-confidence
findings, and verify every candidate against Step 2 before it reaches the report.

Args: `--branch` (default, scans files changed vs the base branch) or `--full` (whole working tree).

## Delegation

Steps 1-4 are the delegable half: they read broadly, verify candidates, and end at a saved report
path. Hand them to a subagent when a delegation mechanism exists and the session holds context worth
protecting - especially under `--full`, where the scan reads the whole tree and almost none of it
belongs in the main thread. Brief it with the scope args, the Step 2 verification rules, the category
list, the report format, and the save path; take back only the report path and the summary counts.

Step 5 never delegates. Confirming categories with the user and applying edits belongs to the main
agent, which reads the saved report first and owns every file it changes.

## 1. Scope

```bash
BASE=$(git merge-base HEAD main 2>/dev/null \
  || git merge-base HEAD master 2>/dev/null \
  || git rev-parse origin/HEAD 2>/dev/null)
git diff "$BASE"...HEAD --name-only
```

Always skip `*.generated.*`, `*.min.*`, `*.lock`, `*.snap`, binaries, and `dist/ build/ vendor/
node_modules/ .next/ __pycache__/`. If `--branch` finds no files, say "No changed files found vs
base. Try `--full` to scan the whole repo." and stop.

Identify the stack (JS/TS, Vue/Nuxt, Next.js, Python, Go) and note whether the repo has tests, Husky
or commitlint config, and framework config files - Step 2 needs all of these.

## 2. Verification rules

Apply these to every candidate before reporting it.

**Docs are not code.** A match appearing only in `context/`, `docs/`, `README*`, `CHANGELOG*`, other
markdown, generated files, lockfiles, or binaries is not a cleanup finding.

**Framework and config awareness.** Before calling anything unused, check whether it is referenced
from framework config (`nuxt.config.*`, `next.config.*`, `vite.config.*`, `vitest.config.*`), tool
config (`eslint.config.*`, `.eslintrc*`, `commitlint.config.*`, `prettier.config.*`), git hooks
(`.husky/**`), or `package.json` scripts. If it is, it stays.

**Test awareness.** Search tests (`**/*.test.*`, `**/*.spec.*`, `**/__tests__/**`) as well as runtime
code. Something used only by tests is reported as, not as dead:

```text
file:line - test-only export: <name> (keep if intentional test surface)
```

**Same-file exports.** An exported symbol used only inside its own file is a lower-severity hint, not
a dead export:

```text
file:line - export can likely be de-exported: <name> (used only within source file)
```

**Framework packages.** `depcheck` is incomplete on framework repos. Before reporting a package,
verify all of: module registration in `nuxt.config.*`/`next.config.*`, use via auto-components or
auto-imports, CSS entrypoint usage (e.g. `tailwindcss`), and CLI or hook usage through
`package.json` scripts or `.husky/**`.

## 3. Scan

Read `references/scan-categories.md` and run every category, collecting findings before modifying
anything:

A - Unused Imports 🔧 · B - Commented-Out Code 🔧 · C - Debug Artifacts 🔧/⚠️ · D - Dead Exports ⚠️ ·
E - Stale Suppression Directives ⚠️ · F - Empty Files 🔧 · G - Unused Packages ⚠️ · H - Stale Feature
Flags ⚠️ · I - Unreferenced Pages/Routes ⚠️ (Nuxt/Next only)

## 4. Write the report

Render the full report to `~/.agents/cleanup-plans/<repo>/<slug>-cleanup-plan.md` - slug preference:
ticket key → branch name → repo name, kebab-cased - with frontmatter `date`, `repo`, `branch`, `mode`.

```markdown
## Cleanup Scan - <branch name or "full repo">
**Scope:** <N> files scanned · <date>
**Stack:** <detected stack>

### A · Unused Imports 🔧
`file:line` - unused import: `<name>`
_(none)_ if clean

### B · Commented-Out Code 🔧
`file:line` - commented-out code block (N lines)

### C · Debug Artifacts
🔧 `file:line` - debug: `console.log(...)`
⚠️ `file:line` - TODO: <text> ← manual action only

### D · Dead Exports ⚠️
`file:line` - ⚠️ dead export: `<name>` (verify before removing)
`file:line` - export can likely be de-exported: `<name>` (used only within source file)
`file:line` - test-only export: `<name>` (keep if intentional test surface)

### E · Stale Suppression Directives ⚠️
`file:line` - ⚠️ `@ts-ignore` (verify still needed)

### F · Empty Files 🔧
`path/to/file` - empty file

### G · Unused Packages ⚠️
`package.json` - ⚠️ verified unused package: `<name>`

### H · Stale Feature Flags ⚠️
`file:line` - ⚠️ `FLAG_X = true` (hardcoded)

### I · Unreferenced Pages ⚠️
`file` - ⚠️ route `/path` has no references (verify)

### Verification Notes
- Suppressed as docs-only false positives: <count or _(none)_>
- Suppressed as framework/config usage: <count or _(none)_>
- Suppressed as test-only usage: <count or _(none)_>
- Reclassified from dead export to de-export hint: <count or _(none)_>

---
**Summary:** <N> auto-fixable 🔧 · <M> manual review ⚠️
```

The terminal gets the file path and the confirmation prompts - nothing else. The report body stays in
the file.

```text
[cleanup-plan.md](<absolute path>)
Apply fixes for Category A? (yes / no / show-me-first)
```

## 5. Confirm and apply

Ask once per category holding at least one 🔧 finding. `show-me-first` prints the exact lines or diff
and re-asks. "Apply all fixable" confirms every 🔧 category at once. For categories with only ⚠️
findings, say they need manual review and move on.

Apply only confirmed categories, using the repo's own tooling where it exists:

- **A - Unused imports:** the repo's linter with its fix flag (`eslint --fix`, `ruff check --fix`,
  `goimports -w`).
- **B - Commented-out code:** Edit out each flagged block in full, not just its first line.
- **C - Debug artifacts:** Edit out flagged `console.log` / `print` / `debugger` lines. TODO, FIXME,
  and HACK lines stay.
- **F - Empty files:** confirm each individually, then `rm`.
- **G - Unused packages:** print the uninstall command for the user to run rather than running it.

Then `git diff --stat` and report:

```markdown
## Cleanup Complete

**Applied:** <N> categories fixed · <M> files modified
**Skipped:** <list>
**Manual review needed:** <count of ⚠️ findings - list categories>

Run your test suite to verify nothing broke.
```

Close by naming what you filtered out - docs-only, config-driven, framework-convention, and test-only
false positives - and reminding the user that the remaining ⚠️ findings are surfaced but untouched.
