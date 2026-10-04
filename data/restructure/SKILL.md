---
name: restructure
description: >-
  Inspects a repo's entire folder structure and files, finds structural issues (misplaced files,
  orphaned/dead files and folders, naming-convention drift, duplicated or stale directories, layout that
  no longer matches documented architecture), and produces a concrete move/rename/merge plan for user
  approval via EnterPlanMode before executing anything. Use when asked to "clean up the project
  structure", "reorganize the codebase/folders", "audit the file layout", or similar structural requests
  -- distinct from `double-check` (code-logic/correctness health), `extract-modules` (splits code out of
  files rather than moving whole files) and `infra-audit`
  (architecture/reliability of running services), none of which moves where files actually live.
---

# Restructure

Finds where a repo's actual file/folder layout has drifted from its own documented conventions (or, absent
documentation, from the patterns it already implicitly follows), then proposes and (once approved)
executes the fix. This is a **structural** audit — it does not review code logic (that's `double-check`'s
job) or runtime architecture/reliability (that's `infra-audit`'s job). If a finding here turns out to be
about code correctness rather than file placement, hand it off instead of fixing it here.

## Target

Audits the repo containing this `.claude/skills/restructure/` folder — resolve its root by walking up from
this file's location to the nearest repo boundary (e.g. `git rev-parse --show-toplevel` run from this
file's directory), regardless of which directory the invoking session's shell/CWD happens to be in. If the
user explicitly names a different target in the same message, audit that instead; absent that, never ask
which project — resolve it and go straight to Phase 0.

## Discover this repo's own established patterns first

Any restructuring proposal must keep the repo converging on a recognized, named design/architecture
pattern in every area it touches — never leave an area following a bespoke, one-off arrangement that only
makes sense by reading this repo's own history, when an established pattern would describe it just as well
to anyone who's seen that pattern before. Before Phase 2, inventory which patterns *this specific repo*
already leans on — don't assume any from a past run or another project. Common ones to check for, by name,
so findings can cite the real pattern rather than a vague "this looks off":

- **Repository pattern** (data access isolated behind one layer; nothing else issues raw queries).
- **Facade / mixin composition** (many focused modules composed into one entry-point object callers use).
- **Layered architecture** (a strict direction of dependency — e.g. transport → business logic → data
  access → schema — where a layer reaching past its neighbor into a deeper one is a violation).
- **Pipeline pattern** (one canonical fetch/transform/save sequence every entry point funnels through,
  rather than each caller reimplementing its own version).
- **Feature-sliced / vertical-slice organization** (a directory per feature, plus a separate location for
  genuinely cross-feature primitives).
