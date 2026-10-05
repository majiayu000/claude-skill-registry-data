---
name: agent-upgrade
description: Upgrades an existing Claude Agent project to the current config schema — migrates information from old locations to new ones, confirms every move with the user, and leaves a backup. Use when a project was initialized on an older version of the framework and needs to pick up schema changes (e.g. v1 inline per-repo testing/build → v2 per-repo agent-build.yaml + mono-repo support + per-iOS mac_build).
---

# Agent Upgrade Skill

You migrate an existing Claude Agent project from an older config schema to
the current one. You are **interactive and non-destructive by default**: you
show the user every change you are about to make before writing a byte,
back up the old files, and stop at the first ambiguity.

This skill is versioned. Each schema bump adds a new migration block below;
older blocks continue to work so chained upgrades (v1 → v2 → v3) stay in
this one skill.

---

## Base Rules

**Environment.** You are running in Claude Code directly in the project
root. Your working directory is the root of the project being upgraded.

**Terminal commands:** Single uninterrupted line, no backslash continuations.

**Hard rules (no exceptions):**
- Do not delete or overwrite any file before:
  1. Showing the user the full migration ledger, and
  2. Copying the file into `.workflow/upgrade-backup-<timestamp>/` with its
     original relative path preserved.
- Do not guess config values the user cared about. If a conflict surfaces
  (e.g. root `agent.yaml` says `dotnet test` but the per-repo `agent.yaml`
  says `dotnet test --no-build`), pause and ask the user to pick.
- Idempotent. If the project is already on the current schema, print the
  detected version and exit without writing anything.
- If the user stops mid-upgrade, the backup is enough to restore state —
  never delete the backup yourself.

---

## Step 1: Detect Schema Version

Read the root `agent.yaml`. Classify into one of:

- **v3 (current)** — schema is on v2 OR newer (multi-repo or single-repo)
  AND `workflow.backend` key is present (set to either `markdown` or
  `github_project`).
- **v2** — `repos:` entries each have a `build:` pointer
  (`build: <path>/agent-build.yaml`) and **no** inline `testing:` or
  `build:` blocks nested under the repo entry. A root-level `mac_build:`
  block is absent or commented. **`workflow.backend` key is absent.**
- **v1 (pre-refactor)** — `repos:` entries inline `testing:` and `build:`
  blocks, and/or a root-level `mac_build:` block is present. Each
  sub-repo directory likely contains a full `agent.yaml`. (`workflow.backend`
  key absent.)
- **single-repo (no version detection needed)** — missing `repos:` and
  `project.type: multi-repo`. Single-repo projects only need v3 detection
  (presence of `workflow.backend`). If absent, jump to Step 9 (v2 → v3).

Migration order:
- v1 → first run Steps 2–8 to get to v2, then continue to Step 9 to land at v3.
- v2 → skip Steps 2–8, run Step 9 only.
- v3 → state `Project is already on schema v3 — no upgrade needed.` and stop.

If **v3**: stop.
If **v2**: jump directly to Step 9.
If **v1**: proceed to Step 2.

---

## Step 2: Scan and Build the Migration Ledger

Walk every repo entry in the root `agent.yaml`. For each:

1. Record the inline `testing.*` and `build.*` values from the root.
2. If `<repo.path>/agent.yaml` exists, read it. Extract:
   - `testing.*` / `build.*` — compare against the root's inline values.
     Equal values are unambiguous. Divergent values are a **conflict**.
   - `code_standards` — this is unique to the per-repo file; it has no
     root counterpart.
   - `design` — if non-empty, record it; it will move to the leaf
     `agent-build.yaml` if the stack is a UI stack.
3. If the root `agent.yaml` has a `mac_build:` block and this repo's
   `stack` is `swift` or `ios`, mark it as an **iOS mac_build candidate**
   — the block will move to this repo's leaf file.
4. **Fastlane check (stack `ios` or `android`).** Look for
   `<repo.path>/fastlane/Fastfile` or `<repo.path>/Fastfile`. If found,
   grep for `lane :<name>` to list lanes. If the existing v1
   `testing.command` / `build.command` for this repo is empty or looks
   like a generic stack default (`xcodebuild ...`, `./gradlew test`,
   `./gradlew assembleDebug`) **and** fastlane offers a better-fitting
   lane (`fastlane test`, `fastlane build`, `fastlane beta`, etc.),
   record this as a **fastlane suggestion** row in the ledger — do NOT
   auto-apply; the user confirms in Step 3.

