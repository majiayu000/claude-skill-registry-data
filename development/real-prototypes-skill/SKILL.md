---
name: real-prototypes-skill
description: Capture an existing web platform's visual design and generate feature prototypes that match its style. Use when a product manager or developer wants to prototype a new feature for an existing platform.
allowed-tools: Bash(agent-browser:*), Bash(npm:*), Bash(npx:*), Bash(mkdir:*), Bash(node:*)
---

## Quick Start (Talk to Claude)

**Just tell Claude what you want:**

> "I want to prototype a chatbot for salesforce.com"

Claude will automatically:
1. Capture the platform's design
2. Extract colors, fonts, and components
3. Generate a Next.js prototype
4. Start a dev server
5. Open it in your browser

**Then describe your feature:**

> "Add a chatbot to the bottom-right of the homepage"

Claude adds it and hot-reloads your browser.

**That's it - 2-3 exchanges to see a working prototype.**

---

### Quick Start Commands

```bash
# One command does everything
node cli.js quickstart --url https://your-platform.com

# With auto-login (if platform requires authentication)
node cli.js quickstart --url https://your-platform.com --email user@example.com --password secret

# Start/restart the dev server
node cli.js serve --project my-app

# Add a feature (conversational)
node cli.js add-feature --project my-app --page homepage --description "chatbot widget"
```

---

### If You Need Login Credentials

Add to your project's `CLAUDE.md`:

```yaml
platform:
  url: https://your-platform.com
  email: your@email.com
  password: your-password
```

Or just tell Claude: "The email is x@y.com and password is abc"

---

### Auto-Login

If your CLAUDE.md has `email` and `password`, Claude will:
1. Detect login pages automatically
2. Fill in credentials
3. Submit and wait for redirect
4. Then capture the authenticated pages

No manual login needed!

---

## Enterprise Platforms (Salesforce, SAP, ServiceNow, etc.)

The prototype is a **visual mockup** that:
- Matches the platform's exact look and feel
- Uses realistic mock data
- Shows how your feature would appear
- Can be demoed to stakeholders

It does NOT require:
- Platform-specific code (Apex, ABAP, etc.)
- Real API connections
- Production credentials

**Perfect for:** Getting stakeholder approval before building the real thing.

---

## MANDATORY: EXTEND EXISTING PLATFORMS ONLY

**This skill adds features to EXISTING platforms. It does NOT create new designs.**

### Before ANY code generation, these MUST exist:
- `references/design-tokens.json` - Captured colors from existing platform
- `references/manifest.json` - Captured pages from existing platform
- `references/screenshots/` - Visual references from existing platform

### If captures don't exist:
**STOP** - Do not proceed with code generation
Run capture on the existing platform first:
```bash
node cli.js capture --project <name> --url <PLATFORM_URL>
```
NEVER create new designs, colors, or layouts from scratch

### If prototype already exists:
Use **EXTEND MODE** - Modify existing files only
NEVER replace or recreate existing pages

### CLI Enforcement:
- `new` command requires `--force-create` flag (blocks by default)
- `generate` command runs pre-flight check (blocks if captures missing)
- `plan` command validates captures exist before generating plan

---

## ⛔ MANDATORY WORKFLOW - NO SHORTCUTS

**BLOCKING REQUIREMENTS - You will be STOPPED if you skip these:**

### Before Writing ANY Prototype Code:

1. **MUST** run: `node cli.js extract-lib --project <name>`
   - This parses HTML and creates `registry.json`
   - Generation is BLOCKED without this file

2. **MUST** run: `node cli.js convert --project <name> --page <page>`
   - Converts captured HTML to React components
   - Shows exact DOM structure to replicate

3. **MUST** read the screenshot file using the Read tool
   - Not glance - actually READ and list every visible element
   - Use the Read tool on: `projects/<name>/references/screenshots/<page>.png`

4. **MUST** read the captured HTML file
   - File location: `projects/<name>/references/html/<page>.html`

5. **MUST** create element inventory:
   - Run: `node cli.js inventory --project <name> --page <page>`
   - Complete the generated `element-inventory.md`

6. **MUST** complete generation checklist:
   - Run: `node cli.js checklist --project <name> --page <page>`
   - All required steps must be marked complete

### ❌ NEVER:
- Build from memory or general knowledge
- Skip the `extract-lib` command
- Skip reading the captured HTML
- Assume you know what the page looks like
- Create colors not in `design-tokens.json`
- Use Tailwind default colors (bg-blue-500, etc.)
- Replace existing prototype pages

