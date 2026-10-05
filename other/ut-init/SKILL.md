---
name: ut-init
description: Initialize UltraThink capabilities in the current project directory
disable-model-invocation: true
allowed-tools: Bash
argument-hint: "[--global | --local]"
---

# Initialize UltraThink

Set up UltraThink in the current project or globally.

## If $ARGUMENTS contains "--global"

Run the global installer:

```bash
"${ULTRATHINK_DIR:-$(cd "$(dirname "$0")/../.." && pwd)}/scripts/init-global.sh"
```

This symlinks all skills, rules, agents, and hooks into `~/.claude/` so every Claude Code session has UltraThink.

## If $ARGUMENTS contains "--uninstall"

Remove UltraThink from global config:

```bash
"${ULTRATHINK_DIR:-$(cd "$(dirname "$0")/../.." && pwd)}/scripts/init-global.sh" --uninstall
```

## Default (local project init)

Symlink UltraThink into the current project's `.claude/` directory:

```bash
ULTRA="${ULTRATHINK_DIR:-$HOME/Documents/GitHub/InuVerse/ai-agents/ultrathink}"
PROJECT_DIR="$(pwd)"

# Create .claude directory if needed
mkdir -p "$PROJECT_DIR/.claude"

# Symlink skills
if [ ! -e "$PROJECT_DIR/.claude/skills" ]; then
  ln -s "$ULTRA/.claude/skills" "$PROJECT_DIR/.claude/skills"
  echo "Linked skills"
else
  echo "Skills already exist — skipping"
fi

# Symlink rules
if [ ! -e "$PROJECT_DIR/.claude/rules" ]; then
  ln -s "$ULTRA/.claude/rules" "$PROJECT_DIR/.claude/rules"
  echo "Linked rules"
else
  echo "Rules already exist — skipping"
fi

# Symlink agents
if [ ! -e "$PROJECT_DIR/.claude/agents" ]; then
  ln -s "$ULTRA/.claude/agents" "$PROJECT_DIR/.claude/agents"
  echo "Linked agents"
else
  echo "Agents already exist — skipping"
fi

# Copy .ckignore if not present
if [ ! -f "$PROJECT_DIR/.ckignore" ]; then
  cp "$ULTRA/.ckignore" "$PROJECT_DIR/.ckignore"
  echo "Copied .ckignore"
fi

echo ""
echo "UltraThink initialized in $PROJECT_DIR"
echo "Skills, rules, and agents are now available in this project."
```

After running, confirm what was linked and remind the user that skills are now available via `/ut-skills`.
