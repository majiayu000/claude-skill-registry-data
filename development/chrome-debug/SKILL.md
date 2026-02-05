---
name: chrome-debug
description: This skill should be used when debugging web applications, diagnosing page errors, inspecting console output, or capturing screenshots of pages. It provides Chrome DevTools Protocol (CDP) automation via the chromectl.py script for collaborative or automated browser debugging.
---

# Chrome Debug

## Overview

This skill enables web application debugging through automated Chrome browser control using the Chrome DevTools Protocol (CDP). Use chromectl.py to launch Chrome instances, inspect pages, monitor console output, execute JavaScript, and capture screenshots—all from the command line.

The skill supports both **collaborative debugging** (visible Chrome window where developer and Claude work together) and **automated debugging** (headless background process for screenshot/console capture).

## When to Use This Skill

Invoke this skill when:
- Debugging web application issues or investigating page errors
- Inspecting browser console for errors, warnings, or log messages
- Capturing screenshots of pages to identify visual problems
- Monitoring page behavior in real-time during development
- Automating page inspection or testing workflows
- Diagnosing JavaScript errors or unexpected page behavior

Do NOT use this skill for:
- General web browsing or information gathering (use WebFetch instead)
- Editing HTML/CSS files directly (this is for runtime inspection only)
- Testing that requires sophisticated user interaction (use proper testing frameworks)

## Critical: Headful vs Headless Mode

**Always consider whether collaborative debugging or automation is needed:**

### Headful Mode (Default - No --headless flag)

```bash
scripts/chromectl.py start
```

**When to use:**
- Collaborative debugging where developer can see and interact with the browser
- Investigating visual issues that require manual inspection
- Complex workflows where developer input is needed
- Real-time troubleshooting sessions

**Benefits:**
- Developer can interact manually while Claude monitors console/inspects state
- Visual feedback for both developer and Claude
- Easier to diagnose UI/layout issues together

### Headless Mode (--headless flag)

```bash
scripts/chromectl.py start --headless
```

**When to use:**
- Automated screenshot capture
- Console monitoring without user interaction
- Batch processing multiple pages
- CI/CD or scripted testing scenarios

**Benefits:**
- No visual window, runs in background
- Faster, lighter weight
- Suitable for automation

**Default choice:** Use headful mode for collaborative debugging unless automation is explicitly needed.

## Debugging Workflows

### Workflow 1: Collaborative Web App Debugging

Use when developer reports errors or unexpected behavior and wants to work together.

```bash
# 1. Start Chrome with visible window
scripts/chromectl.py start

# 2. Open the problematic page
TARGET=$(scripts/chromectl.py open https://myapp.com/problem-page | jq -r .id)

# 3. Start console monitoring in background
scripts/chromectl.py console-tail --id $TARGET --for 60 &

# 4. Take initial screenshot
scripts/chromectl.py screenshot --id $TARGET -o initial-state.png

# 5. Inspect page state using eval
scripts/chromectl.py eval --id $TARGET -e "document.readyState"
scripts/chromectl.py eval --id $TARGET -e "({
  title: document.title,
  errors: window.onerror ? 'Error handler present' : 'No error handler',
  scripts: document.scripts.length
})"

# 6. Developer can now interact with page while Claude monitors console output
# Claude watches console-tail output for errors while developer clicks/navigates

# 7. Clean up when done
scripts/chromectl.py stop
```

### Workflow 2: Automated Screenshot & Console Capture

Use for quick automated inspection without collaboration.

```bash
# 1. Start headless Chrome
scripts/chromectl.py start --headless

# 2. Open page
TARGET=$(scripts/chromectl.py open https://example.com | jq -r .id)

# 3. Wait for page load
sleep 2

# 4. Capture full-page screenshot
scripts/chromectl.py screenshot --id $TARGET -o page.png --full-page

# 5. Check for JavaScript errors via eval
scripts/chromectl.py eval --id $TARGET -e "({
  title: document.title,
  url: location.href,
  readyState: document.readyState,
  hasErrors: typeof window.onerror !== 'undefined'
})"

# 6. Stop Chrome
scripts/chromectl.py stop
```

### Workflow 3: Console Error Monitoring

Use when investigating intermittent errors or monitoring page activity.

```bash
# 1. Start Chrome (headful if developer wants to interact)
scripts/chromectl.py start

# 2. Open target page
TARGET=$(scripts/chromectl.py open https://myapp.com | jq -r .id)

# 3. Start console monitoring for extended period
scripts/chromectl.py console-tail --id $TARGET --for 120 > console-output.log &
TAIL_PID=$!

# 4. While console-tail runs, trigger actions or let developer interact
# Developer can click buttons, navigate, etc. while Claude monitors

# 5. Wait for monitoring to complete
wait $TAIL_PID

# 6. Analyze console-output.log for errors/warnings
grep -E '"console": "(error|warning)"' console-output.log

# 7. Clean up
scripts/chromectl.py stop
```