### After Writing Code:

7. **MUST** run: `node cli.js validate-colors --project <name>`
   - Validates all colors against design tokens

8. **MUST** run: `node cli.js visual-diff --project <name> --page <page>`
   - BLOCKED if similarity < 90%
   - Fix and re-run until passing

---

# Platform Prototype Skill

Enterprise-grade tool for capturing web platforms and generating pixel-perfect prototypes.

---

## Prerequisites

### Automatic Setup (Recommended)
Prerequisites are installed **automatically** the first time you run any capture command (`quickstart`, `capture`, or `pipeline`). The skill will:
1. Install `agent-browser` globally if not present
2. Configure `.claude/settings.json` with required permissions
3. Configure `.claude/settings.local.json` with skill permissions

**No manual setup required!** Just run:
```bash
node cli.js quickstart --url https://your-platform.com
```

### Manual Installation (Optional)
If you prefer to set up manually, run:
```bash
node cli.js install
```

This will:
- Install `agent-browser` globally
- Update `.claude/settings.json` with all agent-browser permissions
- Update `.claude/settings.local.json` with skill permissions

### Required: agent-browser
This skill requires **agent-browser** (v0.9.1+) for browser automation.

`agent-browser` is a **Vercel Labs npm package** for headless browser automation.

**Manual Installation (if auto-setup fails):**
```bash
# Install globally
npm install -g agent-browser

# Download Chromium (required after npm install)
agent-browser install
```

**Verify installation:**
```bash
agent-browser --version  # Should show 0.9.1 or higher
```

### Alternative: Manual Capture
If you can't install `agent-browser`, you can still use this skill by:
1. Manually taking screenshots and saving to `references/screenshots/`
2. Manually saving HTML to `references/html/`
3. Running `node cli.js extract-tokens` to generate design tokens from HTML
4. Then using `generate`, `plan`, and other commands

---

## 🏢 ENTERPRISE PIPELINE - MANDATORY FOR ALL PROTOTYPES

**This pipeline MUST be followed. Validation gates will BLOCK generation if prerequisites are missing.**

```
┌─────────────┐     ┌──────────────┐     ┌──────────┐     ┌──────────────┐     ┌────────┐
│   Capture   │ ──▶ │ Validate Pre │ ──▶ │ Generate │ ──▶ │ Validate Out │ ──▶ │ Output │
│  (ALL pages │     │    (GATE)    │     │   Code   │     │    (GATE)    │     │  Done  │
│  ALL states)│     │              │     │          │     │              │     │        │
└─────────────┘     └──────────────┘     └──────────┘     └──────────────┘     └────────┘
      │                   │                                      │
      ▼                   ▼                                      ▼
  Captures:           BLOCKS if:                             BLOCKS if:
  - ALL pages         - design-tokens.json missing           - Colors not in tokens
  - ALL tabs          - < 10 colors extracted                - Tailwind defaults used
  - ALL detail views  - No primary color found               - Wrong hex values
  - ALL dropdowns     - Screenshots missing
  - ALL modals        - Detail pages missing
```

---

## CRITICAL: Browser Automation Setup

**BEFORE any capture or screenshot operation, you MUST:**

1. **Invoke the agent-browser skill** using the Skill tool:
   ```
   Skill: agent-browser-skill
   ```

2. **Then use agent-browser commands** for all browser operations:
   ```bash
   agent-browser open <url>           # Navigate to page
   agent-browser snapshot -i          # Get interactive elements
   agent-browser fill @e1 "email"     # Fill form fields
   agent-browser click @e2            # Click buttons
   agent-browser screenshot path.png  # Take screenshots
   ```

3. **Do NOT** attempt to run `node cli.js capture` without first having agent-browser available

**Why this matters:** The capture engine relies on agent-browser commands. Without invoking the agent-browser skill first, screenshot and navigation commands will fail.

---

## Quick Start

### Option 1: Direct Browser Automation (Recommended)

1. **First, invoke agent-browser skill** (required before any browser operations)
2. **Then use browser commands:**

```bash
# Navigate and authenticate
agent-browser open https://app.example.com/login
agent-browser snapshot -i
agent-browser fill @e1 "user@test.com"
agent-browser fill @e2 "password"
agent-browser click @e3
agent-browser wait --url "**/dashboard"

# Capture screenshots
agent-browser screenshot projects/my-app/references/screenshots/dashboard.png
```

