---
name: macos-storage-triage
description: Audit and safely liberate macOS disk space by ranking storage candidates by physical size, regenerability, human value, and deletion risk. Use when the user asks to free disk space on macOS, audit storage, clean Xcode simulators, Homebrew/caches, app support data, Dropbox/Drive local data, or design a storage-cleanup plan.
---

# macOS Storage Triage

## Operating Principle

Free entropy before memory. Prefer regenerable caches, runtime artifacts, and tool-managed cleanup before touching human-created files, app profiles, synced folders, or system-managed storage.

## Required Posture

- Start read-only unless the user explicitly asks to clean a named target.
- Measure physical allocation with `du`, not apparent size from `ls`; sparse files can lie.
- Classify every candidate by `value_class`, `risk_class`, `recoverability`, and `expected_gain`.
- Use native managers first: `brew`, `xcrun simctl`, app cleanup flows, package-manager cache commands.
- Never manually delete VM swap, Preboot, Recovery, app profiles, Dropbox/Drive files, or `_nsurlsessiond` MobileAsset files.
- For destructive actions, show exact paths/commands and require explicit confirmation.
- After cleanup, remeasure `df -h /System/Volumes/Data /` and key paths.

## Quick Workflow

1. Run a read-only audit:

```sh
uv run python scripts/audit_storage.py --markdown
```

Run commands from the installed skill directory. Use `--deep` only when a slower broad scan is acceptable.

2. Rank candidates:
   - Low risk: package caches, Homebrew cache, simulator dyld caches, unavailable simulators.
   - Medium risk: Xcode runtimes, local ML/runtime stacks, app service-worker caches.
   - High risk: app profiles, browser profiles, synced folders, media, datasets.
   - Do not delete: VM swap, Recovery/Preboot, system-managed assets not surfaced by a manager.

3. If acting, run only named actions from:

```sh
uv run python scripts/cleanup_actions.py --list
```

4. Use `--dry-run` first when available. For destructive actions, require `--confirm <ACTION_NAME>`.

5. Verify free space and record a short cleanup note.

## Playbook Selection

- **Emergency pressure below 10 GiB free:** read `references/cleanup-playbooks.md`, use "Emergency Oxygen".
- **Xcode/simulator growth:** use `simctl` actions only; read `references/macos-zones.md`.
- **Homebrew/Conda/tooling:** use Homebrew first; only direct-remove user-owned cask residue after failed manager uninstall and explicit user confirmation.
- **App Support/browser state:** close apps first; cache-only subpaths may be candidates, profiles/databases are high risk.
- **Human files/media/synced folders:** produce a review/offload plan, not a deletion plan.

## Known Lessons From Local Audits

- Miniconda under `/opt/homebrew/Caskroom/miniconda` consumed 31G and was removable after the user confirmed it was unused.
- `brew uninstall --cask miniconda` may fail in non-interactive environments because Homebrew invokes `sudo`.
- Xcode simulator runtime cleanup should use:

```sh
xcrun simctl delete unavailable
xcrun simctl runtime dyld_shared_cache remove --all
xcrun simctl runtime delete all --dry-run
xcrun simctl runtime delete all
```

- `simctl runtime delete all` can be asynchronous; poll `xcrun simctl runtime list` until disk images reach `0`.
- `_nsurlsessiond`-owned MobileAsset runtime `.dmg` files may remain after `simctl` cleanup. Do not manually remove them without a separate privileged/system-managed plan.

## References

- `references/safety-model.md`: value/risk taxonomy and non-negotiable rules.
- `references/macos-zones.md`: macOS storage zones and safe managers.
- `references/cleanup-playbooks.md`: ordered cleanup strategies and action templates.