### Workflow 4: Multiple Page Comparison

Use when comparing behavior across multiple pages or environments.

```bash
# 1. Start Chrome
scripts/chromectl.py start --headless

# 2. Open multiple pages
PROD=$(scripts/chromectl.py open https://app.com/page | jq -r .id)
STAGING=$(scripts/chromectl.py open https://staging.app.com/page | jq -r .id)

# 3. Wait for loads
sleep 3

# 4. Capture screenshots
scripts/chromectl.py screenshot --id $PROD -o prod.png
scripts/chromectl.py screenshot --id $STAGING -o staging.png

# 5. Compare page states
scripts/chromectl.py eval --id $PROD -e "document.querySelector('h1').innerText"
scripts/chromectl.py eval --id $STAGING -e "document.querySelector('h1').innerText"

# 6. Clean up
scripts/chromectl.py stop
```

## JavaScript Evaluation for Debugging

The `eval` command is primarily for Claude's implicit use to inspect and debug page state. Use it to:

**Inspect page state:**
```bash
# Check if page loaded
eval --id $ID -e "document.readyState"

# Get page title and URL
eval --id $ID -e "({title: document.title, url: location.href})"

# Check for global variables
eval --id $ID -e "typeof myAppVariable"

# Inspect DOM elements
eval --id $ID -e "document.querySelector('#error-message')?.innerText"
```

**Debug JavaScript functions:**
```bash
# Check if function exists
eval --id $ID -e "typeof myFunction"

# Call function and inspect result
eval --id $ID -e "myFunction(testData)"

# Inspect object properties
eval --id $ID -e "window.myApp.config"
```

**Trigger page actions (for debugging):**
```bash
# Click element to reproduce error
eval --id $ID -e "document.querySelector('button#submit').click()"

# Scroll to bottom
eval --id $ID -e "window.scrollTo(0, document.body.scrollHeight)"

# Fill form field
eval --id $ID -e "document.querySelector('input#email').value = 'test@example.com'"
```

**Note:** Evaluation supports promises automatically, so async operations work seamlessly.

## Important Reminders

### Always Stop Chrome When Done

```bash
scripts/chromectl.py stop
```

**Critical:** Headless Chrome instances run invisibly and can prevent normal Chrome from launching. Always run `stop` at the end of debugging sessions.

### Console-Tail Only Captures New Messages

The `console-tail` command only captures console messages that occur AFTER the command starts. Historical messages are not shown.

**Pattern for effective console monitoring:**
```bash
# Start monitoring FIRST
scripts/chromectl.py console-tail --id $TARGET --for 30 &

# THEN trigger actions that generate console output
scripts/chromectl.py eval --id $TARGET -e "myFunction()"
```

### Multiple Chrome Instances

Can run multiple debugging instances on different ports:

```bash
# Instance 1
scripts/chromectl.py start --port 9222

# Instance 2 (different port and profile)
scripts/chromectl.py start --port 9223 --user-data-dir ~/chromectl-debug2

# Use instance 2
scripts/chromectl.py --port 9223 list
```

### Extract Target IDs

Target IDs are needed for eval, screenshot, and console-tail commands:

```bash
# Extract ID from open command
TARGET=$(scripts/chromectl.py open https://example.com | jq -r .id)

# Or list all targets and manually select
scripts/chromectl.py list
```

## Resources

### scripts/chromectl.py

The main Chrome debugging utility. A self-contained Python script using uv for dependency management (aiohttp). Communicates with Chrome via the DevTools Protocol.

Execute from skill directory:
```bash
scripts/chromectl.py <command> [options]
```

### references/chromectl-reference.md

Complete command reference with all options, examples, and troubleshooting guidance. Consult this for:
- Detailed command syntax
- Advanced usage patterns
- Troubleshooting connection issues
- Technical details about CDP

## Quick Reference

**Common command patterns:**

```bash
# Start debugging session
scripts/chromectl.py start                    # Visible window (collaborative)
scripts/chromectl.py start --headless         # Background (automation)

# Get target ID
TARGET=$(scripts/chromectl.py open URL | jq -r .id)

# Monitor console
scripts/chromectl.py console-tail --id $TARGET --for 30

# Capture screenshot
scripts/chromectl.py screenshot --id $TARGET -o file.png

# Inspect page state
scripts/chromectl.py eval --id $TARGET -e "expression"

# Always clean up
scripts/chromectl.py stop
```

**Troubleshooting:**

```bash
# Verify Chrome is running
lsof -i :9222

# List all targets
scripts/chromectl.py list

# Test CDP connection
curl http://localhost:9222/json
```