### Option 2: CLI Pipeline

**Note:** Requires agent-browser to already be available.

```bash
# Create a new project
node .claude/skills/real-prototypes-skill/cli.js new --project my-app

# Full Pipeline
node .claude/skills/real-prototypes-skill/cli.js pipeline \
  --project my-app \
  --url https://app.example.com \
  --email user@test.com \
  --password secret

# Or Step by Step
node cli.js capture --project my-app --url https://... --email ... --password ...
node cli.js validate --project my-app --phase post-capture
node cli.js validate --project my-app --phase pre-gen
# [Claude generates prototype]
node cli.js validate --project my-app --phase post-gen

# List all projects
node cli.js list
```

## Project Structure

All projects are stored in the `projects/` directory at the repository root:

```
<repository-root>/
└── projects/
    └── <project-name>/
        ├── project.json          # Project metadata
        ├── references/           # Captured platform assets (READ from here)
        │   ├── manifest.json
        │   ├── design-tokens.json
        │   ├── screenshots/
        │   └── html/
        └── prototype/            # Generated prototype (WRITE here)
            ├── src/
            └── package.json
```

### CRITICAL: File Output Location

**ALL generated prototype files MUST be created in:**
```
projects/<project-name>/prototype/
```

**Run `generate` command to see the exact absolute path:**
```bash
node cli.js generate --project <project-name>
```

This will output the full path where prototype files should be created.

---

## Capture Engine

The capture engine automatically discovers and captures:

### Pages
- ✅ Auto-discovers all navigation links
- ✅ Follows list → detail page patterns
- ✅ Captures all tab states
- ✅ Captures dropdown/menu states
- ✅ Multiple viewport sizes (desktop, tablet, mobile)

### Design Tokens
- ✅ Extracts ALL colors from HTML
- ✅ Categorizes colors (primary, text, background, border, status)
- ✅ Extracts font families
- ✅ Sorts by usage frequency

### Output
```
projects/<project-name>/references/
├── manifest.json           # All pages with metadata
├── design-tokens.json      # Extracted colors & fonts
├── screenshots/
│   ├── accounts-list-desktop.png
│   ├── account-details-overview-desktop.png
│   ├── account-details-tab-activity.png
│   ├── actions-dropdown.png
│   └── ...
└── html/
    ├── accounts-list.html
    ├── account-details.html
    └── ...
```

---

## Validation Gates

### Gate 1: Post-Capture Validation
Runs after capture, blocks if:
- ❌ Less than 5 pages captured
- ❌ Missing screenshots
- ❌ Less than 10 colors extracted
- ❌ No primary color identified
- ❌ List pages without detail pages

### Gate 2: Pre-Generation Validation
Runs before prototype generation, blocks if:
- ❌ manifest.json missing
- ❌ design-tokens.json missing
- ❌ Required color categories missing (primary, text, background, border)
- ❌ No screenshots available

### Gate 3: Post-Generation Validation
Runs after prototype generation, blocks if:
- ❌ Colors used that aren't in design-tokens.json
- ❌ Tailwind default colors used (e.g., `bg-blue-500`)
- ❌ Missing component files

---

## CLI Commands

### quickstart (RECOMMENDED)
```bash
node cli.js quickstart --url <URL> [options]

One command does everything: capture → extract → scaffold → serve → open browser.

Options:
  --url       Platform URL (required)
  --email     Login email (optional, for auto-login)
  --password  Login password (optional, for auto-login)
  --port      Dev server port (default: 3000)
  --no-open   Don't auto-open browser

Example:
  node cli.js quickstart --url https://salesforce.com --email user@test.com --password secret
```

### serve
```bash
node cli.js serve --project <name> [options]

Start dev server and open browser.

Options:
  --project   Project name (required)
  --port      Dev server port (default: 3000)
  --no-open   Don't auto-open browser
```

### add-feature
```bash
node cli.js add-feature --project <name> --page <page> --description <feature>

Conversational feature injection - describes how to add a feature to a page.

Options:
  --project      Project name (required)
  --page         Target page name (required)
  --description  Feature description (required)

Example:
  node cli.js add-feature --project my-app --page homepage --description "chatbot widget"
```

### new
```bash
node cli.js new --project <name>

Creates a new project with folder structure.
```

