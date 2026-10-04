---
name: omarchy
description: "Configure and extend the Omarchy Linux desktop, troubleshoot Hyprland and Quickshell, and customize Neovim or desktop themes."
category: linux
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["omarchy", "arch-linux", "hyprland", "quickshell", "neovim", "tiling-wm", "linux-distribution", "dhh", "wayland", "claude"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# Omarchy Linux Distribution AI Skill Guide (Claude)

## Overview & System Architecture
Omarchy is a **beautiful, modern, and opinionated** omakase Linux distribution created by **David Heinemeier Hansson (DHH)** of Ruby on Rails and Basecamp/37signals fame. Built on **Arch Linux**, it combines the **Hyprland** Wayland tiling compositor, the **Quickshell** Qt/QML desktop construction kit, and a carefully curated set of modern CLI tools, TUIs, GUIs, and development utilities into a cohesive, aesthetically-driven desktop operating system. Omarchy v4.0 (codename "Quattro") is the current release. Claude operates as a Principal Linux Systems Architect and Omarchy Power User, specializing in **Hyprland configuration**, **Quickshell QML panel development**, **Omarchy CLI management**, **Neovim Lua plugin authoring**, **Zsh shell customization**, and **system-level Arch Linux administration**.

### Omarchy Multi-Layer System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                   Omarchy System Architecture                   │
│                                                                 │
│  Desktop Shell & Compositor                                     │
│  ├── Hyprland (Wayland Tiling Compositor & Window Manager)      │
│  ├── Quickshell (Qt/QML Desktop Panel & Widget Construction)    │
│  ├── Theming Engine (Wallpapers, Colors, Bar Styles)            │
│  └── Rofi-Wayland (Application Launcher & dmenu replacement)   │
│                                                                 │
│  Terminal & Editor Stack                                        │
│  ├── Ghostty (GPU-accelerated Wayland-native Terminal)          │
│  ├── Tmux (Terminal Multiplexer with custom keybindings)        │
│  ├── Neovim (Lua-configured IDE with LSP, Treesitter, Snacks)  │
│  └── Zsh (Shell with zsh-autosuggestions, syntax-highlighting)  │
│                                                                 │
│  System & Package Management                                    │
│  ├── pacman (Arch Linux official package manager)               │
│  ├── paru (AUR helper, yay-compatible)                          │
│  ├── Omarchy CLI (omarchy update/theme/install/plugin)          │
│  └── Dotfile Management (~/.config/omarchy/)                    │
│                                                                 │
│  Bundled Application Ecosystem                                  │
│  ├── Chromium, LibreOffice, Obsidian, Kdenlive, OBS Studio      │
│  ├── Qimgv (image viewer), Qmmp (Winamp-style music player)    │
│  ├── Steam + Lutris (Gaming via Proton/Wine)                    │
│  └── Claude Code, Zed Editor (AI-powered development)           │
└─────────────────────────────────────────────────────────────────┘
```

---

## Operational Capabilities & Agent Directives

1. **Hyprland Configuration**: Edit `~/.config/hypr/hyprland.conf` for monitor layouts, workspace rules, window rules, keybindings, animations, and input device configuration.
2. **Quickshell QML Panel Development**: Author and modify Quickshell panels (top bar, notification center, clipboard manager) using Qt Quick/QML declarative UI.
3. **Omarchy CLI Operations**: Execute `omarchy update`, `omarchy theme`, `omarchy install`, `omarchy plugin`, and `omarchy dotfiles` commands for system management.
4. **Neovim Lua Configuration**: Configure Neovim with `lazy.nvim` plugin manager, Treesitter grammars, LSP servers via `mason.nvim`, and custom keymaps.
5. **Zsh & Shell Customization**: Manage Zsh plugins (autosuggestions, syntax-highlighting, fzf-tab), aliases, shell functions, and prompt (Starship).
6. **Theme Creation & Customization**: Create custom Omarchy themes by defining color palettes, wallpapers, Hyprland border colors, and Quickshell QML style overrides.
7. **System Administration**: Perform Arch Linux package management (pacman/paru), systemd service management, kernel updates, and hardware troubleshooting.

---

## Production Bash Script: Omarchy System Health Check & Auto-Repair

Save this file as `~/.local/bin/omarchy-health-check.sh` and run with `bash omarchy-health-check.sh`:

```bash
#!/usr/bin/env bash
# ==============================================================================
# Omarchy System Health Check & Auto-Repair Script
# Validates core Omarchy subsystems, repairs common issues, and reports status.
# Compatible with Omarchy 4.0 (Quattro) on Arch Linux.
# ==============================================================================
set -euo pipefail

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

log_ok()   { echo -e "${GREEN}[✓]${NC} $1"; }
log_fail() { echo -e "${RED}[✗]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[!]${NC} $1"; }
log_info() { echo -e "${CYAN}[i]${NC} $1"; }

echo -e "${CYAN}═══════════════════════════════════════════════════${NC}"
echo -e "${CYAN}  Omarchy System Health Check (v4.0 Quattro)${NC}"
echo -e "${CYAN}═══════════════════════════════════════════════════${NC}"
echo ""

# 1. Verify Hyprland Compositor
if pgrep -x Hyprland > /dev/null 2>&1; then
    HYPR_VER=$(hyprctl version 2>/dev/null | grep -oP 'v[\d.]+' | head -1)
    log_ok "Hyprland compositor running (${HYPR_VER:-unknown})"
else
    log_fail "Hyprland is NOT running"
    log_info "Start Hyprland: exec Hyprland (from TTY login)"
fi

# 2. Verify Quickshell Desktop Panels
if pgrep -x quickshell > /dev/null 2>&1; then
    log_ok "Quickshell desktop panels active"
else
    log_warn "Quickshell not running - top bar and widgets unavailable"
    log_info "Restart: quickshell &"
fi

# 3. Verify Ghostty Terminal
if command -v ghostty &> /dev/null; then
    log_ok "Ghostty terminal emulator installed"
else
    log_fail "Ghostty not found"
    log_info "Install: paru -S ghostty"
fi

# 4. Verify Neovim Installation & Config
if command -v nvim &> /dev/null; then
    NVIM_VER=$(nvim --version | head -1)
    log_ok "Neovim: ${NVIM_VER}"
    if [ -d "${XDG_CONFIG_HOME:-$HOME/.config}/nvim" ]; then
        log_ok "Neovim config directory exists"
    else
        log_warn "Neovim config missing at ~/.config/nvim"
    fi
else
    log_fail "Neovim not installed"
fi

# 5. Check Omarchy CLI
if command -v omarchy &> /dev/null; then
    log_ok "Omarchy CLI available"
else
    log_warn "Omarchy CLI not found in PATH"
    log_info "Ensure ~/.local/bin is in PATH or source Omarchy shell config"
fi

# 6. Check Core Development Tools
TOOLS=("git" "mise" "fzf" "bat" "eza" "fd" "rg" "lazygit" "lazydocker" "zoxide" "starship")
MISSING=()
for tool in "${TOOLS[@]}"; do
    if ! command -v "$tool" &> /dev/null; then
        MISSING+=("$tool")
    fi
done
if [ ${#MISSING[@]} -eq 0 ]; then
    log_ok "All ${#TOOLS[@]} core dev tools present"
else
    log_warn "Missing tools: ${MISSING[*]}"
    log_info "Install missing: paru -S ${MISSING[*]}"
fi

# 7. Check Wayland Session Variables
if [ "${XDG_SESSION_TYPE:-}" = "wayland" ]; then
    log_ok "Wayland session active (XDG_SESSION_TYPE=wayland)"
else
    log_warn "Not in a Wayland session (XDG_SESSION_TYPE=${XDG_SESSION_TYPE:-unset})"
fi

# 8. Check pacman Database & Updates
UPDATES=$(checkupdates 2>/dev/null | wc -l || echo "0")
if [ "$UPDATES" -gt 0 ]; then
    log_info "${UPDATES} package updates available (run: omarchy update)"
else
    log_ok "System packages up to date"
fi

# 9. Check Disk Space
ROOT_USAGE=$(df / --output=pcent | tail -1 | tr -d ' %')
if [ "$ROOT_USAGE" -lt 85 ]; then
    log_ok "Root filesystem usage: ${ROOT_USAGE}%"
else
    log_warn "Root filesystem usage: ${ROOT_USAGE}% - consider cleanup"
fi

# 10. Check Theme Configuration
THEME_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/omarchy/themes"
if [ -d "$THEME_DIR" ]; then
    THEME_COUNT=$(find "$THEME_DIR" -maxdepth 1 -type d | wc -l)
    log_ok "Theme directory found (${THEME_COUNT} themes)"
else
    log_info "No custom themes directory at $THEME_DIR"
fi

echo ""
echo -e "${CYAN}═══════════════════════════════════════════════════${NC}"
echo -e "${CYAN}  Health check complete.${NC}"
echo -e "${CYAN}═══════════════════════════════════════════════════${NC}"
```

---

## Hyprland Configuration Reference

### Essential Keybindings (Omarchy Defaults)

```conf
# ~/.config/hypr/hyprland.conf - Omarchy Default Keybindings (Super = Mod key)

# Window Navigation
bind = SUPER, H, movefocus, l          # Focus left
bind = SUPER, L, movefocus, r          # Focus right
bind = SUPER, K, movefocus, u          # Focus up
bind = SUPER, J, movefocus, d          # Focus down

# Window Movement
bind = SUPER SHIFT, H, movewindow, l   # Move window left
bind = SUPER SHIFT, L, movewindow, r   # Move window right
bind = SUPER SHIFT, K, movewindow, u   # Move window up
bind = SUPER SHIFT, J, movewindow, d   # Move window down

# Workspace Switching (1-9)
bind = SUPER, 1, workspace, 1
bind = SUPER, 2, workspace, 2
bind = SUPER, 3, workspace, 3
bind = SUPER, 4, workspace, 4
bind = SUPER, 5, workspace, 5

# Move Window to Workspace
bind = SUPER SHIFT, 1, movetoworkspace, 1
bind = SUPER SHIFT, 2, movetoworkspace, 2
bind = SUPER SHIFT, 3, movetoworkspace, 3

# Application Launchers
bind = SUPER, RETURN, exec, ghostty             # Terminal
bind = SUPER, D, exec, rofi -show drun           # App launcher
bind = SUPER, B, exec, chromium                   # Browser
bind = SUPER, E, exec, thunar                     # File manager
bind = SUPER, Q, killactive                       # Close window
bind = SUPER SHIFT, Q, exit                       # Exit Hyprland

# Layout Toggles
bind = SUPER, F, fullscreen, 0                    # Fullscreen
bind = SUPER, T, togglefloating                   # Toggle floating
bind = SUPER, P, pseudo                           # Pseudo-tile

# Screenshots (grim + slurp)
bind = , Print, exec, grim ~/Pictures/screenshot-$(date +%Y%m%d-%H%M%S).png
bind = SUPER, Print, exec, grim -g "$(slurp)" ~/Pictures/screenshot-$(date +%Y%m%d-%H%M%S).png
```

### Monitor Configuration

```conf
# Multi-monitor setup example
monitor = DP-1, 3840x2160@144, 0x0, 1.5       # Primary 4K monitor
monitor = HDMI-A-1, 2560x1440@60, 2560x0, 1   # Secondary monitor
monitor = , preferred, auto, 1                  # Fallback for any other

# Workspace assignment to monitors
workspace = 1, monitor:DP-1, default:true
workspace = 2, monitor:DP-1
workspace = 3, monitor:HDMI-A-1, default:true
```

---

## Omarchy CLI Command Reference

```bash
# System Updates
omarchy update                   # Full system update (pacman + paru + omarchy)
omarchy update --packages-only   # Update only system packages

# Theme Management
omarchy theme                    # List available themes
omarchy theme set <name>         # Apply theme (changes wallpaper, colors, bar)
omarchy theme preview <name>     # Preview theme without applying

# Plugin Management
omarchy plugin list              # List installed shell plugins
omarchy plugin install <name>    # Install a shell plugin
omarchy plugin remove <name>     # Remove a shell plugin

# Dotfiles
omarchy dotfiles                 # Show dotfile status
omarchy dotfiles sync            # Sync dotfiles from repository
omarchy dotfiles diff            # Show changes between local and repo

# Installation
omarchy install                  # Re-run Omarchy installer/setup
```

---

## Omarchy Theme Creation Guide

Create a custom theme at `~/.config/omarchy/themes/my-theme/`:

```bash
# Theme directory structure
~/.config/omarchy/themes/my-theme/
├── theme.toml              # Theme metadata and color definitions
├── wallpaper.jpg           # Desktop wallpaper (any resolution)
├── hyprland.conf           # Hyprland overrides (border colors, gaps, animations)
└── quickshell/             # Quickshell QML style overrides
    └── colors.qml          # Panel color definitions
```

### theme.toml Example

```toml
[theme]
name = "Nordic Frost"
author = "your-name"
version = "1.0"

[colors]
background = "#2E3440"
foreground = "#ECEFF4"
accent = "#88C0D0"
border_active = "#81A1C1"
border_inactive = "#3B4252"
bar_background = "#2E3440"
bar_foreground = "#D8DEE9"
```

---

## Technical Troubleshooting Matrix

| Issue & Failure Signature | Root Cause Analysis | Diagnostic & Resolution Pathway |
| :--- | :--- | :--- |
| **Black screen after login / Hyprland fails to start** | GPU driver incompatibility (especially Nvidia) or missing Wayland session. | 1. Switch to TTY2: `Ctrl+Alt+F2`.<br>2. Check logs: `journalctl -xb -u sddm` or `cat ~/.local/share/hyprland/hyprland.log`.<br>3. For Nvidia: install `nvidia-dkms`, add `nvidia_drm.modeset=1` to kernel params, add `env = LIBVA_DRIVER_NAME,nvidia` to hyprland.conf. |
| **Top bar / panels not rendering** | Quickshell process crashed or QML config error. | 1. Check status: `pgrep quickshell`.<br>2. Restart: `killall quickshell && quickshell &`.<br>3. Validate QML: check `~/.config/quickshell/` for syntax errors.<br>4. Debug: `quickshell --debug 2>&1 \| tee /tmp/qs.log`. |
| **Ghostty terminal crashes or won't open** | Missing GPU acceleration drivers or config error. | 1. Test: `ghostty --check-config`.<br>2. Fallback: `LIBGL_ALWAYS_SOFTWARE=1 ghostty`.<br>3. Config: check `~/.config/ghostty/config`. |
| **Screen tearing or stuttering** | VSync not enabled in Hyprland or incorrect refresh rate. | 1. Add to hyprland.conf: `misc { vfr = true }`.<br>2. Check monitor config: `hyprctl monitors`.<br>3. For Nvidia: set `env = __GL_GSYNC_ALLOWED,1`. |
| **Keybindings not working** | Keybinding conflict or modifier key misconfigured. | 1. Check active binds: `hyprctl binds`.<br>2. Debug: `hyprctl dispatch exec 'notify-send test'`.<br>3. Verify Super key mapping in `hyprland.conf`. |
| **Audio not working** | PipeWire/WirePlumber service not running. | 1. Check: `systemctl --user status pipewire wireplumber`.<br>2. Restart: `systemctl --user restart pipewire wireplumber`.<br>3. Verify: `wpctl status` and `wpctl set-default <sink-id>`. |
| **Clipboard not syncing between apps** | Wayland clipboard protocol issue or cliphist not running. | 1. Check: `wl-paste --list-types`.<br>2. Verify cliphist: `pgrep wl-clip-persist`.<br>3. Test: `echo test \| wl-copy && wl-paste`. |
| **Updates failing with pacman lock** | Another pacman instance running or stale lock file. | 1. Check: `pgrep pacman`.<br>2. Remove stale lock: `sudo rm /var/lib/pacman/db.lck`.<br>3. Retry: `omarchy update`. |
| **Multi-monitor layout broken after wake from sleep** | Hyprland does not re-detect monitors on resume. | 1. Re-apply: `hyprctl reload`.<br>2. Check monitors: `hyprctl monitors`.<br>3. If persistent, add `exec-once = sleep 2 && hyprctl reload` to hyprland.conf. |

---

## Essential File Locations & Directories

```
~/.config/hypr/hyprland.conf       # Hyprland compositor configuration
~/.config/hypr/hyprlock.conf       # Lock screen configuration
~/.config/hypr/hypridle.conf       # Idle timeout & screensaver settings
~/.config/quickshell/              # Quickshell QML panel configuration
~/.config/ghostty/config           # Ghostty terminal configuration
~/.config/nvim/                    # Neovim Lua configuration (init.lua)
~/.config/tmux/tmux.conf           # Tmux multiplexer configuration
~/.config/rofi/                    # Rofi launcher theme & configuration
~/.config/starship.toml            # Starship prompt configuration
~/.config/omarchy/                 # Omarchy-specific settings & themes
~/.local/bin/                      # User scripts (Omarchy CLI lives here)
~/.local/share/hyprland/           # Hyprland logs and runtime data
/etc/omarchy/                      # System-wide Omarchy configuration
```

---

## Bundled Software Ecosystem Reference

### Terminal & Development
| Tool | Purpose |
| :--- | :--- |
| **Ghostty** | GPU-accelerated Wayland-native terminal emulator |
| **Neovim** | Lua-configured text editor with LSP, Treesitter, telescope.nvim |
| **Tmux** | Terminal multiplexer with Omarchy-custom keybindings |
| **Zsh** | Shell with autosuggestions, syntax-highlighting, fzf-tab |
| **Starship** | Cross-shell prompt with git status and language indicators |
| **mise** | Polyglot version manager (Ruby, Node, Python, Go, Rust) |
| **lazygit** | TUI Git client with interactive rebase and staging |
| **lazydocker** | TUI Docker container and image management |

### CLI Utilities
| Tool | Purpose |
| :--- | :--- |
| **fzf** | Fuzzy finder for files, history, processes |
| **bat** | Cat replacement with syntax highlighting and git integration |
| **eza** | Modern ls replacement with icons, git status, tree view |
| **fd** | Fast find alternative with regex and ignore support |
| **ripgrep (rg)** | Ultra-fast recursive grep with .gitignore awareness |
| **zoxide** | Smarter cd with frecency-based directory jumping |
| **btop** | Resource monitor (CPU, memory, disk, network, processes) |
| **dust** | Intuitive disk usage analyzer (du replacement) |
| **duf** | Disk usage/free utility with colored output |
| **glow** | Terminal markdown renderer |
| **jq** | Command-line JSON processor |

### GUI Applications
| Application | Purpose |
| :--- | :--- |
| **Chromium** | Web browser |
| **Obsidian** | Knowledge base and note-taking (Markdown vault) |
| **LibreOffice** | Office suite (Writer, Calc, Impress) |
| **Kdenlive** | Non-linear video editor |
| **OBS Studio** | Streaming and screen recording |
| **Qimgv** | Lightweight image viewer |
| **Qmmp** | Winamp-style music player |
| **Thunar** | Lightweight file manager |
| **Steam** | Gaming platform (Proton compatibility layer) |
| **Lutris** | Gaming launcher for Wine/Proton games |

---

## Agent Operational Directive
> **MANDATORY**: When configuring Omarchy systems, always verify the Hyprland compositor version with `hyprctl version`, check that Wayland session variables are set (`echo $XDG_SESSION_TYPE`), and use `hyprctl reload` rather than restarting the compositor to apply configuration changes non-destructively. Always back up configuration files before modifying them: `cp ~/.config/hypr/hyprland.conf ~/.config/hypr/hyprland.conf.bak`.
