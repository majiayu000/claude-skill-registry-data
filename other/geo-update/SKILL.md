---
name: geo-update
description: "Pull the latest GEO-SEO skill updates from the upstream repository. Compares installed files against the latest release, shows what changed, and updates all skills, agents, scripts, and schema templates in place."
---

# GEO-SEO Update Skill

## Purpose

Updates the locally installed GEO-SEO skills, agents, scripts, and schema templates to the latest version from the upstream repository. Shows a summary of what changed before and after the update.

---

## Update Workflow

### Step 1: Determine Installed Location

The GEO-SEO toolkit installs to these locations under `~/.codex/`:

| Component | Install Path |
|-----------|-------------|
| Main skill | `~/.codex/skills/geo/` |
| Sub-skills | `~/.codex/skills/geo-*/` |
| Agents | `~/.codex/agents/geo-*.toml` |
| Scripts | `~/.codex/skills/geo/scripts/` |
| Schema templates | `~/.codex/skills/geo/schema/` |
| Hooks | `~/.codex/skills/geo/hooks/` |

Verify the installation exists by checking for `~/.codex/skills/geo/SKILL.md`. If it does not exist, inform the user that GEO-SEO is not installed and suggest running the installer instead.

### Step 2: Clone Latest from Upstream

```bash
TEMP_DIR=$(mktemp -d)
git clone --depth 1 https://github.com/bytefer/geo-seo-codex.git "$TEMP_DIR/repo"
```

If the clone fails, report the error and stop. Do not modify any installed files.

### Step 3: Compare Installed vs Latest

Before copying files, generate a diff summary so the user knows what will change:

1. For each component directory, compare the installed files against the cloned files using `diff --recursive --brief`.
2. Categorise changes as:
   - **New files** — exist in upstream but not locally
   - **Modified files** — exist in both but differ
   - **Removed files** — exist locally but not in upstream (these are NOT deleted automatically)
3. Present the summary to the user.

### Step 4: Apply Updates

Copy files from the cloned repo over the installed locations:

```bash
CODEX_DIR="${CODEX_HOME:-${HOME}/.codex}"
SKILLS_DIR="${CODEX_SKILLS_DIR:-${CODEX_DIR}/skills}"
AGENTS_DIR="${CODEX_AGENTS_DIR:-${CODEX_DIR}/agents}"
INSTALL_DIR="${SKILLS_DIR}/geo"
VENV_DIR="${INSTALL_DIR}/.venv"
VENV_PY="${VENV_DIR}/bin/python"
SOURCE_DIR="$TEMP_DIR/repo"

# Main skill
mkdir -p "$INSTALL_DIR"
cp -R "$SOURCE_DIR/skills/geo/." "$INSTALL_DIR/"

# Sub-skills
for skill_dir in "$SOURCE_DIR/skills"/*/; do
    skill_name=$(basename "$skill_dir")
    [ "$skill_name" = "geo" ] && continue
    mkdir -p "$SKILLS_DIR/${skill_name}"
    cp -R "$skill_dir/." "$SKILLS_DIR/${skill_name}/"
done

# Agents
mkdir -p "$AGENTS_DIR"
for agent_file in "$SOURCE_DIR/agents/"*.toml; do
    [ -f "$agent_file" ] || continue
    cp "$agent_file" "$AGENTS_DIR/"
done

# Scripts
if [ -d "$SOURCE_DIR/scripts" ]; then
    mkdir -p "$INSTALL_DIR/scripts"
    cp -R "$SOURCE_DIR/scripts/." "$INSTALL_DIR/scripts/"
    chmod +x "$INSTALL_DIR/scripts/"*.py "$INSTALL_DIR/scripts/webapp/"*.py 2>/dev/null || true
fi

# Schema templates
if [ -d "$SOURCE_DIR/schema" ]; then
    mkdir -p "$INSTALL_DIR/schema"
    cp -R "$SOURCE_DIR/schema/." "$INSTALL_DIR/schema/"
fi

# Report templates
if [ -d "$SOURCE_DIR/templates" ]; then
    mkdir -p "$INSTALL_DIR/templates"
    cp -R "$SOURCE_DIR/templates/." "$INSTALL_DIR/templates/"
fi

# White-label support files
if [ -d "$SOURCE_DIR/white-label" ]; then
    mkdir -p "$INSTALL_DIR/white-label"
    cp -R "$SOURCE_DIR/white-label/." "$INSTALL_DIR/white-label/"
fi

# Hooks
if [ -d "$SOURCE_DIR/hooks" ] && [ "$(ls -A "$SOURCE_DIR/hooks" 2>/dev/null)" ]; then
    mkdir -p "$INSTALL_DIR/hooks"
    cp -R "$SOURCE_DIR/hooks/." "$INSTALL_DIR/hooks/"
    chmod +x "$INSTALL_DIR/hooks/"* 2>/dev/null || true
fi
```

### Step 5: Update Python Dependencies

If `requirements.txt` exists in the upstream repo and differs from the installed version:

```bash
if [ ! -x "$VENV_PY" ]; then
    python3 -m venv "$VENV_DIR"
fi

"$VENV_PY" -m pip install --upgrade pip --quiet
"$VENV_PY" -m pip install -r "$SOURCE_DIR/requirements.txt" --quiet
cp "$SOURCE_DIR/requirements.txt" "$INSTALL_DIR/" 2>/dev/null || true

for f in "$INSTALL_DIR"/scripts/*.py "$INSTALL_DIR"/scripts/webapp/*.py; do
    [ -f "$f" ] || continue
    sed -i.bak "1s|^#!.*|#!${VENV_PY}|" "$f" && rm -f "${f}.bak"
    chmod +x "$f"
done
```

Report any failures but do not treat them as fatal.

### Step 6: Clean Up

```bash
rm -rf "$TEMP_DIR"
```

### Step 7: Report Results

Present a summary:

```
GEO-SEO Update Complete
=======================
New files:      [count]
Modified files: [count]
Unchanged:      [count]
Removed upstream (kept locally): [count]

Dependencies: [updated / unchanged / failed]
```

If there were removed files upstream, list them and suggest the user review whether to delete them manually.

---

## Important Notes

- **Never delete locally installed files** that no longer exist upstream. The user may have customised them. List them and let the user decide.
- **Never modify `~/.codex/config.toml` or other user Codex configuration files** — these are user configuration files, not part of the GEO-SEO toolkit.
- **If already up to date** (no diff), report that and skip the copy step.
- **Restart notice:** Remind the user that skill changes take effect in new Codex sessions. They should restart their session to use the updated skills.