### list
```bash
node cli.js list

Lists all projects with their status.
```

### detect
```bash
node cli.js detect --project <name>

Detects existing prototype in project.
- Identifies framework (Next.js, React, Vue, Angular)
- Detects styling approach (Tailwind, CSS modules, etc.)
- Maps captured pages to existing prototype files
- Recommends EXTEND vs CREATE mode
```

### capture
```bash
node cli.js capture --project <name> --url <URL> [options]

Options:
  --project   Project name (required)
  --url       Platform URL (required)
  --email     Login email (or set PLATFORM_EMAIL env var)
  --password  Login password (or set PLATFORM_PASSWORD env var)
  --config    Path to JSON config file
  --mode      auto|manual|hybrid (default: auto)
```

### validate
```bash
node cli.js validate --project <name> --phase <PHASE>

Options:
  --project   Project name (required)
  --phase     Validation phase (required)

Phases:
  pre-capture      Before starting capture
  post-capture     After capture completes
  pre-generation   Before generating prototype
  post-generation  After generating prototype
  all              Run all validations
```

### validate-colors
```bash
node cli.js validate-colors --project <name>

Validates all colors in prototype against design-tokens.json.
- Scans TSX/JSX/CSS files for color values
- Reports violations with line numbers
- Suggests closest matching design token colors
- Flags Tailwind default colors (bg-blue-500, etc.)
```

### convert
```bash
node cli.js convert --project <name> --page <page>

Converts captured HTML to React components.
- Parses HTML using jsdom
- Extracts component tree structure
- Converts to JSX (class→className, for→htmlFor)
- Preserves exact class names and inline styles
- Outputs to prototype/src/components/extracted/
```

### extract-css
```bash
node cli.js extract-css --project <name> --page <page>

Extracts and analyzes CSS from captured HTML.
- Parses <style> tags and inline styles
- Detects styling paradigm (Tailwind, SLDS, Bootstrap, etc.)
- Shows most used CSS classes
- Recommends styling approach for prototype
```

### extract-lib
```bash
node cli.js extract-lib --project <name>

Extracts reusable component library from all captured HTML.
- Identifies common patterns (buttons, cards, inputs, tables)
- Detects component variants (primary, secondary, disabled)
- Generates TypeScript React components
- Creates component registry (registry.json)
- Outputs to prototype/src/components/extracted/
```

### visual-diff
```bash
node cli.js visual-diff --project <name> --page <page>
node cli.js visual-diff --project <name> --list

Compares generated screenshots with reference captures.
- Pixel-level comparison using pixelmatch
- Generates diff images highlighting differences
- Calculates similarity score (target: >95%)
- Use --list to see available reference screenshots
```

### plan
```bash
node cli.js plan --project <name> --feature "description"

Generates implementation plan with exact details.
- Analyzes existing prototype structure
- Specifies EXTEND vs CREATE mode
- Provides exact file paths for modifications
- Includes injection points with selectors
- Lists validation checkpoints
- Outputs plan.json to project directory

Options:
  --feature   Description of feature to implement
  --target    Target page for modification
  --output    Custom output path for plan.json
```

### checklist (MANDATORY)
```bash
node cli.js checklist --project <name> --page <page>

Creates and manages pre-generation checklist.
- Tracks completion of required steps
- Auto-detects completed steps based on file existence
- BLOCKS generation if checklist incomplete
- Outputs generation-checklist.json

Options:
  --page      Page name (required)
  --complete  Mark a step as complete: --complete <step-name>
  --reset     Mark a step as incomplete: --reset <step-name>

Steps tracked:
  - extract-lib: Parse captured HTML
  - convert: Generate React components
  - read-screenshot: Analyze screenshot
  - read-html: Read captured HTML
  - list-all-elements: Create element inventory
```

### inventory (MANDATORY)
```bash
node cli.js inventory --project <name> --page <page>

Creates element inventory template.
- Generates element-inventory.md
- Auto-detects elements from HTML if available
- MUST be completed before code generation
- Forces listing of ALL visible elements

Output: references/element-inventory.md
```

### pipeline
```bash
node cli.js pipeline --project <name> --url <URL> [options]

Runs: capture → validate → generate guidance
```

### init
```bash
node cli.js init [--output <path>]

Creates capture-config.json template
```

---

## Extended Workflow (MANDATORY)

**This workflow MUST be followed. Skipping steps will BLOCK generation.**