Also detect **mono-repo candidates**: any repo whose `<repo.path>`
directory contains at least two recognizable sub-project layouts (e.g.
`ios/` + `android/` + a Rust-toolchain directory). Prompt:

```
`<repo.path>/` contains what look like multiple independently-built
sub-projects: <list>. Expand this into a mono-repo parent with each
as a separate sub-project? [Y/n]
```

If yes, for each sub-project ask its stack (run stack detection from the
`agent-init` skill's detection table on that subdir) and — for iOS — the
Mac SSH host/workspace, defaulting to the root `mac_build:` block if one
was present.

Build a single **Migration Ledger** in memory:

```
Repo: <id> (<path>)
  Stack: <stack>
  Shape: leaf | mono-repo
  Destination: <path>/agent-build.yaml
  Source → Destination:
    root agent.yaml repos[<id>].testing.command   → <dest>.testing.command   ("<value>")
    root agent.yaml repos[<id>].build.command     → <dest>.build.command     ("<value>")
    <path>/agent.yaml code_standards              → <dest>.code_standards    (N lines)
    root agent.yaml mac_build.host                → <dest>.mac_build.host    ("<value>")   [iOS only]
    root agent.yaml mac_build.workspace           → <dest>.mac_build.workspace ("<value>") [iOS only]
  Conflicts:
    <field> — root says "<a>", per-repo agent.yaml says "<b>" — <unresolved>
  Fastlane suggestions: [iOS/Android only, if Fastfile found]
    testing.command: current "<value>" → suggest "fastlane test"       [lane :test found]
    build.command:   current "<value>" → suggest "fastlane build"      [lane :build found]
  Sub-projects: [only if mono-repo]
    <id> (<path>) → <path>/agent-build.yaml (stack: <stack>, mac_build: <host|—>)
```

---

## Step 3: Confirm with the User

Print the full ledger. For every **Conflict** row, ask which value to
keep, offering both plus "Other" (free-form input). Do not proceed until
every conflict is resolved.

For every **Fastlane suggestion** row, ask "Adopt `fastlane <name>` for
`<field>`? [Y/n]". On yes, the new value goes into the leaf
`agent-build.yaml`; on no, keep the current value.

Then show the summary:

```
About to:
- Back up N files to .workflow/upgrade-backup-<timestamp>/
- Write M new files (agent-build.yaml per repo/sub-project)
- Rewrite the root agent.yaml (repos: block + remove root mac_build:)
- Delete K per-repo agent.yaml files after backup

Proceed? [Y/n]
```

Only continue on an explicit yes.

---

## Step 4: Write the Backup

Create `.workflow/upgrade-backup-<YYYY-MM-DDTHH-MM-SS>/`. For every file
the upgrade will modify or delete:

1. Copy it into the backup under its original relative path (preserve
   directory structure — e.g.
   `.workflow/upgrade-backup-.../Backend/middleware/agent.yaml`).
2. Also copy the root `agent.yaml` in full.

Write a manifest `backup/MANIFEST.md` listing every backed-up file with
its size and sha256.

---

## Step 5: Write New Files

1. **Per-repo leaf `agent-build.yaml`** — for each leaf repo, render using
   `templates/<stack>/agent-build.yaml.tmpl` where available, filling in
   `stack`, `testing`, `build`, `code_standards`, and (iOS only)
   `mac_build`. If the stack has no matching template (e.g. stack was
   `base`), emit the minimal leaf shape from
   `templates/ios/agent-build.yaml.tmpl` adapted to that stack.
2. **Mono-repo parent `agent-build.yaml`** — for each repo the user
   elected to expand, render using
   `templates/mono-repo/agent-build.yaml.tmpl`. Populate `projects:`
   with each sub-project's `id`, `stack`, `path`, and `build` pointer.
3. **Sub-project leaf `agent-build.yaml`** — one per sub-project inside a
   mono-repo, same rules as (1).
4. **New root `agent.yaml`** — replace the `repos:` block with the
   pointer shape (`id`, `path`, `stack`, `build`). Remove the root-level
   `mac_build:` block entirely (those values now live per iOS leaf).
   Preserve everything else verbatim (`project`, `git`, `workflow`,
   `agents`, `github`, etc.).

Write to disk in this order: sub-project leaves → mono-repo parents →
top-level leaves → new root `agent.yaml`. If any write fails, stop and
surface the partial state; do not delete anything in Step 6.

---

## Step 6: Remove Old Files

Only after Step 5 succeeds end-to-end:

1. Delete each per-repo `<repo.path>/agent.yaml` (they are in the backup).
2. Leave `.workflow/` untouched except for the new backup directory.

Print each deletion as it happens.

---

## Step 7: Validate Task Files

Scan `.workflow/tasks/` for every task file. For each, read its `Repo:`
field and attempt to resolve it against the new root `agent.yaml`:

- Leaf repo id → must exist in `repos:`.
- Dotted `<parent>.<sub>` → `<parent>` must exist as a mono-repo, and
  `<sub>` must appear in the parent's `agent-build.yaml` `projects:` list.
- Legacy relative-path values (e.g. `Repo: Backend/mobile_api`) — flag
  these. Suggest the correct id based on path match; do not rewrite the
  task file automatically.

Write any unresolved tasks to `.workflow/upgrade-backup-<timestamp>/TASKS-TO-FIX.md`
with one line per task and a suggested rewrite.

---

## Step 8: Report

Print:
- Backup location (`.workflow/upgrade-backup-<timestamp>/`)
- Files created (`+`), rewritten (`~`), deleted (`-`) — one per line
- Conflicts resolved (field, chosen value)
- Any unresolved task `Repo:` fields
- Recommended next commands:
  - `git status` — review the changes
  - `git diff <backup>/agent.yaml agent.yaml` — compare root before/after
  - `git add -A && git commit -m "chore: upgrade agent config to schema v2"`

Do **not** run `git add` or `git commit` yourself. Leave that to the user.

---

## Step 9: v2 → v3 (workflow backend choice)

A v3 project has `workflow.backend` set in `agent.yaml`. v2 projects don't
have the key — they implicitly used markdown. The v3 migration makes the
choice explicit and optionally moves the project to a GitHub Project board.

1. **Backup `agent.yaml`** to
   `.workflow/upgrade-backup-<timestamp>/agent.yaml.v2` (re-use the
   timestamp from Step 4 if v1 → v2 ran in the same session, else create
   a fresh backup dir).

2. **Ask the user:**
   ```
   Which workflow backend?
     (a) markdown — keep using `.workflow/*.md` files (no behavioral change).
     (b) github_project — migrate to a GitHub Project board now via /agent-migrate.
   Choice [a/b]?
   ```

3. **On (a) — markdown:** Insert a single line under the `workflow:` block:
   ```
   backend: "markdown"
   ```
   That's the entire migration. Print:
   `Project is now on schema v3 (backend: markdown). No behavioral change.`
   Done.

4. **On (b) — github_project:** Do NOT modify `agent.yaml` here — the
   `agent-migrate` skill handles the agent.yaml update as part of its own
   Step 7. Hand off:
   ```
   Delegating to /agent-migrate.

   That skill will:
   - Provision the GitHub Project board (labels, columns, fields)
   - Migrate every BACKLOG/TODO/DONE item, plan, and task to the board
   - Update agent.yaml with workflow.backend: github_project
   - Run install-skills-local.sh to pin .claude/ to the current framework commit
   - Copy issue templates into .github/ISSUE_TEMPLATE/

   Press Enter to continue or Ctrl+C to abort.
   ```
   On Enter, invoke `/agent-migrate`. The migration is non-destructive —
   if the user aborts inside agent-migrate, the project stays on v2
   (backend key still absent) and they can re-run later.

5. **Either way**, also append `.workflow/temp/` to `.gitignore` if not
   already present (cheap, harmless on markdown backend, required for
   github_project). Show the diff and ask the user to commit.

---

## Future schema bumps

When a new schema version ships, add a new top-level section below
("## Step 10: v3 → v4") describing the detection criteria, ledger rows,
and write steps for that migration. Re-use Steps 3 (confirm), 4 (backup),
6 (delete), 7 (validate tasks), and 8 (report) with version-specific
overrides. Keep the v1 → v2 and v2 → v3 blocks working indefinitely —
projects upgrade on their own cadence.
