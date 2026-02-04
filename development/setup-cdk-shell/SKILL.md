---
name: setup-cdk-shell
description: Use when setting up shell environment for Claude Code - installs zsh, Oh My Zsh, Powerlevel10k theme, MesloLGS NF fonts, Claude CLI completions, and productivity aliases
---

# Setup CDK Shell

## Overview

Complete shell environment optimized for Claude Code development. Installs modern zsh setup with fast prompt, nerd fonts, completions, and aliases.

## When to Use

- Setting up shell for Claude development
- User asks about terminal/shell optimization
- Part of `setup-claude-dev-kit` bundle
- User wants zsh, powerlevel10k, or nerd fonts

## Quick Reference

| Component | Location |
|-----------|----------|
| Oh My Zsh | `~/.oh-my-zsh` |
| Theme | `~/.oh-my-zsh/custom/themes/powerlevel10k` |
| Fonts | `~/Library/Fonts/MesloLGS*.ttf` (macOS) |
| Config | `~/.p10k.zsh` |
| Completions | `~/.zsh/completions/_claude` |

## Installation Steps

### 1. Install Oh My Zsh (if needed)

```bash
# Check if installed
if [ ! -d ~/.oh-my-zsh ]; then
  sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended
fi
```

### 2. Install Powerlevel10k

```bash
# Clone theme
git clone --depth=1 https://github.com/romkatv/powerlevel10k.git \
  ${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/themes/powerlevel10k

# Or update if exists
cd ${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/themes/powerlevel10k && git pull
```

### 3. Install MesloLGS NF Fonts

**macOS:**
```bash
# Download fonts
curl -L -o /tmp/MesloLGS_NF_Regular.ttf "https://github.com/romkatv/powerlevel10k-media/raw/master/MesloLGS%20NF%20Regular.ttf"
curl -L -o /tmp/MesloLGS_NF_Bold.ttf "https://github.com/romkatv/powerlevel10k-media/raw/master/MesloLGS%20NF%20Bold.ttf"
curl -L -o /tmp/MesloLGS_NF_Italic.ttf "https://github.com/romkatv/powerlevel10k-media/raw/master/MesloLGS%20NF%20Italic.ttf"
curl -L -o /tmp/MesloLGS_NF_Bold_Italic.ttf "https://github.com/romkatv/powerlevel10k-media/raw/master/MesloLGS%20NF%20Bold%20Italic.ttf"

# Install to user fonts
mkdir -p ~/Library/Fonts
mv /tmp/MesloLGS_NF_*.ttf ~/Library/Fonts/
```

**Linux:**
```bash
mkdir -p ~/.local/share/fonts
# Same curl commands, then:
mv /tmp/MesloLGS_NF_*.ttf ~/.local/share/fonts/
fc-cache -fv
```

### 4. Install Useful Plugins

```bash
# zsh-autosuggestions
git clone https://github.com/zsh-users/zsh-autosuggestions \
  ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions

# zsh-syntax-highlighting
git clone https://github.com/zsh-users/zsh-syntax-highlighting \
  ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting
```

### 5. Configure .zshrc

Add/update in `~/.zshrc`:

```bash
# At the very top (instant prompt)
if [[ -r "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh" ]]; then
  source "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh"
fi

# Theme
ZSH_THEME="powerlevel10k/powerlevel10k"

# Plugins
plugins=(git zsh-autosuggestions zsh-syntax-highlighting)

# At the bottom
[[ -f ~/.p10k.zsh ]] && source ~/.p10k.zsh
```

### 6. Install Claude CLI Completions

```bash
mkdir -p ~/.zsh/completions

# Generate completions (if claude supports it)
claude --completions zsh > ~/.zsh/completions/_claude 2>/dev/null || true

# Add to .zshrc
echo 'fpath=(~/.zsh/completions $fpath)' >> ~/.zshrc
```

### 7. Add Claude Aliases

```bash
cat >> ~/.zshrc << 'EOF'

# Claude Dev Kit aliases
alias cc='claude'
alias ccp='claude -p'
alias cch='claude --help'
alias ccv='claude --version'
alias ccc='claude --continue'
alias ccr='claude --resume'
EOF
```

### 8. Configure Terminal Font

**Terminal.app:** Preferences → Profiles → Text → Font → "MesloLGS NF"

**iTerm2:** Preferences → Profiles → Text → Font → "MesloLGS NF"

**VS Code:** Add to settings.json:
```json
"terminal.integrated.fontFamily": "MesloLGS NF"
```

### 9. Run p10k Configuration

```bash
# Interactive wizard
p10k configure
```

## Verification

```bash
# Check components
[ -d ~/.oh-my-zsh ] && echo "✓ Oh My Zsh"
[ -d ~/.oh-my-zsh/custom/themes/powerlevel10k ] && echo "✓ Powerlevel10k"
ls ~/Library/Fonts/MesloLGS* 2>/dev/null && echo "✓ Fonts installed"
[ -f ~/.p10k.zsh ] && echo "✓ p10k configured"
command -v claude && echo "✓ Claude CLI"
```

## Adaptation Mode

When existing shell setup detected:

1. **Backup .zshrc:**
```bash
cp ~/.zshrc ~/.claude-dev-kit/backups/$(date +%Y-%m-%d)/.zshrc.bak
```

2. **Check for conflicts:**
- Starship prompt → Ask: keep or try p10k?
- Existing theme → Preserve or replace?
- Custom plugins → Merge, don't overwrite

3. **Append, don't replace:**
```bash
echo "# Claude Dev Kit Shell Additions" >> ~/.zshrc
```

## Common Issues

| Issue | Fix |
|-------|-----|
| Icons show as boxes | Terminal not using MesloLGS NF font |
| Theme not loading | Check `ZSH_THEME` in .zshrc |
| Slow prompt | Enable instant prompt at top of .zshrc |
| Completions not working | Run `compinit` or restart shell |

## Updating

```bash
# Update powerlevel10k
cd ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/themes/powerlevel10k && git pull

# Update plugins
cd ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions && git pull
cd ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting && git pull
```