### Phase 0: Pre-Implementation
```bash
# 1. Check for existing prototype FIRST
node cli.js detect --project my-app

# 2. Generate implementation plan
node cli.js plan --project my-app --feature "Add health score widget"

# 3. Review plan.json before proceeding
```

### Phase 1: Analysis (MANDATORY)
```bash
# 4. Extract component library from captured HTML (REQUIRED)
node cli.js extract-lib --project my-app

# 5. Analyze CSS patterns
node cli.js extract-css --project my-app --page homepage

# 6. Convert specific pages to React (REQUIRED)
node cli.js convert --project my-app --page account-detail

# 7. Create element inventory (REQUIRED)
node cli.js inventory --project my-app --page account-detail

# 8. Initialize generation checklist (REQUIRED)
node cli.js checklist --project my-app --page account-detail
```

### Phase 2: Implementation
**Before writing ANY code:**
- ✅ Read the screenshot using Read tool
- ✅ Read the captured HTML using Read tool
- ✅ Complete element inventory
- ✅ Mark checklist steps as complete
- ✅ Read the generated plan.json
- ✅ Use EXTEND mode if prototype exists (modify, don't replace)
- ✅ Use ONLY colors from design-tokens.json
- ✅ Match styling approach detected by extract-css

### Phase 3: Validation (MANDATORY)
```bash
# 9. Validate colors
node cli.js validate-colors --project my-app

# 10. Visual comparison (if screenshots available)
node cli.js visual-diff --project my-app --page homepage

# 11. Full validation
node cli.js validate --project my-app --phase post-gen
```

---

## Critical Rules (ENFORCED BY CLI)

### BLOCKING GATES:

| Gate | Blocks If | Command to Fix |
|------|-----------|----------------|
| Pre-Generation | `registry.json` missing | `node cli.js extract-lib --project <name>` |
| Pre-Generation | `design-tokens.json` missing | `node cli.js capture --project <name>` |
| Pre-Generation | `element-inventory.md` missing | `node cli.js inventory --project <name> --page <page>` |
| Pre-Generation | Checklist incomplete | `node cli.js checklist --project <name> --page <page>` |
| Post-Generation | visual-diff similarity < 90% | Fix code, re-run `visual-diff` |
| Post-Generation | Colors not in design-tokens.json | Fix code, re-run `validate-colors` |

### AUTOMATIC FAILURES:
- Building from memory = **INVALID**
- Skipping HTML parsing = **INVALID**
- Missing elements from inventory = **INVALID**
- Using Tailwind default colors = **INVALID**

### NEVER:
1. ❌ Create new design systems or color schemes
2. ❌ Deviate from captured design tokens
3. ❌ Use colors not in design-tokens.json
4. ❌ Create new prototype if one exists (use EXTEND mode)
5. ❌ Replace existing pages - always extend
6. ❌ Introduce new styling paradigms (don't add styled-components if using CSS modules)
7. ❌ Skip the mandatory workflow steps
8. ❌ Generate code without completing the checklist

### ALWAYS:
1. ✅ Run `detect` first to check for existing prototype
2. ✅ Run `extract-lib` to parse captured HTML
3. ✅ Run `inventory` to create element checklist
4. ✅ Run `checklist` to track progress
5. ✅ Run `plan` to get implementation guidance
6. ✅ Parse captured HTML for exact structure
7. ✅ Validate colors against design-tokens.json
8. ✅ Use screenshot for visual reference
9. ✅ Preserve 100% of existing functionality
10. ✅ Match framework and styling of existing code
11. ✅ Insert at exact location specified in plan
12. ✅ Verify visual output matches reference >95%

---

## REQUIRED: Element Inventory

Before writing code, you MUST create an element inventory by:

1. Reading the screenshot with the Read tool
2. Listing EVERY visible element in this format:

```markdown
ELEMENT INVENTORY FOR: <page-name>

HEADER:
- Logo + text
- Navigation items (list each)
- User menu

LEFT COLUMN:
- Section 1 (collapsible)
  - Field 1 + edit icon
  - Field 2 + edit icon
- Section 2 (collapsible)
  - Field 3
  - Field 4

CENTER COLUMN:
- Filters row (icons + text)
- Main content area
- Empty state OR data display

RIGHT COLUMN:
- Widget 1
  - Sub-elements
- Widget 2
  - Sub-elements

FOOTER:
- Footer content
```

**Generation is BLOCKED until this inventory exists and all items are accounted for in the code.**

---

## Configuration

```json
{
  "platform": {
    "name": "My Platform",
    "baseUrl": "https://app.example.com"
  },
  "auth": {
    "type": "form",
    "loginUrl": "/login",
    "credentials": {
      "emailField": "email",
      "passwordField": "password",
      "submitButton": "Sign in"
    }
  },
  "capture": {
    "mode": "auto",
    "maxPages": 100,
    "maxDepth": 5,
    "viewports": [
      { "name": "desktop", "width": 1920, "height": 1080 },
      { "name": "tablet", "width": 768, "height": 1024 },
      { "name": "mobile", "width": 375, "height": 812 }
    ],
    "interactions": {
      "clickButtons": true,
      "clickDropdowns": true,
      "clickTabs": true,
      "clickTableRows": true,
      "clickModals": true
    },
    "exclude": ["/logout", "/delete", "/remove"]
  },
  "validation": {
    "minPages": 5,
    "minColors": 10,
    "requireDetailPages": true,
    "requireAllTabs": true
  }
}
```

---

## For Claude: Prototype Generation Rules

### MANDATORY: Color Usage
```typescript
// ✅ CORRECT: Use exact hex from design-tokens.json
style={{ backgroundColor: "#1c64f2" }}
style={{ color: "#111928" }}
style={{ borderColor: "#e7e7e6" }}

// ❌ WRONG: Tailwind default colors
className="bg-blue-500"
className="text-gray-900"
className="border-gray-200"

// ❌ WRONG: Custom Tailwind colors (may not compile)
className="bg-primary"
className="text-text-heading"
```

### MANDATORY: Before Generating
1. Read `projects/<project>/references/manifest.json` - understand all captured pages
2. Read `projects/<project>/references/design-tokens.json` - get exact colors
3. View screenshots in `projects/<project>/references/screenshots/` - match layout exactly
4. Use ONLY colors from design-tokens.json

### MANDATORY: After Generating
```bash
node .claude/skills/real-prototypes-skill/cli.js validate --project <project> --phase post-gen
```

---

## Checklist: What Gets Captured

### Pages
- [ ] All sidebar/navigation pages
- [ ] All detail pages (click into list items)
- [ ] All tabs within pages
- [ ] All dropdown/menu states
- [ ] All modal dialogs
- [ ] Multiple viewports (if configured)

### Design Tokens
- [ ] Primary color
- [ ] Text colors (primary, secondary, muted)
- [ ] Background colors (white, light, gray)
- [ ] Border colors
- [ ] Status colors (success, error, warning)
- [ ] Font families

### Validation
- [ ] Minimum pages captured
- [ ] All screenshots exist
- [ ] Design tokens extracted
- [ ] List-detail pattern complete
- [ ] All tabs captured

---

## Cross-Platform Notes

**ALWAYS use the `run_in_background` parameter for long-running processes:**

```bash
# ✅ CORRECT - works on all platforms
# Use run_in_background: true in the Bash tool
npx serve -p 3000
# with parameter: run_in_background: true

# ✅ CORRECT - Next.js dev server
npm run dev
# with parameter: run_in_background: true
```

### ❌ WRONG - Do NOT use these:
```bash
# ❌ WRONG - Linux only, doesn't work on Windows
npx serve -p 3000 &

# ❌ WRONG - Windows specific and unreliable
start /b npx serve -p 3000

# ❌ WRONG - PowerShell issues with npx
PowerShell Start-Process npx serve

# ❌ WRONG - Linux timeout syntax
timeout 3 && curl localhost:3000
```

### Platform Detection
Check the platform from environment info before running OS-specific commands:
- `win32` = Windows
- `darwin` = macOS
- `linux` = Linux

**Rule:** When in doubt, use `run_in_background: true` - it's the tool's built-in cross-platform solution.

---

## Troubleshooting

### "Capture missed detail pages"
- Increase `maxDepth` in config
- Enable `clickTableRows` in interactions
- Use `hybrid` mode with manual includes

### "Colors don't match"
- Run post-generation validation
- Use inline styles, not Tailwind classes
- Verify design-tokens.json has correct colors

### "Tailwind colors not working"
- Use inline `style={{ }}` for all colors
- Tailwind custom colors may not compile correctly on Windows/WSL

### "Login failed"
- Check credentials in env vars
- Verify loginUrl in config
- Check for CAPTCHA/2FA
