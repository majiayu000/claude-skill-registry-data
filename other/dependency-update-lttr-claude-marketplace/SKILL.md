---
name: dependency-update
description: Periodic dependency update run. Reads what the package manager says is outdated, upgrades what is safe, applies the code changes the new versions need, verifies, and opens one reviewable PR. Supports a read-only dry run that reports what it would do. Use when the user says "dependency update", "/dependency-update", "update deps", "dry run the dep update", or when a scheduled cloud routine fires.
argument-hint: "[dry-run]"
allowed-tools: Bash, Read, Write, Edit, Glob, Grep, WebFetch
---

# Dependency update

One run produces at most one pull request. Apart from the scan script
(`${CLAUDE_SKILL_DIR}/scripts/dep-scan.mjs`), every step here is a judgement call, not a mechanical
procedure.

Merging the PR may deploy to production, and nothing is automerged. The goal is
therefore a PR a tired human can review honestly in a few minutes, not the
largest batch that passes CI.

**Dry run** (`/dependency-update dry-run`, or any "dry run" / "just report"
phrasing): do §0–§3 strictly read-only — no branch, no install or update, no
edit, commit, push, PR, or run note — then print a report and stop. The
report covers what you would bump and would not, and why (including the
breaking-change evidence for majors), the exact commands §4 would run, the
DELETE-WHEN status, and what even a real run could not verify; state up front
that nothing was verified. Still read the release notes — the value of a dry
run is the reasoning about each update, not the list of versions. Stop
conditions from §0 don't stop a dry run; name them in the report and carry on
scanning. Do not proceed to §4 unless the user asks in a new message.

## What this skill does not know

This skill carries the procedure. It does not carry any project's specifics,
and it should not be edited to. Before §0, learn them from where that project
already enforces them:

- **A project skill wrapping this one**, if there is one. A repo with real
  toolchain constraints is better served by its own skill (`nuxt-deps-update`
  and the like) that names the run's additional rules and then defers here for
  the procedure. When you were invoked through such a skill, its rules win over
  every default below.
- **The workspace config itself** — `pnpm-workspace.yaml`, the root
  `package.json`. Comments at the point of enforcement are the most reliable
  source a repo has, because the person editing the pin reads them.
- **The repo's `CLAUDE.md`** — especially its verification and shipping
  sections.

Where none of them answers, use the defaults named below, and say in the PR
body which defaults you had to assume.

## 0. Preflight: stop conditions

Run these first. If any stop condition holds, do the stated thing and end the
run; do not "work around" it.

```bash
BASE=$(git symbolic-ref --short refs/remotes/origin/HEAD | sed 's|^origin/||')   # or the profile's base branch
git fetch origin --quiet
gh pr list --state open --json number,title,headRefName \
  --jq '[.[] | select(.headRefName | startswith("claude/deps-"))]'
```

- **A dependency PR is already open** → do not rebase, supersede or close it.
  Write the run note (§7) saying which PR is open, say so in the final
  message, stop. What happens to that PR is the maintainer's call.
- **Working tree dirty, or HEAD is not an ancestor of `origin/$BASE`** → stop
  and say so. This run only ever starts from a clean, current base branch.

On a host that is not GitHub, use its own CLI for the open-PR check and for §8
(`az repos pr list` on Azure DevOps, `glab mr list` on GitLab). The stop
condition is the same; only the command changes.

Set the run identifier once and reuse it:

```bash
WEEK=$(date +%G-W%V)   # e.g. 2026-W35
TODAY=$(date +%F)
```

## 1. Scan

```bash
node "${CLAUDE_SKILL_DIR}/scripts/dep-scan.mjs" > /tmp/dep-scan.json
jq '.manager, .counts' /tmp/dep-scan.json
```

It detects the repo root from git, and the package manager from the lockfile
(pnpm and npm are supported; for yarn or bun it sets `scanError` and you do the
outdated pass by hand). The JSON output holds one row per outdated direct
dependency per workspace, with `declared` (the range in `package.json`), `bump`
(`patch`/`minor`/`major`, 0.x-aware), `inScope`, `outOfScopeReason` and `repo`.

- `inScope: false` rows are **report only**: exact pins, `catalog:` aliases,
  `npm:`/`workspace:` aliases and packages covered by an override. Never bump
  them. They go in the PR body's "Reported, not touched" section. An exact pin
  is someone's decision; when the workspace config or a project skill says why,
  quote that reason rather than re-deriving it.
