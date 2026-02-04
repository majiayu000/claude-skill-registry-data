---
name: statusline
description: Configure Claude Code's terminal status line display
version: 1.0.0
allowed-tools: [Read, Write, Edit, Bash]
---

# Statusline Implementation

Configure Claude Code's terminal status line with themes, modules, and presets.

---

## Quick Start

Choose a preset and apply it:

| Preset | Example Output |
|--------|----------------|
| **minimal** | `Opus 4.5 45%` |
| **informative** | `🤖 Opus 4.5 │ 📊 45%🟢 │ 💰 $1.23` |
| **developer** | `📁project │ 🤖Opus4.5 │ 📊45%🟢 │ 🌿main* │ 📦Node │ 💰$1.23` |
| **system** | `📁project │ 🤖Opus4.5 │ 📊45%🟢 │ 🌿main │ 💻15%🟢 │ 🧠62%🟡 │ 🐳3` |
| **bluera** | `Opus4.5 project 🐍 main* │ $1.23 │ ██████░░░░ 60% │ +42/-8 │ 5h:12% 7d:8%` |

---

## References

Detailed implementation docs:

- **@bluera-base/skills/statusline/references/themes.md** - 5 theme definitions (default, minimal, vibrant, monochrome, nerd)
- **@bluera-base/skills/statusline/references/modules.md** - All module implementations (directory, model, context, git, cost, rate-limits, project, lines-changed, battery, cpu, memory, docker, time, cca-status)
- **@bluera-base/skills/statusline/references/preset-scripts.md** - Complete ready-to-use bash scripts for each preset

---

## Helper Functions

Essential utilities for all statusline scripts:

```bash
get_status() {
  local pct=$1 warn_threshold=${2:-50} crit_threshold=${3:-75}
  if (( pct >= crit_threshold )); then echo "$STATUS_CRIT"
  elif (( pct >= warn_threshold )); then echo "$STATUS_WARN"
  else echo "$STATUS_OK"; fi
}

get_status_4level() {
  local pct=$1 fair=${2:-25} warn=${3:-50} crit=${4:-75}
  if (( pct >= crit )); then echo "$STATUS_4_CRIT"
  elif (( pct >= warn )); then echo "$STATUS_4_WARN"
  elif (( pct >= fair )); then echo "$STATUS_4_FAIR"
  else echo "$STATUS_4_OK"; fi
}

progress_bar() {
  local pct=$1 width=${2:-10}
  local filled=$(( pct * width / 100 )) empty=$(( width - filled ))
  printf "["; printf "%${filled}s" | tr ' ' '='; printf "%${empty}s" | tr ' ' '-'; printf "]"
}

safe_int() {
  local val="${1%%.*}"; val="${val//[^0-9-]/}"
  [[ "$val" =~ ^-?[0-9]+$ ]] && echo "$val" || echo "${2:-0}"
}

json_get() {
  local json="$1" path="$2" default="${3:-}"
  if command -v jq &>/dev/null; then
    local result; result=$(echo "$json" | jq -r "$path // empty" 2>/dev/null)
    echo "${result:-$default}"
  else echo "$default"; fi
}
```

---

## File Operations (REQUIRED)

After generating the statusline script:

```bash
# 1. Determine config directory
CLAUDE_CONFIG="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"

# 2. Backup existing (if present)
if [ -f "$CLAUDE_CONFIG/statusline.sh" ]; then
    cp "$CLAUDE_CONFIG/statusline.sh" "$CLAUDE_CONFIG/statusline.sh.backup-$(date +%Y%m%d-%H%M%S)"
fi

# 3. Write the script
cat > "$CLAUDE_CONFIG/statusline.sh" << 'STATUSLINE_EOF'
<generated script content here>
STATUSLINE_EOF

# 4. Make executable
chmod +x "$CLAUDE_CONFIG/statusline.sh"

# 5. Verify
ls -la "$CLAUDE_CONFIG/statusline.sh"
```

---

## Preserving User Customizations

When modifying an existing statusline, preserve user-added content:

**Detection patterns:**

- Boundary comments: `# --- custom ---` / `# --- end custom ---`
- Custom functions not matching standard module names
- External service integration (`curl` to localhost, non-standard config files)
- Custom variables referenced in final output

**Preservation algorithm:**

1. Read existing script
2. Extract sections between boundary comments
3. Identify custom variables used in output
4. Generate new script with standard modules
5. Append preserved custom sections before output
6. Update output format to include custom variables

---

## Preset Definitions

### minimal

```bash
THEME="minimal"
MODULES="model,context"
DISPLAY_MODE="compact"
```

### informative

```bash
THEME="default"
MODULES="model,context,cost"
DISPLAY_MODE="normal"
```

### developer

```bash
THEME="default"
MODULES="directory,model,context,git,project,cost"
DISPLAY_MODE="normal"
```

### system

```bash
THEME="default"
MODULES="directory,model,context,git,cpu,memory,docker"
DISPLAY_MODE="normal"
```

### bluera

Advanced with rate limits, context bar, ANSI colors. See preset-scripts.md for full implementation.
