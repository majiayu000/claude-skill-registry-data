---
name: new-skill
description: "Install, create, scaffold, and validate new skills in Codex-first skill folders such as .codex/skills/ and .agents/skills/. Use when adding a skill from a URL, GitHub repo, zip file, or markdown content, or when creating a new skill from scratch. Also use for validating existing skills, fixing registration issues, or restructuring agent skill folders."
---

# New Skill Installer & Scaffolder

## Overview

This skill helps you install, create, and manage skills in your Codex-first `.codex/skills/` or `.agents/skills/` directory. It handles the full lifecycle: scaffolding new skills from scratch, installing skills from external sources, validating skill structure, and troubleshooting registration issues.

---

## Workflow 1: Create a New Skill From Scratch

When the user wants to create a brand new skill:

1. **Ask for details** (if not provided):
   - Skill name (lowercase, hyphenated, e.g. `api-tester`)
   - What it should do (purpose)
   - When it should trigger (contexts)
   - Whether it needs scripts, references, or assets

2. **Scaffold the folder structure:**

```bash
SKILL_NAME="the-skill-name"
PROJECT_DIR="$(pwd)"
SKILL_DIR="${PROJECT_DIR}/.codex/skills/${SKILL_NAME}"

mkdir -p "${SKILL_DIR}"
mkdir -p "${SKILL_DIR}/scripts"
mkdir -p "${SKILL_DIR}/references"
mkdir -p "${SKILL_DIR}/assets"
```

3. **Generate the SKILL.md** with proper frontmatter:

```markdown
---
name: {skill-name}
description: "{What it does}. Use when {trigger conditions}. Handles {capabilities}."
---

# {Skill Title}

## Overview
{One paragraph purpose statement}

## Instructions
1. {Step-by-step instructions}

## Examples
### Example 1
**Input:** "{example user request}"
**Action:** {what the skill does}
**Output:** {expected result}

## Error Handling
- {How to handle failures}

## Notes
- {Caveats and edge cases}
```

4. **Validate the skill** (run Workflow 4 below)

5. **Report back** with the file tree and confirmation it's registered.

---

## Workflow 2: Install a Skill From External Source

When the user provides a URL, GitHub repo, zip file, or raw markdown:

### From a GitHub Repository URL

```bash
REPO_URL="$1"
SKILL_NAME="$2"  # Extract from repo name if not given
SKILL_DIR=".codex/skills/${SKILL_NAME}"

# Clone just the skill content
git clone --depth 1 "${REPO_URL}" "/tmp/${SKILL_NAME}-clone"

# Find the SKILL.md
SKILL_FILE=$(find "/tmp/${SKILL_NAME}-clone" -name "SKILL.md" -type f | head -1)

if [ -z "$SKILL_FILE" ]; then
  echo "ERROR: No SKILL.md found in repository."
  echo "This repo may not be a valid AgentSkills package."
  exit 1
fi

# Get the skill's parent directory (contains SKILL.md + siblings)
SKILL_SRC=$(dirname "$SKILL_FILE")

# Copy to .codex/skills/
mkdir -p "${SKILL_DIR}"
cp -r "${SKILL_SRC}/"* "${SKILL_DIR}/"

# Cleanup
rm -rf "/tmp/${SKILL_NAME}-clone"

echo "Installed ${SKILL_NAME} to ${SKILL_DIR}"
```

### From Raw Markdown Content

If the user pastes or uploads a SKILL.md file:

1. Extract the `name` field from YAML frontmatter
2. Create `.codex/skills/{name}/SKILL.md`
3. Write the content
4. Check if it references external files (scripts/, references/, assets/)
5. Warn the user about any missing referenced files

### From a Zip File

```bash
ZIP_FILE="$1"
TEMP_DIR="/tmp/skill-install-$$"

mkdir -p "$TEMP_DIR"
unzip -q "$ZIP_FILE" -d "$TEMP_DIR"

# Find SKILL.md (may be nested in a folder)
SKILL_FILE=$(find "$TEMP_DIR" -name "SKILL.md" -type f | head -1)

if [ -z "$SKILL_FILE" ]; then
  echo "ERROR: No SKILL.md found in zip."
  exit 1
fi

SKILL_SRC=$(dirname "$SKILL_FILE")
SKILL_NAME=$(grep "^name:" "$SKILL_FILE" | head -1 | sed 's/name: *//' | tr -d '"' | tr ' ' '-' | tr '[:upper:]' '[:lower:]')

if [ -z "$SKILL_NAME" ]; then
  SKILL_NAME=$(basename "$SKILL_SRC")
fi

SKILL_DIR=".codex/skills/${SKILL_NAME}"
mkdir -p "$SKILL_DIR"
cp -r "$SKILL_SRC/"* "$SKILL_DIR/"

rm -rf "$TEMP_DIR"
echo "Installed ${SKILL_NAME} to ${SKILL_DIR}"
```

---

## Workflow 3: Install the Uploaded MCP Builder Skill

When the user wants to install the `mcp-builder` skill specifically:

1. Create the directory structure:

```bash
mkdir -p .codex/skills/mcp-builder/reference
```

2. Copy or create the SKILL.md from the user's uploaded file into `.codex/skills/mcp-builder/SKILL.md`

3. Note that the SKILL.md references these files that need to be populated:
   - `{baseDir}/reference/mcp_best_practices.md`
   - `{baseDir}/reference/python_mcp_server.md`
   - `{baseDir}/reference/node_mcp_server.md`
   - `{baseDir}/reference/evaluation.md`