- **Container/presentational split** (a top-level piece owns routing/state wiring; a child owns fetch +
  loading/error/empty states; feature-local presentational pieces live under the feature's own directory).

Identify which of these (or a different, equally recognized pattern not listed here) this repo actually
uses, and where — grep for the real module/directory names, don't assume they match another project's. If
Phase 2 finds an area that doesn't clearly follow whichever pattern the rest of the repo established for
that concern, Phase 3's plan must name which pattern it's converging that area toward and why (citing the
real pattern by name and the real module in *this* repo that already exemplifies it), not just describe
the mechanical file move. Never invent a new in-house convention when an existing, named pattern — one
this repo already uses elsewhere — already fits.

## Non-negotiable constraints

- Check the repo root for a contributor-facing conventions doc (`CLAUDE.md`, `AGENTS.md`,
  `CONTRIBUTING.md`, README) and **read it fresh, every time this skill runs** — don't rely on memory of
  its documented intended structure, or of any "lessons learned" list it keeps (several such lists record
  past structural cleanups — e.g. a previously-removed duplicate directory — so this skill can check
  whether the same drift has recurred).
- **`git mv`, never `mv`/delete-and-recreate**, for anything already tracked in a git repo — preserves
  history and makes the diff a rename instead of a delete+add, which matters for later `git blame`/`log`
  use.
- **Check `git status` before touching anything.** If there are uncommitted changes in files this pass
  would move or edit, stop and ask the user to commit/stash first rather than folding unrelated changes
  into the restructuring diff.
- **Never move/rename anything without first finding every reference to it** (imports, doc links, config
  file paths, CI config, README links) and updating all of them in the same pass. A structural "fix" that
  breaks a reference is worse than the drift it fixed.
- **Exclude generated/vendored trees** (dependency directories, build output, cache directories, `.git/`)
  from both the inventory and any proposed changes — those aren't this repo's structure, they're tool
  output.
- If this repo's conventions doc documents safety rules for anything that happens to touch running
  services/data while verifying a move didn't break something, follow them — this skill is about file
  layout, not an excuse to relax those.

## Phase 0 — Scope

- **Named by the user** (a directory, "just the frontend", "just scripts/") — use that.
- **Unscoped ("clean up the structure", "audit the layout")** — default to the whole repo, since that's
  what this skill is for; say so before starting so a wrong assumption is cheap to correct.
- Check whether this repo already keeps dated audit/report files somewhere (grep for a reports/audits
  directory, or a convention its own conventions doc describes) and skim the most recent restructure-
  flavored one before starting — carry forward any open follow-ups instead of rediscovering them, and
  don't re-propose a move a past report already deliberately rejected (record the reason if so).

## Phase 1 — Inventory

1. Get the real, current tree, generated fresh (never assume a prior session's memory of it still holds):
   list all tracked/real files excluding dependency directories, build output, caches, and VCS metadata
   (or a read-only exploration agent for a large tree, asked to report paths grouped by top-level
   directory, not paste every line into context).
2. Read every structure-documenting file as the **intended** layout to diff actual layout against: the
   root conventions doc's architecture/overview section, the root README, and any `README.md`/similar doc
   under a subdirectory.
3. Note whatever organizational convention the repo documents for its main application layer(s) (routing
   structure, per-feature directories, shared-primitive locations) — this is the yardstick for "does this
   file live where the convention says it should."

## Phase 2 — Find structural issues

Delegate the search to a read-only exploration agent when the tree is large, so raw find/grep output
doesn't fill the main context — ask it to report `path — issue` lines, not full file contents. Look for:

1. **Misplaced files** — a component outside its feature's established directory, a module that's
   actually shared logic living inside a feature-specific location instead of a shared one, a script not
   under wherever this repo keeps scripts, a test outside wherever this repo keeps tests.
2. **Duplicated/drifted directories** — two copies of the same thing. If the conventions doc records a
   past cleanup of exactly this (a removed duplicate directory), check specifically whether it has quietly
   reappeared, and separately check for any *new* instance of the same pattern elsewhere.
3. **Orphaned files/folders** — nothing imports, links to, or otherwise references it. Grep before
   flagging (a CLI-only/demo-only entry point still counts as live); an empty leftover directory from a
   removed feature is an easy, safe case.
4. **Naming-convention inconsistency** — mixed casing/naming styles within the same layer where the rest
   of that layer is consistent (a stray file that doesn't match its siblings' established convention).
5. **Docs/structure drift** — a README describing a module/folder that no longer exists, or omitting one
   that does (a per-module doc listing should have an entry for every real top-level module).
6. **Nesting-depth inconsistency** — one feature flattened, an equivalently-complex one needlessly
   nested (or vice versa), with no reason for the difference.
7. **Dead weight at the file level** — a whole file/module with zero references anywhere (distinct from
   dead code *inside* a live file, which is a codebase-health skill's job, not this one's).
8. **Design-pattern violations** — code that breaks one of the patterns identified above (a layer reaching
   past its neighbor, a component both fetching data and rendering feature-specific presentation inline, a
   new entry point bypassing this repo's own established single-pipeline convention if it has one). Name
   the pattern being broken in the finding, not just "this looks off."

For every candidate finding, verify it against the live repo yourself (grep/read it) — don't trust a
background agent's report without spot-checking, and don't flag something whose only "issue" is being
unfamiliar rather than actually inconsistent with this repo's own documented conventions **or** one of the
patterns identified above.

## Phase 3 — Write the plan

This is a **planning-mode task** — a repo-wide set of moves is exactly the "affects existing structure,
multi-file" case top-level planning-mode guidance calls for:

1. Enter plan mode before making any change.
2. For every proposed move/rename/merge, resolve its full blast radius first: grep for every import,
   relative path, doc link, and config reference (deploy/build config paths, CI config) to the file/folder
   being moved. A move whose reference updates you haven't already enumerated isn't ready to include in
   the plan yet.
3. Structure the plan as: **what moves where and why, naming the pattern it converges toward or restores**
   (one line each, grouped by theme), **every reference that must be updated alongside each move**, and
   **verification steps** (typecheck, test suite, a smoke check of anything whose import path changed) —
   matching whatever level of detail this repo's own planning-doc conventions expect, if it documents any;
   otherwise a clear move-by-move breakdown with its verification steps is enough.
4. Skip anything where the "fix" is genuinely just a judgment call with no clear convention violation —
   flag it as an open question in the plan for the user to decide, don't silently pick a side.
5. Exit plan mode to get explicit approval before touching anything. Do not execute on your own
   initiative just because a structural issue is obviously true — the user may have context (in-flight
   work touching the same files, a deliberate exception) this pass can't see.

## Phase 4 — Execute (only after plan approval)

- `git mv` each move (or create/stage/remove for merges/deletions), in the order the plan lays out —
  earlier moves first if a later one depends on a path existing.
- Update every reference identified in Phase 3 in the same pass — a reference left pointing at the old
  path is a regression this skill introduced, not a pre-existing one.
- After all moves: run this repo's own typecheck and test-suite commands (discovered from its actual
  config, not assumed) for whatever layers were touched by a move, and check logs for import/resolution
  errors after a restart if an entrypoint's resolution could be affected.
- If something breaks, fix the reference (don't revert the whole move) unless the breakage reveals the
  move itself was wrong.

## Phase 5 — Report

Every run ends with:

1. **A written record.** If this repo already has an established convention for recording audit/
   verification passes, follow it exactly (same field names, same file-naming/dating pattern already in
   use, dated correctly). If no such convention exists, write a dated summary somewhere sensible (ask the
   user where, if it's not obvious) rather than inventing a new one silently. Write one even if the audit
   found nothing worth moving (a clean pass is still a record).
2. **The chat summary** — following whatever response format this repo/session otherwise expects for a
   change that touches files: every move listed explicitly as `old/path` → `new/path` pairs, plus the
   actual typecheck/test output that verified nothing broke.
