---
name: playwright-cli-archived
description: Automates browser interactions for web testing, form filling, screenshots, and data extraction. Use when the user needs to navigate websites, interact with web pages, fill forms, take screenshots, test web applications, or extract information from web pages.
allowed-tools: Bash(playwright-cli:*)
version: 2.1.1
---

# Browser Automation with playwright-cli

## Quick start

```bash
playwright-cli --config profiles/chromium.json open https://example.com
playwright-cli snapshot
playwright-cli click e3
playwright-cli fill e5 "user@example.com"
playwright-cli press Enter
```

**Note on Blazor apps**: For Interactive Server render mode, Playwright auto-waits for the SignalR circuit. The next command after an interaction (like click) will wait for the server to process. See [BLAZOR_TESTING.md](references/BLAZOR_TESTING.md) for timing strategies.

## Path Resolution

All file paths referenced in this skill (including profiles, references, and scripts) are resolved relative to the skill's root directory at runtime. This ensures portability when the skill is published to different locations such as:

- Windows: `%USERPROFILE%\.copilot\skills\playwright-cli`
- Windows: `%USERPROFILE%\.claude\skills\playwright-cli`
- Windows: `%USERPROFILE%\.codex\skills\playwright-cli`
- WSL: `~/.copilot/skills/playwright-cli` (if WSL is available)
- WSL: `~/.claude/skills/playwright-cli` (if WSL is available)
- WSL: `~/.codex/skills/playwright-cli` (if WSL is available)

The playwright-cli tool automatically resolves relative paths based on its execution context, maintaining compatibility across publishing destinations.

## Core workflow

1. **Navigate**: `playwright-cli --config profiles/chromium.json open https://example.com`
2. **Interact**: Use element references from the snapshot (e.g., `e3`, `e5`)
3. **Inspect**: Re-snapshot after significant changes to see the DOM
4. **Always profile-first**: Use explicit profiles from `profiles/` (default: `chromium.json`)
5. **Mobile-first testing**: Start with device profiles (`iphone15`, `pixel7`) for responsive validation

For conventional folder structure to manage artifacts (screenshots, logs, scripts, .playwright-cli), see [FOLDER_STRUCTURE.md](references/FOLDER_STRUCTURE.md).

## When to use

- **POC/Exploratory**: Manual testing, debugging, form filling, data extraction
- **Production**: Use E2E scripts instead (Playwright Test Framework)
- **Hybrid**: Explore with CLI, then convert to scripts for automation. Use this approach when you need repeatable E2E validations with automated CLI execution but manual verification is acceptable—ideal for prototyping, quick validations, or scenarios where full test framework setup is overkill but some automation is required (e.g., <30 min tasks, solo development, or pre-CI checks). Transition to production scripts if repeatability exceeds 3 runs or requires programmatic assertions. See [HYBRID_TEMPLATE.md](references/HYBRID_TEMPLATE.md) for a reusable bash script example.

For detailed decision guidance, see [BOUNDARIES.md](references/BOUNDARIES.md).

## Command reference

All Playwright CLI commands organized by type:

- [**COMMANDS.md**](references/COMMANDS.md) - Core, navigation, keyboard, mouse, save, tabs, DevTools
- [**CONFIGURATION.md**](references/CONFIGURATION.md) - Profiles, HTTPS/SSL, sessions, config manager script
- [**WORKFLOWS.md**](references/WORKFLOWS.md) - Form submission, multi-tab, debugging, responsive testing examples
- [**BLAZOR_TESTING.md**](references/BLAZOR_TESTING.md) - Blazor Interactive Server with SignalR, readiness signals, best practices

## E2E scripts & integration

Playwright CLI complements code-based E2E test scripts. When to integrate:

- **Exploratory Testing**: Use CLI for manual flows before scripting
- **Debugging Failures**: Reproduce script issues interactively
- **Prototyping**: Quick validations or data setup
- **CI/CD**: Pre-checks or parallel sessions alongside suites

See [**INTEGRATION.md**](references/INTEGRATION.md) for 10 solid workflows, best practices, and hybrid approach patterns.

## Glossary & boundaries

- [**GLOSSARY.md**](references/GLOSSARY.md) - Domain terminology (assertions, E2E, flaky tests, etc.)
- [**BOUNDARIES.md**](references/BOUNDARIES.md) - POC vs Production decision matrix and rules
