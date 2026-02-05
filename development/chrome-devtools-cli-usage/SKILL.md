---
name: chrome-devtools-cli-usage
description: Complete guide for Chrome DevTools CLI - browser automation, debugging, performance analysis, network inspection. Use when automating Chrome, taking screenshots, analyzing performance, monitoring network/console, device emulation, or user mentions chrome-devtools, browser automation, puppeteer, debugging, performance testing, screenshot, network monitoring, console monitoring, or 크롬 개발자도구, 브라우저 자동화, 디버깅, 성능 분석.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, AskUserQuestion
version: 1.0.0
lastUpdated: 2025-11-08
---

# Chrome DevTools CLI Usage Guide

**chrome-devtools-cli** provides command-line control of Chrome browsers for automation, debugging, and performance analysis. Perfect for developers, scripts, and CI/CD pipelines.

## Quick Installation

```bash
# Homebrew (macOS/Linux)
brew install pleaseai/tap/chrome-devtools-cli

# Quick install script (auto-detects platform)
curl -fsSL https://raw.githubusercontent.com/pleaseai/chrome-devtools-cli/main/install.sh | bash

# npm/Bun
npm install -g @pleaseai/chrome-devtools-cli
```

> **Detailed installation**: See [references/INSTALLATION.md](references/INSTALLATION.md)

## Quick Start

### Basic Navigation

```bash
# Open a new page
chrome-devtools nav new-page --url https://example.com

# Navigate current page
chrome-devtools nav navigate --url https://google.com

# List all pages
chrome-devtools nav list-pages
```

### Screenshots

```bash
# Standard screenshot
chrome-devtools debug screenshot --path screenshot.png

# Full page screenshot
chrome-devtools debug screenshot --path screenshot.png --full-page
```

### Performance Analysis

```bash
# Quick performance analysis
chrome-devtools perf analyze --url https://example.com --format json
```

### Network Monitoring

```bash
# Start monitoring
chrome-devtools network start-monitoring

# List requests (TOON format for 58.9% token reduction)
chrome-devtools network list-requests --format toon
```

## Essential Commands

### Input Automation

```bash
# Click element
chrome-devtools input click --uid <element-uid>

# Fill input
chrome-devtools input fill --uid input-email --value "user@example.com"

# Press keys
chrome-devtools input press-key --key Enter

# Handle dialogs
chrome-devtools input handle-dialog --action accept
```

### Page Navigation

```bash
# Create new page
chrome-devtools nav new-page --url <url>

# Wait for element
chrome-devtools nav wait-for --selector "#element"

# Wait for text
chrome-devtools nav wait-for --text "Welcome"
```

### Device Emulation

```bash
# Emulate device
chrome-devtools emulate device --name "iPhone 13"

# Custom viewport
chrome-devtools emulate resize --width 1920 --height 1080
```

### Debugging

```bash
# Start console monitoring
chrome-devtools debug start-console-monitoring

# List console messages
chrome-devtools debug list-console --types error,warning

# Evaluate JavaScript
chrome-devtools debug evaluate --script "document.title"

# Take screenshot
chrome-devtools debug screenshot --path screenshot.png --full-page
```

### Performance

```bash
# Start trace
chrome-devtools perf start-trace

# Stop trace
chrome-devtools perf stop-trace --output trace.json

# Automated analysis
chrome-devtools perf analyze --url <url> --duration 10000 --format json
```

### Network

```bash
# Start monitoring
chrome-devtools network start-monitoring

# List requests
chrome-devtools network list-requests --format toon

# Get request details
chrome-devtools network get-request --id <request-id>

# Clear history
chrome-devtools network clear
```

## Global Options

Available on all commands:

```bash
chrome-devtools [options] <command> [command-options]
```

**Connection:**

- `--browser-url <url>` - Connect to existing Chrome instance
- `--ws-endpoint <endpoint>` - WebSocket endpoint

**Browser:**

- `--headless` - Run without GUI
- `--isolated` - Temporary profile
- `--channel <channel>` - Chrome channel (stable, beta, dev, canary)

**Output:**

- `--format <format>` - json, toon, or text (default)

**Display:**

- `--viewport <size>` - Initial viewport (e.g., 1280x720)

> **Complete options**: See [references/COMMANDS.md](references/COMMANDS.md)

