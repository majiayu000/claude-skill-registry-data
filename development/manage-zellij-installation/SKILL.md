---
name: manage-zellij-installation
description: Installs and configures Zellij terminal multiplexer from GitHub releases. Use when setting up Zellij for terminal workspace management.
---

## Prerequisites
- macOS or Linux
- curl installed
- tar installed

## Installation

### 1. Ensure ~/.local/bin exists and is in PATH

```bash
mkdir -p ~/.local/bin
```

Add to `~/.bashrc` if not already present:
```bash
export PATH="$HOME/.local/bin:$PATH"
```

Then reload:
```bash
source ~/.bashrc
```

### 2. Download and install Zellij binary

Determine OS and architecture, then download the appropriate release from https://github.com/zellij-org/zellij/releases

**For macOS (Apple Silicon):**
```bash
curl -L https://github.com/zellij-org/zellij/releases/latest/download/zellij-aarch64-apple-darwin.tar.gz -o /tmp/zellij.tar.gz
```

**For macOS (Intel):**
```bash
curl -L https://github.com/zellij-org/zellij/releases/latest/download/zellij-x86_64-apple-darwin.tar.gz -o /tmp/zellij.tar.gz
```

**For Linux (x86_64):**
```bash
curl -L https://github.com/zellij-org/zellij/releases/latest/download/zellij-x86_64-unknown-linux-musl.tar.gz -o /tmp/zellij.tar.gz
```

**For Linux (aarch64):**
```bash
curl -L https://github.com/zellij-org/zellij/releases/latest/download/zellij-aarch64-unknown-linux-musl.tar.gz -o /tmp/zellij.tar.gz
```

### 3. Extract and install

```bash
tar -xvf /tmp/zellij.tar.gz -C /tmp
chmod +x /tmp/zellij
mv /tmp/zellij ~/.local/bin/
rm /tmp/zellij.tar.gz
```

### 4. Configure Zellij

Create config directory and dump default configuration:
```bash
mkdir -p ~/.config/zellij
zellij setup --dump-config > ~/.config/zellij/config.kdl
```

### 5. Set locked mode as default

Edit `~/.config/zellij/config.kdl` and ensure this line is present (uncommented) near the top:
```kdl
default_mode "locked"
```

## Verify

```bash
zellij --version
```

Confirm config exists:
```bash
cat ~/.config/zellij/config.kdl | grep default_mode
```

## Update

1. Download the latest release (repeat step 2 from Installation with the new version)
2. Extract and replace the binary:
```bash
tar -xvf /tmp/zellij.tar.gz -C /tmp
chmod +x /tmp/zellij
mv /tmp/zellij ~/.local/bin/
rm /tmp/zellij.tar.gz
```

Check releases at: https://github.com/zellij-org/zellij/releases

## Uninstall

1. Remove the binary:
```bash
rm ~/.local/bin/zellij
```

2. Remove configuration:
```bash
rm -rf ~/.config/zellij
```

3. Remove cache and data (if any):
```bash
rm -rf ~/.cache/zellij
rm -rf ~/.local/share/zellij
```
