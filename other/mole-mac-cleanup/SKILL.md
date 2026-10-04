---
name: mole-mac-cleanup
description: Safely operate the installed Mole CLI (`mo`) on macOS using machine-readable status, analysis, history, and dry-run surfaces. Use when Codex is asked to inspect Mac disk, CPU, memory, or network usage; find large files; preview or perform cleanup; remove apps, installers, or project artifacts; diagnose Mole results; or check and upgrade Mole.
---

# Mole Mac Cleanup

Use the official Mole agent skill at `tw93/Mole/.claude/skills/mole/SKILL.md` as the command-semantics baseline. The repo-only `runtime.yaml` pins the audited upstream version. For version-sensitive behavior, confirm the installed version and read `mo <command> --help`; trust the actual dry-run over stale assumptions.

## Safety Contract

1. Always preview before deletion. Run the matching `--dry-run`, inspect its candidates, summarize the impact, and obtain explicit user confirmation in the current turn before running the destructive command.
2. Treat `clean`, `uninstall`, `purge`, `installer`, and `optimize` as destructive. Treat `update`, `remove`, and whitelist changes as state-changing and require an explicit request.
3. Never parse or act from a TUI frame. Use JSON surfaces where available. If a selector opens, do not infer a selection or press bulk-select keys on the user's behalf.
4. Never invent flags. Run `mo <command> --help` when the documented surface is insufficient.
5. Preserve Mole's safety layer. Use `mo clean --whitelist` for protected paths; never replace Mole with raw `rm`, hand-written recursive deletion, or broad globs.
6. Do not request `sudo`, close applications, remove login items or dotfiles, prune Docker/OrbStack, or delete virtualenvs and project artifacts unless the user separately confirms that exact scope.
7. Bound long scans and watches. Send progress updates, stop low-value scans that remain silent, and never leave `mo status --watch` running in the background.

## Establish the Runtime

Confirm the binary, version, and real package manager:

```bash
command -v mo
mo --version
brew list --versions mole
brew info mole --json=v2
```

Do not trust the `Install:` line from `mo --version` alone; a Homebrew-managed build can report `Manual`. If `brew list --versions mole` succeeds, manage it with Homebrew.

## Choose the Surface

| User intent | Agent-facing command |
|---|---|
| Explain disk usage | `mo analyze --json` or `mo analyze --json <path>` |
| Preview safe cleanup | `mo clean --dry-run` |
| List installed apps with exact uninstall names | `mo uninstall --list` |
| Remove one app completely | `mo uninstall --list` to read the exact name, then `mo uninstall --dry-run <app>` |
| Preview bounded maintenance | `mo optimize --dry-run` |
| Preview old project artifacts | `mo purge --dry-run` |
| Preview downloaded installers | `mo installer --dry-run` |
| Audit prior cleanup | `mo history --json --limit 20` |
| Capture one health snapshot | `mo status --json` |
| Capture a short time series | `mo status --watch --interval 1s` |

Interactive `analyze`, terminal-attached `status`, app selectors, and installer selectors are human surfaces. Prefer the commands above. If a dry-run still opens a selector, stop after reporting the visible candidates and ask the user to make the selection.

## Machine-Readable Evidence

### Disk analysis

`mo analyze --json` returns one JSON object containing `path`, `overview`, and `entries[]`. Each entry includes `name`, `path`, `size`, `is_dir`, and `insight`; sizes are bytes. Scope expensive scans when possible, for example:

```bash
mo analyze --json "$HOME/Library"
```

### Cleanup candidates

`mo clean --dry-run` prints a summary and writes the candidate paths to:

```text
~/.config/mole/clean-list.txt
```

Read that file to review the paths this dry-run found. It is a preview snapshot, not an executable deletion plan: a later `mo clean` rescans and revalidates current candidates, so the two target sets can differ. Never promise the user that the real run will remove exactly this list. `purge --dry-run` and `installer --dry-run` report their candidates in the terminal and do not write this list.

### Cleanup history

`mo history --json --limit N` returns session summaries and the operation/deletion log paths. Use `actions.removed`, `trashed`, `skipped`, and `failed` to verify the outcome. When `failed` is nonzero, inspect only the matching session in the operations log and classify permission-protected or running-app paths separately from real cleanup failures.

### Installed apps

`mo uninstall --list` prints the app inventory as a JSON array when stdout is not a TTY. Each entry has `name`, `bundle_id`, `source`, `uninstall_name`, `path`, and `size`. Read `uninstall_name` for the exact argument `mo uninstall` accepts, so the app selector TUI never has to be opened.

```bash
mo uninstall --list
```

### System status

Use `mo status --json` for a single CPU, memory, disk, and network snapshot. `mo status --watch --interval 1s` emits NDJSON; collect only the number of samples needed, then terminate it.

## Command Notes

- `mo clean` permanently removes caches and also sweeps evidence-backed leftovers from already-uninstalled apps. It does not uninstall an installed app.
- `mo uninstall` moves the app and matched leftovers to Trash by default, so they remain recoverable until Trash is emptied.
- `mo clean --external <path>` cleans macOS metadata from an external volume; resolve and show the exact mounted path before asking for confirmation.
- In current upstream Mole, `mo purge` targets both local build output (`target/`, `build/`, `dist/`, `.next/`) and dependency directories that require a network to restore (`node_modules/`, `Pods/`, `venv/`, `vendor/`). A purge is therefore not always recoverable offline: classify the dry-run candidates by recovery type and show that distinction before requesting confirmation. Add `--include-empty` to surface zero-size candidates. A non-interactive real run requires an explicit `--yes`; dry-run does not. Use `--yes` only after the user has authorized removal in the current turn. Artifacts with authored content stay protected, and an inconclusive content probe keeps the candidate and reports an incomplete run. `mo purge --paths` opens an interactive editor for the scan directories; it is a human surface, so report that the user has to edit it themselves instead of entering it.
- `mo optimize` refreshes caches and system services rather than only deleting files. Explain the planned effects before requesting approval.
- Use `--debug` only to diagnose a command that did nothing or failed; normal runs should stay concise.

## Upgrade Mole

If Homebrew manages Mole, prefer:

```bash
brew upgrade mole
```

Otherwise, upstream provides `mo update`. `mo update --nightly` installs unreleased `main`; never run it unless the user explicitly requests nightly. After any upgrade, verify the installed version and run a non-destructive smoke test:

```bash
mo --version
mo clean --dry-run
```

## Report and Verify

Before cleanup, report the command, potential bytes/items, largest categories, exact risky paths, protected/running-app skips, and the proposed real command. After an approved cleanup:

1. Compare free space before and after.
2. Read `mo history --json --limit 1`.
3. Explain nonzero `failed` and important `skipped` counts without escalating to `sudo` automatically.
4. Verify separately protected paths still exist when the dry-run surfaced dotfiles, login items, Docker data, dependency stores, virtualenvs, or active project state.

A dry-run provides no backup and no undo. Clean deletions are normally permanent, so the preview is the only point at which the user can veto; it is not a way to reverse anything afterwards, and it does not guarantee the real run will target the same set. If a user asks whether Mole removed a specific file, use the deletion log path returned by history and answer from the exact matching record.