## Output Formats

### Text (Default)

Human-readable console output.

### JSON

Standard JSON for programmatic use.

### TOON (Token-Optimized)

58.9% token reduction vs JSON - ideal for LLM workflows.

```bash
chrome-devtools network list-requests --format toon
```

## Common Workflows

### Complete Automation

```bash
# Start monitoring
chrome-devtools debug start-console-monitoring
chrome-devtools network start-monitoring

# Navigate and interact
chrome-devtools nav new-page --url https://example.com
chrome-devtools input fill --uid input-email --value "user@example.com"
chrome-devtools input click --uid button-submit

# Capture results
chrome-devtools debug screenshot --path result.png
chrome-devtools network list-requests --format toon

# Cleanup
chrome-devtools close
```

### CI/CD Integration

```bash
#!/bin/bash
# Headless browser testing

chrome-devtools --headless nav new-page --url https://staging.example.com
chrome-devtools --headless debug screenshot --path ci-screenshot.png
chrome-devtools --headless perf analyze --url https://staging.example.com --format json > perf.json
chrome-devtools close
```

### Mobile Testing

```bash
# Test on different devices
chrome-devtools emulate device --name "iPhone 13"
chrome-devtools nav new-page --url https://example.com
chrome-devtools debug screenshot --path mobile-iphone.png

chrome-devtools emulate device --name "iPad Pro"
chrome-devtools nav navigate --url https://example.com
chrome-devtools debug screenshot --path mobile-ipad.png
```

> **More workflows**: See [references/WORKFLOWS.md](references/WORKFLOWS.md)

## Advanced Usage

### Connect to Existing Chrome

```bash
# Start Chrome with remote debugging
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --remote-debugging-port=9222 \
  --user-data-dir=/tmp/chrome-profile

# Connect via CLI
chrome-devtools --browser-url http://127.0.0.1:9222 nav list-pages
```

### Headless Mode

```bash
chrome-devtools --headless --viewport 1920x1080 nav new-page --url https://example.com
```

### Programmatic API

```typescript
import { closeBrowser, navigatePage, takeScreenshot } from '@pleaseai/chrome-devtools-cli'

await navigatePage({ url: 'https://example.com' })
await takeScreenshot({ path: 'screenshot.png', fullPage: true })
await closeBrowser()
```

> **Advanced features**: See [references/ADVANCED-USAGE.md](references/ADVANCED-USAGE.md)

## Key Features

- **Input Automation** - Click, hover, fill forms, keyboard, drag-drop
- **Navigation** - Multi-page management, URL navigation, wait conditions
- **Emulation** - Device emulation, viewport resizing
- **Performance** - Trace recording, performance analysis
- **Network** - Request monitoring and inspection
- **Debugging** - Console monitoring, JavaScript evaluation, screenshots
- **Multiple Formats** - JSON, TOON (58.9% token reduction), text
- **Flexible Connection** - Launch new or connect to existing Chrome

## Requirements

- Node.js v20.19+ (LTS)
- Chrome stable version
- npm or Bun

## Architecture

Built on [Puppeteer](https://pptr.dev/) with CLI framework and output formatting utilities.

## Tips and Best Practices

1. **Use TOON format** for LLM workflows (58.9% token reduction)
2. **Start monitoring before navigation** to capture all requests
3. **Use headless mode** for CI/CD pipelines
4. **Use isolated mode** for reproducible tests
5. **Connect to existing Chrome** for debugging live instances

## Reference Documentation

- [Installation Guide](references/INSTALLATION.md) - All installation methods
- [Commands Reference](references/COMMANDS.md) - Complete command documentation
- [Advanced Usage](references/ADVANCED-USAGE.md) - Advanced features and patterns
- [Common Workflows](references/WORKFLOWS.md) - Practical workflow examples

## Resources

- [GitHub Repository](https://github.com/pleaseai/chrome-devtools-cli)
- [npm Package](https://www.npmjs.com/package/@pleaseai/chrome-devtools-cli)
- [Chrome DevTools MCP](https://github.com/ChromeDevTools/chrome-devtools-mcp)
- [Puppeteer Docs](https://pptr.dev/)

---

**Version**: 1.0.0
**Author**: Minsu Lee ([@amondnet](https://github.com/amondnet))
**License**: MIT
