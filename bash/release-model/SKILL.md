---
name: release-model
description: 'Creates, upgrades, or audits RELEASING.md branching policy. Use when defining a release process, adding maintenance branches, or checking release-model drift.'
argument-hint: '[--upgrade | --audit] [--model trunk-only|release-branches] [--trunk NAME] [--yes]'
allowed-tools:
  - Read
  - Grep
  - Glob
  - Write
  - Edit
  - AskUserQuestion
  - Bash(git:*)
  - Bash(gh:*)
  - Bash(ls:*)
  - Bash(test:*)
  - Bash(cat:*)
  - Bash(diff:*)
  - Bash(mktemp:*)
  - Bash(cp:*)
  - 'Bash(${CLAUDE_PLUGIN_ROOT}/skills/release-model/scripts/*.sh:*)'
  - 'Bash(${CLAUDE_PLUGIN_ROOT}/skills/_shared/scripts/release-state.sh:*)'
  - 'Bash(${CLAUDE_PLUGIN_ROOT}/skills/_shared/scripts/release-state-update.sh:*)'
  - 'Bash(${CLAUDE_PLUGIN_ROOT}/skills/_shared/scripts/rules-pointer.sh:*)'
---

# Release Model

Create, upgrade, or audit a project's `RELEASING.md` — the single source of truth for its
trunk, maintenance branches, and release steps. Every other ycc skill that picks a base
branch, opens a PR, cuts a release, or cleans up branches reads it through `release-state.sh`.

**Operational context:** Render project-specific RELEASING.md with machine-readable state and CLAUDE.md/AGENTS.md pointers. Trunk-only tags every release from trunk; release-branches tags minors from trunk and patches from release/X.Y with backports. --upgrade moves to release-branches; --audit reports drift read-only.

The rules themselves (both models, where a change goes, backporting, the state-block
format) live in `${CLAUDE_PLUGIN_ROOT}/skills/_shared/references/branching-model.md`. Cite
its sections; do not restate them in output or in generated files beyond what the
template already contains.

**Hard limits:** this skill never commits, pushes, tags, creates branches, or creates
labels. It writes files in the working tree only after a dry-run preview, and prints the
commands a maintainer runs for everything else.

## Arguments

Parse `$ARGUMENTS`:

| Flag                                   | Meaning                                                                   |
| -------------------------------------- | ------------------------------------------------------------------------- |
| _(none)_                               | **create** when `RELEASING.md` is missing, **audit** when it exists       |
| `--upgrade`                            | Move an existing trunk-only model to release-branches                     |
| `--audit`                              | Read-only drift report with suggested fixes                               |
| `--model trunk-only\|release-branches` | Preselect the model (create only); skips the model question               |
| `--trunk NAME`                         | Preselect the trunk branch; skips the trunk question                      |
| `--yes`                                | Accept the proposal without questions and write after showing the preview |

`--upgrade` and `--audit` are mutually exclusive; reject both together. Reject a
`--model` value other than `trunk-only` or `release-branches`.

Script paths used below:

- `SIGNALS=${CLAUDE_PLUGIN_ROOT}/skills/release-model/scripts/collect-signals.sh`
- `STATE=${CLAUDE_PLUGIN_ROOT}/skills/_shared/scripts/release-state.sh`
- `TARGETS=${CLAUDE_PLUGIN_ROOT}/skills/release-model/scripts/pointer-targets.sh`
- `UPDATE=${CLAUDE_PLUGIN_ROOT}/skills/_shared/scripts/release-state-update.sh`
- `POINTER=${CLAUDE_PLUGIN_ROOT}/skills/_shared/scripts/rules-pointer.sh` — the single canonical `AGENTS.md`/`CLAUDE.md` pointer helper shared with `ycc:init`; `$TARGETS` delegates to it. Release-model only reads it: it never migrates a layout and never creates a missing rules file.
- `TEMPLATE=${CLAUDE_PLUGIN_ROOT}/skills/release-model/templates/RELEASING.md.tmpl`

**Questions:** class `confirm-publish` (model questions, write after preview); headless (no question tool or chat turn) and without `--yes`: print the proposal and preview, write nothing, and print `rerun with --yes`. See `${CLAUDE_PLUGIN_ROOT}/skills/_shared/references/question-policy.md`.

## Phase 0 — Preflight and mode

1. `git rev-parse --show-toplevel` must succeed; call the result `ROOT`. Otherwise STOP:
   "not a git repository".
2. Run `$STATE --repo "$ROOT" get` and branch on the result:

