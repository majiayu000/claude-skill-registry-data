---
name: playwright
description: Browser automation scripts for testing, screenshots, and web interaction. 16 scripts with persistent state.
---

# Playwright Skill

Browser automation with persistent state between commands.

## Setup

```bash
cd .claude/skills/playwright/scripts
npm install && npm run install-browsers
```

## Scripts

All in `.claude/skills/playwright/scripts/`:

**Navigation**: `navigate.js <url>`, `go-back.js`, `go-forward.js`

**Discovery**: `snapshot.js` - Get element refs (run first)

**Interaction**: `click.js <ref>`, `hover.js <ref>`, `type.js <text> [ref]`, `select-option.js <ref> <value>`, `press-key.js <key>`

**Forms**: `fill-form.js <json>`

**Wait**: `wait.js <ms>`, `wait-for.js <selector> [timeout]`

**Capture**: `screenshot.js [file] [--full]`, `pdf-save.js [file]`

**Utility**: `evaluate.js <script>`, `close.js`, `generate-test.js [name]`

## Basic Workflow

```bash
node navigate.js "http://localhost:5173"
node snapshot.js          # Get refs: ref1, ref2...
node click.js ref1        # Use refs from snapshot
node type.js "text" ref2
node screenshot.js "out.png"
node close.js             # Always close when done
```

## Key Concepts

**Refs**: `snapshot.js` returns `[ref=ref1]` markers. Use these in subsequent commands. **Refs expire on page changes** - run snapshot again.

**State**: Browser stays open between commands. `close.js` clears state.

**Output**: All scripts return JSON: `{"success": true, "data": {...}}`

## Documentation

- [EXAMPLES.md](docs/EXAMPLES.md) - Complete workflow examples
- [TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) - Common issues and fixes
- [ARCHITECTURE.md](docs/ARCHITECTURE.md) - Technical details
- [scripts/README.md](scripts/README.md) - Quick reference

## Limitations

- Single browser instance at a time
- Refs expire on DOM changes
- Browser opens visually (not headless)