- Read `pnpm-workspace.yaml` and the root `package.json` for `# ISSUE:` /
  `# DELETE WHEN:` comment pairs. Evaluate each condition against what you
  learned reading release notes and report it as satisfied or not. **Never
  remove a workaround**, even when its condition is satisfied.
- `duplicateMajors.duplicates` lists every package installed at two or more
  majors. In a large tree that is routinely a hundred rows and most are
  harmless, so do not report it wholesale — it is a lookup table for §6, not a
  section of the PR. Pass `--tsconfig-paths=<glob>` when the project generates
  tsconfigs that record which copy won (a project skill will name the glob) and
  the rows gain `pathsAt`; those few are worth reporting.
- `counts.inScope == 0` → nothing to do. Write the run note (§7), say so,
  stop.

## 2. Read release notes, but only where it pays off

Fetch notes per package, only when needed. Read notes for: **every major**,
every package in an indivisible group the profile names, and minors of
consequential packages — anything that touches build, lint, types, runtime
rendering, or the project's data layer. Patch bumps and pure data packages
(icon sets, locale tables) need no reading.

```bash
gh api repos/{owner}/{repo}/releases --paginate --jq \
  '.[] | select(.draft==false and .prerelease==false) | {tag: .tag_name, body: .body}' | head -c 40000
```

`gh` is authenticated, so the unauthenticated 60/hour ceiling never applies.

Two rules:

- **Tag-to-package guard.** Monorepos tag per package (`@nuxt/kit@4.2.0`,
  `nuxt@4.5.2`). Match releases to _this_ package by name; never compare bare
  version numbers across a monorepo's tags, or you will read another package's
  breaking changes as your own.