| Result                   | Flag        | Mode                                                                                |
| ------------------------ | ----------- | ----------------------------------------------------------------------------------- |
| exit 0, `present=0`      | none        | create                                                                              |
| exit 0, `present=0`      | `--audit`   | report "no RELEASING.md" and suggest `/ycc:release-model`; stop                     |
| exit 0, `present=0`      | `--upgrade` | STOP: nothing to upgrade; suggest `/ycc:release-model --model release-branches`     |
| exit 0, `present=1`      | none        | audit (say so: "RELEASING.md exists — auditing; use --upgrade to change the model") |
| exit 0, `present=1`      | `--upgrade` | upgrade, unless `model=release-branches` already — then report that and audit       |
| exit 0, `present=1`      | `--audit`   | audit                                                                               |
| exit 2 (malformed state) | any         | show the stderr parse error verbatim, then audit (the error is the first finding)   |

A dirty working tree does not block: this skill only touches `RELEASING.md`, `CLAUDE.md`,
`AGENTS.md`, `.github/copilot-instructions.md`, and `.github/labels.md`. If any of those
has uncommitted changes, warn before writing to it.

## Phase 1 — Signals

Run `$SIGNALS --repo "$ROOT"` and keep every `key=value` line (keys and meanings are in
the script header). Signals never fail the skill: `gh_releases=unknown` means `gh` is
missing, unauthenticated, or offline — list it under "unknown signals" in the proposal.

Also resolve, without network writes:

- **Project name:** the `origin` remote's repository name
  (`basename -s .git "$(git remote get-url origin)"`), else the `name` field of the first
  version file, else the basename of `ROOT`.
- **Tracker candidates** — read `references/signals-and-proposal.md#tracker-detection` when listing tracker candidates.

## Phase 2 — Proposal and questions

Present one compact proposal: the suggested model with `suggested_reason`, the trunk
(`--trunk`, else `default_branch`), the support window (`latest-minor` by default,
release-branches only), the tracker, and the supporting signals (tags, release branches,
publish workflow, version files, changelog, long-lived branches, sync merges). Flag
`long_lived_branches` and `sync_merges_recent > 0` as habits the new model forbids
(`branching-model.md#rules`, rules 2 and 3) — they are advisory, not blockers.

Then ask **at most three questions** with `AskUserQuestion`, skipping any whose answer
is already fixed by a flag:

1. **Model** — suggested model first, marked "(Recommended)".
2. **Trunk** — `default_branch` first; offer `main`/`master` if they exist and differ.
3. **Support window** (release-branches only) — `latest-minor` (Recommended) or
   `latest-two-minors`.

Ask about the tracker only when detection is ambiguous, and only if a question slot is
left (under release-branches with an ambiguous tracker, default the support window to
`latest-minor`, say so in the proposal, and ask about the tracker instead).

`--yes` skips every question and accepts the proposal; an ambiguous tracker becomes
`none`, noted in the summary. Read `references/signals-and-proposal.md` when
assembling the Phase 2 proposal — it holds the details and the reason-to-model mapping.

## Phase 3 — Render RELEASING.md (create)

Build the file in a scratch directory (`SCRATCH=$(mktemp -d)`), never in `ROOT` yet.

1. Read `$TEMPLATE` as UTF-8 with optional leading BOM stripped (`utf-8-sig` semantics), and `${CLAUDE_PLUGIN_ROOT}/skills/release-model/references/template-placeholders.md`.
2. **Conditional blocks:** for `release-branches` keep `{{#IF_RELEASE_BRANCHES}}` blocks
   and drop `{{#IF_TRUNK_ONLY}}` blocks; for `trunk-only` the reverse. Delete the marker
   lines of kept blocks and the whole of dropped blocks (markers included), then collapse
   any run of blank lines this leaves into a single blank line.
3. **State block:** run

   ```bash
   $UPDATE --print-block --model <M> --trunk <B> [--support <S>] [--tracker <T> --tracker-ref <R>]
   ```

   Pass `--support` only under release-branches, and `--tracker-ref` only with a non-empty
   ref. The output is the block, a blank line, then a table. Take only the block: from
   the first output line up to and including the first line that is exactly `-->`. Copy
   it verbatim (never retype the marker strings) and replace the `{{STATE_BLOCK}}` line
   with it. Leave the template's empty table markers alone.

4. **Placeholders:** fill the rest from signals per `template-placeholders.md`
   (`{{PROJECT_NAME}}`, `{{TRUNK}}`, `{{TAG_PATTERN}}` from `tag_pattern` with `none` →
   `vX.Y.Z`, `{{VERSION_FILES}}` as backticked comma list, `{{CHANGELOG_FILE}}`,
   `{{PUBLISH_STEP}}`, `{{TRACKER_SECTION}}`). When the project already has its own
   release tooling — a release script or npm/make target, a documented release command in
   `CLAUDE.md`/`CONTRIBUTING.md`, a release-notes directory — name it in `{{PUBLISH_STEP}}`
   and adapt the numbered Releasing steps so they match what maintainers actually do.
   Keep the section structure.
5. Write the result to `$SCRATCH/RELEASING.md`, then run
   `$UPDATE --repo "$SCRATCH" --render` to fill the Current state table.
