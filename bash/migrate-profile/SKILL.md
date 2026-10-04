---
name: migrate-profile
description: Move every Claude and Codex session from retired Emacs profiles into the current one. Use when the user says "/migrate-profile", has deployed or switched to a new Emacs/elpaca profile, or wants old-profile sessions, history or resume to follow the current profile.
---

# Migrate sessions to the current profile

The current profile is the target of `~/.config/emacs-profiles/active`. Every
other profile is retired, and all of its sessions belong in the current
profile. Invoking this skill is the authority to move them: do not ask which
profile, which packages or whether to proceed.

```bash
"$HOME/My Drive/dotfiles/bin/migrate-profile"
```

The script finds every Claude bucket, Claude prompt-history entry and Codex
rollout/thread whose directory lies in a retired profile, maps it to the same
relative directory in the current profile, and relocates it through the
reviewed `move-session-log` adapters with recovery backups under
`~/.local/state/profile-migrations/`. Several retired profiles may feed the
same package; Claude sessions are then merged one by one into the existing
bucket. `--dry-run` previews without writing.

Report the result in a few lines: what moved, what did not and why.

- **`not moved (agent still running there …)`**: a Claude or Codex process
  still runs in that retired directory, so its sessions stay put. Name the
  pid, ask whether to end it, then re-run the script.
- **`not moved (no counterpart …)`**: the directory no longer exists in the
  current profile. List it; there is nothing to move it to.
- **Marker mismatch** (`active` vs `.current-profile`): the script stops.
  Report it; do not edit either marker or restart Emacs.
- **Any other refusal**: do not hand-migrate around it. Fix the script or the
  adapter, add a test, and re-run.

Out of scope unless asked: trust/permission keys in `.claude.json`,
package-local `.claude/`/`.codex/` directories, Claude memory, repository
updates and deleting retired profiles.
