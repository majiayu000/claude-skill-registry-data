---
name: mde-homebrew
description: >
  Use when diagnosing brew failures in mde update, auditing brew-owned packages,
  resolving brew-vs-mise ownership conflicts, or troubleshooting Homebrew on macOS.
  Key files: src/mde/maintain/update.py, src/mde/validate/brew.py,
  configs/mde-tool-ownership.json. Keywords: brew doctor, brew upgrade,
  cask sudo, tap repair, formula conflict, Brewfile.
---

# Homebrew Boundary & Diagnostics

## Use This Skill When

- `mde update` fails at the brew step
- Auditing what brew owns vs what mise owns
- Adding or removing a brew formula/cask
- Investigating `brew doctor` warnings

## Contract

1. Brew owns **only 3 formulae**: `gnupg`, `curl`, `chafa` (+ `tree` as optional utility).
2. Brew owns all **casks** (GUI apps: ghostty, iterm2, sublime-text, etc.).
3. All CLI tools are managed by **mise** — no exceptions, no fallback.
4. Runtimes (python, node, go, rust) belong to mise — **never** brew.
5. The Brewfile is managed by chezmoi at `home/Brewfile.tmpl`.
6. `chezmoi apply` triggers `run_onchange_before_install-packages-darwin.sh.tmpl` to run `brew bundle`.
7. PATH ordering places brew at positions 11-12, after all other managers.
8. `HOMEBREW_NO_AUTO_UPDATE=1` should be set in CI contexts.

## What Was Migrated to Mise

These were previously brew formulae, now mise-managed:

| Former brew formula | Mise entry |
|--------------------|-----------|
| glow | `glow = "latest"` (registry) |
| crush | `"aqua:charmbracelet/crush"` |
| cloudflared | `cloudflared = "latest"` |
| direnv | `direnv = "latest"` |
| pandoc | `pandoc = "latest"` |
| tmux | `tmux = "latest"` |
| xcodegen | `xcodegen = "latest"` |
| llvm | `clang = "latest"` |
| docker | `docker-cli = "latest"` |
| docker-compose | `docker-compose = "latest"` |
| buildkit | `"aqua:moby/buildkit" = "latest"` |
| docker-agent (cagent) | `"github:docker/docker-agent" = "latest"` |
| session-manager-plugin | `"aqua:aws/session-manager-plugin" = "latest"` |

## Diagnostic Playbook

```bash
# 1. Check brew health
brew doctor

# 2. List outdated formulae/casks
brew outdated

# 3. Show what brew owns (should be ~3-4 formulae + casks)
brew leaves
brew list --cask

# 4. Validate with mde
uv run mde-py validate --brew

# 5. Compare against mise ownership
mise ls --current
```

## Common Failures

| Symptom | Cause | Resolution |
|---------|-------|------------|
| `brew upgrade` non-zero exit | Individual cask/formula failure | Non-fatal; check output for specific package |
| Cask requires sudo | macOS app bundle in /Applications | Run `brew upgrade --cask <name>` manually with sudo |
| `No available formula` | Tap removed or renamed | `brew tap --repair` then retry |
| Unexpected formula in `brew leaves` | Tool not yet uninstalled from brew | `brew uninstall <formula>` — it's now in mise |

## Periodic Maintenance

- `brew cleanup --prune=all` to reclaim disk
- `brew autoremove` to remove orphaned deps
- Review `brew leaves` quarterly — should be 3-4 items only