- **Thin-changelog rule.** When notes are missing or thin for a significant
  jump, fetch the actual changelog (`CHANGELOG.md` on the default branch, or
  the project's migration guide) with WebFetch rather than reasoning from the
  version number. Rows with `repo: null` have no GitHub source: use
  `https://www.npmjs.com/package/<name>?activeTab=versions`.

## 3. Decide the shape of the run

**What matters is the impact on this codebase, not the semver digit.**

- A **major whose breaking changes provably do not touch this codebase** goes
  into the batch. "Provably" means: you read the breaking-change list, and for
  each item you searched our source and found nothing. Record the evidence
  (the item, the search, the result); it goes in the PR body.
- A **major that demands real code changes** gets its own PR, at most one per
  run. Further such majors are listed as queued in the batch PR and left alone.
- **Indivisible groups move together or not at all.** A framework and its
  first-party packages, a linter and its plugins, a test runner and its
  adapters: shipping half of one is how you get a red build with no single
  culprit. A project skill or the workspace config names the groups that repo
  has; a catalog entry shared by several packages is usually one.
- When a package ships a **codemod or migration CLI**, find it in the release
  notes and run it instead of re-deriving the changes by hand.

When an update could go either way, prefer the batch PR: only one PR ships per
run, and a migration PR uses up that slot.

## 4. Branch and apply

```bash
git switch -c claude/deps-$WEEK    # migration run: claude/deps-$WEEK-<package>
pnpm update --latest <pkg> <pkg> ...            # root workspace packages
pnpm --filter <ws> update --latest <pkg> ...    # per-workspace packages
pnpm dedupe                                      # when the lockfile gained duplicates
```

Under npm the equivalents are `npm install <pkg>@latest ...` and `npm install
-w <ws> <pkg>@latest ...`.

Always name the packages explicitly: a bare `update --latest` would also bump
the out-of-scope rows.

**Commit 1 (bumps only)**: `package.json`(s), the lockfile, and the run note
from §7 — nothing else. Subject `deps: batch update $WEEK`; body lists each
bump (`name current → latest`) and quotes the exact update commands run.

## 5. Repair the code

Only now touch source. Codemod output and hand repairs both land here, and they
become **commit 2** (`deps: adapt code to <package> <version>`, one bullet per
API), the only commit the maintainer has to read. Skip commit 2 entirely when
no code changes were needed.

**Where symbols are auto-imported, "find all usages" means a text search, not
an import graph.** Framework auto-imports, test-runner globals and compiler
macros have no import statement, so "no import found, so it is unused" is a
conclusion that feels certain and is wrong. Use `rg '\bmySymbol\b' <source
dirs>` or LSP references, and assume the symbol is used until ripgrep says
otherwise.

## 6. Verify, and the repair loop

Run the project's own full gate — the command a project skill or `CLAUDE.md`
names (`pnpm test && pnpm typecheck && pnpm lint`, `make check`, a single
project-specific task).
Run it as the project states it, bare, without narrowing it to the subset you
think is affected. If no such command is documented, assemble one from the
`package.json` scripts and say in the PR body which one you used.

On failure in a **batch** run:

1. Identify the offending package (the failure text usually names it; otherwise
   bisect by dropping the most suspicious bump).
2. Drop it (revert its `package.json` entry and re-run the install so the
   lockfile matches) and re-verify.
3. Bounds: **at most 2 drops and 3 verify cycles per problem.** Hitting either
   bound means stop and hand over: open the PR with the failure quoted at the
   top of the body. Do not keep trying.

A **migration** run has nothing to bisect: on failure, hand over directly with
the failure at the top.

**Type errors naming two copies of one package** are not a bad bump to bisect.
A failure reading "Type `X` from `.pnpm/pkg@1.…` is missing the following
properties from `X` from `.pnpm/pkg@2.…`" means a duplicated package resolved
to the wrong copy, which install order decides rather than the lockfile — so a
regen can cause it with nothing in the diff to explain why.

Look the package up in `duplicateMajors.duplicates` and follow the dependency
chain that declares it to learn which major is correct; the declared range
answers it outright, so do not reconstruct old installs to prove when it broke.
The fix is to declare the package in the consuming workspace at that major, so
that copy is the one resolved locally. Pin it exactly — the declaration exists
to name one specific copy, so a range that can drift off it defeats the
purpose — and document it as an `# ISSUE:` / `# DELETE-WHEN:` pair where §1
reads conditions from.

When a hand-resolved lockfile conflict is what preceded the failure, re-run a
full install before believing any of it. A lockfile-only install leaves
`node_modules` and generated tsconfigs describing the old tree, and the
resulting errors point at packages that are already fine.

Report every dropped package as deferred in the PR body: a problem package
must be visible, never silently skipped.

If commit 1 already exists when a drop happens, rewrite it to include the
revert only while it is unpushed. Once pushed, let the drop be its own commit
and say so in the body.

**Forbidden, without exception:**

- Never edit, skip, or weaken a test to make verification pass.
- Never widen a version range to dodge a peer conflict.
- Never touch files unrelated to the upgrade.
- Never remove or edit a workspace workaround, override, catalog entry or pin.
- Never hand-edit a generated audit-exclusion list (only the audit tool's own
  `--fix` writes those).
- Never `git push --force` this branch or amend a pushed commit.

## 7. Run note

Write a short note where the profile says notes go — `.aiwork/{TODAY}_dep-update/notes.md`
under the aiwork protocol, otherwise wherever that project keeps them —
committed as part of commit 1 (or on its own when the run stops early). Keep it
short: what the scan found, what was bumped, what was deferred and why,
DELETE-WHEN status, and the outcome. A run that did nothing still writes this
file, so that next time it is clear the run happened and found nothing, rather
than not happening at all.

## 8. Open the PR

```bash
git push -u origin claude/deps-$WEEK
gh pr create --label deps --title "deps: safe batch $WEEK" --body-file <file>
```

Title: `deps: safe batch {week}` or, for a migration, `deps: {package} {from}→{to}`.
Body in English, first line the verification result (✅ green, or ❌ HANDED
OVER with the failure quoted). Then these sections:

- **Bumps** — table: package, from, to, notes.
- **Majors in this batch** — per major: the breaking-change items, the search
  run for each, and the result.
- **Code changes** — one line per change, or "none — commit 2 absent".
- **Deferred** — dropped packages with the failure, and majors queued for a
  later run.
- **Reported, not touched** — pins, catalog aliases, override workarounds, with
  the newer version available.
- **Duplicate majors** — only the rows that matter: any package this run
  touched that appears in `duplicateMajors`, plus every row with a `pathsAt`
  that disagrees with `hoistedAtRoot`. Those are latent typecheck breaks
  whether or not this run tripped one. Never paste the full list.
- **DELETE-WHEN status** — each condition: satisfied / not satisfied, and why.
- **Not verified** — what this run could NOT check (runtime behaviour against
  live services, visual rendering, anything behind a feature flag).

The **Not verified** list is mandatory and must be honest. A PR that claims
everything is fine is a failure of this skill, not a good run. If the list is
hard to write, the batch was probably too large.

Finish by telling the user the PR URL and the one thing worth their attention.
