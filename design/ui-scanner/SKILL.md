---
name: ui-scanner
description: >
  Skill for analyzing a project's existing UI in Vue. Activates when the user
  uses /pwdev-uiux:scan or asks to "analyze the project UI", "map existing
  components", "understand project patterns", or "create project skill".
  Generates .planning/ui/project-ui-skill.md with project-specific patterns and tokens.
context: fork
agent: Explore
---

# Skill: UI Scanner

This skill analyzes the project's existing UI and generates a project-specific
contextual skill to guide new development.

## When to use

- Before starting development on an existing project (`/pwdev-uiux:scan`)
- When the ui-builder needs real project context
- For consistency auditing of the existing design system
- To map what exists before deciding what to build

## What it produces

Generates `.planning/ui/project-ui-skill.md` — contextual skill with:
- Confirmed Vue stack and actual versions
- Project custom CSS tokens
- Inventory of installed shadcn-vue components
- Mapped product components
- Identified code patterns (SFC style, form pattern, etc.)
- Naming conventions
- Visual observations (when browser is available)
- Inconsistencies to avoid repeating

## Execution protocol

### Step 1 — Verify project structure

```bash
# Directory structure
find . -maxdepth 3 -type d | grep -v node_modules | grep -v .git | sort

# Installed stack
cat package.json | python3 -m json.tool 2>/dev/null | grep -A2 '"dependencies"'
```

### Step 2 — Analyze components

```bash
# Total SFCs
find . -name "*.vue" | grep -v node_modules | wc -l

# Installed shadcn-vue components
ls components/ui/ 2>/dev/null || ls src/components/ui/ 2>/dev/null

# Product components (sample)
find components/ src/components/ -name "*.vue" 2>/dev/null | \
  grep -v "/ui/" | head -20

# Read 3-5 representative components to understand patterns
```

### Step 3 — Extract tokens

```bash
# globals.css or app.css or assets/
find . -name "*.css" | grep -v node_modules | xargs grep "^--" 2>/dev/null | head -40

# tailwind.config
cat tailwind.config.ts 2>/dev/null || cat tailwind.config.js 2>/dev/null
```

### Step 4 — Check browser (if available)

```bash
# Dev server running?
PORT=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:3000 2>/dev/null)
PORT5173=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:5173 2>/dev/null)
echo "3000: $PORT, 5173: $PORT5173"
```

If accessible, analyze visually via WebFetch.

### Step 5 — Generate skill

Write result to `.planning/ui/project-ui-skill.md` following the template
documented in the `ui-scanner` agent.

## Usage example

```
/pwdev-uiux:scan                    # Scan current project
/pwdev-uiux:scan http://localhost:3000/dashboard  # Focus on a specific route
/pwdev-uiux:scan --visual-only      # Visual analysis only (no code)
/pwdev-uiux:scan --code-only        # Code analysis only (no browser)
```

## Expected output

```
✅ UI Scanner completed

Project: [name]
Vue Components: 47
shadcn-vue installed: 18/58 available
Custom tokens found: 12
Patterns identified: script setup TS, vee-validate, composables per feature

Skill generated at: .planning/ui/project-ui-skill.md
The ui-builder will use this skill as a reference for new components.

Next step: /pwdev-uiux:start "description of the new feature"
```
