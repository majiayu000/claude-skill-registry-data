---
name: playwright
description: Browser automation via Playwright MCP through mcporter. Use when you need to navigate pages, extract data, take screenshots, interact with UI elements, or scrape web content. All tools called via mcporter to avoid context pollution.
---

# Playwright (MCPorter)

All tools called via mcporter:

```bash
npx mcporter call playwright.TOOL_NAME [args]
```

## Core Workflow

### Navigate
```bash
npx mcporter call playwright.browser_navigate url:"https://example.com"
```

### Snapshot (preferred for data extraction — better than screenshot)
```bash
npx mcporter call playwright.browser_snapshot
# Save to file to avoid flooding context:
npx mcporter call playwright.browser_snapshot filename:"snapshot.md"
```

### Screenshot
```bash
npx mcporter call playwright.browser_take_screenshot type:png filename:"page.png"
npx mcporter call playwright.browser_take_screenshot type:png fullPage:true filename:"full.png"
```

### Wait for dynamic content
```bash
npx mcporter call playwright.browser_wait_for text:"Loaded"
npx mcporter call playwright.browser_wait_for time:2
```

### Click (use ref from snapshot)
```bash
npx mcporter call playwright.browser_click ref:"e123" element:"Submit button"
```

### Type into field
```bash
npx mcporter call playwright.browser_type ref:"e45" text:"search query" submit:true
```

### Run arbitrary Playwright code
```bash
npx mcporter call playwright.browser_run_code \
  code:"async (page) => { return await page.title(); }"
```

### Evaluate JS in page context
```bash
npx mcporter call playwright.browser_evaluate \
  function:"() => Array.from(document.querySelectorAll('table tr')).map(r => r.innerText)"
```

## Common Patterns

### Scrape table data
```bash
npx mcporter call playwright.browser_navigate url:"https://site.com/data"
npx mcporter call playwright.browser_wait_for time:2
npx mcporter call playwright.browser_snapshot filename:"raw.md"
```

### Login then scrape
```bash
npx mcporter call playwright.browser_navigate url:"https://site.com/login"
npx mcporter call playwright.browser_snapshot
# use refs from snapshot for fields
npx mcporter call playwright.browser_type ref:"REF" text:"user@email.com"
npx mcporter call playwright.browser_type ref:"REF" text:"password" submit:true
npx mcporter call playwright.browser_wait_for text:"Dashboard"
```

### Tab management
```bash
npx mcporter call playwright.browser_tabs action:list
npx mcporter call playwright.browser_tabs action:new
npx mcporter call playwright.browser_tabs action:select index:0
```

### Network inspection
```bash
npx mcporter call playwright.browser_network_requests includeStatic:false
```

## Tool Reference (22 tools)

| Tool | Purpose |
|---|---|
| `browser_navigate` | Go to URL |
| `browser_snapshot` | Accessibility tree (use for data extraction) |
| `browser_take_screenshot` | Visual screenshot |
| `browser_click` | Click element by ref |
| `browser_type` | Type text into element |
| `browser_fill_form` | Fill multiple fields at once |
| `browser_select_option` | Select dropdown option |
| `browser_hover` | Hover over element |
| `browser_drag` | Drag and drop |
| `browser_evaluate` | Run JS in page context |
| `browser_run_code` | Run Playwright code snippet |
| `browser_press_key` | Press keyboard key |
| `browser_wait_for` | Wait for text/element/time |
| `browser_navigate_back` | Browser back |
| `browser_tabs` | List/create/close/select tabs |
| `browser_network_requests` | Inspect network traffic |
| `browser_console_messages` | Get console output |
| `browser_handle_dialog` | Accept/dismiss dialogs |
| `browser_file_upload` | Upload files |
| `browser_resize` | Resize browser window |
| `browser_install` | Install browser (if missing error) |
| `browser_close` | Close browser |

## When to Use

- Frontend UI testing (visible browser by default — no extra config needed)
- Pages requiring JavaScript rendering / SPAs
- Extracting tables/prices from web pages
- Automated form submission and interaction flows
- Screenshots of web pages

## Anti-Patterns

❌ Don't call `browser_snapshot` without `filename:` when output is large — floods context
❌ Don't load playwright MCP in `.claude.json` alongside this skill — mcporter only
❌ Don't add `--headless` to mcporter.json for UI testing — defeats the purpose
