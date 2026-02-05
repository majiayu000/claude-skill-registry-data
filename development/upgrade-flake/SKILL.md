---
name: upgrade-flake
description: |
  This skill updates flake.lock to get latest packages within current NixOS release.
  Triggers: "update flake", "upgrade flake", "nix flake update", "bump flake.lock",
  "update flake inputs", "refresh inputs", "update dependencies".
  Runs nix flake update, checks build, optionally applies.
  Not for NixOS release upgrades (use upgrade-nixos for major version changes).
---

# Upgrade Flake Inputs

Update `flake.lock` to pull in the latest commits from all flake inputs. This gets you newer package versions without changing NixOS release channels.

## What this does

- Updates all inputs to their latest commits (nixpkgs, home-manager, etc.)
- Does NOT change release channels (stays on same NixOS version)
- Safe operation - can always rollback

## Process

1. **Update the lock file**
   ```bash
   just update
   ```
   This runs `nix flake update` and updates `flake.lock`.

2. **Build and verify** (safe dry-run)
   ```bash
   just check
   ```
   Builds all configurations without applying. If this fails, fix errors before proceeding.

3. **Apply the update** (when ready)
   ```bash
   just switch
   ```

4. **Verify services are running**
   ```bash
   systemctl status docker tailscaled
   ```

## Rollback if needed
When you're done echo out the instructions to:
```bash
# Revert to previous system generation
sudo nixos-rebuild switch --rollback

# Revert flake.lock to previous state
git checkout flake.lock
```

## Tips

- show the user what ch `git diff flake.lock` to see what changed before applying
- Old boot entries remain available for rollback until garbage collected

$ARGUMENTS
