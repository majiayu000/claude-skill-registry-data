---
name: agent-browser
description: Operate an agent-browser CLI for auditable navigation, extraction, screenshots, and UI checks.
category: web
aliases:
- browser
triggers:
- Navigate to this URL
- Take a screenshot
- Extract data from a webpage
- Fill out a web form
- Click a button on a page
keywords:
- browser
- automation
- navigation
- scrape
- screenshot
- click
- type
- extract
dependencies:
- optional:agent-browser
risk: medium
version: 1.0.0
source: custom
enabled: true
capabilities:
- agent-browser
- web
inputs:
- task
- context
outputs:
- result
- report
lifecycle: enabled
author: Mr-Nobody-Anonymous
tags:
- agent
- automation
- browser
- navigation
- scrape
- web
compatibility:
  claude-code: '>=1.0'
  skillhub: '*'
  cursor: '>=0.40'
  codex: '*'
network_access: false
filesystem_access: read
credential_access: false
destructive_operations: false
---

# Agent Browser

## Purpose
Operate a headless browser CLI (agent-browser) for AI agents to interact with websites.
The skill enables navigation, clicking, typing, screenshot capture, and structured data
extraction with full auditability.

## When to Use
- The user wants to interact with a website programmatically
- Screenshot or visual verification is needed
- Form submission or data extraction is required
- Accessibility tree inspection is needed

## When NOT to Use
- The website blocks automated access (check robots.txt first)
- The action requires human interaction for CAPTCHAs
- The task is read-only but the website requires login

## Capabilities
- Navigate to URLs with configurable viewport and headers
- Click, type, scroll, and hover interactions
- Screenshot capture (full page or viewport)
- Accessibility tree extraction for LLM-readable content
- DOM extraction with CSS selectors
- Wait for elements, network idle, or custom conditions
- Proxy and authentication support

## Inputs
- `url` (required) — target URL
- `action` (required) — one of: navigate, click, type, screenshot, extract, wait
- `selector` (optional) — CSS selector for element targeting
- `value` (optional) — text to type or other action parameter
- `timeout` (optional, default 30s)

## Workflow
1. **Validate** — URL format, selector validity, required tools available
2. **Execute** — Run the browser action via agent-browser CLI
3. **Capture** — Store output (screenshot path, extracted text, error)
4. **Report** — Present results to user

## Tools
- `agent-browser` CLI
- Optional: screenshot storage, file system for outputs

## Examples
**User:** "Take a screenshot of example.com"
**Response:** Navigating to example.com... Screenshot saved to `screenshots/example-2026-02-09.png`

**User:** "Click the login button and extract the form fields"
**Response:** Clicked #login-btn. Extracted form fields: username, password, remember_me

## Safety
- Never store credentials in logs
- Respect robots.txt and terms of service
- Confirm before submitting forms or making changes

## Source
Auto-generated from openclawskills.net description.

## Notes
Maintained as part of canonical web category.
