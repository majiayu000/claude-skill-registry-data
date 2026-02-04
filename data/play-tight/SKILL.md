---
name: play-tight
description: Context-efficient browser automation using Playwright scripts and subagent isolation. Use when you need to interact with web pages, extract data from websites, verify page elements, or automate browser tasks while avoiding context window pollution from verbose HTML/accessibility trees. Provides both direct script execution and a specialized subagent pattern for complex investigations that generate large intermediate responses.
---

# Play-Tight

Play-Tight provides context-efficient browser automation using Playwright scripts executed via bash, with an optional subagent pattern for isolating verbose browser responses. The skill replaces the verbose Playwright MCP server with optimized scripts and subagent patterns to minimize context window pollution, saving context for actual engineering processes.

## When to Use This Skill

Use Play-Tight when you need to:
- Verify elements exist on web pages (buttons, forms, links)
- Extract text content or structured data from websites
- Check status of web dashboards (CI/CD, monitoring, PRs)
- Take screenshots of pages or specific elements
- Automate repetitive browser tasks
- Validate web application behavior

## Automatic Browser Detection

**IMPORTANT**: Before using any Playtight script, automatically check if Playwright browsers are installed.

### Detection Process

1. **Check for browser installation** by running:
```bash
node -e "const { chromium } = require('playwright'); chromium.executablePath()" 2>&1
```

2. **If the check fails** (exit code non-zero or error message):
   - Inform the user that Playwright browsers need to be installed
   - Offer to run the installation: "I can install the required browsers by running `npm run install-browsers` in the scripts directory. Would you like me to do that?"
   - If user agrees, run:
   ```bash
   cd ~/.claude/plugins/mad-skills/play-tight/scripts && npm run install-browsers
   ```

3. **If npm dependencies are missing** (error about 'playwright' module not found):
   - First install npm dependencies: `cd ~/.claude/plugins/mad-skills/play-tight/scripts && npm install`
   - Then install browsers: `npm run install-browsers`

### Example Detection Flow

```bash
# First attempt to use a script
node scripts/check-element.js https://example.com h1

# If error mentions "browserType.launch: Executable doesn't exist"
# Or "Cannot find module 'playwright'"

# Then detect and offer installation:
"I see that Playwright browsers aren't installed yet. I can install them now by running 'npm run install-browsers'. This will download Chromium (~100MB). Would you like me to proceed?"

# On user approval:
cd ~/.claude/plugins/mad-skills/play-tight/scripts && npm install && npm run install-browsers
```

**When to skip detection**: If you've already successfully run a Play-Tight script in the current session, browsers are installed and you can skip detection.

## Two Approaches

### Approach 1: Direct Script Execution (Simple Tasks)

For straightforward tasks where responses are compact, use scripts directly:

```bash
node scripts/check-element.js <url> <selector>
node scripts/get-text.js <url> [selector]
node scripts/take-screenshot.js <url> <output-path> [selector]
```

**Use when:**
- Single element check
- Quick text extraction
- Simple verification
- Parent context has room

### Approach 2: Subagent Isolation (Complex Tasks)

For tasks requiring multiple iterations or verbose exploration, delegate to the browser-investigator subagent:

```bash
# In parent agent
"Use browser-investigator subagent to find all login form elements on example.com"
```

**Use when:**
- Multiple exploration steps needed
- Large HTML responses expected
- Complex element discovery
- Parent context is precious

## Available Scripts

### check-element.js
Check if an element exists and get its properties.

**Usage:**
```bash
node scripts/check-element.js https://example.com "#login-button"
```

**Returns:**
```json
{
  "found": true,
  "tagName": "BUTTON",
  "text": "Sign In",
  "visible": true,
  "enabled": true,
  "attributes": {
    "id": "login-button",
    "class": "btn btn-primary",
    "type": "submit"
  }
}
```

**Key features:**
- Text limited to 100 chars to prevent context flooding
- Only essential attributes extracted (id, class, type, href, value)
- Visibility and enabled state checked
- 30s timeout for page load

