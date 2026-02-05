---
version: 1.0.0
name: dev-browser
description: Integration guide for SawyerHood/dev-browser, a Claude Code plugin for browser automation. This skill enables agents to research, test web UIs, and interact with web applications using a headless browser.
location: user
---

# Dev Browser Integration

## Overview

`dev-browser` is a plugin for Claude Code that provides browser automation capabilities. It allows the agent to control a web browser to navigate pages, interact with elements, take screenshots, and extract information. This is essential for:
- Web research beyond simple text fetching
- Testing web applications (e.g., verifying UI changes)
- Interacting with dynamic web pages (SPA, JavaScript-heavy sites)
- Automating browser-based workflows

## Prerequisites

### Required Tools

- **Claude Code CLI**
- **Bun Runtime** (v1.0 or later)
  ```bash
  curl -fsSL https://bun.sh/install | bash
  ```

### Installation

To install the `dev-browser` plugin in Claude Code:

1.  **Add the Marketplace** (if not already added):
    ```bash
    /plugin marketplace add sawyerhood/dev-browser
    ```

2.  **Install the Plugin**:
    ```bash
    /plugin install dev-browser@sawyerhood/dev-browser
    ```

3.  **Restart Claude Code**:
    You must restart the Claude Code CLI for the changes to take effect.

## Usage Guide

Once installed, the `dev-browser` exposes tools that the agent can use. You generally do not need to call specific tool names manually; instead, you prompt the agent with natural language.

### Common Prompts

**Navigation & Research:**
- "Go to https://example.com and summarize the pricing model."
- "Search Google for 'latest React patterns' and list the top 3 results."
- "Navigate to the local server at http://localhost:3000 and tell me what you see."

**Interaction:**
- "Click on the 'Sign Up' button."
- "Type 'hello world' into the search box and press Enter."
- "Take a screenshot of the homepage."

**Testing/Verification:**
- "Verify that the login form shows an error when I submit an empty password."
- "Check if the navigation bar is responsive on mobile view."

### Tool Capabilities

While the agent handles the specific tool calls, understanding the underlying capabilities helps in crafting better prompts:

- **Navigation**: `goto(url)`, `back()`, `forward()`
- **Interaction**: `click(selector)`, `type(selector, text)`, `press(key)`
- **Extraction**: `content()`, `screenshot()`
- **Evaluation**: `evaluate(javascript)` - Run custom JS on the page

## Best Practices

### For Agents
1.  **Be Specific with Selectors**: When asking to click or type, describe the element clearly (e.g., "the blue 'Submit' button", "the input field labeled 'Email'").
2.  **Wait for Content**: Dynamic pages may load slowly. If an element isn't found, ask the agent to wait or check for a loading state.
3.  **Use Screenshots**: Visual verification is often better than text descriptions for UI layout issues.
4.  **Local Development**: Use `http://localhost:PORT` to test local applications. Ensure the server is running before asking the browser to visit.

### Troubleshooting

**"Browser not found" / "Command failed"**
- Ensure Bun is installed and in your PATH.
- Verify the plugin is installed via `/plugin list`.
- Restart Claude Code.

**"Element not found"**
- The page might not be fully loaded. Ask to wait or use a more robust selector description.
- The element might be inside an iframe or shadow DOM (mention this if known).

**Connection Refused (Localhost)**
- Ensure your local dev server is running (`npm run dev`, etc.).
- Check if the port is correct.

## Reference
- **GitHub Repository**: https://github.com/SawyerHood/dev-browser
- **Marketplace**: `sawyerhood/dev-browser`
