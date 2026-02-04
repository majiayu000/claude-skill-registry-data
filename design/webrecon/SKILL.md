---
name: webrecon
description: WebRecon - reconnaissance tool using parallel Chrome instances for competitive analysis, design extraction, and API discovery
---

# WebRecon

## Overview

This skill provides the methodology for conducting comprehensive website audits using 6 parallel Chrome instances. Each instance is controlled by a specialized agent that focuses on a specific aspect of the audit.

## When to Use

- Competitive analysis of websites
- Design replication prep (extracting design tokens, components, assets)
- API/programmatic access discovery
- Tech stack reconnaissance
- Mobile responsiveness analysis
- SEO and security assessment

## Prerequisites

Before running `/webrecon`:

1. **Launch Chrome instances**: Run `~/.config/opencode/launch-chrome-instances.sh`
2. **Verify Chrome is ready**: Script will confirm all 6 ports responding
3. **Optional**: Set `FIRECRAWL_API_KEY` in environment for better page enumeration

## Command Usage

```bash
# Quick recon (10 pages)
/webrecon quick example.com

# Deep recon (25 pages)
/webrecon deep example.com

# Design-focused (15 pages, skips SEO/security)
/webrecon design example.com

# With options
/webrecon deep example.com --exclude=api
/webrecon deep example.com --max-pages=50
/webrecon deep example.com --design-deep    # Full component/asset extraction
/webrecon --resume                          # Resume interrupted run
```

## Execution Flow

### Phase 0: Setup
1. Create output directory: `~/webrecon-output/<domain>/<timestamp>/`
2. Initialize state file for resumability
3. Verify Chrome instances are running
4. Load filter config from `~/.config/opencode/webrecon-filters.yaml`
5. Check for previous run (for diff computation)

### Phase 1: Page Enumeration

**Fallback chain:**
1. Try `sitemap.xml` (free, instant)
2. Try Firecrawl API if `FIRECRAWL_API_KEY` set
3. Fallback: Jina Reader (`https://r.jina.ai/<url>`) + browser link crawl

**Filtering:**
- Exclude: `/blog/*`, `/docs/*`, `/legal/*`, `/changelog/*`, `/tag/*`, pagination
- Keep everything else, cap by mode: quick=10, deep=25, design=15

### Phase 2: Parallel Analysis

Dispatch 6 agents simultaneously:

| Chrome | Agent | Focus |
|--------|-------|-------|
| chrome-1 | audit-recon | Tech stack, third-party scripts, pixels, GTM |
| chrome-2 | audit-design | CSS tokens, typography, colors, components |
| chrome-3 | audit-api | Endpoints, auth flow, WebSocket, rate limits |
| chrome-4 | audit-mobile | Viewports, touch targets, responsive layouts |
| chrome-5 | audit-seo | Meta tags, OpenGraph, Schema.org, headings |
| chrome-6 | audit-security | HTTP headers, cookies, CSP, exposed source maps |

Each agent:
- Processes assigned URLs one at a time
- Writes results to disk immediately (context hygiene)
- Updates `.state/progress.json`
- Returns summary only

### Phase 2.5: Design Deep (if --design-deep)

Sequential extended extraction on chrome-2:
1. Component inventory with HTML/CSS snippets
2. Asset harvesting (icons, fonts, logos)
3. Motion capture (animations, transitions)
4. Multi-format export (Style Dictionary, Figma Tokens, Tailwind config)

### Phase 3: PWA Check

Quick check for Progressive Web App capabilities:
- Fetch `/manifest.json`
- Detect service worker
- Test offline capability

### Phase 4: Authenticated Audit (Optional)

If user wants to audit logged-in state:
1. Open chrome-1 to login page
2. Prompt: "Log in manually, then type 'done'"
3. Capture session cookies
4. Inject into other Chrome instances
5. Re-run audit-recon and audit-api in auth mode

### Phase 5: Diff Computation

If previous run exists:
1. Load previous `structured/*.json` files
2. Compare: tech-stack, api-map, design-tokens
3. Generate: `changelog/diffs/<timestamp>.json`
4. Append to: `changelog/history.jsonl`

### Phase 6: Compile Output

Generate final deliverables:
- `_manifest.json` - Run metadata + change summary
- `report.md` - Human-readable executive summary
- `structured/` - All JSON exports
- `screenshots/` - Key page screenshots
- `network/` - HAR archive + endpoints
- `assets/` - If --design-deep (components, icons, fonts)
- `exports/` - If --design-deep (Style Dictionary, Figma, Tailwind)

## Output Structure

```
~/webrecon-output/
└── example.com/
    ├── changelog/
    │   ├── history.jsonl           # Append-only event log
    │   └── diffs/
    │       └── 2024-12-25_143022.json
    │
    ├── 2024-12-25_143022/          # This run
    │   ├── _manifest.json
    │   ├── report.md
    │   ├── structured/
    │   │   ├── tech-stack.json
    │   │   ├── design-tokens.json
    │   │   ├── api-map.json
    │   │   ├── seo-data.json
    │   │   ├── security-report.json
    │   │   └── ...
    │   ├── screenshots/
    │   ├── network/
    │   ├── assets/                 # If --design-deep
    │   └── exports/                # If --design-deep
    │
    └── latest -> 2024-12-25_143022  # Symlink
```

## Context Management

**Problem**: Long-running agents can bloat context with network data, screenshots, DOM trees.

**Solution**: Chunked processing + structured handoffs

- Orchestrator holds URL list only, not page content
- Sub-agents process ONE page at a time
- Write findings to disk IMMEDIATELY
- Clear page-specific context before next page
- Return summary only (not full data)

**Resumability**: If interrupted, `/webrecon --resume` reads `.state/progress.json` and continues from last completed page.

## Chrome DevTools MCP Reference

Key tools available:

**Navigation:**
- `navigate_page` - Go to URL
- `new_page` / `close_page` - Tab management
- `list_pages` / `select_page` - Multi-tab handling

**Inspection:**
- `take_screenshot` - Capture page
- `take_snapshot` - Get DOM/accessibility tree
- `evaluate_script` - Run JavaScript

**Network:**
- `list_network_requests` - Get all requests
- `get_network_request` - Get request/response details

**Performance:**
- `performance_start_trace` / `performance_stop_trace` - Record traces
- `performance_analyze_insight` - Get performance insights

## Best Practices

1. **Run Chrome launcher first**: Always start Chrome instances before auditing
2. **Use appropriate mode**: `quick` for rapid checks, `deep` for thorough analysis
3. **Design-deep for replication**: Use `--design-deep` when you need to recreate the design
4. **Check diffs**: Use `/webaudit diff` to track changes over time
5. **Review filtered pages**: Customize include/exclude if defaults miss important pages