### get-text.js
Extract text content from element or entire page.

**Usage:**
```bash
# From specific element
node scripts/get-text.js https://example.com ".main-content"

# From entire page
node scripts/get-text.js https://example.com
```

**Returns:**
```json
{
  "found": true,
  "text": "extracted text content...",
  "length": 1523,
  "truncated": false
}
```

**Key features:**
- Auto-truncates to 2000 chars to prevent context flooding
- Extracts only visible text (excludes hidden, script, style tags)
- Selector optional - defaults to entire page body
- Whitespace normalized

### take-screenshot.js
Capture page or element screenshot.

**Usage:**
```bash
# Full page
node scripts/take-screenshot.js https://example.com output.png

# Specific element
node scripts/take-screenshot.js https://example.com output.png "#dashboard"
```

**Returns:**
```json
{
  "success": true,
  "path": "/absolute/path/to/output.png",
  "url": "https://example.com",
  "selector": "full-page"
}
```

**Key features:**
- Full page or specific element
- Returns file path for evidence
- Keeps response compact by saving to disk

### navigate-and-extract.js
Extract structured data using configuration.

**Usage:**
```bash
node scripts/navigate-and-extract.js "https://example.com" '{
  "waitFor": ".content",
  "selectors": {"title": "h1", "description": ".desc"},
  "counts": {"items": ".list-item"},
  "checks": {"has_error": ".error-message"}
}'
```

**Config format:**
- `waitFor` (optional): Selector to wait for before extracting
- `selectors`: Map of names to selectors for text extraction (200 char limit per field)
- `counts`: Map of names to selectors for element counting
- `checks`: Map of names to selectors for visibility checks

**Returns:**
```json
{
  "success": true,
  "url": "https://example.com",
  "data": {
    "title": "Page Title",
    "description": "Page description text",
    "items": 5,
    "has_error": false
  }
}
```

**Example:**
```bash
node scripts/navigate-and-extract.js "https://github.com/user/repo/pull/123" '{
  "waitFor": ".merge-status-item",
  "selectors": {"title": ".js-issue-title"},
  "counts": {"total_checks": ".merge-status-item"},
  "checks": {"is_approved": ".review-status.approved"}
}'
```

## Browser Investigator Subagent

For complex tasks that generate verbose intermediate responses, use the browser-investigator subagent.

**Location:** `agents/browser-investigator-subagent.md`

**Purpose:** Execute complex multi-step browser investigations while isolating verbose responses from parent agent.

### Setup

1. Copy the subagent definition to your project:
```bash
cp agents/browser-investigator-subagent.md .claude/agents/
```

2. Ensure scripts are accessible from project root:
```bash
# Either copy scripts to project
cp -r scripts/ ./scripts/

# Or create symlink
ln -s /path/to/skill/scripts ./scripts
```

### Usage Pattern

```bash
# Parent agent delegates task
"Use browser-investigator subagent to check the status of PR #123 on github.com/user/repo"
```

The subagent will:
1. Make multiple script calls to explore the page (5-10+ calls typical)
2. Absorb all verbose HTML/accessibility responses in its context
3. Process and filter the information
4. Return concise structured summary (< 500 tokens) to parent

### Return Format

The subagent always returns structured JSON:

**Element location:**
```json
{
  "type": "element_location",
  "selector": "#login-button",
  "element_type": "button",
  "verification": "element found and visible",
  "attempts": 3
}
```

**Data extraction:**
```json
{
  "type": "data_extraction",
  "extracted_data": {...},
  "data_points": 5,
  "confidence": "high"
}
```

**Verification:**
```json
{
  "type": "verification",
  "status": "success",
  "checks_completed": ["element_exists", "text_matches"],
  "issues": [],
  "screenshot_path": "/path/to/screenshot.png"
}
```

**Status check:**
```json
{
  "type": "status_check",
  "url": "https://example.com",
  "status": {...},
  "summary": "brief description"
}
```

