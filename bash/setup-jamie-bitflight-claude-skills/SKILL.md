---
name: setup
description: Use when installing, updating, or troubleshooting the dasel v3 binary — runs the install script, verifies installation, and diagnoses PATH and download issues
allowed-tools: Bash, Read
user-invocable: true
---

## Purpose

Install or update the dasel v3 binary from GitHub Releases into user-space (`~/.local/bin` on Linux/WSL2/macOS, `%LOCALAPPDATA%\Programs\dasel` on Windows). The install script handles platform detection, SHA256 verification, and PATH setup.

## Install Script

The install script is a PEP 723 Python script at `${CLAUDE_PLUGIN_ROOT}/scripts/install_dasel.py`.

### Commands

Install or update to latest version:

```bash
${CLAUDE_PLUGIN_ROOT}/scripts/install_dasel.py
```

Force reinstall (even if already at latest version):

```bash
${CLAUDE_PLUGIN_ROOT}/scripts/install_dasel.py --force
```

Preview what would happen without making changes:

```bash
${CLAUDE_PLUGIN_ROOT}/scripts/install_dasel.py --dry-run
```

Install to a custom directory instead of the default:

```bash
${CLAUDE_PLUGIN_ROOT}/scripts/install_dasel.py --bin-dir /custom/path
```

## Verify Installation

After install, confirm dasel is available:

```bash
dasel --version
```

Expected output format: `dasel version v3.x.x`

## Supported Platforms

- Linux x86_64 (amd64)
- Linux ARM64 (aarch64)
- Windows x64 (native + WSL2)

WSL2 uses the Linux binary (`dasel_linux_amd64`), not the Windows `.exe`. The WSL2 environment is a full Linux subsystem.

## Troubleshooting

### "command not found" after install

`~/.local/bin` is not in PATH. Add it:

```bash
export PATH="$HOME/.local/bin:$PATH"
```

Make persistent by adding to `~/.bashrc` or `~/.zshrc`:

```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

### Download failures

- Check internet connectivity: `curl -I https://api.github.com`
- GitHub API rate limits: unauthenticated requests are limited to 60/hour. Set `GITHUB_TOKEN` environment variable for higher limits.
- Retry with `--force` after transient failures.

### SHA256 mismatch

The install script verifies the downloaded binary against the SHA256 digest from the GitHub API response. A mismatch indicates a corrupted download or tampered binary.

Fix: re-download with `--force`:

```bash
${CLAUDE_PLUGIN_ROOT}/scripts/install_dasel.py --force
```

### Permission denied

Ensure the install directory exists and is writable:

```bash
mkdir -p ~/.local/bin
ls -ld ~/.local/bin
```

The directory should be owned by the current user with write permission.
