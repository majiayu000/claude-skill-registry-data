---
name: update-dev-tools
description: >-
  Autonomously update this Mac's dev toolchain (Python and Node via mise, global npm
  CLIs, bun, Homebrew formulae and casks), verify it, report what needs a password. Use
  for 'update my tools', 'mets à jour mes outils', 'upgrade everything'. NOT for
  uninstalling apps or repo dependencies.
disable-model-invocation: true
---

# Update dev tools — autonomous macOS toolchain updater

This skill brings the user's **local developer toolchain** up to date in one shot and
**reports back** — it's meant to be invoked whenever they want their tools refreshed,
and to do the whole job autonomously (the way it was done manually once: Python via
mise, doc libraries, Node via mise + global-CLI reinstall, bun, Homebrew, npm globals,
with full verification). The repetitive, error-prone work lives in a bundled script so
every run is consistent and encodes the lessons already learned.

**Assumed stack (this machine):** runtimes managed by **mise**, packages by
**Homebrew**, shell **zsh**, on macOS. The script detects each tool and skips any
section whose prerequisite is missing, so it degrades gracefully — but if `mise` or
`brew` is absent, say so and adapt rather than pretending it ran.

## How to run it

The work is one resilient, self-verifying, logged script. Default behavior =
**everything** (the full update we want each time). Run it and let it finish:

```bash
bash ~/.claude/skills/update-dev-tools/scripts/update-toolchain.sh
```

Because it can take several minutes (mise runtime installs + brew upgrades + pip/npm
reinstalls), prefer running it as a **background job** and read the log when it
completes, rather than blocking.

**Options** (defaults already match "do everything"):
- `--dry-run` — print the plan and change nothing. Good for a first look or an
  unfamiliar machine.
- `--python <stable|X.Y|skip>` (default `stable`) · `--node <lts|latest|X|skip>`
  (default `lts`).
- `--skip-brew` · `--skip-npm` · `--skip-bun` · `--skip-casks`.
- `--prune-old` — remove superseded mise runtime versions (OFF by default: a repo's
  `.tool-versions` may pin an older one; only prune when the user asks).
- `--log <path>` — where to write the full log (default: a timestamped temp file).

If the user names a subset ("just update brew", "only python"), pass the matching
`--skip-*` / `--python skip` / `--node skip` flags. Otherwise run the full default.

## What the script already handles (don't re-derive these)

It surveys first, then updates, then **verifies** (it doesn't just trust that commands
ran). Baked in:
- **mise self-update**, then **Python** to current stable and **Node** to LTS, each
  set as the mise global so the user's `python3` / `node` become the new versions.
- **Package preservation across a version bump** — pip packages and global npm CLIs
  live *per runtime version*, so a bump would silently drop them. The script snapshots
  the old version's top-level packages and **reinstalls them into the new one**, and
  always ensures the document libraries (`python-docx`, `openpyxl`, `python-pptx`,
  `pypdf`, `pdfplumber`, `pillow`, `markitdown`, `pandas`).
- **npm is left at the version bundled with Node** — self-updating npm under a version
  manager races and rolls back; the bundled npm is the supported pairing.
- **Homebrew** formulae upgrade; casks attempted one-by-one.
- **Verification**: confirms `python3`/`node`/`npm` resolve to the new versions, that
  every doc library imports, that `wrangler`'s native `workerd` binary executes (npm 11
  defers postinstall scripts, but the binary arrives via optionalDependencies), and
  that `brew missing` is empty (no broken dependents from any orphan removal).

## After it runs — read the log, handle the manual items, report

1. **Read the log** (path printed at the end; also the `REPORT` section). Relay the
   `Updated` / `Failed` lists to the user concisely (before → after versions).
2. **Act on `NEEDS YOUR ACTION`** — these are the things a non-interactive shell
   genuinely can't do:
   - **`.pkg` casks** (e.g. `dotnet-sdk`) need the user's Mac password. Give them the
     exact one-liner the report printed (`brew upgrade --cask <name>`); do **not** try
     to feed a password or wrap it in a way that hangs.
   - **Stale casks** (the app was deleted, so brew can't upgrade it) — offer the choice
     the report shows: `brew reinstall --cask <name>` to get it back updated, or
     `brew uninstall --cask <name>` to clear the dangling reference.
3. **Tell the user** that new terminals already see the new `python3`/`node`; in an
   already-open terminal they run `exec $SHELL`.
4. If `Failed` is non-empty or `brew missing` flagged something, **investigate the
   log** before declaring success — don't report a clean run on a red result.
<!-- runtime-slot:path-warning -->
5. **Relay any `WARNINGS`** (non-fatal — they don't fail the run). The key one flags
   that mise's runtimes aren't resolvable in a non-interactive shell, so **Claude Code
   hooks / GUI apps can hit `node: command not found`** after a Node bump. Pass on the
   remedy the report prints (add the shims dir to a global PATH), but **do not edit
   `~/.claude/settings.json` yourself** unless the user asks — the script deliberately
   only warns; see `references/gotchas.md`.
<!-- /runtime-slot:path-warning -->

## Adapting / the why

The non-obvious reasoning behind each step (and what to do when the machine differs —
no mise, Linux, a different shell, an npm self-update that fails, a node major-version
jump that could break a project) is in **`references/gotchas.md`**. Read it when a run
hits something the script flags as `Failed`, or before adapting the script to a
machine that isn't the mise+brew+zsh setup it assumes.
