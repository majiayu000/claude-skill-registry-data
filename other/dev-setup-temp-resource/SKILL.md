---
name: dev-setup-temp-resource
description: >-
  Set up and use the committed `_temp-resource/<issue>-<topic>/` convention for handing scratch
  resources (prototypes, design references, fixtures, sample data) from one Claude Code session to a
  LATER session through git — not Dropbox/cclogs. Use when: (1) setting up `_temp-resource/` in a
  repo, (2) a planning or dev session must delegate files a later session will need — especially
  `/big-plan` → `/x-wt-teams`, or any handoff to Claude Code web where Dropbox/cclogs is
  unavailable, (3) deciding where to put prototype output (e.g. from `/protodev`) that
  you've decided a downstream session should reuse, (4) reading resources a prior session left under
  `_temp-resource/`. Keywords: _temp-resource, temp resource, delegate resources, share prototype
  across sessions, web Claude Code handoff, "use this PR as base".
---

# Dev Setup: Temp Resource

A repo-committed handoff channel for scratch resources that one session produces and a **later**
session consumes. Git is the channel — so it works where Dropbox/cclogs does not (most importantly
**Claude Code web**, which has no Dropbox).

## The convention

- **Location:** `_temp-resource/` at the repo root, **committed** (NOT gitignored). Being in git is the
  whole point — the resources ride the branch/PR to whatever machine or web session picks the work up.
- **Per topic:** `_temp-resource/<issue-number>-<topic-slug>/`, e.g. `_temp-resource/4444-tweak-header/`.
  The number is the GitHub issue — the **epic** for `/big-plan`, the single issue for `/x-as-pr`.
- **Temporary:** delete the topic subdir when the delegated work merges, so it never reaches the default
  branch. Harmless if left (tooling ignores the dir), but prefer clean.

## When to use it — and when not

Use it **only when delegating to a later session** AND the resource is not already in the repo and is
too big/binary to express inline in the issue (a prototype, a design mockup + screenshots, test
fixtures, sample data).

Do **not** reflexively store everything. `/protodev` output is often discarded or never
acted on — keep that in cclogs. Promote a copy into `_temp-resource/` only once you've decided a
downstream session concretely needs it. In-session work needs none of this; just use the file directly.

## One-time repo setup

A stray prototype (`.ts`/`.tsx`/`.md`/`.html`) under `_temp-resource/` must not trip CI's
**format / lint / test** gates. Most repo tooling is path-scoped (e.g. `pnpm --filter ...`) and never
sees a root dir — but the broad scanners (markdown formatters, repo-wide linters, root test configs)
will, so they need an explicit exclude. Run the helper:

```bash
bash "$HOME/.claude/skills/dev-setup-temp-resource/scripts/ensure-temp-resource.sh"
```

It creates `_temp-resource/` + a `README.md`, verifies the dir is not gitignored, and **auto-patches**
the configs whose shape is known and safe to edit:

- file-based ignore lists — `.prettierignore` / `.eslintignore` / `.stylelintignore`.
- **format** — `.mdx-formatter.json` → adds `_temp-resource/**` to its `exclude` array.
- **lint** — `.design-token-lint.json` → adds `**/_temp-resource/**` to its `ignore` array.

Then it **reports** the remaining **lint / test / typecheck** configs for you to finish by hand (their
shapes vary too much to patch blindly):

- **lint** — `eslint.config.*` (flat) → `"_temp-resource/**"` in an `ignores` entry; `.eslintrc*` →
  `ignorePatterns`; `biome.json` → `files.ignore`.
- **test** — `vitest.config.*` / `vite.config.*` (if it defines `test`) → `"_temp-resource/**"` in
  `test.exclude`; `jest.config.*` → `testPathIgnorePatterns`; `playwright.config.*` is usually
  `testDir`-scoped (safe — just confirm `testDir` isn't the repo root).
- **typecheck** — `tsconfig*.json` → `"_temp-resource"` in `exclude`, but only if its `include` globs
  the repo root (per-package tsconfigs that scope to their own `src` need nothing).

> **Edit the tool's own config array — never add a CLI `--ignore`/`--exclude` flag to the npm script.**
> For tools that auto-load a config (mdx-formatter's `.mdx-formatter.json`, etc.), a CLI flag *replaces*
> the config's list instead of extending it, silently re-exposing everything else the config was
> excluding (e.g. generated docs). The helper edits the config array for exactly this reason.

Commit this setup once (its own small PR, or fold it into the first delegating base branch). It is
permanent repo plumbing; the per-topic subdirs come and go on feature branches.

## Store a resource (the delegating session)

1. Pick the issue number + a short topic slug.
2. `mkdir -p _temp-resource/<issue>-<slug>/` and put the files there.
3. In the issue body, reference them by this in-repo path — never a `$DROPBOX_*`/`$HOME/cclogs`/absolute
   path (those don't exist on another machine or on web). A compact inline summary (e.g. ASCII of a
   layout) alongside the path makes the issue self-contained even before the file is opened.

## The base-branch delegation protocol — `/big-plan` → `/x-wt-teams`

By default `/x-wt-teams` creates the base branch and `/big-plan` creates issues only. When resources
must be delegated, **`/big-plan` prepares the base branch instead**, and `/x-wt-teams` reuses it:

1. **`/big-plan`** (after the epic + sub-issues exist, so the epic number is known):
- Create `base/<impl-title-slug>` from the parent branch.
- Commit the resources under `_temp-resource/<epic#>-<slug>/`; push; open the **base PR**
     (`base/<slug>` → parent).
- Add to the **epic body**: a "**Use this PR as base**" note naming the base branch + base PR and the
     `_temp-resource/<epic#>-<slug>/` path. This is the cross-session message.
2. **`/x-wt-teams`**: when the epic says "use this PR as base", **reuse that existing base branch** —
   do NOT create a new one. Topic branches fork from it, so every child inherits the resources, and each
   sub-issue can point at `_temp-resource/<epic#>-<slug>/` in the working tree.

For Claude Code web this is the only reliable handoff: the PR + committed dir ARE the shared state.

## Consume (the later session / child agents)

The resources are already on the branch — read `_temp-resource/<issue>-<topic>/` straight from the
working tree. The issue body points there. No download step, no Dropbox.

## Cleanup

When the delegated work merges, remove `_temp-resource/<issue>-<topic>/` so it doesn't land on the
default branch — fold this into the consuming workflow's cleanup/confirm step (or the docs step that
migrates anything durable into real docs). Leaving it is harmless but untidy.