4. Either fetch them from the source repo (if URL provided) or create stub files:

```bash
for ref in mcp_best_practices python_mcp_server node_mcp_server evaluation; do
  if [ ! -f ".codex/skills/mcp-builder/reference/${ref}.md" ]; then
    echo "# ${ref}" > ".codex/skills/mcp-builder/reference/${ref}.md"
    echo "" >> ".codex/skills/mcp-builder/reference/${ref}.md"
    echo "TODO: Populate with content from the original skill repository." >> ".codex/skills/mcp-builder/reference/${ref}.md"
    echo "Source: https://github.com/ComposioHQ/awesome-claude-skills/tree/main/mcp-builder/reference" >> ".codex/skills/mcp-builder/reference/${ref}.md"
  fi
done
```

5. Warn the user that stub reference files need real content for full functionality.

---

## Workflow 4: Validate Skills

Run these checks on any skill to ensure it will register properly:

### Validation Checklist

```bash
SKILL_DIR="$1"  # e.g., .codex/skills/my-skill

# 1. Check SKILL.md exists
if [ ! -f "${SKILL_DIR}/SKILL.md" ]; then
  echo "FAIL: No SKILL.md found in ${SKILL_DIR}"
  exit 1
fi

# 2. Check frontmatter exists
if ! head -1 "${SKILL_DIR}/SKILL.md" | grep -q "^---"; then
  echo "FAIL: SKILL.md must start with --- (YAML frontmatter)"
  exit 1
fi

# 3. Check name field
if ! grep -q "^name:" "${SKILL_DIR}/SKILL.md"; then
  echo "FAIL: Missing 'name:' in frontmatter"
  exit 1
fi

# 4. Check description field
if ! grep -q "^description:" "${SKILL_DIR}/SKILL.md"; then
  echo "FAIL: Missing 'description:' in frontmatter"
  exit 1
fi

# 5. Check description is quoted if it has special chars
DESC_LINE=$(grep "^description:" "${SKILL_DIR}/SKILL.md" | head -1)
if echo "$DESC_LINE" | grep -qE '[\[\]#]' && ! echo "$DESC_LINE" | grep -q '"'; then
  echo "WARN: Description contains special characters but is not quoted. This may cause YAML parse failures."
fi

# 6. Check line count
LINES=$(wc -l < "${SKILL_DIR}/SKILL.md")
if [ "$LINES" -gt 500 ]; then
  echo "WARN: SKILL.md is ${LINES} lines (recommended max: 500). Move detail to references/."
fi

# 7. Check for referenced files that don't exist
grep -oE '\{baseDir\}/[^ )"]+' "${SKILL_DIR}/SKILL.md" | while read -r ref; do
  REAL_PATH="${SKILL_DIR}/${ref#{baseDir}/}"
  if [ ! -f "$REAL_PATH" ]; then
    echo "WARN: Referenced file not found: ${ref} -> ${REAL_PATH}"
  fi
done

echo "PASS: Skill structure is valid."
```

---

## Workflow 5: Restructure / Audit Agent Skill Folders

When the user wants to audit or fix their Codex-first skill setup:

1. **Scan current structure:**

```bash
echo "=== Current agent skill structure ==="
find .codex .agents skills -type f 2>/dev/null | head -50
echo ""
echo "=== Skills found ==="
find .codex/skills .agents/skills skills -name "SKILL.md" 2>/dev/null || echo "No skills directory found"
```

2. **For each SKILL.md found, run validation** (Workflow 4)

3. **Check for common problems:**
   - SKILL.md files not inside a named subfolder
   - Missing AGENTS.md at project root
   - Skills with duplicate names
   - Orphan folders (no SKILL.md inside)

4. **Report findings** and offer to fix issues.

5. **If no Codex skill folder exists, scaffold one:**

```bash
mkdir -p .codex/skills
mkdir -p .agent/playbooks

# Create starter AGENTS.md
cat > AGENTS.md << 'EOF'
# Project Configuration

## Stack
- TODO: List your tech stack

## Commands
- `npm run dev` — Start dev server
- `npm test` — Run tests
- `npm run build` — Production build

## Conventions
- TODO: Add your code style preferences
- TODO: Add your naming conventions

## Notes
- TODO: Add project-specific context for Codex
EOF

echo "Created .codex/skills and starter AGENTS.md"
```

---

## Important Rules

1. **Always validate after install** — run the validation checklist on every new skill
2. **Never overwrite without asking** — if a skill folder already exists, confirm before replacing
3. **Quote all descriptions** — use double quotes around description values as a default habit
4. **Keep SKILL.md lean** — under 500 lines, use references/ for depth
5. **Test the trigger** — after installing, suggest the user try a prompt that should activate the skill
6. **Preserve existing structure** — when restructuring, don't delete files without confirmation
7. **Handle both project-local and global installs** — ask the user which scope they want:
   - Project: `./.codex/skills/` or `./.agents/skills/`
   - Global: `~/.codex/skills/`
   - Hermes: the configured Hermes skills path, commonly under `~/.hermes/skills/`

---

## Error Handling

- **Git clone fails:** Check if URL is valid, suggest HTTPS vs SSH
- **No SKILL.md in source:** The source isn't a valid AgentSkills package — offer to create one from the content
- **YAML parse error:** Almost always unquoted special characters in description — auto-fix by quoting
- **Skill doesn't trigger:** Check description keywords match what users would actually say
- **Skill triggers but fails:** Check that referenced scripts/files exist and are executable