See `agents/browser-investigator-subagent.md` for complete subagent definition.

## Setup Requirements

### First-Time Setup

```bash
# In skill's scripts directory
cd scripts/
npm install
npm run install-browsers
```

This installs Playwright and Chromium browser.

### Project Integration

For projects using this skill:

```bash
# Option 1: Copy scripts to project
cp -r /path/to/skill/scripts ./browser-scripts
cd browser-scripts && npm install && npm run install-browsers

# Option 2: Global installation (if using across multiple projects)
cd /path/to/skill/scripts
npm install -g playwright
playwright install chromium
```

## Common Patterns

See `references/patterns.md` for detailed examples including:
- GitHub PR status checks
- Form field discovery
- Content verification
- CI/CD dashboard monitoring

## Context Efficiency

**Problem**: Browser automation typically floods context with verbose HTML, accessibility trees, and JavaScript. The Playwright MCP server returns 50KB+ HTML accessibility trees per interaction.

**Solution**: Playtight solves it two ways:
1. **Scripts return compact JSON**: Only essential data, no raw HTML
2. **Subagent isolation**: Verbose exploration happens in subagent's context, parent receives summary

### Comparison

**Traditional Playwright MCP:**
```
Query: "Find login form"
Response 1: [30KB HTML tree] = 7,200 tokens
Response 2: [25KB narrowing] = 6,000 tokens
Response 3: [20KB more] = 4,800 tokens
Total: 18,000 tokens, context nearly exhausted
```

**Playtight Direct Scripts:**
```
Query: "Find login form"
Script 1: {found: true, ...} = 150 tokens
Script 2: {found: true, ...} = 150 tokens
Script 3: {found: true, ...} = 150 tokens
Total: 450 tokens in parent context
```

**Playtight with Subagent:**
```
Parent query: "Find login form"
Subagent internally:
  - 10 script calls = 1,500 tokens (isolated in subagent)
Parent receives:
  - {type: "element_location", elements: {...}} = 80 tokens
Total in parent: 80 tokens
```

**Result:** 225x more efficient, enabling 100+ queries vs 2-3 with MCP

## Best Practices

1. **Use subagent for exploration**: When you need multiple iterations to find elements, delegate to browser-investigator
2. **Direct scripts for known targets**: When you know exact selectors, use scripts directly
3. **Batch extractions**: Use navigate-and-extract for multiple data points
4. **Error handling**: Always check `success`, `found`, or `error` fields in responses
5. **Screenshot for evidence**: When reporting issues, take screenshots and save to file
6. **Context preservation**: Keep parent agent context clean for engineering work

## Critical Design Principles

When modifying or extending this skill:

1. **Never Return Raw HTML** - Always return structured JSON with specific fields
2. **Truncate Everything** - Text: 100-2000 chars, errors: 100 chars
3. **Keep Responses Compact** - Target < 500 bytes per script response
4. **Filter at Source** - Extract only essential data in the script
5. **Use Subagent for Verbosity** - Complex exploration happens in isolated context
6. **Headless by Default** - All scripts use headless: true for performance
7. **Timeout Protection** - 30s page load timeout, avoid hangs

## Troubleshooting

### Browser not found / "Executable doesn't exist"
This should be automatically detected (see "Automatic Browser Detection" section above). If you encounter this error:

1. Check if npm dependencies are installed:
```bash
cd ~/.claude/plugins/mad-skills/play-tight/scripts
npm list playwright
```

2. If playwright is missing, install dependencies:
```bash
npm install
```

3. Install browsers:
```bash
npm run install-browsers
```

The automatic detection should offer to do this for you when you first use the skill.

### Script errors
Check that Playwright is installed: `npm list playwright` in the scripts directory

### Element not found
- Verify selector is correct
- Try get-text.js to see page content
- Take screenshot to visually inspect
- Use waitFor in navigate-and-extract config

### Timeout errors
Increase timeout or check network connectivity. Scripts use 30s default timeout for page loads.