6. Verify: `grep -n '{{' "$SCRATCH/RELEASING.md"` prints nothing, and
   `$STATE --repo "$SCRATCH" get` exits 0 with the chosen `model` and `trunk`.
7. **Existing release branches (release-branches only):** for each branch in
   `release_branches`, oldest first, run
   `$UPDATE --repo "$SCRATCH" --add-maintenance <branch>`; the support window moves older
   ones to `frozen` automatically. Branch names that are not `release/X.Y` are skipped
   and reported.

## Phase 4 — Pointer sections

For each `POINTER_TARGET` below (every line `$TARGETS --repo "$ROOT"` prints: existing
`CLAUDE.md`, `AGENTS.md`, and `.github/copilot-instructions.md` — never create one), read
the pointer section in `references/pointer-and-labels.md#pointer-section` and add it unless
a line matching `^## Branching & releases` is already present — then leave the file untouched
and report "already present". Append it at the end of the file, separated by one blank line.
When neither `CLAUDE.md` nor `AGENTS.md` exists, report that and suggest `/ycc:init`.

## Phase 5 — Labels doc (release-branches only)

If `.github/labels.md` exists and does not mention `backport:`, read
`references/pointer-and-labels.md#labels-doc` and add the `backport:X.Y`
family exactly as it describes. Otherwise
skip. Never create or edit labels on the forge.

## Phase 6 — Preview, then write

Show a dry-run preview of every change: the full new `RELEASING.md` (or `diff -u` against
the existing one) and a `diff -u` for each pointer or labels edit. Then:

- Without `--yes`: ask once, "Write these N files?" — stop on no.
- With `--yes`: write after printing the preview.

Write with `cp "$SCRATCH/RELEASING.md" "$ROOT/RELEASING.md"` and Edit/Write for the
others. Afterwards run `$STATE --repo "$ROOT" get` (must exit 0) and
`$STATE --repo "$ROOT" check`; `check` findings about branches missing on origin are
expected when the trunk has not been pushed yet — report them, do not fix them.

## Phase 7 — Summary

Report: mode, model, trunk, support window, tracker, files written, `check` result, any
unknown signals, and the advisory findings (long-lived branches, sync merges). Next steps:

- Ship the change as a normal PR, e.g. `/ycc:git-workflow` (suggested commit:
  `docs: add RELEASING.md`). Nothing has been committed.
- Under release-branches with no maintenance branch yet, print the cut-over commands for
  the latest tag's line (`X.Y` from `latest_tag`), for the maintainer to run:

  ```bash
  git push origin <latest_tag>^{commit}:refs/heads/release/X.Y
  gh label create "backport:X.Y" --description "Cherry-pick to release/X.Y"
  <resolved $UPDATE path> --add-maintenance release/X.Y   # then commit RELEASING.md
  ```

  Print `$UPDATE` as its resolved absolute path; maintainers cannot expand the plugin
  root variable.

  With no tags yet, say that `release/X.Y` is created when the first minor is tagged
  (`/ycc:releaser` does this).

## Mode: upgrade (trunk-only → release-branches)

Follow `references/upgrade-and-audit.md#upgrade`. In short:

1. Change the model on a scratch copy with `$UPDATE --set-model release-branches`
   (block and table only; `support`, `tracker`, `tracker_ref` are kept). No questions.
2. Build the release-branches sections with the Phase 3 renderer in `$SCRATCH`, using the
   current state's trunk, tracker, and the signals.
3. Merge them into the existing file section by section, preserving human prose exactly
   as the reference describes. Anything that cannot be merged safely is left alone and
   listed as "update by hand" with the rendered text.
4. Labels doc (Phase 5), preview (Phase 6), then write — the state change through
   `$UPDATE --repo "$ROOT" --set-model release-branches`, never by hand.
5. Summary with the cut-over commands from Phase 7.

## Mode: audit (read-only)

Follow `references/upgrade-and-audit.md#audit`. Run `$STATE --repo "$ROOT" check`, the
signals, and (when `gh` is authenticated) `gh label list`. Report each finding with its
severity and the exact fix command. Checks cover: state parse errors, table drift,
branches missing on origin, a maintenance branch with no tag on its line, a minor tag
newer than the newest maintenance branch, `release/*` branches the state does not list,
a trunk-only model that has already patched an older line, long-lived branches, recent
sync merges on the trunk, missing `backport:X.Y` labels, and missing pointer sections.
Change nothing.

## Important Notes

- The state block and table change only through `release-state-update.sh`; the skill
  never edits them by hand. Prose after the table end marker is human-owned.
- A malformed block is never "fixed" by regenerating the file; audit reports the parse
  error and the maintainer decides.
- This skill does not choose releases or versions; `/ycc:releaser` cuts releases and
  `/ycc:backport` moves fixes to maintenance branches, both reading the state written here.
